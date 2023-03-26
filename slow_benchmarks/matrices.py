from sympy import Matrix, symbols, SparseMatrix
from sympy import S
from sympy.simplify.simplify import simplify

_TEST_SIMPLIFY = False # test simplify after operation?

x, y, z = symbols('x y z')

A = Matrix(8, 8, ([1+x, 1-x]*4 + [1-x, 1+x]*4)*4)
B = Matrix(8, 8, [x+i for i in range (64)])
C = Matrix(S('''[
            [             -3/4,       45/32 - 37*I/16,         1/4 + I/2,      -129/64 - 9*I/64,      1/4 - 5*I/16,      65/128 + 87*I/64,         -9/32 - I/16,      183/256 - 97*I/128],
            [-149/64 + 49*I/32, -177/128 - 1369*I/128,  125/64 + 87*I/64, -2063/256 + 541*I/128,  85/256 - 33*I/16,  805/128 + 2415*I/512, -219/128 + 115*I/256, 6301/4096 - 6609*I/1024],
            [          1/2 - I,         9/4 + 55*I/16,              -3/4,       45/32 - 37*I/16,         1/4 + I/2,      -129/64 - 9*I/64,         1/4 - 5*I/16,        65/128 + 87*I/64],
            [   -5/8 - 39*I/16,   2473/256 + 137*I/64, -149/64 + 49*I/32, -177/128 - 1369*I/128,  125/64 + 87*I/64, -2063/256 + 541*I/128,     85/256 - 33*I/16,    805/128 + 2415*I/512],
            [            1 + I,         -19/4 + 5*I/4,           1/2 - I,         9/4 + 55*I/16,              -3/4,       45/32 - 37*I/16,            1/4 + I/2,        -129/64 - 9*I/64],
            [         21/8 + I,    -537/64 + 143*I/16,    -5/8 - 39*I/16,   2473/256 + 137*I/64, -149/64 + 49*I/32, -177/128 - 1369*I/128,     125/64 + 87*I/64,   -2063/256 + 541*I/128],
            [               -2,         17/4 - 13*I/2,             1 + I,         -19/4 + 5*I/4,           1/2 - I,         9/4 + 55*I/16,                 -3/4,         45/32 - 37*I/16],
            [     1/4 + 13*I/4,    -825/64 - 147*I/32,          21/8 + I,    -537/64 + 143*I/16,    -5/8 - 39*I/16,   2473/256 + 137*I/64,    -149/64 + 49*I/32,   -177/128 - 1369*I/128]]'''))
D = Matrix(S('''[
            [             -3/4,       45/32 - 37*I/16,         1/4 + x/2,      -129/64 - 9*y/64,      1/4 - 5*z/16,      65/128 + 87*I/64,         -9/32 - x/16,      183/256 - 97*y/128],
            [-149/64 + 49*z/32, -177/128 - 1369*I/128,  125/64 + 87*x/64, -2063/256 + 541*y/128,  85/256 - 33*z/16,  805/128 + 2415*I/512, -219/128 + 115*x/256, 6301/4096 - 6609*y/1024],
            [          1/2 - z,         9/4 + 55*I/16,              -3/4,       45/32 - 37*x/16,         1/4 + y/2,      -129/64 - 9*z/64,         1/4 - 5*I/16,        65/128 + 87*x/64],
            [   -5/8 - 39*y/16,   2473/256 + 137*z/64, -149/64 + 49*I/32, -177/128 - 1369*x/128,  125/64 + 87*y/64, -2063/256 + 541*z/128,     85/256 - 33*I/16,    805/128 + 2415*x/512],
            [            1 + y,         -19/4 + 5*z/4,           1/2 - I,         9/4 + 55*x/16,              -3/4,       45/32 - 37*y/16,            1/4 + z/2,        -129/64 - 9*I/64],
            [         21/8 + x,    -537/64 + 143*y/16,    -5/8 - 39*z/16,   2473/256 + 137*I/64, -149/64 + 49*x/32, -177/128 - 1369*y/128,     125/64 + 87*z/64,   -2063/256 + 541*I/128],
            [               -2,         17/4 - 13*x/2,             1 + y,         -19/4 + 5*z/4,           1/2 - I,         9/4 + 55*x/16,                 -3/4,         45/32 - 37*y/16],
            [     1/4 + 13*z/4,    -825/64 - 147*I/32,          21/8 + x,    -537/64 + 143*y/16,    -5/8 - 39*z/16,   2473/256 + 137*I/64,    -149/64 + 49*x/32,   -177/128 - 1369*y/128]]'''))

