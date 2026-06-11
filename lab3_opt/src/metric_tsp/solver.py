"""
METRIC-TSP 求解器
OPTIMIZED: 暴力求解部分使用回溯+剪枝以减少搜索空间。
"""

import itertools
import time
from typing import List, Tuple

from src.metric_tsp.dfs import build_tsp_tour, dfs_traversal
from src.metric_tsp.models import Edge, WeightedGraph
from src.metric_tsp.mst import kruskal, mst_total_cost


class TSPResult:
    def __init__(
        self,
        mst_edges: List[Edge],
        mst_cost: int,
        dfs_order: List[str],
        tsp_tour: List[str],
        tsp_cost: int,
        optimal_tour: List[str],
        optimal_cost: int,
        approximation_ratio: float,
        elapsed_time: float,
    ) -> None:
        self.mst_edges = mst_edges
        self.mst_cost = mst_cost
        self.dfs_order = dfs_order
        self.tsp_tour = tsp_tour
        self.tsp_cost = tsp_cost
        self.optimal_tour = optimal_tour
        self.optimal_cost = optimal_cost
        self.approximation_ratio = approximation_ratio
        self.elapsed_time = elapsed_time

    def __repr__(self) -> str:
        return (
            f"TSPResult(tsp_cost={self.tsp_cost}, optimal_cost={self.optimal_cost}, ratio={self.approximation_ratio:.3f}, time={self.elapsed_time:.4f}s)"
        )


def solve(graph: WeightedGraph, root: str = None) -> TSPResult:
    if root is None:
        root = graph.city_names[0]

    start_time = time.perf_counter()

    mst_edges = kruskal(graph)
    mst_cost = mst_total_cost(mst_edges)
    dfs_order = dfs_traversal(mst_edges, root)
    tsp_tour = build_tsp_tour(dfs_order)
    tsp_cost = compute_tour_cost(tsp_tour, graph)

    # OPTIMIZED: 使用回溯剪枝求最优解（比枚举全排列更易于剪枝）
    optimal_tour, optimal_cost = brute_force_optimal_with_pruning(graph)

    approximation_ratio = tsp_cost / optimal_cost if optimal_cost > 0 else float("inf")

    elapsed_time = time.perf_counter() - start_time

    return TSPResult(
        mst_edges=mst_edges,
        mst_cost=mst_cost,
        dfs_order=dfs_order,
        tsp_tour=tsp_tour,
        tsp_cost=tsp_cost,
        optimal_tour=optimal_tour,
        optimal_cost=optimal_cost,
        approximation_ratio=approximation_ratio,
        elapsed_time=elapsed_time,
    )


def brute_force_optimal_with_pruning(graph: WeightedGraph) -> Tuple[List[str], int]:
    names = graph.city_names
    n = len(names)
    if n <= 1:
        return names + [names[0]], 0

    start = names[0]
    rest = names[1:]

    best_tour: List[str] = []
    best_cost = float("inf")

    # 回溯构造路径并剪枝
    def backtrack(path: List[str], used: set, current_cost: int):
        nonlocal best_cost, best_tour
        if current_cost >= best_cost:
            return
        if len(path) == n:
            tour = path + [start]
            total_cost = current_cost + graph.get_weight(path[-1], start)
            if total_cost < best_cost:
                best_cost = total_cost
                best_tour = tour
            return
        for city in rest:
            if city in used:
                continue
            added = graph.get_weight(path[-1], city)
            backtrack(path + [city], used | {city}, current_cost + added)

    backtrack([start], set(), 0)

    return best_tour, int(best_cost)


def compute_tour_cost(tour: List[str], graph: WeightedGraph) -> int:
    return sum(graph.get_weight(tour[i], tour[i + 1]) for i in range(len(tour) - 1))


def print_result(graph: WeightedGraph, result: TSPResult, root: str) -> None:
    print(f"城市数量：{graph.num_cities}")
    print(f"根节点：{root}")
    print(f"最小生成树 MST 边集：")
    for edge in result.mst_edges:
        print(f"  {edge}")
    print(f"MST 总代价：{result.mst_cost}")
    print(f"DFS 遍历顺序：")
    print(f"  {' -> '.join(result.dfs_order)}")
    print(f"TSP 近似回路：")
    print(f"  {' -> '.join(result.tsp_tour)}")
    print(f"TSP 近似回路总代价：{result.tsp_cost}")
    print(f"2 * MST 总代价：{2 * result.mst_cost}")
    print(f"最优 TSP 回路：")
    print(f"  {' -> '.join(result.optimal_tour)}")
    print(f"最优 TSP 回路总代价：{result.optimal_cost}")
    print(f"近似比例：{result.tsp_cost} / {result.optimal_cost} = {result.approximation_ratio:.3f}")
    print(f"运行时间：{result.elapsed_time:.3f}s")
