# -*- coding: utf-8 -*-

import sympy

class _Polynomial(object):
    
    expr = None
    x = sympy.Symbol('x', real=True)
    x0 = sympy.symbols('x0', real=True)
    x1 = sympy.symbols('x1', real=True)

    def __init__(self, c=None):
        self.c = c

    def diff(self, deg):
        return self.expr.diff(self.x, deg)

    # Below are properties to be subclassed
    @property
    def expr(self):
        return sum([c*self.x**o for o, c in enumerate(self.c)])

    def eval(self, x_val, deriv=0):
        return self.expr.diff(self.x, deriv).subs({self.x: x_val})


def _make_poly(order, Poly=None):
    if Poly is None:
        Poly = _Polynomial
    c = [sympy.Symbol('c_' + str(o), real=True) for o in range(order+1)]
    return Poly(c)


def _mk_eqs(wy=3, **kwargs):
    # Equations for fitting a wy*2 - 1 degree polynomial between two points,
    # at end points derivatives are known up to order: wy - 1
    p = _make_poly(2*wy-1, **kwargs)
    y0 = [sympy.Symbol('y0_' + str(i), real=True) for i in range(wy)]
    y1 = [sympy.Symbol('y1_' + str(i), real=True) for i in range(wy)]
    eqs = []
    for i in range(wy):
        eqs.append(p.diff(i).subs({p.x: p.x0}) - y0[i])
        eqs.append(p.diff(i).subs({p.x: p.x1}) - y1[i])
    return eqs, p, (y0, y1)


class TimeSolve01:

    def setup(self):
        self.eqs, self.p, self.y = _mk_eqs()

    def time_solve(self):
        sympy.solve(self.eqs, *self.p.c)

    def time_solve_nocheck(self):
        sympy.solve(self.eqs, *self.p.c, check=False)
