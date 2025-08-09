#metrics/scaling_study.py
import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import csv
import time
import numpy as np
import matplotlib.pyplot as plt

from src.burgers_hse_solver import run_simulation as run_hse
from src.burgers_qtn_solver import run_qtn_simulation as run_qtn
from metrics.error_analysis import classical_solution
from src.utils import l2_error

os.makedirs("results", exist_ok=True)

def run_scaling_study(grid_sizes=[8, 16, 32, 64], T=3, dt=0.01, output_csv="results/scaling_results.csv"):
    results = []

    for N in grid_sizes:
        print(f"\n=== Running for N = {N} ===")

        # Classical
        start = time.time()
        x_classical, u_classical = classical_solution(N, T, dt)
        t_classical = time.time() - start

        # HSE
        start = time.time()
        x_hse, u_hse = run_hse(N, T, dt)
        t_hse = time.time() - start
        e_hse = l2_error(u_hse, u_classical)

        # QTN
        start = time.time()
        x_qtn, u_qtn = run_qtn(N, T, dt, plot=False)
        t_qtn = time.time() - start
        e_qtn = l2_error(u_qtn, u_classical)

        results.append({
            "N": N,
            "T": T,
            "dt": dt,
            "time_classical": t_classical,
            "time_hse": t_hse,
            "time_qtn": t_qtn,
            "l2_error_hse": e_hse,
            "l2_error_qtn": e_qtn,
        })

    # Save CSV
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\n Scaling study saved to: {output_csv}")
    return results

def plot_scaling(csv_path="results/scaling_results.csv"):
    data = np.genfromtxt(csv_path, delimiter=",", names=True)

    N_vals = data["N"]
    plt.figure()
    plt.plot(N_vals, data["time_classical"], label="Classical", marker="o")
    plt.plot(N_vals, data["time_hse"], label="HSE", marker="o")
    plt.plot(N_vals, data["time_qtn"], label="QTN", marker="o")
    plt.xlabel("Grid Size N")
    plt.ylabel("Runtime (s)")
    plt.title("Runtime Scaling")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/runtime_vs_N.png")
    print("Saved: results/runtime_vs_N.png")

    plt.figure()
    plt.plot(N_vals, data["l2_error_hse"], label="HSE", marker="o")
    plt.plot(N_vals, data["l2_error_qtn"], label="QTN", marker="o")
    plt.xlabel("Grid Size N")
    plt.ylabel("L2 Error")
    plt.title("Error Scaling")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/l2_error_vs_N.png")
    print("Saved: results/l2_error_vs_N.png")

if __name__ == "__main__":
    run_scaling_study()
    plot_scaling()
