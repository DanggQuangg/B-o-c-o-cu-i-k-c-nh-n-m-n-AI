# engines/__init__.py
"""
Package engines: chứa tất cả các class thuật toán tìm kiếm, ràng buộc, heuristic.
Mỗi engine triển khai step-by-step interface:
    - reset()
    - step() -> dict(state, added, found, progressed)
"""

from .search_step import StepSearch
from .hill_climb import StepHillClimb
from .simulated_anneal import StepSimAnneal
from .beam import StepBeam
from .genetic import StepGA
from .backtracking import StepBacktracking
from .forward_checking import StepForwardChecking
from .ac3 import StepAC3
from .belief_bfs import StepBeliefSearch
from .and_or import StepAndOrSearch
from .partial_belief import StepPartialBelief

__all__ = [
    "StepSearch",
    "StepHillClimb",
    "StepSimAnneal",
    "StepBeam",
    "StepGA",
    "StepBacktracking",
    "StepForwardChecking",
    "StepAC3",
    "StepBeliefSearch",
    "StepAndOrSearch",
    "StepPartialBelief",
]
