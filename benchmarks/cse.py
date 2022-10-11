"""Benchmarks for SymPy's common subexpression elimination (CSE)."""

from functools import reduce
from operator import add

from sympy import cse, exp, sin, symbols, tan, Matrix


def _get_args_exprs(nexprs, nterms):
    """Construct expressions with a number of symbols based on chained additions
    and subtractions.

    Examples
    ========

    >>> _get_args_exprs(1, 1)
    ((x0,), [x0])
    >>> _get_args_exprs(1, 3)
    ((x0, x1, x2), [x0 - x1 + x2])
    >>> _get_args_exprs(3, 1)
    ((x0,), [x0, -x0, x0])
    >>> _get_args_exprs(3, 3)
    ((x0, x1, x2), [x0 - x1 + x2, -x0 + x1 - x2, x0 - x1 + x2])

    """
    x = symbols('x:%d' % nterms)
    exprs = [
        reduce(add, [x[j]*(-1)**(i+j) for j in range(nterms)]) for i in range(nexprs)
    ]
    return x, exprs


class TimeCSE:

    params = (((2, 8), (3, 8), (4, 8), (2, 9), (2, 10), (2, 11), ), )

    def setup(self, nexprs_nterms):
        self.args, self.exprs = _get_args_exprs(*nexprs_nterms)

    def time_cse(self, nexprs_nterms):
        cse(self.exprs)


class GriewankBabyExampleCSE:
    """Simple test function with multiple repeated subexpressions.

    Function is the "baby example" taken from Griewank, A., & Walther, A.
    (2008). Evaluating derivatives: principles and techniques of algorithmic
    differentiation. SIAM.

    The baby example function expressed as a tree structure is as follows:

                           (MUL)
                      _______|______
                     /              \
                  (SUB)            (SUB)
                 ___|___           __|__
                /       \         /     \
              (ADD)    (EXP)   (DIV)   (EXP)
             ___|___     |      _|_      |
            /       \    |     /   \     |
          (SIN)   (DIV) (x2) (x1) (x2)  (x2)
            |      _|_
            |     /   \
          (DIV) (x1) (x2)
           _|_
          /   \
        (x1) (x2)

    It involves 1 ADD, 3 DIV, 2 EXP, 1 MUL, 1 SIN, and 2 SUB operations.

    When CSE is conducted on the expression, the following intermediate terms
    are introduced:

    @0: EXP[x2]
    @1: DIV[x1, x2]
    @2: SUB[@1, @0]
    @3: SIN[@1]
    @4: ADD[@2, @3]
    @5: MUL[@2, @4]

    @0, @3, and @4 are operands in only one operation each so can be collapsed.
    @1 and @2 are operands in two operations each so are required common
    subexpressions. @1 will become the first common subexpression (x0, x1 / x2)
    and @2 will become the second common subexpression (x3, x0 - exp(x2)). @6 is
    the expression itself so can used directly there resulting in the
    substituted expression x3 * (x3 + sin(x0)).

    This example highlights an important optimisation around operation ordering
    in CSE. The @4 operation could instead be constructed as
    ADD[@1, SUB[@3, @0]]. This is suboptimal CSE as it would require the
    introduction of an additional unnecessary operation.

    """

    def setup(self):
        """Create the required symbols (x1, x2), the expression (y), and its
        Jacobian (G).

        G is the 1x2 matrix that contains the derivatives of y with respect to
        x1 and x2 as the two columns respectively.
        
        """
        x1, x2 = symbols("x1, x2")
        x = Matrix([x1, x2])
        self.y = (sin(x1 / x2) + (x1 / x2) - exp(x2)) * ((x1 / x2) - exp(x2))
        self.G = self.y.diff(x)

    def test_function_cse(self):
        """Expected result from SymPy's CSE on the baby example."""
        x0 = sym.Symbol("x0")
        x1 = sym.Symbol("x1")
        x2 = sym.Symbol("x2")
        x3 = sym.Symbol("x3")

        cse = [
            (x0, x1 / x2),
            (x3, x0 - exp(x2)),
        ]
        expr = [
            x3 * (x3 + sin(x0)),
        ]

        assert cse(self.y) == (cse, expr)

    def test_jacobian_cse(self):
        """Expected result from SymPy's CSE on the baby example's Jacobian."""
        pass

    def time_function_cse(self):
        """Time CSE on the baby example."""
        cse(self.y)

    def time_jacobian_cse(self):
        """Time CSE on the baby example's Jacobian."""
        cse(self.G)

    def time_combined_cse(self):
        """Time simultaneous CSE on the baby example and its Jacobian."""
        cse([self.y, self.G])
