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


class PolyPrem:
    """Benchmark for the prem method"""

    def setup(self, n):
        self.x, *self.y = symbols("x, y1:11")
        self.R1 = [self.x] + list(self.y)
        self.R = ZZ[self.R1]

        self.values = {}

        self.f_case1, self.g_case1 = self.generate_poly_case1(n)
        self.f_case2, self.g_case2 = self.generate_poly_case2(n)
        self.f_case3, self.g_case3 = self.generate_poly_case3(n)
        self.f_case4, self.g_case4 = self.generate_poly_case4(n)

        self.fp_case1 = Poly(self.f_case1, self.x, *(self.y)[:n])
        self.gp_case1 = Poly(self.g_case1, self.x, *(self.y)[:n])
        self.fpe_case1 = self.R.from_sympy(self.f_case1)
        self.gpe_case1 = self.R.from_sympy(self.g_case1)

        self.fp_case2 = Poly(self.f_case2, self.x, *(self.y)[:n])
        self.gp_case2 = Poly(self.g_case2, self.x, *(self.y)[:n])
        self.fpe_case2 = self.R.from_sympy(self.f_case2)
        self.gpe_case2 = self.R.from_sympy(self.g_case2)

        self.fp_case3 = Poly(self.f_case3, self.x, *(self.y)[:n])
        self.gp_case3 = Poly(self.g_case3, self.x, *(self.y)[:n])
        self.fpe_case3 = self.R.from_sympy(self.f_case3)
        self.gpe_case3 = self.R.from_sympy(self.g_case3)

        self.fp_case4 = Poly(self.f_case4, self.x, *(self.y)[:n])
        self.gp_case4 = Poly(self.g_case4, self.x, *(self.y)[:n])
        self.fpe_case4 = self.R.from_sympy(self.f_case4)
        self.gpe_case4 = self.R.from_sympy(self.g_case4)

    def generate_poly_case1(self, n):
        """Linearly dense quartic inputs with quadratic GCDs."""
        D = (1 + self.x + sum((self.y)[:n])) ** 2
        f = D * (-2 + self.x - sum((self.y)[:n])) ** 2
        g = D * (2 + self.x + sum((self.y)[:n])) ** 2
        return f, g

    def generate_poly_case2(self, n):
        """Sparse GCD and inputs where degree is proportional to the number of variables."""
        D = 1 + self.x ** (n + 1) + sum([(self.y)[i] ** (n + 1) for i in range(n)])
        f = D * (-2 + self.x ** (n + 1) + sum([(self.y)[i] ** (n + 1) for i in range(n)]))
        g = D * (2 + self.x ** (n + 1) + sum([(self.y)[i] ** (n + 1) for i in range(n)]))
        return f, g

    def generate_poly_case3(self, n):
        """Quadratic non-monic GCD, F and G have other quadratic factors."""
        D = 1 + self.x ** 2 * (self.y)[0] ** 2 + sum([(self.y)[i] ** 2 for i in range(1, n)])
        f = D * (-1 + self.x ** 2 - (self.y)[0] ** 2 + sum([(self.y)[i] ** 2 for i in range(1, n)]))
        g = D * (2 + self.x * (self.y)[0] + sum((self.y)[1:n])) ** 2
        return f, g

    def generate_poly_case4(self, n):
        """Sparse non-monic quadratic inputs with linear GCDs."""
        D = -1 + self.x * prod((self.y)[:n])
        f = D * (3 + self.x * prod((self.y)[:n]))
        g = D * (-3 + self.x * prod((self.y)[:n]))
        return f, g


class TimePolyPremFast(PolyPrem):

    # Test for n=1, 5, 8, 10 with the fast methods
    params = [1, 5, 8, 10]

    def time_Polyprem_case1(self, n):
        self.values['Polyprem_case1'] = self.fp_case1.prem(self.gp_case1)

    def time_PolyElement_prem_case1(self, n):
        self.values['PolyElement_prem_case1'] = self.fpe_case1.prem(self.gpe_case1)

    def time_prem_case2(self, n):
        self.values['prem_case2'] = prem(self.f_case2, self.g_case2, self.x)

    def time_Polyprem_case2(self, n):
        self.values['Polyprem_case2'] = self.fp_case2.prem(self.gp_case2)

    def time_PolyElement_prem_case2(self, n):
        self.values['PolyElement_prem_case2'] = self.fpe_case2.prem(self.gpe_case2)

    def time_Polyprem_case3(self, n):
        self.values['Polyprem_case3'] = self.fp_case3.prem(self.gp_case3)

    def time_PolyElement_prem_case3(self, n):
        self.values['PolyElement_prem_case3'] = self.fpe_case3.prem(self.gpe_case3)

    def time_prem_case4(self, n):
        self.values['prem_case4'] = prem(self.f_case4, self.g_case4, self.x)

    def time_Polyprem_case4(self, n):
        self.values['Polyprem_case4'] = self.fp_case4.prem(self.gp_case4)

    def time_PolyElement_prem_case4(self, n):
        self.values['PolyElement_prem_case4'] = self.fpe_case4.prem(self.gpe_case4)



class TimePolyPremSlow(PolyPrem):

    # This methods are slow for n=8 and n=10.
    params = [1, 5]

    def time_prem_case1(self, n):
        self.values['prem_case1'] = prem(self.f_case1, self.g_case1, self.x)

    def time_prem_case3(self, n):
        self.values['prem_case3'] = prem(self.f_case3, self.g_case3, self.x)