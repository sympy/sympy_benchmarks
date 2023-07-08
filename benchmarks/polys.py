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


class LinearDenseQuadraticGCD:
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


class SparseGCDHighDegree:
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


class QuadraticNonMonicGCD:
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


class SparseNonMonicQuadratic:
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


class PolyPrem:
    """Benchmark for the prem method"""

    def setup(self, n):
        self.x, *self.y = symbols("x, y1:9")
        self.R1 = [self.x] + list(self.y)
        self.R = ZZ[self.R1]

        self.values = {}

        (self.f_LinearDenseQuadraticGCD, self.g_LinearDenseQuadraticGCD,
        self.fp_LinearDenseQuadraticGCD, self.gp_LinearDenseQuadraticGCD,
        self.fpe_LinearDenseQuadraticGCD, self.gpe_LinearDenseQuadraticGCD) = LinearDenseQuadraticGCD().generate(n)

        (self.f_SparseGCDHighDegree, self.g_SparseGCDHighDegree,
        self.fp_SparseGCDHighDegree, self.gp_SparseGCDHighDegree,
        self.fpe_SparseGCDHighDegree, self.gpe_SparseGCDHighDegree) = SparseGCDHighDegree().generate(n)

        (self.f_QuadraticNonMonicGCD, self.g_QuadraticNonMonicGCD,
        self.fp_QuadraticNonMonicGCD, self.gp_QuadraticNonMonicGCD,
        self.fpe_QuadraticNonMonicGCD, self.gpe_QuadraticNonMonicGCD) = QuadraticNonMonicGCD().generate(n)

        (self.f_SparseNonMonicQuadratic, self.g_SparseNonMonicQuadratic,
        self.fp_SparseNonMonicQuadratic, self.gp_SparseNonMonicQuadratic,
        self.fpe_SparseNonMonicQuadratic, self.gpe_SparseNonMonicQuadratic) = SparseNonMonicQuadratic().generate(n)


class TimePolyPremFast(PolyPrem):

    # Test for n=1, 3, 5, 8 with the fast methods
    params = [1, 3, 5, 8]

    def time_prem_SparseGCDHighDegree(self, n):
        self.values['prem_SparseGCDHighDegree'] = prem(self.f_SparseGCDHighDegree, self.g_SparseGCDHighDegree, self.x)

    def time_prem_SparseNonMonicQuadratic(self, n):
        self.values['prem_SparseNonMonicQuadratic'] = prem(self.f_SparseNonMonicQuadratic, self.g_SparseNonMonicQuadratic, self.x)

    def time_Polyprem_SparseGCDHighDegree(self, n):
        self.values['Polyprem_SparseGCDHighDegree'] = self.fp_SparseGCDHighDegree.prem(self.gp_SparseGCDHighDegree)

    def time_Polyprem_QuadraticNonMonicGCD(self, n):
        self.values['Polyprem_QuadraticNonMonicGCD'] = self.fp_QuadraticNonMonicGCD.prem(self.gp_QuadraticNonMonicGCD)

    def time_Polyprem_SparseNonMonicQuadratic(self, n):
        self.values['Polyprem_SparseNonMonicQuadratic'] = self.fp_SparseNonMonicQuadratic.prem(self.gp_SparseNonMonicQuadratic)

    def time_PolyElement_prem_SparseGCDHighDegree(self, n):
        self.values['PolyElement_prem_SparseGCDHighDegree'] = self.fpe_SparseGCDHighDegree.prem(self.gpe_SparseGCDHighDegree)

    def time_PolyElement_prem_SparseNonMonicQuadratic(self, n):
        self.values['PolyElement_prem_SparseNonMonicQuadratic'] = self.fpe_SparseNonMonicQuadratic.prem(self.gpe_SparseNonMonicQuadratic)


class TimePolyPremSlow(PolyPrem):

    # This methods are slow for n=8.
    params = [1, 3, 5]

    def time_prem_LinearDenseQuadraticGCD(self, n):
        self.values['prem_LinearDenseQuadraticGCD'] = prem(self.f_LinearDenseQuadraticGCD, self.g_LinearDenseQuadraticGCD, self.x)

    def time_prem_QuadraticNonMonicGCD(self, n):
        self.values['prem_QuadraticNonMonicGCD'] = prem(self.f_QuadraticNonMonicGCD, self.g_QuadraticNonMonicGCD, self.x)

    def time_Polyprem_LinearDenseQuadraticGCD(self, n):
        self.values['Polyprem_LinearDenseQuadraticGCD'] = self.fp_LinearDenseQuadraticGCD.prem(self.gp_LinearDenseQuadraticGCD)

    def time_PolyElement_prem_LinearDenseQuadraticGCD(self, n):
        self.values['PolyElement_prem_LinearDenseQuadraticGCD'] = self.fpe_LinearDenseQuadraticGCD.prem(self.gpe_LinearDenseQuadraticGCD)

    def time_PolyElement_prem_QuadraticNonMonicGCD(self, n):
        self.values['PolyElement_prem_QuadraticNonMonicGCD'] = self.fpe_QuadraticNonMonicGCD.prem(self.gpe_QuadraticNonMonicGCD)