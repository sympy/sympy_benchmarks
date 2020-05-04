# -*- coding: utf-8 -*-

from sympy import symbols, Integral, exp, log, Add

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


class _TimeIntegrationRisch(object):
    params = [1, 10, 100]

    def setup(self, n):
        x = symbols('x')
        self.integral = Integral(self.make_expr(n), x)
        self.values = {}

    def teardown(self, n):
        x = symbols('x')
        for key, val in self.values.items():
            ref = self.make_expr(n)
            if (ref - val.diff(x)).simplify() != 0:
                raise ValueError("Incorrect result, invalid timing:"
                                     " %s != %s" % (ref, val))

    def time_doit(self, n):
        self.values['time_doit'] = self.integral.doit()

    def time_doit_risch(self, n):
        self.values['time_doit_risch'] = self.integral.doit(risch=True)


class TimeIntegrationRisch01(_TimeIntegrationRisch):
    def make_expr(self, n):
        x = symbols('x')
        expr = x**n*exp(x)
        return expr

class TimeIntegrationRisch02(_TimeIntegrationRisch):
    def make_expr(self, n):
        x = symbols('x')
        expr = log(Add(*[exp(i*x) for i in range(n)])).diff(x)
        return expr

class TimeIntegrationRisch03(_TimeIntegrationRisch):
    def make_expr(self, n):
        x = symbols('x')
        expr = Add(*[log(x)**i for i in range(n)])
        return expr
