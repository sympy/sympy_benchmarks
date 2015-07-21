# -*- coding: utf-8 -*-

import os

import sympy as sm


def _load_matrix():

    path = os.path.join(os.path.split(__file__)[0], 'eom.txt')

    with open(path, 'r') as f:
        txt = f.read()

    return sm.sympify(txt)


class TimeLargeExpressionOperations:

    def setup(self):

        t = sm.symbols('t')

        self.funcs = [s(t) for s in sm.symbols('q:6, u:6', cls=sm.Function)]

        self.syms = sm.symbols('x:{}'.format(len(self.funcs)))

        self.subs = dict(zip(self.funcs, self.syms))

        self.func_matrix = _load_matrix()

        self.sym_matrix = self.func_matrix.subs(self.subs)

    def time_subs(self):

        self.func_matrix.subs(self.subs)

    def peakmem_subs(self):

        self.func_matrix.subs(self.subs)

    def time_jacobian_wrt_functions(self):

        self.func_matrix.jacobian(self.funcs)

    def time_manual_jacobian_wrt_functions(self):

        for expr in self.func_matrix:
            for func in self.funcs:
                expr.diff(func)

    def time_jacobian_wrt_symbols(self):

        self.sym_matrix.jacobian(self.syms)

    def peakmem_jacobian_wrt_functions(self):

        self.func_matrix.jacobian(self.funcs)

    def peakmem_jacobian_wrt_symbols(self):

        self.sym_matrix.jacobian(self.syms)
