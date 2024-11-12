"""
Some baseline benchmarks that don't use SymPy and should never change
"""

class TimeBaseline:
    def time_noop(self):
        pass

    def time_loop10(self):
        for i in range(10):
            pass

    def time_loop10000000(self):
        for i in range(10000000):
            pass

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

class TimeBasicGCD:
    # Testing a basic pure Python function that does not use SymPy.
    def setup(self):
        self.a = 2**20*3**30
        self.b = 2**30*3**20
        self.result = 2**20*3**20

    def time_gcd(self):
        g = gcd(self.a, self.b)
        assert g == self.result
