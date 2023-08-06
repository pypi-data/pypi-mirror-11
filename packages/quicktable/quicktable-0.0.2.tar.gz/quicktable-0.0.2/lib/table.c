#include "table.h"


static PyObject *
PyUnicodeCopy(PyObject *object) {
    return PyUnicode_FromKindAndData(
        PyUnicode_KIND(object),
        PyUnicode_DATA(object),
        PyUnicode_GET_LENGTH(object)
    );
}


static void Table_dealloc(Table *self) {
    Py_ssize_t i;
    for (i = 0; i < self->width; i++)
        Column_dealloc(self->columns[i]);

    free(self->columns);
    Py_TYPE(self)->tp_free((PyObject *)self);
}


static PyObject *Table_new(PyTypeObject *type, PyObject *args, PyObject *kwargs) {
    Table *self;
    self = (Table *)type->tp_alloc(type, 0);
    self->width = 0;
    return (PyObject *)self;
}


static int Table_columns_init(Table *self, PyObject *schema) {
    Column *column;
    Py_ssize_t i, length;
    PyObject *element;

    // Check if columns is a sequence
    if (PySequence_Check(schema) == 0) {
        PyErr_SetString(PyExc_TypeError, "Schema definition must be a sequence.");
        return -1;
    }

    length = PySequence_Length(schema);

    self->columns = (Column **)malloc(sizeof(Column *));
    if (self->columns == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Failed to initialise column.");
        return -1;
    }

    for (i = 0; i < length; i++) {
        element = PySequence_GetItem(schema, i);
        if (element == NULL) {
            PyErr_SetString(PyExc_MemoryError, "Failed to initialise column.");
            return -1;
        }

        column = Column_new(element);
        if (column == NULL)
            return -1;

        self->width++;
        Py_DECREF(element);

        self->columns[i] = column;
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


PyObject *
Table_getcolumnnames(Table *self, void *closure) {
    Py_ssize_t i;
    PyObject *names, *name;

    names = PyTuple_New(self->width);
    if (names == NULL)
        return NULL;

    for (i = 0; i < self->width; i++) {
        name = PyUnicodeCopy(self->columns[i]->name);
        if (name == NULL) {
            Py_DECREF(names);
            return NULL;
        }
        PyTuple_SetItem(names, i, name);
    }

    return names;
}


PyObject *
Table_getcolumntypes(Table *self, void *closure) {
    PyObject *types = PyTuple_New(self->width);
    if (types == NULL)
        return NULL;

    Py_ssize_t i;
    for (i = 0; i < self->width; i++) {
        PyObject *type = PyUnicodeCopy(self->columns[i]->type);
        if (type == NULL) {
            Py_DECREF(types);
            return NULL;
        }
        PyTuple_SetItem(types, i, type);
    }

    return types;
}


static PyObject *
Table_getschema(Table *self, void *closure) {
    PyObject *schema, *column, *item;
    Py_ssize_t i;

    schema = PyList_New(self->width);
    if (schema == NULL)
        return NULL;

    for (i = 0; i < self->width; i++) {
        column = PyTuple_New(2);
        if (column == NULL) {
            Py_DECREF(schema);
            return NULL;
        }

        item = PyUnicodeCopy(self->columns[i]->name);
        if (item == NULL) {
            Py_DECREF(schema);
            return NULL;
        }
        PyTuple_SetItem(column, 0, item);

        item = PyUnicodeCopy(self->columns[i]->type);
        if (item == NULL) {
            Py_DECREF(schema);
            return NULL;
        }
        PyTuple_SetItem(column, 1, item);

        PyList_SetItem(schema, i, column);
    }

    return schema;
}


static PyGetSetDef Table_getseters[] = {
    {"column_names", (getter)Table_getcolumnnames, NULL, "Tuple of names of columns.", NULL},
    {"column_types", (getter)Table_getcolumntypes, NULL, "Tuple of types of columns.", NULL},
    {"schema", (getter)Table_getschema, NULL, "Schema of the table.", NULL},
    {NULL}
};


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
    Table_getseters,  // tp_getset
    0,  // tp_base
    0,  // tp_dict
    0,  // tp_descr_get
    0,  // tp_descr_set
    0,  // tp_dictoffset
    (initproc)Table_init,  // tp_init
    0,  // tp_alloc
    Table_new  // tp_new
};


int TableType_init(PyTypeObject *tabletype) {
    PyObject *valid_types;
    PyObject *type;

    if ((valid_types = PyTuple_New(1)) == NULL)
        return -1;

    if ((type = PyUnicode_FromString("string")) == NULL) {
        Py_DECREF(valid_types);
        return -1;
    }
    PyTuple_SetItem(valid_types, 0, type);

    if ((tabletype->tp_dict = PyDict_New()) == NULL) {
        Py_DECREF(valid_types);
        return -1;
    }

    if ((PyDict_SetItemString(tabletype->tp_dict, "COLUMN_TYPES", valid_types)) != 1) {
        Py_DECREF(valid_types);
        return -1;
    }

    return 0;
}
