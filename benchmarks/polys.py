from sympy import symbols, prod, prem, rem, degree, LC, subresultants, gcd
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
    """A pair of linearly dense quartic inputs with quadratic GCDs.

    This class generates benchmark examples with two polynomials, ``f`` and
    ``g``, that are linearly dense quartic polynomials with quadratic GCDs. The
    polynomials are constructed based on the input parameter ``n`.

    Examples
    ========

    >>> example = _LinearDenseQuadraticGCD(3)
    >>> f, g, d, syms = example.as_expr()
    >>> f
    (x - y1 - y2 - y3 - 2)**2*(x + y1 + y2 + y3 + 1)**2
    >>> g
    (x + y1 + y2 + y3 + 1)**2*(x + y1 + y2 + y3 + 2)**2
    >>> d
    (x + y1 + y2 + y3 + 1)**2
    >>> syms
    (x, y1, y2, y3)

    """

    def make_poly(self, n):
        x, *y = syms = symbols("x, y1:{}".format(n+1))
        d = (1 + x + sum(y[:n])) ** 2
        f = d * (-2 + x - sum(y[:n])) ** 2
        g = d * (2 + x + sum(y[:n])) ** 2
        return f, g, d, syms


class _SparseGCDHighDegree(_GCDExample):
    """A pair of polynomials in n symbols with a high degree sparse GCD.

    This class generates benchmark examples with two polynomials, ``f`` and
    ``g``, that have a high degree sparse GCD. The polynomials are constructed
    based on the input parameter ``n``.

    Examples
    ========

    >>> example = _SparseGCDHighDegree(3)
    >>> f, g, d, syms = example.as_expr()
    >>> f
    (x**4 + y1**4 + y2**4 + y3**4 - 2)*(x**4 + y1**4 + y2**4 + y3**4 + 1)
    >>> g
    (x**4 + y1**4 + y2**4 + y3**4 + 1)*(x**4 + y1**4 + y2**4 + y3**4 + 2)
    >>> d
    x**4 + y1**4 + y2**4 + y3**4 + 1
    >>> syms
    (x, y1, y2, y3)

    """

    def make_poly(self, n):
        x, *y = syms = symbols("x, y1:{}".format(n+1))
        d = 1 + x ** (n + 1) + sum([y[i] ** (n + 1) for i in range(n)])
        f = d * (-2 + x ** (n + 1) + sum([y[i] ** (n + 1) for i in range(n)]))
        g = d * (2 + x ** (n + 1) + sum([y[i] ** (n + 1) for i in range(n)]))
        return f, g, d, syms


class _QuadraticNonMonicGCD(_GCDExample):
    """A pair of quadratic polynomials with a non-monic GCD.

    This class generates benchmark examples with two quadratic polynomials,
    ``f`` and ``g``, that have a non-monic GCD. The polynomials are constructed
    based on the input parameter ``n``.

    Examples
    ========

    >>> example = _QuadraticNonMonicGCD(3)
    >>> f, g, d, syms = example.as_expr()
    >>> f
    (x**2*y1**2 + y2**2 + y3**2 + 1)*(x**2 - y1**2 + y2**2 + y3**2 - 1)
    >>> g
    (x*y1 + y2 + y3 + 2)**2*(x**2*y1**2 + y2**2 + y3**2 + 1)
    >>> d
    x**2*y1**2 + y2**2 + y3**2 + 1
    >>> syms
    (x, y1, y2, y3)

    """

    def make_poly(self, n):
        x, *y = syms = symbols("x, y1:{}".format(n+1))
        d = 1 + x ** 2 * y[0] ** 2 + sum([y[i] ** 2 for i in range(1, n)])
        f = d * (-1 + x ** 2 - y[0] ** 2 + sum([y[i] ** 2 for i in range(1, n)]))
        g = d * (2 + x * y[0] + sum(y[1:n])) ** 2
        return f, g, d, syms


