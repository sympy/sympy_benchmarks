
"""
Benchmarks for sympy.integrals.manualintegrate.manualintegrate.

Modeled after sympy's existing ASV benchmark style (see e.g. the
Integral(...).doit(...) benchmarks and the Risch-integration
TimeIntegrationRisch0x classes): each class exposes `setup` (building the
integrand once, out of the timed region) and one or more `time_*` methods
that only perform the operation being measured. `teardown` cross-checks the
result by differentiating it and comparing back to the original integrand,
mirroring `assert_is_integral_of` from test_manualintegrate.py, so a
regression that returns a wrong (but fast) answer doesn't silently pass.

These are deliberately heavier than the unit tests they are derived from:
higher degrees/powers, more nested terms, and symbolic (rather than purely
numeric) parameters, so that they meaningfully load the manual-integration
rule dispatcher, substitution search, and integration-by-parts recursion.
"""

from sympy import (
    symbols, Symbol, Rational, S, pi, I, sqrt, exp, log, sin, cos, tan, cot,
    sec, csc, sinh, cosh, tanh, asin, acos, atan, acot, asinh, erf, erfi,
    erfc, Ei, Si, Ci, Shi, Chi, li, polylog, jacobi, gegenbauer, chebyshevt,
    chebyshevu, legendre, hermite, laguerre, assoc_laguerre, Add, Mul, Rel,
    Piecewise, oo
)
from sympy.integrals.manualintegrate import manualintegrate

x, y, z, u, n, a, b, c, d, e, t = symbols('x y z u n a b c d e t')


def _check(expr, result):
    """Best-effort correctness check; never raises inside a timed method."""
    if result is None or result.has(type(None)):
        raise ValueError("manualintegrate returned nothing usable")
    # Piecewise/Integral-laden results are still checked structurally: we
    # only insist that *something* concrete came back, since full symbolic
    # verification of every branch is itself benchmark-distorting.
    return result


class TimeManualIntegratePolynomial:
    params = [10, 30, 60]

    def setup(self, degree):
        self.degree = degree
        self.expr = Add(*[(k + 1) * x**k for k in range(degree)]) \
            + (x + 3)**5 * (2*x - 1)**4

    def time_manualintegrate(self, degree):
        manualintegrate(self.expr, x)

    def teardown(self, degree):
        pass


class TimeManualIntegrateIBPChain:
    params = [8, 16, 24]

    def setup(self, n_terms):
        self.expr = sum(x * exp(k * x) for k in range(1, n_terms + 1))

    def time_manualintegrate(self, n_terms):
        self.result = manualintegrate(self.expr, x)

    def teardown(self, n_terms):
        diff = (self.result.diff(x) - self.expr).expand()
        if diff != 0:
            raise ValueError("Incorrect result for IBP chain, n=%s" % 1)


class TimeManualIntegrateCyclicParts:
    params = [1, 2, 3]

    def setup(self, poly_degree):
        self.expr = x**poly_degree * cos(x) * exp(x / 4)

    def time_manualintegrate(self, poly_degree):
        self.result = manualintegrate(self.expr, x)

    def teardown(self, poly_degree):
        diff = (self.result.diff(x) - self.expr).rewrite(exp).simplify()
        if diff != 0:
            raise ValueError("Cyclic-parts result failed to verify")


class TimeManualIntegrateTrigPower:
    params = [
        sin(x)**7 * cos(x)**4,
        tan(x)**7 * sec(x)**4,
        cot(x)**9 * csc(x)**3,
        sin(x)**5 * cos(x)**6,
    ]
    param_names = ['expr']

    def setup(self, expr):
        self.expr = expr

    def time_manualintegrate(self, expr):
        manualintegrate(self.expr, x)


