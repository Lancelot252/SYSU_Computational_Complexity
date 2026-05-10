"""
预定义测试用例

本模块包含用于测试3SAT归约算法的预定义测试用例。
包括课件中的例子和自定义的测试用例。
"""

from typing import List, Tuple
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import Literal, Clause, Formula3SAT
from src.parsers import parse_cnf_string


# =============================================================================
# 课件例子
# =============================================================================

# 课件中的示例公式
COURSE_EXAMPLE = "(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z) ∧ (¬x ∨ y ∨ ¬z)"
COURSE_EXAMPLE_VARIABLES = {'x', 'y', 'z'}
COURSE_EXAMPLE_CLAUSE_COUNT = 3

# 课件例子的解析版本
def get_course_example() -> Formula3SAT:
    """
    获取课件例子的Formula3SAT对象
    
    Returns:
        课件中的示例公式
    """
    return parse_cnf_string(COURSE_EXAMPLE)


# =============================================================================
# 自定义测试用例
# =============================================================================

# 自定义5+子句例子
CUSTOM_EXAMPLE = "(x ∨ y ∨ ¬z) ∧ (¬x ∨ z ∨ w) ∧ (y ∨ ¬w ∨ u) ∧ (¬y ∨ ¬u ∨ x) ∧ (z ∨ w ∨ ¬u) ∧ (¬x ∨ ¬z ∨ u)"
CUSTOM_EXAMPLE_VARIABLES = {'x', 'y', 'z', 'w', 'u'}
CUSTOM_EXAMPLE_CLAUSE_COUNT = 6

def get_custom_example() -> Formula3SAT:
    """
    获取自定义例子的Formula3SAT对象
    
    Returns:
        自定义的5+子句公式
    """
    return parse_cnf_string(CUSTOM_EXAMPLE)


# =============================================================================
# 简单测试用例
# =============================================================================

# 单子句公式（可满足）
SIMPLE_SAT = "(x ∨ y ∨ z)"

def get_simple_sat() -> Formula3SAT:
    """
    获取简单的可满足公式
    
    Returns:
        单子句公式
    """
    return parse_cnf_string(SIMPLE_SAT)


# 单子句公式（所有变量取反）
SIMPLE_UNSAT_PATTERN = "(¬x ∨ ¬y ∨ ¬z)"

def get_simple_unsat_pattern() -> Formula3SAT:
    """
    获取简单公式（所有变量取反）
    
    Returns:
        单子句公式
    """
    return parse_cnf_string(SIMPLE_UNSAT_PATTERN)


# =============================================================================
# 可满足性测试用例
# =============================================================================

# 明确可满足的公式
SATISFIABLE_EXAMPLES: List[str] = [
    # 单子句
    "(x ∨ y ∨ z)",
    # 两个子句，容易满足
    "(x ∨ y ∨ z) ∧ (¬x ∨ y ∨ z)",
    # 三个子句
    "(x ∨ y ∨ z) ∧ (¬x ∨ y ∨ z) ∧ (x ∨ ¬y ∨ z)",
    # 课件例子
    "(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z) ∧ (¬x ∨ y ∨ ¬z)",
]

def get_satisfiable_examples() -> List[Formula3SAT]:
    """
    获取所有可满足的测试公式
    
    Returns:
        可满足公式列表
    """
    return [parse_cnf_string(s) for s in SATISFIABLE_EXAMPLES]


# =============================================================================
# 边界测试用例
# =============================================================================

# 最小公式（单子句）
MINIMAL_FORMULA = "(x ∨ y ∨ z)"

def get_minimal_formula() -> Formula3SAT:
    """
    获取最小公式
    
    Returns:
        单子句公式
    """
    return parse_cnf_string(MINIMAL_FORMULA)


# 包含重复变量的公式
DUPLICATE_VARIABLES = "(x ∨ x ∨ y)"

def get_duplicate_variables_formula() -> Formula3SAT:
    """
    获取包含重复变量的公式
    
    Returns:
        包含重复变量的公式
    """
    return parse_cnf_string(DUPLICATE_VARIABLES)


# =============================================================================
# DIMACS格式测试用例
# =============================================================================

