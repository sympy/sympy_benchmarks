# -*- coding: utf-8 -*-

from sympy.core import Add, Mul, symbols, I

x, y, z = symbols('x,y,z')

p = 3*x**2*y*z**7 + 7*x*y*z**2 + 4*x + x*y**4
e = (x + y + z + 1)**32

class TimeArit:
    def timeit_neg(self):
        -x


    def timeit_Add_x1(self):
        x + 1


    def timeit_Add_1x(self):
        1 + x


    def timeit_Add_x05(self):
        x + 0.5


    def timeit_Add_xy(self):
        x + y


    def timeit_Add_xyz(self):
        Add(*[x, y, z])


    def timeit_Mul_xy(self):
        x*y


    def timeit_Mul_xyz(self):
        Mul(*[x, y, z])


    def timeit_Div_xy(self):
        x/y


    def timeit_Div_2y(self):
        2/y

class TimeExpand:
    def timeit_expand_nothing_todo(self):
        p.expand(self)


    def bench_expand_32(self):
        """(x+y+z+1)**32  -> expand"""
        e.expand(self)


    def timeit_expand_complex_number_1(self):
        ((2 + 3*I)**1000).expand(complex=True)


    def timeit_expand_complex_number_2(self):
        ((2 + 3*I/4)**1000).expand(complex=True)
