# -*- coding: utf-8 -*-

from sympy.core import Add, Mul, symbols, I, Pow, S

x, y, z = symbols('x,y,z')

p = 3*x**2*y*z**7 + 7*x*y*z**2 + 4*x + x*y**4
e = (x + y + z + 1)**32

class TimeCoreArit:
    def time_neg(self):
        -x


    def time_Add_x1(self):
        x + 1


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

    def time_pow2(self):
        Pow(x, 2)

    def time_pow100(self):
        Pow(x, 100)

    def time_mod_pow(self):
        for x, y, z in [(4, 13, 497), (4, -3, 497), (3.2, 2.1, 1.9)]:
            pow(S(x), y, z)
            pow(S(x), S(y), z)
            pow(S(x), y, S(z))
            pow(S(x), S(y), S(z))

    def time_pow_im(self):
        (2*x*I)**(7/3)
