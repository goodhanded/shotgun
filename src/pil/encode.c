/*
 * The Python Imaging Library.
 *
 * standard encoder interfaces for the Imaging library
 *
 * History:
 * 1996-04-19 fl   Based on decoders.c
 * 1996-05-12 fl   Compile cleanly as C++
 * 1996-12-30 fl   Plugged potential memory leak for tiled images
 * 1997-01-03 fl   Added GIF encoder
 * 1997-01-05 fl   Plugged encoder buffer leaks
 * 1997-01-11 fl   Added encode_to_file method
 * 1998-03-09 fl   Added mode/rawmode argument to encoders
 * 1998-07-09 fl   Added interlace argument to GIF encoder
 * 1999-02-07 fl   Added PCX encoder
 *
 * Copyright (c) 1997-2001 by Secret Labs AB
 * Copyright (c) 1996-1997 by Fredrik Lundh 
 *
 * See the README file for information on usage and redistribution.
 */

/* FIXME: make these pluggable! */

#include "Python.h"
#include "compat.h"

#include "Imaging.h"
#include "Gif.h"

#ifdef HAVE_UNISTD_H
#include <unistd.h> /* write */
#endif

/* -------------------------------------------------------------------- */
/* Common								*/
/* -------------------------------------------------------------------- */

typedef struct {
    PyObject_HEAD
    int (*encode)(Imaging im, ImagingCodecState state,
		  UINT8* buffer, int bytes);
    struct ImagingCodecStateInstance state;
    Imaging im;
    PyObject* lock;
} ImagingEncoderObject;

static PyTypeObject ImagingEncoderType;

int
PyImaging_EncoderInit(void)
{
#ifdef PY2
    ImagingEncoderType.ob_type = &PyType_Type;
#else
    if (PyType_Ready(&ImagingEncoderType) < 0)
        return 0;
#endif
    return 1;
}

static ImagingEncoderObject*
PyImaging_EncoderNew(int contextsize)
{
    ImagingEncoderObject *encoder;
    void *context;

    encoder = PyObject_New(ImagingEncoderObject, &ImagingEncoderType);
    if (encoder == NULL)
	return NULL;

    /* Clear the encoder state */
    memset(&encoder->state, 0, sizeof(encoder->state));

    /* Allocate encoder context */
    if (contextsize > 0) {
	context = (void*) calloc(1, contextsize);
	if (!context) {
	    Py_DECREF(encoder);
	    (void) PyErr_NoMemory();
	    return NULL;
	}
    } else
	context = 0;

    /* Initialize encoder context */
    encoder->state.context = context;

    /* Target image */
    encoder->lock = NULL;
    encoder->im = NULL;

    return encoder;
}

static void
_dealloc(ImagingEncoderObject* encoder)
{
    free(encoder->state.buffer);
    free(encoder->state.context);
    Py_XDECREF(encoder->lock);
    PyObject_Del(encoder);
}

static PyObject* 
_encode(ImagingEncoderObject* encoder, PyObject* args)
{
    PyObject* buf;
    PyObject* result;
    int status;

    /* Encode to a Python string (allocated by this method) */

    int bufsize = 16384;

    if (!PyArg_ParseTuple(args, "|i", &bufsize))
	return NULL;

    buf = PyString_FromStringAndSize(NULL, bufsize);
    if (!buf)
	return NULL;

    status = encoder->encode(encoder->im, &encoder->state,
			     (UINT8*) PyString_AsString(buf), bufsize);

    /* adjust string length to avoid slicing in encoder */
    if (_PyString_Resize(&buf, (status > 0) ? status : 0) < 0)
        return NULL;

    result = Py_BuildValue("iiO", status, encoder->state.errcode, buf);

    Py_DECREF(buf); /* must release buffer!!! */

    return result;
}

