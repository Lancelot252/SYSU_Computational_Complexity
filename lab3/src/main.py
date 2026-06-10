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


def run_max3sat(input_file: str, mode: str = "fixed") -> None:
    """
    运行 MAX-3SAT 随机近似算法

    Args:
        input_file: 输入文件路径
        mode: "fixed" 表示读取已有公式，"random" 表示根据配置随机生成
    """
    # TODO: 实现任务1的运行逻辑
    raise NotImplementedError("MAX-3SAT 求解器尚未实现")


def run_metric_tsp(input_file: str) -> None:
    """
    运行 METRIC-TSP 2-近似算法

    Args:
        input_file: 输入文件路径（城市坐标）
    """
    # TODO: 实现任务2的运行逻辑
    raise NotImplementedError("METRIC-TSP 求解器尚未实现")


def run_all() -> None:
    """运行所有测试用例"""
    # TODO: 实现批量运行逻辑
    raise NotImplementedError("批量运行尚未实现")


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
