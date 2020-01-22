import os

from sympy.logic.utilities import load_file
from sympy.logic import satisfiable

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
