# -*- coding: utf-8 -*-

from sympy.core import Add, Mul, symbols, I

x, y, z = symbols('x,y,z')

p = 3*x**2*y*z**7 + 7*x*y*z**2 + 4*x + x*y**4
e = (x + y + z + 1)**32

class TimeCoreArit:
    def time_neg(self):
        -x


    def time_Add_x1(self):
        x + 1

    def time_Add_thousands(self):
        # from https://github.com/sympy/sympy/pull/27254
        a = symbols("a0:2000")
        b = Add(*a);
        b + a[0]

    def time_Add_1x(self):
        1 + x


    def time_Add_x05(self):
        x + 0.5


    def time_Add_xy(self):
        x + y


    def time_Add_xyz(self):
        Add(*[x, y, z])


    def time_Mul_xy(self):
        x*y


    def time_Mul_xyz(self):
        Mul(*[x, y, z])


    def time_Div_xy(self):
        x/y


    def time_Div_2y(self):
        2/y

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
