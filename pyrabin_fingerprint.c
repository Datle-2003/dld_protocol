#define PY_SSIZE_T_CLEAN
#include <Python.h>

// fingerprint calculation
static inline int fls32(uint32_t x)
{
	int r = 32;

	if (!x)
		return 0;
	if (!(x & 0xffff0000u)) {
		x <<= 16;
		r -= 16;
	}
	if (!(x & 0xff000000u)) {
		x <<= 8;
		r -= 8;
	}
	if (!(x & 0xf0000000u)) {
		x <<= 4;
		r -= 4;
	}
	if (!(x & 0xc0000000u)) {
		x <<= 2;
		r -= 2;
	}
	if (!(x & 0x80000000u)) {
		x <<= 1;
		r -= 1;
	}
	return r;
}

static inline int fls64 (uint64_t v)
{
  uint32_t h;
  if ((h = v >> 32))
    return 32 + fls32 (h);
  else
    return fls32 ((uint32_t) v);
}


uint32_t rabinFingerprint(uint64_t data, uint64_t polynomial) {
    int k = fls64 (polynomial) - 1;
	polynomial <<= 63 - k;// shift the polynomial to the highest bit position
    if (data) {
		if (data & ((uint64_t) 1) << 63)
			data ^= polynomial;  
		for (int i = 62; i >= k; i--)
			if (data & ((uint64_t) 1) << i) {
				data ^= polynomial >> (63 - i);
			}
	}

    return (uint32_t) data; // result is the lower 32 bits
}

// Python bindings
static PyObject *pyrabin_fingerprint(PyObject *self, PyObject *args) {
    uint64_t data;
    uint64_t polynomial;
    if (!PyArg_ParseTuple(args, "OO", &data, &polynomial)) {
        return NULL;
    }
    uint32_t fingerprint = rabinFingerprint(data, polynomial);
    return PyLong_FromUnsignedLongLong(fingerprint);
}

PyMODINIT_FUNC PyInit_pyrabin_fingerprint() {
    static PyMethodDef methods[] = {
        {"rabin_fingerprint", pyrabin_fingerprint, METH_VARARGS, "Calculate Rabin fingerprint"},
        {NULL, NULL, 0, NULL}
    };
    static struct PyModuleDef pyrabin_fingerprint = {
        PyModuleDef_HEAD_INIT,
        "pyrabin_fingerprint",
        "Rabin fingerprint calculation",
        -1,
        methods
    };
    return PyModule_Create(&pyrabin_fingerprint);
}