
#include <stdio.h>
#include <stddef.h>
#include <stdarg.h>
#include <errno.h>
#include <sys/types.h>   /* XXX for ssize_t on some platforms */

#ifdef _WIN32
#  include <Windows.h>
#  define snprintf _snprintf
typedef __int8 int8_t;
typedef __int16 int16_t;
typedef __int32 int32_t;
typedef __int64 int64_t;
typedef unsigned __int8 uint8_t;
typedef unsigned __int16 uint16_t;
typedef unsigned __int32 uint32_t;
typedef unsigned __int64 uint64_t;
typedef SSIZE_T ssize_t;
typedef unsigned char _Bool;
#else
#  include <stdint.h>
#endif


                 #include<Python.h>
                 #ifdef PyTuple_GetItem
                 #error "Picking Python.h from pypy"
                 #endif
                 
static void _cffi_check__PyMethodDef(PyMethodDef *p)
{
  /* only to generate compile-time warnings or errors */
  { char * *tmp = &p->ml_name; (void)tmp; }
  { void * *tmp = &p->ml_meth; (void)tmp; }
  (void)((p->ml_flags) << 1);
  { char * *tmp = &p->ml_doc; (void)tmp; }
}
ssize_t _cffi_layout__PyMethodDef(ssize_t i)
{
  struct _cffi_aligncheck { char x; PyMethodDef y; };
  static ssize_t nums[] = {
    sizeof(PyMethodDef),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(PyMethodDef, ml_name),
    sizeof(((PyMethodDef *)0)->ml_name),
    offsetof(PyMethodDef, ml_meth),
    sizeof(((PyMethodDef *)0)->ml_meth),
    offsetof(PyMethodDef, ml_flags),
    sizeof(((PyMethodDef *)0)->ml_flags),
    offsetof(PyMethodDef, ml_doc),
    sizeof(((PyMethodDef *)0)->ml_doc),
    -1
  };
  return nums[i];
  /* the next line is not executed, but compiled */
  _cffi_check__PyMethodDef(0);
}

static void _cffi_check__PyObject(PyObject *p)
{
  /* only to generate compile-time warnings or errors */
  { PyTypeObject * *tmp = &p->ob_type; (void)tmp; }
  (void)((p->ob_refcnt) << 1);
}
ssize_t _cffi_layout__PyObject(ssize_t i)
{
  struct _cffi_aligncheck { char x; PyObject y; };
  static ssize_t nums[] = {
    sizeof(PyObject),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(PyObject, ob_type),
    sizeof(((PyObject *)0)->ob_type),
    offsetof(PyObject, ob_refcnt),
    sizeof(((PyObject *)0)->ob_refcnt),
    -1
  };
  return nums[i];
  /* the next line is not executed, but compiled */
  _cffi_check__PyObject(0);
}

int _cffi_const_METH_KEYWORDS(long long *out_value)
{
  *out_value = (long long)(METH_KEYWORDS);
  return (METH_KEYWORDS) <= 0;
}

int _cffi_const_METH_VARARGS(long long *out_value)
{
  *out_value = (long long)(METH_VARARGS);
  return (METH_VARARGS) <= 0;
}

PyObject * _cffi_const_PyExc_ArithmeticError(void)
{
  return (PyExc_ArithmeticError);
}

PyObject * _cffi_const_PyExc_AssertionError(void)
{
  return (PyExc_AssertionError);
}

PyObject * _cffi_const_PyExc_AttributeError(void)
{
  return (PyExc_AttributeError);
}

PyObject * _cffi_const_PyExc_BaseException(void)
{
  return (PyExc_BaseException);
}

PyObject * _cffi_const_PyExc_EOFError(void)
{
  return (PyExc_EOFError);
}

PyObject * _cffi_const_PyExc_EnvironmentError(void)
{
  return (PyExc_EnvironmentError);
}

PyObject * _cffi_const_PyExc_Exception(void)
{
  return (PyExc_Exception);
}

PyObject * _cffi_const_PyExc_FloatingPointError(void)
{
  return (PyExc_FloatingPointError);
}

PyObject * _cffi_const_PyExc_IOError(void)
{
  return (PyExc_IOError);
}

PyObject * _cffi_const_PyExc_ImportError(void)
{
  return (PyExc_ImportError);
}

PyObject * _cffi_const_PyExc_IndexError(void)
{
  return (PyExc_IndexError);
}

PyObject * _cffi_const_PyExc_KeyError(void)
{
  return (PyExc_KeyError);
}

