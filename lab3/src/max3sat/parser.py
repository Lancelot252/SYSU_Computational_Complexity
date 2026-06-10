"""
MAX-3SAT 公式解析器与随机生成器

支持两种输入模式：
1. 从 txt 文件读取已有的 MAX-3SAT 公式
2. 根据配置文件随机生成 MAX-3SAT 公式
"""

from src.max3sat.models import Clause, Formula, Literal


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
    # TODO: 实现
    raise NotImplementedError


def parse_literal(text: str) -> Literal:
    """
    解析单个文字字符串

    Args:
        text: 文字字符串，如 "x1" 或 "-x1"

    Returns:
        Literal 对象
    """
    # TODO: 实现
    raise NotImplementedError


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
    # TODO: 实现
    raise NotImplementedError


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
    # TODO: 实现
    raise NotImplementedError


def save_formula(formula: Formula, filepath: str) -> None:
    """
    将公式保存为 txt 文件

    Args:
        formula: 要保存的公式
        filepath: 保存路径
    """
    # TODO: 实现
    raise NotImplementedError
