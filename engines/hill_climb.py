import random
from core.nqueens_utils import (
    random_permutation,
    diag_conflicts,
)
class StepHillClimb:
    def __init__(self, n=8, step_logger=None, max_sideways=0):
        self.n = n; self.step_logger = step_logger
        self.max_sideways = max_sideways
        self.reset()
    def reset(self):
        self.cols = random_permutation(self.n)
        self.best_conf = diag_conflicts(self.cols)
        self.sideways_left = self.max_sideways
        self.last_added = None
    def is_goal(self): return self.best_conf == 0
    def _all_best_swaps(self):
        n = self.n; best = self.best_conf; best_pairs = []
        for i in range(n):
            for j in range(i+1, n):
                self.cols[i], self.cols[j] = self.cols[j], self.cols[i]
                c = diag_conflicts(self.cols)
                self.cols[i], self.cols[j] = self.cols[j], self.cols[i]
                if c < best: best, best_pairs = c, [(i,j,c)]
                elif c == best: best_pairs.append((i,j,c))
        return best, best_pairs
    def step(self):
        if self.is_goal():
            return {'state': self.cols[:], 'added': None, 'found': True, 'progressed': True}
        best_after, pairs = self._all_best_swaps()
        if best_after < self.best_conf:
            i,j,c = random.choice([p for p in pairs if p[2]==best_after])
            self.cols[i], self.cols[j] = self.cols[j], self.cols[i]
            self.best_conf = c; self.last_added = (i, self.cols[i])
            return {'state': self.cols[:], 'added': self.last_added, 'found': self.is_goal(), 'progressed': True}
        if self.sideways_left > 0:
            eq = [p for p in pairs if p[2]==self.best_conf]
            if eq:
                i,j,c = random.choice(eq)
                self.cols[i], self.cols[j] = self.cols[j], self.cols[i]
                self.sideways_left -= 1; self.last_added = (i, self.cols[i])
                return {'state': self.cols[:], 'added': self.last_added, 'found': self.is_goal(), 'progressed': True}
        return {'state': self.cols[:], 'added': None, 'found': False, 'progressed': False}