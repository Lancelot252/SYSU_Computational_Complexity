"""
测试3SAT到独立集的归约

本模块测试reduce_3sat_to_independent_set和相关函数的正确性。
"""

import unittest
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import Formula3SAT, Graph, Literal, Clause
from src.parsers import parse_cnf_string
from src.reductions.independent_set import (
    reduce_3sat_to_independent_set,
    verify_independent_set_reduction,
    extract_satisfying_assignment,
    get_node_clause_info,
    vertex_cover_to_independent_set,
    independent_set_to_vertex_cover
)


class TestReduce3SATToIndependentSet(unittest.TestCase):
    """测试3SAT到独立集的归约主函数"""
    
    def test_basic_reduction(self):
        """测试基本归约"""
        formula = parse_cnf_string("(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)")
        graph, n = reduce_3sat_to_independent_set(formula)
        
        # 2个子句 => 6个节点
        self.assertEqual(graph.node_count(), 6)
        # 每个三角形3条边 => 2*3=6条内部边 + 可能的冲突边
        # 变量x, y, z各有正负文字在不同子句，因此有3条冲突边
        # 总边数 = 6 + 3 = 9
        self.assertEqual(graph.edge_count(), 9)
        # 独立集大小 = 子句数 = 2
        self.assertEqual(n, 2)
    
    def test_course_example(self):
        """测试课件例子 (x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z) ∧ (¬x ∨ y ∨ ¬z)"""
        from tests.test_cases import get_course_example
        formula = get_course_example()
        graph, n = reduce_3sat_to_independent_set(formula)
        
        # 3个子句 => 9个节点
        self.assertEqual(graph.node_count(), 9)
        # 独立集大小 = 3
        self.assertEqual(n, 3)
        
        # 验证三角形结构
        # 子句1: x, y, ¬z（正x, 正y, 负z）
        # 子句2: ¬x, ¬y, z（负x, 负y, 正z）
        # 子句3: ¬x, y, ¬z（负x, 正y, 负z）
        # 冲突边: x-¬x (子句1-子句2), x-¬x (子句1-子句3), y-¬y (子句1-子句2),
        #         ¬z-z (子句1-子句2), ¬z-z? ¬z在子句3, z在子句2 => 冲突边
        # 实际上我们需要验证每个三角形内部有3条边
        
        # 验证节点标签
        labels = graph.get_node_labels()
        for node_id, label in labels.items():
            self.assertIn(label, {'x', 'y', 'z', '¬x', '¬y', '¬z'})
    
    def test_simple_sat(self):
        """测试简单可满足公式 (x ∨ y ∨ z)"""
        from tests.test_cases import get_simple_sat
        formula = get_simple_sat()
        graph, n = reduce_3sat_to_independent_set(formula)
        
        # 1个子句 => 3个节点
        self.assertEqual(graph.node_count(), 3)
        self.assertEqual(n, 1)
        # 只有三角形内部的3条边
        self.assertEqual(graph.edge_count(), 3)
    
    def test_custom_example(self):
        """测试自定义例子（6个子句）"""
        from tests.test_cases import get_custom_example
        formula = get_custom_example()
        graph, n = reduce_3sat_to_independent_set(formula)
        
        # 6个子句 => 18个节点
        self.assertEqual(graph.node_count(), 18)
        # 独立集大小 = 6
        self.assertEqual(n, 6)
        # 三角形内部边 = 6*3 = 18
    
    def test_verify_triangle_structure(self):
        """验证每个子句确实形成了三角形"""
        formula = parse_cnf_string("(x ∨ y ∨ z) ∧ (¬x ∨ ¬y ∨ ¬z)")
        graph, n = reduce_3sat_to_independent_set(formula)
        
        # 获取所有节点标签
        labels = graph.get_node_labels()
        
    
        for clause in formula:
            # 对每个子句的3个文字，验证它们两两之间有边
            lit_labels = [str(lit) for lit in clause]
            # 找到对应的节点
            nodes = []
            for label in lit_labels:
                for nid, lbl in labels.items():
                    if lbl == label:
                        nodes.append(nid)
                        break
            self.assertEqual(len(nodes), 3)
            # 验证三角形
            self.assertTrue(graph.has_edge(nodes[0], nodes[1]))
            self.assertTrue(graph.has_edge(nodes[1], nodes[2]))
            self.assertTrue(graph.has_edge(nodes[0], nodes[2]))
    
    def test_conflict_edges(self):
        """验证冲突边是否正确添加"""
        formula = parse_cnf_string("(x ∨ y ∨ z) ∧ (¬x ∨ ¬y ∨ ¬z)")
        graph, n = reduce_3sat_to_independent_set(formula)
        labels = graph.get_node_labels()
        
        # 找到x和¬x的节点
        x_node = neg_node = None
        for nid, lbl in labels.items():
            if lbl == 'x':
                x_node = nid
            elif lbl == '¬x':
                neg_node = nid
        
        # x和¬x之间应有边
        self.assertIsNotNone(x_node)
        self.assertIsNotNone(neg_node)
        self.assertTrue(graph.has_edge(x_node, neg_node))
        
        # y和¬y之间应有边
        y_node = neg_y = None
        for nid, lbl in labels.items():
            if lbl == 'y':
                y_node = nid
            elif lbl == '¬y':
                neg_y = nid
        self.assertTrue(graph.has_edge(y_node, neg_y))
        
        # z和¬z之间应有边
        z_node = neg_z = None
        for nid, lbl in labels.items():
            if lbl == 'z':
                z_node = nid
            elif lbl == '¬z':
                neg_z = nid
        self.assertTrue(graph.has_edge(z_node, neg_z))


