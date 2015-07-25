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
        self.INPUT = [5 * i for i in range(2, 16)]
        self.ALGORITHMS = ['dpll', 'dpll2']

    def time_logic():
        for test in self.INPUT:
            for alg in self.ALGORITHMS:
                file_name = os.path.join(input_path, 'logic-inputs', '%s.cnf' % test)
                theory = load_file(file_name)
                if not satisfiable(theory, algorithm=alg):
                    raise ValueError("Function returned false")