static PyObject* 
_encode_to_file(ImagingEncoderObject* encoder, PyObject* args)
{
    UINT8* buf;
    int status;
    ImagingSectionCookie cookie;

    /* Encode to a file handle */

    int fh;
    int bufsize = 16384;

    if (!PyArg_ParseTuple(args, "i|i", &fh, &bufsize))
	return NULL;

    /* Allocate an encoder buffer */
    buf = (UINT8*) malloc(bufsize);
    if (!buf)
	return PyErr_NoMemory();

    ImagingSectionEnter(&cookie);

    do {

	/* This replaces the inner loop in the ImageFile _save
	   function. */

	status = encoder->encode(encoder->im, &encoder->state, buf, bufsize);

	if (status > 0)
	    if (write(fh, buf, status) < 0) {
                ImagingSectionLeave(&cookie);
		free(buf);
		return PyErr_SetFromErrno(PyExc_IOError);
	    }

    } while (encoder->state.errcode == 0);

    ImagingSectionLeave(&cookie);

    free(buf);

    return Py_BuildValue("i", encoder->state.errcode);
}

extern Imaging PyImaging_AsImaging(PyObject *op);

static PyObject*
_setimage(ImagingEncoderObject* encoder, PyObject* args)
{
    PyObject* op;
    Imaging im;
    ImagingCodecState state;
    int x0, y0, x1, y1;

    /* Define where image data should be stored */

    x0 = y0 = x1 = y1 = 0;

    /* FIXME: should publish the ImagingType descriptor */
    if (!PyArg_ParseTuple(args, "O|(iiii)", &op, &x0, &y0, &x1, &y1))
	return NULL;
    im = PyImaging_AsImaging(op);
    if (!im)
	return NULL;

    encoder->im = im;

    state = &encoder->state;

    if (x0 == 0 && x1 == 0) {
	state->xsize = im->xsize;
	state->ysize = im->ysize;
    } else {
	state->xoff = x0;
	state->yoff = y0;
	state->xsize = x1 - x0;
	state->ysize = y1 - y0;
    }

    if (state->xsize <= 0 ||
	state->xsize + state->xoff > im->xsize ||
	state->ysize <= 0 ||
	state->ysize + state->yoff > im->ysize) {
	PyErr_SetString(PyExc_SystemError, "tile cannot extend outside image");
	return NULL;
    }

    /* Allocate memory buffer (if bits field is set) */
    if (state->bits > 0) {
	state->bytes = (state->bits * state->xsize+7)/8;
	state->buffer = (UINT8*) malloc(state->bytes);
	if (!state->buffer)
	    return PyErr_NoMemory();
    }

    /* Keep a reference to the image object, to make sure it doesn't
       go away before we do */
    Py_INCREF(op);
    Py_XDECREF(encoder->lock);
    encoder->lock = op;

    Py_INCREF(Py_None);
    return Py_None;
}

static struct PyMethodDef methods[] = {
    {"encode", (PyCFunction)_encode, METH_VARARGS},
    {"encode_to_file", (PyCFunction)_encode_to_file, METH_VARARGS},
    {"setimage", (PyCFunction)_setimage, METH_VARARGS},
    {NULL, NULL} /* sentinel */
};

#ifdef PY2
static PyObject*  
_getattr(ImagingEncoderObject* self, char* name)
{
    return Py_FindMethod(methods, (PyObject*) self, name);
}
#endif

static PyTypeObject ImagingEncoderType = {
	PyObject_HEAD_INIT(NULL)
#ifdef PY2
	0,				/*ob_size*/
	"ImagingEncoder",		/*tp_name*/
	sizeof(ImagingEncoderObject),	/*tp_size*/
	0,				/*tp_itemsize*/
	/* methods */
	(destructor)_dealloc,		/*tp_dealloc*/
	0,				/*tp_print*/
	(getattrfunc)_getattr,		/*tp_getattr*/
	0,				/*tp_setattr*/
	0,				/*tp_compare*/
	0,				/*tp_repr*/
	0,                              /*tp_hash*/
#else
    "ImagingEncoder", sizeof(ImagingEncoderObject),	0,
    /* methods */
    (destructor) _dealloc, /* tp_dealloc */
    0, /* tp_print */
    0, /* tp_getattr */
    0, /* tp_setattr */
    0, /* tp_reserved */
    0, /* tp_repr */
    0, /* tp_as_number */
    0, /* tp_as_sequence */
    0, /* tp_as_mapping */
    0, /* tp_hash */
    0, /* tp_call */
    0, /* tp_str */
    0, /* tp_getattro */
    0, /* tp_setattro */
    0, /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT, /* tp_flags */
    0, /* tp_doc */
    0, /* tp_traverse */
    0, /* tp_clear */
    0, /* tp_richcompare */
    0, /* tp_weaklistoffset */
    0, /* tp_iter */
    0, /* tp_iternext */
    methods, /* tp_methods */
    0, /* tp_members */
#endif
};

