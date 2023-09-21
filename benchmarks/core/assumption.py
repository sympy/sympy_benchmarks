# -*- coding: utf-8 -*-

from sympy import pi, oo
from sympy.core import Symbol
from sympy.core import Symbol, S, Rational, Integer


class Time_assumption:

    def setup(self):
        self.x = Symbol('x', real=True, integer=True)
        self.z_0 = Integer(0)
        self.z_1 = Integer(1)
        self.z__1 = Integer(-1)
        self.oo = S.Infinity
        self.mm = S.NegativeInfinity
        self.zoo = S.ComplexInfinity
        self.nan = S.NaN
        self.r_pos = Rational(3, 4)
        self.r_neg = Rational(-3, 4)
        self.pi = S.Pi
        self.ex = S.Exp1
        self.I = S.ImaginaryUnit
        self.a_1 = Symbol('a', real=False)
        self.a_2 = Symbol('a', extended_real=False)
        self.a_3 = Symbol('a', imaginary=True)
        self.x_0 = Symbol('x', zero=True)
        self.x_1 = Symbol('x', positive=True)
        self.x_2 = Symbol('x', nonpositive=True)
        self.x_3 = Symbol('x', positive=False)

    def time_symbol_unset(self):

        self.x.is_real is True
        self.x.is_integer is True
        self.x.is_imaginary is False
        self.x.is_noninteger is False
        self.x.is_number is False


    def time_zero(self):

	    self.z_0.is_commutative is True
	    self.z_0.is_integer is True
	    self.z_0.is_rational is True
	    self.z_0.is_algebraic is True
	    self.z_0.is_transcendental is False
	    self.z_0.is_real is True
	    self.z_0.is_complex is True
	    self.z_0.is_noninteger is False
	    self.z_0.is_irrational is False
	    self.z_0.is_imaginary is False
	    self.z_0.is_positive is False
	    self.z_0.is_negative is False
	    self.z_0.is_nonpositive is True
	    self.z_0.is_nonnegative is True
	    self.z_0.is_even is True
	    self.z_0.is_odd is False
	    self.z_0.is_finite is True
	    self.z_0.is_infinite is False
	    self.z_0.is_comparable is True
	    self.z_0.is_prime is False
	    self.z_0.is_composite is False
	    self.z_0.is_number is True


    def time_one(self):

	    self.z_1.is_commutative is True
	    self.z_1.is_integer is True
	    self.z_1.is_rational is True
	    self.z_1.is_algebraic is True
	    self.z_1.is_transcendental is False
	    self.z_1.is_real is True
	    self.z_1.is_complex is True
	    self.z_1.is_noninteger is False
	    self.z_1.is_irrational is False
	    self.z_1.is_imaginary is False
	    self.z_1.is_positive is True
	    self.z_1.is_negative is False
	    self.z_1.is_nonpositive is False
	    self.z_1.is_nonnegative is True
	    self.z_1.is_even is False
	    self.z_1.is_odd is True
	    self.z_1.is_finite is True
	    self.z_1.is_infinite is False
	    self.z_1.is_comparable is True
	    self.z_1.is_prime is False
	    self.z_1.is_number is True
	    self.z_1.is_composite is False


    def time_negativeone(self):

	    self.z__1.is_commutative is True
	    self.z__1.is_integer is True
	    self.z__1.is_rational is True
	    self.z__1.is_algebraic is True
	    self.z__1.is_transcendental is False
	    self.z__1.is_real is True
	    self.z__1.is_complex is True
	    self.z__1.is_noninteger is False
	    self.z__1.is_irrational is False
	    self.z__1.is_imaginary is False
	    self.z__1.is_positive is False
	    self.z__1.is_negative is True
	    self.z__1.is_nonpositive is True
	    self.z__1.is_nonnegative is False
	    self.z__1.is_even is False
	    self.z__1.is_odd is True
	    self.z__1.is_finite is True
	    self.z__1.is_infinite is False
	    self.z__1.is_comparable is True
	    self.z__1.is_prime is False
	    self.z__1.is_composite is False
	    self.z__1.is_number is True

    def time_infinity(self):

	    self.oo.is_commutative is True
	    self.oo.is_integer is False
	    self.oo.is_rational is False
	    self.oo.is_algebraic is False
	    self.oo.is_transcendental is False
	    self.oo.is_extended_real is True
	    self.oo.is_real is False
	    self.oo.is_complex is False
	    self.oo.is_noninteger is True
	    self.oo.is_irrational is False
	    self.oo.is_imaginary is False
	    self.oo.is_nonzero is False
	    self.oo.is_positive is False
	    self.oo.is_negative is False
	    self.oo.is_nonpositive is False
	    self.oo.is_nonnegative is False
	    self.oo.is_extended_nonzero is True
	    self.oo.is_extended_positive is True
	    self.oo.is_extended_negative is False
	    self.oo.is_extended_nonpositive is False
	    self.oo.is_extended_nonnegative is True
	    self.oo.is_even is False
	    self.oo.is_odd is False
	    self.oo.is_finite is False
	    self.oo.is_infinite is True
	    self.oo.is_comparable is True
	    self.oo.is_prime is False
	    self.oo.is_composite is False
	    self.oo.is_number is True

    def time_neg_infinity(self):

	    self.mm.is_commutative is True
	    self.mm.is_integer is False
	    self.mm.is_rational is False
	    self.mm.is_algebraic is False
	    self.mm.is_transcendental is False
	    self.mm.is_extended_real is True
	    self.mm.is_real is False
	    self.mm.is_complex is False
	    self.mm.is_noninteger is True
	    self.mm.is_irrational is False
	    self.mm.is_imaginary is False
	    self.mm.is_nonzero is False
	    self.mm.is_positive is False
	    self.mm.is_negative is False
	    self.mm.is_nonpositive is False
	    self.mm.is_nonnegative is False
	    self.mm.is_extended_nonzero is True
	    self.mm.is_extended_positive is False
	    self.mm.is_extended_negative is True
	    self.mm.is_extended_nonpositive is True
	    self.mm.is_extended_nonnegative is False
	    self.mm.is_even is False
	    self.mm.is_odd is False
	    self.mm.is_finite is False
	    self.mm.is_infinite is True
	    self.mm.is_comparable is True
	    self.mm.is_prime is False
	    self.mm.is_composite is False
	    self.mm.is_number is True

    def time_zoo(self):

	    self.zoo.is_complex is False
	    self.zoo.is_real is False
	    self.zoo.is_prime is False

    def time_nan(self):

	    self.nan.is_commutative is True
	    self.nan.is_integer is None
	    self.nan.is_rational is None
	    self.nan.is_algebraic is None
	    self.nan.is_transcendental is None
	    self.nan.is_real is None
	    self.nan.is_complex is None
	    self.nan.is_noninteger is None
	    self.nan.is_irrational is None
	    self.nan.is_imaginary is None
	    self.nan.is_positive is None
	    self.nan.is_negative is None
	    self.nan.is_nonpositive is None
	    self.nan.is_nonnegative is None
	    self.nan.is_even is None
	    self.nan.is_odd is None
	    self.nan.is_finite is None
	    self.nan.is_infinite is None
	    self.nan.is_comparable is False
	    self.nan.is_prime is None
	    self.nan.is_composite is None
	    self.nan.is_number is True

    def time_pos_rational(self):

	    self.r_pos.is_commutative is True
	    self.r_pos.is_integer is False
	    self.r_pos.is_rational is True
	    self.r_pos.is_algebraic is True
	    self.r_pos.is_transcendental is False
	    self.r_pos.is_real is True
	    self.r_pos.is_complex is True
	    self.r_pos.is_noninteger is True
	    self.r_pos.is_irrational is False
	    self.r_pos.is_imaginary is False
	    self.r_pos.is_positive is True
	    self.r_pos.is_negative is False
	    self.r_pos.is_nonpositive is False
	    self.r_pos.is_nonnegative is True
	    self.r_pos.is_even is False
	    self.r_pos.is_odd is False
	    self.r_pos.is_finite is True
	    self.r_pos.is_infinite is False
	    self.r_pos.is_comparable is True
	    self.r_pos.is_prime is False
	    self.r_pos.is_composite is False

    def time_neg_rational(self):

	    self.r_neg.is_positive is False
	    self.r_neg.is_nonpositive is True
	    self.r_neg.is_negative is True
	    self.r_neg.is_nonnegative is False

    def time_pi(self):

	    self.pi.is_commutative is True
	    self.pi.is_integer is False
	    self.pi.is_rational is False
	    self.pi.is_algebraic is False
	    self.pi.is_transcendental is True
	    self.pi.is_real is True
	    self.pi.is_complex is True
	    self.pi.is_noninteger is True
	    self.pi.is_irrational is True
	    self.pi.is_imaginary is False
	    self.pi.is_positive is True
	    self.pi.is_negative is False
	    self.pi.is_nonpositive is False
	    self.pi.is_nonnegative is True
	    self.pi.is_even is False
	    self.pi.is_odd is False
	    self.pi.is_finite is True
	    self.pi.is_infinite is False
	    self.pi.is_comparable is True
	    self.pi.is_prime is False
	    self.pi.is_composite is False

    def time_E(self):

	    self.ex.is_commutative is True
	    self.ex.is_integer is False
	    self.ex.is_rational is False
	    self.ex.is_algebraic is False
	    self.ex.is_transcendental is True
	    self.ex.is_real is True
	    self.ex.is_complex is True
	    self.ex.is_noninteger is True
	    self.ex.is_irrational is True
	    self.ex.is_imaginary is False
	    self.ex.is_positive is True
	    self.ex.is_negative is False
	    self.ex.is_nonpositive is False
	    self.ex.is_nonnegative is True
	    self.ex.is_even is False
	    self.ex.is_odd is False
	    self.ex.is_finite is True
	    self.ex.is_infinite is False
	    self.ex.is_comparable is True
	    self.ex.is_prime is False
	    self.ex.is_composite is False

    def time_I(self):

	    self.I.is_commutative is True
	    self.I.is_integer is False
	    self.I.is_rational is False
	    self.I.is_algebraic is True
	    self.I.is_transcendental is False
	    self.I.is_real is False
	    self.I.is_complex is True
	    self.I.is_noninteger is False
	    self.I.is_irrational is False
	    self.I.is_imaginary is True
	    self.I.is_positive is False
	    self.I.is_negative is False
	    self.I.is_nonpositive is False
	    self.I.is_nonnegative is False
	    self.I.is_even is False
	    self.I.is_odd is False
	    self.I.is_finite is True
	    self.I.is_infinite is False
	    self.I.is_comparable is False
	    self.I.is_prime is False
	    self.I.is_composite is False

    def time_symbol_real_false(self):

	    self.a_1.is_real is False
	    self.a_1.is_integer is False
	    self.a_1.is_zero is False

	    self.a_1.is_negative is False
	    self.a_1.is_positive is False
	    self.a_1.is_nonnegative is False
	    self.a_1.is_nonpositive is False
	    self.a_1.is_nonzero is False

	    self.a_1.is_extended_negative is None
	    self.a_1.is_extended_positive is None
	    self.a_1.is_extended_nonnegative is None
	    self.a_1.is_extended_nonpositive is None
	    self.a_1.is_extended_nonzero is None

    def time_symbol_extended_real_false(self):

	    self.a_2.is_real is False
	    self.a_2.is_integer is False
	    self.a_2.is_zero is False

	    self.a_2.is_negative is False
	    self.a_2.is_positive is False
	    self.a_2.is_nonnegative is False
	    self.a_2.is_nonpositive is False
	    self.a_2.is_nonzero is False

	    self.a_2.is_extended_negative is False
	    self.a_2.is_extended_positive is False
	    self.a_2.is_extended_nonnegative is False
	    self.a_2.is_extended_nonpositive is False
	    self.a_2.is_extended_nonzero is False

    def time_symbol_imaginary(self):

	    self.a_3.is_real is False
	    self.a_3.is_integer is False
	    self.a_3.is_negative is False
	    self.a_3.is_positive is False
	    self.a_3.is_nonnegative is False
	    self.a_3.is_nonpositive is False
	    self.a_3.is_zero is False
	    self.a_3.is_nonzero is False

    def time_symbol_zero(self):

	    self.x_0.is_positive is False
	    self.x_0.is_nonpositive
	    self.x_0.is_negative is False
	    self.x_0.is_nonnegative
	    self.x_0.is_zero is True
	    self.x_0.is_nonzero is False
	    self.x_0.is_finite is True

    def time_symbol_positive(self):

	    self.x_1.is_positive is True
	    self.x_1.is_nonpositive is False
	    self.x_1.is_negative is False
	    self.x_1.is_nonnegative is True
	    self.x_1.is_zero is False
	    self.x_1.is_nonzero is True		

    def time_neg_symbol_positive(self):

        -self.x_1.is_positive is False
        -self.x_1.is_nonpositive is True
        -self.x_1.is_negative is True
        -self.x_1.is_nonnegative is False
        -self.x_1.is_zero is False
        -self.x_1.is_nonzero is True


    def time_symbol_nonpositive(self):

        self.x_2.is_positive is False
        self.x_2.is_nonpositive is True
        self.x_2.is_negative is None
        self.x_2.is_nonnegative is None
        self.x_2.is_zero is None
        self.x_2.is_nonzero is None


    def time_neg_symbol_nonpositive(self):

        (-self.x_2).is_positive is None
        (-self.x_2).is_nonpositive is None
        (-self.x_2).is_negative is False
        (-self.x_2).is_nonnegative is True
        (-self.x_2).is_zero is None
        (-self.x_2).is_nonzero is None


    def test_symbol_falsepositive(self):

        self.x_3.is_positive is False
        self.x_3.is_nonpositive is None
        self.x_3.is_negative is None
        self.x_3.is_nonnegative is None
        self.x_3.is_zero is None
        self.x_3.is_nonzero is None
