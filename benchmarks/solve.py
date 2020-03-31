# -*- coding: utf-8 -*-

import sympy

class _Polynomial(object):

    expr = None
    x = sympy.Symbol('x', real=True)
    x0 = sympy.symbols('x0', real=True)
    x1 = sympy.symbols('x1', real=True)

    def __init__(self, c=None):
        self.c = c

    def diff(self, deg):
        return self.expr.diff(self.x, deg)

    # Below are properties to be subclassed
    @property
    def expr(self):
        return sum([c*self.x**o for o, c in enumerate(self.c)])

    def eval(self, x_val, deriv=0):
        return self.expr.diff(self.x, deriv).subs({self.x: x_val})


def _make_poly(order, Poly=None):
    if Poly is None:
        Poly = _Polynomial
    c = [sympy.Symbol('c_' + str(o), real=True) for o in range(order+1)]
    return Poly(c)


def _mk_eqs(wy=3, **kwargs):
    # Equations for fitting a wy*2 - 1 degree polynomial between two points,
    # at end points derivatives are known up to order: wy - 1
    p = _make_poly(2*wy-1, **kwargs)
    y0 = [sympy.Symbol('y0_' + str(i), real=True) for i in range(wy)]
    y1 = [sympy.Symbol('y1_' + str(i), real=True) for i in range(wy)]
    eqs = []
    for i in range(wy):
        eqs.append(p.diff(i).subs({p.x: p.x0}) - y0[i])
        eqs.append(p.diff(i).subs({p.x: p.x1}) - y1[i])
    return eqs, p, (y0, y1)


class TimeSolve01:

    def setup(self):
        self.eqs, self.p, self.y = _mk_eqs(2)  # running with wy=3 is too slow (~5s)

    def time_solve(self):
        sympy.solve(self.eqs, *self.p.c)

    def time_solve_nocheck(self):
        sympy.solve(self.eqs, *self.p.c, check=False)


class TimeRationalSystem:
    """Solve a dense system of linear equations with rational coefficients"""

    M = sympy.Matrix([
        [43,  5, 36,  0, 92, 47, 98, 62, 30, 12, 14, 91, 64, 71, 39, 95,  7,  8, 11,  0, 74],
        [ 4, 94, 75, 67, 46, 28, 49, 54, 28, 15, 61, 23, 45, 24, 63, 50, 12, 59,  9, 25,  6],
        [52, 70, 97, 65,  8, 38, 20, 36, 57, 48, 47, 79,  3, 94, 90, 60, 74, 53, 60, 84, 79],
        [ 0, 82, 61, 63, 89, 44, 78, 90,  9, 38, 41, 72, 75, 57,  9, 83, 53, 93, 54, 31, 12],
        [90, 14, 68,  9, 16, 50, 67, 40, 18, 83, 80, 28, 30, 72, 96, 61, 54,  6, 40,  3, 83],
        [55, 81, 98, 26,  0, 36, 92, 79, 55, 25, 68, 68, 31, 73, 28, 77, 14, 86, 93, 29, 59],
        [72, 39, 18, 62, 77, 93, 66, 49, 76, 70, 63, 86, 20, 41, 81, 74, 39, 65, 53, 92, 79],
        [ 6, 34, 81, 27, 99, 55, 99, 78, 56, 56, 52, 67, 29, 26, 83, 78, 58, 83, 41,  2, 17],
        [10, 24, 88, 59,  5, 44, 89, 34, 96, 53, 92, 73, 19, 76, 51, 23, 62, 64, 40, 63, 67],
        [21, 98, 12, 30, 97, 59, 79, 16, 18, 81, 76, 74, 14, 86, 61, 61, 27, 63, 20, 78, 80],
        [74, 20, 46, 99,  1, 19,  0, 18, 69, 45, 18, 69, 86, 89, 92, 39, 47, 77, 96, 25, 62],
        [60, 43, 44, 97, 74, 89, 65, 50, 38, 95, 73, 37, 57, 24, 81, 51, 74, 74, 75, 53, 32],
        [15, 43, 13, 24, 22, 66, 30,  5, 71, 52, 10, 98, 62, 76, 78, 49, 48, 58,  5, 83,  4],
        [89, 30, 37, 47, 90, 21, 13,  1, 38, 56, 32, 16, 79, 47, 36, 45, 97, 80, 21, 86, 76],
        [28, 45, 95, 46,  5, 31, 32, 35, 60, 18,  6, 74, 97, 42, 42, 92, 83, 52, 37,  5, 35],
        [45,  3, 17, 66, 91, 75,  3, 25, 48, 95, 41,  8, 15, 65, 70, 64, 64, 96, 91, 73, 47],
        [85, 36, 30, 25, 32, 79, 70, 36, 69, 57, 23, 38, 10,  3, 25, 18, 78, 83, 94, 39, 39],
        [ 2, 61, 50,  4,  4, 86, 70,  5, 64, 90, 75,  4, 53, 38, 22, 17, 27, 32, 58, 37, 26],
        [97, 64,  2,  6, 59, 37, 98,  4, 97,  7, 21, 49, 98, 47, 77, 85,  2, 53, 26, 10, 55],
        [59, 93, 94, 42, 25, 42, 26, 73, 73, 61, 43,  5, 99, 62, 48, 75, 43, 96, 12, 91, 46]
    ])

    syms = sympy.symbols('x:20')

    params = [1, 3, 5, 10, 20]

    def setup(self, n):
        Mn = self.M[:n, :n+1]
        self.symsn = self.syms[:n]
        self.eqsn = list(Mn * sympy.Matrix(self.symsn + (1,)))

    def time_solve(self, n):
        sympy.solve(self.eqsn, self.symsn)

    def time_linsolve(self, n):
        sympy.linsolve(self.eqsn, self.symsn)


