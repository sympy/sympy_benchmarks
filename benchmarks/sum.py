# -*- coding: utf-8 -*-
"""
The evalutation of symbolic sum via the doit method got slowed by the introdution of Piecewise. Simple profiling suggest that piecewise_fold is taking up to 97% of the time.
It worked much faster on 0.7.2(3) than on 1.0.
"""
import sympy
from sympy import symbols, Function, Sum, I, Symbol, KroneckerDelta

int12Sigma, int22Sigma, exgg12SU2L, intgg11SU2L, intgg11SU2L, ext12Sigma, ext11Sigma, ext11Sigma, exgg22SU2L, intgg11SU2L, intgg11SU2L, ext22Sigma, ext31Sigma, ext31Sigma, exgg32SU2L, intgg21SU2L, intgg21SU2L, ext32Sigma, ext21Sigma, ext21Sigma, exgg42SU2L, intgg21SU2L, intgg21SU2L, ext42Sigma, ext41Sigma, ext41Sigma, int32ASU2L, int42ASU2L, int52ASU2L,  int62ASU2L, ext12Pi, ext11Pi, ext11Pi, exgg22SU2L, intgg11SU2L, intg11SU2L, ext22Pi, ext41Pi, int12Pi, int22Pi, ext32Pi, int62ASU2L, ext42Pi, exgg12SU2L, exgg32SU2L, intgg21SU2L, ext31Pi, exgg42SU2L, intgg21SU2L, intgg21SU2L, ext42Pi, ext21Pi, ext21Pi = symbols('int12Sigma int22Sigma exgg12SU2L intgg11SU2L intgg11SU2L ext12Sigma ext11Sigma ext11Sigma exgg22SU2L intgg11SU2L intgg11SU2L ext22Sigma ext31Sigma ext31Sigma exgg32SU2L intgg21SU2L intgg21SU2L ext32Sigma ext21Sigma ext21Sigma exgg42SU2L intgg21SU2L intgg21SU2L ext42Sigma ext41Sigma ext41Sigma int32ASU2L int42ASU2L int52ASU2L  int62ASU2L ext12Pi ext11Pi ext11Pi exgg22SU2L intgg11SU2L intg11SU2L ext22Pi ext41Pi int12Pi int22Pi ext32Pi int62ASU2L ext42Pi exgg12SU2L exgg32SU2L intgg21SU2L ext31Pi exgg42SU2L intgg21SU2L intgg21SU2L ext42Pi ext21Pi ext21Pi')



class Ts(Function):
    narg = 4
    is_commutative = True

    @classmethod
    def eval(cls, A, mats, f1, f2):
        if not isinstance(A, Symbol) and not isinstance(f1, Symbol) and not isinstance(f2, Symbol):
            # reconstruct the matrix
            for el in mats[A]:
                if el != ():
                    if (f1 - 1, f2 - 1) == el[0:2]:
                        return el[-1]
            return 0

class TimeSum:

    def setup(self):
        self.expr = Sum(Ts(int32ASU2L, ((), ((0, 1, -I/2), (1, 0, I/2)), ()), ext12Pi, int12Pi)*Ts(int42ASU2L, ((), ((0, 1, -I/2), (1, 0, I/2)), ()), ext22Pi, int22Pi)*Ts(int52ASU2L, ((), ((0, 1, -I/2), (1, 0, I/2)), ()), int12Pi, ext32Pi)*Ts(int62ASU2L, ((), ((0, 1, -I/2), (1, 0, I/2)), ()), int22Pi, ext42Pi)*KroneckerDelta(int32ASU2L, int42ASU2L)*KroneckerDelta(int52ASU2L, int62ASU2L), (int12Pi, 1, 2), (int22Pi, 1, 2), (exgg12SU2L, intgg11SU2L, intgg11SU2L), (ext12Pi, ext11Pi, ext11Pi), (exgg22SU2L, intgg11SU2L, intgg11SU2L), (ext22Pi, ext31Pi, ext31Pi), (exgg32SU2L, intgg21SU2L, intgg21SU2L), (ext32Pi, ext21Pi, ext21Pi), (exgg42SU2L, intgg21SU2L, intgg21SU2L), (ext42Pi, ext41Pi, ext41Pi), (int32ASU2L, 0, 2), (int42ASU2L, 0, 2), (int52ASU2L, 0, 2), (int62ASU2L, 0, 2))

    def time_doit(self):
        self.expr.doit()


if __name__ == '__main__':
    mytime = TimeSum()
    mytime.setup()
    mytime.time_doit()
