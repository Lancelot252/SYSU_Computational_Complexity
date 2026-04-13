"""
图数据结构

本模块定义了无向图的数据结构，用于表示归约后的节点覆盖和独立集问题实例。
"""

from typing import List, Set, Tuple, Dict, Optional, Any
from copy import deepcopy


class Graph:
    """
    无向图数据结构
    
    用于表示归约后生成的图，支持节点和边的操作。
    节点使用整数ID标识，可以有可选的标签。
    
    Attributes:
        _nodes: 节点ID列表
        _edges: 边集合，每条边是节点ID的元组 (u, v)，其中 u < v
        _node_labels: 节点ID到标签的映射
        _adjacency: 邻接表，节点ID到邻居集合的映射
    """
    
    def __init__(self):
        """
        初始化一个空图
        """
        self._nodes: List[int] = []
        self._edges: Set[Tuple[int, int]] = set()
        self._node_labels: Dict[int, str] = {}
        self._adjacency: Dict[int, Set[int]] = {}
        self._next_node_id: int = 0
    
    def add_node(self, label: str = "") -> int:
        """
        添加一个新节点
        
        Args:
            label: 节点的可选标签，用于标识节点（如变量名）
            
        Returns:
            新节点的ID
        """
        node_id = self._next_node_id
        self._next_node_id += 1
        self._nodes.append(node_id)
        self._adjacency[node_id] = set()
        if label:
            self._node_labels[node_id] = label
        return node_id
    
    def add_edge(self, u: int, v: int) -> None:
        """
        添加一条无向边
        
        Args:
            u: 第一个节点的ID
            v: 第二个节点的ID
            
        Raises:
            ValueError: 如果节点不存在或尝试添加自环
        """
        if u not in self._nodes or v not in self._nodes:
            raise ValueError(f"节点 {u} 或 {v} 不存在")
        if u == v:
            raise ValueError("不允许添加自环边")
        
        # 确保边的表示一致（较小的ID在前）
        edge = (min(u, v), max(u, v))
        self._edges.add(edge)
        
        # 更新邻接表
        self._adjacency[u].add(v)
        self._adjacency[v].add(u)
    
    def remove_node(self, node_id: int) -> None:
        """
        移除一个节点及其所有关联的边
        
        Args:
            node_id: 要移除的节点ID
            
        Raises:
            ValueError: 如果节点不存在
        """
        if node_id not in self._nodes:
            raise ValueError(f"节点 {node_id} 不存在")
        
        # 移除所有关联的边
        neighbors = self._adjacency[node_id].copy()
        for neighbor in neighbors:
            self.remove_edge(node_id, neighbor)
        
        # 移除节点
        self._nodes.remove(node_id)
        del self._adjacency[node_id]
        if node_id in self._node_labels:
            del self._node_labels[node_id]
    
    def remove_edge(self, u: int, v: int) -> None:
        """
        移除一条无向边
        
        Args:
            u: 第一个节点的ID
            v: 第二个节点的ID
            
        Raises:
            ValueError: 如果边不存在
        """
        edge = (min(u, v), max(u, v))
        if edge not in self._edges:
            raise ValueError(f"边 ({u}, {v}) 不存在")
        
        self._edges.remove(edge)
        self._adjacency[u].discard(v)
        self._adjacency[v].discard(u)
    
    def nodes(self) -> List[int]:
        """
        获取所有节点ID
        
        Returns:
            节点ID列表
        """
        return self._nodes.copy()
    
    def edges(self) -> List[Tuple[int, int]]:
        """
        获取所有边
        
        Returns:
            边列表，每条边是节点ID的元组
        """
        return list(self._edges)
    
    def node_count(self) -> int:
        """
        获取节点数量
        
        Returns:
            节点数量
        """
        return len(self._nodes)
    
    def edge_count(self) -> int:
        """
        获取边数量
        
        Returns:
            边数量
        """
        return len(self._edges)
    
    def get_label(self, node_id: int) -> str:
        """
        获取节点的标签
        
        Args:
            node_id: 节点ID
            
        Returns:
            节点标签，如果没有标签则返回空字符串
            
        Raises:
            ValueError: 如果节点不存在
        """
        if node_id not in self._nodes:
            raise ValueError(f"节点 {node_id} 不存在")
        return self._node_labels.get(node_id, "")
    
    def set_label(self, node_id: int, label: str) -> None:
        """
        设置节点的标签
        
        Args:
            node_id: 节点ID
            label: 要设置的标签
            
        Raises:
            ValueError: 如果节点不存在
        """
        if node_id not in self._nodes:
            raise ValueError(f"节点 {node_id} 不存在")
        if label:
            self._node_labels[node_id] = label
        elif node_id in self._node_labels:
            del self._node_labels[node_id]
    
    def neighbors(self, node_id: int) -> Set[int]:
        """
        获取节点的所有邻居
        
        Args:
            node_id: 节点ID
            
        Returns:
            邻居节点ID集合
            
        Raises:
            ValueError: 如果节点不存在
        """
        if node_id not in self._nodes:
            raise ValueError(f"节点 {node_id} 不存在")
        return self._adjacency[node_id].copy()
    
    def degree(self, node_id: int) -> int:
        """
        获取节点的度数
        
        Args:
            node_id: 节点ID
            
        Returns:
            节点的度数
            
        Raises:
            ValueError: 如果节点不存在
        """
        if node_id not in self._nodes:
            raise ValueError(f"节点 {node_id} 不存在")
        return len(self._adjacency[node_id])
    
    def has_edge(self, u: int, v: int) -> bool:
        """
        检查两个节点之间是否有边
        
        Args:
            u: 第一个节点的ID
            v: 第二个节点的ID
            
        Returns:
            如果存在边则返回 True
        """
        edge = (min(u, v), max(u, v))
        return edge in self._edges
    
    def has_node(self, node_id: int) -> bool:
        """
        检查节点是否存在
        
        Args:
            node_id: 节点ID
            
        Returns:
            如果节点存在则返回 True
        """
        return node_id in self._nodes
    
    def to_networkx(self) -> Any:
        """
        转换为networkx图对象
        
        用于可视化和进一步分析。
        
        Returns:
            networkx.Graph 对象
        """
        try:
            import networkx as nx
        except ImportError:
            raise ImportError("需要安装networkx库: pip install networkx")
        
        G = nx.Graph()
        
        # 添加节点
        for node_id in self._nodes:
            label = self._node_labels.get(node_id, str(node_id))
            G.add_node(node_id, label=label)
        
        # 添加边
        for u, v in self._edges:
            G.add_edge(u, v)
        
        return G
    
    def copy(self) -> 'Graph':
        """
        创建图的深拷贝
        
        Returns:
            新的Graph对象，与原图完全独立
        """
        new_graph = Graph()
        new_graph._nodes = self._nodes.copy()
        new_graph._edges = self._edges.copy()
        new_graph._node_labels = self._node_labels.copy()
        new_graph._adjacency = {k: v.copy() for k, v in self._adjacency.items()}
        new_graph._next_node_id = self._next_node_id
        return new_graph
    
    def __str__(self) -> str:
        """
        返回图的字符串表示
        
        Returns:
            图的描述字符串
        """
        return f"Graph(nodes={self.node_count()}, edges={self.edge_count()})"
    
    def __repr__(self) -> str:
        """
        返回图的正式表示
        
        Returns:
            图的正式表示字符串
        """
        return f"Graph(nodes={self._nodes}, edges={list(self._edges)})"
    
    def __len__(self) -> int:
        """
        返回节点数量
        
        Returns:
            节点数量
        """
        return self.node_count()
    
    def __contains__(self, node_id: int) -> bool:
        """
        检查节点是否存在
        
        Args:
            node_id: 节点ID
            
        Returns:
            如果节点存在则返回 True
        """
        return self.has_node(node_id)
    
    def get_node_labels(self) -> Dict[int, str]:
        """
        获取所有节点标签
        
        Returns:
            节点ID到标签的映射字典
        """
        return self._node_labels.copy()
    
    def get_adjacency_dict(self) -> Dict[int, Set[int]]:
        """
        获取邻接表
        
        Returns:
            邻接表字典
        """
        return {k: v.copy() for k, v in self._adjacency.items()}
    
    def is_vertex_cover(self, vertices: Set[int]) -> bool:
        """
        检查给定的顶点集合是否是图的顶点覆盖
        
        顶点覆盖是指一个顶点集合，使得图中的每条边都至少有一个端点在该集合中。
        
        Args:
            vertices: 顶点集合
            
        Returns:
            如果是顶点覆盖则返回 True
        """
        for u, v in self._edges:
            if u not in vertices and v not in vertices:
                return False
        return True
    
    def is_independent_set(self, vertices: Set[int]) -> bool:
        """
        检查给定的顶点集合是否是图的独立集
        
        独立集是指一个顶点集合，其中任意两个顶点之间都没有边相连。
        
        Args:
            vertices: 顶点集合
            
        Returns:
            如果是独立集则返回 True
        """
        for u, v in self._edges:
            if u in vertices and v in vertices:
                return False
        return True
    
    def get_complement_edges(self) -> List[Tuple[int, int]]:
        """
        获取补图的边
        
        Returns:
            补图中所有边的列表
        """
        complement_edges = []
        nodes = self._nodes
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                u, v = nodes[i], nodes[j]
                if not self.has_edge(u, v):
                    complement_edges.append((u, v))
        return complement_edges