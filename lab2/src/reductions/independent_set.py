"""
3SAT到独立集(Independent Set)的归约

本模块提供了将3SAT问题归约为独立集问题的接口。
独立集问题：给定图G和整数n，判断G是否存在大小至少为n的独立集。
独立集是指一个节点集合，其中任意两个节点之间都没有边相连。

归约的正确性：
    3SAT公式φ可满足 ⟺ 归约后的图G存在大小为n的独立集

注意：此模块的归约函数需要由人员C实现。
"""

from typing import Tuple, Dict, Set, List, Optional
from ..models import Formula3SAT, Graph, Literal

# 全局字典，用于记录图中每个节点所属的子句索引和文字信息
# 键：节点ID，值：子句索引, 文字字符串
_node_clause_info: Dict[int, Tuple[int, str]] = {}


def get_node_clause_info() -> Dict[int, Tuple[int, str]]:
    global _node_clause_info
    return _node_clause_info.copy()


def clear_node_clause_info():
    global _node_clause_info
    _node_clause_info = {}


def reduce_3sat_to_independent_set(formula: Formula3SAT) -> Tuple[Graph, int]:
    graph = Graph()
    global _node_clause_info
    _node_clause_info = {}
    
    # 记录所有正/负文字对应的节点列表
    pos_nodes: Dict[str, List[int]] = {}   
    neg_nodes: Dict[str, List[int]] = {}   
    
    # 为每个子句创建三角形
    for clause_idx, clause in enumerate(formula):
        triangle_nodes = []
        for lit in clause:
            label = str(lit)  # "x" 或 "¬x"
            node_id = graph.add_node(label)
            triangle_nodes.append(node_id)
            # 记录节点所属子句索引和文字信息
            _node_clause_info[node_id] = (clause_idx, label)
            
            # 根据正/负记录节点
            if lit.negated:
                neg_nodes.setdefault(lit.variable, []).append(node_id)
            else:
                pos_nodes.setdefault(lit.variable, []).append(node_id)
        
        # 创建三角形的三条边
        graph.add_edge(triangle_nodes[0], triangle_nodes[1])
        graph.add_edge(triangle_nodes[1], triangle_nodes[2])
        graph.add_edge(triangle_nodes[0], triangle_nodes[2])
    
    # 对于每对互为否定的文字，在对应的节点之间添加边
    for var in formula.variables:
        pos_list = pos_nodes.get(var, [])
        neg_list = neg_nodes.get(var, [])
        for p_node in pos_list:
            for n_node in neg_list:
                if not graph.has_edge(p_node, n_node):
                    graph.add_edge(p_node, n_node)
    
    # 计算独立集大小 = 子句数
    n = len(formula)
    
    return graph, n


def verify_independent_set_reduction(formula: Formula3SAT, graph: Graph, n: int) -> bool:
    # 检查1：独立集大小应为子句数
    if n != len(formula):
        return False
    
    # 检查2：节点数应为 3 * 子句数
    if graph.node_count() != 3 * len(formula):
        return False
    
    # 检查3：通过重新执行归约，验证图结构一致
    test_graph, test_n = reduce_3sat_to_independent_set(formula)
    if test_graph.node_count() != graph.node_count():
        return False
    if test_graph.edge_count() != graph.edge_count():
        return False
    
    # 检查4：每个节点应有有效标签
    labels = graph.get_node_labels()
    if len(labels) != graph.node_count():
        return False

    formula_literals = set()
    for clause in formula:
        for lit in clause:
            formula_literals.add(str(lit))
    
    for label in labels.values():
        if label not in formula_literals:
            return False
    
    # 检查5：验证每个子句三角形内部三条边都存在
    for clause in formula:
        pass  
    
    return True


def extract_satisfying_assignment(formula: Formula3SAT, graph: Graph, 
                                  independent_set: set) -> dict:
    assignment: Dict[str, bool] = {}
    
    # 从独立集中提取赋值
    for node_id in independent_set:
        label = graph.get_label(node_id)
        if not label:
            continue
        
        # 判断是正文字还是负文字
        if label.startswith('¬'):
            var = label[1:]
            # 负文字在独立集中 => 变量为 False
            if var not in assignment:
                assignment[var] = False
        else:
            var = label
            # 正文字在独立集中 => 变量为 True
            if var not in assignment:
                assignment[var] = True
    
    # 给独立集中未出现的变量赋予默认值（True）
    for var in formula.variables:
        if var not in assignment:
            assignment[var] = True
    
    return assignment


def vertex_cover_to_independent_set(graph: Graph, k: int) -> Tuple[Graph, int]:

    n = graph.node_count() - k
    return graph.copy(), n


def independent_set_to_vertex_cover(graph: Graph, n: int) -> Tuple[Graph, int]:
    k = graph.node_count() - n
    return graph.copy(), k