PyObject * _cffi_const_PyExc_KeyboardInterrupt(void)
{
  return (PyExc_KeyboardInterrupt);
}

PyObject * _cffi_const_PyExc_LookupError(void)
{
  return (PyExc_LookupError);
}

PyObject * _cffi_const_PyExc_MemoryError(void)
{
  return (PyExc_MemoryError);
}

PyObject * _cffi_const_PyExc_NameError(void)
{
  return (PyExc_NameError);
}

PyObject * _cffi_const_PyExc_NotImplementedError(void)
{
  return (PyExc_NotImplementedError);
}

PyObject * _cffi_const_PyExc_OSError(void)
{
  return (PyExc_OSError);
}

PyObject * _cffi_const_PyExc_OverflowError(void)
{
  return (PyExc_OverflowError);
}

PyObject * _cffi_const_PyExc_ReferenceError(void)
{
  return (PyExc_ReferenceError);
}

PyObject * _cffi_const_PyExc_RuntimeError(void)
{
  return (PyExc_RuntimeError);
}

PyObject * _cffi_const_PyExc_StandardError(void)
{
  return (PyExc_StandardError);
}

PyObject * _cffi_const_PyExc_SyntaxError(void)
{
  return (PyExc_SyntaxError);
}

PyObject * _cffi_const_PyExc_SystemError(void)
{
  return (PyExc_SystemError);
}

PyObject * _cffi_const_PyExc_SystemExit(void)
{
  return (PyExc_SystemExit);
}

PyObject * _cffi_const_PyExc_TypeError(void)
{
  return (PyExc_TypeError);
}

PyObject * _cffi_const_PyExc_ValueError(void)
{
  return (PyExc_ValueError);
}

PyObject * _cffi_const_PyExc_ZeroDivisionError(void)
{
  return (PyExc_ZeroDivisionError);
}

PyObject * _cffi_const_Py_False(void)
{
  return (Py_False);
}

PyObject * _cffi_const_Py_None(void)
{
  return (Py_None);
}

PyObject * _cffi_const_Py_True(void)
{
  return (Py_True);
}

int _cffi_const_Py_file_input(long long *out_value)
{
  *out_value = (long long)(Py_file_input);
  return (Py_file_input) <= 0;
}

PyObject * _cffi_f_PyCFunction_New(PyMethodDef * x0, PyObject * x1)
{
  return PyCFunction_New(x0, x1);
}

PyObject * _cffi_f_PyDict_Items(PyObject * x0)
{
  return PyDict_Items(x0);
}

PyObject * _cffi_f_PyDict_New(void)
{
  return PyDict_New();
}

int _cffi_f_PyDict_SetItem(PyObject * x0, PyObject * x1, PyObject * x2)
{
  return PyDict_SetItem(x0, x1, x2);
}

int _cffi_f_PyDict_SetItemString(PyObject * x0, char const * x1, PyObject * x2)
{
  return PyDict_SetItemString(x0, x1, x2);
}

void _cffi_f_PyErr_Clear(void)
{
  PyErr_Clear();
}

int _cffi_f_PyErr_ExceptionMatches(PyObject * x0)
{
  return PyErr_ExceptionMatches(x0);
}

PyObject * _cffi_f_PyErr_Occurred(void)
{
  return PyErr_Occurred();
}

void _cffi_f_PyErr_Print(void)
{
  PyErr_Print();
}

void _cffi_f_PyErr_SetString(PyObject * x0, char const * x1)
{
  PyErr_SetString(x0, x1);
}

PyObject * _cffi_f_PyEval_EvalCode(PyObject * x0, PyObject * x1, PyObject * x2)
{
  return PyEval_EvalCode(x0, x1, x2);
}

PyObject * _cffi_f_PyEval_GetBuiltins(void)
{
  return PyEval_GetBuiltins();
}

double _cffi_f_PyFloat_AsDouble(PyObject * x0)
{
  return PyFloat_AsDouble(x0);
}

PyObject * _cffi_f_PyFloat_FromDouble(double x0)
{
  return PyFloat_FromDouble(x0);
}

PyObject * _cffi_f_PyImport_ImportModule(char const * x0)
{
  return PyImport_ImportModule(x0);
}

PyObject * _cffi_f_PyInt_FromLong(long x0)
{
  return PyInt_FromLong(x0);
}

PyObject * _cffi_f_PyIter_Next(PyObject * x0)
{
  return PyIter_Next(x0);
}