_n         = 6
A, B, C, D = A[:_n,:_n], B[:_n,:_n], C[:_n,:_n], D[:_n,:_n]

# has eigenvects
AE = Matrix([
    [    0, 1 - x, x + 1, 1 - x],
    [1 - x, x + 1,     0, x + 1],
    [    0, 1 - x, x + 1, 1 - x],
    [    0,     0,     1 - x, 0]])
BE = Matrix([
    [    x,  x + 1,      0,      0],
    [x + 8,  x + 9,      0, x + 11],
    [    0, x + 17, x + 18,      0],
    [    0,      0,      0, x + 27]])
CE = Matrix(S('''[
            [             -3/4,                     0,         1/4 + I/2,                     0],
            [                0, -177/128 - 1369*I/128,                 0, -2063/256 + 541*I/128],
            [          1/2 - I,                     0,                 0,                     0],
            [                0,                     0,                 0, -177/128 - 1369*I/128]]'''))
DE = Matrix(S('''[
            [                0,       45/32 - 37*I/16,         1/4 + x/2,                     0],
            [                0,                     0,                 0, -2063/256 + 541*y/128],
            [                0,                     0,                 0,                     0],
            [                0,   2473/256 + 137*z/64,                 0,                     0]]'''))

# diagonalizable
AD = Matrix([
    [x + 1,  1 - x,      0,      0],
    [1 - x,  x + 1,      0,  x + 1],
    [    0,  1 - x,  x + 1,      0],
    [    0,      0,      0,  x + 1]])
BD = Matrix([
    [    x,  x + 1,      0,      0],
    [x + 8,  x + 9,      0, x + 11],
    [    0, x + 17, x + 18,      0],
    [    0,      0,      0, x + 27]])
CD = Matrix(S('''[
    [             -3/4,       45/32 - 37*I/16,                   0,                     0],
    [-149/64 + 49*I/32, -177/128 - 1369*I/128,                   0, -2063/256 + 541*I/128],
    [                0,         9/4 + 55*I/16, 2473/256 + 137*I/64,                     0],
    [                0,                     0,                   0, -177/128 - 1369*I/128]]'''))
DD = Matrix(S('''[
    [             -3/4,       45/32 - 37*I/16,                   0,                     0],
    [-149/64 + 49*z/32, -177/128 - 1369*I/128,                   0,  541*y/128 - 2063/256],
    [                0,         9/4 + 55*I/16, 137*z/64 + 2473/256,                     0],
    [                0,                     0,                   0, -1369*x/128 - 177/128]]'''))

ADS = SparseMatrix(AD)
BDS = SparseMatrix(BD)
CDS = SparseMatrix(CD)
DDS = SparseMatrix(DD)

O4 = Matrix(4, 1, [1, 1, 1, 1])


class TimePow4:
    def time_A(self): A**4
    def time_B(self): B**4
    def time_C(self): C**4
    def time_D(self): D**4

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): simplify(A**4)
        def time_B_simplify(self): simplify(B**4)
        def time_C_simplify(self): simplify(C**4)
        def time_D_simplify(self): simplify(D**4)

class TimePow16:
    def time_A(self): A**16
    def time_B(self): B**16
    def time_C(self): C**16
    def time_D(self): D**16

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): simplify(A**16)
        def time_B_simplify(self): simplify(B**16)
        def time_C_simplify(self): simplify(C**16)
        def time_D_simplify(self): simplify(D**16)

class TimeCharPoly:
    def time_A(self): A.charpoly()
    def time_B(self): B.charpoly()
    def time_C(self): C.charpoly()
    def time_D(self): D.charpoly()

    if _TEST_SIMPLIFY:
        def time_A_simp_ident(self): A.charpoly(simplify=lambda e: e)
        def time_B_simp_ident(self): B.charpoly(simplify=lambda e: e)
        def time_C_simp_ident(self): C.charpoly(simplify=lambda e: e)
        def time_D_simp_ident(self): D.charpoly(simplify=lambda e: e)

class TimeRREF:
    def time_A(self): A.rref()
    def time_B(self): B.rref()
    def time_C(self): C.rref()
    def time_D(self): D.rref()

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): simplify(A.rref()[0])
        def time_B_simplify(self): simplify(B.rref()[0])
        def time_C_simplify(self): simplify(C.rref()[0])
        def time_D_simplify(self): simplify(D.rref()[0])

class TimeEigenVals:
    def time_A(self): A.eigenvals()
    def time_B(self): B.eigenvals()
    def time_C(self): C.eigenvals()
    def time_D(self): D.eigenvals()

