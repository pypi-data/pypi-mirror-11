# Copyright © 2007-2015 Jakub Wilk <jwilk@jwilk.net>
#
# This package is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 dated June, 1991.
#
# This package is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

cdef extern from 'libdjvu/miniexp.h':
    struct cexpr_s 'miniexp_s'
    ctypedef cexpr_s* cexpr_t 'miniexp_t'

    cdef extern struct cvar_s 'minivar_s'
    ctypedef cvar_s cvar_t 'minivar_t'

cdef class _WrappedCExpr:
    cdef cvar_t* cvar
    cdef cexpr_t cexpr(self)
    cdef object print_into(self, object, object, int)
    cdef object as_string(self, object, int)

cdef object public_c2py(cexpr_t)
cdef _WrappedCExpr public_py2c(object)

# vim:ts=4 sts=4 sw=4 et ft=pyrex
