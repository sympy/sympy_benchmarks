from sympy import MatrixSymbol, Add, MatAdd, Mul, MatMul, Symbol, Matrix
from sympy import \
    MutableDenseMatrix, ImmutableDenseMatrix, \
    MutableSparseMatrix, ImmutableSparseMatrix
from sympy import S

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
        self.M = Matrix([
            [0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 2, 0, 0],
            [0, 1, 2, 3, 0],
            [0, 1, 2, 3, 4]])

    def time_eigenvals(self):
        self.M.eigenvals()


class TimeBlockDiagonalEigenvals:
    """Benchmark examples obtained by similarly transforming random
    block diagonal matrices with permutation matrices to make it look
    like non block diagonal.

    The original block matrices can be obtained by using
    Matrix.connected_components_decomposition.
    """
    def setup(self):
        self.m22 = Matrix([
            [26, 0, 0, 7], [0, 27, 21, 0],
            [0, 18, 89, 0], [13, 0, 0, 28]])
        self.m222 = Matrix([
            [37, 0, 0, 0, 0, 5], [0, 32, 0, 0, 33, 0], [0, 0, 78, 91, 0, 0],
            [0, 0, 51, 97, 0, 0], [0, 97, 0, 0, 77, 0], [37, 0, 0, 0, 0, 61]])
        self.m2222 = Matrix([
            [87, 0, 12, 0, 0, 0, 0, 0], [0, 35, 0, 0, 0, 0, 0, 51],
            [31, 0, 47, 0, 0, 0, 0, 0], [0, 0, 0, 84, 0, 41, 0, 0],
            [0, 0, 0, 0, 70, 0, 57, 0], [0, 0, 0, 56, 0, 30, 0, 0],
            [0, 0, 0, 0, 54, 0, 55, 0], [0, 61, 0, 0, 0, 0, 0, 0]])
        self.m33 = Matrix([
            [48, 0, 44, 0, 0, 67], [0, 16, 0, 28, 61, 0],
            [5, 0, 5, 0, 0, 52], [0, 28, 0, 78, 13, 0],
            [0, 3, 0, 52, 35, 0], [98, 0, 86, 0, 0, 70]])
        self.m333 = Matrix([
            [60, 0, 74, 0, 0, 0, 0, 39, 0], [0, 36, 0, 0, 14, 0, 10, 0, 0],
            [33, 0, 32, 0, 0, 0, 0, 46, 0], [0, 0, 0, 9, 0, 46, 0, 0, 7],
            [0, 51, 0, 0, 92, 0, 46, 0, 0], [0, 0, 0, 86, 0, 21, 0, 0, 16],
            [0, 55, 0, 0, 28, 0, 12, 0, 0], [6, 0, 1, 0, 0, 0, 0, 31, 0],
            [0, 0, 0, 61, 0, 59, 0, 0, 57]])

    def time_eigenvals_22(self):
        self.m22.eigenvals()

    def time_eigenvals_222(self):
        self.m222.eigenvals()

    def time_eigenvals_2222(self):
        self.m2222.eigenvals()

    def time_eigenvals_33(self):
        self.m33.eigenvals()

    def time_eigenvals_333(self):
        self.m333.eigenvals()


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


class TimeMatrixPower:
    Case1 = Matrix(8, 8, [n+1]*64)
    Case2 = Matrix(8, 8, [n+i for i in range (64)])
    Case3 = Matrix(S('''[
            [             -3/4,       45/32 - 37*I/16,         1/4 + I/2,      -129/64 - 9*I/64,      1/4 - 5*I/16,      65/128 + 87*I/64,         -9/32 - I/16,      183/256 - 97*I/128],
            [-149/64 + 49*I/32, -177/128 - 1369*I/128,  125/64 + 87*I/64, -2063/256 + 541*I/128,  85/256 - 33*I/16,  805/128 + 2415*I/512, -219/128 + 115*I/256, 6301/4096 - 6609*I/1024],
            [          1/2 - I,         9/4 + 55*I/16,              -3/4,       45/32 - 37*I/16,         1/4 + I/2,      -129/64 - 9*I/64,         1/4 - 5*I/16,        65/128 + 87*I/64],
            [   -5/8 - 39*I/16,   2473/256 + 137*I/64, -149/64 + 49*I/32, -177/128 - 1369*I/128,  125/64 + 87*I/64, -2063/256 + 541*I/128,     85/256 - 33*I/16,    805/128 + 2415*I/512],
            [            1 + I,         -19/4 + 5*I/4,           1/2 - I,         9/4 + 55*I/16,              -3/4,       45/32 - 37*I/16,            1/4 + I/2,        -129/64 - 9*I/64],
            [         21/8 + I,    -537/64 + 143*I/16,    -5/8 - 39*I/16,   2473/256 + 137*I/64, -149/64 + 49*I/32, -177/128 - 1369*I/128,     125/64 + 87*I/64,   -2063/256 + 541*I/128],
            [               -2,         17/4 - 13*I/2,             1 + I,         -19/4 + 5*I/4,           1/2 - I,         9/4 + 55*I/16,                 -3/4,         45/32 - 37*I/16],
            [     1/4 + 13*I/4,    -825/64 - 147*I/32,          21/8 + I,    -537/64 + 143*I/16,    -5/8 - 39*I/16,   2473/256 + 137*I/64,    -149/64 + 49*I/32,   -177/128 - 1369*I/128]]'''))

    def time_Case1(self):
        m = self.Case1**4

    def time_Case2(self):
        m = self.Case2**4

    def time_Case3(self):
        m = self.Case3**4
