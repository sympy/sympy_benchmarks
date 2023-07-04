from sympy import symbols
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

    def setup(self):
        self.R, self.x, self.y, self.y1, self.y2, self.y3, self.y4, self.y5, self.y6, self.y7, self.y8, self.y9, self.y10 = ring("x, y, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10", ZZ)
        self.y = [self.y1, self.y2, self.y3, self.y4, self.y5, self.y6, self.y7, self.y8, self.y9, self.y10]
        self.values = {}

    def bench1_core_prem(self):
        self.f = (self.x - self.y1 - 2)**2*(self.x + self.y1 + 1)**2
        self.g = (self.x + self.y1 + 1)**2*(self.x + self.y1 + 2)**2

    def bench2_core_prem(self):
        self.f = (self.x - self.y1 - self.y10 - self.y2 - self.y3 - self.y4 - self.y5 - self.y6 - self.y7 - self.y8 - self.y9 - 2)**2*(self.x + self.y1 + self.y10 + self.y2 + self.y3 + self.y4 + self.y5 + self.y6 + self.y7 + self.y8 + self.y9 + 1)**2
        self.g = (self.x + self.y1 + self.y10 + self.y2 + self.y3 + self.y4 + self.y5 + self.y6 + self.y7 + self.y8 + self.y9 + 1)**2*(self.x + self.y1 + self.y10 + self.y2 + self.y3 + self.y4 + self.y5 + self.y6 + self.y7 + self.y8 + self.y9 + 2)**2

    def time_doit_prem(self):
        self.values['bench1_core_prem'] =  self.prem(self.f, self.g)
        self.values['bench2_core_prem'] =  self.prem(self.f, self.g)
