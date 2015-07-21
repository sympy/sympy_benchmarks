#!/usr/bin/env python
from __future__ import print_function, division
from sympy.core.compatibility import range

from random import random
from sympy import factor, I, Integer, pi, simplify, sin, sqrt, Symbol, sympify
from sympy.abc import x, y, z
from timeit import default_timer as clock

def _hermite(n, y):
    if n == 1:
        return 2*y
    if n == 0:
        return 1
    return (2*y*_hermite(n-1, y) - 2*(n-1)*_hermite(n-2, y)).expand()


def _right(f, a, b, n):
    a = sympify(a)
    b = sympify(b)
    n = sympify(n)
    x = f.atoms(Symbol).pop()
    Deltax = (b - a)/n
    c = a
    est = 0
    for i in range(n):
        c += Deltax
        est += f.subs(x, c)
    return est*Deltax


def _srange(min_, max_, step):
    v = [min_]
    while (max_ - v[-1]).evalf() > 0:
        v.append(v[-1] + step)
    return v[:-1]


class TimeSymbench:
    # originally from sympy/benchmarks/bench_symbench.py

    def time_bench_R1(self):
        def f(z):
            return sqrt(Integer(1)/3)*z**2 + I/3
        e = f(f(f(f(f(f(f(f(f(f(I/2)))))))))).as_real_imag()[0]

    def time_hermite(self):
        "Hermite polynomial"
        a = _hermite(15, y)

    def time_R3(self):
        f = x + y + z
        a = [bool(f == f) for _ in range(10)]

    def time_R6(self):
        s = sum(simplify((x + sin(i))/x + (x - sin(i))/x) for i in range(100))

    def time_R7(self):
        f = x**24 + 34*x**12 + 45*x**3 + 9*x**18 + 34*x**10 + 32*x**21
        a = [f.subs(x, random()) for _ in range(10**3)]

    def time_R8(self):
        a = _right(x**2, 0, 5, 10**4)

    def time_R10(self):
        v = _srange(-pi, pi, sympify(1)/10)

    def time_S1(self):
        e = (x + y + z + 1)**7
        f = e*(e + 1)
        f = f.expand()
