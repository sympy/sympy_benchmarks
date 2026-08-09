class TimeMatrixMultiply:
    def setup(self):
        from sympy import Matrix, symbols
        x = symbols('x')
        self.A = Matrix([[x+i for i in range(30)] for j in range(30)])

    def time_matrix_multiply(self):
        self.A * self.A