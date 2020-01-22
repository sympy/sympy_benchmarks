from __future__ import absolute_import

import sympy
from sympy import dsolve, Ne, exp, refine

from benchmarks.dsolve import _make_ode_01

def test_make_ode_01():
    ode, params = _make_ode_01()
    t, y, y0, k = params
    result = dsolve(ode, y[1](t))
    eq_assumption = sympy.Q.is_true(Ne(k[1], k[0]))
    refined = refine(result, eq_assumption)
    ignore = k + y0 + (t,)
    int_const = [fs for fs in refined.free_symbols if fs not in ignore][0]
    ref = int_const*exp(-k[1]*t) - exp(-k[0]*t)*k[0]*y0[0]/(k[0] - k[1])
    assert (refined.rhs - ref).simplify() == 0
