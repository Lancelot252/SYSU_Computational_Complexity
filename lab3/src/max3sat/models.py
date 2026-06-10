"""
MAX-3SAT 数据模型

定义 MAX-3SAT 问题的核心数据结构，包括文字(Literal)、子句(Clause)和公式(Formula)。
"""

import math


class Literal:
    """
    布尔文字，表示一个变量或其否定

    Attributes:
        var: 变量名（如 "x1"）
        negated: 是否为否定文字
    """

    def __init__(self, var: str, negated: bool = False) -> None:
        self.var = var
        self.negated = negated

    def evaluate(self, assignment: dict[str, bool]) -> bool:
        """
        在给定变量赋值下求值

        Args:
            assignment: 变量名 -> 布尔值的映射

        Returns:
            该文字的真值
        """
        value = assignment.get(self.var, False)
        return not value if self.negated else value

    def __repr__(self) -> str:
        prefix = "¬" if self.negated else ""
        return f"{prefix}{self.var}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Literal):
            return NotImplemented
        return self.var == other.var and self.negated == other.negated

    def __hash__(self) -> int:
        return hash((self.var, self.negated))


class Clause:
    """
    3SAT 子句，由恰好3个文字组成

    Attributes:
        literals: 子句中的3个文字列表
        index: 子句编号（从1开始）
    """

    def __init__(self, literals: list[Literal], index: int) -> None:
        if len(literals) != 3:
            raise ValueError(f"每个子句必须恰好包含3个文字，当前有 {len(literals)} 个")
        self.literals = literals
        self.index = index

    def is_satisfied(self, assignment: dict[str, bool]) -> bool:
        """
        判断在给定赋值下该子句是否被满足

        Args:
            assignment: 变量名 -> 布尔值的映射

        Returns:
            该子句是否被满足
        """
        return any(lit.evaluate(assignment) for lit in self.literals)

    def __repr__(self) -> str:
        return "(" + " ∨ ".join(str(l) for l in self.literals) + ")"


class Formula:
    """
    MAX-3SAT 布尔公式

    Attributes:
        clauses: 子句列表
        variables: 变量名集合（有序）
    """

    def __init__(self, clauses: list[Clause]) -> None:
        self.clauses = clauses
        # 保持变量顺序一致（按变量名中的数字排序）
        var_set: set[str] = set()
        for clause in clauses:
            for lit in clause.literals:
                var_set.add(lit.var)
        # 按变量编号排序
        self.variables: list[str] = sorted(
            var_set, key=lambda v: int(v[1:]) if v[1:].isdigit() else v
        )

    @property
    def num_clauses(self) -> int:
        """子句数量"""
        return len(self.clauses)

    @property
    def num_variables(self) -> int:
        """变量数量"""
        return len(self.variables)

    @property
    def threshold(self) -> int:
        """目标满足子句数量：⌈7/8 * m⌉"""
        return math.ceil(7 / 8 * self.num_clauses)

    def count_satisfied(self, assignment: dict[str, bool]) -> int:
        """
        统计在给定赋值下被满足的子句数量

        Args:
            assignment: 变量名 -> 布尔值的映射

        Returns:
            被满足的子句数量
        """
        return sum(1 for clause in self.clauses if clause.is_satisfied(assignment))

    def get_satisfied_indices(self, assignment: dict[str, bool]) -> list[int]:
        """
        获取在给定赋值下被满足的子句编号列表

        Args:
            assignment: 变量名 -> 布尔值的映射

        Returns:
            被满足的子句编号列表
        """
        return [c.index for c in self.clauses if c.is_satisfied(assignment)]

    def __repr__(self) -> str:
        return " ∧ ".join(str(c) for c in self.clauses)
