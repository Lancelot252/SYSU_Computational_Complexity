"""
CNF公式解析器

本模块提供了解析CNF格式字符串和DIMACS CNF格式文件的功能。
支持多种输入格式，包括数学符号格式和编程格式。
"""

import re
from typing import List, Dict
from ..models import Literal, Clause, Formula3SAT


def parse_cnf_string(s: str) -> Formula3SAT:
    """
    解析CNF格式字符串，支持多种格式
    
    支持的格式：
    1. 数学符号格式: "(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)"
    2. 编程格式: "(x|y|~z)&(~x|~y|z)"
    3. 简化格式: "(x+y+!z)*(!x+!y+z)"
    
    Args:
        s: CNF公式字符串
        
    Returns:
        解析后的Formula3SAT对象
        
    Raises:
        ValueError: 如果字符串格式无效或子句不包含恰好3个文字
        
    Examples:
        >>> formula = parse_cnf_string("(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)")
        >>> print(formula)
        (x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)
        
        >>> formula = parse_cnf_string("(x|y|~z)&(~x|~y|z)")
        >>> print(formula)
        (x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)
    """
    # 标准化字符串：移除空白字符
    s = s.strip()
    
    if not s:
        raise ValueError("输入字符串不能为空")
    
    # 检测分隔符类型
    clause_separator = _detect_clause_separator(s)
    literal_separator = _detect_literal_separator(s)
    
    # 分割子句
    clauses_str = _split_clauses(s, clause_separator)
    
    # 解析每个子句
    clauses: List[Clause] = []
    for clause_str in clauses_str:
        clause = _parse_clause(clause_str, literal_separator)
        clauses.append(clause)
    
    return Formula3SAT(clauses)


def _detect_clause_separator(s: str) -> str:
    """
    检测子句分隔符
    
    Args:
        s: 输入字符串
        
    Returns:
        子句分隔符字符
    """
    # 检查各种可能的子句分隔符
    if '∧' in s or '∧' in s:
        return '∧'
    if '&' in s:
        return '&'
    if '*' in s:
        return '*'
    if '&&' in s:
        return '&&'
    # 默认使用 ∧
    return '∧'


def _detect_literal_separator(s: str) -> str:
    """
    检测文字分隔符
    
    Args:
        s: 输入字符串
        
    Returns:
        文字分隔符字符
    """
    # 检查各种可能的文字分隔符
    if '∨' in s:
        return '∨'
    if '|' in s:
        return '|'
    if '+' in s:
        return '+'
    # 默认使用 ∨
    return '∨'


def _split_clauses(s: str, separator: str) -> List[str]:
    """
    分割子句字符串
    
    Args:
        s: 输入字符串
        separator: 子句分隔符
        
    Returns:
        子句字符串列表
    """
    # 移除最外层的括号（如果有）
    s = s.strip()
    
    # 处理不同的分隔符
    if separator == '∧':
        # 使用 Unicode 字符
        parts = s.split('∧')
    elif separator == '&&':
        parts = s.split('&&')
    else:
        parts = s.split(separator)
    
    # 清理每个部分
    clauses_str = []
    for part in parts:
        part = part.strip()
        if part:
            clauses_str.append(part)
    
    if not clauses_str:
        raise ValueError("未找到有效的子句")
    
    return clauses_str


def _parse_clause(clause_str: str, literal_separator: str) -> Clause:
    """
    解析单个子句
    
    Args:
        clause_str: 子句字符串，如 "(x ∨ y ∨ ¬z)"
        literal_separator: 文字分隔符
        
    Returns:
        解析后的Clause对象
    """
    # 移除括号
    clause_str = clause_str.strip()
    if clause_str.startswith('(') and clause_str.endswith(')'):
        clause_str = clause_str[1:-1].strip()
    elif clause_str.startswith('[') and clause_str.endswith(']'):
        clause_str = clause_str[1:-1].strip()
    elif clause_str.startswith('{') and clause_str.endswith('}'):
        clause_str = clause_str[1:-1].strip()
    
    # 分割文字
    if literal_separator == '∨':
        literals_str = clause_str.split('∨')
    else:
        literals_str = clause_str.split(literal_separator)
    
    # 解析每个文字
    literals: List[Literal] = []
    for lit_str in literals_str:
        lit_str = lit_str.strip()
        if lit_str:
            literal = _parse_literal(lit_str)
            literals.append(literal)
    
    return Clause(literals)


