import os

from sympy.core.compatibility import range
from sympy.logic.utilities import load_file
from sympy.logic import satisfiable

input_path = os.path.dirname(__file__)


class LogicSuite:
    """
    Benchmark suite for sympy.logic
    """
    def setup(self):
        self.INPUT = [5*i for i in range(2, 16)]

    def time_dpll(self):
        for test in self.INPUT:
            file_name = os.path.join(input_path, 'logic-inputs', '%s.cnf' % test)
            theory = load_file(file_name)
            if not satisfiable(theory, algorithm='dpll'):
                raise ValueError("Function returned false")

    def time_dpll2(self):
        for test in self.INPUT:
            file_name = os.path.join(input_path, 'logic-inputs', '%s.cnf' % test)
            theory = load_file(file_name)
            if not satisfiable(theory, algorithm='dpll2'):
                raise ValueError("Function returned false")
