"""
METRIC-TSP 2-近似算法求解器

实现基于最小生成树与 DFS 遍历的 2-近似算法，以及暴力求解最优 TSP 回路。
"""

import itertools
import time

from src.metric_tsp.dfs import build_tsp_tour, dfs_traversal
from src.metric_tsp.models import Edge, WeightedGraph
from src.metric_tsp.mst import kruskal, mst_total_cost


class TSPResult:
    """
    METRIC-TSP 求解结果

    Attributes:
        mst_edges: 最小生成树边集
        mst_cost: MST 总代价
        dfs_order: DFS 遍历顺序
        tsp_tour: TSP 近似回路
        tsp_cost: TSP 近似回路总代价
        optimal_tour: 最优 TSP 回路
        optimal_cost: 最优 TSP 回路总代价
        approximation_ratio: 近似比例
        elapsed_time: 运行时间（秒）
    """

    def __init__(
        self,
        mst_edges: list[Edge],
        mst_cost: int,
        dfs_order: list[str],
        tsp_tour: list[str],
        tsp_cost: int,
        optimal_tour: list[str],
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
            f"TSPResult("
            f"tsp_cost={self.tsp_cost}, "
            f"optimal_cost={self.optimal_cost}, "
            f"ratio={self.approximation_ratio:.3f}, "
            f"time={self.elapsed_time:.4f}s)"
        )


def solve(graph: WeightedGraph, root: str | None = None) -> TSPResult:
    """
    运行 METRIC-TSP 2-近似算法

    算法流程：
    1. 计算带权完全图的最小生成树 MST
    2. 任选一个顶点 s 作为根
    3. 从 s 开始对 MST 进行 DFS 遍历
    4. 根据 DFS 遍历顺序构造 TSP 近似回路
    5. 计算 TSP 近似回路总代价
    6. 暴力求解最优 TSP 回路
    7. 计算近似比例
    8. 记录运行时间

    Args:
        graph: 带权完全图
        root: 根节点名称，若为 None 则默认选择第一个城市

    Returns:
        TSPResult 求解结果
    """
    if root is None:
        root = graph.city_names[0]

    start_time = time.perf_counter()

    # 1. 计算 MST
    mst_edges = kruskal(graph)
    mst_cost = mst_total_cost(mst_edges)

    # 2. DFS 遍历 MST
    dfs_order = dfs_traversal(mst_edges, root)

    # 3. 构造 TSP 近似回路
    tsp_tour = build_tsp_tour(dfs_order)

    # 4. 计算 TSP 近似回路总代价
    tsp_cost = compute_tour_cost(tsp_tour, graph)

    # 5. 暴力求解最优 TSP 回路
    optimal_tour, optimal_cost = brute_force_optimal(graph)

    # 6. 计算近似比例
    if optimal_cost > 0:
        approximation_ratio = tsp_cost / optimal_cost
    else:
        approximation_ratio = float("inf")

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


def brute_force_optimal(graph: WeightedGraph) -> tuple[list[str], int]:
    """
    暴力求解最优 TSP 回路

    遍历所有排列，找到总代价最小的回路。
    城市数量不宜过大（建议不超过9个）。

    Args:
        graph: 带权完全图

    Returns:
        (最优回路, 最优总代价)
    """
    names = graph.city_names
    n = len(names)

    if n <= 1:
        return names + [names[0]], 0

    # 固定起点为第一个城市，遍历其余城市的排列
    start = names[0]
    rest = names[1:]

    best_tour: list[str] = []
    best_cost = float("inf")

    for perm in itertools.permutations(rest):
        tour = [start] + list(perm) + [start]
        cost = compute_tour_cost(tour, graph)
        if cost < best_cost:
            best_cost = cost
            best_tour = tour

    return best_tour, int(best_cost)


def compute_tour_cost(tour: list[str], graph: WeightedGraph) -> int:
    """
    计算 TSP 回路总代价

    Args:
        tour: TSP 回路（闭合，首尾相同）
        graph: 带权完全图

    Returns:
        回路总代价
    """
    total = 0
    for i in range(len(tour) - 1):
        total += graph.get_weight(tour[i], tour[i + 1])
    return total


def print_result(graph: WeightedGraph, result: TSPResult, root: str) -> None:
    """
    按规格说明格式输出求解结果

    Args:
        graph: 带权完全图
        result: 求解结果
        root: 根节点名称
    """
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