class _SparseNonMonicQuadratic(_GCDExample):
    """A pair of sparse non-monic quadratic polynomials with linear GCDs.

    This class generates benchmark examples with two sparse non-monic quadratic
    polynomials, ``f`` and ``g``, that have a linear GCD. The polynomials are
    constructed based on the input parameter ``n``.

    Examples
    ========

    >>> example = _SparseNonMonicQuadratic(3)
    >>> f, g, d, syms = example.as_expr()
    >>> f
    (x*y1*y2*y3 - 1)*(x*y1*y2*y3 + 3)
    >>> g
    (x*y1*y2*y3 - 3)*(x*y1*y2*y3 - 1)
    >>> d
    x*y1*y2*y3 - 1
    >>> syms
    (x, y1, y2, y3)

    """

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
            if isinstance(expected, list):
                # some methods output a list of polynomials
                expected = [examples.to_poly(p) for p in expected]
            else:
                # others output only a single polynomial.
                expected = examples.to_poly(expected)

        elif impl == 'sparse':
            func = self.get_func_sparse(*examples.as_ring())
            if isinstance(expected, list):
                expected = [examples.to_ring(p) for p in expected]
            else:
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
    """This case involves linearly dense quartic inputs with quadratic GCDs.
    The quadratic GCD suggests that the pseudo remainder method could be
    applicable and potentially efficient for computing the GCD of these
    polynomials."""

    GCDExampleCLS = _LinearDenseQuadraticGCD
    # This case is slow for n>5.
    params = [(1, 3, 5), ('expr', 'dense', 'sparse')]


class TimePREM_QuadraticNonMonicGCD(_TimePREM):
    """This case deals with quadratic polynomials having a non-monic GCD. The
    non-monic aspect may introduce additional complexities, but the quadratic
    nature suggests that the pseudo remainder method could be useful.
    """

    GCDExampleCLS = _QuadraticNonMonicGCD
    # This case is slow for n>5.
    params = [(1, 3, 5), ('expr', 'dense', 'sparse')]


class _TimeSUBRESULTANTS(_TimeOP):
    """Benchmarks for subresultants PRS method"""

    def expected(self, f, g, d, syms):
        x = syms[0]
        subresultant = subresultants(f, g, x)

        return subresultant

    def get_func_expr(self, f, g, d, syms):
        x = syms[0]
        return lambda: subresultants(f, g, x)

    def get_func_poly(self, f, g, d):
        return lambda: f.subresultants(g)

    def get_func_sparse(self, f, g, d, ring):
        return lambda: f.subresultants(g)


class TimeSUBRESULTANTS_LinearDenseQuadraticGCD(_TimeSUBRESULTANTS):
    GCDExampleCLS = _LinearDenseQuadraticGCD
    # This case is slow for n>3.
    params = [(1, 2, 3), ('expr', 'dense', 'sparse')]


class TimeSUBRESULTANTS_SparseGCDHighDegree(_TimeSUBRESULTANTS):
    GCDExampleCLS = _SparseGCDHighDegree
    params = [(1, 3, 5), ('expr', 'dense', 'sparse')]


class TimeSUBRESULTANTS_QuadraticNonMonicGCD(_TimeSUBRESULTANTS):
    GCDExampleCLS = _QuadraticNonMonicGCD
    # This case is slow for n>3.
    params = [(1, 2, 3), ('expr', 'dense', 'sparse')]


class TimeSUBRESULTANTS_SparseNonMonicQuadratic(_TimeSUBRESULTANTS):
    GCDExampleCLS = _SparseNonMonicQuadratic
    params = [(1, 3, 5), ('expr', 'dense', 'sparse')]


class _TimeGCD(_TimeOP):
    """Benchmarks for GCDs method"""

    def expected(self, f, g, d, syms):
        x = syms[0]
        gcd = gcd(f, g, x)

        return gcd

    def get_func_expr(self, f, g, d, syms):
        x = syms[0]
        return lambda: gcd(f, g, x)

    def get_func_poly(self, f, g, d):
        return lambda: f.gcd(g)

    def get_func_sparse(self, f, g, d, ring):
        return lambda: f.gcd(g)


class TimeGCD_LinearDenseQuadraticGCD(_TimeGCD):
    GCDExampleCLS = _LinearDenseQuadraticGCD
    # This case is slow for n>3.
    params = [(1, 2, 3), ('expr', 'dense', 'sparse')]


class TimeGCD_SparseGCDHighDegree(_TimeGCD):
    GCDExampleCLS = _SparseGCDHighDegree
    params = [(1, 3, 5), ('expr', 'dense', 'sparse')]


class TimeGCD_QuadraticNonMonicGCD(_TimeGCD):
    GCDExampleCLS = _QuadraticNonMonicGCD
    # This case is slow for n>3.
    params = [(1, 2, 3), ('expr', 'dense', 'sparse')]


class TimeGCD_SparseNonMonicQuadratic(_TimeGCD):
    GCDExampleCLS = _SparseNonMonicQuadratic
    params = [(1, 3, 5), ('expr', 'dense', 'sparse')]