from sympy import symbols
class TimeLargePolynomialExpand:
    params = [50, 100, 200]
    param_names = ["degree"]
    def setup(self, degree):
        x = symbols("x")
        self.expr = (x + 1) ** degree
    def time_expand(self, degree):
        self.expr.expand()