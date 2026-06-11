"""
DFS 遍历
"""

from typing import List, Dict
from src.metric_tsp.models import Edge


def build_adjacency_list(edges: List[Edge]) -> Dict[str, List[str]]:
    adj: Dict[str, List[str]] = {}
    for edge in edges:
        adj.setdefault(edge.u, []).append(edge.v)
        adj.setdefault(edge.v, []).append(edge.u)
    for key in adj:
        adj[key].sort()
    return adj


def dfs_traversal(edges: List[Edge], root: str) -> List[str]:
    adj = build_adjacency_list(edges)
    visited: set[str] = set()
    order: List[str] = []

    def _dfs(node: str) -> None:
        visited.add(node)
        order.append(node)
        for neighbor in adj.get(node, []):
            if neighbor not in visited:
                _dfs(neighbor)

    _dfs(root)
    return order


def build_tsp_tour(dfs_order: List[str]) -> List[str]:
    return dfs_order + [dfs_order[0]]
