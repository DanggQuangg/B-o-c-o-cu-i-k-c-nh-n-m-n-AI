from collections import deque
from typing import Optional, Callable

class StepAC3:
    def __init__(self, n=8, target_pairs=None):
        self.n = n
        self._logger: Optional[Callable[[str], None]] = None
        self.reset()

    def set_logger(self, fn: Callable[[str], None]):
        self._logger = fn

    def reset(self):
        n = self.n
        self.assign = [-1] * n
        self.domains = [set(range(n)) for _ in range(n)]
        self.arc_q = deque()
        self.stack = []
        self._enqueue_all_arcs()
        self.done = False
        self.solution = None
        self.last_added = None


    def _log(self, s: str):
        if self._logger:
            self._logger(s)

    @staticmethod
    def _consistent_pair(ri, vi, rj, vj) -> bool:
        if vi == vj:  
            return False
        return abs(ri - rj) != abs(vi - vj)  
    def _enqueue_all_arcs(self):
        self.arc_q.clear()
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    self.arc_q.append((i, j))

    def _enqueue_arcs_from(self, var):
        for k in range(self.n):
            if k != var:
                self.arc_q.append((k, var))

    def _revise(self, xi, xj) -> bool:

        Di = self.domains[xi]
        Dj = self.domains[xj]
        if not Dj:
            return False

        removed_any = False
        to_remove = set()
        for vi in Di:
            ok = False
            for vj in Dj:
                if self._consistent_pair(xi, vi, xj, vj):
                    ok = True
                    break
            if not ok:
                to_remove.add(vi)

        if to_remove:
            Di.difference_update(to_remove)
            removed_any = True
            self._log(f"revise: D[{xi}] -= {sorted(to_remove)} -> {sorted(Di)}")

        return removed_any

    def _select_unassigned_mrv(self):
        mrv_var = None
        mrv_size = 10**9
        for r in range(self.n):
            if self.assign[r] != -1:
                continue
            size = len(self.domains[r])
            if size == 0:
                return r
            if size < mrv_size:
                mrv_size = size
                mrv_var = r
        return mrv_var  

    def _snapshot(self):
        doms = [set(s) for s in self.domains]
        arcq = deque(self.arc_q)
        assign = self.assign[:]
        return doms, arcq, assign

    def _restore(self, snap):
        doms, arcq, assign = snap
        self.domains = [set(s) for s in doms]
        self.arc_q = deque(arcq)
        self.assign = assign[:]

    def step(self):
        if self.done:
            return {
                'state': self.solution[:] if self.solution else self.assign[:],
                'added': None,
                'removed': None,
                'action': 'done',
                'found': self.solution is not None,
                'progressed': False
            }

        n = self.n

        if all(v != -1 for v in self.assign):
            self.solution = self.assign[:]
            self.done = True
            self._log("✔ AC-3/MAC: ĐÃ TÌM THẤY LỜI GIẢI " + str(self.solution))
            return {
                'state': self.solution[:],
                'added': None,
                'removed': None,
                'action': 'done',
                'found': True,
                'progressed': True
            }

        if self.arc_q:
            xi, xj = self.arc_q.popleft()
            changed = self._revise(xi, xj)
            if changed:
                if len(self.domains[xi]) == 0:
                    if not self.stack:
                        self.done = True
                        self._log(f"✖ AC-3: D[{xi}] rỗng, vô nghiệm.")
                        return {
                            'state': [],
                            'added': None,
                            'removed': None,
                            'action': 'done',
                            'found': False,
                            'progressed': False
                        }
                    snap = self.stack.pop()
                    prev_assign = snap[2]
                    cur_assign = self.assign
                    removed = None
                    for r in range(n):
                        if prev_assign[r] != -1 and cur_assign[r] == -1:
                            removed = (r, prev_assign[r])
                            break
                    self._restore(snap)
                    self._log("↩ BACKTRACK (do domain rỗng sau revise)")
                    return {
                        'state': self.assign[:],
                        'added': None,
                        'removed': removed,
                        'action': 'backtrack',
                        'found': False,
                        'progressed': True
                    }
                for xk in range(n):
                    if xk != xi and xk != xj:
                        self.arc_q.append((xk, xi))
            return {
                'state': self.assign[:],
                'added': None,
                'removed': None,
                'action': 'revise',
                'found': False,
                'progressed': True
            }

        var = self._select_unassigned_mrv()
        if var is None:
            self.solution = self.assign[:]
            self.done = True
            return {
                'state': self.solution[:],
                'added': None,
                'removed': None,
                'action': 'done',
                'found': True,
                'progressed': True
            }

        if len(self.domains[var]) == 0:
            if not self.stack:
                self.done = True
                self._log(f"✖ AC-3: MRV chọn var={var} nhưng domain rỗng, vô nghiệm.")
                return {
                    'state': [],
                    'added': None,
                    'removed': None,
                    'action': 'done',
                    'found': False,
                    'progressed': False
                }
            snap = self.stack.pop()
            prev_assign = snap[2]
            removed = None
            for r in range(n):
                if prev_assign[r] != -1 and self.assign[r] == -1:
                    removed = (r, prev_assign[r])
                    break
            self._restore(snap)
            self._log("↩ BACKTRACK (MRV domain rỗng)")
            return {
                'state': self.assign[:],
                'added': None,
                'removed': removed,
                'action': 'backtrack',
                'found': False,
                'progressed': True
            }

        v = min(self.domains[var])
        self.stack.append(self._snapshot())

        self.assign[var] = v
        self.domains[var] = {v}
        self.last_added = (var, v)
        self._log(f"→ PLACE: (r={var}, c={v})")

        self._enqueue_arcs_from(var)

        return {
            'state': self.assign[:],
            'added': (var, v),
            'removed': None,
            'action': 'place',
            'found': all(x != -1 for x in self.assign),
            'progressed': True
        }
