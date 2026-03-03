# -*- coding: utf-8 -*-
"""
CodSpeed benchmarks for SymPy core operations.

These are pytest-codspeed compatible benchmarks that mirror the ASV benchmarks
in benchmarks/core/. They are instrmented via Valgrind/Callgrind so results
are deterministic and suitable for CI regression detection.

References
----------
Issue: https://github.com/sympy/sympy/issues/21374
CodSpeed docs: https://docs.codspeed.io/
"""

import pytest
from sympy import sin
from sympy.core import Add, Mul, Pow, S, Symbol, symbols, I



@pytest.fixture(scope="module")
def core_symbols():
    x, y, z = symbols("x,y,z")
    a5000 = symbols("a0:5000")
    sum_a5000 = Add(*a5000)
    return x, y, z, a5000, sum_a5000


@pytest.fixture(scope="module")
def assumption_symbols():
    ncx = Symbol("x", commutative=False)
    ncy = Symbol("y", commutative=False)
    k_i = Symbol("k", integer=True)
    x_f = Symbol("x", extended_real=True, finite=False)
    return ncx, ncy, k_i, x_f



@pytest.mark.benchmark
def test_neg(core_symbols):
    """Benchmark: negation of a symbol."""
    x, *_ = core_symbols
    -x


@pytest.mark.benchmark
def test_add_x_1(core_symbols):
    """Benchmark: symbol + integer."""
    x, *_ = core_symbols
    x + 1


@pytest.mark.benchmark
def test_add_xy(core_symbols):
    """Benchmark: two-symbol addition."""
    x, y, *_ = core_symbols
    x + y


@pytest.mark.benchmark
def test_add_thousands(core_symbols, benchmark):
    """Benchmark: adding to a sum of 5000 symbols (PR #27254 regression test)."""
    x, y, z, a5000, sum_a5000 = core_symbols
    benchmark(lambda: sum_a5000 + a5000[0])


@pytest.mark.benchmark
def test_mul_xy(core_symbols):
    """Benchmark: two-symbol multiplication."""
    x, y, *_ = core_symbols
    x * y


@pytest.mark.benchmark
def test_div_xy(core_symbols):
    """Benchmark: symbolic division."""
    x, y, *_ = core_symbols
    x / y


@pytest.mark.benchmark
def test_pow_2(core_symbols, benchmark):
    """Benchmark: Pow(x, 2)."""
    x, *_ = core_symbols
    benchmark(lambda: Pow(x, 2))


@pytest.mark.benchmark
def test_pow_100(core_symbols, benchmark):
    """Benchmark: Pow(x, 100)."""
    x, *_ = core_symbols
    benchmark(lambda: Pow(x, 100))


@pytest.mark.benchmark
def test_pow_im(core_symbols, benchmark):
    """Benchmark: imaginary power expression."""
    x, *_ = core_symbols
    benchmark(lambda: (2 * x * I) ** (7 / 3))



@pytest.mark.benchmark
def test_is_integer(assumption_symbols, benchmark):
    """Benchmark: .is_integer checks on Add and Mul expressions."""
    _, _, k_i, _ = assumption_symbols
    def run():
        (k_i + 1).is_integer
        (2 * k_i).is_integer
        (k_i / 3).is_integer
    benchmark(run)


@pytest.mark.benchmark
def test_is_finite(assumption_symbols, benchmark):
    """Benchmark: .is_finite propagation through sin and Mul."""
    _, _, _, x_f = assumption_symbols
    def run():
        sin(x_f).is_finite
        (x_f * sin(x_f)).is_finite
        (sin(x_f) - 67).is_finite
    benchmark(run)


@pytest.mark.benchmark
def test_ncmul_commutative(assumption_symbols, benchmark):
    """Benchmark: non-commutative symbol multiplication comparison."""
    ncx, ncy, *_ = assumption_symbols
    def run():
        ncx * ncy != ncy * ncx
        ncx * ncy * 3 == 3 * ncx * ncy
    benchmark(run)