class TimeEigenVects:
    def time_A(self): AE.eigenvects()
    def time_B(self): BE.eigenvects()
    def time_C(self): CE.eigenvects()
    def time_D(self): DE.eigenvects()

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): [simplify(e) for e in sum((e[2] for e in AE.eigenvects()), [])]
        def time_B_simplify(self): [simplify(e) for e in sum((e[2] for e in BE.eigenvects()), [])]
        def time_C_simplify(self): [simplify(e) for e in sum((e[2] for e in CE.eigenvects()), [])]
        def time_D_simplify(self): [simplify(e) for e in sum((e[2] for e in DE.eigenvects()), [])]

class TimeLeftEigenVects:
    def time_A(self): AE.left_eigenvects()
    def time_B(self): BE.left_eigenvects()
    def time_C(self): CE.left_eigenvects()
    def time_D(self): DE.left_eigenvects()

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): [simplify(e) for e in AE.left_eigenvects()]
        def time_B_simplify(self): [simplify(e) for e in BE.left_eigenvects()]
        def time_C_simplify(self): [simplify(e) for e in CE.left_eigenvects()]
        def time_D_simplify(self): [simplify(e) for e in DE.left_eigenvects()]

class TimeDetBerkowitz:
    def time_A(self): A.det('berkowitz')
    def time_B(self): B.det('berkowitz')
    def time_C(self): C.det('berkowitz')
    def time_D(self): D.det('berkowitz')

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): simplify(A.det('berkowitz'))
        def time_B_simplify(self): simplify(B.det('berkowitz'))
        def time_C_simplify(self): simplify(C.det('berkowitz'))
        def time_D_simplify(self): simplify(D.det('berkowitz'))

class TimeDetBareiss:
    def time_A(self): A.det('bareiss')
    def time_B(self): B.det('bareiss')
    def time_C(self): C.det('bareiss')
    def time_D(self): D.det('bareiss')

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): simplify(A.det('bareiss'))
        def time_B_simplify(self): simplify(B.det('bareiss'))
        def time_C_simplify(self): simplify(C.det('bareiss'))
        def time_D_simplify(self): simplify(D.det('bareiss'))

class TimeDetLU:
    def time_A(self): A.det('lu')
    def time_B(self): B.det('lu')
    def time_C(self): C.det('lu')
    def time_D(self): D.det('lu')

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): simplify(A.det('lu'))
        def time_B_simplify(self): simplify(B.det('lu'))
        def time_C_simplify(self): simplify(C.det('lu'))
        def time_D_simplify(self): simplify(D.det('lu'))

class TimeInvGE:
    def time_A(self): AD.inv(method='GE')
    def time_B(self): BD.inv(method='GE')
    def time_C(self): CD.inv(method='GE')
    def time_D(self): DD.inv(method='GE')

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): simplify(AD.inv(method='GE'))
        def time_B_simplify(self): simplify(BD.inv(method='GE'))
        def time_C_simplify(self): simplify(CD.inv(method='GE'))
        def time_D_simplify(self): simplify(DD.inv(method='GE'))

class TimeInvLU:
    def time_A(self): AD.inv(method='LU')
    def time_B(self): BD.inv(method='LU')
    def time_C(self): CD.inv(method='LU')
    def time_D(self): DD.inv(method='LU')

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): simplify(AD.inv(method='LU'))
        def time_B_simplify(self): simplify(BD.inv(method='LU'))
        def time_C_simplify(self): simplify(CD.inv(method='LU'))
        def time_D_simplify(self): simplify(DD.inv(method='LU'))

class TimeInvADJ:
    def time_A(self): AD.inv(method='ADJ')
    def time_B(self): BD.inv(method='ADJ')
    def time_C(self): CD.inv(method='ADJ')
    def time_D(self): DD.inv(method='ADJ')

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): simplify(AD.inv(method='ADJ'))
        def time_B_simplify(self): simplify(BD.inv(method='ADJ'))
        def time_C_simplify(self): simplify(CD.inv(method='ADJ'))
        def time_D_simplify(self): simplify(DD.inv(method='ADJ'))

class TimeInvCH:
    def time_A(self): ADS.inv(method='CH')
    def time_B(self): BDS.inv(method='CH')
    def time_C(self): CDS.inv(method='CH')
    def time_D(self): DDS.inv(method='CH')

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): simplify(ADS.inv(method='CH'))
        def time_B_simplify(self): simplify(BDS.inv(method='CH'))
        def time_C_simplify(self): simplify(CDS.inv(method='CH'))
        def time_D_simplify(self): simplify(DDS.inv(method='CH'))

