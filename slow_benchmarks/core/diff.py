"""Benchmarks for symbolic differentiation."""

import pathlib

from sympy import sympify


class Gait2DDerivatives:
    """Large real-world example equations of motion in 42 variables.

    The equations of motion (EoMs) are derived from the Gait2D dynamic model of
    gait (see here: https://github.com/csu-hmc/gait2d). This specific benchmark,
    involving the derivation of the 18x42 Jacobian matrix, was highlighted in
    SymPy issue #8191 (see here: https://github.com/sympy/sympy/issues/8191).

    """

    def setup(self):
        """Read the equation of motion and variables from artifact files.

        The 18 equations of motion are specified in `dis_eom.txt` while the 42
        variables are specified in `partials.txt`. Copies of both `dis_eom.txt`
        and `partials.txt` are in the `artifacts` subdirectory.

        """
        artifacts_dir_path = pathlib.Path(__file__).parents[0] / "artifacts"
        dis_eom_path = pathlib.Path(artifacts_dir_path, "dis_eom.txt")
        with open(dis_eom_path, "r") as A_file:
            self.A = sympify(A_file.read())
        partials_path = pathlib.Path(artifacts_dir_path, "partials.txt")
        with open(partials_path, "r") as x_file:
            self.x = sympify(x_file.read())

    def time_jacobian(self):
        """Time differentiation to construct the 18x42 Jacobian matrix."""
        self.A.jacobian(self.x)
