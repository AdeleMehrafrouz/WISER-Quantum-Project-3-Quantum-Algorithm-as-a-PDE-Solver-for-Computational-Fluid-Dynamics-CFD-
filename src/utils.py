# src/s.py

import numpy as np
import matplotlib.pyplot as plt

def l2_error(u_approx, u_exact):
    return np.sqrt(np.sum((u_approx - u_exact) ** 2) / len(u_approx))

def plot_solution(x, u, title="Burgers Solution", save_path=None):
    plt.plot(x, u, label="Final u(x)")
    plt.xlabel("x")
    plt.ylabel("u")
    plt.title(title)
    plt.grid(True)
    if save_path:
        plt.savefig(save_path)
    plt.show()
