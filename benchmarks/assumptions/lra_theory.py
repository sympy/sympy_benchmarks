import os
import sys

import random

from sympy.core.symbol import Symbol, symbols
from sympy.core.relational import Eq
from sympy.core.numbers import Rational
from sympy.logic.boolalg import And
from sympy.logic.inference import satisfiable


ASSUMPTION_PROFILES = [
    {},
    {'integer': True},
    {'rational': True},
    {'positive': True},
    {'negative': True},
    {'nonnegative': True},
    {'nonpositive': True},
    {'integer': True, 'positive': True},
    {'integer': True, 'negative': True},
    {'integer': True, 'nonnegative': True},
    {'even': True},
    {'odd': True},
    {'prime': True},
]


def make_variables(num_variables, rng, assumptions=True):
    variables = []
    for i in range(1, num_variables + 1):
        profile = rng.choice(ASSUMPTION_PROFILES)
        if not assumptions:
            profile = {}
        variables.append(Symbol('x%d' % i, **profile))
    return variables


def make_problem(num_variables, num_constraints, terms_per_constraint, seed,
                 assumptions=True):
    rng = random.Random(seed)
    variables = make_variables(num_variables, rng, assumptions)
    constraints = []
    for _ in range(num_constraints):
        chosen = rng.sample(variables, terms_per_constraint)
        lhs = sum(rng.randint(-9, 9) * v for v in chosen)
        rhs = rng.randint(-9, 9)
        op = rng.choice(['<=', '>=', '<', '>'])
        constraints.append({'<=': lhs <= rhs, '>=': lhs >= rhs,
                            '<': lhs < rhs, '>': lhs > rhs}[op])
    return And(*constraints)


class _LRASuiteBase:
    # label -> (num_variables, num_constraints, terms_per_constraint)
    # practically we should aim to maximize the performance of fine
    ASSUMPTIONS = False
    SIZES = {
        'fine' : (2,3,2),
        'small': (4, 5, 3),
        'medium': (20, 40, 5),
        'large': (32, 70, 6),
    }
    params = ['fine', 'small', 'medium', 'large']
    param_names = ['size']

    def setup(self, size):
        num_variables, num_constraints, terms = self.SIZES[size]
        self.formula = make_problem(num_variables, num_constraints, terms,
                                    seed=1, assumptions=self.ASSUMPTIONS)

    def time_satisfiable(self, size):
        satisfiable(self.formula, use_lra_theory=True)


class Suite(_LRASuiteBase):
    ASSUMPTIONS = False


class Suite_ActivatedAssump(_LRASuiteBase):
    ASSUMPTIONS = True


def special_cases():
    # Special kind of formulas that each (should) have special porperties
    # e.g basic bounds, Equalities, Cycles, Rational coeffs etc.
    x = symbols('x1:13')
    return [
        And(x[0] >= 0, x[0] <= 10),
        And(x[0] >= 5, x[0] <= 2),
        And(x[0] + x[1] <= 10, x[0] - x[1] >= 2),
        And(Eq(x[0] + x[1], 10), x[0] >= 0, x[1] >= 0),
        And(x[0] + x[1] + x[2] <= 10, x[0] >= 2, x[1] >= 3, x[2] >= 1,
            x[0] - x[1] <= 4),
        And(x[0] > 5, x[0] < 3),
        And(Eq(x[0] + x[1] + x[2], 100), x[0] >= 40, x[1] >= 30, x[2] >= 10,
            x[0] - x[1] <= 20),
        And(2*x[0] + 3*x[1] <= 12, x[0] + x[1] >= 1, x[0] >= 0, x[1] >= 0,
            Rational(1, 2)*x[0] - x[1] <= 2),
        And(*[x[i] <= x[i + 1] for i in range(len(x) - 1)], x[-1] < x[0]),
        And(x[0] >= 10, x[0] <= 18, x[1] >= x[0] + 4, x[1] <= 30,
            x[2] <= x[1] - 6, x[2] >= 8),
        And(x[0] + x[1] <= 1, x[0] >= 1, x[1] >= 1),
        And(x[0] >= 0, x[0] <= 0, x[0] > 0),
        And(x[0] - x[1] <= 3, x[1] - x[2] <= 3, x[2] - x[0] <= -1,
            x[0] >= 0, x[2] <= 10),
        And(Eq(x[0] + x[1], 5), Eq(x[0] - x[1], 1), x[0] >= 0, x[1] >= 0),
        And(1000*x[0] + x[1] <= 1000, x[0] >= 0, x[1] >= 0,
            x[0] + 1000*x[1] >= 1),
        And(x[0] <= 5, x[0] <= 7, x[0] <= 9, x[0] >= 1, x[0] >= 0),
        And(*[Eq(x[i], x[i + 1] + 1) for i in range(len(x) - 1)],
            x[-1] >= x[0]),
        And(x[0] + x[1] + x[2] + x[3] <= 4, x[0] >= 1, x[1] >= 1,
            x[2] >= 1, x[3] >= 1),
    ]


class SpecialExamples:
    EXAMPLES = special_cases()
    params = list(range(len(EXAMPLES)))
    param_names = ['case']

    def setup(self, case):
        self.formula = self.EXAMPLES[case]

    def Satisfiable(self, case):
        satisfiable(self.formula, use_lra_theory=True)
