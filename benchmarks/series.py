from sympy import symbols,oo, limit, sin, cos, exp, log, series,sqrt
from sympy.core.cache import clear_cache
x = symbols('x')

# --- Limit benchmarks (warm cache) ---
class TimeLimitWarmCache:

    def time_limit_1_over_x(self):
        limit(1/x, x, oo)

    def time_limit_sin_x_over_x(self):
        limit(sin(x)/x, x, 0)

    def time_limit_exp(self):
        limit((1 + 1/x)**x, x, oo)

    def time_limit_log(self):
        limit(log(x + 1)/log(x), x, oo)


# --- Limit benchmarks (cold cache) ---
class TimeLimitColdCache:
    #Same limits but with cache cleared before each run.
    #Shows realistic first-call performance users experience.

    def setup(self):
        clear_cache()

    def time_limit_1_over_x(self):
        clear_cache()
        limit(1/x, x, oo)

    def time_limit_sin_x_over_x(self):
        clear_cache()
        limit(sin(x)/x, x, 0)

    def time_limit_exp(self):
        clear_cache()
        limit((1 + 1/x)**x, x, oo)

    def time_limit_log(self):
        clear_cache()
        limit(log(x + 1)/log(x), x, oo)


#Series expansion benchmarks
class TimeSeriesExpansion:
    #Series expansion benchmarks parameterized by order.

    params = [5, 10, 20]
    param_names = ['order']

    def time_series_sin(self, order):
        series(sin(x), x, 0, order)

    def time_series_cos(self, order):
        series(cos(x), x, 0, order)

    def time_series_exp(self, order):
        series(exp(x), x, 0, order)

    def time_series_log_1_plus_x(self, order):
        series(log(1 + x), x, 0, order)

    def time_series_sqrt_1_plus_x(self, order):
        series(sqrt(1 + x), x, 0, order)


#Composite expression benchmarks
class TimeSeriesComposite:
    #Series of composed expressions.

    def time_series_sin_exp(self):
        series(sin(exp(x)), x, 0, 10)

    def time_series_exp_sin(self):
        series(exp(sin(x)), x, 0, 10)

    def time_series_log_cos(self):
        series(log(cos(x)), x, 0, 10)
