#include <Python.h>

#include "database.h"
#include "tracer.h"


PyObject *Err_Base;


/**
 * Makes a C string from a Python unicode or bytes object.
 *
 * If successful, the result is a string that the caller must free().
 * Else, returns NULL.
 */
static char *get_string(PyObject *obj)
{
    if(PyUnicode_Check(obj))
    {
        const char *str;
        PyObject *pyutf8 = PyUnicode_AsUTF8String(obj);
        if(pyutf8 == NULL)
            return NULL;
#if PY_MAJOR_VERSION >= 3
        str = PyBytes_AsString(pyutf8);
#else
        str = PyString_AsString(pyutf8);
#endif
        if(str == NULL)
            return NULL;
        {
            char *ret = strdup(str);
            Py_DECREF(pyutf8);
            return ret;
        }
    }
    else if(
#if PY_MAJOR_VERSION >= 3
            PyBytes_Check(obj)
#else
            PyString_Check(obj)
#endif
            )
    {
        const char *str;
#if PY_MAJOR_VERSION >= 3
        str = PyBytes_AsString(obj);
#else
        str = PyString_AsString(obj);
#endif
        if(str == NULL)
            return NULL;
        return strdup(str);
    }
    else
        return NULL;
}


static PyObject *pytracer_execute(PyObject *self, PyObject *args)
{
    PyObject *ret;
    int exit_status;

    /* Reads arguments */
    const char *binary, *databasepath;
    char **argv;
    size_t argv_len;
    int verbosity;
    PyObject *py_binary, *py_argv, *py_databasepath;
    if(!(PyArg_ParseTuple(args, "OO!Oi",
                          &py_binary,
                          &PyList_Type, &py_argv,
                          &py_databasepath,
                          &verbosity)))
        return NULL;

    if(verbosity < 0)
    {
        PyErr_SetString(Err_Base, "verbosity should be >= 0");
        return NULL;
    }
    trace_verbosity = verbosity;

    binary = get_string(py_binary);
    if(binary == NULL)
        return NULL;
    databasepath = get_string(py_databasepath);
    if(databasepath == NULL)
        return NULL;

    /* Converts argv from Python list to char[][] */
    {
        size_t i;
        int bad = 0;
        argv_len = PyList_Size(py_argv);
        argv = malloc((argv_len + 1) * sizeof(char*));
        for(i = 0; i < argv_len; ++i)
        {
            PyObject *arg = PyList_GetItem(py_argv, i);
            char *str = get_string(arg);
            if(str == NULL)
                break;
            argv[i] = str;
        }
        if(bad)
        {
            size_t j;
            for(j = 0; j < i; ++j)
                free(argv[j]);
            free(argv);
            return NULL;
        }
        argv[argv_len] = NULL;
    }

    if(fork_and_trace(binary, argv_len, argv, databasepath, &exit_status) == 0)
    {
        ret = PyLong_FromLong(exit_status);
    }
    else
    {
        PyErr_SetString(Err_Base, "Error occurred");
        ret = NULL;
    }

    /* Deallocs argv */
    {
        size_t i;
        for(i = 0; i < argv_len; ++i)
            free(argv[i]);
        free(argv);
    }

    return ret;
}


static PyMethodDef methods[] = {
    {"execute", pytracer_execute, METH_VARARGS,
     "execute(binary, argv, databasepath, verbosity)\n"
     "\n"
     "Runs the specified binary with the argument list argv under trace and "
     "writes\nthe captured events to SQLite3 database databasepath."},
    { NULL, NULL, 0, NULL }
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "reprozip._pytracer",       /* m_name */
    "C interface to tracer",    /* m_doc */
    -1,                         /* m_size */
    methods,                    /* m_methods */
    NULL,                       /* m_reload */
    NULL,                       /* m_traverse */
    NULL,                       /* m_clear */
    NULL,                       /* m_free */
};
#endif

#if PY_MAJOR_VERSION >= 3
PyMODINIT_FUNC PyInit__pytracer(void)
#else
PyMODINIT_FUNC init_pytracer(void)
#endif
{
    PyObject *mod;

#if PY_MAJOR_VERSION >= 3
    mod = PyModule_Create(&moduledef);
#else
    mod = Py_InitModule("reprozip._pytracer", methods);
#endif
    if(mod == NULL)
    {
#if PY_MAJOR_VERSION >= 3
        return NULL;
#else
        return;
#endif
    }

    Err_Base = PyErr_NewException("_pytracer.Error", NULL, NULL);
    Py_INCREF(Err_Base);
    PyModule_AddObject(mod, "Error", Err_Base);

#if PY_MAJOR_VERSION >= 3
    return mod;
#endif
}
