#include <Python.h>
#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <PCO_errt.h>

// Implement the C function PCO_GetErrorText
static PyObject *error_text(PyObject *self, PyObject *args)
{
		DWORD dwerr, dwlen;
		char buf[100] = {0};
		PyObject *result = NULL;
		if(!PyArg_ParseTuple(args, "k", &dwerr))
			return NULL;
		dwlen = sizeof(buf);
		PCO_GetErrorText(dwerr, buf, dwlen);
		result = Py_BuildValue("s", buf);
		return result;
}

static PyMethodDef errorTextMethods[] =
{
		{"getText", error_text, METH_VARARGS,
				"str errText = getTExt(int errNumber)\n"
				"The function returns the errortext from "
				"PCO_GetErrorText in PCO_errt.h"},
		{NULL, NULL, 0, NULL}
};

static PyModuleDef errorTextModule =
{
		PyModuleDef_HEAD_INIT,
		"pcoError",
		"Insert the docstring here.",
		-1,
		errorTextMethods
};

PyMODINIT_FUNC PyInit_pcoError(void)
{
	return PyModule_Create(&errorTextModule);
};
