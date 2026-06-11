"""
带权完全图构造

根据城市坐标文件构造满足三角不等式的带权完全图。
"""

from src.metric_tsp.models import City, WeightedGraph


def parse_cities(filepath: str) -> list[City]:
    """
    从 txt 文件解析城市坐标

    文件格式：
        每行一个城市：城市名 横坐标 纵坐标
        例如：a 0 0

    Args:
        filepath: 城市坐标文件路径

    Returns:
        城市列表
    """
    cities: list[City] = []
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

    # 检查坐标唯一性
    coords = [(c.x, c.y) for c in cities]
    if len(coords) != len(set(coords)):
        raise ValueError("不同城市不应具有完全相同的坐标")

    return cities


def build_complete_graph(cities: list[City]) -> WeightedGraph:
    """
    根据城市坐标构造带权完全图

    边权为欧氏距离向上取整，由此得到的完全图满足三角不等式。

    Args:
        cities: 城市列表

    Returns:
        构造好的带权完全图
    """
    return WeightedGraph(cities)
