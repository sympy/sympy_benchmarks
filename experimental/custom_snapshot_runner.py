import time
import matplotlib.pyplot as plt
import numpy as np
from sympy import Symbol, Poly
from sympy.core.cache import clear_cache

def time_sympy_poly(N, if_cold_cache):
    if if_cold_cache:
        clear_cache()
    x = Symbol('x')
    p1 = Poly((x + 1)**N)
    p2 = Poly((x - 1)**N)
    
    start_time = time.perf_counter()
    p1 * p2
    return time.perf_counter() - start_time

def time_numpy_poly(N):
    p1 = np.poly1d([1, 1])**N
    p2 = np.poly1d([1, -1])**N
    
    start_time = time.perf_counter()
    np.polymul(p1, p2)
    return time.perf_counter()-start_time

def main(): 
    sympy_cold_times = []
    sympy_hot_times = []
    numpy_times = []

    print("Running custom benchmark")
    for N in range(10, 210, 10):
        print(f"Testing degree N={N}")
        sympy_cold_times.append(time_sympy_poly(N, True))
        numpy_times.append(time_numpy_poly(N))
        sympy_hot_times.append(time_sympy_poly(N, False))
        #suffle the order of tests to avoid bias from caching effects

    plt.figure(figsize=(10, 6))
    plt.plot(range(10, 210, 10), sympy_cold_times, marker='o', label='SymPy Poly (Cold Cache)', color='red', linewidth=2)
    plt.plot(range(10, 210, 10), sympy_hot_times, marker='s', label='SymPy Poly (Hot Cache)', color='orange', linestyle='--')
    plt.plot(range(10, 210, 10), numpy_times, marker='^', label='NumPy polymul', color='blue')
    
    plt.title('Asymptotic Performance: Polynomial Multiplication\n(SymPy vs NumPy)')
    plt.xlabel('Polynomial Degree(N)')
    plt.ylabel('Execution Time(seconds)')
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.yscale('log')
    
    image_name = 'asymptotic_plot_poc.png'
    plt.savefig(image_name, dpi=300)
    print(f"Asymptotic performance plot was saved to {image_name}")

if __name__ == "__main__":
    main()