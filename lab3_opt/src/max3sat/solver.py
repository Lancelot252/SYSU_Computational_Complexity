"""
MAX-3SAT 求解器
OPTIMIZED: 增加 `max_attempts` 限制与可选的局部爬山（hill-climb）启发式。
"""

import random
import time
from typing import Dict, List, Optional

from src.max3sat.models import Formula
from src.utils.timer import Timer


class Max3SatResult:
    def __init__(
        self,
        assignment: Dict[str, bool],
        satisfied_count: int,
        satisfied_indices: List[int],
        total_clauses: int,
        threshold: int,
        random_assignments: int,
        clause_checks: int,
        hill_flips: int,
        elapsed_time: float,
    ) -> None:
        self.assignment = assignment
        self.satisfied_count = satisfied_count
        self.satisfied_indices = satisfied_indices
        self.total_clauses = total_clauses
        self.threshold = threshold
        self.random_assignments = random_assignments
        self.iterations = random_assignments
        self.clause_checks = clause_checks
        self.hill_flips = hill_flips
        self.elapsed_time = elapsed_time

    def __repr__(self) -> str:
        return (
            f"Max3SatResult(satisfied={self.satisfied_count}/{self.total_clauses}, "
            f"threshold={self.threshold}, random_assignments={self.random_assignments}, "
            f"clause_checks={self.clause_checks}, hill_flips={self.hill_flips}, time={self.elapsed_time:.4f}s)"
        )


def solve(formula: Formula, seed: Optional[int] = None, max_attempts: int = 100000, use_hill_climb: bool = True) -> Max3SatResult:
    """
    原始随机算法基础上增加了两点优化：
    - `max_attempts` 防止无限循环并作为失败回退
    - 可选的局部爬山启发式（在随机赋值的基础上尝试翻转能提升满足子句数的变量）

    如果启用 `use_hill_climb`，会在每次随机赋值后做有限步的局部改进。
    """
    rng = random.Random(seed)
    threshold = formula.threshold
    variables = formula.variables

    start_time = time.perf_counter()

    best_assignment = None
    best_count = -1

    random_assignments = 0
    clause_checks = 0
    hill_flips = 0

    def count_satisfied_with_checks(assign: Dict[str, bool]):
        cnt = 0
        checks = 0
        for clause in formula.clauses:
            checks += 1
            # evaluate clause truth
            if any(lit.evaluate(assign) for lit in clause.literals):
                cnt += 1
        return cnt, checks

    while random_assignments < max_attempts:
        random_assignments += 1
        assignment = random_assignment(variables, rng)
        satisfied_count, checks = count_satisfied_with_checks(assignment)
        clause_checks += checks

        # OPTIMIZED: 如果启用局部爬山，则尝试改进当前解
        if use_hill_climb and satisfied_count < threshold:
            assignment, satisfied_count, flips, hc_checks = hill_climb_improve(
                formula, assignment, rng, max_steps=100
            )
            hill_flips += flips
            clause_checks += hc_checks

        if satisfied_count >= threshold:
            break

        if satisfied_count > best_count:
            best_count = satisfied_count
            best_assignment = assignment.copy()

    elapsed_time = time.perf_counter() - start_time

    if best_assignment is None:
        best_assignment = assignment

    satisfied_indices = formula.get_satisfied_indices(best_assignment if best_count >= threshold else assignment)

    return Max3SatResult(
        assignment=best_assignment if best_count >= threshold else assignment,
        satisfied_count=best_count if best_count >= 0 else satisfied_count,
        satisfied_indices=satisfied_indices,
        total_clauses=formula.num_clauses,
        threshold=threshold,
        random_assignments=random_assignments,
        clause_checks=clause_checks,
        hill_flips=hill_flips,
        elapsed_time=elapsed_time,
    )

def random_assignment(variables: List[str], rng: random.Random) -> Dict[str, bool]:
    return {var: rng.choice([True, False]) for var in variables}


def hill_climb_improve(formula: Formula, assignment: Dict[str, bool], rng: random.Random, max_steps: int = 100) -> (Dict[str, bool], int):
    """简单的局部搜索：尝试翻转单个变量以获得更高满足子句数，直到没有改进或达到步数上限。"""
    current = assignment.copy()
    current_score = formula.count_satisfied(current)

    flips = 0
    checks = 0

    def count_satisfied_local(assign: Dict[str, bool]):
        cnt = 0
        local_checks = 0
        for clause in formula.clauses:
            local_checks += 1
            if any(lit.evaluate(assign) for lit in clause.literals):
                cnt += 1
        return cnt, local_checks

    for _ in range(max_steps):
        improved = False
        vars_shuffled = list(current.keys())
        rng.shuffle(vars_shuffled)
        for v in vars_shuffled:
            # attempt flip
            flips += 1
            current[v] = not current[v]
            new_score, local_checks = count_satisfied_local(current)
            checks += local_checks
            if new_score > current_score:
                current_score = new_score
                improved = True
                break
            else:
                # revert
                current[v] = not current[v]
        if not improved:
            break
    return current, current_score, flips, checks


def print_result(formula: Formula, result: Max3SatResult) -> None:
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
    print(f"随机赋值次数：{result.random_assignments}")
    print(f"子句检查次数：{getattr(result, 'clause_checks', 'N/A')}")
    print(f"爬山翻转尝试次数：{getattr(result, 'hill_flips', 'N/A')}")
    print(f"运行时间：{result.elapsed_time:.4f} 秒")
