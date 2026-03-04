import sympy as sp
class TimeSimplifyLargeExpr:
    params = [10, 20, 40]
    param_names = ["n"]
    def setup(self, n):
        x = sp.symbols("x")
        expr = 0
        for i in range(1, n):
            expr += sp.sin(x)**2 + sp.cos(x)**2
        self.expr = expr
    def time_simplify(self, n):
        sp.simplify(self.expr)