class TimeRationalSystemSymbol(TimeRationalSystem):
    """Solve a dense system of linear equations with a symbol in coefficients"""


    def setup(self, n):
        super().setup(n)
        y = sympy.Symbol('y')
        self.eqsn = [y*eq for eq in self.eqsn]


class TimeSparseSystem:
    """Solve a large, sparse system of linear equations"""

    def mk_eqs(self, n):
        xs = sympy.symbols('x:{}'.format(n))
        ys = sympy.symbols('y:{}'.format(n))
        syms = xs + ys
        eqs = []
        for xi, yi in zip(xs, ys):
            eqs.extend([xi + yi, xi - yi + 1])
        return eqs, syms

    params = [10, 20, 50, 100]

    def setup(self, n):
        self.eqs, self.syms = self.mk_eqs(n)
        self.Ab = sympy.linear_eq_to_matrix(self.eqs, self.syms)
        self.Aaug = sympy.Matrix.hstack(*self.Ab)

    def time_solve(self, n):
        sympy.solve(self.eqs, self.syms)

    def time_linsolve_eqs(self, n):
        sympy.linsolve(self.eqs, self.syms)

    def time_linsolve_Ab(self, n):
        sympy.linsolve(self.Ab)

    def time_linsolve_Aaug(self, n):
        sympy.linsolve(self.Aaug)

    def time_linear_eq_to_matrix(self, n):
        sympy.linear_eq_to_matrix(self.eqs, self.syms)


class TimeSolveSparsePolySystem:
    """Solve a sparse, separable polynomial system"""

    def make_polysys(self, n):
        xs = sympy.symbols('x:%d' % n)
        ys = sympy.symbols('y:%d' % n)
        eqs = []
        for xi, yi in zip(xs, ys):
            eqs.append(xi**2 + yi**2-1)
            eqs.append(xi + yi - 2)
        syms = xs + ys
        return eqs, syms

    params = [1, 2, 3, 4, 5]

    def setup(self, n):
        self.eqs, self.syms = self.make_polysys(n)

    def time_solve(self, n):
        sympy.solve(self.eqs, self.syms)


