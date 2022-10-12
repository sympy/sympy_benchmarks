"""Benchmarks for symbolic differentiation."""

import pathlib

from sympy import sympify


class GriewankBabyExampleDerivatives:
    """Simple test function in two variables.

    Function is the "baby example" taken from Griewank, A., & Walther, A.
    (2008). Evaluating derivatives: principles and techniques of algorithmic
    differentiation. SIAM.

    """

    def setup(self):
        """Create the required symbols (x1, x2) and the expression (y)."""
        x1, x2 = symbols("x1, x2")
        self.x = Matrix([x1, x2])
        self.y = (sin(x1 / x2) + (x1 / x2) - exp(x2)) * ((x1 / x2) - exp(x2))

    def time_jacobian(self):
        """Time differentiation of the baby example."""
        self.G = self.y.diff(self.x)