class TimeInvLDL:
    def time_A(self): ADS.inv(method='LDL')
    def time_B(self): BDS.inv(method='LDL')
    def time_C(self): CDS.inv(method='LDL')
    def time_D(self): DDS.inv(method='LDL')

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): simplify(ADS.inv(method='LDL'))
        def time_B_simplify(self): simplify(BDS.inv(method='LDL'))
        def time_C_simplify(self): simplify(CDS.inv(method='LDL'))
        def time_D_simplify(self): simplify(DDS.inv(method='LDL'))

class TimeCoFactor:
    def time_A(self): A.cofactor(0, 0)
    def time_B(self): B.cofactor(0, 0)
    def time_C(self): C.cofactor(0, 0)
    def time_D(self): D.cofactor(0, 0)

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): simplify(A.cofactor(0, 0))
        def time_B_simplify(self): simplify(B.cofactor(0, 0))
        def time_C_simplify(self): simplify(C.cofactor(0, 0))
        def time_D_simplify(self): simplify(D.cofactor(0, 0))

class TimeCoFactorMatrix:
    def time_A(self): A.cofactor_matrix()
    def time_B(self): B.cofactor_matrix()
    def time_C(self): C.cofactor_matrix()
    def time_D(self): D.cofactor_matrix()

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): simplify(A.cofactor_matrix())
        def time_B_simplify(self): simplify(B.cofactor_matrix())
        def time_C_simplify(self): simplify(C.cofactor_matrix())
        def time_D_simplify(self): simplify(D.cofactor_matrix())

class TimeEchelonForm:
    def time_A(self): A.echelon_form()
    def time_B(self): B.echelon_form()
    def time_C(self): C.echelon_form()
    def time_D(self): D.echelon_form()

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): simplify(A.echelon_form())
        def time_B_simplify(self): simplify(B.echelon_form())
        def time_C_simplify(self): simplify(C.echelon_form())
        def time_D_simplify(self): simplify(D.echelon_form())

class TimeNullSpace:
    def time_A(self): A.nullspace()
    def time_B(self): B.nullspace()
    def time_C(self): C.nullspace()
    def time_D(self): D.nullspace()

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): [simplify(e) for e in A.nullspace()]
        def time_B_simplify(self): [simplify(e) for e in B.nullspace()]
        def time_C_simplify(self): [simplify(e) for e in C.nullspace()]
        def time_D_simplify(self): [simplify(e) for e in D.nullspace()]

class TimeRowSpace:
    def time_A(self): A.rowspace()
    def time_B(self): B.rowspace()
    def time_C(self): C.rowspace()
    def time_D(self): D.rowspace()

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): [simplify(e) for e in A.rowspace()]
        def time_B_simplify(self): [simplify(e) for e in B.rowspace()]
        def time_C_simplify(self): [simplify(e) for e in C.rowspace()]
        def time_D_simplify(self): [simplify(e) for e in D.rowspace()]

class TimeColumnSpace:
    def time_A(self): A.columnspace()
    def time_B(self): B.columnspace()
    def time_C(self): C.columnspace()
    def time_D(self): D.columnspace()

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): [simplify(e) for e in A.columnspace()]
        def time_B_simplify(self): [simplify(e) for e in B.columnspace()]
        def time_C_simplify(self): [simplify(e) for e in C.columnspace()]
        def time_D_simplify(self): [simplify(e) for e in D.columnspace()]

class TimeDiagonalize:
    def time_A(self): AD.diagonalize()
    def time_B(self): BD.diagonalize()
    def time_C(self): CD.diagonalize()
    def time_D(self): DD.diagonalize()

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): [simplify(e) for e in AD.diagonalize()]
        def time_B_simplify(self): [simplify(e) for e in BD.diagonalize()]
        def time_C_simplify(self): [simplify(e) for e in CD.diagonalize()]
        def time_D_simplify(self): [simplify(e) for e in DD.diagonalize()]

class TimeJordanForm:
    def time_A(self): AE.jordan_form()
    def time_B(self): BE.jordan_form()
    def time_C(self): CE.jordan_form()
    def time_D(self): DE.jordan_form()

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): [simplify(e) for e in AE.jordan_form()]
        def time_B_simplify(self): [simplify(e) for e in BE.jordan_form()]
        def time_C_simplify(self): [simplify(e) for e in CE.jordan_form()]
        def time_D_simplify(self): [simplify(e) for e in DE.jordan_form()]

