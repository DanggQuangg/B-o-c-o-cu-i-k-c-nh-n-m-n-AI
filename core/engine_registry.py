# core/engine_registry.py
from engines.search_step import StepSearch
from engines.hill_climb import StepHillClimb
from engines.simulated_anneal import StepSimAnneal
from engines.beam import StepBeam
from engines.genetic import StepGA
from engines.backtracking import StepBacktracking
from engines.forward_checking import StepForwardChecking
from engines.ac3 import StepAC3
from engines.belief_bfs import StepBeliefSearch
from engines.and_or import StepAndOrSearch
from engines.partial_belief import StepPartialBelief

ALGO_BUTTONS = [
    "BFS", "DFS", "DLS", "IDS", "Greedy", "A*", "UCS",
    "Hill Climbing", "Simulated Annealing", "Genetic Algorithm",
    "Beam Search", "Belief Search", "Backtracking",
    "Forward Checking", "AC-3",
    "AND-OR Search", "Tăng tốc", "Partial Belief Search"
]

def make_engine(name: str, n: int, target_pairs):
    up = name.upper()
    if up in {"BFS","DFS","DLS","IDS","GREEDY","A*","UCS"}:
        return StepSearch(algo=up, n=n, target_pairs=target_pairs, dls_limit=n)
    if up == "HILL CLIMBING":
        return StepHillClimb(n=n)
    if up == "SIMULATED ANNEALING":
        return StepSimAnneal(n=n)
    if up == "BEAM SEARCH":
        return StepBeam(n=n, target_pairs=target_pairs, beam_width=3)
    if up == "GENETIC ALGORITHM":
        return StepGA(n=n, target_pairs=target_pairs, pop_size=30, mutate_rate=0.2, elite=2)
    if up == "BACKTRACKING":
        return StepBacktracking(n=n, target_pairs=target_pairs)
    if up == "FORWARD CHECKING":
        return StepForwardChecking(n=n, target_pairs=target_pairs)
    if up == "AC-3":
        return StepAC3(n=n, target_pairs=target_pairs)
    if up == "BELIEF SEARCH":
        return StepBeliefSearch(n=n)
    if up == "AND-OR SEARCH":
        return StepAndOrSearch(n=n)
    if up == "PARTIAL BELIEF SEARCH":
        return StepPartialBelief(n=n, target_pairs=target_pairs)
    return None  # fallback xử lý ở main (mô phỏng ngẫu nhiên)
