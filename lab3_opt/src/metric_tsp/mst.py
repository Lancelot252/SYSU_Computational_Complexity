"""
Kruskal 最小生成树
"""

from typing import List
from src.metric_tsp.models import Edge, WeightedGraph


class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


def kruskal(graph: WeightedGraph) -> List[Edge]:
    city_to_idx = {name: i for i, name in enumerate(graph.city_names)}
    sorted_edges = sorted(graph.edges, key=lambda e: (e.weight, e.u, e.v))
    uf = UnionFind(graph.num_cities)
    mst_edges: List[Edge] = []

    for edge in sorted_edges:
        u_idx = city_to_idx[edge.u]
        v_idx = city_to_idx[edge.v]
        if uf.union(u_idx, v_idx):
            mst_edges.append(edge)
            if len(mst_edges) == graph.num_cities - 1:
                break

    return mst_edges


def mst_total_cost(mst_edges: List[Edge]) -> int:
    return sum(e.weight for e in mst_edges)
