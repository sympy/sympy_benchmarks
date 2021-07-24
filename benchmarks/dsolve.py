# -*- coding: utf-8 -*-

import sympy
from sympy import S, symbols, dsolve, Eq, Function, exp
from sympy.solvers.ode.riccati import match_riccati, solve_riccati

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


def _make_riccati_particular():
    # Particular solution solver for the Riccati ODE -
    #     f'(x) = b_0 + b_1*f(x) + b_2*f(x)**2
    # where b_0, b_1, b_2 are rational functions of x
    f = Function('f')
    x = symbols('x')

    eq = Eq(f(x).diff(x), x*f(x) + 2*x + (3*x - \
    2)*f(x)**2/(4*x + 2) + (8*x**2 - 7*x + 26)/(\
    16*x**3 - 24*x**2 + 8) - S(3)/2)

    # Check if equation matches and get b0, b1, b2
    _, (b0, b1, b2) = match_riccati(eq, f, x)

    return (f(x), x, b0, b1, b2)


def _make_riccati_general():
    # General solution solver for the Riccati ODE -
    #     f'(x) = b_0 + b_1*f(x) + b_2*f(x)**2
    # where b_0, b_1, b_2 are rational functions of x
    f = Function('f')
    x = symbols('x')

    eq = f(x).diff(x) + (3*x**2 + 1)*f(x)**2/x + (6*x**2 \
    - x + 3)*f(x)/(x*(x - 1)) + (3*x**2 - 2*x + 2)/(x*(x \
    - 1)**2)

    hint = "1st_rational_riccati"

    return eq, f(x), hint


class TimeDsolve01:

    def setup(self):
        self.ode, self.params = _make_ode_01()
        self.geneq, self.func, self.hint = _make_riccati_general()
        self.parteq, self.args = _make_riccati_particular()

    def time_dsolve(self):
        t, y, y0, k = self.params
        dsolve(self.ode, y[1](t))

    def time_riccati_partsol(self):
        sols = solve_riccati(*self.args)

    def time_riccati_gensol(self):
        dsolve(self.eq, self.func, hint=self.hint)