def _matrix_solve_setup():

        n = 3

        A = sympy.Matrix(n, n, lambda i, j: sympy.Symbol('a{}{}'.format(i, j)))
        b = sympy.Matrix(n, 1, lambda i, j: sympy.Symbol('b{}{}'.format(i, j)))
        A_sym = sympy.Matrix(n, n, lambda i, j:
                             sympy.Symbol('a{}{}'.format(*sorted((i, j)))))

        return A, b, A_sym


class TimeMatrixSolve:

    params = ['GE', 'LU', 'ADJ']

    def setup(self, name):

        self.A, self.b, _ = _matrix_solve_setup()

    def time_solve(self, name):

        self.A.solve(self.b, method=name)


class TimeMatrixSolve2:

    def setup(self):

        self.A, self.b, self.A_sym = _matrix_solve_setup()

    def time_lusolve(self):

        self.A.LUsolve(self.b)

    def time_cholesky_solve(self):

        self.A_sym.cholesky_solve(self.b)

class TimeMatrixOperations:
    # first param is the size of the matrix, second is the number of symbols in it
    params = ((3,4), (0, 2, 5))

    def setup(self, n, num_symbols):
        from sympy import Matrix, Symbol

        # every test will be based of a submatrix of this matrix
        big_mat = Matrix([[3, 8, 10, 5, 10, 7, 10, 10, 8, 6],
                          [10, 9, 3, 7, 10, 1, 4, 2, 8, 1],
                          [5, 9, 9, 0, 2, 10, 5, 9, 3, 9],
                          [1, 8, 0, 7, 8, 8, 0, 4, 1, 10],
                          [6, 5, 3, 0, 3, 4, 6, 1, 10, 5],
                          [7, 10, 8, 9, 10, 7, 2, 8, 3, 2],
                          [10, 8, 5, 10, 3, 5, 10, 4, 2, 3],
                          [8, 4, 10, 9, 1, 9, 7, 4, 8, 6],
                          [6, 2, 4, 1, 1, 0, 1, 3, 1, 9],
                          [9, 2, 6, 10, 9, 4, 10, 2, 1, 8]])
        symbol_locations = [(2, 2), (1, 9), (0, 0), (0, 7), (9, 1),
                            (6, 9), (8, 9), (4, 0), (3, 8), (3, 2),
                            (2, 8), (1, 8), (5, 3), (5, 9), (6, 4),
                            (5, 5), (7, 9), (5, 1), (1, 0), (3, 3),
                            (7, 1), (2, 5), (1, 5), (4, 4), (4, 2),
                            (7, 3), (3, 4), (6, 6), (9, 5), (1, 6),
                            (9, 0), (3, 1), (0, 4), (8, 3), (2, 3),
                            (3, 9), (9, 6), (4, 8), (9, 3), (8, 0),
                            (6, 7), (5, 7), (8, 6), (3, 6), (4, 5),
                            (1, 2), (9, 8), (7, 4), (8, 8), (6, 1),
                            (0, 3), (4, 7), (7, 0), (9, 7), (5, 4),
                            (7, 6), (2, 6), (3, 7), (3, 5), (1, 4),
                            (5, 0), (4, 9), (7, 8), (6, 8), (2, 1),
                            (9, 2), (3, 0), (7, 7), (2, 7), (2, 0),
                            (8, 1), (7, 5), (4, 3), (1, 3), (9, 9),
                            (0, 6), (4, 1), (5, 8), (8, 4), (0, 8),
                            (2, 4), (9, 4), (7, 2), (1, 7), (6, 3),
                            (6, 5), (5, 2), (6, 0), (0, 1), (8, 2),
                            (2, 9), (8, 5), (0, 2), (0, 9), (8, 7),
                            (4, 6), (0, 5), (1, 1), (6, 2), (5, 6)]

        symbol_locations = [(i, j) for (i, j) in symbol_locations if i <= n and j <= n]
        symbol_locations = symbol_locations[:num_symbols]

        def entry(i, j):
            if (i, j) in symbol_locations:
                return Symbol('x')
            return big_mat[i, j]
        self.A = Matrix(n, n, entry)

    def time_rank(self, n, num_symbols):
        self.A.rank()

    def time_rref(self, n, num_symbols):
        self.A.rref()

    def time_det(self, n, num_symbols):
        self.A.det()

    def time_det_bareiss(self, n, num_symbols):
        self.A.det(method='bareiss')

    def time_det_berkowitz(self, n, num_symbols):
        self.A.det(method='berkowitz')


