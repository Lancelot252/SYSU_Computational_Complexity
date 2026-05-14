"""
测试3SAT到节点覆盖的归约

本模块测试reduce_3sat_to_vertex_cover和相关函数的正确性。
"""

import unittest
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import Formula3SAT, Graph, Literal, Clause
from src.parsers import parse_cnf_string
from src.reductions.vertex_cover import (
    reduce_3sat_to_vertex_cover,
    verify_vertex_cover_reduction,
    extract_satisfying_assignment
)


class TestReduce3SATToVertexCover(unittest.TestCase):
    """测试3SAT到节点覆盖的归约主函数"""
    
    def test_basic_reduction(self):
        """测试基本归约"""
        formula = parse_cnf_string("(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)")
        graph, k = reduce_3sat_to_vertex_cover(formula)
        
        # 2个子句 => 6个节点
        self.assertEqual(graph.node_count(), 6)
        # 每个三角形3条边 => 2*3=6条内部边 + 可能的冲突边
        # 变量x, y, z各有正负文字在不同子句，因此有3条冲突边
        # 总边数 = 6 + 3 = 9
        self.assertEqual(graph.edge_count(), 9)
        # 覆盖大小 k = 2m = 4
        self.assertEqual(k, 4)
    
    def test_course_example(self):
        """测试课件例子 (x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z) ∧ (¬x ∨ y ∨ ¬z)"""
        from tests.test_cases import get_course_example
        formula = get_course_example()
        graph, k = reduce_3sat_to_vertex_cover(formula)
        
        # 3个子句 => 9个节点
        self.assertEqual(graph.node_count(), 9)
        # 覆盖大小 k = 2*3 = 6
        self.assertEqual(k, 6)
        
        # 验证节点标签
        labels = graph.get_node_labels()
        for node_id, label in labels.items():
            # 标签格式为 "C{子句编号}:{文字}"
            self.assertTrue(label.startswith('C'))
    
    def test_simple_sat(self):
        """测试简单可满足公式 (x ∨ y ∨ z)"""
        from tests.test_cases import get_simple_sat
        formula = get_simple_sat()
        graph, k = reduce_3sat_to_vertex_cover(formula)
        
        # 1个子句 => 3个节点
        self.assertEqual(graph.node_count(), 3)
        self.assertEqual(k, 2)
        # 只有三角形内部的3条边
        self.assertEqual(graph.edge_count(), 3)
    
    def test_custom_example(self):
        """测试自定义例子（6个子句）"""
        from tests.test_cases import get_custom_example
        formula = get_custom_example()
        graph, k = reduce_3sat_to_vertex_cover(formula)
        
        # 6个子句 => 18个节点
        self.assertEqual(graph.node_count(), 18)
        # 覆盖大小 k = 2*6 = 12
        self.assertEqual(k, 12)
    
    def test_verify_triangle_structure(self):
        """验证每个子句确实形成了三角形"""
        formula = parse_cnf_string("(x ∨ y ∨ z) ∧ (¬x ∨ ¬y ∨ ¬z)")
        graph, k = reduce_3sat_to_vertex_cover(formula)
        
        # 验证每个子句形成三角形
        for i in range(2):
            base = i * 3
            self.assertTrue(graph.has_edge(base, base + 1))
            self.assertTrue(graph.has_edge(base + 1, base + 2))
            self.assertTrue(graph.has_edge(base, base + 2))
    
    def test_conflict_edges(self):
        """验证冲突边是否正确添加"""
        formula = parse_cnf_string("(x ∨ y ∨ z) ∧ (¬x ∨ ¬y ∨ ¬z)")
        graph, k = reduce_3sat_to_vertex_cover(formula)
        
        # x和¬x之间应有边（节点0和节点3）
        self.assertTrue(graph.has_edge(0, 3))
        # y和¬y之间应有边（节点1和节点4）
        self.assertTrue(graph.has_edge(1, 4))
        # z和¬z之间应有边（节点2和节点5）
        self.assertTrue(graph.has_edge(2, 5))


