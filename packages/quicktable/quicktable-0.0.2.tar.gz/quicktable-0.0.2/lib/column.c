#include "column.h"


static PyObject *
PyUnicodeCopy(PyObject *object) {
    return PyUnicode_FromKindAndData(
        PyUnicode_KIND(object),
        PyUnicode_DATA(object),
        PyUnicode_GET_LENGTH(object)
    );
}


void Column_dealloc(Column *column) {
    Py_XDECREF(column->name);
    Py_XDECREF(column->type);
    free(column);
}


Column *Column_new(PyObject *column_schema) {
    Column* column;
    PyObject *name, *type;

    if (PySequence_Check(column_schema) == 0 || PySequence_Length(column_schema) != 2) {
        PyErr_SetString(PyExc_TypeError, "Column definition must be a sequence containing two items.");
        return NULL;
    }

    column = (Column *)malloc(sizeof(Column));
    if (column == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Failed to initialise column.");
        return NULL;
    }

    column->name = NULL;
    column->type = NULL;

    name = PySequence_GetItem(column_schema, 0);
    if (name == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Failed to initialise column.");
        Column_dealloc(column);
        return NULL;
    }

    type = PySequence_GetItem(column_schema, 1);
    if (type == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Failed to initialise column.");
        Column_dealloc(column);
        Py_DECREF(name);
        return NULL;
    }

    if (!PyUnicode_Check(name)) {
        PyErr_SetString(PyExc_TypeError, "Column name must be a string.");
        Py_DECREF(name);
        Py_DECREF(type);
        Column_dealloc(column);
        return NULL;
    }

    if (!PyUnicode_Check(type) || PyUnicode_CompareWithASCIIString(type, "string") != 0) {
        PyErr_SetString(PyExc_TypeError, "Column type must be one of quicktable.Table.COLUMN_TYPES.");
        Py_DECREF(name);
        Py_DECREF(type);
        Column_dealloc(column);
        return NULL;
    }

    column->name = PyUnicodeCopy(name);
    column->type = PyUnicodeCopy(type);

    Py_DECREF(name);
    Py_DECREF(type);

    if (column->name == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Failed to initialise column.");
        Column_dealloc(column);
        return NULL;
    }

    if (column->type == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Failed to initialise column.");
        Column_dealloc(column);
        return NULL;
    }

    return column;
}
