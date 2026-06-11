import os
import sys
import csv
import random
from pathlib import Path

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = script_dir
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.max3sat.parser import generate_random_formula
from src.max3sat.solver import solve


def run_experiment():
    sizes = [50, 100, 150, 200, 250]
    clause_ratio = 4.0
    seeds = [2026]

    output_dir = os.path.join(project_root, "output", "max3sat")
    os.makedirs(output_dir, exist_ok=True)
    test_dir = os.path.join(project_root, "test", "max3sat")
    os.makedirs(test_dir, exist_ok=True)

    csv_path = os.path.join(output_dir, "max3sat_scaling_results.csv")
    png_path = os.path.join(output_dir, "max3sat_scaling_plot.png")

    rows = []

    for n in sizes:
        m = int(n * clause_ratio)
        for run_idx, seed in enumerate(seeds, start=1):
            formula_file = os.path.join(test_dir, f"random_{n}_{m}_seed{seed}.txt")
            formula = generate_random_formula(
                num_variables=n,
                num_clauses=m,
                seed=seed,
                output_file=formula_file,
            )
            print(f"[{n},{m}] 运行第 {run_idx} 次，seed={seed}...", flush=True)
            result = solve(formula, seed=seed, max_attempts=200000, use_hill_climb=True)
            success = result.satisfied_count >= result.threshold

            rows.append({
                "num_variables": n,
                "num_clauses": m,
                "seed": seed,
                "random_assignments": result.random_assignments,
                "clause_checks": getattr(result, 'clause_checks', 0),
                "hill_flips": getattr(result, 'hill_flips', 0),
                "elapsed_time": result.elapsed_time,
                "satisfied_count": result.satisfied_count,
                "threshold": result.threshold,
                "success": int(success),
            })

            print(
                f"  满足 {result.satisfied_count}/{result.total_clauses}, "
                f"阈值 {result.threshold}, 随机赋值次数 {result.random_assignments}, "
                f"子句检查次数 {getattr(result, 'clause_checks', 0)}, 爬山翻转尝试 {getattr(result, 'hill_flips', 0)}, 时间 {result.elapsed_time:.4f}s, "
                f"成功={success}"
            )

    fieldnames = [
        "num_variables",
        "num_clauses",
        "seed",
        "random_assignments",
        "clause_checks",
        "hill_flips",
        "elapsed_time",
        "satisfied_count",
        "threshold",
        "success",
    ]
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    try:
        import numpy as np
        import matplotlib.pyplot as plt
    except ImportError as exc:
        print("绘图库不可用，请安装 matplotlib 和 numpy", exc)
        return

    sizes_arr = np.array([row["num_variables"] for row in rows])
    times_arr = np.array([row["elapsed_time"] for row in rows])
    iters_arr = np.array([row["random_assignments"] for row in rows])
    checks_arr = np.array([row["clause_checks"] for row in rows])

    fig, ax1 = plt.subplots(figsize=(10, 6))
    for seed in seeds:
        mask = [row["seed"] == seed for row in rows]
        xs = sizes_arr[mask]
        ys_time = times_arr[mask]
        ys_iters = iters_arr[mask]
        ax1.plot(xs, ys_time, marker="o", label=f"Time seed={seed}")
    ax1.set_xlabel("Number of Variables")
    ax1.set_ylabel("Elapsed Time (s)")
    ax1.grid(True, linestyle="--", alpha=0.5)

    ax2 = ax1.twinx()
    for seed in seeds:
        mask = [row["seed"] == seed for row in rows]
        xs = sizes_arr[mask]
        ys_iters = iters_arr[mask]
        ax2.plot(xs, ys_iters, marker="x", linestyle="--", label=f"Random Assignments seed={seed}")
        # also plot clause checks as dotted line
        ax2.plot(xs, checks_arr[mask], marker=".", linestyle=":", label=f"Clause Checks seed={seed}")
    ax2.set_ylabel("Random Assignments")

    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    fig.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper left", bbox_to_anchor=(0.12, 0.95))
    fig.suptitle("MAX-3SAT Scaling Experiment: Variables vs Time / Random Assignments")
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig(png_path, dpi=200)
    plt.close(fig)

    summary_path = os.path.join(output_dir, "max3sat_scaling_summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("MAX-3SAT Scaling Experiment Summary\n")
        f.write("===============================\n")
        f.write("Problem size, avg_random_assignments, avg_clause_checks, avg_hill_flips, avg_time_s, avg_satisfied, threshold, success_rate\n")
        for n in sizes:
            filtered = [row for row in rows if row["num_variables"] == n]
            avg_iter = sum(row["random_assignments"] for row in filtered) / len(filtered)
            avg_checks = sum(row["clause_checks"] for row in filtered) / len(filtered)
            avg_hill = sum(row["hill_flips"] for row in filtered) / len(filtered)
            avg_time = sum(row["elapsed_time"] for row in filtered) / len(filtered)
            avg_sat = sum(row["satisfied_count"] for row in filtered) / len(filtered)
            threshold = filtered[0]["threshold"]
            success_rate = sum(row["success"] for row in filtered) / len(filtered)
            f.write(f"{n},{avg_iter:.2f},{avg_checks:.0f},{avg_hill:.0f},{avg_time:.4f},{avg_sat:.2f},{threshold},{success_rate:.2f}\n")

    print(f"实验结果已保存到: {csv_path}")
    print(f"可视化图表已保存到: {png_path}")
    print(f"摘要已保存到: {summary_path}")


if __name__ == "__main__":
    run_experiment()
