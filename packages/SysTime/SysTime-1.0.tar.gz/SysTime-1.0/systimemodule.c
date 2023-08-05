//
//  systimemodule.c
//  whattime
//
//  Created by Eric Li on 7/26/15.
//  Copyright (c) 2015 Eric Li. All rights reserved.
//

#include <Python/Python.h>
#include <sys/time.h>

static PyObject *
set_time(PyObject *self, PyObject *args) {
    float tv_;
    float tvu_;
    int sts;

    if (!PyArg_ParseTuple(args, "ff", &tv_, &tvu_))
        return NULL;
    struct timeval tv;
    tv.tv_sec = tv_;
    tv.tv_usec = tvu_;
    sts = settimeofday(&tv, NULL);
    return Py_BuildValue("i",sts);
}

static PyMethodDef SysTimeMethods[] = {
    {"set_time", set_time, METH_VARARGS, "Set system time."},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initsystime(void)
{
    (void) Py_InitModule("systime", SysTimeMethods);
}
