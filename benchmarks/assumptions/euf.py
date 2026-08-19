import glob
import os
import random
import re
import signal
import time
from functools import cache
from inspect import signature

from sympy import Symbol, Function, Q
from sympy.core.relational import Eq, Ne
from sympy.logic.algorithms.dpll2 import dpll_satisfiable
from sympy.logic.boolalg import And, Not, Or


@cache
def euf_kwargs():
    if 'theory_solvers' in signature(dpll_satisfiable).parameters:
        from sympy.logic.algorithms.euf_theory_solver import EUFTheorySolver
        return {'theory_solvers': [EUFTheorySolver]}
    return {'use_euf_theory': True}


def merge(cc, lhs, rhs):
    return (getattr(cc, 'merge', None) or cc.add_equality)(lhs, rhs)


def are_congruent(cc, lhs, rhs):
    return (getattr(cc, 'are_congruent', None) or cc.are_equal)(lhs, rhs)


def random_formula(n_consts, n_atoms, n_clauses, clause_len, depth, seed):
    rng = random.Random(seed)
    consts = [Symbol('x%d' % i) for i in range(n_consts)]
    f, g = Function('f'), Function('g')

    def term():
        t = rng.choice(consts)
        for _ in range(rng.randint(0, depth)):
            t = f(t) if rng.random() < 0.7 else g(t, rng.choice(consts))
        return t

    atoms = []
    while len(atoms) < n_atoms:
        lhs, rhs = term(), term()
        if lhs != rhs:
            atoms.append(Eq(lhs, rhs))
    clauses = []
    for _ in range(n_clauses):
        lits = [a if rng.random() < 0.5 else Not(a)
                for a in rng.sample(atoms, min(clause_len, n_atoms))]
        if len(lits) > 2 and rng.random() < 0.25:
            lits[:2] = [And(lits[0], lits[1])]
        clauses.append(Or(*lits))
    return And(*clauses)


def congruence_conflict(n):
    f = Function('f')
    xs = [Symbol('x%d' % i) for i in range(n)]
    return And(*[Eq(xs[i], xs[i + 1]) for i in range(n - 1)],
               Ne(f(xs[0]), f(xs[-1])))


def disjunctive_merge(n):
    f = Function('f')
    a, b = Symbol('a'), Symbol('b')
    xs = [Symbol('x%d' % i) for i in range(n)]
    return And(Ne(a, b),
               *[Or(Eq(x, a), Eq(x, b)) for x in xs],
               Ne(f(xs[0]), f(xs[-1])))


def pigeonhole(n_terms, n_values):
    xs = [Symbol('x%d' % i) for i in range(n_terms)]
    vs = [Symbol('v%d' % i) for i in range(n_values)]
    return And(*[Or(*[Eq(x, v) for v in vs]) for x in xs],
               *[Ne(vs[i], vs[j])
                 for i in range(n_values) for j in range(i + 1, n_values)],
               *[Ne(xs[i], xs[j])
                 for i in range(n_terms) for j in range(i + 1, n_terms)])


class Ask:

    params = ['small', 'medium', 'large']
    param_names = ['size']
    sizes = {'small': 50, 'medium': 200, 'large': 600}

    def setup(self, size):
        from sympy.assumptions.euf_ask import euf_ask
        self.euf_ask = euf_ask
        f = Function('f')
        y = Symbol('y')
        xs = [Symbol('x%d' % i) for i in range(self.sizes[size])]
        self.chain = And(*[Q.eq(xs[i], xs[i + 1])
                           for i in range(len(xs) - 1)])
        self.transitive = Q.eq(xs[0], xs[-1])
        self.congruence = Q.eq(f(xs[0]), f(xs[-1]))
        self.predicate = Q.positive(xs[-1])
        self.chain_positive = Q.positive(xs[0]) & self.chain
        self.disequality = Q.ne(xs[0], y)
        self.chain_distinct = self.chain & Q.ne(xs[-1], y)

    def time_transitive(self, size):
        self.euf_ask(self.transitive, self.chain)

    def time_congruence(self, size):
        self.euf_ask(self.congruence, self.chain)

    def time_predicate_propagation(self, size):
        self.euf_ask(self.predicate, self.chain_positive)

    def time_disequality(self, size):
        self.euf_ask(self.disequality, self.chain_distinct)


