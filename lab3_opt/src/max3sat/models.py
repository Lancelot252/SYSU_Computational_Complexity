"""
MAX-3SAT 数据模型（副本）
"""

import math
from typing import Dict, List, Set


class Literal:
    def __init__(self, var: str, negated: bool = False) -> None:
        self.var = var
        self.negated = negated

    def evaluate(self, assignment: Dict[str, bool]) -> bool:
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
    def __init__(self, literals: List[Literal], index: int) -> None:
        if len(literals) != 3:
            raise ValueError(f"每个子句必须恰好包含3个文字，当前有 {len(literals)} 个")
        self.literals = literals
        self.index = index

    def is_satisfied(self, assignment: Dict[str, bool]) -> bool:
        return any(lit.evaluate(assignment) for lit in self.literals)

    def __repr__(self) -> str:
        return "(" + " ∨ ".join(str(l) for l in self.literals) + ")"


class Formula:
    def __init__(self, clauses: List[Clause]) -> None:
        self.clauses = clauses
        var_set: Set[str] = set()
        for clause in clauses:
            for lit in clause.literals:
                var_set.add(lit.var)
        self.variables: List[str] = sorted(
            var_set, key=lambda v: int(v[1:]) if v[1:].isdigit() else v
        )

    @property
    def num_clauses(self) -> int:
        return len(self.clauses)

    @property
    def num_variables(self) -> int:
        return len(self.variables)

    @property
    def threshold(self) -> int:
        return math.ceil(7 / 8 * self.num_clauses)

    def count_satisfied(self, assignment: Dict[str, bool]) -> int:
        return sum(1 for clause in self.clauses if clause.is_satisfied(assignment))

    def get_satisfied_indices(self, assignment: Dict[str, bool]) -> List[int]:
        return [c.index for c in self.clauses if c.is_satisfied(assignment)]

    def __repr__(self) -> str:
        return " ∧ ".join(str(c) for c in self.clauses)
