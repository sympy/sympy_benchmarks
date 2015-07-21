# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sympy

from benchmarks.solve import _mk_eqs, _Polynomial

class TestPoly(_Polynomial):
    x0 = 0

def test_mk_eqs():
    eqs, p, y = _mk_eqs(3, Poly=TestPoly)
    y0, y1 = y
    sol = sympy.solve(eqs, *p.c)
    assert sol[p.c[2]] == y0[2]/2
    assert sol[p.c[4]] == (p.x1**2*(3*y0[2] - 2*y1[2])/2 + p.x1*(8*y0[1] + 7*y1[1]) + 15*y0[0] - 15*y1[0])/p.x1**4
    assert sol[p.c[0]] == y0[0]
    assert sol[p.c[3]] == (p.x1**2*(-3*y0[2] + y1[2]) - 4*p.x1*(3*y0[1] + 2*y1[1]) - 20*y0[0] + 20*y1[0])/(2*p.x1**3)
    assert sol[p.c[5]] == (p.x1**2*(-y0[2] + y1[2]) - 6*p.x1*(y0[1] + y1[1]) - 12*y0[0] + 12*y1[0])/(2*p.x1**5)
    assert sol[p.c[1]] == y0[1]
