#include <Python.h>
#include <table.h>


extern PyTypeObject TableType;


static PyModuleDef quicktablemodule = {
    PyModuleDef_HEAD_INIT,
    "quicktable",
    "Pythonic representation of tabular data.",
    -1,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC PyInit_quicktable(void) {
    PyObject *module;

    TableType_init(&TableType);

    if (PyType_Ready(&TableType) < 0)
        return NULL;

    module = PyModule_Create(&quicktablemodule);
    if (module == NULL)
        return NULL;

    Py_INCREF(&TableType);
    PyModule_AddObject(module, "Table", (PyObject *)&TableType);

    return module;
}
