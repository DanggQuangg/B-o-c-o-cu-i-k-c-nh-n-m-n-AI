class StepAndOrSearch:
    """OR node: chọn cột cho hàng r; AND node: kiểm tra ràng buộc (deterministic -> chuyển sang OR của r+1)."""
    def __init__(self, n=8):
        self.n = n
        self.reset()
    def reset(self):
        self.stack = []  # khung: ('OR', row, assign(list), next_c)
        self.stack.append(('OR', 0, [-1]*self.n, 0))
        self.cur_assign = [-1]*self.n
        self.last_added = None
    def _safe(self, assign, r, c):
        for i in range(r):
            ci = assign[i]
            if ci == -1: continue
            if ci == c or abs(r-i) == abs(c-ci):
                return False
        return True
    def step(self):
        if not self.stack:
            return {'state': self.cur_assign[:], 'added': None, 'found': False, 'progressed': False}
        typ, row, assign, next_c = self.stack.pop()
        if row == self.n:
            self.cur_assign = assign[:]
            return {'state': assign[:], 'added': None, 'found': True, 'progressed': True}
        if typ == 'OR':
            n = self.n
            # tìm c hợp lệ từ next_c
            c = next_c
            while c < n and not self._safe(assign, row, c):
                c += 1
            if c < n:
                # vẫn còn lựa chọn tại row -> giữ OR node lại cho c kế tiếp
                self.stack.append(('OR', row, assign[:], c+1))
                # tạo AND node: xác nhận gán (row=c), rồi chuyển sang OR của row+1
                new_assign = assign[:]
                new_assign[row] = c
                self.stack.append(('OR', row+1, new_assign, 0))
                self.cur_assign = new_assign[:]
                self.last_added = (row, c)
                return {'state': new_assign[:], 'added': self.last_added, 'found': (row+1==self.n), 'progressed': True}
            else:
                # hết lựa chọn -> backtrack
                self.cur_assign = assign[:]
                return {'state': assign[:], 'added': None, 'found': False, 'progressed': True}
        # không có AND riêng vì ràng buộc được kiểm ngay khi chọn c
        return {'state': self.cur_assign[:], 'added': None, 'found': False, 'progressed': True}