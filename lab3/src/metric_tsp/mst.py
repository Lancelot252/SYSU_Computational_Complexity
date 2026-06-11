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
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        合并两个集合（按秩合并）

        Returns:
            是否成功合并（若已在同一集合则返回 False）
        """
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


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
    # 建立城市名到索引的映射
    city_to_idx = {name: i for i, name in enumerate(graph.city_names)}

    # 按权重排序所有边
    sorted_edges = sorted(graph.edges, key=lambda e: (e.weight, e.u, e.v))

    uf = UnionFind(graph.num_cities)
    mst_edges: list[Edge] = []

    for edge in sorted_edges:
        u_idx = city_to_idx[edge.u]
        v_idx = city_to_idx[edge.v]
        if uf.union(u_idx, v_idx):
            mst_edges.append(edge)
            if len(mst_edges) == graph.num_cities - 1:
                break

    return mst_edges


def mst_total_cost(mst_edges: list[Edge]) -> int:
    """
    计算 MST 总代价

    Args:
        mst_edges: MST 边列表

    Returns:
        MST 总代价
    """
    return sum(e.weight for e in mst_edges)
