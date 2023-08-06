
# Copyright 2015 Chintalagiri Shashank  (Python Wrapper)
# Copyright 2006 DJ Delorie             (Original C code)
# Distributed under the terms of the GPLv2 License.

cdef extern from 'src/_sym2eps.h':
    int convert(char * inpath, char * outpath)
