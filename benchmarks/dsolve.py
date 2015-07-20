# -*- coding: utf-8 -*-

import sympy
from sympy import symbols, dsolve, Eq, Function, exp

def _make_ode_01():
    # du/dt = -k0*u
    # dv/dt = k0*u - k1*v
    t = symbols('t')
    y = u, v = symbols('u v', cls=Function)
    y0 = symbols('u0 v0')
    k = symbols('k0 k1')
    u_ = y0[0]*exp(-k[0]*t)
    dvdt_ = k[0]*u_ - k[1]*v(t)
    params = (t, y, y0, k)
    return Eq(v(t).diff(t), dvdt_), params


class TimeDsolve01:

    def setup(self):
        self.ode, self.params = _make_ode_01()

    def time_dsolve(self):
        t, y, y0, k = self.params
        dsolve(self.ode, y[1](t))
