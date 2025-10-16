from core.nqueens_utils import (
    cols_from_pairs,
    generate_solution,
)
class StepForwardChecking:
    """
    Mỗi hàng là biến, domain ban đầu = {0..7}.
    Khi gán row=r -> c, loại bỏ cột và chéo khỏi domain các hàng sau.
    Dừng khi cols == target_cols.
    """
    def __init__(self, n=8, target_pairs=None):
        self.n = n
        self.target_cols = cols_from_pairs(target_pairs or generate_solution(n), n)
        self.reset()
    def reset(self):
        n=self.n
        self.assign = []               # list cột đã gán theo hàng 0..k-1
        self.domains = [set(range(n)) for _ in range(n)]
        self.stack = []               # lưu (assign_len_before, removed_list_for_each_row)
        self.last_added = None
    def is_goal(self):
        return len(self.assign)==self.n and all(self.assign[r]==self.target_cols[r] for r in range(self.n))
    def _forward_prune(self, r, c):
        """
        Sau khi gán row=r -> c, loại bỏ khỏi domain của các hàng > r:
        - c (trùng cột)
        - c±d cho d = (row' - r) (chéo)
        Trả về danh sách các (row', removed_values_set) để có thể undo khi backtrack.
        """
        removed = [set() for _ in range(self.n)]
        n=self.n
        for rr in range(r+1, n):
            to_remove=set()
            if c in self.domains[rr]: to_remove.add(c)
            d = rr - r
            if (c-d) in self.domains[rr]: to_remove.add(c-d)
            if (c+d) in self.domains[rr]: to_remove.add(c+d)
            for v in to_remove:
                self.domains[rr].remove(v)
            removed[rr]=to_remove
        return removed
    def _undo_prune(self, removed):
        for rr, s in enumerate(removed):
            for v in s:
                self.domains[rr].add(v)
    def step(self):
        # goal?
        if self.is_goal():
            return {'state': self.assign[:], 'added': self.last_added, 'found': True, 'progressed': True}
        r = len(self.assign)
        # nếu domain r trống -> backtrack
        while True:
            if r<self.n and not self.domains[r]:
                # backtrack
                if not self.stack:
                    return {'state': self.assign[:], 'added': None, 'found': False, 'progressed': False}
                prev_r, removed, c_used = self.stack.pop()
                # undo gán
                self.assign.pop()
                # khôi phục domain đã xóa
                self._undo_prune(removed)
                # loại bỏ giá trị đã dùng khỏi domain hiện tại (để thử giá trị kế tiếp)
                if c_used in self.domains[prev_r]:
                    self.domains[prev_r].discard(c_used)
                r = prev_r
            else:
                break
        if r==self.n:
            return {'state': self.assign[:], 'added': self.last_added, 'found': self.is_goal(), 'progressed': True}
        # chọn một giá trị từ domain[r] (ưu tiên cột mục tiêu trước cho nhanh)
        domain_list = sorted(self.domains[r], key=lambda x: (x!=self.target_cols[r], x))
        if not domain_list:
            # sẽ backtrack ở tick kế
            return {'state': self.assign[:], 'added': None, 'found': False, 'progressed': False}
        c = domain_list[0]
        # gán
        self.assign.append(c)
        removed = self._forward_prune(r, c)
        self.stack.append((r, removed, c))
        self.last_added = (r, c)
        return {'state': self.assign[:], 'added': self.last_added, 'found': self.is_goal(), 'progressed': True}