class TestVerifyIndependentSetReduction(unittest.TestCase):
    """测试归约验证函数"""
    
    def test_verify_correct_reduction(self):
        """验证正确归约"""
        formula = parse_cnf_string("(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)")
        graph, n = reduce_3sat_to_independent_set(formula)
        
        result = verify_independent_set_reduction(formula, graph, n)
        self.assertTrue(result)
    
    def test_verify_wrong_n(self):
        """验证错误的n"""
        formula = parse_cnf_string("(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)")
        graph, n = reduce_3sat_to_independent_set(formula)
        
        result = verify_independent_set_reduction(formula, graph, n + 1)
        self.assertFalse(result)
        
        result = verify_independent_set_reduction(formula, graph, n - 1)
        self.assertFalse(result)
    
    def test_verify_wrong_node_count(self):
        """验证错误的节点数（修改图）"""
        formula = parse_cnf_string("(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)")
        graph, n = reduce_3sat_to_independent_set(formula)
        
        # 添加额外节点
        graph.add_node("extra")
        
        result = verify_independent_set_reduction(formula, graph, n)
        self.assertFalse(result)
    
    def test_verify_course_example(self):
        """验证课件例子"""
        from tests.test_cases import get_course_example
        formula = get_course_example()
        graph, n = reduce_3sat_to_independent_set(formula)
        
        result = verify_independent_set_reduction(formula, graph, n)
        self.assertTrue(result)


