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