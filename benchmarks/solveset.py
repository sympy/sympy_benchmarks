from sympy.solvers.solveset import solveset
from sympy.core.symbol import Symbol
from sympy.functions.elementary.exponential import exp, log
from sympy.functions.elementary.trigonometric import sin, cos
from sympy.functions.elementary.miscellaneous import root
from sympy.core.singleton import S


class TimeSolvesetPolynomial:
    '''Benchmark for Solveset polynomial calculation'''

    params = [1,5,10]

    def setup(self,n):
        self.x = Symbol ('x')
        self.polynomial_eq = (self.x**(4*n)) - (self.x**(2*n)) + 1

    def time_polynomial_solveset_complexes(self, n):
        solveset(self.polynomial_eq, self.x, S.Complexes)

    def time_polynomial_solveset_reals(self,n):
        solveset(self.polynomial_eq, self.x, S.Reals)


class TimeSolvesetTrigonometric:
    '''Benchmark for Solveset Trigonometric functions calculation'''

    # Trigonometric functions increase their time complexity non-linearly. We use small params to test them:
    # param = 5 is an edge case (scaling from ~26ms to ~61ms), and param = 6 causes an ASV timeout.
    params = [1,2,5]

    def setup(self,n):
        self.x = Symbol('x')
        self.trigonometric_eq = sin(n * self.x) - cos(self.x)

    def time_trigonometric_solveset(self,n):
        solveset(self.trigonometric_eq, self.x)


class TimeSolvesetExponential:
    '''Benchmark for Solveset exponential functions calculation'''

    # Solveset quickly returns an EmptySet when the domain is real.
    # In contrast, evaluating infinite solutions in the complex domain takes significantly more time.
    params = [1,5,10]

    def setup(self,n):
        self.x = Symbol ('x')
        self.exponential_eq = exp(n * self.x) + 1

    def time_exponential_solveset_complexes(self,n):
        solveset(self.exponential_eq, self.x, S.Complexes)

    def time_exponential_solveset_reals(self,n):
        solveset(self.exponential_eq, self.x, S.Reals)


class TimeSolvesetRational:
    '''Benchmark for Solveset rational functions calculation'''

    params = [1,5,10]

    def setup(self,n):
        self.x = Symbol('x')
        self.rational_eq = (self.x**n - self.x - 1)/ (self.x - 2)

    def time_rational_solveset_reals(self,n):
        solveset(self.rational_eq, self.x, S.Reals)

    def time_rational_solveset_complex(self,n):
        solveset(self.rational_eq, self.x, S.Complexes)


class TimeSolvesetIrrational:
    '''Benchmark for Solveset irrational functions calculation'''

    # When the domain is complex, param = 10 is an edge case: causes an ASV timeout.
    # When the domain is real, solveset works perfectly and fast with every param.
    params = [1,5,8]

    def setup(self,n):
        self.x = Symbol('x')
        self.irrational_eq = root(self.x**n - self.x - 1, 4) + self.x

    def time_irrational_solveset_real(self,n):
        solveset(self.irrational_eq, self.x, S.Reals)

    def time_irrational_solveset_complex(self,n):
        solveset(self.irrational_eq, self.x, S.Complexes)


class TimeSolvesetLogarithm:
    '''Benchmark for Solveset logarithm functions calculation'''

    params = [1,5,10]

    def setup(self,n):
        self.x = Symbol('x')
        self.logarithm_eq = log(self.x**n) + log(self.x) - n

    def time_logarithm_solveset(self,n):
        solveset(self.logarithm_eq, self.x)
