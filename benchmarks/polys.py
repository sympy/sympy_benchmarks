from sympy import symbols, prod, prem
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

class _PolyGCDExample:
    def setup(self, n):
        (self.f, self.g, self.fp, self.gp, self.fpe, self.gpe) = self.generate(n)
        self.values = {}
        self.x = symbols("x")

class _TimePREM(_PolyGCDExample):

    def time_prem(self, n):
        self.values['prem'] = prem(self.f, self.g, self.x)

    def time_prem_PolyElement(self, n):
        self.values['prem_PolyElement'] = self.fpe.prem(self.gpe)

    def time_Poly_prem(self, n):
        self.values['Poly_prem'] = self.fp.prem(self.gp)

class TimePREMLinearDenseQuadraticGCD(_LinearDenseQuadraticGCD, _TimePREM):
    """Calculate time for Linearly dense quartic inputs with quadratic GCDs polynomials."""

    params = [1, 3, 5] # This case is slow for n=8.

class TimePREMQuadraticNonMonicGCD(_QuadraticNonMonicGCD, _TimePREM):
    """Calculate time for Quadratic non-monic GCD, F and G have other quadratic factors polynomials."""

    params = [1, 3, 5] # This case is slow for n=8.

class TimePREMSparseGCDHighDegree(_SparseGCDHighDegree, _TimePREM):
    """Calculate Sparse GCD and inputs where degree is proportional to the number of variables polynomials."""
    params = [1, 3, 5, 8]

class TimePREMSparseNonMonicQuadratic(_SparseNonMonicQuadratic, _TimePREM):
    """Calculate time for Sparse non-monic quadratic inputs with linear GCDs polynomials."""

    params = [1, 3, 5, 8]