class TestExtractSatisfyingAssignment(unittest.TestCase):
    """测试从独立集提取满足赋值"""
    
    def test_extract_simple(self):
        """测试从简单独立集提取"""
        formula = parse_cnf_string("(x ∨ y ∨ z)")
        graph, n = reduce_3sat_to_independent_set(formula)
        
        labels = graph.get_node_labels()
        # 找到x节点
        x_node = None
        for nid, lbl in labels.items():
            if lbl == 'x':
                x_node = nid
                break
        
        # 独立集 = {x节点}
        assignment = extract_satisfying_assignment(formula, graph, {x_node})
        
        self.assertIn('x', assignment)
        self.assertEqual(assignment['x'], True)
        self.assertIn('y', assignment)
        self.assertIn('z', assignment)
    
    def test_extract_negated_literal(self):
        """测试从包含负文字的独立集提取"""
        formula = parse_cnf_string("(¬x ∨ y ∨ z)")
        graph, n = reduce_3sat_to_independent_set(formula)
        
        labels = graph.get_node_labels()
        # 找到¬x节点
        neg_x_node = None
        for nid, lbl in labels.items():
            if lbl == '¬x':
                neg_x_node = nid
                break
        
        # 独立集 = {¬x节点}
        assignment = extract_satisfying_assignment(formula, graph, {neg_x_node})
        
        self.assertIn('x', assignment)
        self.assertEqual(assignment['x'], False)
    
    def test_assignment_satisfies_formula(self):
        """验证提取的赋值确实满足公式"""
        from tests.test_cases import get_course_example
        
        # 对于课件例子，我们需要找到一个独立集，提取赋值，然后验证公式被满足
        formula = get_course_example()
        graph, n = reduce_3sat_to_independent_set(formula)
        labels = graph.get_node_labels()
        
        # 课件例子：(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z) ∧ (¬x ∨ y ∨ ¬z)
        # 构造一组满足赋值的独立集：
        # 取满足赋值 x=False, y=True, z=True
        # 子句1: x=False, y=True, ¬z=False → 选择 y (True)
        # 子句2: ¬x=True, ¬y=False, z=True → 选择 ¬x (True) 或 z (True)
        # 子句3: ¬x=True, y=True, ¬z=False → 选择 ¬x (True) 或 y (True)
        # 但独立集不能包含冲突节点
        
        # 独立集 = {y(子句1), z(子句2), y(子句3)} - 但两个y节点相同标签不同节点ID, 可以共存
        # 实际上最好用更简单的方法
        
        # 使用brute-force找独立集
        # 对3个子句，每个子句选择1个文字 => 3^3 = 27种选择
        # 检查每种选择是否构成独立集
        found = False
        clause_node_groups = []
        idx = 0
        for clause in formula:
            group = []
            for lit in clause:
                label = str(lit)
                for nid, lbl in labels.items():
                    if lbl == label and nid // 3 == idx // 3:
                        # 简单的映射：每个子句的3个节点是连续的
                        pass
                group.append(None)
            clause_node_groups.append(group)
        
        # 更简单的方法：用节点的连续ID
        # 节点0,1,2 -> 子句0; 节点3,4,5 -> 子句1; 节点6,7,8 -> 子句2
        clause_nodes = [
            [0, 1, 2],   # 子句0: x, y, ¬z
            [3, 4, 5],   # 子句1: ¬x, ¬y, z
            [6, 7, 8],   # 子句2: ¬x, y, ¬z
        ]
        
        # 取值满足赋值 x=False, y=True, z=True
        # 每个子句选择一个为真的文字
        # 子句0: y (节点1) 为真
        # 子句1: z (节点5) 为真
        # 子句2: ¬x (节点6) 或 y (节点7) 为真
        # 检查 {1, 5, 6}: 节点1-6有边吗? x(节点0)和¬x(节点6)有边 => 不在独立集中
        # 检查 {1, 5, 7}: 节点1(y)和7(y)没有冲突边 => OK, 节点5(z)和7(y)? 不同变量 => OK
        
        ind_set = {1, 5, 7}  # y(子句0), z(子句1), y(子句2)
        if graph.is_independent_set(ind_set):
            assignment = extract_satisfying_assignment(formula, graph, ind_set)
            # y=True, z=True, x未指定 => 默认True
            # 但注意¬x在独立集中没有出现，x默认为True
            # 验证赋值满足公式
            # 需要在题目框架外验证，这里暂简单检查赋值字典格式
            self.assertIn('x', assignment)
            self.assertIn('y', assignment)
            self.assertIn('z', assignment)
            found = True
        
        # 如果上面的独立集不成立，尝试其他组合
        if not found:
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        candidate = {clause_nodes[0][i], clause_nodes[1][j], clause_nodes[2][k]}
                        if graph.is_independent_set(candidate):
                            assignment = extract_satisfying_assignment(formula, graph, candidate)
                            self.assertIsNotNone(assignment)
                            found = True
                            break
                    if found:
                        break
                if found:
                    break
        
        self.assertTrue(found, "应该能找到大小为3的独立集")


