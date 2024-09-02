#include <Python.h>
#include <math.h>

static PyObject* factorize(PyObject* self, PyObject* args) {
    long num;
    if (!PyArg_ParseTuple(args, "l", &num)) {
        return NULL;
    }

    if (num <= 0) {
        PyErr_SetString(PyExc_ValueError, "Input must be a positive integer");
        return NULL;
    }

    PyObject* factor_list = PyList_New(0);

    while (num % 2 == 0) {
        PyList_Append(factor_list, PyLong_FromLong(2));
        num /= 2;
    }

    for (long i = 3; i * i <= num; i += 2) {
        while (num % i == 0) {
            PyList_Append(factor_list, PyLong_FromLong(i));
            num /= i;
        }
    }

    if (num > 2) {
        PyList_Append(factor_list, PyLong_FromLong(num));
    }

    return factor_list;
}

static PyMethodDef methods[] = {
    {"factorize", factorize, METH_VARARGS, "Factorize a number"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "factorizer",
    NULL,
    -1,
    methods
};

PyMODINIT_FUNC PyInit_factorizer(void) {
    return PyModule_Create(&module);
}
