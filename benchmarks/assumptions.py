from inspect import signature

from sympy import Q, symbols
from sympy.assumptions.satask import satask


class SataskSuite:
    params = (
        ['propagate_true', 'propagate_false', 'search_true', 'search_false', 'unknown'],
        [False, True],
    )
    param_names = ['case', 'early_return']

    def setup(self, case, early_return):
        if 'early_return' not in signature(satask).parameters:
            raise NotImplementedError

        x, y = symbols('x y')
        positive_x = Q.positive(x)
        positive_y = Q.positive(y)
        assumptions = {
            'propagate_true': positive_x,
            'propagate_false': ~positive_x,
            # Resolving the two clauses requires search when neither literal is fixed.
            'search_true': (positive_x | positive_y) & (positive_x | ~positive_y),
            'search_false': (~positive_x | positive_y) & (~positive_x | ~positive_y),
            'unknown': positive_x | positive_y,
        }
        self.proposition = positive_x
        self.assumptions = assumptions[case]

    def time_satask(self, case, early_return):
        satask(self.proposition, self.assumptions, early_return=early_return)

    def peakmem_satask(self, case, early_return):
        satask(self.proposition, self.assumptions, early_return=early_return)