class Solving:

    params = ['small', 'medium', 'large']
    param_names = ['size']
    chain = {'small': 200, 'medium': 600, 'large': 1500}
    merge = {'small': 8, 'medium': 12, 'large': 14}
    holes = {'small': (5, 4), 'medium': (6, 5), 'large': (7, 6)}
    randoms = {
        'small': (8, 15, 13, 3, 2),
        'medium': (12, 25, 22, 3, 3),
        'large': (16, 40, 35, 4, 3),
    }
    seeds = range(3)

    def setup(self, size):
        self.conflict = congruence_conflict(self.chain[size])
        self.merge_formula = disjunctive_merge(self.merge[size])
        self.pigeonhole = pigeonhole(*self.holes[size])
        self.formulas = [random_formula(*self.randoms[size], seed=n)
                         for n in self.seeds]

    def time_congruence_conflict(self, size):
        dpll_satisfiable(self.conflict, **euf_kwargs())

    def time_disjunctive_merge(self, size):
        dpll_satisfiable(self.merge_formula, **euf_kwargs())

    def time_pigeonhole(self, size):
        dpll_satisfiable(self.pigeonhole, **euf_kwargs())

    def time_random(self, size):
        for f in self.formulas:
            dpll_satisfiable(f, **euf_kwargs())


STATUS = re.compile(r':status\s+(sat|unsat)')


def _timeout(signum, frame):
    raise TimeoutError


def suite_files():
    directory = os.environ.get(
        'QF_UF_DIR', os.path.expanduser('~/Downloads/non-incremental/QF_UF'))
    if not os.path.isdir(directory):
        raise NotImplementedError('%s does not exist' % directory)
    paths = sorted(glob.glob(os.path.join(directory, '**', '*.smt2'),
                             recursive=True))
    limit = int(os.environ.get('QF_UF_LIMIT', 100))
    max_bytes = int(os.environ.get('QF_UF_MAX_BYTES', 100000))
    paths = [p for p in paths if os.path.getsize(p) <= max_bytes]
    return paths[::max(1, len(paths) // limit)][:limit]


def suite_formula(source):
    from sympy.assumptions.assume import AppliedPredicate
    from sympy.parsing.smtlib import parse_smtlib
    _, assertions = parse_smtlib(source)
    return And(*[a for a in assertions if not isinstance(a, AppliedPredicate)])


def file_outcome(path, seconds):
    source = open(path).read()
    status = STATUS.search(source)
    if not status:
        return 'unknown', 0.0
    expected = status.group(1) == 'sat'
    signal.alarm(seconds)
    start = time.perf_counter()
    try:
        answer = bool(dpll_satisfiable(suite_formula(source), **euf_kwargs()))
        result = 'ok' if answer is expected else 'wrong'
    except TimeoutError:
        result = 'timeout'
    except Exception:
        result = 'error'
    finally:
        signal.alarm(0)
    return result, time.perf_counter() - start


class Suite:

    timeout = 3600

    def setup(self):
        signal.signal(signal.SIGALRM, _timeout)
        seconds = int(os.environ.get('QF_UF_TIMEOUT', 10))
        self.results = [file_outcome(p, seconds) for p in suite_files()]

    def track_files(self):
        return len(self.results)

    def track_accepted(self):
        return sum(o in ('ok', 'wrong') for o, _ in self.results)

    def track_correct(self):
        return sum(o == 'ok' for o, _ in self.results)

    def track_timeout(self):
        return sum(o == 'timeout' for o, _ in self.results)

    def track_accepted_time(self):
        return sum(t for o, t in self.results if o in ('ok', 'wrong'))

    track_files.unit = 'files'
    track_accepted.unit = 'files'
    track_correct.unit = 'files'
    track_timeout.unit = 'files'
    track_accepted_time.unit = 'seconds'


class CC:

    params = ['small', 'medium', 'large']
    param_names = ['size']
    sizes = {'small': 500, 'medium': 2000, 'large': 5000}

    def setup(self, size):
        from sympy.logic.algorithms.euf_theory import EUFCongruenceClosure
        self.EUFCongruenceClosure = EUFCongruenceClosure
        self.f = Function('f')
        self.syms = [Symbol('x%d' % i) for i in range(self.sizes[size])]
        self.eqs = [Q.eq(self.syms[i], self.syms[i + 1])
                    for i in range(len(self.syms) - 1)]

    def time_build(self, size):
        self.EUFCongruenceClosure(self.eqs)

    def time_congruence_query(self, size):
        cc = self.EUFCongruenceClosure(self.eqs)
        cc._flatten(self.f(self.syms[0]))
        cc._flatten(self.f(self.syms[-1]))
        are_congruent(cc, self.f(self.syms[0]), self.f(self.syms[-1]))

    def time_incremental_merges(self, size):
        cc = self.EUFCongruenceClosure([])
        for s in self.syms:
            cc._flatten(self.f(s))
        for i in range(len(self.syms) - 1):
            merge(cc, self.syms[i], self.syms[i + 1])