PyObject * _cffi_f_PyList_GetItem(PyObject * x0, size_t x1)
{
  return PyList_GetItem(x0, x1);
}

PyObject * _cffi_f_PyList_New(size_t x0)
{
  return PyList_New(x0);
}

int _cffi_f_PyList_SetItem(PyObject * x0, size_t x1, PyObject * x2)
{
  return PyList_SetItem(x0, x1, x2);
}

size_t _cffi_f_PyList_Size(PyObject * x0)
{
  return PyList_Size(x0);
}

long _cffi_f_PyLong_AsLong(PyObject * x0)
{
  return PyLong_AsLong(x0);
}

PyObject * _cffi_f_PyObject_Call(PyObject * x0, PyObject * x1, PyObject * x2)
{
  return PyObject_Call(x0, x1, x2);
}

int _cffi_f_PyObject_DelItem(PyObject * x0, PyObject * x1)
{
  return PyObject_DelItem(x0, x1);
}

PyObject * _cffi_f_PyObject_Dir(PyObject * x0)
{
  return PyObject_Dir(x0);
}

PyObject * _cffi_f_PyObject_GetAttrString(PyObject * x0, char const * x1)
{
  return PyObject_GetAttrString(x0, x1);
}

PyObject * _cffi_f_PyObject_GetItem(PyObject * x0, PyObject * x1)
{
  return PyObject_GetItem(x0, x1);
}

PyObject * _cffi_f_PyObject_GetIter(PyObject * x0)
{
  return PyObject_GetIter(x0);
}

int _cffi_f_PyObject_IsTrue(PyObject * x0)
{
  return PyObject_IsTrue(x0);
}

PyObject * _cffi_f_PyObject_Repr(PyObject * x0)
{
  return PyObject_Repr(x0);
}

PyObject * _cffi_f_PyObject_SetAttr(PyObject * x0, PyObject * x1, PyObject * x2)
{
  return PyObject_SetAttr(x0, x1, x2);
}

int _cffi_f_PyObject_SetItem(PyObject * x0, PyObject * x1, PyObject * x2)
{
  return PyObject_SetItem(x0, x1, x2);
}

size_t _cffi_f_PyObject_Size(PyObject * x0)
{
  return PyObject_Size(x0);
}

PyObject * _cffi_f_PyObject_Str(PyObject * x0)
{
  return PyObject_Str(x0);
}

int _cffi_f_PyRun_SimpleString(char const * x0)
{
  return PyRun_SimpleString(x0);
}

PyObject * _cffi_f_PySlice_New(PyObject * x0, PyObject * x1, PyObject * x2)
{
  return PySlice_New(x0, x1, x2);
}

char * _cffi_f_PyString_AsString(PyObject * x0)
{
  return PyString_AsString(x0);
}

PyObject * _cffi_f_PyString_FromString(char const * x0)
{
  return PyString_FromString(x0);
}

PyObject * _cffi_f_PyTuple_GetItem(PyObject * x0, int x1)
{
  return PyTuple_GetItem(x0, x1);
}

PyObject *(* _cffi_const_PyTuple_Pack(void))(size_t, ...)
{
  return (PyTuple_Pack);
}

size_t _cffi_f_PyTuple_Size(PyObject * x0)
{
  return PyTuple_Size(x0);
}

PyObject * _cffi_f_PyUnicode_AsUTF8String(PyObject * x0)
{
  return PyUnicode_AsUTF8String(x0);
}

PyObject * _cffi_f_PyUnicode_FromString(char const * x0)
{
  return PyUnicode_FromString(x0);
}

PyObject * _cffi_f_Py_CompileString(char const * x0, char const * x1, int x2)
{
  return Py_CompileString(x0, x1, x2);
}

void _cffi_f_Py_DECREF(PyObject * x0)
{
  Py_DECREF(x0);
}

void _cffi_f_Py_Finalize(void)
{
  Py_Finalize();
}

void _cffi_f_Py_INCREF(PyObject * x0)
{
  Py_INCREF(x0);
}

void _cffi_f_Py_Initialize(void)
{
  Py_Initialize();
}

void _cffi_f_Py_SetProgramName(char * x0)
{
  Py_SetProgramName(x0);
}

void _cffi_f_Py_XDECREF(PyObject * x0)
{
  Py_XDECREF(x0);
}

void _cffi_f_Py_XINCREF(PyObject * x0)
{
  Py_XINCREF(x0);
}

