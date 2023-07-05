from sympy import symbols, prod
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


x, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10 = symbols("x, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10")
y = [y1, y2, y3, y4, y5, y6, y7, y8, y9, y10]
R = ZZ[x, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10]

def generate_poly_case1(n):
    """Linearly dense quartic inputs with quadratic GCDs."""
    D = (1 + x + sum(y)) ** 2
    f = D * (-2 + x - sum(y)) ** 2
    g = D * (2 + x + sum(y)) ** 2
    return f, g


def generate_poly_case2(n):
    """Sparse GCD and inputs where degree is proportional to the number of variables."""
    D = 1 + x ** (n + 1) + sum([y[i] ** (n + 1) for i in range(n)])
    f = D * (-2 + x ** (n + 1) + sum([y[i] ** (n + 1) for i in range(n)]))
    g = D * (2 + x ** (n + 1) + sum([y[i] ** (n + 1) for i in range(n)]))
    return f, g


def generate_poly_case3(n):
    """Quadratic non-monic GCD, F and G have other quadratic factors."""
    D = 1 + x ** 2 * y[0] ** 2 + sum([y[i] ** 2 for i in range(1, n)])
    f = D * (-1 + x ** 2 - y[0] ** 2 + sum([y[i] ** 2 for i in range(1, n)]))
    g = D * (2 + x * y[0] + sum(y[1:n])) ** 2
    return f, g


def generate_poly_case4(n):
    """Sparse non-monic quadratic inputs with linear GCDs."""
    D = -1 + x * prod(y[:n])
    f = D * (3 + x * prod(y[:n]))
    g = D * (-3 + x * prod(y[:n]))
    return f, g


class TimePolyprem:
    """Benchmark for the prem method"""

    params = [(1,), (3,), (6,), (8,), (10,)]

    def setup(self, size):
        self.values = {}
        self.size = size
        n = self.size[0]
        self.f_case1, self.g_case1 = generate_poly_case1(n)
        self.f_case2, self.g_case2 = generate_poly_case2(n)
        self.f_case3, self.g_case3 = generate_poly_case3(n)
        self.f_case4, self.g_case4 = generate_poly_case4(n)

        self.fp_case1 = Poly(self.f_case1, x, *(y)[:n])
        self.gp_case1 = Poly(self.g_case1, x, *(y)[:n])
        self.fpe_case1 = R.from_sympy(self.f_case1)
        self.gpe_case1 = R.from_sympy(self.g_case1)

        self.fp_case2 = Poly(self.f_case2, x, *(y)[:n])
        self.gp_case2 = Poly(self.g_case2, x, *(y)[:n])
        self.fpe_case2 = R.from_sympy(self.f_case2)
        self.gpe_case2 = R.from_sympy(self.g_case2)

        self.fp_case3 = Poly(self.f_case3, x, *(y)[:n])
        self.gp_case3 = Poly(self.g_case3, x, *(y)[:n])
        self.fpe_case3 = R.from_sympy(self.f_case3)
        self.gpe_case3 = R.from_sympy(self.g_case3)

        self.fp_case4 = Poly(self.f_case4, x, *(y)[:n])
        self.gp_case4 = Poly(self.g_case4, x, *(y)[:n])
        self.fpe_case4 = R.from_sympy(self.f_case4)
        self.gpe_case4 = R.from_sympy(self.g_case4)

    def time_prem_case1(self):
        self.values['prem_case1'] = prem(self.f_case1, self.g_case1, x)

    def time_Polyprem_case1(self):
        self.values['Polyprem_case1'] = self.fp_case1.prem(self.gp_case1)

    def time_PolyElement_prem_case1(self):
        self.values['PolyElement_prem_case1'] = self.fpe_case1.prem(self.gpe_case1)

    def time_prem_case2(self):
        self.values['prem_case2'] = prem(self.f_case2, self.g_case2, x)

    def time_Polyprem_case2(self):
        self.values['Polyprem_case2'] = self.fp_case2.prem(self.gp_case2)

    def time_PolyElement_prem_case2(self):
        self.values['PolyElement_prem_case2'] = self.fpe_case2.prem(self.gpe_case2)

    def time_prem_case3(self):
        self.values['prem_case3'] = prem(self.f_case3, self.g_case3, x)

    def time_Polyprem_case3(self):
        self.values['Polyprem_case3'] = self.fp_case3.prem(self.gp_case3)

    def time_PolyElement_prem_case3(self):
        self.values['PolyElement_prem_case3'] = self.fpe_case3.prem(self.gpe_case3)

    def time_prem_case4(self):
        self.values['prem_case4'] = prem(self.f_case4, self.g_case4, x)

    def time_Polyprem_case4(self):
        self.values['Polyprem_case4'] = self.fp_case4.prem(self.gp_case4)

    def time_PolyElement_prem_case4(self):
        self.values['PolyElement_prem_case4'] = self.fpe_case4.prem(self.gpe_case4)