/* -------------------------------------------------------------------- */

int
get_packer(ImagingEncoderObject* encoder, const char* mode,
           const char* rawmode)
{
    int bits;
    ImagingShuffler pack;

    pack = ImagingFindPacker(mode, rawmode, &bits);
    if (!pack) {
	Py_DECREF(encoder);
	PyErr_SetString(PyExc_SystemError, "unknown raw mode");
	return -1;
    }

    encoder->state.shuffle = pack;
    encoder->state.bits = bits;

    return 0;
}


/* -------------------------------------------------------------------- */
/* EPS									*/
/* -------------------------------------------------------------------- */

PyObject*
PyImaging_EpsEncoderNew(PyObject* self, PyObject* args)
{
    ImagingEncoderObject* encoder;

    encoder = PyImaging_EncoderNew(0);
    if (encoder == NULL)
	return NULL;

    encoder->encode = ImagingEpsEncode;

    return (PyObject*) encoder;
}


/* -------------------------------------------------------------------- */
/* GIF									*/
/* -------------------------------------------------------------------- */

PyObject*
PyImaging_GifEncoderNew(PyObject* self, PyObject* args)
{
    ImagingEncoderObject* encoder;

    char *mode;
    char *rawmode;
    int bits = 8;
    int interlace = 0;
    if (!PyArg_ParseTuple(args, "ss|ii", &mode, &rawmode, &bits, &interlace))
	return NULL;

    encoder = PyImaging_EncoderNew(sizeof(GIFENCODERSTATE));
    if (encoder == NULL)
	return NULL;

    if (get_packer(encoder, mode, rawmode) < 0)
	return NULL;

    encoder->encode = ImagingGifEncode;

    ((GIFENCODERSTATE*)encoder->state.context)->bits = bits;
    ((GIFENCODERSTATE*)encoder->state.context)->interlace = interlace;

    return (PyObject*) encoder;
}


/* -------------------------------------------------------------------- */
/* PCX									*/
/* -------------------------------------------------------------------- */

PyObject*
PyImaging_PcxEncoderNew(PyObject* self, PyObject* args)
{
    ImagingEncoderObject* encoder;

    char *mode;
    char *rawmode;
    int bits = 8;
    if (!PyArg_ParseTuple(args, "ss|ii", &mode, &rawmode, &bits))
	return NULL;

    encoder = PyImaging_EncoderNew(0);
    if (encoder == NULL)
	return NULL;

    if (get_packer(encoder, mode, rawmode) < 0)
	return NULL;

    encoder->encode = ImagingPcxEncode;

    return (PyObject*) encoder;
}


/* -------------------------------------------------------------------- */
/* RAW									*/
/* -------------------------------------------------------------------- */

PyObject*
PyImaging_RawEncoderNew(PyObject* self, PyObject* args)
{
    ImagingEncoderObject* encoder;

    char *mode;
    char *rawmode;
    int stride = 0;
    int ystep = 1;

    if (!PyArg_ParseTuple(args, "ss|ii", &mode, &rawmode, &stride, &ystep))
	return NULL;

    encoder = PyImaging_EncoderNew(0);
    if (encoder == NULL)
	return NULL;

    if (get_packer(encoder, mode, rawmode) < 0)
	return NULL;

    encoder->encode = ImagingRawEncode;

    encoder->state.ystep = ystep;
    encoder->state.count = stride;

    return (PyObject*) encoder;
}


/* -------------------------------------------------------------------- */
/* XBM									*/
/* -------------------------------------------------------------------- */

