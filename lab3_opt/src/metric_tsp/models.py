"""
METRIC-TSP 数据模型（副本）
"""

from __future__ import annotations

import math
from typing import List, Dict, Tuple


class City:
    def __init__(self, name: str, x: float, y: float) -> None:
        self.name = name
        self.x = x
        self.y = y

    def euclidean_distance(self, other: 'City') -> int:
        dx = self.x - other.x
        dy = self.y - other.y
        return math.ceil(math.sqrt(dx * dx + dy * dy))

    def __repr__(self) -> str:
        return f"{self.name}({self.x}, {self.y})"


class Edge:
    def __init__(self, u: str, v: str, weight: int) -> None:
        self.u = u
        self.v = v
        self.weight = weight

    def __repr__(self) -> str:
        return f"({self.u}, {self.v}, {self.weight})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Edge):
            return NotImplemented
        return self.u == other.u and self.v == other.v and self.weight == other.weight

    def __hash__(self) -> int:
        return hash((self.u, self.v, self.weight))


class WeightedGraph:
    def __init__(self, cities: List[City]) -> None:
        self.cities = cities
        self.edges: List[Edge] = []
        self.adjacency: Dict[str, List[Tuple[str, int]]] = {c.name: [] for c in cities}
        self._weight_map: Dict[Tuple[str, str], int] = {}

        for i in range(len(cities)):
            for j in range(i + 1, len(cities)):
                c1, c2 = cities[i], cities[j]
                w = c1.euclidean_distance(c2)
                edge = Edge(c1.name, c2.name, w)
                self.edges.append(edge)
                self.adjacency[c1.name].append((c2.name, w))
                self.adjacency[c2.name].append((c1.name, w))
                self._weight_map[(c1.name, c2.name)] = w
                self._weight_map[(c2.name, c1.name)] = w

    def get_weight(self, u: str, v: str) -> int:
        return self._weight_map.get((u, v), 0)

    @property
    def city_names(self) -> List[str]:
        return [c.name for c in self.cities]

    @property
    def num_cities(self) -> int:
        return len(self.cities)
