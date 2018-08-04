from sympy import Matrix, Symbol


class TimeDiagonalEigenvals:

    def setup(self):
        n = 20

        M = []
        for i in range(n):
            row = [j for j in range(i)] + [Symbol('x'+str(i))] + [0]*(n-i-1)
            M.append(row)

        self.M = Matrix(M)

    def time_eigenvals(self):
        self.M.eigenvals()