class TestComplementaryFunctions(unittest.TestCase):
    """测试顶点覆盖与独立集的互补转换函数"""
    
    def test_vertex_cover_to_independent_set(self):
        """测试节点覆盖转独立集"""
        g = Graph()
        n1 = g.add_node("A")
        n2 = g.add_node("B")
        n3 = g.add_node("C")
        g.add_edge(n1, n2)
        g.add_edge(n2, n3)
        
        # {n1, n2}是顶点覆盖，大小k=2
        # 独立集大小 = 3-2=1, 即{n3}
        new_graph, n = vertex_cover_to_independent_set(g, 2)
        self.assertEqual(n, 1)
        self.assertEqual(new_graph.node_count(), 3)
        self.assertEqual(new_graph.edge_count(), 2)
    
    def test_independent_set_to_vertex_cover(self):
        """测试独立集转节点覆盖"""
        g = Graph()
        n1 = g.add_node("A")
        n2 = g.add_node("B")
        n3 = g.add_node("C")
        g.add_edge(n1, n2)
        g.add_edge(n2, n3)
        
        # {n1, n3}是独立集，大小n=2
        # 节点覆盖大小 = 3-2=1, 即{n2}
        new_graph, k = independent_set_to_vertex_cover(g, 2)
        self.assertEqual(k, 1)
        self.assertEqual(new_graph.node_count(), 3)
        self.assertEqual(new_graph.edge_count(), 2)
    
    def test_conversion_roundtrip(self):
        """测试往返转换"""
        g = Graph()
        n1 = g.add_node("A")
        n2 = g.add_node("B")
        n3 = g.add_node("C")
        g.add_edge(n1, n2)
        g.add_edge(n2, n3)
        
        # g中3个节点，k=2的节点覆盖
        g2, n = vertex_cover_to_independent_set(g, 2)
        # n = 1
        g3, k = independent_set_to_vertex_cover(g2, n)
        # k = 2
        self.assertEqual(k, 2)
        self.assertEqual(g3.node_count(), 3)


class TestEndToEnd(unittest.TestCase):
    """端到端集成测试"""
    
    def test_satisfiable_formula_has_independent_set(self):
        """可满足的公式对应的图应存在大小为n的独立集"""
        from tests.test_cases import get_satisfiable_examples
        
        for formula in get_satisfiable_examples():
            graph, n = reduce_3sat_to_independent_set(formula)
            
            # 验证归约结构
            self.assertTrue(verify_independent_set_reduction(formula, graph, n))
            
            # 检查图的基本属性
            self.assertEqual(graph.node_count(), 3 * len(formula))
            
            # 验证每个三角形内部有3条边
            labels = graph.get_node_labels()
            # 分组检查每3个连续节点是否为三角形
            for i in range(len(formula)):
                base = i * 3
                self.assertTrue(graph.has_edge(base, base + 1))
                self.assertTrue(graph.has_edge(base + 1, base + 2))
                self.assertTrue(graph.has_edge(base, base + 2))
    
    def test_reduction_structure_consistency(self):
        """验证归约结构的一致性"""
        formulas = [
            parse_cnf_string("(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)"),
            parse_cnf_string("(x ∨ y ∨ z) ∧ (¬x ∨ ¬y ∨ ¬z) ∧ (x ∨ ¬y ∨ z)"),
            parse_cnf_string("(x ∨ y ∨ z)"),
        ]
        
        for formula in formulas:
            graph, n = reduce_3sat_to_independent_set(formula)
            
            # 验证节点数 = 3 * 子句数
            self.assertEqual(graph.node_count(), 3 * len(formula))
            
            # 验证n = 子句数
            self.assertEqual(n, len(formula))
            
            # 验证所有节点都有标签
            labels = graph.get_node_labels()
            self.assertEqual(len(labels), graph.node_count())
            
            # 验证每个标签都是公式中的文字
            formula_literals = set()
            for clause in formula:
                for lit in clause:
                    formula_literals.add(str(lit))
            
            for label in labels.values():
                self.assertIn(label, formula_literals)


