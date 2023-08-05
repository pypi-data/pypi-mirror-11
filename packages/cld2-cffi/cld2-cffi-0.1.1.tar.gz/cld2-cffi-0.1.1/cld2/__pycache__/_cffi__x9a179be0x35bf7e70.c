
#include <Python.h>
#include <stddef.h>

/* this block of #ifs should be kept exactly identical between
   c/_cffi_backend.c, cffi/vengine_cpy.py, cffi/vengine_gen.py */
#if defined(_MSC_VER)
# include <malloc.h>   /* for alloca() */
# if _MSC_VER < 1600   /* MSVC < 2010 */
   typedef __int8 int8_t;
   typedef __int16 int16_t;
   typedef __int32 int32_t;
   typedef __int64 int64_t;
   typedef unsigned __int8 uint8_t;
   typedef unsigned __int16 uint16_t;
   typedef unsigned __int32 uint32_t;
   typedef unsigned __int64 uint64_t;
   typedef __int8 int_least8_t;
   typedef __int16 int_least16_t;
   typedef __int32 int_least32_t;
   typedef __int64 int_least64_t;
   typedef unsigned __int8 uint_least8_t;
   typedef unsigned __int16 uint_least16_t;
   typedef unsigned __int32 uint_least32_t;
   typedef unsigned __int64 uint_least64_t;
   typedef __int8 int_fast8_t;
   typedef __int16 int_fast16_t;
   typedef __int32 int_fast32_t;
   typedef __int64 int_fast64_t;
   typedef unsigned __int8 uint_fast8_t;
   typedef unsigned __int16 uint_fast16_t;
   typedef unsigned __int32 uint_fast32_t;
   typedef unsigned __int64 uint_fast64_t;
   typedef __int64 intmax_t;
   typedef unsigned __int64 uintmax_t;
# else
#  include <stdint.h>
# endif
# if _MSC_VER < 1800   /* MSVC < 2013 */
   typedef unsigned char _Bool;
# endif
#else
# include <stdint.h>
# if (defined (__SVR4) && defined (__sun)) || defined(_AIX)
#  include <alloca.h>
# endif
#endif

#if PY_MAJOR_VERSION < 3
# undef PyCapsule_CheckExact
# undef PyCapsule_GetPointer
# define PyCapsule_CheckExact(capsule) (PyCObject_Check(capsule))
# define PyCapsule_GetPointer(capsule, name) \
    (PyCObject_AsVoidPtr(capsule))
#endif

#if PY_MAJOR_VERSION >= 3
# define PyInt_FromLong PyLong_FromLong
#endif

#define _cffi_from_c_double PyFloat_FromDouble
#define _cffi_from_c_float PyFloat_FromDouble
#define _cffi_from_c_long PyInt_FromLong
#define _cffi_from_c_ulong PyLong_FromUnsignedLong
#define _cffi_from_c_longlong PyLong_FromLongLong
#define _cffi_from_c_ulonglong PyLong_FromUnsignedLongLong

#define _cffi_to_c_double PyFloat_AsDouble
#define _cffi_to_c_float PyFloat_AsDouble

#define _cffi_from_c_int_const(x)                                        \
    (((x) > 0) ?                                                         \
        ((unsigned long long)(x) <= (unsigned long long)LONG_MAX) ?      \
            PyInt_FromLong((long)(x)) :                                  \
            PyLong_FromUnsignedLongLong((unsigned long long)(x)) :       \
        ((long long)(x) >= (long long)LONG_MIN) ?                        \
            PyInt_FromLong((long)(x)) :                                  \
            PyLong_FromLongLong((long long)(x)))

#define _cffi_from_c_int(x, type)                                        \
    (((type)-1) > 0 ? /* unsigned */                                     \
        (sizeof(type) < sizeof(long) ?                                   \
            PyInt_FromLong((long)x) :                                    \
         sizeof(type) == sizeof(long) ?                                  \
            PyLong_FromUnsignedLong((unsigned long)x) :                  \
            PyLong_FromUnsignedLongLong((unsigned long long)x)) :        \
        (sizeof(type) <= sizeof(long) ?                                  \
            PyInt_FromLong((long)x) :                                    \
            PyLong_FromLongLong((long long)x)))

