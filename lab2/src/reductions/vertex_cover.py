"""
3SAT到节点覆盖(Vertex Cover)的归约

本模块提供了将3SAT问题归约为节点覆盖问题的接口。
节点覆盖问题：给定图G和整数k，判断G是否存在大小不超过k的节点覆盖。
节点覆盖是指一个节点集合，使得图中的每条边都至少有一个端点在该集合中。

归约的正确性：
    3SAT公式φ可满足 ⟺ 归约后的图G存在大小为k的节点覆盖
"""

from typing import Tuple
from ..models import Formula3SAT, Graph
from ..utils import format_node_label


def reduce_3sat_to_vertex_cover(formula: Formula3SAT) -> Tuple[Graph, int]:
    """
    将3SAT公式归约为节点覆盖问题

    归约算法：
    1. 对于每个子句，创建一个三角形（3个节点，每个节点代表一个文字）
    2. 对于每对互为否定的文字，在对应的节点之间添加冲突边
    3. 覆盖大小 k = 2m，其中 m 为子句数量

    参数:
        formula: 3SAT公式

    返回:
        (Graph, k): 图G和覆盖大小k
        使得公式可满足 ⟺ G有大小为k的节点覆盖
    """
    graph = Graph()
    m = formula.get_clause_count()
    k = 2 * m

    # 记录每个 (variable, negated) 对应的节点ID列表，用于添加冲突边
    literal_nodes = {}  # key: (variable, negated) -> list of node_id

    for i, clause in enumerate(formula):
        for j, literal in enumerate(clause):
            label = format_node_label(i + 1, str(literal))
            graph.add_node(label)

            key = (literal.variable, literal.negated)
            if key not in literal_nodes:
                literal_nodes[key] = []
            # node_id = i * 3 + j (since nodes are added sequentially)
            literal_nodes[key].append(i * 3 + j)

        # 为子句创建三角形边
        base = i * 3
        graph.add_edge(base, base + 1)
        graph.add_edge(base + 1, base + 2)
        graph.add_edge(base, base + 2)

    # 添加冲突边：连接互为否定的文字节点
    for var in formula.get_variables():
        pos_key = (var, False)
        neg_key = (var, True)

        if pos_key in literal_nodes and neg_key in literal_nodes:
            for pos_node in literal_nodes[pos_key]:
                for neg_node in literal_nodes[neg_key]:
                    if not graph.has_edge(pos_node, neg_node):
                        graph.add_edge(pos_node, neg_node)

    return graph, k


def verify_vertex_cover_reduction(formula: Formula3SAT, graph: Graph, k: int) -> bool:
    """
    验证归约的正确性

    检查：
    1. 节点数是否为 3m（m为子句数）
    2. k 是否等于 2m
    3. 每个子句对应的3个节点是否构成三角形
    4. 冲突边是否存在于互补文字节点之间

    参数:
        formula: 原始3SAT公式
        graph: 归约后的图
        k: 覆盖大小

    返回:
        bool: 如果归约结构正确返回True
    """
    m = formula.get_clause_count()
    n_vars = formula.get_variable_count()

    # 检查节点数和k值
    if graph.node_count() != 3 * m:
        return False
    if k != 2 * m:
        return False

    # 检查每个子句的三角形结构
    for i in range(m):
        base = i * 3
        a, b, c = base, base + 1, base + 2
        if not (graph.has_edge(a, b) and graph.has_edge(b, c) and graph.has_edge(a, c)):
            return False

    # 建立文字到节点的映射
    literal_to_nodes = {}
    for i, clause in enumerate(formula):
        for j, literal in enumerate(clause):
            node_id = i * 3 + j
            key = (literal.variable, literal.negated)
            if key not in literal_to_nodes:
                literal_to_nodes[key] = []
            literal_to_nodes[key].append(node_id)

    # 检查冲突边：互补文字节点之间应有边
    for var in formula.get_variables():
        pos_key = (var, False)
        neg_key = (var, True)
        if pos_key in literal_to_nodes and neg_key in literal_to_nodes:
            for pos_node in literal_to_nodes[pos_key]:
                for neg_node in literal_to_nodes[neg_key]:
                    if not graph.has_edge(pos_node, neg_node):
                        return False

    return True


def extract_satisfying_assignment(formula: Formula3SAT, graph: Graph,
                                  vertex_cover: set) -> dict:
    """
    从节点覆盖解中提取满足赋值

    对于大小为 k = 2m 的节点覆盖，每个子句三角形中恰好有2个节点被选中。
    未被选中的节点对应的文字为真，由此确定变量赋值。

    参数:
        formula: 原始3SAT公式
        graph: 归约后的图
        vertex_cover: 节点覆盖集合

    返回:
        dict: 变量名到布尔值的映射，表示满足赋值
    """
    assignment = {}
    m = formula.get_clause_count()

    for i, clause in enumerate(formula):
        for j, literal in enumerate(clause):
            node_id = i * 3 + j
            if node_id not in vertex_cover:
                # 此节点不在覆盖中 → 对应文字为真
                if literal.negated:
                    assignment[literal.variable] = False
                else:
                    assignment[literal.variable] = True

    # 对于未赋值的变量，默认为True
    for var in formula.get_variables():
        if var not in assignment:
            assignment[var] = True

    return assignment
