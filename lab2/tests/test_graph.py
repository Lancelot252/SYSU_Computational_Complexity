"""
测试Graph数据结构

本模块测试Graph类的功能。
"""

import unittest
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import Graph


class TestGraph(unittest.TestCase):
    """测试Graph类"""
    
    def setUp(self):
        """设置测试用例"""
        self.graph = Graph()
    
    def test_graph_creation(self):
        """测试图创建"""
        self.assertEqual(self.graph.node_count(), 0)
        self.assertEqual(self.graph.edge_count(), 0)
    
    def test_add_node(self):
        """测试添加节点"""
        node1 = self.graph.add_node("A")
        node2 = self.graph.add_node("B")
        
        self.assertEqual(self.graph.node_count(), 2)
        self.assertEqual(self.graph.get_label(node1), "A")
        self.assertEqual(self.graph.get_label(node2), "B")
    
    def test_add_node_without_label(self):
        """测试添加无标签节点"""
        node = self.graph.add_node()
        
        self.assertEqual(self.graph.node_count(), 1)
        self.assertEqual(self.graph.get_label(node), "")
    
    def test_add_edge(self):
        """测试添加边"""
        node1 = self.graph.add_node("A")
        node2 = self.graph.add_node("B")
        
        self.graph.add_edge(node1, node2)
        
        self.assertEqual(self.graph.edge_count(), 1)
        self.assertTrue(self.graph.has_edge(node1, node2))
    
    def test_add_edge_invalid_nodes(self):
        """测试添加边到无效节点"""
        with self.assertRaises(ValueError):
            self.graph.add_edge(0, 1)  # 节点不存在
    
    def test_add_self_loop(self):
        """测试添加自环"""
        node = self.graph.add_node()
        
        with self.assertRaises(ValueError):
            self.graph.add_edge(node, node)
    
    def test_remove_node(self):
        """测试移除节点"""
        node1 = self.graph.add_node("A")
        node2 = self.graph.add_node("B")
        self.graph.add_edge(node1, node2)
        
        self.graph.remove_node(node1)
        
        self.assertEqual(self.graph.node_count(), 1)
        self.assertEqual(self.graph.edge_count(), 0)
        self.assertFalse(self.graph.has_node(node1))
    
    def test_remove_edge(self):
        """测试移除边"""
        node1 = self.graph.add_node("A")
        node2 = self.graph.add_node("B")
        self.graph.add_edge(node1, node2)
        
        self.graph.remove_edge(node1, node2)
        
        self.assertEqual(self.graph.edge_count(), 0)
        self.assertFalse(self.graph.has_edge(node1, node2))
    
    def test_neighbors(self):
        """测试获取邻居"""
        node1 = self.graph.add_node("A")
        node2 = self.graph.add_node("B")
        node3 = self.graph.add_node("C")
        
        self.graph.add_edge(node1, node2)
        self.graph.add_edge(node1, node3)
        
        neighbors = self.graph.neighbors(node1)
        self.assertEqual(neighbors, {node2, node3})
    
    def test_degree(self):
        """测试获取度数"""
        node1 = self.graph.add_node("A")
        node2 = self.graph.add_node("B")
        node3 = self.graph.add_node("C")
        
        self.graph.add_edge(node1, node2)
        self.graph.add_edge(node1, node3)
        
        self.assertEqual(self.graph.degree(node1), 2)
        self.assertEqual(self.graph.degree(node2), 1)
    
    def test_copy(self):
        """测试图复制"""
        node1 = self.graph.add_node("A")
        node2 = self.graph.add_node("B")
        self.graph.add_edge(node1, node2)
        
        copied = self.graph.copy()
        
        self.assertEqual(copied.node_count(), self.graph.node_count())
        self.assertEqual(copied.edge_count(), self.graph.edge_count())
        
        # 修改原图不影响复制
        self.graph.add_node("C")
        self.assertEqual(copied.node_count(), 2)
    
    def test_is_vertex_cover(self):
        """测试顶点覆盖检查"""
        node1 = self.graph.add_node()
        node2 = self.graph.add_node()
        node3 = self.graph.add_node()
        
        self.graph.add_edge(node1, node2)
        self.graph.add_edge(node2, node3)
        
        # {node1, node2} 是顶点覆盖
        self.assertTrue(self.graph.is_vertex_cover({node1, node2}))
        
        # {node1} 不是顶点覆盖（边(node2, node3)未被覆盖）
        self.assertFalse(self.graph.is_vertex_cover({node1}))
        
        # {node2} 是顶点覆盖
        self.assertTrue(self.graph.is_vertex_cover({node2}))
    
    def test_is_independent_set(self):
        """测试独立集检查"""
        node1 = self.graph.add_node()
        node2 = self.graph.add_node()
        node3 = self.graph.add_node()
        
        self.graph.add_edge(node1, node2)
        self.graph.add_edge(node2, node3)
        
        # {node1, node3} 是独立集
        self.assertTrue(self.graph.is_independent_set({node1, node3}))
        
        # {node1, node2} 不是独立集（有边相连）
        self.assertFalse(self.graph.is_independent_set({node1, node2}))
        
        # {node2} 是独立集（单节点）
        self.assertTrue(self.graph.is_independent_set({node2}))
    
    def test_str_representation(self):
        """测试字符串表示"""
        node1 = self.graph.add_node("A")
        node2 = self.graph.add_node("B")
        self.graph.add_edge(node1, node2)
        
        self.assertEqual(str(self.graph), "Graph(nodes=2, edges=1)")
    
    def test_contains(self):
        """测试包含检查"""
        node = self.graph.add_node()
        
        self.assertTrue(node in self.graph)
        self.assertFalse(999 in self.graph)
    
    def test_set_label(self):
        """测试设置标签"""
        node = self.graph.add_node()
        
        self.graph.set_label(node, "NewLabel")
        self.assertEqual(self.graph.get_label(node), "NewLabel")
        
        # 清除标签
        self.graph.set_label(node, "")
        self.assertEqual(self.graph.get_label(node), "")


