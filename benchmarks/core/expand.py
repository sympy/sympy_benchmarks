# -*- coding: utf-8 -*-

from sympy import log, Rational as R
from sympy.core import symbols, I
from sympy.core.function import expand_power_base, expand

x, y, z = symbols('x,y,z')
A, B, C = symbols("A B C", commutative=False)
t = symbols('t', positive=True)
p = 3*x**2*y*z**7 + 7*x*y*z**2 + 4*x + x*y**4
e = (x + y + z + 1)**32

class TimeExpand:

    def time_expand_nothing_todo(self):
        p.expand(self)

    def bench_expand_32(self):
        """(x+y+z+1)**32  -> expand"""
        e.expand(self)

    def time_expand_complex_number_1(self):
        ((2 + 3*I)**1000).expand(complex=True)

    def time_expand_complex_number_2(self):
        ((2 + 3*I/4)**1000).expand(complex=True)

    def time_expand_no_log(self):
        ((1 + log(x**4))**2).expand(log=False)

    def time_expand_no_multinomial(self):
        ((1 + x)*(1 + (1 + x)**4)).expand(multinomial=False)

    def time_expand_negative_integers_powers(self):
        ((x + y)**(-2)).expand()
        ((x + y)**(-3)).expand(multinomial=False)

    def time_expand_non_commutative(self):
        (C*(A + B)).expand()
        ((x*A*B*A**-1)**2).expand()

    def time_expnad_radicals(self):
        (((x+ y)**R(1, 2))**3).expand()
        (1/((x+ y)**R(1, 2))**3).expand()

    def time_expand_modulus(self):
        ((x + y)**11).expand(modulus=11)

    def time_expand_frac(self):
        expand((x + y)*y/x/(x + 1), frac=True)

    def time_expand_power_base(self):
        expand_power_base((x*y*z)**4)
        expand_power_base((x*y*z)**x, force=True)

    def time_expand_arit(self):
        ((x + y)*z).expand()
        ((x + z)*(x + y)*(y + z)).expand()

    def time_expand_log(self):
        expand(log(t**2) - log(t**2/4) - 2*log(2))
