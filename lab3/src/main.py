"""
计算复杂性第三次编程作业主入口

本程序实现两个近似算法：
- 任务1: MAX-3SAT 随机近似算法（Las Vegas 风格）
- 任务2: METRIC-TSP 2-近似算法（MST + DFS）

使用方法:
    python src/main.py --task 1 --input test/max3sat/fixed.txt
    python src/main.py --task 1 --input test/max3sat/random_config.txt --mode random
    python src/main.py --task 2 --input test/metric_tsp/sample.txt
    python src/main.py --all  # 运行所有测试用例

注意：请从项目根目录运行此脚本
"""

import argparse
import os
import sys
from pathlib import Path

# 设置标准输出编码为UTF-8，解决Windows终端中文显示问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 确保从项目根目录运行
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# 将项目根目录添加到路径
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.max3sat.parser import parse_formula, parse_random_config, generate_random_formula
from src.max3sat.solver import solve as max3sat_solve, print_result as max3sat_print
from src.metric_tsp.graph import parse_cities, build_complete_graph
from src.metric_tsp.solver import solve as tsp_solve, print_result as tsp_print
from src.utils.timer import Timer


def run_max3sat(input_file: str, mode: str = "fixed") -> None:
    """
    运行 MAX-3SAT 随机近似算法

    Args:
        input_file: 输入文件路径
        mode: "fixed" 表示读取已有公式，"random" 表示根据配置随机生成
    """
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
            result = max3sat_solve(formula)
            max3sat_print(formula, result)

            base_name = Path(output_file or f"random_{config['number_of_variables']}_{config['number_of_clauses']}_seed{config['seed']}.txt").stem
            result_path = os.path.join(output_dir, f"{base_name}_result.txt")
            _save_max3sat_result(formula, result, result_path)
            print(f"\n结果已保存至: {result_path}")
        return
    else:
        formula = parse_formula(input_path)

    print()
    result = max3sat_solve(formula)
    max3sat_print(formula, result)

    # 保存结果到 output 目录
    output_dir = os.path.join(project_root, "output", "max3sat")
    os.makedirs(output_dir, exist_ok=True)
    base_name = Path(input_file).stem
    result_path = os.path.join(output_dir, f"{base_name}_result.txt")
    _save_max3sat_result(formula, result, result_path)
    print(f"\n结果已保存至: {result_path}")


def _save_max3sat_result(formula, result, filepath: str) -> None:
    """将 MAX-3SAT 结果保存到文件"""
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
        f.write(f"随机循环次数：{result.iterations}\n")
        f.write(f"运行时间：{result.elapsed_time:.4f} 秒\n")


def run_metric_tsp(input_file: str) -> None:
    """
    运行 METRIC-TSP 2-近似算法

    Args:
        input_file: 输入文件路径（城市坐标）
    """
    input_path = os.path.join(project_root, input_file)

    # 解析城市坐标
    cities = parse_cities(input_path)

    # 构造带权完全图
    graph = build_complete_graph(cities)

    # 运行 2-近似算法
    root = graph.city_names[0]
    result = tsp_solve(graph, root)
    tsp_print(graph, result, root)

    # 保存结果到 output 目录
    output_dir = os.path.join(project_root, "output", "metric_tsp")
    os.makedirs(output_dir, exist_ok=True)
    base_name = Path(input_file).stem
    result_path = os.path.join(output_dir, f"{base_name}_result.txt")
    _save_tsp_result(graph, result, root, result_path)
    print(f"\n结果已保存至: {result_path}")


def _save_tsp_result(graph, result, root: str, filepath: str) -> None:
    """将 METRIC-TSP 结果保存到文件"""
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
    """运行所有测试用例"""
    print("=" * 60)
    print("运行所有测试用例")
    print("=" * 60)

    # 任务1：固定测试用例
    fixed_path = os.path.join(project_root, "test", "max3sat", "fixed.txt")
    if os.path.exists(fixed_path):
        print("\n" + "=" * 60)
        print("任务1 - 固定测试用例")
        print("=" * 60)
        run_max3sat(fixed_path, mode="fixed")

    # 任务1：随机生成测试用例
    random_config_path = os.path.join(project_root, "test", "max3sat", "random_config.txt")
    if os.path.exists(random_config_path):
        print("\n" + "=" * 60)
        print("任务1 - 随机生成测试用例")
        print("=" * 60)
        run_max3sat(random_config_path, mode="random")

    # 任务2：METRIC-TSP 测试
    tsp_path = os.path.join(project_root, "test", "metric_tsp", "sample.txt")
    if os.path.exists(tsp_path):
        print("\n" + "=" * 60)
        print("任务2 - METRIC-TSP 测试")
        print("=" * 60)
        run_metric_tsp(tsp_path)


def main() -> int:
    """主函数，解析命令行参数并执行对应任务"""
    parser = argparse.ArgumentParser(
        description="计算复杂性第三次编程作业：近似算法实现"
    )
    parser.add_argument(
        "--task", type=int, choices=[1, 2],
        help="任务编号：1=MAX-3SAT, 2=METRIC-TSP"
    )
    parser.add_argument(
        "--input", type=str,
        help="输入文件路径"
    )
    parser.add_argument(
        "--mode", type=str, choices=["fixed", "random"], default="fixed",
        help="MAX-3SAT 输入模式：fixed=读取已有公式, random=随机生成"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="运行所有测试用例"
    )

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
