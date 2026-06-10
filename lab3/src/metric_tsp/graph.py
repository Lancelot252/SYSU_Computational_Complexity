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
    # TODO: 实现
    raise NotImplementedError


def build_complete_graph(cities: list[City]) -> WeightedGraph:
    """
    根据城市坐标构造带权完全图

    边权为欧氏距离向上取整，由此得到的完全图满足三角不等式。

    Args:
        cities: 城市列表

    Returns:
        构造好的带权完全图
    """
    # TODO: 实现
    raise NotImplementedError