PyObject*
PyImaging_XbmEncoderNew(PyObject* self, PyObject* args)
{
    ImagingEncoderObject* encoder;

    encoder = PyImaging_EncoderNew(0);
    if (encoder == NULL)
	return NULL;

    if (get_packer(encoder, "1", "1;R") < 0)
	return NULL;

    encoder->encode = ImagingXbmEncode;

    return (PyObject*) encoder;
}


/* -------------------------------------------------------------------- */
/* WEBP									*/
/* -------------------------------------------------------------------- */

#ifdef HAVE_LIBWEBP

#include "WebP.h"

PyObject*
PyImaging_WebPEncoderNew(PyObject* self, PyObject* args)
{
    ImagingEncoderObject* encoder;

    char* mode;
    char* rawmode;
    int quality = 0;
    if (!PyArg_ParseTuple(args, ARG("ss|i", "ss|i"), &mode, &rawmode,
			  &quality))
	return NULL;

    encoder = PyImaging_EncoderNew(sizeof(WEBPCONTEXT));
    if (encoder == NULL)
	return NULL;

    if (get_packer(encoder, mode, rawmode) < 0)
	return NULL;

    encoder->encode = ImagingWebPEncode;

    ((WEBPCONTEXT*)encoder->state.context)->quality = quality;

    return (PyObject*) encoder;
}
#endif


/* -------------------------------------------------------------------- */
/* ZIP									*/
/* -------------------------------------------------------------------- */

#ifdef HAVE_LIBZ

#include "Zip.h"

PyObject*
PyImaging_ZipEncoderNew(PyObject* self, PyObject* args)
{
    ImagingEncoderObject* encoder;

    char* mode;
    char* rawmode;
    int optimize = 0;
    int compress_level = -1;
    int compress_type = -1;
    char* dictionary = NULL;
    int dictionary_size = 0;
    if (!PyArg_ParseTuple(args, ARG("ss|iiis#", "ss|iiiy#"),
			  &mode, &rawmode, &optimize,
			  &compress_level, &compress_type,
			  &dictionary, &dictionary_size))
	return NULL;

    encoder = PyImaging_EncoderNew(sizeof(ZIPSTATE));
    if (encoder == NULL)
	return NULL;

    if (get_packer(encoder, mode, rawmode) < 0)
	return NULL;

    encoder->encode = ImagingZipEncode;

    if (rawmode[0] == 'P')
	/* disable filtering */
	((ZIPSTATE*)encoder->state.context)->mode = ZIP_PNG_PALETTE;

    ((ZIPSTATE*)encoder->state.context)->optimize = optimize;
    ((ZIPSTATE*)encoder->state.context)->compress_level = compress_level;
    ((ZIPSTATE*)encoder->state.context)->compress_type = compress_type;
    ((ZIPSTATE*)encoder->state.context)->dictionary = dictionary;
    ((ZIPSTATE*)encoder->state.context)->dictionary_size = dictionary_size;

    return (PyObject*) encoder;
}
#endif


/* -------------------------------------------------------------------- */
/* JPEG									*/
/* -------------------------------------------------------------------- */

#ifdef HAVE_LIBJPEG

/* We better define this encoder last in this file, so the following
   undef's won't mess things up for the Imaging library proper. */

#undef	HAVE_PROTOTYPES
#undef	HAVE_STDDEF_H
#undef	HAVE_STDLIB_H
#undef	UINT8
#undef	UINT16
#undef	UINT32
#undef	INT8
#undef	INT16
#undef	INT32

#include "Jpeg.h"

