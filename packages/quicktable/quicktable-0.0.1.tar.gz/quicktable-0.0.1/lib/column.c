#include "column.h"


int Column_init(PyObject *column) {
    if (PySequence_Check(column) != 1 || PySequence_Length(column) != 2) {
        // Check if column definition is a sequence of length 2
        PyErr_SetString(PyExc_TypeError, "Column definition must be a sequence containing two items.");
        return -1;
    }

    PyObject *name = PySequence_ITEM(column, 0);
    if (name == NULL) {
        PyErr_SetString(PyExc_TypeError, "Column name must be a string.");
        return -1;
    }

    if (!PyUnicode_Check(name)) {
        PyErr_SetString(PyExc_TypeError, "Column name must be a string.");
        Py_DECREF(name);
        return -1;
    }

    return 0;
}
