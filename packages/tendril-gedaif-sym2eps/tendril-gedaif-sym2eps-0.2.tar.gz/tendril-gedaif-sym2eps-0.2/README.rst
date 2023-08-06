
gEDA sym2eps Python Wrapper
---------------------------

.. image:: https://badge.fury.io/py/tendril-gedaif-sym2eps.png
    :target: http://badge.fury.io/py/tendril-gedaif-sym2eps

.. image:: https://travis-ci.org/chintal/tendril-gedaif-sym2eps.svg
    :target: https://travis-ci.org/chintal/tendril-gedaif-sym2eps

Provides a _very_ simple wrapper around DJ Delorie's ``sym2eps``.

This package (and the wrapper) are mostly for fun and for having a simple
reference implementation for a Cython wrapper package handy. There isn't
much inherent utility to it. Normally, you would just use DJ Delorie's C file
`sym2eps.cc <http://www.gedasymbols.org/user/dj_delorie/tools/sym2eps.cc>`_
directly. Or better yet, the ``gaf`` binary from ``geda 1.9.2``, and get much
more than you would from here. This wrapper, for instance, doesn't support
reading from and writing to stdin/stdout, which the C file does.

The excuse for writing this wrapper was to be able to remove the C code and
the consequent requirement of figuring out a safe build process for it from
within the ``tendril`` core module. This way, we just list this package
as a dependency and let setuptools / distutils take care of it.

Cython tutorial (for future reference): http://docs.cython.org/src/tutorial/

Installation
------------
::

    pip install tendril-gedaif-sym2eps

Usage Example
-------------

    >>> import sym2eps
    >>> sym2eps.convert('test/symbol.sym', 'test/output.eps')

.. hint:: The paths specified here should either be absolute or relative
          to the CWD.

License
-------
Distributed under the terms of the GPLv2 License.

Copyright 2015 Chintalagiri Shashank  (Cython Wrapper)
Copyright 2006 DJ Delorie             (Original C code)

