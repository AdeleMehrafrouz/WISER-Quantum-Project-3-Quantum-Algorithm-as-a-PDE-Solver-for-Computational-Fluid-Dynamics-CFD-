# metrics/error_analysis.py
import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import numpy as np
from src.burgers_hse_solver import run_simulation
from src.utils import l2_error


def classical_solution(N, T, dt):
    # Simple upwind finite difference method for 1D Burgers' Equation
    x = np.linspace(0, 1, N)
    u = np.where(x < 0.5, 1.0, 0.0)
    dx = 1.0 / N
    nu = 0.01

    for _ in range(T):
        u_new = u.copy()
        for i in range(1, N - 1):
            convection = u[i] * (u[i] - u[i - 1]) / dx
            diffusion = nu * (u[i + 1] - 2 * u[i] + u[i - 1]) / dx**2
            u_new[i] = u[i] - dt * convection + dt * diffusion
        u = u_new
    return x, u

def compare_methods(N=16, T=3, dt=0.01):
    start = time.time()
    x_q, u_q = run_simulation(N, T, dt)
    t_q = time.time() - start

    start = time.time()
    x_c, u_c = classical_solution(N, T, dt)
    t_c = time.time() - start

    error = l2_error(u_q, u_c)

    print("Quantum HSE Runtime:", t_q, "sec")
    print("Classical Runtime   :", t_c, "sec")
    print("L2 Error (quantum vs classical):", error)

    return error, t_q, t_c

if __name__ == "__main__":
    compare_methods()
