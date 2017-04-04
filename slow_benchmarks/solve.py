# -*- coding: utf-8 -*-

import sympy

class TimeMatrixOperations:
    # first param is the size of the matrix, second is the number of symbols in it
    params = ((6,10), (0, 2, 5))

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
