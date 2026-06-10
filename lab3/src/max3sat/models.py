"""
MAX-3SAT 数据模型

定义 MAX-3SAT 问题的核心数据结构，包括文字(Literal)、子句(Clause)和公式(Formula)。
"""


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
        # TODO: 实现
        raise NotImplementedError

    def __repr__(self) -> str:
        prefix = "¬" if self.negated else ""
        return f"{prefix}{self.var}"


class Clause:
    """
    3SAT 子句，由恰好3个文字组成

    Attributes:
        literals: 子句中的3个文字列表
        index: 子句编号（从1开始）
    """

    def __init__(self, literals: list[Literal], index: int) -> None:
        if len(literals) != 3:
            raise ValueError("每个子句必须恰好包含3个文字")
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
        # TODO: 实现
        raise NotImplementedError

    def __repr__(self) -> str:
        return "(" + " ∨ ".join(str(l) for l in self.literals) + ")"


class Formula:
    """
    MAX-3SAT 布尔公式

    Attributes:
        clauses: 子句列表
        variables: 变量名集合
    """

    def __init__(self, clauses: list[Clause]) -> None:
        self.clauses = clauses
        self.variables: set[str] = set()
        for clause in clauses:
            for lit in clause.literals:
                self.variables.add(lit.var)

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
        """目标满足子句数量：ceil(7/8 * m)"""
        import math
        return math.ceil(7 / 8 * self.num_clauses)

    def count_satisfied(self, assignment: dict[str, bool]) -> int:
        """
        统计在给定赋值下被满足的子句数量

        Args:
            assignment: 变量名 -> 布尔值的映射

        Returns:
            被满足的子句数量
        """
        # TODO: 实现
        raise NotImplementedError

    def get_satisfied_indices(self, assignment: dict[str, bool]) -> list[int]:
        """
        获取在给定赋值下被满足的子句编号列表

        Args:
            assignment: 变量名 -> 布尔值的映射

        Returns:
            被满足的子句编号列表
        """
        # TODO: 实现
        raise NotImplementedError

    def __repr__(self) -> str:
        return " ∧ ".join(str(c) for c in self.clauses)
