# -*- coding: utf-8 -*-
"""Benchmarks for SymPy numeric types: Integer, Rational, and utility functions.

Migrated from sympy/core/benchmarks/bench_numbers.py.
"""

from sympy.core.numbers import Integer, Rational, pi, oo
from sympy.core.intfunc import integer_nthroot, igcd
from sympy.core.singleton import S

# Shared instances — created once at module import time.
i3 = Integer(3)
i4 = Integer(4)
r34 = Rational(3, 4)
q45 = Rational(4, 5)


class TimeInteger:
    """Benchmarks for Integer arithmetic, conversion, and comparison."""

    def time_create(self):
        Integer(2)

    def time_int_conversion(self):
        int(i3)

    def time_neg(self):
        -i3

    def time_neg_one(self):
        -S.One

    def time_abs(self):
        abs(i3)

    def time_abs_pi(self):
        abs(pi)

    def time_neg_oo(self):
        -oo

    def time_add_int(self):
        i3 + 1

    def time_add_Integer(self):
        i3 + i4

    def time_add_Rational(self):
        i3 + r34

    def time_sub(self):
        i3 - i3

    def time_mul_int(self):
        i3 * 4

    def time_mul_Integer(self):
        i3 * i4

    def time_mul_Rational(self):
        i3 * r34

    def time_eq_int(self):
        i3 == 3

    def time_eq_Rational(self):
        i3 == r34


class TimeRational:
    """Benchmarks for Rational arithmetic."""

    def time_add_int(self):
        r34 + 1

    def time_add_Rational(self):
        r34 + q45


class TimeNumberUtils:
    """Benchmarks for integer utility functions: igcd and integer_nthroot."""

    def time_igcd_coprime(self):
        igcd(23, 17)

    def time_igcd_multiple(self):
        igcd(60, 3600)

    def time_nthroot(self):
        integer_nthroot(100, 2)
