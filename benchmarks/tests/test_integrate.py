from __future__ import absolute_import

import sympy
from sympy import exp

from benchmarks.integrate import _make_integral_01

def test_make_integral_01():
    integral, params = _make_integral_01()
    intgr = integral.doit()
    u0, k, l, t = params

    # eq: k == l, neq: k != l
    ref_eq = k*u0*t
    ref_neq = -k*u0/(k-l)*(exp(t*(l-k)) - 1)

    refined_eq = integral.subs({l: k}).doit()
    assert (refined_eq - ref_eq).simplify() == 0

    eq_assumption = sympy.Q.is_true(sympy.Ne(l, k))
    refined_neq = sympy.refine(intgr, eq_assumption).simplify()
    assert (refined_neq - ref_neq).simplify() == 0
