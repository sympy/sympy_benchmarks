# -*- coding: utf-8 -*-
"""
CodSpeed benchmarks for SymPy printing subsystem.

Wraps benchmarks/printing.py for noise-free CI measurement via Callgrind.

References
----------
Issue: https://github.com/sympy/sympy/issues/21374
"""

import pytest
from sympy import Symbol, Matrix, symbols, log, atan2, sin, cos
from sympy import latex, pretty, srepr, ccode, fcode



@pytest.fixture(scope="module")
def matrix_expr_10():
    x = Symbol("x")
    return Matrix(10, 10, lambda i, j: x ** (i + j))


@pytest.fixture(scope="module")
def poly_expr_50():
    x, y = symbols("x y")
    return ((x + y) ** 50).expand()


@pytest.fixture(scope="module")
def nested_log_50():
    x = Symbol("x")
    expr = x
    for _ in range(50):
        expr = log(expr)
    return expr


@pytest.fixture(scope="module")
def nested_atan2_5():
    x = Symbol("x")
    expr = x
    for _ in range(5):
        expr = atan2(expr, expr)
    return expr


@pytest.fixture(scope="module")
def trig_expr():
    x = Symbol("x")
    return sin(x) ** 2 + cos(x) ** 2 - 1



@pytest.mark.benchmark
def test_str_matrix(matrix_expr_10, benchmark):
    """Benchmark: str() on a 10x10 symbolic matrix (ASV TimeMatrixPrinting)."""
    benchmark(lambda: str(matrix_expr_10))


@pytest.mark.benchmark
def test_str_poly(poly_expr_50, benchmark):
    """Benchmark: str() on an expanded (x+y)^50 polynomial."""
    benchmark(lambda: str(poly_expr_50))


@pytest.mark.benchmark
def test_str_nested_log(nested_log_50, benchmark):
    """Benchmark: str() on a 50-deep nested log expression."""
    benchmark(lambda: str(nested_log_50))


@pytest.mark.benchmark
def test_str_nested_atan2(nested_atan2_5, benchmark):
    """Benchmark: str() on a 5-deep nested atan2 expression."""
    benchmark(lambda: str(nested_atan2_5))



@pytest.mark.benchmark
def test_latex_matrix(matrix_expr_10, benchmark):
    """Benchmark: latex() on a 10x10 symbolic matrix."""
    benchmark(lambda: latex(matrix_expr_10))


@pytest.mark.benchmark
def test_latex_poly(poly_expr_50, benchmark):
    """Benchmark: latex() on an expanded (x+y)^50 polynomial."""
    benchmark(lambda: latex(poly_expr_50))


@pytest.mark.benchmark
def test_latex_nested_log(nested_log_50, benchmark):
    """Benchmark: latex() on a 50-deep nested log expression."""
    benchmark(lambda: latex(nested_log_50))



@pytest.mark.benchmark
def test_pretty_poly(poly_expr_50, benchmark):
    """Benchmark: pretty() on an expanded (x+y)^50 polynomial."""
    benchmark(lambda: pretty(poly_expr_50))


@pytest.mark.benchmark
def test_pretty_trig(trig_expr, benchmark):
    """Benchmark: pretty() on a trigonometric expression."""
    benchmark(lambda: pretty(trig_expr))



@pytest.mark.benchmark
def test_ccode_poly(poly_expr_50, benchmark):
    """Benchmark: ccode() C-code printer on an expanded polynomial."""
    benchmark(lambda: ccode(poly_expr_50))


@pytest.mark.benchmark
def test_ccode_trig(trig_expr, benchmark):
    """Benchmark: ccode() on a trigonometric expression."""
    benchmark(lambda: ccode(trig_expr))
