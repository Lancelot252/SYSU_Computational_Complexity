"""
副本：带权完全图构造
"""

from typing import List
from src.metric_tsp.models import City, WeightedGraph


def parse_cities(filepath: str) -> List[City]:
    cities: List[City] = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) != 3:
                raise ValueError(f"城市行格式错误，需要3项（名称 x y）: '{line}'")
            name = parts[0]
            try:
                x = float(parts[1])
                y = float(parts[2])
            except ValueError:
                raise ValueError(f"坐标必须为数字: '{line}'")
            cities.append(City(name, x, y))

    if len(cities) < 6:
        raise ValueError(f"至少需要6个城市，当前只有 {len(cities)} 个")

    coords = [(c.x, c.y) for c in cities]
    if len(coords) != len(set(coords)):
        raise ValueError("不同城市不应具有完全相同的坐标")

    return cities


def build_complete_graph(cities: List[City]) -> WeightedGraph:
    return WeightedGraph(cities)
