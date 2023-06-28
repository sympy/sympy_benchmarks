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



x, y, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10 = symbols("x y y1 y2 y3 y4 y5 y6 y7 y8 y9 y10")

y = [y1, y2, y3, y4, y5, y6, y7, y8, y9, y10] # set values of y for v = 1 to 10

R = ZZ[x, y, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10]

# Case: Linearly dense quartic inputs with quadratic GCDs
def bench1_core_prem():
    for v in range(1, 11):
        D = (1 + x + sum(y[:v])) ** 2
        f = D * (-2 + x - sum(y[:v])) ** 2
        g = D * (2 + x + sum(y[:v])) ** 2

        return prem(f, g, x)

def bench1_Poly_prem():
    for v in range(1, 11):
        D = (1 + x + sum(y[:v])) ** 2
        f = D * (-2 + x - sum(y[:v])) ** 2
        g = D * (2 + x + sum(y[:v])) ** 2

        fp, gp = Poly(f, x, *y[:v]), Poly(g, x, *y[:v])

        return fp.prem(gp)

def bench1_PolyElement_prem():
    for v in range(1, 11):
        D = (1 + x + sum(y[:v])) ** 2
        f = D * (-2 + x - sum(y[:v])) ** 2
        g = D * (2 + x + sum(y[:v])) ** 2

        fpe, gpe = R.from_sympy(f), R.from_sympy(g)

        return fpe.prem(gpe)


# Case: Sparse GCD and inputs where degree are proportional to the number of variables
def bench2_core_prem():
    for v in range(1, 11):
        D = 1 + x ** (v + 1) + sum([y[i] ** (v + 1) for i in range(v)])
        f = D * (-2 + x ** (v + 1) + sum([y[i] ** (v + 1) for i in range(v)]))
        g = D * (2 + x ** (v + 1) + sum([y[i] ** (v + 1) for i in range(v)]))

        return prem(f, g, x)

def bench2_Poly_prem():
    for v in range(1, 11):
        D = 1 + x ** (v + 1) + sum([y[i] ** (v + 1) for i in range(v)])
        f = D * (-2 + x ** (v + 1) + sum([y[i] ** (v + 1) for i in range(v)]))
        g = D * (2 + x ** (v + 1) + sum([y[i] ** (v + 1) for i in range(v)]))

        fp, gp = Poly(f, x, *y[:v]), Poly(g, x, *y[:v])

        return fp.prem(gp)

def bench2_PolyElement_prem():
    for v in range(1, 11):
        D = 1 + x ** (v + 1) + sum([y[i] ** (v + 1) for i in range(v)])
        f = D * (-2 + x ** (v + 1) + sum([y[i] ** (v + 1) for i in range(v)]))
        g = D * (2 + x ** (v + 1) + sum([y[i] ** (v + 1) for i in range(v)]))

        fpe, gpe = R.from_sympy(f), R.from_sympy(g)

        return fpe.prem(gpe)


# Case: Quadratic non-monic GCD, F and G have other quadratic factors
def bench3_core_prem():
    for v in range(1, 11):
        D = 1 + x**2 * y[0]**2 + sum([y[i]**2 for i in range(1, v)])
        f = D * (-1 + x**2 - y[0]**2 + sum([y[i]**2 for i in range(1, v)]))
        g = D * (2 + x * y[0] + sum(y[1:v]))**2

        return prem(f, g, x)

def bench3_Poly_prem():
    for v in range(1, 11):
        D = 1 + x**2 * y[0]**2 + sum([y[i]**2 for i in range(1, v)])
        f = D * (-1 + x**2 - y[0]**2 + sum([y[i]**2 for i in range(1, v)]))
        g = D * (2 + x * y[0] + sum(y[1:v]))**2

        fp, gp = Poly(f, x, *y[:v]), Poly(g, x, *y[:v])

        return fp.prem(gp)

def bench3_PolyElement_prem():
    for v in range(1, 11):
        D = 1 + x**2 * y[0]**2 + sum([y[i]**2 for i in range(1, v)])
        f = D * (-1 + x**2 - y[0]**2 + sum([y[i]**2 for i in range(1, v)]))
        g = D * (2 + x * y[0] + sum(y[1:v]))**2

        fpe, gpe = R.from_sympy(f), R.from_sympy(g)

        return fpe.prem(gpe)


# Case: Sparse non-monic quadratic inputs with linear GCDs
def bench4_core_prem():
    for v in range(1, 11):
        D = -1 + x * (prod(y[:v]))
        f = D * (3 + x * (prod(y[:v])))
        g = D * (-3 + x * (prod(y[:v])))

        return prem(f, g, x)

def bench4_Poly_prem():
    for v in range(1, 11):
        D = -1 + x * (prod(y[:v]))
        f = D * (3 + x * (prod(y[:v])))
        g = D * (-3 + x * (prod(y[:v])))

        fp, gp = Poly(f, x, *y[:v]), Poly(g, x, *y[:v])

        return fp.prem(gp)

def bench4_PolyElement_prem():
    for v in range(1, 11):
        D = -1 + x * (prod(y[:v]))
        f = D * (3 + x * (prod(y[:v])))
        g = D * (-3 + x * (prod(y[:v])))

        fpe, gpe = R.from_sympy(f), R.from_sympy(g)

        return fpe.prem(gpe)
