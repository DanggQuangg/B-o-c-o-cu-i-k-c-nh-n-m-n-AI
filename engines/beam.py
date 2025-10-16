from core.nqueens_utils import (
    cols_from_pairs,
    generate_solution,
    neighbors_partial,
)
class StepBeam:
    def __init__(self, n=8, target_pairs=None, beam_width=3):
        self.n = n
        self.target_cols = cols_from_pairs(target_pairs or generate_solution(n), n)
        self.K = beam_width
        self.reset()
    def reset(self):
        self.beam=[[]]; self.level=0; self.cur_state=[]; self.last_added=None
    def _score_child(self, child):
        row = len(child)-1; target_c = self.target_cols[row]
        return 1 if child[-1]==target_c else 0
    def is_goal(self, cols):
        return len(cols)==self.n and all(cols[r]==self.target_cols[r] for r in range(self.n))
    def step(self):
        if not self.beam: return {'state': self.cur_state, 'added': None, 'found': False, 'progressed': False}
        if self.level >= self.n:
            self.cur_state = self.beam[0][:]
            return {'state': self.cur_state, 'added': None, 'found': self.is_goal(self.cur_state), 'progressed': False}
        candidates=[]
        for node in self.beam:
            for child in neighbors_partial(node, self.n):
                candidates.append((self._score_child(child), child))
        if not candidates: return {'state': self.cur_state, 'added': None, 'found': False, 'progressed': False}
        candidates.sort(key=lambda x: (-x[0], x[1]))
        self.beam = [child for (sc, child) in candidates[:self.K]]
        self.cur_state = self.beam[0][:]
        self.level = len(self.cur_state)
        self.last_added = (self.level-1, self.cur_state[-1]) if self.level>0 else None
        return {'state': self.cur_state, 'added': self.last_added, 'found': self.is_goal(self.cur_state), 'progressed': True}