static unsigned int** get_qtables_arrays(PyObject* qtables) {
    PyObject* tables;
    PyObject* table;
    PyObject* table_data;
    int i, j, num_tables;
    unsigned int **qarrays;
    
    if (qtables == Py_None) {
        return NULL;
    }
    
    if (!PySequence_Check(qtables)) {
        PyErr_SetString(PyExc_ValueError, "Invalid quantization tables");
        return NULL;
    }
    
    tables = PySequence_Fast(qtables, "expected a sequence");
    num_tables = PySequence_Size(qtables);
    if (num_tables < 2 || num_tables > NUM_QUANT_TBLS) {
        PyErr_SetString(PyExc_ValueError, "Not a valid numbers of quantization tables. Should be between 2 and 4.");
        return NULL;
    }
    qarrays = (unsigned int**) PyMem_Malloc(num_tables * sizeof(unsigned int));
    if (!qarrays) {
        Py_DECREF(tables);
        PyErr_NoMemory();
        return NULL;
    }
    for (i = 0; i < num_tables; i++) {
        table = PySequence_Fast_GET_ITEM(tables, i);
        if (!PySequence_Check(table)) {
            Py_DECREF(tables);
            PyErr_SetString(PyExc_ValueError, "Invalid quantization tables");
            return NULL;
        }
        if (PySequence_Size(table) != DCTSIZE2) {
            Py_DECREF(tables);
            PyErr_SetString(PyExc_ValueError, "Invalid quantization tables");
            return NULL;
        }
        table_data = PySequence_Fast(table, "expected a sequence");
        qarrays[i] = (unsigned int*) PyMem_Malloc(DCTSIZE2 * sizeof(unsigned int));
        if (!qarrays[i]) {
            Py_DECREF(tables);
            PyErr_NoMemory();
            return NULL;
        }
        for (j = 0; j < DCTSIZE2; j++) {
            qarrays[i][j] = PyInt_AS_LONG(PySequence_Fast_GET_ITEM(table_data, j));
        }
    }

    Py_DECREF(tables);

    if (PyErr_Occurred()) {
        PyMem_Free(qarrays);
        qarrays = NULL;
    }

    return qarrays;
}


PyObject*
PyImaging_JpegEncoderNew(PyObject* self, PyObject* args)
{
    ImagingEncoderObject* encoder;

    char *mode;
    char *rawmode;
    int quality = 0;
    int progressive = 0;
    int smooth = 0;
    int optimize = 0;
    int streamtype = 0; /* 0=interchange, 1=tables only, 2=image only */
    int xdpi = 0, ydpi = 0;
    int subsampling = -1; /* -1=default, 0=none, 1=medium, 2=high */
    PyObject* qtables;
    unsigned int **qarrays = NULL;
    char* extra = NULL; int extra_size;
    if (!PyArg_ParseTuple(args, ARG("ss|iiiiiiiiOs#", "ss|iiiiiiiiOy#"),
			  &mode, &rawmode, &quality,
			  &progressive, &smooth, &optimize, &streamtype,
                          &xdpi, &ydpi, &subsampling, &qtables, &extra, &extra_size))
	return NULL;

    encoder = PyImaging_EncoderNew(sizeof(JPEGENCODERSTATE));
    if (encoder == NULL)
	return NULL;

    if (get_packer(encoder, mode, rawmode) < 0)
	return NULL;

    qarrays = get_qtables_arrays(qtables);

    if (extra && extra_size > 0) {
        char* p = malloc(extra_size);
        if (!p)
            return PyErr_NoMemory();
        memcpy(p, extra, extra_size);
        extra = p;
    } else
        extra = NULL;

    encoder->encode = ImagingJpegEncode;

    ((JPEGENCODERSTATE*)encoder->state.context)->quality = quality;
    ((JPEGENCODERSTATE*)encoder->state.context)->qtables = qarrays;
    ((JPEGENCODERSTATE*)encoder->state.context)->subsampling = subsampling;
    ((JPEGENCODERSTATE*)encoder->state.context)->progressive = progressive;
    ((JPEGENCODERSTATE*)encoder->state.context)->smooth = smooth;
    ((JPEGENCODERSTATE*)encoder->state.context)->optimize = optimize;
    ((JPEGENCODERSTATE*)encoder->state.context)->streamtype = streamtype;
    ((JPEGENCODERSTATE*)encoder->state.context)->xdpi = xdpi;
    ((JPEGENCODERSTATE*)encoder->state.context)->ydpi = ydpi;
    ((JPEGENCODERSTATE*)encoder->state.context)->extra = extra;
    ((JPEGENCODERSTATE*)encoder->state.context)->extra_size = extra_size;

    return (PyObject*) encoder;
}

#endif