#define _cffi_to_c_int(o, type)                                          \
    (sizeof(type) == 1 ? (((type)-1) > 0 ? (type)_cffi_to_c_u8(o)        \
                                         : (type)_cffi_to_c_i8(o)) :     \
     sizeof(type) == 2 ? (((type)-1) > 0 ? (type)_cffi_to_c_u16(o)       \
                                         : (type)_cffi_to_c_i16(o)) :    \
     sizeof(type) == 4 ? (((type)-1) > 0 ? (type)_cffi_to_c_u32(o)       \
                                         : (type)_cffi_to_c_i32(o)) :    \
     sizeof(type) == 8 ? (((type)-1) > 0 ? (type)_cffi_to_c_u64(o)       \
                                         : (type)_cffi_to_c_i64(o)) :    \
     (Py_FatalError("unsupported size for type " #type), (type)0))

#define _cffi_to_c_i8                                                    \
                 ((int(*)(PyObject *))_cffi_exports[1])
#define _cffi_to_c_u8                                                    \
                 ((int(*)(PyObject *))_cffi_exports[2])
#define _cffi_to_c_i16                                                   \
                 ((int(*)(PyObject *))_cffi_exports[3])
#define _cffi_to_c_u16                                                   \
                 ((int(*)(PyObject *))_cffi_exports[4])
#define _cffi_to_c_i32                                                   \
                 ((int(*)(PyObject *))_cffi_exports[5])
#define _cffi_to_c_u32                                                   \
                 ((unsigned int(*)(PyObject *))_cffi_exports[6])
#define _cffi_to_c_i64                                                   \
                 ((long long(*)(PyObject *))_cffi_exports[7])
#define _cffi_to_c_u64                                                   \
                 ((unsigned long long(*)(PyObject *))_cffi_exports[8])
#define _cffi_to_c_char                                                  \
                 ((int(*)(PyObject *))_cffi_exports[9])
#define _cffi_from_c_pointer                                             \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[10])
#define _cffi_to_c_pointer                                               \
    ((char *(*)(PyObject *, CTypeDescrObject *))_cffi_exports[11])
#define _cffi_get_struct_layout                                          \
    ((PyObject *(*)(Py_ssize_t[]))_cffi_exports[12])
#define _cffi_restore_errno                                              \
    ((void(*)(void))_cffi_exports[13])
#define _cffi_save_errno                                                 \
    ((void(*)(void))_cffi_exports[14])
#define _cffi_from_c_char                                                \
    ((PyObject *(*)(char))_cffi_exports[15])
#define _cffi_from_c_deref                                               \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[16])
#define _cffi_to_c                                                       \
    ((int(*)(char *, CTypeDescrObject *, PyObject *))_cffi_exports[17])
#define _cffi_from_c_struct                                              \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[18])
#define _cffi_to_c_wchar_t                                               \
    ((wchar_t(*)(PyObject *))_cffi_exports[19])
#define _cffi_from_c_wchar_t                                             \
    ((PyObject *(*)(wchar_t))_cffi_exports[20])
#define _cffi_to_c_long_double                                           \
    ((long double(*)(PyObject *))_cffi_exports[21])
#define _cffi_to_c__Bool                                                 \
    ((_Bool(*)(PyObject *))_cffi_exports[22])
#define _cffi_prepare_pointer_call_argument                              \
    ((Py_ssize_t(*)(CTypeDescrObject *, PyObject *, char **))_cffi_exports[23])
#define _cffi_convert_array_from_object                                  \
    ((int(*)(char *, CTypeDescrObject *, PyObject *))_cffi_exports[24])
#define _CFFI_NUM_EXPORTS 25

typedef struct _ctypedescr CTypeDescrObject;

static void *_cffi_exports[_CFFI_NUM_EXPORTS];
static PyObject *_cffi_types, *_cffi_VerificationError;

static int _cffi_setup_custom(PyObject *lib);   /* forward */

static PyObject *_cffi_setup(PyObject *self, PyObject *args)
{
    PyObject *library;
    int was_alive = (_cffi_types != NULL);
    (void)self; /* unused */
    if (!PyArg_ParseTuple(args, "OOO", &_cffi_types, &_cffi_VerificationError,
                                       &library))
        return NULL;
    Py_INCREF(_cffi_types);
    Py_INCREF(_cffi_VerificationError);
    if (_cffi_setup_custom(library) < 0)
        return NULL;
    return PyBool_FromLong(was_alive);
}

static int _cffi_init(void)
{
    PyObject *module, *c_api_object = NULL;

    module = PyImport_ImportModule("_cffi_backend");
    if (module == NULL)
        goto failure;

    c_api_object = PyObject_GetAttrString(module, "_C_API");
    if (c_api_object == NULL)
        goto failure;
    if (!PyCapsule_CheckExact(c_api_object)) {
        PyErr_SetNone(PyExc_ImportError);
        goto failure;
    }
    memcpy(_cffi_exports, PyCapsule_GetPointer(c_api_object, "cffi"),
           _CFFI_NUM_EXPORTS * sizeof(void *));

    Py_DECREF(module);
    Py_DECREF(c_api_object);
    return 0;

  failure:
    Py_XDECREF(module);
    Py_XDECREF(c_api_object);
    return -1;
}

#define _cffi_type(num) ((CTypeDescrObject *)PyList_GET_ITEM(_cffi_types, num))

/**********/


#include <binding_decls.h>

static void _cffi_check__cld_chunk_t(cld_chunk_t *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  (void)((p->offset) << 1);
  (void)((p->bytes) << 1);
  { char const * *tmp = &p->lang_name; (void)tmp; }
  { char const * *tmp = &p->lang_code; (void)tmp; }
}
static PyObject *
_cffi_layout__cld_chunk_t(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; cld_chunk_t y; };
  static Py_ssize_t nums[] = {
    sizeof(cld_chunk_t),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(cld_chunk_t, offset),
    sizeof(((cld_chunk_t *)0)->offset),
    offsetof(cld_chunk_t, bytes),
    sizeof(((cld_chunk_t *)0)->bytes),
    offsetof(cld_chunk_t, lang_name),
    sizeof(((cld_chunk_t *)0)->lang_name),
    offsetof(cld_chunk_t, lang_code),
    sizeof(((cld_chunk_t *)0)->lang_code),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__cld_chunk_t(0);
}

static void _cffi_check__cld_language_details_t(cld_language_details_t *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  { char * *tmp = &p->lang_name; (void)tmp; }
  { char * *tmp = &p->lang_code; (void)tmp; }
}
static PyObject *
_cffi_layout__cld_language_details_t(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; cld_language_details_t y; };
  static Py_ssize_t nums[] = {
    sizeof(cld_language_details_t),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(cld_language_details_t, lang_name),
    sizeof(((cld_language_details_t *)0)->lang_name),
    offsetof(cld_language_details_t, lang_code),
    sizeof(((cld_language_details_t *)0)->lang_code),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__cld_language_details_t(0);
}

static void _cffi_check__cld_result_t(cld_result_t *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  { char const * *tmp = &p->lang_name; (void)tmp; }
  { char const * *tmp = &p->lang_code; (void)tmp; }
  (void)((p->percent) << 1);
  { double *tmp = &p->normalized_score; (void)tmp; }
}
static PyObject *
_cffi_layout__cld_result_t(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; cld_result_t y; };
  static Py_ssize_t nums[] = {
    sizeof(cld_result_t),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(cld_result_t, lang_name),
    sizeof(((cld_result_t *)0)->lang_name),
    offsetof(cld_result_t, lang_code),
    sizeof(((cld_result_t *)0)->lang_code),
    offsetof(cld_result_t, percent),
    sizeof(((cld_result_t *)0)->percent),
    offsetof(cld_result_t, normalized_score),
    sizeof(((cld_result_t *)0)->normalized_score),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__cld_result_t(0);
}

static void _cffi_check__cld_results_t(cld_results_t *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  { cld_result_t * *tmp = &p->results; (void)tmp; }
  { cld_chunk_t * *tmp = &p->chunks; (void)tmp; }
  (void)((p->num_chunks) << 1);
  (void)((p->reliable) << 1);
  (void)((p->bytes_found) << 1);
  (void)((p->valid_prefix_bytes) << 1);
}
static PyObject *
_cffi_layout__cld_results_t(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; cld_results_t y; };
  static Py_ssize_t nums[] = {
    sizeof(cld_results_t),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(cld_results_t, results),
    sizeof(((cld_results_t *)0)->results),
    offsetof(cld_results_t, chunks),
    sizeof(((cld_results_t *)0)->chunks),
    offsetof(cld_results_t, num_chunks),
    sizeof(((cld_results_t *)0)->num_chunks),
    offsetof(cld_results_t, reliable),
    sizeof(((cld_results_t *)0)->reliable),
    offsetof(cld_results_t, bytes_found),
    sizeof(((cld_results_t *)0)->bytes_found),
    offsetof(cld_results_t, valid_prefix_bytes),
    sizeof(((cld_results_t *)0)->valid_prefix_bytes),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__cld_results_t(0);
}

static PyObject *
_cffi_f_cld_create_results(PyObject *self, PyObject *noarg)
{
  cld_results_t * result;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = cld_create_results(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(0));
}

static PyObject *
_cffi_f_cld_destroy_results(PyObject *self, PyObject *arg0)
{
  cld_results_t * x0;
  Py_ssize_t datasize;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { cld_destroy_results(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_cld_detect(PyObject *self, PyObject *args)
{
  char * x0;
  int x1;
  cld_results_t * x2;
  char const * x3;
  char const * x4;
  char const * x5;
  char const * x6;
  int x7;
  int x8;
  int x9;
  int x10;
  int x11;
  int x12;
  int x13;
  int x14;
  int x15;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;
  PyObject *arg5;
  PyObject *arg6;
  PyObject *arg7;
  PyObject *arg8;
  PyObject *arg9;
  PyObject *arg10;
  PyObject *arg11;
  PyObject *arg12;
  PyObject *arg13;
  PyObject *arg14;
  PyObject *arg15;

  if (!PyArg_ParseTuple(args, "OOOOOOOOOOOOOOOO:cld_detect", &arg0, &arg1, &arg2, &arg3, &arg4, &arg5, &arg6, &arg7, &arg8, &arg9, &arg10, &arg11, &arg12, &arg13, &arg14, &arg15))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(2), arg0) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, int);
  if (x1 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca((size_t)datasize);
    memset((void *)x2, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(0), arg2) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(3), arg3, (char **)&x3);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x3 = alloca((size_t)datasize);
    memset((void *)x3, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x3, _cffi_type(3), arg3) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(3), arg4, (char **)&x4);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x4 = alloca((size_t)datasize);
    memset((void *)x4, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x4, _cffi_type(3), arg4) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(3), arg5, (char **)&x5);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x5 = alloca((size_t)datasize);
    memset((void *)x5, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x5, _cffi_type(3), arg5) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(3), arg6, (char **)&x6);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x6 = alloca((size_t)datasize);
    memset((void *)x6, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x6, _cffi_type(3), arg6) < 0)
      return NULL;
  }

  x7 = _cffi_to_c_int(arg7, int);
  if (x7 == (int)-1 && PyErr_Occurred())
    return NULL;

  x8 = _cffi_to_c_int(arg8, int);
  if (x8 == (int)-1 && PyErr_Occurred())
    return NULL;

  x9 = _cffi_to_c_int(arg9, int);
  if (x9 == (int)-1 && PyErr_Occurred())
    return NULL;

  x10 = _cffi_to_c_int(arg10, int);
  if (x10 == (int)-1 && PyErr_Occurred())
    return NULL;

  x11 = _cffi_to_c_int(arg11, int);
  if (x11 == (int)-1 && PyErr_Occurred())
    return NULL;

  x12 = _cffi_to_c_int(arg12, int);
  if (x12 == (int)-1 && PyErr_Occurred())
    return NULL;

  x13 = _cffi_to_c_int(arg13, int);
  if (x13 == (int)-1 && PyErr_Occurred())
    return NULL;

  x14 = _cffi_to_c_int(arg14, int);
  if (x14 == (int)-1 && PyErr_Occurred())
    return NULL;

  x15 = _cffi_to_c_int(arg15, int);
  if (x15 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = cld_detect(x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_cld_langcodes(PyObject *self, PyObject *noarg)
{
  char const * * result;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = cld_langcodes(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(4));
}

static PyObject *
_cffi_f_cld_languages(PyObject *self, PyObject *noarg)
{
  char const * * result;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = cld_languages(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(4));
}

static PyObject *
_cffi_f_cld_num_encodings(PyObject *self, PyObject *noarg)
{
  int result;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = cld_num_encodings(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_cld_num_langcodes(PyObject *self, PyObject *noarg)
{
  int result;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = cld_num_langcodes(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_cld_num_languages(PyObject *self, PyObject *noarg)
{
  int result;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = cld_num_languages(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_cld_supported_encodings(PyObject *self, PyObject *noarg)
{
  char const * * result;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = cld_supported_encodings(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(4));
}

static int _cffi_setup_custom(PyObject *lib)
{
  return ((void)lib,0);
}

static PyMethodDef _cffi_methods[] = {
  {"_cffi_layout__cld_chunk_t", _cffi_layout__cld_chunk_t, METH_NOARGS, NULL},
  {"_cffi_layout__cld_language_details_t", _cffi_layout__cld_language_details_t, METH_NOARGS, NULL},
  {"_cffi_layout__cld_result_t", _cffi_layout__cld_result_t, METH_NOARGS, NULL},
  {"_cffi_layout__cld_results_t", _cffi_layout__cld_results_t, METH_NOARGS, NULL},
  {"cld_create_results", _cffi_f_cld_create_results, METH_NOARGS, NULL},
  {"cld_destroy_results", _cffi_f_cld_destroy_results, METH_O, NULL},
  {"cld_detect", _cffi_f_cld_detect, METH_VARARGS, NULL},
  {"cld_langcodes", _cffi_f_cld_langcodes, METH_NOARGS, NULL},
  {"cld_languages", _cffi_f_cld_languages, METH_NOARGS, NULL},
  {"cld_num_encodings", _cffi_f_cld_num_encodings, METH_NOARGS, NULL},
  {"cld_num_langcodes", _cffi_f_cld_num_langcodes, METH_NOARGS, NULL},
  {"cld_num_languages", _cffi_f_cld_num_languages, METH_NOARGS, NULL},
  {"cld_supported_encodings", _cffi_f_cld_supported_encodings, METH_NOARGS, NULL},
  {"_cffi_setup", _cffi_setup, METH_VARARGS, NULL},
  {NULL, NULL, 0, NULL}    /* Sentinel */
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef _cffi_module_def = {
  PyModuleDef_HEAD_INIT,
  "_cffi__x9a179be0x35bf7e70",
  NULL,
  -1,
  _cffi_methods,
  NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit__cffi__x9a179be0x35bf7e70(void)
{
  PyObject *lib;
  lib = PyModule_Create(&_cffi_module_def);
  if (lib == NULL)
    return NULL;
  if (((void)lib,0) < 0 || _cffi_init() < 0) {
    Py_DECREF(lib);
    return NULL;
  }
  return lib;
}

#else

PyMODINIT_FUNC
init_cffi__x9a179be0x35bf7e70(void)
{
  PyObject *lib;
  lib = Py_InitModule("_cffi__x9a179be0x35bf7e70", _cffi_methods);
  if (lib == NULL)
    return;
  if (((void)lib,0) < 0 || _cffi_init() < 0)
    return;
  return;
}

#endif
