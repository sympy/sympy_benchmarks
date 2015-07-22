# -*- coding: utf-8 -*-

import sympy
from sympy import symbols, Eq, Function, exp, Piecewise

def _mk_piecewise_01():
    t = symbols('t')
    y = u, v = symbols('u v', cls=Function)
    u0, v0 = y0 = symbols('u0 v0')
    k0, k1 = k = symbols('k0 k1')
    C1 = symbols('C1')
    params = (t, y, y0, k, C1)    
    pw = Piecewise(
        (t, Eq(k1, k0)),
        (-exp(k1*t)/(k0*exp(k0*t) - k1*exp(k0*t)), True)
    )
    equality = Eq(v(t), (C1 + k0*u0*pw)*exp(-k1*t))
    return equality, params


class TimeRefine01:

    def setup(self):
        self.eq, self.params = _mk_piecewise_01()

    def time_refine(self):
        t, y, y0, k, C1 = self.params
        self.eq.refine(~sympy.Q.is_true(Eq(k[1], k[0])))
