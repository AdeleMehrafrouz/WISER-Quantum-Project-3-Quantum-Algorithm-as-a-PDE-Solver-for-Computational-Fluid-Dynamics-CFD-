#hardware_run/ibmq_run.py
from qiskit_ibm_provider import IBMProvider
from qiskit import transpile
from src.quantum_hse_solver import hse_quantum_circuit
import numpy as np

provider = IBMProvider(token="YOUR_API_KEY")  # Replace or load via env
backend = provider.get_backend("ibmq_lima")

# Params
N = 8
dt = 0.01
steps = 1

qc = hse_quantum_circuit(N, dt, steps)
qc.measure_all()

compiled = transpile(qc, backend)
job = backend.run(compiled, shots=1024)

print("Job submitted:", job.job_id())
print("You can check progress at:", job.status())
