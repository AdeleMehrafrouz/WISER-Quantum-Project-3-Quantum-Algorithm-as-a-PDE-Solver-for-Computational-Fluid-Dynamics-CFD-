import numpy as np
import matplotlib.pyplot as plt

def initialize_velocity_mps(N, shock_position=0.5):
    x = np.linspace(0, 1, N)
    u = np.where(x < shock_position, 1.0, 0.0)

    # Basic rank-3 tensors (phys_dim, 1, 1)
    mps = [
        np.array([
            [np.sqrt(val + 1e-6)],
            [np.sqrt(1.0 - val + 1e-6)]
        ])[:, np.newaxis, :]  # Shape: (2, 1, 1)
        for val in u
    ]
    return x, mps

def apply_local_unitaries(mps, dt, steps=3):
    d = 2  # Physical dimension
    swap_like = np.array([
        [1, 0, 0, 0],
        [0, 0.99, 0.01, 0],
        [0, 0.01, 0.99, 0],
        [0, 0, 0, 1]
    ]).reshape(d, d, d, d)

    for _ in range(steps):
        for i in range(len(mps) - 1):
            A, B = mps[i], mps[i + 1]  # Each shape: (2,1,1)

            # Combine into joint state (2,1) x (2,1) => (2,2)
            psi = np.tensordot(A, B, axes=([2], [1]))  # (2,1,1) x (2,1,1) -> (2,1,2,1)
            psi = np.squeeze(psi)  # (2,2)

            # Apply gate: contract with (2,2,2,2)
            psi = np.tensordot(swap_like, psi, axes=([2, 3], [0, 1]))  # -> (2,2)

            # Reshape back to rank-3 tensors
            A_new = psi[:, 0].reshape(2, 1, 1)
            B_new = psi[:, 1].reshape(2, 1, 1)

            mps[i] = A_new
            mps[i + 1] = B_new
    return mps

def reconstruct_velocity(mps):
    u = []
    for tensor in mps:
        psi = tensor[:, 0, 0]
        prob = np.abs(psi[0])**2  # |amp_0|^2
        u.append(prob)
    return np.array(u)

def run_qtn_simulation(N=16, T=3, dt=0.01, plot=True):
    x, mps = initialize_velocity_mps(N)
    mps = apply_local_unitaries(mps, dt, steps=T)
    u_final = reconstruct_velocity(mps)

    if plot:
        plt.plot(x, u_final, label="QTN u(x)")
        plt.title("QTN-Inspired Simulation of 1D Burgers Equation")
        plt.xlabel("x")
        plt.ylabel("Velocity")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("results/qtn_mps_output.png")
        plt.close()

    return x, u_final
