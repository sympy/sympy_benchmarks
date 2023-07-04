from sympy import symbols, prod
from sympy.polys import ZZ, Poly, ring


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


class TimePolyprem:
    """Benchmark for the prem method"""

    params = [(1,), (5,), (10,), (15,)]

    def setup(self, size):
        self.R, self.x, self.y, self.y1, self.y2, self.y3, self.y4, self.y5, self.y6, self.y7, self.y8, self.y9, self.y10 = ring("x, y, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10", ZZ)
        self.y = [self.y1, self.y2, self.y3, self.y4, self.y5, self.y6, self.y7, self.y8, self.y9, self.y10]
        self.values = {}
        self.size = size

    def generate_poly_case1(self):
        # Linearly dense quartic inputs with quadratic GCDs.
        n = self.size
        D = (1 + self.x + sum(self.y[:n])) ** 2
        self.f = D * (-2 + self.x - sum(self.y[:n])) ** 2
        self.g = D * (2 + self.x + sum(self.y[:n])) ** 2

    def time_new_prem_case1(self):
        self.generate_poly_case1()
        self.values['new_prem_case1'] = prem(self.f, self.g, self.x)

    def time_Polyprem_case1(self):
        self.generate_poly_case1()
        n = self.size
        fp, gp = Poly(self.f, self.x, *(self.y)[:n]), Poly(self.g, self.x, *(self.y)[:n])
        self.values['Polyprem_case1'] = fp.prem(gp)

    def time_PolyElement_prem_case1(self):
            self.generate_poly_case1()
            self.R = ZZ[self.x, self.y, self.y1, self.y2, self.y3, self.y4, self.y5, self.y6, self.y7, self.y8, self.y9, self.y10]
            fpe, gpe = self.R.from_sympy(self.f), self.R.from_sympy(self.g)
            self.values['PolyElement_prem_case1'] = fpe.prem(gpe)

    def generate_poly_case2(self):
        # Sparse GCD and inputs where degree are proportional to the number of variables.
        n = self.size
        D = 1 + self.x ** (n + 1) + sum([self.y[i] ** (n + 1) for i in range(n)])
        self.f = D * (-2 + self.x ** (n + 1) + sum([self.y[i] ** (n + 1) for i in range(n)]))
        self.g = D * (2 + self.x ** (n + 1) + sum([self.y[i] ** (n + 1) for i in range(n)]))

    def time_new_prem_case2(self):
        self.generate_poly_case2()
        self.values['new_prem_case2'] = prem(self.f, self.g, self.x)

    def time_Polyprem_case2(self):
        self.generate_poly_case2()
        n = self.size
        fp, gp = Poly(self.f, self.x, *(self.y)[:n]), Poly(self.g, self.x, *(self.y)[:n])
        self.values['Polyprem_case2'] = fp.prem(gp)

    def time_PolyElement_prem_case2(self):
        self.generate_poly_case2()
        self.R = ZZ[self.x, self.y, self.y1, self.y2, self.y3, self.y4, self.y5, self.y6, self.y7, self.y8, self.y9, self.y10]
        fpe, gpe = self.R.from_sympy(self.f), self.R.from_sympy(self.g)
        self.values['PolyElement_prem_case2'] = fpe.prem(gpe)

    def generate_poly_case3(self):
        # Quadratic non-monic GCD, F and G have other quadratic factors.
        n = self.size
        D = 1 + self.x**2 * self.y[0]**2 + sum([self.y[i]**2 for i in range(1, n)])
        self.f = D * (-1 + self.x**2 - self.y[0]**2 + sum([self.y[i]**2 for i in range(1, n)]))
        self.g = D * (2 + self.x * self.y[0] + sum(self.y[1:n]))**2

    def time_new_prem_case3(self):
        self.generate_poly_case3()
        self.values['new_prem_case3'] = prem(self.f, self.g, self.x)

    def time_Polyprem_case3(self):
        self.generate_poly_case3()
        n = self.size
        fp, gp = Poly(self.f, self.x, *(self.y)[:n]), Poly(self.g, self.x, *(self.y)[:n])
        self.values['Polyprem_case3'] = fp.prem(gp)

    def time_PolyElement_prem_case3(self):
        self.generate_poly_case3()
        self.R = ZZ[self.x, self.y, self.y1, self.y2, self.y3, self.y4, self.y5, self.y6, self.y7, self.y8, self.y9, self.y10]
        fpe, gpe = self.R.from_sympy(self.f), self.R.from_sympy(self.g)
        self.values['PolyElement_prem_case3'] = fpe.prem(gpe)

    def generate_poly_case4(self):
        # Sparse non-monic quadratic inputs with linear GCDs.
        n = self.size
        D = -1 + self.x * prod(self.y[:n])
        self.f = D * (3 + self.x * prod(self.y[:n]))
        self.g = D * (-3 + self.x * prod(self.y[:n]))

    def time_new_prem_case4(self):
        self.generate_poly_case4()
        self.values['new_prem_case4'] = prem(self.f, self.g, self.x)

    def time_Polyprem_case4(self):
        self.generate_poly_case4()
        n = self.size
        fp, gp = Poly(self.f, self.x, *(self.y)[:n]), Poly(self.g, self.x, *(self.y)[:n])
        self.values['Polyprem_case4'] = fp.prem(gp)

    def time_PolyElement_prem_case4(self):
        self.generate_poly_case4()
        self.R = ZZ[self.x, self.y, self.y1, self.y2, self.y3, self.y4, self.y5, self.y6, self.y7, self.y8, self.y9, self.y10]
        fpe, gpe = self.R.from_sympy(self.f), self.R.from_sympy(self.g)
        self.values['PolyElement_prem_case4'] = fpe.prem(gpe)