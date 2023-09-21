"""Benchmarks for symbolic differentiation."""

from sympy import exp, sin, symbols, tan, Matrix


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


class GriewankLighthouseExampleDerivatives:
    """Simple matrix test function in four variables.

    Function is the "lighthouse example" taken from Griewank, A., & Walther, A.
    (2008). Evaluating derivatives: principles and techniques of algorithmic
    differentiation. SIAM.
    
    """

    def setup(self):
        """Create the required symbols (nu, gamma, omega, t) and the expression
        (y).

        """
        nu, gamma, omega, t = symbols("nu, gamma, omega, t")
        self.x = Matrix([nu, gamma, omega, t])
        self.y = Matrix([
            nu * tan(omega * t) / (gamma - tan(omega * t)),
            nu * gamma * tan(omega * t) / (gamma - tan(omega * t)),
        ])

    def time_jacobian(self):
        """Time differentiation of the lighthouse example."""
        self.G = self.y.jacobian(self.x)
