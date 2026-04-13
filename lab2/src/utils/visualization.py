"""
可视化工具

本模块提供图的可视化功能，使用matplotlib和networkx绘制图结构。
"""

from typing import Set, Optional, Dict, Any
import os
from ..models import Graph


def draw_graph(graph: Graph, output_path: Optional[str] = None, 
               title: Optional[str] = None, 
               figsize: tuple = (10, 8)) -> None:
    """
    使用matplotlib/networkx绘制图并保存
    
    Args:
        graph: 要绘制的图对象
        output_path: 输出文件路径，如果为None则显示图形
        title: 图标题
        figsize: 图形大小，默认为(10, 8)
        
    Raises:
        ImportError: 如果未安装必要的库
        
    Examples:
        >>> from src.models import Graph
        >>> graph = Graph()
        >>> node1 = graph.add_node("x")
        >>> node2 = graph.add_node("¬x")
        >>> graph.add_edge(node1, node2)
        >>> draw_graph(graph, "output.png", "示例图")
    """
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError(
            "需要安装networkx和matplotlib库:\n"
            "pip install networkx matplotlib"
        )
    
    # 转换为networkx图
    G = graph.to_networkx()
    
    # 创建图形
    fig, ax = plt.subplots(figsize=figsize)
    
    # 设置布局
    pos = nx.spring_layout(G, seed=42)
    
    # 获取节点标签
    labels = nx.get_node_attributes(G, 'label')
    
    # 绘制节点
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightblue', 
                          node_size=500, alpha=0.9)
    
    # 绘制边
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray', 
                          width=1.5, alpha=0.7)
    
    # 绘制标签
    nx.draw_networkx_labels(G, pos, labels, ax=ax, font_size=10)
    
    # 设置标题
    if title:
        ax.set_title(title, fontsize=14)
    
    # 移除坐标轴
    ax.axis('off')
    
    # 保存或显示
    if output_path:
        # 确保目录存在
        dir_path = os.path.dirname(output_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def draw_graph_with_highlight(graph: Graph, highlight_nodes: Set[int], 
                              output_path: Optional[str] = None,
                              title: Optional[str] = None,
                              highlight_color: str = 'red',
                              figsize: tuple = (10, 8)) -> None:
    """
    绘制图并高亮显示特定节点
    
    Args:
        graph: 要绘制的图对象
        highlight_nodes: 要高亮的节点集合
        output_path: 输出文件路径，如果为None则显示图形
        title: 图标题
        highlight_color: 高亮颜色，默认为红色
        figsize: 图形大小，默认为(10, 8)
        
    Raises:
        ImportError: 如果未安装必要的库
        
    Examples:
        >>> from src.models import Graph
        >>> graph = Graph()
        >>> nodes = [graph.add_node() for _ in range(4)]
        >>> graph.add_edge(nodes[0], nodes[1])
        >>> graph.add_edge(nodes[1], nodes[2])
        >>> graph.add_edge(nodes[2], nodes[3])
        >>> draw_graph_with_highlight(graph, {nodes[0], nodes[2]}, 
        ...                           "highlight.png", "独立集")
    """
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError(
            "需要安装networkx和matplotlib库:\n"
            "pip install networkx matplotlib"
        )
    
    # 转换为networkx图
    G = graph.to_networkx()
    
    # 创建图形
    fig, ax = plt.subplots(figsize=figsize)
    
    # 设置布局
    pos = nx.spring_layout(G, seed=42)
    
    # 获取节点标签
    labels = nx.get_node_attributes(G, 'label')
    
    # 分离高亮和非高亮节点
    normal_nodes = [n for n in G.nodes() if n not in highlight_nodes]
    highlighted_nodes = list(highlight_nodes)
    
    # 绘制普通节点
    if normal_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=normal_nodes, ax=ax,
                              node_color='lightblue', node_size=500, 
                              alpha=0.9)
    
    # 绘制高亮节点
    if highlighted_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=highlighted_nodes, ax=ax,
                              node_color=highlight_color, node_size=600,
                              alpha=0.9)
    
    # 绘制边
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray',
                          width=1.5, alpha=0.7)
    
    # 绘制标签
    nx.draw_networkx_labels(G, pos, labels, ax=ax, font_size=10)
    
    # 设置标题
    if title:
        ax.set_title(title, fontsize=14)
    
    # 移除坐标轴
    ax.axis('off')
    
    # 保存或显示
    if output_path:
        # 确保目录存在
        dir_path = os.path.dirname(output_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def draw_graph_with_vertex_cover(graph: Graph, vertex_cover: Set[int],
                                  output_path: Optional[str] = None,
                                  title: str = "Vertex Cover") -> None:
    """
    绘制图并显示顶点覆盖
    
    Args:
        graph: 要绘制的图对象
        vertex_cover: 顶点覆盖集合
        output_path: 输出文件路径
        title: 图标题，默认为"Vertex Cover"
    """
    draw_graph_with_highlight(graph, vertex_cover, output_path, 
                              title, highlight_color='green')


def draw_graph_with_independent_set(graph: Graph, independent_set: Set[int],
                                     output_path: Optional[str] = None,
                                     title: str = "Independent Set") -> None:
    """
    绘制图并显示独立集
    
    Args:
        graph: 要绘制的图对象
        independent_set: 独立集
        output_path: 输出文件路径
        title: 图标题，默认为"Independent Set"
    """
    draw_graph_with_highlight(graph, independent_set, output_path,
                              title, highlight_color='orange')


def draw_reduction_result(formula_str: str, graph: Graph, 
                          k_or_n: int, problem_type: str,
                          output_path: Optional[str] = None) -> None:
    """
    绘制归约结果
    
    显示原始公式和归约后的图。
    
    Args:
        formula_str: 原始公式字符串
        graph: 归约后的图
        k_or_n: 覆盖大小或独立集大小
        problem_type: 问题类型，"Vertex Cover" 或 "Independent Set"
        output_path: 输出文件路径
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError("需要安装matplotlib库: pip install matplotlib")
    
    # 创建图形
    fig = plt.figure(figsize=(12, 10))
    
    # 添加公式文本
    ax_text = fig.add_axes([0.1, 0.85, 0.8, 0.1])
    ax_text.axis('off')
    ax_text.text(0.5, 0.5, f"公式: {formula_str}", 
                fontsize=12, ha='center', va='center',
                transform=ax_text.transAxes)
    
    # 添加问题信息
    ax_info = fig.add_axes([0.1, 0.75, 0.8, 0.08])
    ax_info.axis('off')
    ax_info.text(0.5, 0.5, f"归约到 {problem_type}，大小 = {k_or_n}",
                fontsize=11, ha='center', va='center',
                transform=ax_info.transAxes)
    
    # 绘制图
    ax_graph = fig.add_axes([0.1, 0.1, 0.8, 0.6])
    draw_graph_on_axis(graph, ax_graph)
    
    # 保存或显示
    if output_path:
        dir_path = os.path.dirname(output_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def draw_graph_on_axis(graph: Graph, ax: Any) -> None:
    """
    在指定的轴上绘制图
    
    Args:
        graph: 要绘制的图对象
        ax: matplotlib轴对象
    """
    try:
        import networkx as nx
    except ImportError:
        raise ImportError("需要安装networkx库: pip install networkx")
    
    # 转换为networkx图
    G = graph.to_networkx()
    
    # 设置布局
    pos = nx.spring_layout(G, seed=42)
    
    # 获取节点标签
    labels = nx.get_node_attributes(G, 'label')
    
    # 绘制节点
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightblue',
                          node_size=500, alpha=0.9)
    
    # 绘制边
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray',
                          width=1.5, alpha=0.7)
    
    # 绘制标签
    nx.draw_networkx_labels(G, pos, labels, ax=ax, font_size=10)
    
    # 移除坐标轴
    ax.axis('off')


def create_comparison_plot(graph: Graph, 
                           vertex_cover: Optional[Set[int]] = None,
                           independent_set: Optional[Set[int]] = None,
                           output_path: Optional[str] = None) -> None:
    """
    创建对比图，同时显示顶点覆盖和独立集
    
    Args:
        graph: 要绘制的图对象
        vertex_cover: 顶点覆盖集合（可选）
        independent_set: 独立集（可选）
        output_path: 输出文件路径
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError("需要安装matplotlib库: pip install matplotlib")
    
    n_plots = 1 + (1 if vertex_cover else 0) + (1 if independent_set else 0)
    
    fig, axes = plt.subplots(1, n_plots, figsize=(5 * n_plots, 5))
    
    if n_plots == 1:
        axes = [axes]
    
    # 绘制原图
    draw_graph_on_axis(graph, axes[0])
    axes[0].set_title("原图")
    
    idx = 1
    
    # 绘制顶点覆盖
    if vertex_cover:
        draw_graph_with_highlight_on_axis(graph, vertex_cover, axes[idx],
                                          highlight_color='green')
        axes[idx].set_title(f"顶点覆盖 (k={len(vertex_cover)})")
        idx += 1
    
    # 绘制独立集
    if independent_set:
        draw_graph_with_highlight_on_axis(graph, independent_set, axes[idx],
                                          highlight_color='orange')
        axes[idx].set_title(f"独立集 (n={len(independent_set)})")
    
    plt.tight_layout()
    
    if output_path:
        dir_path = os.path.dirname(output_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def draw_graph_with_highlight_on_axis(graph: Graph, highlight_nodes: Set[int],
                                       ax: Any, 
                                       highlight_color: str = 'red') -> None:
    """
    在指定的轴上绘制图并高亮节点
    
    Args:
        graph: 要绘制的图对象
        highlight_nodes: 要高亮的节点集合
        ax: matplotlib轴对象
        highlight_color: 高亮颜色
    """
    try:
        import networkx as nx
    except ImportError:
        raise ImportError("需要安装networkx库: pip install networkx")
    
    # 转换为networkx图
    G = graph.to_networkx()
    
    # 设置布局
    pos = nx.spring_layout(G, seed=42)
    
    # 获取节点标签
    labels = nx.get_node_attributes(G, 'label')
    
    # 分离高亮和非高亮节点
    normal_nodes = [n for n in G.nodes() if n not in highlight_nodes]
    highlighted_nodes = list(highlight_nodes)
    
    # 绘制普通节点
    if normal_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=normal_nodes, ax=ax,
                              node_color='lightblue', node_size=500,
                              alpha=0.9)
    
    # 绘制高亮节点
    if highlighted_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=highlighted_nodes, ax=ax,
                              node_color=highlight_color, node_size=600,
                              alpha=0.9)
    
    # 绘制边
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray',
                          width=1.5, alpha=0.7)
    
    # 绘制标签
    nx.draw_networkx_labels(G, pos, labels, ax=ax, font_size=10)
    
    # 移除坐标轴
    ax.axis('off')