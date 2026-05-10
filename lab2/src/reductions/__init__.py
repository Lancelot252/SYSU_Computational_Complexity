"""
归约算法模块

包含3SAT到节点覆盖和独立集问题的归约算法。
"""

from .vertex_cover import (
    reduce_3sat_to_vertex_cover,
    verify_vertex_cover_reduction,
    extract_satisfying_assignment as extract_satisfying_assignment_vc
)
from .independent_set import (
    reduce_3sat_to_independent_set,
    verify_independent_set_reduction,
    extract_satisfying_assignment as extract_satisfying_assignment_is,
    vertex_cover_to_independent_set,
    independent_set_to_vertex_cover
)

__all__ = [
    'reduce_3sat_to_vertex_cover',
    'verify_vertex_cover_reduction',
    'extract_satisfying_assignment_vc',
    'reduce_3sat_to_independent_set',
    'verify_independent_set_reduction',
    'extract_satisfying_assignment_is',
    'vertex_cover_to_independent_set',
    'independent_set_to_vertex_cover'
]