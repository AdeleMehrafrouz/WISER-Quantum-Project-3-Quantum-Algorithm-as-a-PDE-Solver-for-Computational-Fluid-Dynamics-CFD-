#metrics/compare_all.py
import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import numpy as np
import matplotlib.pyplot as plt

from src.burgers_hse_solver import run_simulation as run_hse
from src.burgers_qtn_solver import run_qtn_simulation as run_qtn
from metrics.error_analysis import classical_solution
from src.utils import l2_error

# Ensure results directory exists
os.makedirs("results", exist_ok=True)

def compare_all(N=16, T=3, dt=0.01):
    print(f"\n=== Comparing all solvers for N = {N}, T = {T}, dt = {dt} ===")

    # Classical Solver
    start = time.time()
    x_classical, u_classical = classical_solution(N, T, dt)
    t_classical = time.time() - start

    # HSE Solver
    start = time.time()
    x_hse, u_hse = run_hse(N, T, dt)
    t_hse = time.time() - start

    # QTN Solver (MPS-based)
    start = time.time()
    x_qtn, u_qtn = run_qtn(N, T, dt, plot=False)
    t_qtn = time.time() - start

    # Errors
    err_hse = l2_error(u_hse, u_classical)
    err_qtn = l2_error(u_qtn, u_classical)

    # Print Summary
    print(f"[Classical]    Time: {t_classical:.4f} s")
    print(f"[HSE]          Time: {t_hse:.4f} s | L2 error: {err_hse:.6f}")
    print(f"[QTN (MPS)]    Time: {t_qtn:.4f} s | L2 error: {err_qtn:.6f}")

    # Plot Comparison
    plt.plot(x_classical, u_classical, label="Classical", linestyle="--")
    plt.plot(x_hse, u_hse, label="HSE")
    plt.plot(x_qtn, u_qtn, label="QTN (MPS)")
    plt.xlabel("x")
    plt.ylabel("u(x)")
    plt.title(f"Burgers Equation: N={N}, T={T}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"results/comparison_N{N}.png")
    plt.show()

    return {
        "N": N,
        "T": T,
        "dt": dt,
        "time_classical": t_classical,
        "time_hse": t_hse,
        "time_qtn": t_qtn,
        "l2_error_hse": err_hse,
        "l2_error_qtn": err_qtn
    }

if __name__ == "__main__":
    compare_all(N=16, T=3, dt=0.01)
