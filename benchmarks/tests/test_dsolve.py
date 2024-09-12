from __future__ import absolute_import

import sympy
from sympy import dsolve, Ne, Eq, exp, refine, Symbol
from sympy.solvers.ode.riccati import solve_riccati

from benchmarks.dsolve import _make_ode_01, _make_riccati_particular, _make_riccati_general

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


def test_riccati_particular():
    fx, x, b0, b1, b2 = _make_riccati_particular()
    sol = solve_riccati(fx, x, b0, b1, b2)
    assert sol == [Eq(fx, (1 - 4*x)/(2*x - 2))]


def test_riccati_general():
    eq, fx, hint = _make_riccati_general()
    x = list(fx.atoms(Symbol))[0]
    gensol = dsolve(eq, hint=hint)
    C1 = Symbol('C1')
    assert gensol == Eq(fx, (-C1 - x**3 + x**2 - \
    2*x + 1)/(C1*x - C1 + x**4 - x**3 + x**2 - 2*x + 1))
