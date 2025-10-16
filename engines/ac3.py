from collections import deque
from core.nqueens_utils import (
    cols_from_pairs,
    generate_solution,
)
from collections import deque
from core.nqueens_utils import cols_from_pairs
class StepAC3:
    """
    MAC (Maintaining Arc Consistency) + backtrack theo MRV, target-mode:
    - assign: list độ dài n, -1 nếu chưa gán
    - domains[i]: tập cột hợp lệ cho hàng i
    - arc_q: hàng đợi các cung (i, j) để revise Di theo Dj
    - mỗi tick: ưu tiên propagate 1 arc; nếu rỗng thì thử gán 1 biến (MRV)
    """
    def __init__(self, n=8, target_pairs=None):
        self.n = n
        self.target_cols = cols_from_pairs(target_pairs or generate_solution(n), n)
        self.reset()

    def reset(self):
        n = self.n
        self.assign = [-1] * n
        self.domains = [set(range(n)) for _ in range(n)]
        # Ưu tiên domain chứa target trước (không bắt buộc, chỉ giúp hội tụ nhanh)
        for r in range(n):
            tc = self.target_cols[r]
            if tc != -1 and tc in self.domains[r]:
                # Đưa target lên "ưu tiên" bằng cách giữ nguyên set nhưng ta sẽ chọn tc trước khi thử giá trị khác.
                pass
        self.arc_q = deque((i, j) for i in range(n) for j in range(n) if i != j)
        self.stack = []  # (domains_snapshot, arc_snapshot, assign_snapshot)
        self.last_added = None

    def is_goal(self):
        return all(self.assign[r] != -1 for r in range(self.n)) and \
               all(self.assign[r] == self.target_cols[r] for r in range(self.n))

    def _consistent_pair(self, ri, vi, rj, vj):
        if vi == vj:
            return False
        return abs(ri - rj) != abs(vi - vj)

    def _revise(self, xi, xj):
        removed = set()
        Di = self.domains[xi]; Dj = self.domains[xj]
        if not Dj:
            # nếu Dj rỗng thì Di chắc chắn sẽ bị xóa hết ở vòng sau (backtrack sẽ xử lý)
            return removed
        for vi in list(Di):
            ok = False
            for vj in Dj:
                if self._consistent_pair(xi, vi, xj, vj):
                    ok = True
                    break
            if not ok:
                Di.remove(vi)
                removed.add(vi)
        return removed

    def _enqueue_arcs_from(self, xk, excluding=None):
        for i in range(self.n):
            if i != xk and i != excluding:
                self.arc_q.append((i, xk))

    def _mrv_unassigned(self):
        # chọn biến chưa gán có domain nhỏ nhất; tie-break theo index
        cand = [(len(self.domains[i]), i) for i in range(self.n) if self.assign[i] == -1]
        if not cand:
            return None
        cand.sort()
        return cand[0][1]

    def _snapshot(self):
        return [set(s) for s in self.domains], deque(self.arc_q), self.assign[:]

    def _restore(self, doms, arcq, assign):
        self.domains = [set(s) for s in doms]
        self.arc_q = deque(arcq)
        self.assign = assign[:]

    def step(self):
        # 1) Propagate một arc nếu còn
        if self.arc_q:
            xi, xj = self.arc_q.popleft()
            removed = self._revise(xi, xj)
            if removed:
                # domain rỗng -> backtrack
                if not self.domains[xi]:
                    if not self.stack:
                        return {'state': self.assign[:], 'added': None, 'found': False, 'progressed': False}
                    doms, arcq, assign = self.stack.pop()
                    self._restore(doms, arcq, assign)
                    self.last_added = None
                    return {'state': self.assign[:], 'added': None, 'found': False, 'progressed': True}
                # có thay đổi -> enqueue lại các cung (k|xi), k≠xi,xj
                self._enqueue_arcs_from(xi, excluding=xj)
            return {'state': self.assign[:], 'added': self.last_added, 'found': self.is_goal(), 'progressed': True}

        # 2) Không còn arc để propagate: thử gán một biến (MRV)
        if self.is_goal():
            return {'state': self.assign[:], 'added': self.last_added, 'found': True, 'progressed': True}

        var = self._mrv_unassigned()
        if var is None:
            return {'state': self.assign[:], 'added': None, 'found': False, 'progressed': False}

        # Sắp xếp domain: ưu tiên target trước để khớp đích
        target_first = self.target_cols[var]
        domain_list = sorted(self.domains[var], key=lambda x: (x != target_first, x))

        if not domain_list:
            # Backtrack
            if not self.stack:
                return {'state': self.assign[:], 'added': None, 'found': False, 'progressed': False}
            doms, arcq, assign = self.stack.pop()
            self._restore(doms, arcq, assign)
            self.last_added = None
            return {'state': self.assign[:], 'added': None, 'found': False, 'progressed': True}

        # Snapshot trước khi thử một giá trị (để có thể backtrack)
        doms_snap, arcq_snap, assign_snap = self._snapshot()
        self.stack.append((doms_snap, arcq_snap, assign_snap))

        # Thử giá trị đầu tiên
        v = domain_list[0]
        self.assign[var] = v
        self.last_added = (var, v)

        # Thu hẹp domain của var thành singleton
        self.domains[var] = {v}
        # Enqueue các cung (k -> var) để propagate
        self.arc_q.clear()
        self._enqueue_arcs_from(var)

        return {'state': self.assign[:], 'added': self.last_added, 'found': self.is_goal(), 'progressed': True}