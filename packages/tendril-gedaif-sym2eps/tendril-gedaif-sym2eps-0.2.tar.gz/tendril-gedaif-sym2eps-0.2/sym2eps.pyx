
# Copyright 2015 Chintalagiri Shashank  (Python Wrapper)
# Copyright 2006 DJ Delorie             (Original C code)
# Distributed under the terms of the GPLv2 License.

import os
cimport _sym2eps
ctypedef unsigned char char_type


cdef __convert(char* inpath, char* outpath):
    if _sym2eps.convert(inpath, outpath) != 0:
        raise RuntimeError(
            "Error converting {0} to {1}".format(inpath, outpath)
        )


cpdef _convert(_py_bytes_inpath, _py_bytes_outpath):
    cdef char* _c_inpath = _py_bytes_inpath
    cdef char* _c_outpath = _py_bytes_outpath
    __convert(_c_inpath, _c_outpath)


def get_bytes(s):
    if isinstance(s, unicode):
        bytes = s.encode('UTF-8')
        return bytes
    return s


def convert(inpath, outpath):
    _py_inpath = get_bytes(os.path.normpath(inpath))
    _py_outpath = get_bytes(os.path.normpath(outpath))
    _convert(_py_inpath, _py_outpath)

