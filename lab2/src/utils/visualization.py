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


def draw_reduction_graph_spec(formula_str: str,
                               graph: Graph,
                               k_or_n: int,
                               problem_type: str,
                               clause_edges: list = None,
                               conflict_edges: list = None,
                               output_path: Optional[str] = None,
                               figsize: tuple = (12, 8)) -> None:
    """
    按照规格说明要求绘制归约结果图
    
    满足以下要求：
    1. 完整图结构：展示全部节点和全部边
    2. 圆形节点：节点绘制为圆形，标签包含子句编号和文字（如 C2:¬x）
    3. 边清晰可见：使用不同线型区分子句内部边和互补文字之间的边
    4. 问题文本描述：展示输入公式和所规约问题的文本
    
    Args:
        formula_str: 原始3SAT公式字符串
        graph: 归约后的图
        k_or_n: 覆盖大小k或独立集大小n
        problem_type: 问题类型，"Vertex Cover" 或 "Independent Set"
        clause_edges: 子句内部边的列表（用于区分线型）
        conflict_edges: 互补文字之间的边列表（用于区分线型）
        output_path: 输出文件路径
        figsize: 图形大小
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
    
    # 设置标题：显示原始公式
    ax.set_title(f"输入公式: {formula_str}", fontsize=14, pad=20)
    
    # 计算布局：使用分层布局使子句节点分组显示
    # 获取节点标签
    labels = nx.get_node_attributes(G, 'label')
    
    # 按子句分组计算位置
    pos = _calculate_clause_layout(G, labels)
    
    # 绘制子句内部边（实线，蓝色）
    if clause_edges:
        nx.draw_networkx_edges(
            G, pos, edgelist=clause_edges, ax=ax,
            edge_color='#3b82f6', width=1.6, style='solid',
            alpha=0.8
        )
    
    # 绘制互补文字边（虚线，红色）
    if conflict_edges:
        nx.draw_networkx_edges(
            G, pos, edgelist=conflict_edges, ax=ax,
            edge_color='#ef4444', width=1.2, style='dashed',
            alpha=0.7
        )
    
    # 如果没有区分边类型，绘制所有边
    if not clause_edges and not conflict_edges:
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray',
                              width=1.5, alpha=0.7)
    
    # 绘制圆形节点
    nx.draw_networkx_nodes(
        G, pos, ax=ax,
        node_shape='o',  # 圆形
        node_size=1400,
        node_color='#eef5ff',
        edgecolors='#1f2937',
        linewidths=1.2
    )
    
    # 绘制节点标签
    nx.draw_networkx_labels(G, pos, labels, ax=ax, font_size=10)
    
    # 移除坐标轴
    ax.axis('off')
    
    # 添加问题文本描述（底部）
    if problem_type == "Vertex Cover":
        problem_text = f"点覆盖：在上图中是否存在大小不超过 k = {k_or_n} 的点覆盖？"
    else:
        problem_text = f"独立集：在上图中是否存在大小至少为 n = {k_or_n} 的独立集？"
    
    fig.text(
        0.5, 0.04,
        problem_text,
        ha='center', va='bottom',
        fontsize=11,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#f0f0f0', alpha=0.8)
    )
    
    # 调整布局
    fig.subplots_adjust(bottom=0.12)
    
    # 保存或显示
    if output_path:
        dir_path = os.path.dirname(output_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
        fig.savefig(output_path, dpi=180, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()


def _calculate_clause_layout(G, labels: Dict[int, str]) -> Dict[int, tuple]:
    """
    计算按子句分组的节点布局
    
    使同一子句的节点聚集在一起，便于观察三角形结构。
    
    Args:
        G: networkx图对象
        labels: 节点标签字典
        
    Returns:
        节点位置字典
    """
    import networkx as nx
    import math
    
    # 从标签中提取子句编号
    clause_groups = {}
    for node_id, label in labels.items():
        # 标签格式如 "C1:x" 或 "C2:¬x"
        if ':' in label:
            clause_num = label.split(':')[0]  # 如 "C1"
            if clause_num not in clause_groups:
                clause_groups[clause_num] = []
            clause_groups[clause_num].append(node_id)
        else:
            # 如果标签没有子句编号，放入默认组
            if 'default' not in clause_groups:
                clause_groups['default'] = []
            clause_groups['default'].append(node_id)
    
    # 计算每个子句组的位置
    pos = {}
    num_clauses = len(clause_groups)
    
    # 子句组排列成圆形或水平排列
    if num_clauses <= 4:
        # 水平排列
        group_width = 3.0
        total_width = num_clauses * group_width
        start_x = -total_width / 2 + group_width / 2
        
        for i, (clause_name, nodes) in enumerate(clause_groups.items()):
            group_center_x = start_x + i * group_width
            group_center_y = 0
            
            # 子句内的3个节点排列成三角形
            num_nodes = len(nodes)
            if num_nodes == 3:
                # 三角形布局
                triangle_radius = 1.0
                for j, node_id in enumerate(nodes):
                    angle = j * 2 * math.pi / 3 - math.pi / 2  # 从顶部开始
                    x = group_center_x + triangle_radius * math.cos(angle)
                    y = group_center_y + triangle_radius * math.sin(angle)
                    pos[node_id] = (x, y)
            else:
                # 其他数量的节点，均匀排列
                for j, node_id in enumerate(nodes):
                    x = group_center_x + (j - num_nodes/2) * 0.8
                    y = group_center_y
                    pos[node_id] = (x, y)
    else:
        # 多个子句时，使用圆形排列
        radius = num_clauses * 0.8
        for i, (clause_name, nodes) in enumerate(clause_groups.items()):
            angle = i * 2 * math.pi / num_clauses
            group_center_x = radius * math.cos(angle)
            group_center_y = radius * math.sin(angle)
            
            # 子句内的节点排列成小三角形
            num_nodes = len(nodes)
            triangle_radius = 0.8
            for j, node_id in enumerate(nodes):
                node_angle = j * 2 * math.pi / 3 - math.pi / 2
                x = group_center_x + triangle_radius * math.cos(node_angle)
                y = group_center_y + triangle_radius * math.sin(node_angle)
                pos[node_id] = (x, y)
    
    # 如果有默认组的节点，使用spring_layout
    if 'default' in clause_groups:
        remaining_pos = nx.spring_layout(G, pos=pos, fixed=pos.keys(), seed=42)
        pos.update(remaining_pos)
    
    return pos


def format_node_label(clause_index: int, literal_str: str) -> str:
    """
    格式化节点标签，符合规格说明要求
    
    Args:
        clause_index: 子句编号（从1开始）
        literal_str: 文字字符串，如 "x" 或 "¬x"
        
    Returns:
        格式化的标签，如 "C1:x" 或 "C2:¬x"
    """
    return f"C{clause_index}:{literal_str}"