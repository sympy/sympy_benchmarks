from sympy import MatrixSymbol, Add, MatAdd, Mul, MatMul, symbols

n = symbols('n')

A = MatrixSymbol("A", n, n)
B = MatrixSymbol("B", n, n)
args = (A, B, A*B, B*A, A**2, B**2, A**-1, B**-1, A*B**-1, B*A**-1, A**-1*B, B*A**-1, A**-2, B**-2, A**-1*B**-1, B**-1*A**-1, A, B, A*B, B*A, A**2, B**2, A**-1, B**-1, A*B**-1, B*A**-1, A**-1*B, B*A**-1, A**-2, B**-2, A**-1*B**-1, B**-1*A**-1)

class TimeMatrixExpression:
    def time_Add():
        Add(*args)

    def time_MatAdd():
        MatAdd(*args)

    def time_MatAdd_doit():
        MatAdd(*args).doit()

    def time_Mul():
        Mul(*args)

    def time_MatMul():
        MatMul(*args)

    def time_MatMul_doit():
        MatMul(*args).doit()
