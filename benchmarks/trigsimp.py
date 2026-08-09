import sympy as sp


class TimeTrigSimplify:
    """
    Benchmark trigonometric simplification on expanded angle-sum identities.
    """

    params = [5, 10, 20]

    def setup(self, n):
        xs = sp.symbols(f"x0:{n + 1}")
        expr = 0
        for i in range(n):
            angle = xs[i] + xs[i + 1]
            # Expanded trig identity that should simplify to 1
            expr += sp.expand_trig(sp.sin(angle)**2 + sp.cos(angle)**2)
        self.expr = expr

    def time_trigsimp(self, n):
        sp.trigsimp(self.expr)