class TimeMatrixArithmetic:
    # first param is the size of the matrix, second is the number of symbols in it
    params = ((3, 4, 6, 10), (0, 5))

    def setup(self, n, num_symbols):
        from sympy import Matrix, Symbol

        # every test will be based off a submatrix of this matrix
        big_mat = Matrix([[3, 8, 10, 5, 10, 7, 10, 10, 8, 6],
                          [10, 9, 3, 7, 10, 1, 4, 2, 8, 1],
                          [5, 9, 9, 0, 2, 10, 5, 9, 3, 9],
                          [1, 8, 0, 7, 8, 8, 0, 4, 1, 10],
                          [6, 5, 3, 0, 3, 4, 6, 1, 10, 5],
                          [7, 10, 8, 9, 10, 7, 2, 8, 3, 2],
                          [10, 8, 5, 10, 3, 5, 10, 4, 2, 3],
                          [8, 4, 10, 9, 1, 9, 7, 4, 8, 6],
                          [6, 2, 4, 1, 1, 0, 1, 3, 1, 9],
                          [9, 2, 6, 10, 9, 4, 10, 2, 1, 8]])
        symbol_locations = [(2, 2), (1, 9), (0, 0), (0, 7), (9, 1),
                            (6, 9), (8, 9), (4, 0), (3, 8), (3, 2),
                            (2, 8), (1, 8), (5, 3), (5, 9), (6, 4),
                            (5, 5), (7, 9), (5, 1), (1, 0), (3, 3),
                            (7, 1), (2, 5), (1, 5), (4, 4), (4, 2),
                            (7, 3), (3, 4), (6, 6), (9, 5), (1, 6),
                            (9, 0), (3, 1), (0, 4), (8, 3), (2, 3),
                            (3, 9), (9, 6), (4, 8), (9, 3), (8, 0),
                            (6, 7), (5, 7), (8, 6), (3, 6), (4, 5),
                            (1, 2), (9, 8), (7, 4), (8, 8), (6, 1),
                            (0, 3), (4, 7), (7, 0), (9, 7), (5, 4),
                            (7, 6), (2, 6), (3, 7), (3, 5), (1, 4),
                            (5, 0), (4, 9), (7, 8), (6, 8), (2, 1),
                            (9, 2), (3, 0), (7, 7), (2, 7), (2, 0),
                            (8, 1), (7, 5), (4, 3), (1, 3), (9, 9),
                            (0, 6), (4, 1), (5, 8), (8, 4), (0, 8),
                            (2, 4), (9, 4), (7, 2), (1, 7), (6, 3),
                            (6, 5), (5, 2), (6, 0), (0, 1), (8, 2),
                            (2, 9), (8, 5), (0, 2), (0, 9), (8, 7),
                            (4, 6), (0, 5), (1, 1), (6, 2), (5, 6)]

        symbol_locations = [(i, j) for (i, j) in symbol_locations if i <= n and j <= n]
        symbol_locations = symbol_locations[:num_symbols]

        # create a matrix with the appropriate number of symbols based on
        # a pre-determined list of positions.
        def entry(i, j):
            if (i, j) in symbol_locations:
                return Symbol('x')
            return big_mat[i, j]
        self.A = Matrix(n, n, entry)

    def time_dense_multiply(self, n, num_symbols):
        self.A * self.A

    def time_dense_add(self, n, num_symbols):
        self.A + self.A
