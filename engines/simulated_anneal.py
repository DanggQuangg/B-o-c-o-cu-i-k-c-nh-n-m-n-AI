import random, math
from core.nqueens_utils import (
    random_permutation,
    diag_conflicts,
)
class StepSimAnneal:
    def __init__(self, n=8, step_logger=None, T0=5.0, alpha=0.95, Tmin=0.01):
        self.n = n; self.step_logger = step_logger
        self.T0=T0; self.alpha=alpha; self.Tmin=Tmin
        self.reset()
    def reset(self):
        self.cols = random_permutation(self.n)
        self.cur_conf = diag_conflicts(self.cols)
        self.T = self.T0; self.last_added=None
    def is_goal(self): return self.cur_conf == 0
    def step(self):
        if self.is_goal():
            return {'state': self.cols[:], 'added': None, 'found': True, 'progressed': True}
        i,j = random.sample(range(self.n), 2)
        self.cols[i], self.cols[j] = self.cols[j], self.cols[i]
        new_conf = diag_conflicts(self.cols); delta = new_conf - self.cur_conf
        accept = (delta <= 0) or (self.T>0 and random.random() < math.exp(-delta/self.T))
        if accept:
            self.cur_conf = new_conf; self.last_added = (i, self.cols[i])
        else:
            self.cols[i], self.cols[j] = self.cols[j], self.cols[i]; self.last_added = None
        self.T = max(self.T*self.alpha, self.Tmin)
        return {'state': self.cols[:], 'added': self.last_added, 'found': self.is_goal(), 'progressed': True}