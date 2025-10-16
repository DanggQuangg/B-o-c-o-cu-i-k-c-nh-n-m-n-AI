from core.nqueens_utils import (
    cols_from_pairs,
)
class StepPartialBelief:
    """
    Cần bảng đích 'một phần': target_pairs có thể chứa (-1) ngầm (hàng không chỉ định).
    - Hàng r nếu target_cols[r] != -1 -> bắt buộc đặt c = target_cols[r]
    - Ngược lại -> c bất kỳ an toàn
    Dừng khi gán đủ n hàng và mọi hàng có chỉ định đều khớp.
    """
    def __init__(self, n=8, target_pairs=None):
        self.n = n
        self.target_cols = cols_from_pairs(target_pairs or [], n)
        self.reset()
    def reset(self):
        self.stack = []  # DFS trên hoán vị từng hàng
        self.stack.append([])  # state là list cột đã đặt cho 0..row-1
        self.cur_state = []
        self.last_added = None
    def _goal_ok(self, cols):
        if len(cols) != self.n: return False
        for r in range(self.n):
            tc = self.target_cols[r]
            if tc != -1 and cols[r] != tc:
                return False
        return True
    def _safe_partial(self, cols, r, c):
        for i, ci in enumerate(cols):
            if ci == c or abs(r - i) == abs(c - ci):
                return False
        return True
    def step(self):
        if not self.stack:
            return {'state': self.cur_state[:], 'added': None, 'found': False, 'progressed': False}
        node = self.stack.pop()
        self.cur_state = node[:]
        if len(node) == self.n:
            return {'state': node[:], 'added': None, 'found': self._goal_ok(node), 'progressed': True}
        r = len(node)
        tc = self.target_cols[r]
        children = []
        if tc != -1:
            if self._safe_partial(node, r, tc):
                children.append(node + [tc])
        else:
            for c in range(self.n):
                if self._safe_partial(node, r, c):
                    children.append(node + [c])
        # push DFS (để duyệt trái->phải tự nhiên)
        for child in reversed(children):
            self.stack.append(child)
        if children:
            child = children[0]
            self.last_added = (r, child[-1])
            return {'state': child[:], 'added': self.last_added, 'found': len(child)==self.n and self._goal_ok(child), 'progressed': True}
        return {'state': node[:], 'added': None, 'found': False, 'progressed': True}