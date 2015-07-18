# -*- coding: utf-8 -*-

import sympy
from sympy import symbols, Integral, exp

def _make_integral_01():
    # Scaled down version of an integration by parts example
    params = symbols('u0 k l t'.split(), positive=True)
    u0, k, l, t = params
    M = exp(l*t)
    Q = k*u0*exp(-k*t)
    integral = Integral(M*Q, (t, 0, t))
    return integral, params


class TimeIntegration01:

    def setup(self):
        self.integral, self.params = _make_integral_01()

    def time_doit(self):
        self.integral.doit()

    def time_doit_meijerg():
        self.integral.doit(meijerg=True)
