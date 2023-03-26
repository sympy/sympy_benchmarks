"""Benchmarks for common subexpression elimination (CSE)."""

from functools import reduce
from operator import add

import sympy as sym
from sympy import cse, exp, sin, symbols, tan, Matrix, ImmutableDenseMatrix, MatAdd, MatMul, Transpose, Inverse, \
    MatrixSymbol
from sympy.core.singleton import SingletonRegistry


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
        """Expected result from CSE on the baby example."""
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

    def time_function_cse(self):
        """Time CSE on the baby example."""
        cse(self.y)

    def time_jacobian_cse(self):
        """Time CSE on the baby example's Jacobian."""
        cse(self.G)

    def time_combined_cse(self):
        """Time simultaneous CSE on the baby example and its Jacobian."""
        cse([self.y, self.G])


class GriewankLighthouseExampleCSE:
    """Simple matrix test function with multiple repeated subexpressions.

    Function is the "lighthouse example" taken from Griewank, A., & Walther, A.
    (2008). Evaluating derivatives: principles and techniques of algorithmic
    differentiation. SIAM.

    The lighthouse example function expressed as a tree structure is as follows:

                               (MATRIX)
                        __________|___________
                       /                      \    
                     (MUL)                  (MUL)
                     __|__                   _|_              
                    /     \                 /   \              
                  (MUL) (gamma)          (DIV) (nu)      
                   _|_               ______|_____          
                  /   \             /            \             
               (DIV) (nu)         (TAN)        (SUB)             
           ______|_____             |          __|__              
          /            \            |         /     \               
        (TAN)        (SUB)        (MUL)   (gamma) (TAN)                
          |          __|__         _|_              |                
          |         /     \       /   \             |                 
        (MUL)   (gamma) (TAN) (omega) (t)         (MUL)                
         _|_              |                        _|_                
        /   \             |                       /   \            
    (omega) (t)         (MUL)                 (omega) (t)            
                         _|_             
                        /   \             
                    (omega) (t)          

    It involves 2 DIV, 7 MUL, 2 SUB, and 4 TAN operations. Additionally, one
    matrix population is required.

    When CSE is conducted on the expression, the following intermediate terms
    are introduced:

    @0: MUL[omega, t]
    @1: TAN[@0]
    @2: SUB[gamma, @1]
    @3: DIV[@1, @2]
    @4: MUL[nu, @3]
    @5: MUL[gamma, @4]

    @0, @2, and @3 are operands in only one operation each so can be collapsed.
    @1 is an operand in four operations and @4 is both a required expression and
    an operand in an expression so both are required common subexpressions. @1
    will become the first common subexpression (x0, tan(omega * t)) and @4 will
    become the second common subexpression (x1, nu * x0 / (gamma - x0)). @5 is
    one of the required expressions in the matrix so can used directly there
    resulting in the substituted matrix expression Matrix([x1, gamma * x1]).

    """

    def setup(self):
        """Create the required symbols (nu, gamma, omega, t), the matrix of
        expressions (y), and its Jacobian (G).

        G is the 2x4 matrix that contains the derivatives of y with respect to
        nu, gamma, omega, and t as the four columns respectively.
        
        """
        nu, gamma, omega, t = symbols("nu, gamma, omega, t")
        x = Matrix([nu, gamma, omega, t])
        self.y = Matrix([
            nu * tan(omega * t) / (gamma - tan(omega * t)),
            nu * gamma * tan(omega * t) / (gamma - tan(omega * t)),
        ])
        self.G = self.y.jacobian(x)

    def test_function_cse(self):
        """Expected result from CSE on the lighthouse example."""
        nu = sym.Symbol("nu")
        gamma = sym.Symbol("gamma")
        omega = sym.Symbol("omega")
        t = sym.Symbol("t")
        x0 = sym.Symbol("x0")
        x1 = sym.Symbol("x1")

        cse = [
            (x0, tan(omega * t)),
            (x1, nu * x0 / (gamma - x0)),
        ]
        expr = [
            Matrix([x1, gamma * x1]),
        ]

        assert cse(self.y) == (cse, expr)

    def time_function_cse(self):
        """Time CSE on the lighthouse example."""
        cse(self.y)

    def time_jacobian_cse(self):
        """Time CSE on the lighthouse example's Jacobian."""
        cse(self.G)

    def time_combined_cse(self):
        """Time simultaneous CSE on the lighthouse example and its Jacobian."""
        cse([self.y, self.G])


S = SingletonRegistry()


class KalmanFilterMatrixEquationCSE:
    """Kalman filter example from Matthew Rocklin's SciPy 2013 talk.

    Talk titled: "Matrix Expressions and BLAS/LAPACK; SciPy 2013 Presentation"

    https://pyvideo.org/scipy-2013/matrix-expressions-and-blaslapack-scipy-2013-pr

    Notes
    =====

    Equations are:
        new_mu = mu + Sigma*H.T * (R + H*Sigma*H.T).I * (H*mu - data)
        new_Sigma = Sigma - Sigma*H.T * (R + H*Sigma*H.T).I * H * Sigma

    """

    def setup(self):
        """Create the 2x2 matrix equations for mu and Sigma."""
        N = 2
        mu = ImmutableDenseMatrix(symbols(f'mu:{N}'))
        Sigma = ImmutableDenseMatrix(symbols(f'Sigma:{N * N}')).reshape(N, N)
        H = ImmutableDenseMatrix(symbols(f'H:{N * N}')).reshape(N, N)
        R = ImmutableDenseMatrix(symbols(f'R:{N * N}')).reshape(N, N)
        data = ImmutableDenseMatrix(symbols(f'data:{N}'))
        self.new_mu = MatAdd(
            mu,
            MatMul(
                Sigma,
                Transpose(H),
                Inverse(MatAdd(R, MatMul(H, Sigma, Transpose(H)))),
                MatAdd(MatMul(H, mu), MatMul(S.NegativeOne, data)),
            )
        )
        self.new_Sigma = MatAdd(
            Sigma,
            MatMul(
                S.NegativeOne,
                Sigma,
                Transpose(H),
                Inverse(MatAdd(R, MatMul(H, Sigma, Transpose(H)))),
                H,
                Sigma,
            )
        )

        x0 = MatrixSymbol('x0', N, N)
        x1 = MatrixSymbol('x1', N, N)
        replacements_expected = [
            (x0, Transpose(H)),
            (x1, Inverse(MatAdd(R, MatMul(H, Sigma, x0)))),
        ]
        reduced_exprs_expected = [
            MatAdd(
                mu,
                MatMul(
                    Sigma,
                    x0,
                    x1,
                    MatAdd(MatMul(H, mu), MatMul(S.NegativeOne, data)),
                ),
            ),
            MatAdd(Sigma, MatMul(S.NegativeOne, Sigma, x0, x1, H, Sigma)),
        ]
        self.cse_expr_expected = (replacements_expected, reduced_exprs_expected)

    def test_cse(self):
        """Expected result from CSE on the Kalman filter example."""
        cse_expr = cse([self.new_mu, self.new_Sigma])
        assert cse_expr == self.cse_expr_expected

    def time_cse(self):
        """Time CSE on the Kalman filter example."""
        cse([self.new_mu, self.new_Sigma])

