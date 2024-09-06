#include <Python.h>

// Function to get the memory address of an object
PyObject* pointer(PyObject* self, PyObject* obj) {
    char address[32];
    snprintf(address, sizeof(address), "%p", obj);
    
    // Remove "0x" if present
    if (strncmp(address, "0x", 2) == 0) {
        memmove(address, address + 2, strlen(address) - 1);
    }
    
    return PyUnicode_FromString(address);
}

// Function to get the value at a memory address
PyObject* value(PyObject* self, PyObject* args) {
    const char* address_str;
    if (!PyArg_ParseTuple(args, "s", &address_str)) {
        return NULL;
    }
    
    // Remove "0x" if present
    if (strncmp(address_str, "0x", 2) == 0) {
        address_str += 2;
    }
    
    unsigned long long address;
    if (sscanf(address_str, "%llx", &address) != 1) {
        PyErr_SetString(PyExc_ValueError, "Invalid memory address format");
        return NULL;
    }
    
    PyObject* obj = (PyObject*)address;
    
    if (!PyObject_IsInstance(obj, (PyObject*)&PyBaseObject_Type)) {
        PyErr_SetString(PyExc_ValueError, "Invalid memory address or object");
        return NULL;
    }

    // Add a warning about potential security risks
     PyErr_WarnEx(PyExc_RuntimeWarning, "Accessing memory directly can be dangerous and may crash the program", 1);
    
    Py_INCREF(obj);
    return obj;
}

// Method definitions for the module
static PyMethodDef PointerMethods[] = {
    {"pointer", (PyCFunction)pointer, METH_O, "Get memory location of an object"},
    {"value", (PyCFunction)value, METH_VARARGS, "Get value stored at a memory address"},
    {NULL, NULL, 0, NULL}  // Sentinel
};

// Module definition
static struct PyModuleDef pointermodule = {
    PyModuleDef_HEAD_INIT,
    "pointers",  // Module name
    "Module for memory operations",
    -1,
    PointerMethods
};

// Module initialization function
PyMODINIT_FUNC PyInit_pointers(void) {
    return PyModule_Create(&pointermodule);
}
