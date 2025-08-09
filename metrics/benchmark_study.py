#metrics/benchmark_study.py
import csv
from metrics.compare_all import compare_all

grid_sizes = [8, 16, 32]
results = []

for N in grid_sizes:
    res = compare_all(N=N, T=3, dt=0.01)
    results.append(res)

# Write to CSV
with open("results/benchmark_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("\n Benchmark results saved to results/benchmark_results.csv")
