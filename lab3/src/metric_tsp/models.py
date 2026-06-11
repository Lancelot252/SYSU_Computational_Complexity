"""
METRIC-TSP 数据模型

定义 METRIC-TSP 问题的核心数据结构，包括城市(City)和带权完全图(WeightedGraph)。
"""

from __future__ import annotations

import math


class City:
    """
    城市（顶点）

    Attributes:
        name: 城市名称
        x: 横坐标
        y: 纵坐标
    """

    def __init__(self, name: str, x: float, y: float) -> None:
        self.name = name
        self.x = x
        self.y = y

    def euclidean_distance(self, other: City) -> int:
        """
        计算与另一城市之间的欧氏距离（向上取整）

        c(u,v) = ⌈sqrt((x_u - x_v)^2 + (y_u - y_v)^2)⌉

        Args:
            other: 另一个城市

        Returns:
            取整后的欧氏距离
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return math.ceil(math.sqrt(dx * dx + dy * dy))

    def __repr__(self) -> str:
        return f"{self.name}({self.x}, {self.y})"


class Edge:
    """
    带权边

    Attributes:
        u: 端点1城市名
        v: 端点2城市名
        weight: 边权（欧氏距离取整）
    """

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
    """
    带权完全图

    根据城市坐标自动构造，边权为欧氏距离取整，满足三角不等式。

    Attributes:
        cities: 城市列表
        edges: 边列表
        adjacency: 邻接表 {城市名: [(邻居城市名, 边权), ...]}
        _weight_map: 边权映射 {(城市1, 城市2): 边权}
    """

    def __init__(self, cities: list[City]) -> None:
        self.cities = cities
        self.edges: list[Edge] = []
        self.adjacency: dict[str, list[tuple[str, int]]] = {c.name: [] for c in cities}
        self._weight_map: dict[tuple[str, str], int] = {}

        # 构造完全图
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
        """
        获取两个城市之间的边权

        Args:
            u: 城市1名称
            v: 城市2名称

        Returns:
            边权
        """
        return self._weight_map.get((u, v), 0)

    @property
    def city_names(self) -> list[str]:
        """所有城市名称列表"""
        return [c.name for c in self.cities]

    @property
    def num_cities(self) -> int:
        """城市数量"""
        return len(self.cities)
