#ifndef TABLE_H
#define TABLE_H

#include <Python.h>
#include "column.h"

typedef struct {
    PyObject_HEAD
    Py_ssize_t width;
    Column **columns;
} Table;

int TableType_init(PyTypeObject *tabletype);

#endif