class TimeSingularValues:
    def time_A(self): AE.singular_values()
    def time_B(self): BE.singular_values()
    def time_C(self): CE.singular_values()
    def time_D(self): DE.singular_values()

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): [simplify(e) for e in AE.singular_values()]
        def time_B_simplify(self): [simplify(e) for e in BE.singular_values()]
        def time_C_simplify(self): [simplify(e) for e in CE.singular_values()]
        def time_D_simplify(self): [simplify(e) for e in DE.singular_values()]

class TimeGaussJordanSolve:
    def time_A(self): AD.gauss_jordan_solve(O4)
    def time_B(self): BD.gauss_jordan_solve(O4)
    def time_C(self): CD.gauss_jordan_solve(O4)
    def time_D(self): DD.gauss_jordan_solve(O4)

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): [simplify(e) for e in AD.gauss_jordan_solve(O4)]
        def time_B_simplify(self): [simplify(e) for e in BD.gauss_jordan_solve(O4)]
        def time_C_simplify(self): [simplify(e) for e in CD.gauss_jordan_solve(O4)]
        def time_D_simplify(self): [simplify(e) for e in DD.gauss_jordan_solve(O4)]

class TimeCholeskySolve:
    def time_A(self): AD.cholesky_solve(O4)
    def time_B(self): BD.cholesky_solve(O4)
    def time_C(self): CD.cholesky_solve(O4)
    def time_D(self): DD.cholesky_solve(O4)

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): simplify(AD.cholesky_solve(O4))
        def time_B_simplify(self): simplify(BD.cholesky_solve(O4))
        def time_C_simplify(self): simplify(CD.cholesky_solve(O4))
        def time_D_simplify(self): simplify(DD.cholesky_solve(O4))

class TimeLDLsolve:
    def time_A(self): AD.LDLsolve(O4)
    def time_B(self): BD.LDLsolve(O4)
    def time_C(self): CD.LDLsolve(O4)
    def time_D(self): DD.LDLsolve(O4)

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): simplify(AD.LDLsolve(O4))
        def time_B_simplify(self): simplify(BD.LDLsolve(O4))
        def time_C_simplify(self): simplify(CD.LDLsolve(O4))
        def time_D_simplify(self): simplify(DD.LDLsolve(O4))

class TimeLUsolve:
    def time_A(self): AD.LUsolve(O4)
    def time_B(self): BD.LUsolve(O4)
    def time_C(self): CD.LUsolve(O4)
    def time_D(self): DD.LUsolve(O4)

    if _TEST_SIMPLIFY:
        def time_A_simplify(self): simplify(AD.LUsolve(O4))
        def time_B_simplify(self): simplify(BD.LUsolve(O4))
        def time_C_simplify(self): simplify(CD.LUsolve(O4))
        def time_D_simplify(self): simplify(DD.LUsolve(O4))

class TimeRank:
    def time_A(self): A.rank()
    def time_B(self): B.rank()
    def time_C(self): C.rank()
    def time_D(self): D.rank()

class TimeIsNilpotent:
    def time_A(self): A.is_nilpotent()
    def time_B(self): B.is_nilpotent()
    def time_C(self): C.is_nilpotent()
    def time_D(self): D.is_nilpotent()

class TimeIsDiagonalizable:
    def time_A(self): AE.is_diagonalizable()
    def time_B(self): BE.is_diagonalizable()
    def time_C(self): CE.is_diagonalizable()
    def time_D(self): DE.is_diagonalizable()

class TimeConditionNumber:
    def time_A(self): AE[:2,:2].condition_number()
    def time_B(self): BE[:2,:2].condition_number()
    def time_C(self): CE[:2,:2].condition_number()
    def time_D(self): DE[:2,:2].condition_number()

class TimeIsPositiveDefiniteEigen:
    def time_A(self): AE._eval_is_positive_definite(method='eigen')
    def time_B(self): BE._eval_is_positive_definite(method='eigen')
    def time_C(self): CE._eval_is_positive_definite(method='eigen')
    def time_D(self): DE._eval_is_positive_definite(method='eigen')

class TimeIsPositiveDefiniteCH:
    def time_A(self): AE._eval_is_positive_definite(method='CH')
    def time_B(self): BE._eval_is_positive_definite(method='CH')
    def time_C(self): CE._eval_is_positive_definite(method='CH')
    def time_D(self): DE._eval_is_positive_definite(method='CH')

class TimeIsPositiveDefiniteLDL:
    def time_A(self): AE._eval_is_positive_definite(method='LDL')
    def time_B(self): BE._eval_is_positive_definite(method='LDL')
    def time_C(self): CE._eval_is_positive_definite(method='LDL')
    def time_D(self): DE._eval_is_positive_definite(method='LDL')
