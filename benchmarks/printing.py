from sympy import Symbol, Matrix, latex, log, atan2


class TimeMatrixPrinting:
    """Benchmark for grid structures"""
    params = [10, 20, 30]

    def setup(self, n):
        x = Symbol('x')
        self.expr = Matrix(n, n, lambda i, j: x ** (i + j))

    def time_str(self, n):
        str(self.expr)

    def time_latex(self, n):
        latex(self.expr)


class TimePolyPrintin:
    """Benchmark for polynomial structure"""
    params = [10, 50, 500]

    def setup(self, n):
        x = Symbol('x')
        y = Symbol('y')
        self.expr = ((x + y) ** n).expand()

    def time_str(self, n):
        str(self.expr)

    def time_latex(self, n):
        latex(self.expr)


class TimeNestedLogPrinting:
    """Benchmark for deep nested trees structure using log function"""
    params = [10, 50, 100]

    def setup(self, n):
        x = Symbol('x')
        expr = x
        for _ in range(n):
            expr = log(expr)

        self.expr = expr

    def time_str(self, n):
        str(self.expr)

    def time_latex(self, n):
        latex(self.expr)


class TimeNestedAtan2Printing:
    """Benchmark for deep nested trees structure using atan2 function"""
    params = [2, 5, 10]

    def setup(self, n):
        x = Symbol('x')
        expr = x
        for _ in range(n):
            expr = atan2(expr, expr)

        self.expr = expr

    def time_str(self, n):
        str(self.expr)

    def time_latex(self, n):
        latex(self.expr)
