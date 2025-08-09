# src/burgers_hse_solver.py
# Quantum-inspired HSE solver for the 1D viscous Burgers’ equation

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm

def burgers_initial_condition(N, shock_position=0.5):
    x = np.linspace(0, 1, N)
    u = np.where(x < shock_position, 1.0, 0.0)
    return x, u

def map_to_wavefunction(u):
    psi = np.sqrt(u + 1e-8)
    norm = np.linalg.norm(psi)
    return psi / norm

def evolve_wavefunction(psi, dt, N, nu=0.01):
    dx = 1.0 / N
    H = np.zeros((N, N), dtype=np.complex128)

    for i in range(1, N - 1):
        H[i, i - 1] = H[i, i + 1] = -1
        H[i, i] = 2

    H *= nu / dx**2
    U = expm(-1j * H * dt)
    return U @ psi

def run_simulation(N=16, T=3, dt=0.01, nu=0.01):
    x, u = burgers_initial_condition(N)
    psi = map_to_wavefunction(u)

    for _ in range(T):
        psi = evolve_wavefunction(psi, dt, N, nu)

    final_u = np.abs(psi)**2
    return x, final_u

if __name__ == "__main__":
    x, u = run_simulation()
    plt.plot(x, u)
    plt.title("1D Burgers Equation via HSE Method")
    plt.xlabel("x")
    plt.ylabel("Velocity")
    plt.grid(True)
    plt.show()
