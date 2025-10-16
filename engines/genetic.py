import random
from core.nqueens_utils import (
    cols_from_pairs,
    generate_solution,
    random_permutation,
    diag_conflicts,
)
class StepGA:
    def __init__(self, n=8, target_pairs=None, pop_size=30, mutate_rate=0.2, elite=2):
        self.n = n
        self.target_cols = cols_from_pairs(target_pairs or generate_solution(n), n)
        self.P=pop_size; self.mrate=mutate_rate; self.elite=elite
        self.reset()
    def reset(self):
        self.pop=[random_permutation(self.n) for _ in range(self.P)]
        self.generation=0; self.best=max(self.pop, key=self._fitness)
        self.cur_state=self.best[:]; self.last_added=None
    def _fitness(self, cols):
        match = sum(1 for r in range(self.n) if cols[r]==self.target_cols[r])
        conf = diag_conflicts(cols)
        return match*10 - conf*2
    def _tournament(self, k=3):
        cand = random.sample(self.pop, k)
        return max(cand, key=self._fitness)
    def _order_crossover(self,p1,p2):
        n=self.n; a,b=sorted(random.sample(range(n),2))
        child=[-1]*n; child[a:b+1]=p1[a:b+1]
        fill=[x for x in p2 if x not in child]; j=0
        for i in range(n):
            if child[i]==-1: child[i]=fill[j]; j+=1
        return child
    def _mutate(self, ind):
        if random.random()<self.mrate:
            i,j=random.sample(range(self.n),2); ind[i],ind[j]=ind[j],ind[i]
    def is_goal(self, cols):
        return all(cols[r]==self.target_cols[r] for r in range(self.n))
    def step(self):
        if self.is_goal(self.best):
            return {'state': self.best[:], 'added': None, 'found': True, 'progressed': True}
        ranked = sorted(self.pop, key=self._fitness, reverse=True)
        new_pop = ranked[:self.elite]
        while len(new_pop)<self.P:
            p1=self._tournament(); p2=self._tournament()
            child=self._order_crossover(p1,p2); self._mutate(child)
            new_pop.append(child)
        self.pop=new_pop; self.generation+=1
        new_best=max(self.pop, key=self._fitness)
        if new_best!=self.best:
            for r in range(self.n):
                if new_best[r]!=self.best[r]:
                    self.last_added=(r, new_best[r]); break
        self.best=new_best; self.cur_state=self.best[:]
        return {'state': self.cur_state[:], 'added': self.last_added, 'found': self.is_goal(self.best), 'progressed': True}