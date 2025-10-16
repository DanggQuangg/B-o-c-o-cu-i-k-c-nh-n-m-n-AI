from collections import deque
class StepBeliefSearch:
    def __init__(self, n=8):
        self.n = n
        self.reset()
    def reset(self):
        self.queue = deque()
        init_domains = [set(range(self.n)) for _ in range(self.n)]
        init_assign = [-1]*self.n
        self.queue.append((init_assign, init_domains))
        self.cur_assign = [-1]*self.n
        self.last_added = None
    def _safe_after(self, assign, row, c):
        for r_prev, c_prev in enumerate(assign):
            if c_prev == -1: continue
            if c_prev == c or abs(row - r_prev) == abs(c - c_prev):
                return False
        return True
    def _prune(self, assign, domains, row, val):
        # trả về bản sao domains sau khi gán row=val
        n = self.n
        new_domains = [set(d) for d in domains]
        new_domains[row] = {val}
        for r in range(n):
            if r == row: continue
            if assign[r] != -1:
                new_domains[r] = {assign[r]}
                continue
            bad = set()
            for v in new_domains[r]:
                if v == val or abs(r - row) == abs(v - val):
                    bad.add(v)
            if bad:
                new_domains[r] -= bad
        return new_domains
    def step(self):
        if not self.queue:
            return {'state': self.cur_assign[:], 'added': None, 'found': False, 'progressed': False}
        assign, domains = self.queue.popleft()
        # goal?
        if all(a != -1 for a in assign):
            self.cur_assign = assign[:]
            return {'state': assign[:], 'added': None, 'found': True, 'progressed': True}
        # chọn hàng chưa gán có miền nhỏ nhất (MRV)
        cand = [(len(domains[r]), r) for r in range(self.n) if assign[r] == -1]
        if not cand:
            return {'state': assign[:], 'added': None, 'found': False, 'progressed': False}
        _, row = min(cand)
        values = sorted(list(domains[row]))
        children = []
        for v in values:
            if not self._safe_after(assign, row, v): 
                continue
            child_assign = assign[:]
            child_assign[row] = v
            child_domains = self._prune(child_assign, domains, row, v)
            # loại node chết
            if any(len(child_domains[r]) == 0 for r in range(self.n) if child_assign[r] == -1):
                continue
            children.append((child_assign, child_domains))
        # enqueue tất cả child
        for node in children:
            self.queue.append(node)
        # hiển thị child đầu tiên (nếu có)
        if children:
            self.cur_assign = children[0][0][:]
            last_row = next(i for i, val in enumerate(self.cur_assign) if val != assign[i])
            self.last_added = (last_row, self.cur_assign[last_row])
            return {'state': self.cur_assign[:], 'added': self.last_added, 'found': all(a!=-1 for a in self.cur_assign), 'progressed': True}
        # không có child
        self.cur_assign = assign[:]
        return {'state': assign[:], 'added': None, 'found': False, 'progressed': True}
