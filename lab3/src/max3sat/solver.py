"""
MAX-3SAT 随机近似算法求解器

实现 Las Vegas 风格的随机近似算法：
不断随机生成变量赋值，直到找到一组满足至少 ⌈7/8 * m⌉ 个子句的赋值。
"""

import random
import time

from src.max3sat.models import Formula
from src.utils.timer import Timer


class Max3SatResult:
    """
    MAX-3SAT 求解结果

    Attributes:
        assignment: 变量赋值 {变量名: 布尔值}
        satisfied_count: 满足的子句数量
        satisfied_indices: 满足的子句编号列表
        total_clauses: 总子句数量
        threshold: 目标满足子句数量
        iterations: 随机循环次数
        elapsed_time: 运行时间（秒）
    """

    def __init__(
        self,
        assignment: dict[str, bool],
        satisfied_count: int,
        satisfied_indices: list[int],
        total_clauses: int,
        threshold: int,
        iterations: int,
        elapsed_time: float,
    ) -> None:
        self.assignment = assignment
        self.satisfied_count = satisfied_count
        self.satisfied_indices = satisfied_indices
        self.total_clauses = total_clauses
        self.threshold = threshold
        self.iterations = iterations
        self.elapsed_time = elapsed_time

    def __repr__(self) -> str:
        return (
            f"Max3SatResult("
            f"satisfied={self.satisfied_count}/{self.total_clauses}, "
            f"threshold={self.threshold}, "
            f"iterations={self.iterations}, "
            f"time={self.elapsed_time:.4f}s)"
        )


def solve(formula: Formula, seed: int | None = None) -> Max3SatResult:
    """
    运行 MAX-3SAT 随机近似算法

    算法流程：
        循环:
            随机生成一组变量赋值
            计算该赋值满足的子句数量
        直到:
            满足的子句数量 >= ⌈7/8 * m⌉
        输出:
            变量赋值、满足子句数量、循环次数、运行时间

    Args:
        formula: MAX-3SAT 公式
        seed: 可选随机种子

    Returns:
        Max3SatResult 求解结果
    """
    rng = random.Random(seed)
    threshold = formula.threshold
    variables = formula.variables
    iterations = 0

    start_time = time.perf_counter()

    while True:
        iterations += 1
        assignment = random_assignment(variables, rng)
        satisfied_count = formula.count_satisfied(assignment)
        if satisfied_count >= threshold:
            break

    elapsed_time = time.perf_counter() - start_time

    satisfied_indices = formula.get_satisfied_indices(assignment)

    return Max3SatResult(
        assignment=assignment,
        satisfied_count=satisfied_count,
        satisfied_indices=satisfied_indices,
        total_clauses=formula.num_clauses,
        threshold=threshold,
        iterations=iterations,
        elapsed_time=elapsed_time,
    )


def random_assignment(variables: list[str], rng: random.Random) -> dict[str, bool]:
    """
    随机生成一组变量赋值

    Args:
        variables: 变量名列表
        rng: 随机数生成器

    Returns:
        变量名 -> 布尔值的映射
    """
    return {var: rng.choice([True, False]) for var in variables}


def print_result(formula: Formula, result: Max3SatResult) -> None:
    """
    按规格说明格式输出求解结果

    Args:
        formula: MAX-3SAT 公式
        result: 求解结果
    """
    print(f"输入公式：")
    print(f"{formula}")
    print(f"变量数量：{formula.num_variables}")
    print(f"子句数量：{formula.num_clauses}")
    print(f"目标满足子句数量：{result.threshold}")
    print(f"找到的变量赋值：")
    for var in formula.variables:
        val = result.assignment[var]
        print(f"  {var} = {val}")
    print(f"满足的子句数量：{result.satisfied_count} / {result.total_clauses}")
    satisfied_names = [f"C{i}" for i in result.satisfied_indices]
    print(f"满足的子句编号：{', '.join(satisfied_names)}")
    print(f"随机循环次数：{result.iterations}")
    print(f"运行时间：{result.elapsed_time:.4f} 秒")
