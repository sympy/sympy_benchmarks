class TimeLargePolynomialExpand:
    def setup(self):
        from sympy import symbols
        self.x = symbols('x')
        self.expr = (self.x + 1)**200

    def time_expand(self):
        self.expr.expand()
