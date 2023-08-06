#include "table.h"
#include "column.h"


static void Table_dealloc(Table *self) {
    Py_TYPE(self)->tp_free((PyObject *)self);
}


static PyObject *Table_new(PyTypeObject *type, PyObject *args, PyObject *kwargs) {
    Table *self;
    self = (Table *)type->tp_alloc(type, 0);
    return (PyObject *)self;
}


static int Table_columns_init(Table *self, PyObject *columns) {
    // Check if columns is a sequence
    if (PySequence_Check(columns) == 0) {
        PyErr_SetString(PyExc_TypeError, "Schema definition must be a sequence.");
        return -1;
    }

    Py_ssize_t length = PySequence_Length(columns);

    Py_ssize_t i;
    PyObject *column;
    for (i = 0; i < length; i++) {
        column = PySequence_ITEM(columns, i);
        if (Column_init(column) != 0) {
            Py_DECREF(column);
            return -1;
        }
        printf("hello");
    }

    return 0;
}


static int Table_init(Table *self, PyObject *args, PyObject *kwargs) {
    PyObject *columns = NULL;

    if (!PyArg_ParseTuple(args, "O", &columns))
        return -1;

    if (Table_columns_init(self, columns) == -1)
        return -1;

    return 0;
}


PyTypeObject TableType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "quicktable.Table",  // tp_name
    sizeof(Table),  // tp_basicsize
    0,  // tp_itemsize
    (destructor)Table_dealloc,  // tp_dealloc
    0,  // tp_print
    0,  // tp_getattr
    0,  // tp_setattr
    0,  // tp_reserved
    0,  // tp_repr
    0,  // tp_as_number
    0,  // tp_as_sequence
    0,  // tp_as_mapping
    0,  // tp_hash
    0,  // tp_call
    0,  // tp_str
    0,  // tp_getattro
    0,  // tp_setattro
    0,  // tp_as_buffer
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,  // tp_flags
    "quicktable.Table object",  // tp_doc
    0,  // tp_traverse
    0,  // tp_clear
    0,  // tp_richcompare
    0,  // tp_weaklistoffset
    0,  // tp_iter
    0,  // tp_iternext
    0,  // tp_methods
    0,  // tp_members
    0,  // tp_getset
    0,  // tp_base
    0,  // tp_dict
    0,  // tp_descr_get
    0,  // tp_descr_set
    0,  // tp_dictoffset
    (initproc)Table_init,  // tp_init
    0,  // tp_alloc
    Table_new  // tp_new
};
