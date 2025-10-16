from core.nqueens_utils import (
    cols_from_pairs,
    generate_solution,
    is_safe_partial,
)
class StepBacktracking:
    """
    DFS theo hàng, đặt hậu hợp lệ; dừng khi cols == target_cols.
    Mỗi tick mở rộng/backtrack một bước.
    """
    def __init__(self, n=8, target_pairs=None):
        self.n = n
        self.target_cols = cols_from_pairs(target_pairs or generate_solution(n), n)
        self.reset()
    def reset(self):
        self.stack = [([], 0)]  # (partial_cols, next_col_to_try)
        self.last_added = None
        self.cur_state = []
    def is_goal(self, cols):
        return len(cols)==self.n and all(cols[r]==self.target_cols[r] for r in range(self.n))
    def step(self):
        if not self.stack:
            return {'state': self.cur_state, 'added': None, 'found': False, 'progressed': False}
        cols, next_c = self.stack.pop()
        r = len(cols)
        self.cur_state = cols[:]
        self.last_added = (r-1, cols[-1]) if r>0 else None
        # goal?
        if self.is_goal(cols):
            return {'state': cols, 'added': self.last_added, 'found': True, 'progressed': True}
        # try next candidates from next_c..n-1
        progressed = False
        for c in range(next_c, self.n):
            if is_safe_partial(cols, r, c):
                # push continuation (try more columns later)
                self.stack.append((cols, c+1))
                # push child now
                self.stack.append((cols+[c], 0))
                progressed = True
                break
        return {'state': cols, 'added': self.last_added, 'found': False, 'progressed': progressed}