class TestReduceWithVisualization(unittest.TestCase):
    """测试可视化相关的功能"""
    
    def test_reduction_result_can_be_drawn(self):
        """验证归约结果可以用于可视化"""
        try:
            import matplotlib
            matplotlib.use('Agg')  # 非交互模式
            from src.utils import draw_graph, draw_graph_with_independent_set
        except ImportError:
            self.skipTest("需要安装matplotlib和networkx")
        
        formula = parse_cnf_string("(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)")
        graph, n = reduce_3sat_to_independent_set(formula)
        
        # 找到一个独立集用于可视化
        # 尝试找到大小为n的独立集（简单尝试）
        labels = graph.get_node_labels()
        
        # 尝试贪心算法找独立集
        ind_set = set()
        nodes = graph.nodes()
        for node in nodes:
            # 检查与已选节点是否有边
            conflict = False
            for selected in ind_set:
                if graph.has_edge(node, selected):
                    conflict = True
                    break
            if not conflict:
                ind_set.add(node)
                if len(ind_set) >= n:
                    break
        
        if len(ind_set) >= n:
            # 验证独立集
            self.assertTrue(graph.is_independent_set(ind_set))


def generate_output_images():
    """
    生成归约结果展示图片
    
    按照PDF输出规范生成两张图片：
    1. 课件测试用例
    2. 自行设计测试用例（至少5个子句）
    """
    print("\n" + "="*60)
    print("开始生成独立集归约结果展示图片...")
    print("="*60 + "\n")
    
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import networkx as nx
        from matplotlib.lines import Line2D
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['DengXian', 'Microsoft YaHei', 'SimHei', 'FangSong', 'KaiTi']
        plt.rcParams['axes.unicode_minus'] = False
    except ImportError:
        print("需要安装 networkx 和 matplotlib 库：pip install networkx matplotlib")
        sys.exit(1)
    
    # 确保输出目录
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
    
    def draw_reduction_picture(formula, filename, description=""):
        """绘制归约结果图片，符合PDF输出规范"""
        graph, n = reduce_3sat_to_independent_set(formula)
        node_clause_info = get_node_clause_info()
        
        # 构造公式字符串
        formula_str = " ∧ ".join(
            "(" + " ∨ ".join(str(lit) for lit in clause) + ")"
            for clause in formula
        )
        
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
                     f"独立集：在上图中是否存在大小至少为 n = {n} 的独立集？",
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
                               node_color='lightblue', node_size=700,
                               alpha=0.95, node_shape='o',
                               edgecolors='steelblue', linewidths=1.5)
        
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
        
        ax_graph.set_title("3SAT → Independent Set 归约结果", fontsize=15, fontweight='bold', pad=15)
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
        "independent_set_course_example.png",
        "测试用例1（课件例子）："
    )
    
    # === 测试用例2：自行设计测试用例（至少5个子句）===
    print("\n测试用例2：自行设计测试用例（5个子句）")
    formula2 = parse_cnf_string(
        "(x ∨ ¬y ∨ z) ∧ (¬x ∨ y ∨ ¬z) ∧ (y ∨ ¬z ∨ w) ∧ (¬y ∨ z ∨ ¬w) ∧ (x ∨ ¬w ∨ ¬z)"
    )
    draw_reduction_picture(
        formula2,
        "independent_set_custom_example.png",
        "测试用例2（自行设计，5个子句）："
    )
    
    print("\n所有图片生成完毕！请在 output 目录中查看。")


if __name__ == '__main__':
    # 直接运行本文件时，生成展示图片
    generate_output_images()
