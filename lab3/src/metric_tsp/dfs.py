"""
DFS 遍历最小生成树

从指定根节点开始对 MST 进行深度优先搜索遍历。
"""

from src.metric_tsp.models import Edge


def build_adjacency_list(edges: list[Edge]) -> dict[str, list[str]]:
    """
    根据边集构造无向图邻接表

    Args:
        edges: 边列表

    Returns:
        邻接表 {节点: [邻居列表]}
    """
    # TODO: 实现
    raise NotImplementedError


def dfs_traversal(
    edges: list[Edge],
    root: str,
) -> list[str]:
    """
    从根节点开始对 MST 进行 DFS 遍历

    Args:
        edges: MST 边列表
        root: 根节点名称

    Returns:
        DFS 首次访问顶点的顺序列表
    """
    # TODO: 实现
    raise NotImplementedError


def build_tsp_tour(dfs_order: list[str]) -> list[str]:
    """
    根据 DFS 遍历顺序构造 TSP 近似回路

    在 DFS 顺序末尾追加起点，形成闭合回路。
    例如：DFS顺序 [a, b, c, d] -> TSP回路 [a, b, c, d, a]

    Args:
        dfs_order: DFS 遍历顺序

    Returns:
        TSP 近似回路（闭合）
    """
    # TODO: 实现
    raise NotImplementedError
