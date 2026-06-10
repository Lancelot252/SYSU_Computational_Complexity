"""
最小生成树算法

实现 Kruskal 算法计算带权完全图的最小生成树。
"""

from src.metric_tsp.models import Edge, WeightedGraph


class UnionFind:
    """
    并查集数据结构，用于 Kruskal 算法的连通性判断

    Attributes:
        parent: 父节点数组
        rank: 秩数组
    """

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        """查找根节点（带路径压缩）"""
        # TODO: 实现
        raise NotImplementedError

    def union(self, x: int, y: int) -> bool:
        """
        合并两个集合（按秩合并）

        Returns:
            是否成功合并（若已在同一集合则返回 False）
        """
        # TODO: 实现
        raise NotImplementedError


def kruskal(graph: WeightedGraph) -> list[Edge]:
    """
    Kruskal 算法计算最小生成树

    算法流程：
    1. 将所有边按权重从小到大排序
    2. 依次选取最短边，若该边不构成环则加入 MST
    3. 重复直到 MST 包含 n-1 条边

    Args:
        graph: 带权完全图

    Returns:
        MST 边列表
    """
    # TODO: 实现
    raise NotImplementedError


def mst_total_cost(mst_edges: list[Edge]) -> int:
    """
    计算 MST 总代价

    Args:
        mst_edges: MST 边列表

    Returns:
        MST 总代价
    """
    # TODO: 实现
    raise NotImplementedError
