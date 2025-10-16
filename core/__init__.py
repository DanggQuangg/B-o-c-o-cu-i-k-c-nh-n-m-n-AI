# core/__init__.py
"""
Package core: chứa các tiện ích và registry dùng chung cho toàn chương trình 8-Queens AI.
"""

from .nqueens_utils import (
    generate_solution,
    cols_from_pairs,
    pair_list_from_cols,
    is_safe_partial,
    neighbors_partial,
    random_permutation,
    diag_conflicts
)

from .engine_registry import (
    ALGO_BUTTONS,
    make_engine
)

__all__ = [
    "generate_solution",
    "cols_from_pairs",
    "pair_list_from_cols",
    "is_safe_partial",
    "neighbors_partial",
    "random_permutation",
    "diag_conflicts",
    "ALGO_BUTTONS",
    "make_engine",
]