def _parse_literal(lit_str: str) -> Literal:
    """
    解析单个文字
    
    Args:
        lit_str: 文字字符串，如 "x", "¬x", "~x", "!x"
        
    Returns:
        解析后的Literal对象
    """
    lit_str = lit_str.strip()
    
    if not lit_str:
        raise ValueError("文字不能为空")
    
    # 检测否定符号
    negated = False
    variable = lit_str
    
    # 支持多种否定符号: ¬, ~, !, -
    negation_symbols = ['¬', '~', '!', '-']
    
    for symbol in negation_symbols:
        if variable.startswith(symbol):
            negated = True
            variable = variable[1:].strip()
            break
    
    if not variable:
        raise ValueError(f"无效的文字格式: {lit_str}")
    
    # 验证变量名（只允许字母、数字和下划线）
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', variable):
        raise ValueError(f"无效的变量名: {variable}")
    
    return Literal(variable, negated)


def parse_dimacs(file_path: str) -> Formula3SAT:
    """
    解析DIMACS CNF格式文件
    
    DIMACS CNF格式是SAT问题的标准格式：
    - 以 'c' 开头的行是注释
    - 以 'p' 开头的行是问题行: p cnf <变量数> <子句数>
    - 每个子句一行，以 0 结尾
    - 正数表示正文字，负数表示负文字
    - 例如: 1 -2 3 0 表示 (x1 ∨ ¬x2 ∨ x3)
    
    Args:
        file_path: DIMACS CNF文件路径
        
    Returns:
        解析后的Formula3SAT对象
        
    Raises:
        FileNotFoundError: 如果文件不存在
        ValueError: 如果文件格式无效
        
    Examples:
        假设文件内容为:
        c 这是一个示例
        p cnf 3 2
        1 -2 3 0
        -1 -2 3 0
        
        >>> formula = parse_dimacs("example.cnf")
        >>> print(formula)
        (x1 ∨ ¬x2 ∨ x3) ∧ (¬x1 ∨ ¬x2 ∨ x3)
    """
    clauses: List[Clause] = []
    variable_map: Dict[int, str] = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # 跳过空行和注释
            if not line or line.startswith('c'):
                continue
            
            # 跳过问题行
            if line.startswith('p'):
                continue
            
            # 解析子句
            literals: List[Literal] = []
            parts = line.split()
            
            for part in parts:
                try:
                    lit_num = int(part)
                except ValueError:
                    continue
                
                # 0 表示子句结束
                if lit_num == 0:
                    break
                
                # 获取或创建变量名
                var_num = abs(lit_num)
                if var_num not in variable_map:
                    variable_map[var_num] = f"x{var_num}"
                
                variable = variable_map[var_num]
                negated = lit_num < 0
                literals.append(Literal(variable, negated))
            
            if len(literals) == 3:
                clauses.append(Clause(literals))
            elif len(literals) > 0:
                raise ValueError(f"子句必须恰好包含3个文字，但收到了{len(literals)}个")
    
    return Formula3SAT(clauses)


def parse_dimacs_string(s: str) -> Formula3SAT:
    """
    解析DIMACS CNF格式字符串
    
    与parse_dimacs功能相同，但接受字符串输入而非文件路径。
    
    Args:
        s: DIMACS CNF格式字符串
        
    Returns:
        解析后的Formula3SAT对象
        
    Raises:
        ValueError: 如果字符串格式无效
    """
    clauses: List[Clause] = []
    variable_map: Dict[int, str] = {}
    
    for line in s.split('\n'):
        line = line.strip()
        
        # 跳过空行和注释
        if not line or line.startswith('c'):
            continue
        
        # 跳过问题行
        if line.startswith('p'):
            continue
        
        # 解析子句
        literals: List[Literal] = []
        parts = line.split()
        
        for part in parts:
            try:
                lit_num = int(part)
            except ValueError:
                continue
            
            # 0 表示子句结束
            if lit_num == 0:
                break
            
            # 获取或创建变量名
            var_num = abs(lit_num)
            if var_num not in variable_map:
                variable_map[var_num] = f"x{var_num}"
            
            variable = variable_map[var_num]
            negated = lit_num < 0
            literals.append(Literal(variable, negated))
        
        if len(literals) == 3:
            clauses.append(Clause(literals))
        elif len(literals) > 0:
            raise ValueError(f"子句必须恰好包含3个文字，但收到了{len(literals)}个")
    
    return Formula3SAT(clauses)