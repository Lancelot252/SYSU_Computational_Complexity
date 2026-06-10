"""
MAX-3SAT 公式解析器与随机生成器

支持两种输入模式：
1. 从 txt 文件读取已有的 MAX-3SAT 公式
2. 根据配置文件随机生成 MAX-3SAT 公式
"""

import random
import re

from src.max3sat.models import Clause, Formula, Literal


def parse_literal(text: str) -> Literal:
    """
    解析单个文字字符串

    Args:
        text: 文字字符串，如 "x1" 或 "-x1"

    Returns:
        Literal 对象
    """
    text = text.strip()
    if text.startswith("-"):
        return Literal(var=text[1:], negated=True)
    else:
        return Literal(var=text, negated=False)


def parse_formula(filepath: str) -> Formula:
    """
    从 txt 文件解析 MAX-3SAT 公式

    文件格式：
        每行一个子句，3个文字以空格分隔
        正文字直接写变量名（如 x1），负文字前加 -（如 -x1）

    Args:
        filepath: 公式文件路径

    Returns:
        解析得到的 Formula 对象
    """
    clauses: list[Clause] = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line_idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) != 3:
                raise ValueError(
                    f"第 {line_idx} 行: 每个子句必须包含恰好3个文字，"
                    f"当前有 {len(parts)} 个: '{line}'"
                )
            literals = [parse_literal(p) for p in parts]
            # 检查同一子句中变量是否互不相同
            vars_in_clause = [lit.var for lit in literals]
            if len(vars_in_clause) != len(set(vars_in_clause)):
                raise ValueError(
                    f"第 {line_idx} 行: 同一子句中不得出现重复变量: '{line}'"
                )
            # 检查同一子句中不得同时出现某变量及其否定
            for i in range(3):
                for j in range(i + 1, 3):
                    if (literals[i].var == literals[j].var
                            and literals[i].negated != literals[j].negated):
                        raise ValueError(
                            f"第 {line_idx} 行: 同一子句中不得同时出现某变量及其否定: '{line}'"
                        )
            clauses.append(Clause(literals, index=line_idx))

    if len(clauses) < 4:
        raise ValueError(f"输入公式至少需要4个子句，当前只有 {len(clauses)} 个")

    return Formula(clauses)


def parse_random_config(filepath: str) -> dict:
    """
    解析随机生成配置文件

    配置文件格式：
        number_of_variables 8
        number_of_clauses 20
        seed 2026
        output_file random_8_20.txt

    Args:
        filepath: 配置文件路径

    Returns:
        包含配置项的字典
    """
    config: dict = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) != 2:
                raise ValueError(f"配置行格式错误: '{line}'")
            key, value = parts
            config[key] = value

    # 验证必填字段
    required_keys = ["number_of_variables", "number_of_clauses", "seed"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"缺少必填配置项: {key}")

    # 类型转换与验证
    config["number_of_variables"] = int(config["number_of_variables"])
    config["number_of_clauses"] = int(config["number_of_clauses"])
    config["seed"] = int(config["seed"])

    if config["number_of_variables"] < 4:
        raise ValueError("变量数量必须 >= 4")
    if config["number_of_clauses"] < 4:
        raise ValueError("子句数量必须 >= 4")

    return config


def generate_random_formula(
    num_variables: int,
    num_clauses: int,
    seed: int,
    output_file: str | None = None,
) -> Formula:
    """
    根据参数随机生成 MAX-3SAT 公式

    生成规则：
    1. 每个子句恰好包含3个文字
    2. 同一子句中不得出现重复变量
    3. 同一子句中不得同时出现某变量及其否定
    4. 变量统一命名为 x1, x2, ..., xn
    5. 相同 seed + num_variables + num_clauses 生成相同公式

    Args:
        num_variables: 变量数量（>=4）
        num_clauses: 子句数量（>=4）
        seed: 随机种子
        output_file: 可选，将生成的公式保存到文件

    Returns:
        随机生成的 Formula 对象
    """
    if num_variables < 4:
        raise ValueError(f"变量数量必须 >= 4，当前为 {num_variables}")
    if num_clauses < 4:
        raise ValueError(f"子句数量必须 >= 4，当前为 {num_clauses}")
    if num_variables < 3:
        raise ValueError("变量数量必须 >= 3 才能生成3文字子句")

    rng = random.Random(seed)
    var_names = [f"x{i}" for i in range(1, num_variables + 1)]
    clauses: list[Clause] = []

    for clause_idx in range(1, num_clauses + 1):
        # 随机选择3个不同的变量
        chosen_vars = rng.sample(var_names, 3)
        # 对每个变量随机决定是否取否定
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
    """
    将公式保存为 txt 文件

    Args:
        formula: 要保存的公式
        filepath: 保存路径
    """
    with open(filepath, "w", encoding="utf-8") as f:
        for clause in formula.clauses:
            parts: list[str] = []
            for lit in clause.literals:
                if lit.negated:
                    parts.append(f"-{lit.var}")
                else:
                    parts.append(lit.var)
            f.write(" ".join(parts) + "\n")
