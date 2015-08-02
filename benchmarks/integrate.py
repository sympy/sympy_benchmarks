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
        self.values = {}
        self._set_ref()

    def _set_ref(self):
        u0, k, l, t = self.params
        self.ref = {
            'time_doit_meijerg': -k*u0/(k-l)*(exp(t*(l-k)) - 1)
        }

    def teardown(self):
        for key, val in self.values.items():
            try:
                ref = self.ref[key]
            except KeyError:
                pass  # don't fail because of non-existent ref.
            else:
                if (ref - val).simplify() != 0:
                    raise ValueError("Incorrect result, invalid timing:"
                                     " %s != %s" % (ref, val))

    def time_doit(self):
        self.values['time_doit'] = self.integral.doit()

    def time_doit_meijerg(self):
        self.values['time_doit_meijerg'] = self.integral.doit(meijerg=True)