class TestVerifyVertexCoverReduction(unittest.TestCase):
    """测试归约验证函数"""
    
    def test_verify_correct_reduction(self):
        """验证正确归约"""
        formula = parse_cnf_string("(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)")
        graph, k = reduce_3sat_to_vertex_cover(formula)
        
        result = verify_vertex_cover_reduction(formula, graph, k)
        self.assertTrue(result)
    
    def test_verify_wrong_k(self):
        """验证错误的k"""
        formula = parse_cnf_string("(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)")
        graph, k = reduce_3sat_to_vertex_cover(formula)
        
        result = verify_vertex_cover_reduction(formula, graph, k + 1)
        self.assertFalse(result)
        
        result = verify_vertex_cover_reduction(formula, graph, k - 1)
        self.assertFalse(result)
    
    def test_verify_wrong_node_count(self):
        """验证错误的节点数（修改图）"""
        formula = parse_cnf_string("(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)")
        graph, k = reduce_3sat_to_vertex_cover(formula)
        
        # 添加额外节点
        graph.add_node("extra")
        
        result = verify_vertex_cover_reduction(formula, graph, k)
        self.assertFalse(result)
    
    def test_verify_course_example(self):
        """验证课件例子"""
        from tests.test_cases import get_course_example
        formula = get_course_example()
        graph, k = reduce_3sat_to_vertex_cover(formula)
        
        result = verify_vertex_cover_reduction(formula, graph, k)
        self.assertTrue(result)


class TestExtractSatisfyingAssignment(unittest.TestCase):
    """测试从节点覆盖解中提取满足赋值"""
    
    def test_extract_simple(self):
        """测试简单公式的赋值提取"""
        formula = parse_cnf_string("(x ∨ y ∨ z)")
        graph, k = reduce_3sat_to_vertex_cover(formula)
        
        # 对于单子句，覆盖大小为2，即选择2个节点
        # 未被选中的节点对应的文字为真
        vertex_cover = {0, 1}  # 选择x和y节点
        assignment = extract_satisfying_assignment(formula, graph, vertex_cover)
        
        # 节点2（z）不在覆盖中，所以z为True
        self.assertTrue(assignment.get('z', False))
    
    def test_extract_with_negation(self):
        """测试包含否定文字的赋值提取"""
        formula = parse_cnf_string("(¬x ∨ y ∨ z)")
        graph, k = reduce_3sat_to_vertex_cover(formula)
        
        # 选择节点1和2（y和z），留下节点0（¬x）不在覆盖中
        vertex_cover = {1, 2}
        assignment = extract_satisfying_assignment(formula, graph, vertex_cover)
        
        # ¬x为真，所以x为False
        self.assertFalse(assignment.get('x', True))


