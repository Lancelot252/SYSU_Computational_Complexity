"""
MAX-3SAT 公式解析器与随机生成器
"""

import random
import re
from typing import Dict, List

from src.max3sat.models import Clause, Formula, Literal


def parse_literal(text: str) -> Literal:
    text = text.strip()
    if text.startswith("-"):
        return Literal(var=text[1:], negated=True)
    else:
        return Literal(var=text, negated=False)


def parse_formula(filepath: str) -> Formula:
    clauses: list[Clause] = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line_idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) != 3:
                raise ValueError(
                    f"第 {line_idx} 行: 每个子句必须包含恰好3个文字，当前有 {len(parts)} 个: '{line}'"
                )
            literals = [parse_literal(p) for p in parts]
            vars_in_clause = [lit.var for lit in literals]
            if len(vars_in_clause) != len(set(vars_in_clause)):
                raise ValueError(f"第 {line_idx} 行: 同一子句中不得出现重复变量: '{line}'")
            for i in range(3):
                for j in range(i + 1, 3):
                    if (literals[i].var == literals[j].var and literals[i].negated != literals[j].negated):
                        raise ValueError(f"第 {line_idx} 行: 同一子句中不得同时出现某变量及其否定: '{line}'")
            clauses.append(Clause(literals, index=line_idx))

    if len(clauses) < 4:
        raise ValueError(f"输入公式至少需要4个子句，当前只有 {len(clauses)} 个")

    return Formula(clauses)


def parse_random_config(filepath: str) -> List[Dict]:
    configs: List[Dict] = []
    current_config: Dict[str, str] = {}

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            raw = line
            line = line.strip()
            if not line or line.startswith("#"):
                if current_config:
                    configs.append(current_config)
                    current_config = {}
                continue
            parts = line.split()
            if len(parts) != 2:
                raise ValueError(f"配置行格式错误: '{raw.strip()}'")
            key, value = parts
            current_config[key] = value

    if current_config:
        configs.append(current_config)

    if not configs:
        raise ValueError("随机配置文件中未找到任何配置块")

    required_keys = ["number_of_variables", "number_of_clauses", "seed"]
    valid_configs: List[Dict] = []
    for config in configs:
        for key in required_keys:
            if key not in config:
                raise ValueError(f"缺少必填配置项: {key}")
        config["number_of_variables"] = int(config["number_of_variables"])
        config["number_of_clauses"] = int(config["number_of_clauses"])
        config["seed"] = int(config["seed"])
        if config["number_of_variables"] < 4:
            raise ValueError("变量数量必须 >= 4")
        if config["number_of_clauses"] < 4:
            raise ValueError("子句数量必须 >= 4")
        valid_configs.append(config)

    return valid_configs


def generate_random_formula(
    num_variables: int,
    num_clauses: int,
    seed: int,
    output_file: str = None,
) -> Formula:
    if num_variables < 4:
        raise ValueError(f"变量数量必须 >= 4，当前为 {num_variables}")
    if num_clauses < 4:
        raise ValueError(f"子句数量必须 >= 4，当前为 {num_clauses}")

    rng = random.Random(seed)
    var_names = [f"x{i}" for i in range(1, num_variables + 1)]
    clauses: list[Clause] = []

    for clause_idx in range(1, num_clauses + 1):
        chosen_vars = rng.sample(var_names, 3)
        literals: list[Literal] = []
        for var in chosen_vars:
            negated = rng.choice([True, False])
            literals.append(Literal(var=var, negated=negated))
        clauses.append(Clause(literals, index=clause_idx))

    formula = Formula(clauses)

    if output_file:
        save_formula(formula, output_file)

    return formula


def save_formula(formula: Formula, filepath: str) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        for clause in formula.clauses:
            parts: list[str] = []
            for lit in clause.literals:
                if lit.negated:
                    parts.append(f"-{lit.var}")
                else:
                    parts.append(lit.var)
            f.write(" ".join(parts) + "\n")