# DIMACS格式的简单例子
DIMACS_SIMPLE = """c 这是一个简单的3SAT公式示例
c 变量: x1, x2, x3
p cnf 3 2
1 -2 3 0
-1 -2 3 0
"""

# DIMACS格式的课件例子
DIMACS_COURSE_EXAMPLE = """c 课件例子
c 变量: x1, x2, x3
p cnf 3 3
1 2 -3 0
-1 -2 3 0
-1 2 -3 0
"""

# DIMACS格式的自定义例子
DIMACS_CUSTOM = """c 自定义5+子句例子
c 变量: x1, x2, x3, x4, x5
p cnf 5 6
1 2 -3 0
-1 3 4 0
2 -4 5 0
-2 -5 1 0
3 4 -5 0
-1 -3 5 0
"""


# =============================================================================
# 编程格式测试用例
# =============================================================================

# 使用编程符号的公式
PROGRAMMING_FORMAT_EXAMPLES: List[str] = [
    "(x|y|~z)&(~x|~y|z)",
    "(x+y+!z)*(!x+!y+z)",
    "(x1|x2|~x3)&(~x1|~x2|x3)&(x1|~x2|~x3)",
]

def get_programming_format_examples() -> List[Formula3SAT]:
    """
    获取编程格式的测试公式
    
    Returns:
        编程格式公式列表
    """
    return [parse_cnf_string(s) for s in PROGRAMMING_FORMAT_EXAMPLES]


# =============================================================================
# 测试用例集合
# =============================================================================

def get_all_test_cases() -> List[Tuple[str, Formula3SAT]]:
    """
    获取所有测试用例
    
    Returns:
        (名称, 公式) 元组列表
    """
    return [
        ("课件例子", get_course_example()),
        ("自定义例子", get_custom_example()),
        ("简单可满足", get_simple_sat()),
        ("最小公式", get_minimal_formula()),
    ]


def get_test_case_by_name(name: str) -> Formula3SAT:
    """
    根据名称获取测试用例
    
    Args:
        name: 测试用例名称
        
    Returns:
        对应的Formula3SAT对象
        
    Raises:
        ValueError: 如果名称不存在
    """
    cases = {
        "课件例子": get_course_example,
        "自定义例子": get_custom_example,
        "简单可满足": get_simple_sat,
        "最小公式": get_minimal_formula,
    }
    
    if name not in cases:
        raise ValueError(f"未知的测试用例名称: {name}")
    
    return cases[name]()


# =============================================================================
# 验证函数
# =============================================================================

def verify_formula_structure(formula: Formula3SAT, 
                             expected_clause_count: int,
                             expected_variables: set) -> bool:
    """
    验证公式的结构
    
    Args:
        formula: 要验证的公式
        expected_clause_count: 期望的子句数量
        expected_variables: 期望的变量集合
        
    Returns:
        如果结构正确返回True
    """
    if len(formula) != expected_clause_count:
        return False
    
    if formula.get_variables() != expected_variables:
        return False
    
    # 验证每个子句都有3个文字
    for clause in formula:
        if len(clause) != 3:
            return False
    
    return True


def run_basic_tests():
    """
    运行基本测试
    
    用于验证数据结构和解析器的正确性。
    """
    print("运行基本测试...")
    
    # 测试课件例子
    formula = get_course_example()
    assert verify_formula_structure(formula, 3, {'x', 'y', 'z'})
    print(f"✓ 课件例子测试通过: {formula}")
    
    # 测试自定义例子
    formula = get_custom_example()
    assert verify_formula_structure(formula, 6, {'x', 'y', 'z', 'w', 'u'})
    print(f"✓ 自定义例子测试通过: {formula}")
    
    # 测试简单公式
    formula = get_simple_sat()
    assert verify_formula_structure(formula, 1, {'x', 'y', 'z'})
    print(f"✓ 简单公式测试通过: {formula}")
    
    # 测试编程格式
    formulas = get_programming_format_examples()
    for i, f in enumerate(formulas):
        print(f"✓ 编程格式测试{i+1}通过: {f}")
    
    print("\n所有基本测试通过！")


if __name__ == "__main__":
    run_basic_tests()