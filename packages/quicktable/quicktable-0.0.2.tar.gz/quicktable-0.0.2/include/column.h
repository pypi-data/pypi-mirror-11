#ifndef COLUMN_H
#define COLUMN_H

#include <Python.h>

typedef struct {
    PyObject *name;
    PyObject *type;
} Column;

Column *Column_new(PyObject *);
void Column_dealloc(Column *);

#endif
