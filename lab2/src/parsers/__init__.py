"""
解析器模块

包含CNF公式解析器。
"""

from .cnf_parser import parse_cnf_string, parse_dimacs

__all__ = ['parse_cnf_string', 'parse_dimacs']