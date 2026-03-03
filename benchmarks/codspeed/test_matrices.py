# -*- coding: utf-8 -*-
"""
CodSpeed benchmarks for SymPy matrix operations.

Wraps the ASV benchmarks in benchmarks/matrices.py and benchmarks/solve.py
(PyDy examples) to allow noise-free, Callgrind-instrumented CI measurement.

References
----------
Issue: https://github.com/sympy/sympy/issues/21374
"""

import pytest
from sympy import (
    symbols, Symbol, Matrix,
    MutableDenseMatrix, ImmutableDenseMatrix,
    MutableSparseMatrix, ImmutableSparseMatrix,
    MatrixSymbol, Add, MatAdd, Mul, MatMul, S,
)



@pytest.fixture(scope="module")
def matrix_symbols():
    n = Symbol("n")
    A = MatrixSymbol("A", n, n)
    B = MatrixSymbol("B", n, n)
    return A, B


@pytest.fixture(scope="module")
def concrete_3x3():
    """A 3x3 symbolic matrix for solve/decomposition benchmarks."""
    A = Matrix(3, 3, lambda i, j: Symbol("a{}{}".format(i, j)))
    b = Matrix(3, 1, lambda i, j: Symbol("b{}{}".format(i, j)))
    A_sym = Matrix(3, 3, lambda i, j: Symbol("a{}{}".format(*sorted((i, j)))))
    return A, b, A_sym


@pytest.fixture(scope="module")
def zero_matrices():
    return (
        MutableDenseMatrix.zeros(5, 5),
        ImmutableDenseMatrix.zeros(5, 5),
        MutableSparseMatrix.zeros(5, 5),
        ImmutableSparseMatrix.zeros(5, 5),
    )



@pytest.mark.benchmark
def test_matadd(matrix_symbols, benchmark):
    """Benchmark: building a large MatAdd expression."""
    A, B = matrix_symbols
    args = (A, B, A * B, B * A, A ** 2, B ** 2, A ** -1, B ** -1,
            A * B ** -1, B * A ** -1, A ** -1 * B, B * A ** -1)
    benchmark(lambda: MatAdd(*args))


@pytest.mark.benchmark
def test_matmul(matrix_symbols, benchmark):
    """Benchmark: building a large MatMul expression."""
    A, B = matrix_symbols
    args = (A, B, A * B, B * A, A ** 2, B ** 2, A ** -1, B ** -1,
            A * B ** -1, B * A ** -1, A ** -1 * B, B * A ** -1)
    benchmark(lambda: MatMul(*args))


@pytest.mark.benchmark
def test_matrix_lusolve(concrete_3x3, benchmark):
    """Benchmark: LUsolve on a 3x3 symbolic matrix."""
    A, b, _ = concrete_3x3
    benchmark(lambda: A.LUsolve(b))


@pytest.mark.benchmark
def test_matrix_cholesky_solve(concrete_3x3, benchmark):
    """Benchmark: cholesky_solve on a symmetric 3x3 matrix."""
    _, b, A_sym = concrete_3x3
    benchmark(lambda: A_sym.cholesky_solve(b))


@pytest.mark.benchmark
def test_matrix_det_bareiss(benchmark):
    """Benchmark: determinant via Bareiss algorithm on a 4x4 numeric matrix."""
    M = Matrix([[3, 8, 10, 5],
                [10, 9, 3, 7],
                [5, 9, 9, 0],
                [1, 8, 0, 7]])
    benchmark(lambda: M.det(method="bareiss"))


@pytest.mark.benchmark
def test_matrix_det_berkowitz(benchmark):
    """Benchmark: determinant via Berkowitz algorithm on a 4x4 numeric matrix."""
    M = Matrix([[3, 8, 10, 5],
                [10, 9, 3, 7],
                [5, 9, 9, 0],
                [1, 8, 0, 7]])
    benchmark(lambda: M.det(method="berkowitz"))


@pytest.mark.benchmark
def test_matrix_rref(benchmark):
    """Benchmark: rref on a 4x4 numeric matrix."""
    M = Matrix([[3, 8, 10, 5],
                [10, 9, 3, 7],
                [5, 9, 9, 0],
                [1, 8, 0, 7]])
    benchmark(lambda: M.rref())



@pytest.mark.benchmark
def test_mutable_dense_getitem(zero_matrices, benchmark):
    """Benchmark: element access on MutableDenseMatrix."""
    M = zero_matrices[0]
    def run():
        for i in range(M.rows):
            for j in range(M.cols):
                M[i, j]
    benchmark(run)


@pytest.mark.benchmark
def test_sparse_getitem(zero_matrices, benchmark):
    """Benchmark: element access on MutableSparseMatrix."""
    M = zero_matrices[2]
    def run():
        for i in range(M.rows):
            for j in range(M.cols):
                M[i, j]
    benchmark(run)



@pytest.mark.benchmark
def test_diagonal_eigenvals(benchmark):
    """Benchmark: eigenvals on a diagonal-like 5x5 matrix (ASV TimeDiagonalEigenvals)."""
    M = Matrix([
        [0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 2, 0, 0],
        [0, 1, 2, 3, 0],
        [0, 1, 2, 3, 4],
    ])
    benchmark(lambda: M.eigenvals())
