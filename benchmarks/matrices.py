from sympy import MatrixSymbol, Add, MatAdd, Mul, MatMul, Symbol, Matrix

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
