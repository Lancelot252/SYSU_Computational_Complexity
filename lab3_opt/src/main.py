"""
副本主入口（lab3_opt）。通常与原始 `src/main.py` 相同，仅路径和说明保留一致性。
"""

import argparse
import os
import sys
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.max3sat.parser import parse_formula, parse_random_config, generate_random_formula
from src.max3sat.solver import solve as max3sat_solve, print_result as max3sat_print
from src.metric_tsp.graph import parse_cities, build_complete_graph
from src.metric_tsp.solver import solve as tsp_solve, print_result as tsp_print
from src.utils.timer import Timer


def run_max3sat(input_file: str, mode: str = "fixed") -> None:
    input_path = os.path.join(project_root, input_file)

    if mode == "random":
        configs = parse_random_config(input_path)
        print("=" * 60)
        print("MAX-3SAT 随机生成模式")
        print("=" * 60)

        output_dir = os.path.join(project_root, "output", "max3sat")
        os.makedirs(output_dir, exist_ok=True)

        for idx, config in enumerate(configs, start=1):
            print(f"\n配置 {idx}: 变量数={config['number_of_variables']}, 子句数={config['number_of_clauses']}, 种子={config['seed']}")
            output_file = config.get("output_file")
            output_path = os.path.join(project_root, output_file) if output_file else None
            formula = generate_random_formula(
                num_variables=config["number_of_variables"],
                num_clauses=config["number_of_clauses"],
                seed=config["seed"],
                output_file=output_path,
            )
            if output_path:
                print(f"随机公式已保存至: {output_path}")

            print()
            result = max3sat_solve(formula, seed=None, max_attempts=200000, use_hill_climb=True)
            max3sat_print(formula, result)

            base_name = Path(output_file or f"random_{config['number_of_variables']}_{config['number_of_clauses']}_seed{config['seed']}.txt").stem
            result_path = os.path.join(output_dir, f"{base_name}_result.txt")
            _save_max3sat_result(formula, result, result_path)
            print(f"\n结果已保存至: {result_path}")
        return
    else:
        formula = parse_formula(input_path)

    print()
    # 使用优化选项：启用局部爬山, 限制最大尝试次数
    result = max3sat_solve(formula, seed=None, max_attempts=200000, use_hill_climb=True)
    max3sat_print(formula, result)

    output_dir = os.path.join(project_root, "output", "max3sat")
    os.makedirs(output_dir, exist_ok=True)
    base_name = Path(input_file).stem
    result_path = os.path.join(output_dir, f"{base_name}_result.txt")
    _save_max3sat_result(formula, result, result_path)
    print(f"\n结果已保存至: {result_path}")


def _save_max3sat_result(formula, result, filepath: str) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"输入公式：\n{formula}\n")
        f.write(f"变量数量：{formula.num_variables}\n")
        f.write(f"子句数量：{formula.num_clauses}\n")
        f.write(f"目标满足子句数量：{result.threshold}\n")
        f.write(f"找到的变量赋值：\n")
        for var in formula.variables:
            f.write(f"  {var} = {result.assignment[var]}\n")
        f.write(f"满足的子句数量：{result.satisfied_count} / {result.total_clauses}\n")
        satisfied_names = [f"C{i}" for i in result.satisfied_indices]
        f.write(f"满足的子句编号：{', '.join(satisfied_names)}\n")
        f.write(f"随机赋值次数：{result.random_assignments}\n")
        f.write(f"子句检查次数：{getattr(result, 'clause_checks', 'N/A')}\n")
        f.write(f"爬山翻转尝试次数：{getattr(result, 'hill_flips', 'N/A')}\n")
        f.write(f"运行时间：{result.elapsed_time:.4f} 秒\n")


def run_metric_tsp(input_file: str) -> None:
    input_path = os.path.join(project_root, input_file)
    cities = parse_cities(input_path)
    graph = build_complete_graph(cities)
    root = graph.city_names[0]
    result = tsp_solve(graph, root)
    tsp_print(graph, result, root)

    output_dir = os.path.join(project_root, "output", "metric_tsp")
    os.makedirs(output_dir, exist_ok=True)
    base_name = Path(input_file).stem
    result_path = os.path.join(output_dir, f"{base_name}_result.txt")
    _save_tsp_result(graph, result, root, result_path)
    print(f"\n结果已保存至: {result_path}")


def _save_tsp_result(graph, result, root: str, filepath: str) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"城市数量：{graph.num_cities}\n")
        f.write(f"根节点：{root}\n")
        f.write(f"最小生成树 MST 边集：\n")
        for edge in result.mst_edges:
            f.write(f"  {edge}\n")
        f.write(f"MST 总代价：{result.mst_cost}\n")
        f.write(f"DFS 遍历顺序：\n")
        f.write(f"  {' -> '.join(result.dfs_order)}\n")
        f.write(f"TSP 近似回路：\n")
        f.write(f"  {' -> '.join(result.tsp_tour)}\n")
        f.write(f"TSP 近似回路总代价：{result.tsp_cost}\n")
        f.write(f"2 * MST 总代价：{2 * result.mst_cost}\n")
        f.write(f"最优 TSP 回路：\n")
        f.write(f"  {' -> '.join(result.optimal_tour)}\n")
        f.write(f"最优 TSP 回路总代价：{result.optimal_cost}\n")
        f.write(f"近似比例：{result.tsp_cost} / {result.optimal_cost} = {result.approximation_ratio:.3f}\n")
        f.write(f"运行时间：{result.elapsed_time:.3f}s\n")


def run_all() -> None:
    print("=" * 60)
    print("运行所有测试用例（lab3_opt）")
    print("=" * 60)

    fixed_path = os.path.join(project_root, "test", "max3sat", "fixed.txt")
    if os.path.exists(fixed_path):
        print("\n" + "=" * 60)
        print("任务1 - 固定测试用例")
        print("=" * 60)
        run_max3sat(fixed_path, mode="fixed")

    random_config_path = os.path.join(project_root, "test", "max3sat", "random_config.txt")
    if os.path.exists(random_config_path):
        print("\n" + "=" * 60)
        print("任务1 - 随机生成测试用例")
        print("=" * 60)
        run_max3sat(random_config_path, mode="random")

    tsp_path = os.path.join(project_root, "test", "metric_tsp", "sample.txt")
    if os.path.exists(tsp_path):
        print("\n" + "=" * 60)
        print("任务2 - METRIC-TSP 测试")
        print("=" * 60)
        run_metric_tsp(tsp_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="lab3_opt: 近似算法实现（副本）")
    parser.add_argument("--task", type=int, choices=[1, 2], help="任务编号：1=MAX-3SAT, 2=METRIC-TSP")
    parser.add_argument("--input", type=str, help="输入文件路径")
    parser.add_argument("--mode", type=str, choices=["fixed", "random"], default="fixed", help="MAX-3SAT 输入模式：fixed=读取已有公式, random=随机生成")
    parser.add_argument("--all", action="store_true", help="运行所有测试用例")

    args = parser.parse_args()

    if args.all:
        run_all()
    elif args.task == 1:
        if not args.input:
            parser.error("任务1需要指定 --input 参数")
        run_max3sat(args.input, args.mode)
    elif args.task == 2:
        if not args.input:
            parser.error("任务2需要指定 --input 参数")
        run_metric_tsp(args.input)
    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
