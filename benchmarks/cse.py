"""Benchmarks for SymPy's common subexpression elimination (CSE)."""

from functools import reduce
from operator import add

from sympy import cse, exp, sin, symbols, Matrix


def _get_args_exprs(nexprs, nterms):
    """Construct expressions with a number of symbols based on chained additions
    and subtractions.

    Examples
    ========

    >>> _get_args_exprs(1, 1)
    ((x0,), [x0])
    >>> _get_args_exprs(1, 3)
    ((x0, x1, x2), [x0 - x1 + x2])
    >>> _get_args_exprs(3, 1)
    ((x0,), [x0, -x0, x0])
    >>> _get_args_exprs(3, 3)
    ((x0, x1, x2), [x0 - x1 + x2, -x0 + x1 - x2, x0 - x1 + x2])

    """
    x = symbols('x:%d' % nterms)
    exprs = [
        reduce(add, [x[j]*(-1)**(i+j) for j in range(nterms)]) for i in range(nexprs)
    ]
    return x, exprs


class TimeCSE:

    params = (((2, 8), (3, 8), (4, 8), (2, 9), (2, 10), (2, 11), ), )

    def setup(self, nexprs_nterms):
        self.args, self.exprs = _get_args_exprs(*nexprs_nterms)

    def time_cse(self, nexprs_nterms):
        cse(self.exprs)
