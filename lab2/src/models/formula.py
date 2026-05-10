"""
3SAT公式数据结构

本模块定义了表示3SAT公式的数据结构，包括文字(Literal)、子句(Clause)和公式(Formula3SAT)。
"""

from typing import List, Set, Iterator
from dataclasses import dataclass


@dataclass
class Literal:
    """
    文字：变量名 + 是否取反
    
    表示一个布尔变量或其否定形式。
    例如：x 是变量 x 的正文字，¬x 是变量 x 的负文字。
    
    Attributes:
        variable: 变量名，如 'x', 'y', 'z' 等
        negated: 是否取反，True 表示取反，False 表示不取反
    """
    variable: str
    negated: bool = False
    
    def __str__(self) -> str:
        """
        返回文字的字符串表示
        
        Returns:
            如 "x" 或 "¬x"
        """
        if self.negated:
            return f"¬{self.variable}"
        return self.variable
    
    def __repr__(self) -> str:
        """
        返回文字的正式表示
        
        Returns:
            如 "Literal('x', False)" 或 "Literal('x', True)"
        """
        return f"Literal('{self.variable}', {self.negated})"
    
    def __eq__(self, other) -> bool:
        """
        判断两个文字是否相等
        
        Args:
            other: 另一个文字对象
            
        Returns:
            如果变量名和取反状态都相同则返回 True
        """
        if not isinstance(other, Literal):
            return False
        return self.variable == other.variable and self.negated == other.negated
    
    def __hash__(self) -> int:
        """
        返回文字的哈希值，使其可以用于集合和字典
        
        Returns:
            哈希值
        """
        return hash((self.variable, self.negated))
    
    def negate(self) -> 'Literal':
        """
        返回取反的文字
        
        Returns:
            新的取反文字对象
        """
        return Literal(self.variable, not self.negated)


class Clause:
    """
    子句：3个文字的析取
    
    表示形如 (x ∨ y ∨ ¬z) 的子句，其中包含恰好3个文字。
    在3SAT问题中，每个子句必须恰好包含3个文字。
    
    Attributes:
        literals: 包含3个文字的列表
    """
    
    def __init__(self, literals: List[Literal]):
        """
        初始化子句
        
        Args:
            literals: 包含3个文字的列表
            
        Raises:
            ValueError: 如果文字数量不为3
        """
        if len(literals) != 3:
            raise ValueError(f"3SAT子句必须恰好包含3个文字，但收到了{len(literals)}个")
        self.literals = literals
    
    def __str__(self) -> str:
        """
        返回子句的字符串表示
        
        Returns:
            如 "(x ∨ y ∨ ¬z)"
        """
        literal_strs = [str(lit) for lit in self.literals]
        return "(" + " ∨ ".join(literal_strs) + ")"
    
    def __repr__(self) -> str:
        """
        返回子句的正式表示
        
        Returns:
            如 "Clause([Literal('x', False), Literal('y', False), Literal('z', True)])"
        """
        return f"Clause({self.literals})"
    
    def __iter__(self) -> Iterator[Literal]:
        """
        支持迭代遍历子句中的文字
        
        Yields:
            子句中的每个文字
        """
        return iter(self.literals)
    
    def __len__(self) -> int:
        """
        返回子句中文字的数量
        
        Returns:
            总是返回3
        """
        return len(self.literals)
    
    def __eq__(self, other) -> bool:
        """
        判断两个子句是否相等
        
        Args:
            other: 另一个子句对象
            
        Returns:
            如果两个子句包含相同的文字则返回 True
        """
        if not isinstance(other, Clause):
            return False
        return self.literals == other.literals
    
    def __hash__(self) -> int:
        """
        返回子句的哈希值
        
        Returns:
            哈希值
        """
        return hash(tuple(self.literals))
    
    def get_variables(self) -> Set[str]:
        """
        获取子句中所有变量名
        
        Returns:
            变量名集合
        """
        return {lit.variable for lit in self.literals}


class Formula3SAT:
    """
    3SAT公式
    
    表示一个合取范式(CNF)形式的3SAT公式，即多个子句的合取。
    例如：(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)
    
    Attributes:
        clauses: 子句列表
        variables: 所有变量集合
    """
    
    def __init__(self, clauses: List[Clause]):
        """
        初始化3SAT公式
        
        Args:
            clauses: 子句列表
        """
        self.clauses = clauses
        self.variables: Set[str] = set()
        for clause in clauses:
            self.variables.update(clause.get_variables())
    
    def __str__(self) -> str:
        """
        返回公式的字符串表示
        
        Returns:
            如 "(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)"
        """
        if not self.clauses:
            return "⊤"  # 空公式为真
        clause_strs = [str(clause) for clause in self.clauses]
        return " ∧ ".join(clause_strs)
    
    def __repr__(self) -> str:
        """
        返回公式的正式表示
        
        Returns:
            如 "Formula3SAT([Clause(...), Clause(...)])"
        """
        return f"Formula3SAT({self.clauses})"
    
    def __iter__(self) -> Iterator[Clause]:
        """
        支持迭代遍历公式中的子句
        
        Yields:
            公式中的每个子句
        """
        return iter(self.clauses)
    
    def __len__(self) -> int:
        """
        返回公式中子句的数量
        
        Returns:
            子句数量
        """
        return len(self.clauses)
    
    def __eq__(self, other) -> bool:
        """
        判断两个公式是否相等
        
        Args:
            other: 另一个公式对象
            
        Returns:
            如果两个公式包含相同的子句则返回 True
        """
        if not isinstance(other, Formula3SAT):
            return False
        return self.clauses == other.clauses
    
    def __hash__(self) -> int:
        """
        返回公式的哈希值
        
        Returns:
            哈希值
        """
        return hash(tuple(self.clauses))
    
    @classmethod
    def from_string(cls, s: str) -> 'Formula3SAT':
        """
        从字符串解析3SAT公式
        
        支持以下格式：
        - "(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)"
        - "(x|y|~z)&(~x|~y|z)"
        
        Args:
            s: 公式字符串
            
        Returns:
            解析后的Formula3SAT对象
            
        Raises:
            ValueError: 如果字符串格式无效
        """
        from ..parsers import parse_cnf_string
        return parse_cnf_string(s)
    
    def get_clause_count(self) -> int:
        """
        获取子句数量
        
        Returns:
            子句数量
        """
        return len(self.clauses)
    
    def get_variable_count(self) -> int:
        """
        获取变量数量
        
        Returns:
            变量数量
        """
        return len(self.variables)
    
    def get_clauses(self) -> List[Clause]:
        """
        获取所有子句
        
        Returns:
            子句列表
        """
        return self.clauses.copy()
    
    def get_variables(self) -> Set[str]:
        """
        获取所有变量
        
        Returns:
            变量集合
        """
        return self.variables.copy()