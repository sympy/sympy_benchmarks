from sympy import MatrixSymbol, Add, MatAdd, Mul, MatMul, Symbol, Matrix
from sympy import \
    MutableDenseMatrix, ImmutableDenseMatrix, \
    MutableSparseMatrix, ImmutableSparseMatrix

n = Symbol('n')

A = MatrixSymbol("A", n, n)
B = MatrixSymbol("B", n, n)
args = (
    A, B, A*B, B*A, A**2, B**2, A**-1, B**-1, A*B**-1, B*A**-1, A**-1*B,
    B*A**-1, A**-2, B**-2, A**-1*B**-1, B**-1*A**-1, A, B, A*B, B*A, A**2,
    B**2, A**-1, B**-1, A*B**-1, B*A**-1, A**-1*B, B*A**-1, A**-2, B**-2,
    A**-1*B**-1, B**-1*A**-1)


class TimeMatrixExpression:
    def time_Add(self):
        Add(*args)

    def time_MatAdd(self):
        MatAdd(*args)

    def time_MatAdd_doit(self):
        MatAdd(*args).doit()

    def time_Mul(self):
        Mul(*args)

    def time_MatMul(self):
        MatMul(*args)

    def time_MatMul_doit(self):
        MatMul(*args).doit()


class TimeDiagonalEigenvals:
    def setup(self):
        def entry(i, j):
            if i == j:
                return i
            elif i > j:
                return j
            else:
                return 0
        self.M = Matrix(5, 5, entry)

    def time_eigenvals(self):
        self.M.eigenvals()


class TimeMatrixGetItem:
    def setup(self):
        self.M1 = MutableDenseMatrix.zeros(5, 5)
        self.M2 = ImmutableDenseMatrix.zeros(5, 5)
        self.M3 = MutableSparseMatrix.zeros(5, 5)
        self.M4 = ImmutableSparseMatrix.zeros(5, 5)

    def time_MutableDenseMatrix_getitem(self):
        m = self.M1
        for i in range(m.rows):
            for j in range(m.cols):
                m[i, j]

    def time_ImmutableDenseMatrix_getitem(self):
        m = self.M2
        for i in range(m.rows):
            for j in range(m.cols):
                m[i, j]

    def time_MutableSparseMatrix_getitem(self):
        m = self.M3
        for i in range(m.rows):
            for j in range(m.cols):
                m[i, j]

    def time_ImmutableSparseMatrix_getitem(self):
        m = self.M4
        for i in range(m.rows):
            for j in range(m.cols):
                m[i, j]
