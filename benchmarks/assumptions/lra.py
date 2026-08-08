import random

from sympy import Symbol, Q
from sympy.assumptions.cnf import CNF, EncodedCNF
from sympy.assumptions.lra_satask import lra_satask
from sympy.core.add import Add
from sympy.core.relational import Eq
from sympy.logic.algorithms.dpll2 import dpll_satisfiable
from sympy.logic.algorithms.lra_theory import LRASolver
from sympy.logic.boolalg import And, Or, Not

RELATIONS = [lambda a, b: a <= b, lambda a, b: a < b,
             lambda a, b: a >= b, lambda a, b: a > b]


def random_formula(n_vars, n_atoms, n_clauses, clause_len, terms, seed):
    rng = random.Random(seed)
    xs = [Symbol('x%d' % i, real=True) for i in range(n_vars)]
    atoms = []
    for _ in range(n_atoms):
        chosen = rng.sample(xs, min(terms, n_vars))
        lhs = Add(*[(rng.randint(-9, 9) or 1)*v for v in chosen])
        rhs = rng.randint(-20, 20)
        if rng.random() < 0.15:
            atoms.append((Eq(lhs, rhs), False))
        else:
            atoms.append((rng.choice(RELATIONS)(lhs, rhs), True))
    clauses = []
    for _ in range(n_clauses):
        lits = [a if not can_negate or rng.random() < 0.5 else Not(a)
                for a, can_negate in rng.sample(atoms,
                                                min(clause_len, n_atoms))]
        if len(lits) > 2 and rng.random() < 0.25:
            lits[:2] = [And(lits[0], lits[1])]
        clauses.append(Or(*lits))
    return And(*clauses)


def scheduling(n_jobs, slack):
    s = [Symbol('s%d' % i, real=True) for i in range(n_jobs)]
    deadline = n_jobs + slack
    cons = [si >= 0 for si in s] + [si + 1 <= deadline for si in s]
    cons += [Or(s[i] + 1 <= s[j], s[j] + 1 <= s[i])
             for i in range(n_jobs) for j in range(i + 1, n_jobs)]
    return And(*cons)


def disjunctive_chain(n):
    xs = [Symbol('x%d' % i, real=True) for i in range(n)]
    cons = [Or(xs[i] - xs[i + 1] >= 1, xs[i + 1] - xs[i] >= 1)
            for i in range(n - 1)]
    cons += [xs[0] >= 0, xs[0] <= 1, xs[-1] >= 0, xs[-1] <= 1]
    return And(*cons)


class CommonQueries:
    """
    Very small queries that sympy could have used internally.
    """
    def setup(self):
        self.x = Symbol('x', real=True)
        self.y = Symbol('y', real=True)

    def time_positive_from_bound(self):
        lra_satask(Q.positive(self.x), Q.gt(self.x, 1))

    def time_transitive_two_vars(self):
        lra_satask(Q.gt(self.x, 0), Q.gt(self.x, self.y) & Q.gt(self.y, 0))

    def time_zero_from_bounds(self):
        lra_satask(Q.zero(self.x), Q.ge(self.x, 0) & Q.le(self.x, 0))

    def time_unknown(self):
        lra_satask(Q.positive(self.x + self.y), Q.positive(self.x))


class RandomAll:

    params = ['small', 'medium', 'large']
    param_names = ['size']
    sizes = {
        'small': (5, 10, 9, 3, 3),
        'medium': (6, 12, 11, 3, 3),
        'large': (8, 15, 13, 3, 3),
    }
    seeds = range(3)

    def setup(self, size):
        self.formulas = [random_formula(*self.sizes[size], seed=s)
                         for s in self.seeds]

    def time_satisfiable(self, size):
        for f in self.formulas:
            dpll_satisfiable(f, use_lra_theory=True)


class Backtracking:

    params = ['small', 'medium', 'large']
    param_names = ['size']
    sat_jobs = {'small': 4, 'medium': 6, 'large': 8}
    unsat_jobs = {'small': 3, 'medium': 4, 'large': 5}
    chain = {'small': 8, 'medium': 16, 'large': 25}

    def setup(self, size):
        self.sat_schedule = scheduling(self.sat_jobs[size], slack=0)
        self.unsat_schedule = scheduling(self.unsat_jobs[size], slack=-1)
        self.chain_formula = disjunctive_chain(self.chain[size])

    def time_scheduling_sat(self, size):
        dpll_satisfiable(self.sat_schedule, use_lra_theory=True)

    def time_scheduling_unsat(self, size):
        dpll_satisfiable(self.unsat_schedule, use_lra_theory=True)

    def time_disjunctive_chain(self, size):
        dpll_satisfiable(self.chain_formula, use_lra_theory=True)


class TheorySolver:
    """
    TheorySolver internal method(s)
    """
    params = ['small', 'medium', 'large']
    param_names = ['size']
    sizes = RandomAll.sizes

    def setup(self, size):
        formula = random_formula(*self.sizes[size], seed=0)
        cnf = CNF.from_prop(formula)
        self.encoded = EncodedCNF()
        self.encoded.from_cnf(cnf)
        self.literals = [next(iter(clause)) for clause in self.encoded.data
                         if clause]

    def time_from_encoded_cnf(self, size):
        LRASolver.from_encoded_cnf(self.encoded)

    def time_assert_and_check(self, size):
        solver, _ = LRASolver.from_encoded_cnf(self.encoded)
        for lit in self.literals:
            solver.assert_lit(lit)
        solver.check()
