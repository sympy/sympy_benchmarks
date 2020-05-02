# -*- coding: utf-8 -*-

from sympy import sin
from sympy.core import Add, Mul, symbols, I, Pow, S, Symbol

x, y, z = symbols('x,y,z')

p = 3*x**2*y*z**7 + 7*x*y*z**2 + 4*x + x*y**4
e = (x + y + z + 1)**32

class Time_Arit:
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

class Time_assumption:

    def setup(self):
        self.ncx = Symbol("x", commutative=False)
        self.ncy = Symbol("y", commutative=False)
        self.k_i = Symbol('k', integer=True)
        self.x_f = Symbol('x', extended_real=True, finite=False)

    def time_ncmul(self):
        self.ncx*self.ncy != self.ncy*self.ncx
        self.ncx*self.ncy*3 == 3*self.ncx*self.ncy

    def time_ncpow(self):
        (x**2)*(y**2) != (y**2)*(x**2)
        2**x*2**(2*x) == 2**(3*x)

    def time_Add_Mul_is_integer(self):
        (self.k_i + 1).is_integer
        (2*self.k_i).is_integer
        (self.k_i/3).is_integer

    def time_Add_Mul_is_finite(self):
        sin(self.x_f).is_finite
        (self.x_f*sin(self.x_f)).is_finite
        (sin(self.x_f) - 67).is_finite
