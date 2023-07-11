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
        D = (1 + self.x + sum((self.y)[:n])) ** 2
        f = D * (-2 + self.x - sum((self.y)[:n])) ** 2
        g = D * (2 + self.x + sum((self.y)[:n])) ** 2
        fp, gp = Poly(f, self.x, *(self.y)[:n]), Poly(g, self.x, *(self.y)[:n])
        fpe, gpe = self.R.from_sympy(f), self.R.from_sympy(g)
        return f, g, fp, gp, fpe, gpe


class _SparseGCDHighDegree:
    def generate(self, n):
        self.x, *self.y = symbols("x, y1:9")
        self.R1 = [self.x] + list(self.y)
        self.R = ZZ[self.R1]
        D = 1 + self.x ** (n + 1) + sum([(self.y)[i] ** (n + 1) for i in range(n)])
        f = D * (-2 + self.x ** (n + 1) + sum([(self.y)[i] ** (n + 1) for i in range(n)]))
        g = D * (2 + self.x ** (n + 1) + sum([(self.y)[i] ** (n + 1) for i in range(n)]))
        fp, gp = Poly(f, self.x, *(self.y)[:n]), Poly(g, self.x, *(self.y)[:n])
        fpe, gpe = self.R.from_sympy(f), self.R.from_sympy(g)
        return f, g, fp, gp, fpe, gpe


class _QuadraticNonMonicGCD:
    def generate(self, n):
        self.x, *self.y = symbols("x, y1:9")
        self.R1 = [self.x] + list(self.y)
        self.R = ZZ[self.R1]
        D = 1 + self.x ** 2 * (self.y)[0] ** 2 + sum([(self.y)[i] ** 2 for i in range(1, n)])
        f = D * (-1 + self.x ** 2 - (self.y)[0] ** 2 + sum([(self.y)[i] ** 2 for i in range(1, n)]))
        g = D * (2 + self.x * (self.y)[0] + sum((self.y)[1:n])) ** 2
        fp, gp = Poly(f, self.x, *(self.y)[:n]), Poly(g, self.x, *(self.y)[:n])
        fpe, gpe = self.R.from_sympy(f), self.R.from_sympy(g)
        return f, g, fp, gp, fpe, gpe


class _SparseNonMonicQuadratic:
    def generate(self, n):
        self.x, *self.y = symbols("x, y1:9")
        self.R1 = [self.x] + list(self.y)
        self.R = ZZ[self.R1]
        D = -1 + self.x * prod((self.y)[:n])
        f = D * (3 + self.x * prod((self.y)[:n]))
        g = D * (-3 + self.x * prod((self.y)[:n]))
        fp, gp = Poly(f, self.x, *(self.y)[:n]), Poly(g, self.x, *(self.y)[:n])
        fpe, gpe = self.R.from_sympy(f), self.R.from_sympy(g)
        return f, g, fp, gp, fpe, gpe


class _TimePREM:
    """Benchmarks for `prem` method in polynomials."""

    def setup(self, method, n):
        (self.f, self.g, self.fp, self.gp, self.fpe, self.gpe) = self.generate(n)
        self.values = {}
        self.x = symbols("x")
        self.R1 = [self.x] + list(self.y)
        self.R = ZZ[self.R1]

        self.ref = rem((self.f)*LC(self.g, self.x)**(degree(self.f, self.x) - degree(self.g, self.x) + 1), self.g, self.x) # correct results for prem and poly methods.
        self.ref_1  = (self.fpe*(self.R(self.gpe.as_expr().as_poly(self.x).LC()))**(self.fpe.degree() - self.gpe.degree() + 1)).rem(self.gpe) # correct result for sparse method.

        if method == 'prem':
            self.func = lambda: prem(self.f, self.g, self.x)

        elif method == 'poly':
            self.func = lambda: self.fp.prem(self.gp)

        elif method == 'sparse':
            self.func = lambda: self.fpe.prem(self.gpe)

    def teardown(self, method, n):
        for key, val in self.values.items():
            if key == 'sparse':
                if (self.ref_1 - val) != 0:
                    raise ValueError("Incorrect result, invalid timing:"
                                        " %s != %s" % (self.ref_1, val))

            elif (self.ref - val).simplify() != 0:
                raise ValueError("Incorrect result, invalid timing:"
                                    " %s != %s" % (self.ref, val))

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
