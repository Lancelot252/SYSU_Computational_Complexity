"""
解析器模块

包含CNF公式解析器，支持多种输入格式：
- 数学符号格式: "(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)"
- 编程格式: "(x|y|~z)&(~x|~y|z)"
- DIMACS CNF格式: 标准SAT问题格式
- txt格式: 本次作业规定的格式，每行3个文字空格分隔
"""

from .cnf_parser import (
    parse_cnf_string,
    parse_dimacs,
    parse_dimacs_string,
    parse_txt_file,
    parse_txt_string
)

__all__ = [
    'parse_cnf_string',
    'parse_dimacs',
    'parse_dimacs_string',
    'parse_txt_file',
    'parse_txt_string'
]