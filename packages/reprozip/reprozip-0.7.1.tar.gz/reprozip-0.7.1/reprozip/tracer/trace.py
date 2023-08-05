# Copyright (C) 2014-2015 New York University
# This file is part of ReproZip which is released under the Revised BSD License
# See file LICENSE for full license details.

"""Tracing logic for reprozip.

This module contains the :func:`~reprozip.tracer.tracer.tracer` function that
invokes the C tracer (_pytracer) to build the SQLite trace file, and the
generation logic for the config YAML file.
"""

from __future__ import unicode_literals

import heapq
from itertools import count
import logging
import os
import platform
from rpaths import Path
import sqlite3

from reprozip import __version__ as reprozip_version
from reprozip import _pytracer
from reprozip.common import File, InputOutputFile, load_config, save_config, \
    FILE_READ, FILE_WRITE, FILE_WDIR, FILE_LINK
from reprozip.orderedset import OrderedSet
from reprozip.tracer.linux_pkgs import magic_dirs, system_dirs, \
    identify_packages
from reprozip.utils import PY3, izip, iteritems, itervalues, listvalues, \
    unicode_, flatten, UniqueNames, hsize, find_all_links


class TracedFile(File):
    """Override of `~reprozip.common.File` that reads stats from filesystem.
    """
    #                               read
    #                              +------+
    #                              |      |
    #                read          v      +   write
    # (init) +------------------> ONLY_READ +-------> READ_THEN_WRITTEN
    #        |                                           ^         +
    #        |                                           |         |
    #        +-------> WRITTEN +--+                      +---------+
    #          write    ^         |                      read, write
    #                   |         |
    #                   +---------+
    #                   read, write
    READ_THEN_WRITTEN = 0
    ONLY_READ = 1
    WRITTEN = 2

    what = None

    def __init__(self, path):
        path = Path(path)
        size = None
        if path.exists():
            if path.is_link():
                self.comment = "Link to %s" % path.read_link(absolute=True)
            elif path.is_dir():
                self.comment = "Directory"
            else:
                size = path.size()
                self.comment = hsize(size)
        File.__init__(self, path, size)

    def read(self):
        if self.what is None:
            self.what = TracedFile.ONLY_READ

    def write(self):
        if self.what is None:
            self.what = TracedFile.WRITTEN
        elif self.what == TracedFile.ONLY_READ:
            self.what = TracedFile.READ_THEN_WRITTEN


def get_files(conn):
    """Find all the files used by the experiment by reading the trace.
    """
    files = {}
    access_files = [set()]

    # Finds run timestamps, so we can sort input/output files by run
    proc_cursor = conn.cursor()
    executions = proc_cursor.execute(
            '''
            SELECT timestamp
            FROM processes
            WHERE parent ISNULL
            ORDER BY id;
            ''')
    run_timestamps = [r_timestamp for r_timestamp, in executions][1:]
    proc_cursor.close()

    # Adds dynamic linkers
    for libdir in (Path('/lib'), Path('/lib64')):
        if libdir.exists():
            for linker in libdir.listdir('*ld-linux*'):
                for filename in find_all_links(linker, True):
                    if filename not in files:
                        f = TracedFile(filename)
                        f.read()
                        files[f.path] = f

    # Adds executed files
    exec_cursor = conn.cursor()
    executed_files = exec_cursor.execute(
            '''
            SELECT name, timestamp
            FROM executed_files
            ORDER BY timestamp;
            ''')
    executed = set()
    # ... and opened files
    open_cursor = conn.cursor()
    opened_files = open_cursor.execute(
            '''
            SELECT name, mode, timestamp
            FROM opened_files
            ORDER BY timestamp;
            ''')
    # Loop on both lists at once
    rows = heapq.merge(((r[1], 'exec', r) for r in executed_files),
                       ((r[2], 'open', r) for r in opened_files))
    for ts, event_type, data in rows:
        if event_type == 'exec':
            r_name, r_timestamp = data
            r_mode = FILE_READ
        else:  # event_type == 'open'
            r_name, r_mode, r_timestamp = data
        r_name = Path(r_name)

        if event_type == 'exec':
            executed.add(r_name)

        # Stays on the current run
        while run_timestamps and r_timestamp > run_timestamps[0]:
            del run_timestamps[0]
            access_files.append(set())

        # Adds symbolic links as read files
        for filename in find_all_links(r_name.parent if r_mode & FILE_LINK
                                       else r_name, False):
            if filename not in files:
                f = TracedFile(filename)
                f.read()
                files[f.path] = f
        # Go to final target
        if not r_mode & FILE_LINK:
            r_name = r_name.resolve()
        if r_name not in files:
            f = TracedFile(r_name)
            files[f.path] = f
        else:
            f = files[r_name]
        if r_mode & FILE_WRITE:
            f.write()
        elif r_mode & FILE_READ:
            f.read()

        # Identifies input files
        if r_name.is_file() and r_name not in executed:
            access_files[-1].add(f)
    exec_cursor.close()
    open_cursor.close()

    # Further filters input files
    inputs = [[fi.path
               for fi in lst
               # Input files are regular files,
               if fi.path.is_file() and
               # ONLY_READ,
               fi.what == TracedFile.ONLY_READ and
               # not executable,
               # FIXME : currently disabled; only remove executed files
               # not fi.path.stat().st_mode & 0b111 and
               fi.path not in executed and
               # not in a system directory
               not any(fi.path.lies_under(m)
                       for m in magic_dirs + system_dirs)]
              for lst in access_files]

    # Identify output files
    outputs = [[fi.path
                for fi in lst
                # Output files are regular files,
                if fi.path.is_file() and
                # WRITTEN
                fi.what == TracedFile.WRITTEN and
                # not in a system directory
                not any(fi.path.lies_under(m)
                        for m in magic_dirs + system_dirs)]
               for lst in access_files]

    # Displays a warning for READ_THEN_WRITTEN files
    read_then_written_files = [
            fi
            for fi in itervalues(files)
            if fi.what == TracedFile.READ_THEN_WRITTEN and
            not any(fi.path.lies_under(m) for m in magic_dirs)]
    if read_then_written_files:
        logging.warning(
                "Some files were read and then written. We will only pack the "
                "final version of the file; reproducible experiments "
                "shouldn't change their input files:\n%s",
                ", ".join(unicode_(fi.path) for fi in read_then_written_files))

    files = set(
            fi
            for fi in itervalues(files)
            if fi.what != TracedFile.WRITTEN and not any(fi.path.lies_under(m)
                                                         for m in magic_dirs))
    return files, inputs, outputs


