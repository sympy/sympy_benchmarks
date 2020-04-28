# -*- coding: utf-8 -*-

from sympy.core import symbols, I

x, y, z = symbols('x,y,z')
p = 3*x**2*y*z**7 + 7*x*y*z**2 + 4*x + x*y**4
e = (x + y + z + 1)**32

class TimeCoreExpand:
    def time_expand_nothing_todo(self):
        p.expand(self)


    def bench_expand_32(self):
        """(x+y+z+1)**32  -> expand"""
        e.expand(self)


    def time_expand_complex_number_1(self):
        ((2 + 3*I)**1000).expand(complex=True)


    def time_expand_complex_number_2(self):
        ((2 + 3*I/4)**1000).expand(complex=True)
