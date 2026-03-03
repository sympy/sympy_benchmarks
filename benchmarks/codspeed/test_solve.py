# -*- coding: utf-8 -*-
"""
CodSpeed benchmarks for SymPy solve / linsolve / solveset.

These wrap the existing ASV benchmarks so they can be measured under
CodSpeed's Callgrind instrumentation, giving noise-free results on CI.

References
----------
Issue: https://github.com/sympy/sympy/issues/21374
Issue: https://github.com/sympy/sympy_benchmarks/issues/13  (add solveset benchmarks)
"""

import pytest
import sympy
from sympy import symbols, linsolve, solveset, S, Interval, Eq
from sympy import sin, cos, exp, tan, log



def _mk_poly_eqs(wy=2):
    """Build a polynomial fitting system (scaled-down from ASV benchmarks)."""
    from benchmarks.solve import _mk_eqs
    eqs, p, y = _mk_eqs(wy)
    return eqs, p

@pytest.fixture(scope="module")
def poly_eqs():
    return _mk_poly_eqs(wy=2)


@pytest.mark.benchmark
def test_solve_polynomial_system(poly_eqs, benchmark):
    """Benchmark: sympy.solve on a polynomial fitting system (ASV TimeSolve01)."""
    eqs, p = poly_eqs
    benchmark(lambda: sympy.solve(eqs, *p.c))


@pytest.mark.benchmark
def test_solve_polynomial_system_nocheck(poly_eqs, benchmark):
    """Benchmark: sympy.solve with check=False (ASV TimeSolve01.time_solve_nocheck)."""
    eqs, p = poly_eqs
    benchmark(lambda: sympy.solve(eqs, *p.c, check=False))



@pytest.fixture(scope="module")
def sparse_linear_system():
    """A sparse system: xi + yi = 0, xi - yi + 1 = 0 for i in range(n)."""
    n = 10
    xs = symbols("x:{}".format(n))
    ys = symbols("y:{}".format(n))
    syms = xs + ys
    eqs = []
    for xi, yi in zip(xs, ys):
        eqs.extend([xi + yi, xi - yi + 1])
    return eqs, syms


@pytest.mark.benchmark
def test_linsolve_sparse(sparse_linear_system, benchmark):
    """Benchmark: linsolve on a sparse 20-variable linear system."""
    eqs, syms = sparse_linear_system
    benchmark(lambda: linsolve(eqs, syms))


@pytest.mark.benchmark
def test_solve_sparse(sparse_linear_system, benchmark):
    """Benchmark: solve on the same sparse system (compare vs linsolve)."""
    eqs, syms = sparse_linear_system
    benchmark(lambda: sympy.solve(eqs, syms))



@pytest.fixture(scope="module")
def single_var():
    return symbols("x")


@pytest.mark.benchmark
def test_solveset_linear(single_var, benchmark):
    """Benchmark: solveset for a linear equation over Reals."""
    x = single_var
    eq = 3 * x - 7
    benchmark(lambda: solveset(eq, x, domain=S.Reals))


@pytest.mark.benchmark
def test_solveset_quadratic(single_var, benchmark):
    """Benchmark: solveset for a quadratic equation over Complexes."""
    x = single_var
    eq = x ** 2 - 5 * x + 6
    benchmark(lambda: solveset(eq, x, domain=S.Complexes))


@pytest.mark.benchmark
def test_solveset_cubic(single_var, benchmark):
    """Benchmark: solveset for a cubic polynomial equation."""
    x = single_var
    eq = x ** 3 - 6 * x ** 2 + 11 * x - 6
    benchmark(lambda: solveset(eq, x, domain=S.Complexes))


@pytest.mark.benchmark
def test_solveset_trig_sin(single_var, benchmark):
    """Benchmark: solveset for a trigonometric equation sin(x) = 1/2."""
    x = single_var
    eq = sin(x) - S.Half
    benchmark(lambda: solveset(eq, x, domain=Interval(0, 2 * sympy.pi)))


@pytest.mark.benchmark
def test_solveset_exp(single_var, benchmark):
    """Benchmark: solveset for an exponential equation exp(x) = 5."""
    x = single_var
    eq = exp(x) - 5
    benchmark(lambda: solveset(eq, x, domain=S.Reals))


@pytest.mark.benchmark
def test_solveset_log(single_var, benchmark):
    """Benchmark: solveset for a logarithmic equation log(x) = 2."""
    x = single_var
    eq = log(x) - 2
    benchmark(lambda: solveset(eq, x, domain=S.Reals))


@pytest.mark.benchmark
def test_solveset_vs_solve_quadratic(single_var, benchmark):
    """Benchmark: solve() on the same quadratic (compare with test_solveset_quadratic)."""
    x = single_var
    eq = x ** 2 - 5 * x + 6
    benchmark(lambda: sympy.solve(eq, x))


@pytest.mark.benchmark
def test_solveset_rational(single_var, benchmark):
    """Benchmark: solveset for a rational equation."""
    x = single_var
    eq = (x ** 2 - 1) / (x - 2)
    benchmark(lambda: solveset(eq, x, domain=S.Reals))
