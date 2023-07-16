from sympy import symbols, prod, prem, rem, degree, LC, subresultants, resultant
from sympy.polys import QQ, Poly


class TimePolyManyGens:
    """Time using a Poly with many generators"""

    params = [1, 10, 100, 500]

    def setup(self, n):
        self.xs = symbols('x:{}'.format(n))
        self.x = self.xs[n // 2]
        self.px = Poly(self.x, self.xs)

    def time_create_poly(self, n):
        Poly(self.x, self.xs)

    def time_is_linear(self, n):
        self.px.is_linear


class _GCDExample:
    """A benchmark example with two polynomials and their gcd."""

    def __init__(self, n):
        f, g, d, syms = self.make_poly(n)
        self.f = f
        self.g = g
        self.d = d
        self.x = syms[0]
        self.y = syms[1:]
        self.syms = syms
        self.ring = QQ[syms]

    def to_expr(self, expr):
        return expr

    def to_poly(self, expr):
        return Poly(expr, self.syms)

    def to_ring(self, expr):
        return self.ring(expr)

    def as_expr(self):
        return (self.f, self.g, self.d, self.syms)

    def as_poly(self):
        return (self.to_poly(self.f), self.to_poly(self.g), self.to_poly(self.d))

    def as_ring(self):
        return (self.to_ring(self.f), self.to_ring(self.g), self.to_ring(self.d), self.ring)


class _LinearDenseQuadraticGCD(_GCDExample):
    """A pair of linearly dense quartic inputs with quadratic GCDs"""

    def make_poly(self, n):
        x, *y = syms = symbols("x, y1:{}".format(n+1))
        d = (1 + x + sum(y[:n])) ** 2
        f = d * (-2 + x - sum(y[:n])) ** 2
        g = d * (2 + x + sum(y[:n])) ** 2
        return f, g, d, syms


class _SparseGCDHighDegree(_GCDExample):
    """A pair of polynomials in n symbols with a high degree sparse GCD."""

    def make_poly(self, n):
        x, *y = syms = symbols("x, y1:{}".format(n+1))
        d = 1 + x ** (n + 1) + sum([y[i] ** (n + 1) for i in range(n)])
        f = d * (-2 + x ** (n + 1) + sum([y[i] ** (n + 1) for i in range(n)]))
        g = d * (2 + x ** (n + 1) + sum([y[i] ** (n + 1) for i in range(n)]))
        return f, g, d, syms


class _QuadraticNonMonicGCD(_GCDExample):
    """A pair of quadratic polynomials with a non-monic GCD."""

    def make_poly(self, n):
        x, *y = syms = symbols("x, y1:{}".format(n+1))
        d = 1 + x ** 2 * y[0] ** 2 + sum([y[i] ** 2 for i in range(1, n)])
        f = d * (-1 + x ** 2 - y[0] ** 2 + sum([y[i] ** 2 for i in range(1, n)]))
        g = d * (2 + x * y[0] + sum(y[1:n])) ** 2
        return f, g, d, syms


class _SparseNonMonicQuadratic(_GCDExample):
    """A pair of sparse non-monic quadratic polynomials with linear GCDs."""

    def make_poly(self, n):
        x, *y = syms = symbols("x, y1:{}".format(n+1))
        d = -1 + x * prod(y[:n])
        f = d * (3 + x * prod(y[:n]))
        g = d * (-3 + x * prod(y[:n]))
        return f, g, d, syms


class _TimeOP:
    """
    Benchmarks comparing Poly implementations of a given operation.
    """
    param_names = [
        'size',
        'impl',
    ]

    def setup(self, n, impl):

        examples = self.GCDExampleCLS(n)

        expected = self.expected(*examples.as_expr())

        if impl == 'expr':
            func = self.get_func_expr(*examples.as_expr())
            expected = examples.to_expr(expected)
        elif impl == 'dense':
            func = self.get_func_poly(*examples.as_poly())
            expected = examples.to_poly(expected)
        elif impl == 'sparse':
            func = self.get_func_sparse(*examples.as_ring())
            expected = examples.to_ring(expected)

        self.func = func
        self.expected_result = expected

    def time_op(self, n, impl):
        self.returned_result = self.func()

    def teardown(self, n, impl):
        assert self.expected_result == self.returned_result


class _TimePREM(_TimeOP):

    def expected(self, f, g, d, syms):
        x = syms[0]
        prem_f_g_x = rem(f * LC(g, x) ** (degree(f, x) - degree(g, x) + 1), g, x)
        return prem_f_g_x

    def get_func_expr(self, f, g, d, syms):
        x = syms[0]
        return lambda: prem(f, g, x)

    def get_func_poly(self, f, g, d):
        return lambda: f.prem(g)

    def get_func_sparse(self, f, g, d, ring):
        return lambda: f.prem(g)


class TimePREM_LinearDenseQuadraticGCD(_TimePREM):
    GCDExampleCLS = _LinearDenseQuadraticGCD
    params = [(1, 3, 5), ('expr', 'dense', 'sparse')] # This case is slow for n=8.


class TimePREM_SparseGCDHighDegree(_TimePREM):
    GCDExampleCLS = _SparseGCDHighDegree
    params = [(1, 3, 5, 8), ('expr', 'dense', 'sparse')]


class TimePREM_QuadraticNonMonicGCD(_TimePREM):
    GCDExampleCLS = _QuadraticNonMonicGCD
    params = [(1, 3, 5), ('expr', 'dense', 'sparse')] # This case is slow for n=8.


class TimePREM_SparseNonMonicQuadratic(_TimePREM):
    GCDExampleCLS = _SparseNonMonicQuadratic
    params = [(1, 3, 5, 8), ('expr', 'dense', 'sparse')]


class _TimeSUBRESULTANTS(_TimeOP):
    """Benchmarks for pseudo-quotient method"""

    def expected(self, f, g, d, syms):
        x = syms[0]
        subresultant = resultant(f * LC(g, x) ** (degree(f, x) - degree(g, x) + 1), g, x)
        return [f, g, subresultant]

    def get_func_expr(self, f, g, d, syms):
        x = syms[0]
        return lambda: subresultants(f, g, x)

    def get_func_poly(self, f, g, d):
        return lambda: f.subresultants(g)

    def get_func_sparse(self, f, g, d, ring):
        return lambda: f.subresultants(g)


class TimeSUBRESULTANTS_LinearDenseQuadraticGCD(_TimeSUBRESULTANTS):
    GCDExampleCLS = _LinearDenseQuadraticGCD
    params = [(1, 3, 5), ('expr', 'dense', 'sparse')] # This case is slow for n=8.


class TimeSUBRESULTANTS_SparseGCDHighDegree(_TimeSUBRESULTANTS):
    GCDExampleCLS = _SparseGCDHighDegree
    params = [(1, 3, 5, 8), ('expr', 'dense', 'sparse')]


class TimeSUBRESULTANTS_QuadraticNonMonicGCD(_TimeSUBRESULTANTS):
    GCDExampleCLS = _QuadraticNonMonicGCD
    params = [(1, 3, 5), ('expr', 'dense', 'sparse')] # This case is slow for n=8.


class TimeSUBRESULTANTS_SparseNonMonicQuadratic(_TimeSUBRESULTANTS):
    GCDExampleCLS = _SparseNonMonicQuadratic
    params = [(1, 3, 5, 8), ('expr', 'dense', 'sparse')]