def list_directories(conn):
    """Gets additional needed directories from the trace database.

    Returns the directories which are used as a process's working directory or
    in which files are created.
    """
    cur = conn.cursor()
    executed_files = cur.execute(
            '''
            SELECT name, mode
            FROM opened_files
            WHERE mode = ? OR mode = ?
            ''',
            (FILE_WDIR, FILE_WRITE))
    executed_files = ((Path(n).resolve(), m) for n, m in executed_files)
    # If WDIR, the name is a folder that was used as working directory
    # If WRITE, the name is a file that was written to; its directory must
    # exist
    result = set(TracedFile(n if m == FILE_WDIR else n.parent)
                 for n, m in executed_files)
    cur.close()
    return result


def merge_files(newfiles, newpackages, oldfiles, oldpackages):
    """Merges two sets of packages and files.
    """
    files = set(oldfiles)
    files.update(newfiles)

    packages = dict((pkg.name, pkg) for pkg in newpackages)
    for oldpkg in oldpackages:
        if oldpkg.name in packages:
            pkg = packages[oldpkg.name]
            # Here we build TracedFiles from the Files so that the comment
            # (size, etc) gets set
            s = OrderedSet(TracedFile(fi.path) for fi in oldpkg.files)
            s.update(pkg.files)
            oldpkg.files = list(s)
            packages[oldpkg.name] = oldpkg
        else:
            oldpkg.files = [TracedFile(fi.path) for fi in oldpkg.files]
            packages[oldpkg.name] = oldpkg
    packages = listvalues(packages)

    return files, packages


def trace(binary, argv, directory, append, verbosity=1):
    """Main function for the trace subcommand.
    """
    cwd = Path.cwd()
    if (any(cwd.lies_under(c) for c in magic_dirs + system_dirs) and
            not cwd.lies_under('/usr/local')):
        logging.warning(
                "You are running this experiment from a system directory! "
                "Autodetection of non-system files will probably not work as "
                "intended")

    # Trace directory
    if not append:
        if directory.exists():
            logging.info("Removing existing directory %s", directory)
            directory.rmtree()
        directory.mkdir(parents=True)
    else:
        if not directory.exists():
            logging.warning("--continue was specified but %s does not exist "
                            "-- creating", directory)
            directory.mkdir(parents=True)

    # Runs the trace
    database = directory / 'trace.sqlite3'
    logging.info("Running program")
    # Might raise _pytracer.Error
    c = _pytracer.execute(binary, argv, database.path, verbosity)
    if c != 0:
        if c & 0x0100:
            logging.warning("Program appears to have been terminated by "
                            "signal %d", c & 0xFF)
        else:
            logging.warning("Program exited with non-zero code %d", c)
    logging.info("Program completed")