def generate_output_images():
    """生成用于报告的输出图片"""
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')
    import networkx as nx
    import io
    
    # 设置stdout编码为UTF-8，解决Windows终端中文显示问题
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # 配置中文字体
    plt.rcParams['font.sans-serif'] = ['DengXian', 'Microsoft YaHei', 'SimHei', 'FangSong', 'KaiTi']
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    def get_triangle_positions(num_clauses):
        """
        为每个三角形生成固定布局坐标
        每个三角形的3个节点在同一水平线上，等间距排列
        三角形之间有一定间距
        
        返回: {node_id: (x, y)}
        """
        positions = {}
        # 每个三角形的宽度（节点间水平间距）
        intra_gap = 1.5
        # 三角形之间的间距
        inter_gap = 3.0
        
        for clause_idx in range(num_clauses):
            # 三角形的中心x坐标
            center_x = clause_idx * (intra_gap * 2 + inter_gap)
            base_y = 0  # 所有三角形在同一水平线
            
            # 三个节点：左、中、右，在同一水平线上
            # 但为了看起来像三角形，把中间节点稍微抬高一点
            node_positions = [
                (center_x - intra_gap, base_y),           # 左节点
                (center_x, base_y + 1.0),                 # 中节点（抬高一点形成三角形视觉）
                (center_x + intra_gap, base_y),           # 右节点
            ]
            
            for i, (x, y) in enumerate(node_positions):
                node_id = clause_idx * 3 + i
                positions[node_id] = (x, y)
        
        return positions
    
    def get_node_clause_info_from_graph(graph, formula):
        """
        从图和公式中提取节点信息
        返回: {node_id: (clause_idx, lit_str)}
        """
        info = {}
        labels = graph.get_node_labels()
        
        for node_id, label in labels.items():
            # 标签格式为 "C{子句编号}:{文字}"
            if ':' in label:
                parts = label.split(':')
                clause_idx = int(parts[0][1:]) - 1  # 去掉'C'并转为0-based索引
                lit_str = parts[1]
                info[node_id] = (clause_idx, lit_str)
        
        return info
    
    def draw_reduction_picture(formula, filename, description=""):
        """绘制归约结果图片，符合PDF输出规范"""
        graph, k = reduce_3sat_to_vertex_cover(formula)
        node_clause_info = get_node_clause_info_from_graph(graph, formula)
        
        # 构造公式字符串
        formula_str = " ∧ ".join(
            "(" + " ∨ ".join(str(lit) for lit in clause) + ")"
            for clause in formula
        )
        
        # ==================== 终端输出实例信息 ====================
        print("\n" + "=" * 70)
        print(f"【{description}】")
        print("=" * 70)
        print(f"3SAT公式: {formula_str}")
        print(f"子句数 m = {len(formula)}")
        print(f"变量集: {sorted(formula.get_variables())}")
        print("-" * 70)
        print(f"归约结果:")
        print(f"  节点数 |V| = {graph.node_count()} (应为 3m = {3 * len(formula)})")
        print(f"  边数 |E| = {graph.edge_count()}")
        print(f"  覆盖大小 k = {k} (应为 2m = {2 * len(formula)})")
        print("-" * 70)
        
        # 输出节点信息
        labels = graph.get_node_labels()
        print("节点列表:")
        for node_id in sorted(labels.keys()):
            clause_idx, lit_str = node_clause_info.get(node_id, (None, str(labels[node_id])))
            if clause_idx is not None:
                print(f"  节点{node_id}: 子句{clause_idx + 1}的文字 '{lit_str}'")
            else:
                print(f"  节点{node_id}: {labels[node_id]}")
        
        print("-" * 70)
        
        # 区分并输出边信息
        triangle_edges = []
        conflict_edges = []
        for u, v in graph.edges():
            u_info = node_clause_info.get(u)
            v_info = node_clause_info.get(v)
            if u_info is not None and v_info is not None:
                if u_info[0] == v_info[0]:
                    triangle_edges.append((u, v))
                else:
                    conflict_edges.append((u, v, u_info[1], v_info[1]))
        
        print("三角形内部边（同一子句内的边）:")
        for u, v in triangle_edges:
            u_info = node_clause_info.get(u, (None, str(labels.get(u, u))))
            v_info = node_clause_info.get(v, (None, str(labels.get(v, v))))
            print(f"  ({u}, {v}): {u_info[1]} -- {v_info[1]} [子句{u_info[0]+1}]")
        
        print("-" * 70)
        print("冲突边（互补文字之间的边）:")
        for u, v, u_lit, v_lit in conflict_edges:
            print(f"  ({u}, {v}): {u_lit} -- {v_lit}")
        
        print("-" * 70)
        print("三角形结构验证:")
        for i in range(len(formula)):
            base = i * 3
            edges_in_triangle = [(u, v) for u, v in triangle_edges
                                  if u >= base and u < base + 3 and v >= base and v < base + 3]
            print(f"  子句{i+1} (节点{base},{base+1},{base+2}): {len(edges_in_triangle)}条内部边")
        
        print("=" * 70)
        # ==================== 终端输出结束 ====================
        
        # 如果description不为空，在前面添加标题
        if description:
            display_text = description + "\n" + formula_str
        else:
            display_text = "3SAT公式:\n" + formula_str
        
        G = graph.to_networkx()
        
        # 使用手动布局，每个三角形等大小且在同一水平线上
        pos = get_triangle_positions(len(formula))
        
        # 没有在布局中的节点（如果有的话）用spring_layout
        missing_nodes = [n for n in G.nodes() if n not in pos]
        if missing_nodes:
            spring_pos = nx.spring_layout(
                nx.subgraph(G, missing_nodes), seed=42, k=1.0, center=(0, 0)
            )
            pos.update(spring_pos)
        
        # 节点标签：C{子句编号}:{文字}
        node_labels = {}
        for node_id in G.nodes():
            if node_id in node_clause_info:
                clause_idx, lit_str = node_clause_info[node_id]
                node_labels[node_id] = f"C{clause_idx + 1}:{lit_str}"
            else:
                node_labels[node_id] = str(node_id)
        
        # 区分内部边(实线)和冲突边(曲线)
        triangle_edges = []
        conflict_edges = []  # (u, v, var_name)
        for u, v in graph.edges():
            u_info = node_clause_info.get(u)
            v_info = node_clause_info.get(v)
            if u_info is not None and v_info is not None:
                if u_info[0] == v_info[0]:
                    triangle_edges.append((u, v))
                else:
                    # 提取变量名（去掉可能的¬前缀）
                    u_lit = u_info[1]
                    v_lit = v_info[1]
                    var_name = u_lit[1:] if u_lit.startswith('¬') else u_lit
                    conflict_edges.append((u, v, var_name))
            else:
                triangle_edges.append((u, v))
        
        # 冲突边颜色映射：每个变量一种颜色
        conflict_var_colors = {
            'x': '#e41a1c',  # 红
            'y': '#377eb8',  # 蓝
            'z': '#4daf4a',  # 绿
            'w': '#984ea3',  # 紫
            'u': '#ff7f00',  # 橙
            'v': '#a65628',  # 棕
        }
        
        # 绘图
        fig = plt.figure(figsize=(14, 10))
        
        # 公式显示
        ax_formula = fig.add_axes([0.05, 0.88, 0.9, 0.08])
        ax_formula.axis('off')

        ax_formula.axis('off')
        ax_formula.text(0.5, 0.5, display_text,
                        fontsize=12, ha='center', va='center',
                        transform=ax_formula.transAxes,
                        bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow"))
        
        # 问题描述
        ax_desc = fig.add_axes([0.05, 0.80, 0.9, 0.06])
        ax_desc.axis('off')
        ax_desc.text(0.5, 0.5,
                     f"节点覆盖：在上图中是否存在大小不超过 k = {k} 的节点覆盖？",
                     fontsize=14, ha='center', va='center',
                     transform=ax_desc.transAxes, color='darkred',
                     fontweight='bold')
        
        # 图形区域
        ax_graph = fig.add_axes([0.05, 0.05, 0.9, 0.72])
        
        # 第一步：先绘制冲突边（曲线，在节点下层）
        from matplotlib.patches import FancyArrowPatch
        import math
        
        for u, v, var_name in conflict_edges:
            if u in pos and v in pos:
                x1, y1 = pos[u]
                x2, y2 = pos[v]
                dx = x2 - x1
                dy = y2 - y1
                dist = math.sqrt(dx*dx + dy*dy)
                if dist > 0.01:
                    color = conflict_var_colors.get(var_name, 'gray')
                    # 根据y坐标判断：上面的弧线向上拱(rad正)，下面的向下拱(rad负)
                    mid_y = (y1 + y2) / 2
                    if abs(dx) > abs(dy):
                        # 水平方向为主的边，加大弧度避开中间节点
                        if mid_y > 0.3:
                            rad = 0.6  # 上面的边向上拱，加大弧度
                        else:
                            rad = -0.6  # 下面的边向下拱，加大弧度
                    else:
                        # 垂直方向为主的边
                        if mid_y > 0.3:
                            rad = 0.5
                        else:
                            rad = -0.5
                    arrow = FancyArrowPatch(
                        (x1, y1), (x2, y2),
                        connectionstyle=f"arc3,rad={rad}",
                        color=color, linewidth=2.0, alpha=0.8,
                        linestyle='dashed',
                        arrowstyle='-'
                    )
                    ax_graph.add_patch(arrow)
        
        # 第二步：绘制三角形内部边（实线，深灰色）
        if triangle_edges:
            nx.draw_networkx_edges(G, pos, edgelist=triangle_edges, ax=ax_graph,
                                   edge_color='#555555', width=2.0, alpha=0.8,
                                   style='solid')
        
        # 绘制圆形节点
        nx.draw_networkx_nodes(G, pos, ax=ax_graph,
                               node_color='lightgreen', node_size=700,
                               alpha=0.95, node_shape='o',
                               edgecolors='darkgreen', linewidths=1.5)
        
        # 标签
        nx.draw_networkx_labels(G, pos, labels=node_labels, ax=ax_graph,
                                font_size=10, font_weight='bold')
        
        # 图例
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], color='#555555', lw=2.0, linestyle='-',
                   label='子句内部边（三角形）'),
        ]
        # 每种变量的冲突边一种颜色
        used_vars = sorted(set(var for _, _, var in conflict_edges))
        for var_name in used_vars:
            color = conflict_var_colors.get(var_name, 'gray')
            legend_elements.append(
                Line2D([0], [0], color=color, lw=2.0, linestyle='--',
                       label=f'{var_name}-¬{var_name} 冲突边')
            )
        ax_graph.legend(handles=legend_elements, loc='lower left', fontsize=10,
                        framealpha=0.9)
        
        ax_graph.set_title("3SAT → Vertex Cover 归约结果", fontsize=15, fontweight='bold', pad=15)
        ax_graph.axis('off')
        # 调整坐标范围使图在中间
        ax_graph.autoscale_view()
        
        # 保存
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"图片已保存: {filepath}")
    
    # === 测试用例1：课件测试用例 ===
    print("测试用例1：课件测试用例")
    from tests.test_cases import get_course_example
    formula1 = get_course_example()
    draw_reduction_picture(
        formula1,
        "task1_course_example_vertex_cover.png",
        "测试用例1（课件例子）："
    )
    
    # === 测试用例2：自行设计测试用例（至少5个子句）===
    print("\n测试用例2：自行设计测试用例（6个子句）")
    from tests.test_cases import get_custom_example
    formula2 = get_custom_example()
    draw_reduction_picture(
        formula2,
        "task1_custom_example_vertex_cover.png",
        "测试用例2（自行设计，6个子句）："
    )
    
    print("\n所有图片生成完毕！请在 output 目录中查看。")


if __name__ == '__main__':
    # 直接运行本文件时，生成展示图片
    generate_output_images()
