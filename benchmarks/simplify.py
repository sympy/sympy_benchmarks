# -*- coding: utf-8 -*-

from sympy import (
    E,
    Rational,
    acos,
    asin,
    atan,
    cos,
    exp,
    gamma,
    log,
    pi,
    simplify,
    sin,
    sqrt,
    symbols,
    tan,
    trigsimp,
)
from sympy.simplify.fu import fu
from sympy.simplify.combsimp import combsimp
from sympy.simplify.gammasimp import gammasimp
from sympy.simplify.powsimp import powsimp
from sympy.simplify.radsimp import collect_sqrt, radsimp
from sympy.simplify.ratsimp import ratsimp

x, y, z = symbols("x y z")
a, b, c = symbols("a b c", positive=True)
n = symbols("n", integer=True, positive=True)


class TimeGeneralSimplify:
    """General-purpose simplify() benchmarks on common expression patterns."""

    expr_rational = (
        (x**2 - 1)/(x - 1)
        + (x**2 - 4)/(x - 2)
        + (x**2 - 9)/(x - 3)
        + (x**3 - y**3)/(x - y)
    )

    expr_mixed = (
        log(a*b) - log(a) - log(b)
        + sin(x)**2 + cos(x)**2
        + exp(log(y))
        + sqrt(c**2)
    )

    def time_simplify_rational_algebraic_mix(self):
        simplify(self.expr_rational)

    def time_simplify_trig_log_radical_mix(self):
        simplify(self.expr_mixed)


class TimeTrigSimplify:
    """Benchmarks for trigsimp/fu on dense trigonometric expressions."""

    dense_trig = (
        sin(x + y)**2 + cos(x + y)**2
        + sin(x - y)**2 + cos(x - y)**2
        + 2*sin(x)*cos(x)
        - sin(2*x)
        + tan(x) - sin(x)/cos(x)
    )

    inverse_trig = (
        asin(x) + acos(x) - pi/2
        + atan(x) + atan(1/x) - pi/2
    )

    params = [3, 6, 9]

    def setup(self, k):
        self.expand_trig = sum(trigsimp(self.dense_trig.subs(y, i*x)) for i in range(1, k + 1))

    def time_trigsimp_dense(self, k):
        trigsimp(self.expand_trig)

    def time_fu_dense(self, k):
        fu(self.expand_trig)

    def time_trigsimp_inverse_identities(self, k):
        trigsimp(self.inverse_trig.subs(x, Rational(1, k + 2)))


class TimeRationalSimplify:
    """Rational function simplification benchmarks."""

    params = [5, 10, 20]

    def setup(self, n_terms):
        terms = []
        for i in range(1, n_terms + 1):
            terms.append((x + i)/(x**2 - i**2))
            terms.append((x - i)/(x**2 - i**2))
        self.expr = sum(terms)

    def time_ratsimp_partial_fraction_sum(self, n_terms):
        ratsimp(self.expr)

    def time_simplify_partial_fraction_sum(self, n_terms):
        simplify(self.expr)


class TimePowerAndRadicalSimplify:
    """Power and radical simplification benchmarks."""

    expr_pow = (
        (a*b)**x*(a*b)**y*(a*b)**z
        / ((a**x)*(b**x)*(a**y)*(b**y))
    )

    expr_rad = (
        1/(sqrt(2) + sqrt(3) + sqrt(5))
        + 1/(sqrt(2) + sqrt(3) - sqrt(5))
        + 1/(sqrt(2) - sqrt(3) + sqrt(5))
    )

    def time_powsimp_symbolic_powers(self):
        powsimp(self.expr_pow)

    def time_radsimp_nested_denominators(self):
        radsimp(self.expr_rad)

    def time_collect_sqrt_nested_radicals(self):
        collect_sqrt(self.expr_rad.expand())


class TimeCombinatorialAndGammaSimplify:
    """Benchmarks targeting special-function simplification code paths."""

    expr_comb = (
        gamma(n + 3)/(gamma(n + 1)*(n + 2))
        + gamma(n + 2)/(gamma(n + 1)*(n + 1))
    )

    expr_gamma = (
        gamma(x + 3)/(gamma(x + 1)*(x + 2))
        + gamma(x + Rational(5, 2))/gamma(x + Rational(1, 2))
    )

    def time_combsimp_gamma_ratio(self):
        combsimp(self.expr_comb)

    def time_gammasimp_shifted_products(self):
        gammasimp(self.expr_gamma)


class TimeLogExpSimplify:
    """Simplification benchmarks for logarithm/exponential identities."""

    params = [5, 10, 20]

    def setup(self, n_terms):
        self.expr = sum(log(a**i * b**(n_terms - i)) for i in range(1, n_terms + 1))
        self.exp_expr = sum(exp(log(a + i)) - (a + i) for i in range(1, n_terms + 1))

    def time_simplify_log_sums(self, n_terms):
        simplify(self.expr)

    def time_simplify_exp_log_roundtrip(self, n_terms):
        simplify(self.exp_expr)
