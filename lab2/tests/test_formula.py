"""
测试Formula3SAT数据结构

本模块测试Literal、Clause和Formula3SAT类的功能。
"""

import unittest
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import Literal, Clause, Formula3SAT


class TestLiteral(unittest.TestCase):
    """测试Literal类"""
    
    def test_literal_creation(self):
        """测试文字创建"""
        lit = Literal('x', False)
        self.assertEqual(lit.variable, 'x')
        self.assertFalse(lit.negated)
    
    def test_literal_negated(self):
        """测试取反文字"""
        lit = Literal('x', True)
        self.assertEqual(lit.variable, 'x')
        self.assertTrue(lit.negated)
    
    def test_literal_str(self):
        """测试文字字符串表示"""
        lit_pos = Literal('x', False)
        lit_neg = Literal('x', True)
        self.assertEqual(str(lit_pos), 'x')
        self.assertEqual(str(lit_neg), '¬x')
    
    def test_literal_negate(self):
        """测试文字取反操作"""
        lit = Literal('x', False)
        negated = lit.negate()
        self.assertEqual(negated.variable, 'x')
        self.assertTrue(negated.negated)
        
        # 再次取反应该恢复原状态
        double_negated = negated.negate()
        self.assertFalse(double_negated.negated)
    
    def test_literal_equality(self):
        """测试文字相等性"""
        lit1 = Literal('x', False)
        lit2 = Literal('x', False)
        lit3 = Literal('x', True)
        lit4 = Literal('y', False)
        
        self.assertEqual(lit1, lit2)
        self.assertNotEqual(lit1, lit3)
        self.assertNotEqual(lit1, lit4)
    
    def test_literal_hash(self):
        """测试文字哈希值"""
        lit1 = Literal('x', False)
        lit2 = Literal('x', False)
        
        # 相等的文字应该有相同的哈希值
        self.assertEqual(hash(lit1), hash(lit2))
        
        # 可以放入集合
        s = {lit1, lit2}
        self.assertEqual(len(s), 1)


class TestClause(unittest.TestCase):
    """测试Clause类"""
    
    def setUp(self):
        """设置测试用例"""
        self.literals = [
            Literal('x', False),
            Literal('y', False),
            Literal('z', True)
        ]
        self.clause = Clause(self.literals)
    
    def test_clause_creation(self):
        """测试子句创建"""
        self.assertEqual(len(self.clause), 3)
    
    def test_clause_invalid_creation(self):
        """测试无效子句创建"""
        # 少于3个文字
        with self.assertRaises(ValueError):
            Clause([Literal('x', False), Literal('y', False)])
        
        # 多于3个文字
        with self.assertRaises(ValueError):
            Clause([
                Literal('x', False),
                Literal('y', False),
                Literal('z', False),
                Literal('w', False)
            ])
    
    def test_clause_str(self):
        """测试子句字符串表示"""
        self.assertEqual(str(self.clause), '(x ∨ y ∨ ¬z)')
    
    def test_clause_iteration(self):
        """测试子句迭代"""
        count = 0
        for lit in self.clause:
            count += 1
            self.assertIsInstance(lit, Literal)
        self.assertEqual(count, 3)
    
    def test_clause_get_variables(self):
        """测试获取子句变量"""
        variables = self.clause.get_variables()
        self.assertEqual(variables, {'x', 'y', 'z'})
    
    def test_clause_equality(self):
        """测试子句相等性"""
        clause1 = Clause([
            Literal('x', False),
            Literal('y', False),
            Literal('z', True)
        ])
        clause2 = Clause([
            Literal('x', False),
            Literal('y', False),
            Literal('z', True)
        ])
        clause3 = Clause([
            Literal('x', True),
            Literal('y', False),
            Literal('z', True)
        ])
        
        self.assertEqual(clause1, clause2)
        self.assertNotEqual(clause1, clause3)


class TestFormula3SAT(unittest.TestCase):
    """测试Formula3SAT类"""
    
    def setUp(self):
        """设置测试用例"""
        self.clause1 = Clause([
            Literal('x', False),
            Literal('y', False),
            Literal('z', True)
        ])
        self.clause2 = Clause([
            Literal('x', True),
            Literal('y', True),
            Literal('z', False)
        ])
        self.formula = Formula3SAT([self.clause1, self.clause2])
    
    def test_formula_creation(self):
        """测试公式创建"""
        self.assertEqual(len(self.formula), 2)
        self.assertEqual(self.formula.get_variable_count(), 3)
    
    def test_formula_variables(self):
        """测试公式变量集合"""
        variables = self.formula.get_variables()
        self.assertEqual(variables, {'x', 'y', 'z'})
    
    def test_formula_str(self):
        """测试公式字符串表示"""
        self.assertEqual(str(self.formula), '(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)')
    
    def test_formula_iteration(self):
        """测试公式迭代"""
        count = 0
        for clause in self.formula:
            count += 1
            self.assertIsInstance(clause, Clause)
        self.assertEqual(count, 2)
    
    def test_empty_formula(self):
        """测试空公式"""
        formula = Formula3SAT([])
        self.assertEqual(len(formula), 0)
        self.assertEqual(str(formula), '⊤')
    
    def test_formula_equality(self):
        """测试公式相等性"""
        formula1 = Formula3SAT([self.clause1, self.clause2])
        formula2 = Formula3SAT([self.clause1, self.clause2])
        
        self.assertEqual(formula1, formula2)
    
    def test_formula_get_clause_count(self):
        """测试获取子句数量"""
        self.assertEqual(self.formula.get_clause_count(), 2)
    
    def test_formula_get_clauses(self):
        """测试获取子句列表"""
        clauses = self.formula.get_clauses()
        self.assertEqual(len(clauses), 2)
        self.assertIsInstance(clauses, list)


if __name__ == '__main__':
    unittest.main()