def write_configuration(directory, sort_packages, overwrite=False):
    """Writes the canonical YAML configuration file.
    """
    database = directory / 'trace.sqlite3'

    if PY3:
        # On PY3, connect() only accepts unicode
        conn = sqlite3.connect(str(database))
    else:
        conn = sqlite3.connect(database.path)
    conn.row_factory = sqlite3.Row

    # Reads info from database
    files, inputs, outputs = get_files(conn)

    # Identifies which file comes from which package
    if sort_packages:
        files, packages = identify_packages(files)
    else:
        packages = []

    # Makes sure all the directories used as working directories are packed
    # (they already do if files from them are used, but empty directories do
    # not get packed inside a tar archive)
    files.update(d for d in list_directories(conn) if d.path.is_dir())

    # Writes configuration file
    config = directory / 'config.yml'
    distribution = platform.linux_distribution()[0:2]
    cur = conn.cursor()
    if overwrite or not config.exists():
        runs = []
        # This gets all the top-level processes (p.parent ISNULL) and the first
        # executed file for that process (sorting by ids, which are
        # chronological)
        executions = cur.execute(
                '''
                SELECT e.name, e.argv, e.envp, e.workingdir, p.exitcode
                FROM processes p
                JOIN executed_files e ON e.id=(
                    SELECT id FROM executed_files e2
                    WHERE e2.process=p.id
                    ORDER BY e2.id
                    LIMIT 1
                )
                WHERE p.parent ISNULL;
                ''')
    else:
        # Loads in previous config
        runs, oldpkgs, oldfiles = load_config(config,
                                              canonical=False,
                                              File=TracedFile)

        # Same query as previous block but only gets last process
        executions = cur.execute(
                '''
                SELECT e.name, e.argv, e.envp, e.workingdir, p.exitcode
                FROM processes p
                JOIN executed_files e ON e.id=(
                    SELECT id FROM executed_files e2
                    WHERE e2.process=p.id
                    ORDER BY e2.id
                    LIMIT 1
                )
                WHERE p.parent ISNULL
                ORDER BY p.id DESC
                LIMIT 1;
                ''')
        inputs = inputs[-1:]
        outputs = outputs[-1:]

        files, packages = merge_files(files, packages,
                                      oldfiles,
                                      oldpkgs)
    for r_name, r_argv, r_envp, r_workingdir, r_exitcode in executions:
        # Decodes command-line
        argv = r_argv.split('\0')
        if not argv[-1]:
            argv = argv[:-1]

        # Decodes environment
        envp = r_envp.split('\0')
        if not envp[-1]:
            envp = envp[:-1]
        environ = dict(v.split('=', 1) for v in envp)

        runs.append({'binary': r_name, 'argv': argv,
                     'workingdir': unicode_(Path(r_workingdir)),
                     'architecture': platform.machine().lower(),
                     'distribution': distribution,
                     'hostname': platform.node(),
                     'system': [platform.system(), platform.release()],
                     'environ': environ,
                     'uid': os.getuid(),
                     'gid': os.getgid(),
                     'signal' if r_exitcode & 0x0100 else 'exitcode':
                         r_exitcode & 0xFF})

    cur.close()
    conn.close()

    inputs_outputs = compile_inputs_outputs(runs, inputs, outputs)

    save_config(config, runs, packages, files, reprozip_version,
                inputs_outputs)

    print("Configuration file written in {0!s}".format(config))
    print("Edit that file then run the packer -- "
          "use 'reprozip pack -h' for help")


def compile_inputs_outputs(runs, inputs, outputs):
    """Gives names to input/output files and creates InputOutputFile objects.
    """
    # {path: (run_nb, arg_nb) or None}
    runs_with_file = {}
    # run_nb: number_of_file_arguments
    nb_file_args = []
    # {path: [runs]}
    readers = {}
    writers = {}

    for run_nb, run, in_files, out_files in izip(count(), runs,
                                                 inputs, outputs):
        # List which runs read or write each file
        for p in in_files:
            readers.setdefault(p, []).append(run_nb)
        for p in out_files:
            writers.setdefault(p, []).append(run_nb)

        # Locate files that appear on a run's command line
        files_set = set(in_files) | set(out_files)
        nb_files = 0
        for arg_nb, arg in enumerate(run['argv']):
            p = Path(run['workingdir'], arg).resolve()
            if p in files_set:
                nb_files += 1
                if p not in runs_with_file:
                    runs_with_file[p] = run_nb, arg_nb
                elif runs_with_file[p] is not None:
                    runs_with_file[p] = None
        nb_file_args.append(nb_files)

    file_names = {}
    make_unique = UniqueNames()

    for fi in flatten(2, (inputs, outputs)):
        # If it appears in at least one of the command-lines
        if fi in runs_with_file:
            # If it only appears once in the command-lines
            if runs_with_file[fi] is not None:
                run_nb, arg_nb = runs_with_file[fi]
                parts = []
                # Run number, if there are more than one runs
                if len(runs) > 1:
                    parts.append(run_nb)
                # Argument number, if there are more than one file arguments
                if nb_file_args[run_nb] > 1:
                    parts.append(arg_nb)
                file_names[fi] = make_unique(
                        'arg%s' % '_'.join('%s' % s for s in parts))
            else:
                file_names[fi] = make_unique('arg_%s' % fi.unicodename)
        else:
            file_names[fi] = make_unique(fi.unicodename)

    return dict((n, InputOutputFile(p, readers.get(p, []), writers.get(p, [])))
                for p, n in iteritems(file_names))
