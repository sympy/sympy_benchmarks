import sympy

class TimePolyManyGens:
    """Time using a Poly with many generators"""

    params = [1, 10, 100, 500]

    def setup(self, n):
        self.xs = sympy.symbols('x:{}'.format(n))
        self.x = self.xs[n // 2]
        self.px = sympy.Poly(self.x, self.xs)

    def time_create_poly(self, n):
        sympy.Poly(self.x, self.xs)

    def time_is_linear(self, n):
        self.px.is_linear