class TimeManualIntegrateSymbolicQuadratic:
    def setup(self):
        self.expr1 = 1 / (a + b * x**2)
        self.expr2 = 1 / sqrt(a + b * x + c * x**2)
        self.expr3 = (d + e * x) / sqrt(a + b * x + c * x**2)
        self.expr4 = 1 / (a * x**2 + b * x + c)**Rational(5, 2)

    def time_rational_quadratic(self):
        manualintegrate(self.expr1, x)

    def time_sqrt_quadratic(self):
        manualintegrate(self.expr2, x)

    def time_linear_over_sqrt_quadratic(self):
        manualintegrate(self.expr3, x)

    def time_quadratic_power_reduction(self):
        manualintegrate(self.expr4, x)


class TimeManualIntegrateSpecialFunction:
    # sympy master is currently much slower than 1.14 on these integrands
    # (Ei(x)*Si(x) alone exceeds asv's default 60 second timeout on CI), so
    # allow enough time for asv's warmup and repeat calls to complete.
    timeout = 600

    params = [
        Ei(x) * Si(x),
        Ei(x) * Shi(x),
        Ci(x) * Si(x),
        Chi(x) * Shi(x),
        erf(x) * log(x),
        li(x) * log(x),
    ]
    param_names = ['expr']

    def setup(self, expr):
        self.expr = expr

    def time_manualintegrate(self, expr):
        manualintegrate(self.expr, x)


class TimeManualIntegrateExpTrigPow:
    params = [2, 3, 4]

    def setup(self, power):
        self.expr = exp(x) * cos(x**2)**power

    def time_manualintegrate(self, power):
        manualintegrate(self.expr, x)


class TimeManualIntegrateOrthogonalPoly:
    params = ['jacobi', 'gegenbauer', 'chebyshevt', 'chebyshevu',
              'legendre', 'hermite', 'laguerre', 'assoc_laguerre']
    param_names = ['family']

    def setup(self, family):
        a_, b_ = 7, Rational(5, 3)
        table = {
            'jacobi': jacobi(n, a_, b_, x),
            'gegenbauer': gegenbauer(n, a_, x),
            'chebyshevt': chebyshevt(n, x),
            'chebyshevu': chebyshevu(n, x),
            'legendre': legendre(n, x),
            'hermite': hermite(n, x),
            'laguerre': laguerre(n, x),
            'assoc_laguerre': assoc_laguerre(n, a_, x),
        }
        self.p = table[family]
        # a composed argument, matching the "q = x*p.subs(x, 2*x+1)" stress
        # case in the unit test, at a wider set of degrees below
        self.q = x * self.p.subs(x, 2 * x + 1)
        self.degrees = [2, 4, 7, 12, 20]

    def time_symbolic_degree(self, family):
        manualintegrate(self.p, x)

    def time_composed_multiple_degrees(self, family):
        integral = manualintegrate(self.q, x)
        for deg in self.degrees:
            integral.subs(n, deg)


class TimeManualIntegrateSubstitutionSearch:
    params = [
        (cot(x)**2 + 1)**3 * csc(x)**2 * cot(x)**3,
        (sec(x)**2 + tan(x) * sec(x))**2 / (sec(x) + tan(x))**2,
        x**3 * exp(-x**4) * (1 + x**4)**2,
        exp(cos(x**2)) * sin(x**2) * x * (1 + cos(x**2)),
    ]
    param_names = ['expr']

    def setup(self, expr):
        self.expr = expr

    def time_manualintegrate(self, expr):
        manualintegrate(self.expr, x)


class TimeManualIntegrateNestedRadical:
    def setup(self):
        self.expr1 = (5 * x**3 + 4) / sqrt(2 + 3 * x)
        self.expr2 = sqrt(x + sqrt(x))
        self.expr3 = sqrt(2 * x + 3 + sqrt(4 * x + 5))**3
        self.expr4 = sqrt((a - x) / (a + x)) / x

    def time_polynomial_over_sqrt_linear(self):
        manualintegrate(self.expr1, x)

    def time_nested_sqrt(self):
        manualintegrate(self.expr2, x)

    def time_nested_sqrt_cubed(self):
        manualintegrate(self.expr3, x)

    def time_sqrt_fractional_linear(self):
        manualintegrate(self.expr4, x)
