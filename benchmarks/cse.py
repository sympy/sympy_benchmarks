from functools import reduce
from operator import add
import sympy as sp

def _get_args_exprs(nexprs, nterms):
    x = sp.symbols('x:%d' % nterms)
    exprs = [
        reduce(add, [x[j]*(-1)**(i+j) for j in range(nterms)]) for i in range(nexprs)
    ]
    return x, exprs


class TimeCSE:

    params = ((
        (2, 8), (3, 8), (4, 8),
        (2, 9), (2, 10), (2, 11)
    ),)

    def setup(self, nexprs_nterms):
        self.args, self.exprs = _get_args_exprs(*nexprs_nterms)

    def time_cse(self, nexprs_nterms):
        sp.cse(self.exprs)
