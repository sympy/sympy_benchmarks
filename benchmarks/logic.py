import os

from sympy import symbols
from sympy.logic.utilities import load_file
from sympy.logic import satisfiable, SOPform

input_path = os.path.dirname(__file__)


class LogicSuite:
    """
    Benchmark suite for sympy.logic
    """
    def setup(self):
        self.INPUT = [5*i for i in range(2, 16)]
        self.theories = []
        for test in self.INPUT:
            file_name = os.path.join(input_path, 'logic-inputs', '%s.cnf' % test)
            theory = load_file(file_name)
            self.theories.append(theory)

        self.minterms =  [0, 2, 3, 4, 7, 9, 10, 15, 16, 17, 18, 21, 24, 26, 46, 47, 49, 51, 56, 60, 61, 63]
        self.dontcares = [27, 29, 32, 33, 34, 40, 41, 44]
        self.symbols = symbols('a b c d e f')

    def time_load_file(self):
        file_name = os.path.join(input_path, 'logic-inputs', '10.cnf')
        load_file(file_name)

    def time_dpll(self):
        for theory in self.theories:
            if not satisfiable(theory, algorithm='dpll'):
                raise ValueError("Function returned false")

    def time_dpll2(self):
        for theory in self.theories:
            if not satisfiable(theory, algorithm='dpll2'):
                raise ValueError("Function returned false")


class BoolalgSuite:
    def setup(self):
        self.minterms =  [0, 2, 3, 4, 8, 9, 10, 15, 16, 17, 18, 21, 24, 26, 47, 48, 49, 50, 56, 60, 61, 62]
        self.dontcares = [32, 33, 34, 35, 36, 40, 41, 42]
        self.variables = symbols('a b c d e f')
        (a, b, c, d, e, f) = self.variables
        self.ref = ((~a & ~d & ~f) | (~c & ~d & ~f) | (~d & ~e & ~f) |
                    (a & b & c & d & ~e) | (a & b & c & d & ~f) |
                    (c & d & e & f & ~b) | (b & ~c & ~d & ~e) |
                    (c & ~b & ~d & ~e) | (e & ~b & ~c & ~d) |
                    (~b & ~c & ~e & ~f) | (b & f & ~a & ~c & ~e))

    def teardown(self):
        if not self.result.equals(self.ref):
            raise ValueError("Incorrect result, invalid timing:"
                             " %s != %s" % (self.result, self.ref))

    def time_sopform(self):
        self.result =  SOPform(self.variables, self.minterms, self.dontcares)


