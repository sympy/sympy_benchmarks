from sympy import symbols, prod, prem, rem, degree, LC
from sympy.polys import ZZ, Poly

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


class _LinearDenseQuadraticGCD:
    def setup_polys(self, n):
        x, *y = symbols("x, y1:{}".format(n+1))
        R = ZZ[[x] + list(y)]
        D = (1 + x + sum(y[:n])) ** 2
        f = D * (-2 + x - sum(y[:n])) ** 2
        g = D * (2 + x + sum(y[:n])) ** 2
        fp, gp = Poly(f, x, *y[:n]), Poly(g, x, *y[:n])
        fpe, gpe = R.from_sympy(f), R.from_sympy(g)
        return f, g, fp, gp, fpe, gpe, x, y, R


class _SparseGCDHighDegree:
    def setup_polys(self, n):
        x, *y = symbols("x, y1:{}".format(n+1))
        R = ZZ[[x] + list(y)]
        D = 1 + x ** (n + 1) + sum([y[i] ** (n + 1) for i in range(n)])
        f = D * (-2 + x ** (n + 1) + sum([y[i] ** (n + 1) for i in range(n)]))
        g = D * (2 + x ** (n + 1) + sum([y[i] ** (n + 1) for i in range(n)]))
        fp, gp = Poly(f, x, *y[:n]), Poly(g, x, *y[:n])
        fpe, gpe = R.from_sympy(f), R.from_sympy(g)
        return f, g, fp, gp, fpe, gpe, x, y, R


class _QuadraticNonMonicGCD:
    def setup_polys(self, n):
        x, *y = symbols("x, y1:{}".format(n+1))
        R = ZZ[[x] + list(y)]
        D = 1 + x ** 2 * y[0] ** 2 + sum([y[i] ** 2 for i in range(1, n)])
        f = D * (-1 + x ** 2 - y[0] ** 2 + sum([y[i] ** 2 for i in range(1, n)]))
        g = D * (2 + x * y[0] + sum(y[1:n])) ** 2
        fp, gp = Poly(f, x, *y[:n]), Poly(g, x, *y[:n])
        fpe, gpe = R.from_sympy(f), R.from_sympy(g)
        return f, g, fp, gp, fpe, gpe, x, y, R


class _SparseNonMonicQuadratic:
    def setup_polys(self, n):
        x, *y = symbols("x, y1:{}".format(n+1))
        R = ZZ[[x] + list(y)]
        D = -1 + x * prod(y[:n])
        f = D * (3 + x * prod(y[:n]))
        g = D * (-3 + x * prod(y[:n]))
        fp, gp = Poly(f, x, *y[:n]), Poly(g, x, *y[:n])
        fpe, gpe = R.from_sympy(f), R.from_sympy(g)
        return f, g, fp, gp, fpe, gpe, x, y, R


class _TimePREM:
    def setup(self, n, method):
        (f, g, fp, gp, fpe, gpe, x, y, R) = self.setup_polys(n)

        self.values = {}

        prem_f_g_x = rem(f * LC(g, x) ** (degree(f, x) - degree(g, x) + 1), g, x)

        if method == 'prem':
            self.func = lambda: prem(f, g, x)
            self.expected = prem_f_g_x

        elif method == 'poly':
            self.func = lambda: fp.prem(gp)
            self.expected = prem_f_g_x

        elif method == 'sparse':
            self.func = lambda: fpe.prem(gpe)
            self.expected = R(prem_f_g_x.as_expr())

    def teardown(self, n, method):
        self.result = self.values[method]  # Get the result for the current method

        if method == 'prem':
            assert self.result == self.expected

        elif method == 'poly':
            assert self.result == self.expected

        elif method == 'sparse':
            assert self.result == self.expected

    def time_prem_methods(self, n, method):
        self.values[str(method)] = self.func()

    param_names = ['degree', 'Implementation_methods']


class TimePREMLinearDenseQuadraticGCD(_LinearDenseQuadraticGCD, _TimePREM):
    """Calculate time for Linearly dense quartic inputs with quadratic GCDs polynomials."""

    params = [(1, 3 , 5), ('prem', 'poly', 'sparse')] # This case is slow for n=8.


class TimePREMQuadraticNonMonicGCD(_QuadraticNonMonicGCD, _TimePREM):
    """Calculate time for Quadratic non-monic GCD, F and G have other quadratic factors polynomials."""

    params = [(1, 3 , 5), ('prem', 'poly', 'sparse')] # This case is slow for n=8.


class TimePREMSparseGCDHighDegree(_SparseGCDHighDegree, _TimePREM):
    """Calculate Sparse GCD and inputs where degree is proportional to the number of variables polynomials."""

    params = [(1, 3 , 5, 8), ('prem', 'poly', 'sparse')]


class TimePREMSparseNonMonicQuadratic(_SparseNonMonicQuadratic, _TimePREM):
    """Calculate time for Sparse non-monic quadratic inputs with linear GCDs polynomials."""

    params = [(1, 3 , 5, 8), ('prem', 'poly', 'sparse')]