class TestGraphAdvanced(unittest.TestCase):
    """测试Graph高级功能"""
    
    def test_triangle_graph(self):
        """测试三角形图"""
        graph = Graph()
        nodes = [graph.add_node() for _ in range(3)]
        
        # 创建三角形
        graph.add_edge(nodes[0], nodes[1])
        graph.add_edge(nodes[1], nodes[2])
        graph.add_edge(nodes[0], nodes[2])
        
        self.assertEqual(graph.node_count(), 3)
        self.assertEqual(graph.edge_count(), 3)
        
        # 每个节点的度数都是2
        for node in nodes:
            self.assertEqual(graph.degree(node), 2)
    
    def test_complete_graph(self):
        """测试完全图"""
        n = 4
        graph = Graph()
        nodes = [graph.add_node() for _ in range(n)]
        
        # 创建完全图
        for i in range(n):
            for j in range(i + 1, n):
                graph.add_edge(nodes[i], nodes[j])
        
        # 完全图有 n*(n-1)/2 条边
        expected_edges = n * (n - 1) // 2
        self.assertEqual(graph.edge_count(), expected_edges)
        
        # 每个节点的度数都是 n-1
        for node in nodes:
            self.assertEqual(graph.degree(node), n - 1)
    
    def test_get_complement_edges(self):
        """测试获取补图边"""
        graph = Graph()
        nodes = [graph.add_node() for _ in range(4)]
        
        # 只添加部分边
        graph.add_edge(nodes[0], nodes[1])
        graph.add_edge(nodes[2], nodes[3])
        
        complement_edges = graph.get_complement_edges()
        
        # 补图应该有 4*3/2 - 2 = 4 条边
        self.assertEqual(len(complement_edges), 4)


if __name__ == '__main__':
    unittest.main()