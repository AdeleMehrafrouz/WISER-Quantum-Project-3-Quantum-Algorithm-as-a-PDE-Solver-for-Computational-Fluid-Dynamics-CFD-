# src/quantum_hse_solver.py
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer, AerSimulator
from qiskit.circuit import Parameter
from qiskit_aer.noise import NoiseModel
from qiskit_aer.noise import NoiseModel
from qiskit_aer import AerSimulator

import numpy as np
import matplotlib.pyplot as plt
import os



# Ensure results directory exists
os.makedirs("results", exist_ok=True)

def hse_quantum_circuit(N, dt, steps):
    qubits = int(np.ceil(np.log2(N)))
    qc = QuantumCircuit(qubits)
    theta = Parameter("θ")

    # Initialize: uniform superposition
    qc.h(range(qubits))

    # Simple evolution: Rx + CZ layers
    for _ in range(steps):
        for i in range(qubits):
            qc.rx(theta, i)
            qc.cz(i, (i + 1) % qubits)
        qc.barrier()

    return qc.assign_parameters({theta: -dt})


def run_hse_simulation(N=8, dt=0.01, steps=3, noisy=False, plot=True):
    qc = hse_quantum_circuit(N, dt, steps)

    if noisy:
        noise_model = NoiseModel()
        backend = AerSimulator(noise_model=noise_model)
        label = "noisy"
        shots = 1024

        # Add measurement
        qc.measure_all()
    else:
        backend = Aer.get_backend("statevector_simulator")
        label = "ideal"
        shots = 1

    compiled = transpile(qc, backend)
    job = backend.run(compiled, shots=shots)
    result = job.result()

    if noisy:
        counts = result.get_counts()
        probs = np.zeros(2 ** qc.num_qubits)
        for bitstring, count in counts.items():
            idx = int(bitstring, 2)
            probs[idx] = count / shots
    else:
        statevector = result.get_statevector()
        probs = np.abs(statevector) ** 2

    if plot:
        plt.bar(range(len(probs)), probs)
        plt.title(f"HSE Quantum Evolution Output ({label})")
        plt.xlabel("Basis State")
        plt.ylabel("Probability")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"results/quantum_hse_{label}_distribution.png")
        plt.close()

    return probs


def compare_noisy_vs_ideal(N=8, dt=0.01, steps=3):
    p_ideal = run_hse_simulation(N, dt, steps, noisy=False, plot=True)
    p_noisy = run_hse_simulation(N, dt, steps, noisy=True, plot=True)

    l2 = np.sqrt(np.sum((p_ideal - p_noisy) ** 2))
    print(f"L2 error between ideal and noisy HSE simulation: {l2:.6f}")

    return l2


if __name__ == "__main__":
    print("Running comparison of noisy vs. ideal HSE circuits...")
    compare_noisy_vs_ideal()
