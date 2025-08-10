# WISER-Quantum-Project-3-Quantum-Algorithm-as-a-PDE-Solver-for-Computational-Fluid-Dynamics-CFD-

## Overview

This project explores quantum and quantum-inspired algorithms for solving partial differential equations (PDEs) arising in Computational Fluid Dynamics (CFD), using the 1D viscous **Burgers’ Equation** as a benchmark.

I implement and benchmark two methods:

- **Hydrodynamic Schrödinger Equation (HSE)**: Reformulates Burgers' equation as a quantum wavefunction evolution and simulates it on quantum circuits.
- **Quantum Tensor Network (QTN)**: Uses matrix product states (MPS) to compress and evolve the velocity field, leveraging quantum-inspired classical computing.

This work was conducted as part of the ** WISER Quantum Program 2025**.

## Project Structure

```
project3-quantum-cfd/
├── src/
│   ├── burgers_hse_solver.py          # HSE implementation
│   ├── burgers_qtn_solver.py          # QTN implementation
│   ├── quantum_hse_solver.py          # Quantum HSE circuit design
│   ├── utils.py                            # Helper functions: discretization, visualization
├── results/
│   ├── burgers_hse_output.png
│   ├── burgers_qtn_output.png
│   └── error_metrics.csv
├── metrics/
│   ├── error_analysis.py              # L2 error, runtime, noise profile analysis
│   ├── benchmark_study.py             # Benchmark study script
│   ├── compare_all.py                 # Function to compare all solvers
│   ├── scaling_study.py               # Scaling study for runtime and error analysis
│   └── comparison_summary.py          # Final comparison summary
├── hardware/
│   └── ibmq_run.py                    # Script to run on real IBM quantum hardware
├── docs/
│   ├── algorithm_brief.pdf            # technical design description
│── README.md                          # Project overview and instructions
└── run_all.ipynb                      # Full walkthrough notebook
```


## Problem Background

The **1D Burgers’ Equation** is a nonlinear PDE capturing convective and diffusive dynamics:

```math
∂u/∂t + u ∂u/∂x = ν ∂²u/∂x²
```

It is widely used as a simplified model of incompressible Navier–Stokes flow.

## Deliverables

| No. | Task Description |
|-----|------------------|
| 1️ | **Algorithm Design Brief** – Describes chosen method (HSE or QTN), PDE mapping, and gate structure. |
| 2️ | **Prototype Code** – Implements 1D Burgers' equation simulation using HSE and/or QTN. |
| 3️ | **Validation & Benchmarking** – Compare quantum results to classical reference solution, report L₂ error and runtime. |
| 4️ | **Resource & Noise Analysis** – List qubit count, circuit depth, and noise mitigation strategy. |
| 5️ | **Quantum Hardware Execution** – Execute at least one time step on a real QPU and analyze output. |
| 6️ | **Scalability Study** – Show how grid size affects resource usage (e.g., N = 16, 32, 64). |
| 7️ | **Algorithm Comparison** – Evaluate and contrast HSE vs. QTN (or hybrid) in terms of scalability and efficiency. |

## Getting Started

1. **Set up the environment**:
   ```bash
   python -m venv qufluid-env
   source qufluid-env/bin/activate
   pip install -r requirements.txt
   ```

2. **Run all experiments**:
   Open `run_all.ipynb` in Jupyter and follow the instructions for HSE and QTN workflows.

## Output & Metrics

- L₂ error between quantum and classical results.
- Total Variation Distance and KL Divergence for distributions.
- Runtime and circuit resource estimates (depth, T-count).
- Visualizations of velocity evolution, error heatmaps.

## 👥 Team

- **Adele Mehrafrouz**

## References

- Meng & Yang. *Quantum Computing of Fluid Dynamics Using the HSE*, Phys. Rev. Research 5, 033182 (2023)
- Peddinti et al. *Quantum-Inspired Framework for CFD*, Commun. Phys. 7, 135 (2024)

## Notes

- Start with a grid size of N=16 and short time integration to keep circuit depth low.
- Use `Aer` noise models or real QPUs via IBMQ for noisy runs.
- All code is modular and ready for extension to 2D/3D solvers.
