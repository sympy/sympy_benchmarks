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
    def generate(self, n):
        self.x, *self.y = symbols("x, y1:9")
        self.R1 = [self.x] + list(self.y)
        self.R = ZZ[self.R1]
        x, y, R = self.x, self.y, self.R
        D = (1 + x + sum(y[:n])) ** 2
        f = D * (-2 + x - sum(y[:n])) ** 2
        g = D * (2 + x + sum(y[:n])) ** 2
        fp, gp = Poly(f, x, *y[:n]), Poly(g, x, *y[:n])
        fpe, gpe = R.from_sympy(f), R.from_sympy(g)
        return f, g, fp, gp, fpe, gpe, x, y, R


class _SparseGCDHighDegree:
    def generate(self, n):
        self.x, *self.y = symbols("x, y1:9")
        self.R1 = [self.x] + list(self.y)
        self.R = ZZ[self.R1]
        x, y, R = self.x, self.y, self.R
        D = 1 + x ** (n + 1) + sum([y[i] ** (n + 1) for i in range(n)])
        f = D * (-2 + x ** (n + 1) + sum([y[i] ** (n + 1) for i in range(n)]))
        g = D * (2 + x ** (n + 1) + sum([y[i] ** (n + 1) for i in range(n)]))
        fp, gp = Poly(f, x, *y[:n]), Poly(g, x, *y[:n])
        fpe, gpe = R.from_sympy(f), R.from_sympy(g)
        return f, g, fp, gp, fpe, gpe, x, y, R


class _QuadraticNonMonicGCD:
    def generate(self, n):
        self.x, *self.y = symbols("x, y1:9")
        self.R1 = [self.x] + list(self.y)
        self.R = ZZ[self.R1]
        x, y, R = self.x, self.y, self.R
        D = 1 + x ** 2 * y[0] ** 2 + sum([y[i] ** 2 for i in range(1, n)])
        f = D * (-1 + x ** 2 - y[0] ** 2 + sum([y[i] ** 2 for i in range(1, n)]))
        g = D * (2 + x * y[0] + sum(y[1:n])) ** 2
        fp, gp = Poly(f, x, *y[:n]), Poly(g, x, *y[:n])
        fpe, gpe = R.from_sympy(f), R.from_sympy(g)
        return f, g, fp, gp, fpe, gpe, x, y, R


class _SparseNonMonicQuadratic:
    def generate(self, n):
        self.x, *self.y = symbols("x, y1:9")
        self.R1 = [self.x] + list(self.y)
        self.R = ZZ[self.R1]
        x, y, R = self.x, self.y, self.R
        D = -1 + x * prod(y[:n])
        f = D * (3 + x * prod(y[:n]))
        g = D * (-3 + x * prod(y[:n]))
        fp, gp = Poly(f, x, *y[:n]), Poly(g, x, *y[:n])
        fpe, gpe = R.from_sympy(f), R.from_sympy(g)
        return f, g, fp, gp, fpe, gpe, x, y, R


class _TimePREM:
    """Benchmarks for `prem` method in polynomials."""

    def setup_polys(self, n):
        (f, g, fp, gp, fpe, gpe, x, y, R) = self.generate(n)

        self.values = {}
        self.f = f
        self.g = g
        self.fp = fp
        self.gp = gp
        self.fpe = fpe
        self.gpe = gpe
        self.x = x
        self.y = y
        self.R = R

    def setup(self, method, n):
        self.setup_polys(n)

        f, g, x, R = self.f, self.g, self.x, self.R
        prem_f_g_x = rem(f * LC(g, x) ** (degree(f, x) - degree(g, x) + 1), g, x)

        self.ref_expr = prem_f_g_x
        self.ref_ring = R(prem_f_g_x.as_expr())

        if method == 'prem':
            self.func = lambda: prem(self.f, self.g, self.x)

        elif method == 'poly':
            self.func = lambda: self.fp.prem(self.gp)

        elif method == 'sparse':
            self.func = lambda: self.fpe.prem(self.gpe)

    def teardown(self, method, n):
        for key, val in self.values.items():
            if key == 'sparse':
                if (self.ref_ring - val) != 0:
                    raise ValueError("Incorrect result, invalid timing:"
                                        " %s != %s" % (self.ref_ring, val))

            elif (self.ref_expr - val).simplify() != 0:
                raise ValueError("Incorrect result, invalid timing:"
                                    " %s != %s" % (self.ref_expr, val))

    def time_prem_methods(self, method, n):
        self.values[str(method)] = self.func()


class TimePREMLinearDenseQuadraticGCD(_LinearDenseQuadraticGCD, _TimePREM):
    """Calculate time for Linearly dense quartic inputs with quadratic GCDs polynomials."""

    params = [('prem', 'poly', 'sparse'), (1, 3 , 5)] # This case is slow for n=8.


class TimePREMQuadraticNonMonicGCD(_QuadraticNonMonicGCD, _TimePREM):
    """Calculate time for Quadratic non-monic GCD, F and G have other quadratic factors polynomials."""

    params = [('prem', 'poly', 'sparse'), (1, 3 , 5)] # This case is slow for n=8.


class TimePREMSparseGCDHighDegree(_SparseGCDHighDegree, _TimePREM):
    """Calculate Sparse GCD and inputs where degree is proportional to the number of variables polynomials."""

    params = [('prem', 'poly', 'sparse'), (1, 3 , 5, 8)]


class TimePREMSparseNonMonicQuadratic(_SparseNonMonicQuadratic, _TimePREM):
    """Calculate time for Sparse non-monic quadratic inputs with linear GCDs polynomials."""

    params = [('prem', 'poly', 'sparse'), (1, 3 , 5, 8)]
