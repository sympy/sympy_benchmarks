from __future__ import absolute_import

import sympy
from sympy import dsolve, Eq, exp, refine

from slow_benchmarks.refine import _mk_piecewise_01

def test_mk_piecewise_01():
    eq, params = _mk_piecewise_01()
    t, y, y0, k, C1 = params
    k0, k1 = k
    u0, v0 = y0
    refined = refine(eq, ~sympy.Q.is_true(Eq(k[1], k[0])))
    assert refined.lhs == y[1](t)
    ref_rhs = (C1 - k0*u0*exp(k1*t)/(k0*exp(k0*t) - k1*exp(k0*t)))*exp(-k1*t)
    assert refined.rhs == ref_rhs
