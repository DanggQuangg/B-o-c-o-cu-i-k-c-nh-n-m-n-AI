# engines/search_step.py
import heapq
from collections import deque
from core.nqueens_utils import (
    cols_from_pairs,
    neighbors_partial,
)
class StepSearch:
    """
    - target-mode (BFS/DFS/DLS/IDS): dừng khi trùng bảng đích.
    - any-solution-mode (GREEDY/A*/UCS): dừng khi đủ n hậu (không dùng đích).
    """
    def __init__(self, algo, n, target_pairs, dls_limit=None, step_logger=None):
        self.algo = algo.upper()
        self.n = n
        self.target_cols = cols_from_pairs(target_pairs, n)
        self.step_logger = step_logger
        self.queue = deque()
        self.stack = []
        self.heap = []
        self.heap_counter = 0
        self.ids_limit = 0
        self.ids_max = n
        self.dls_limit = dls_limit if dls_limit is not None else n
        self.goal_any_solution = (self.algo in {"GREEDY", "A*", "UCS"})
        self.reset()

    def g_cost(self, cols): return len(cols)
    def h_cost(self, cols): return self.n - len(cols)
    def f_cost(self, cols):
        if self.algo == "UCS": return self.g_cost(cols)
        if self.algo == "GREEDY": return self.h_cost(cols)
        if self.algo == "A*": return self.g_cost(cols) + self.h_cost(cols)
        return 0

    def push_heap(self, node):
        f = self.f_cost(node)
        self.heap_counter += 1
        heapq.heappush(self.heap, (f, self.heap_counter, node))

    def pop_heap(self):
        if not self.heap: return None
        f, _, node = heapq.heappop(self.heap); return node

    def reset(self):
        self.queue.clear(); self.stack.clear(); self.heap.clear()
        self.heap_counter = 0
        self.last_added = None
        self.cur_state = []
        if self.algo == "BFS":
            self.queue.append([])
        elif self.algo in ("DFS", "DLS"):
            self.stack.append([])
        elif self.algo == "IDS":
            self.ids_limit = 0; self.stack.append([])
        elif self.algo in {"GREEDY", "A*", "UCS"}:
            self.push_heap([])

    def is_goal(self, cols):
        if self.goal_any_solution:
            return len(cols) == self.n
        if len(cols) != self.n: return False
        tgt = self.target_cols
        return all(cols[r] == tgt[r] for r in range(self.n))

    def step(self):
        # Greedy/A*/UCS
        if self.algo in {"GREEDY", "A*", "UCS"}:
            node = self.pop_heap()
            if node is None:
                return {'state': self.cur_state, 'added': None, 'found': False, 'progressed': False}
            self.cur_state = node[:]
            if len(node) > 0:
                self.last_added = (len(node)-1, node[-1])
            if self.is_goal(node):
                return {'state': node, 'added': self.last_added, 'found': True, 'progressed': True}
            for child in neighbors_partial(node, self.n):
                self.push_heap(child)
            return {'state': node, 'added': self.last_added, 'found': False, 'progressed': True}

        # BFS
        if self.algo == "BFS":
            if not self.queue:
                return {'state': self.cur_state, 'added': None, 'found': False, 'progressed': False}
            node = self.queue.popleft()
            self.cur_state = node[:]
            if len(node) > 0: self.last_added = (len(node)-1, node[-1])
            if self.is_goal(node):
                return {'state': node, 'added': self.last_added, 'found': True, 'progressed': True}
            for child in neighbors_partial(node, self.n):
                self.queue.append(child)
            return {'state': node, 'added': self.last_added, 'found': False, 'progressed': True}

        # DFS
        if self.algo == "DFS":
            if not self.stack:
                return {'state': self.cur_state, 'added': None, 'found': False, 'progressed': False}
            node = self.stack.pop()
            self.cur_state = node[:]
            if len(node) > 0: self.last_added = (len(node)-1, node[-1])
            if self.is_goal(node):
                return {'state': node, 'added': self.last_added, 'found': True, 'progressed': True}
            childs = neighbors_partial(node, self.n)
            for child in reversed(childs): self.stack.append(child)
            return {'state': node, 'added': self.last_added, 'found': False, 'progressed': True}

        # DLS
        if self.algo == "DLS":
            if not self.stack:
                return {'state': self.cur_state, 'added': None, 'found': False, 'progressed': False}
            node = self.stack.pop()
            self.cur_state = node[:]
            if len(node) > 0: self.last_added = (len(node)-1, node[-1])
            if self.is_goal(node):
                return {'state': node, 'added': self.last_added, 'found': True, 'progressed': True}
            if len(node) < self.dls_limit:
                childs = neighbors_partial(node, self.n)
                for child in reversed(childs): self.stack.append(child)
            return {'state': node, 'added': self.last_added, 'found': False, 'progressed': True}

        # IDS
        if self.algo == "IDS":
            if not self.stack:
                if self.ids_limit >= self.ids_max:
                    return {'state': self.cur_state, 'added': None, 'found': False, 'progressed': False}
                self.ids_limit += 1
                self.stack.append([])
            node = self.stack.pop()
            self.cur_state = node[:]
            if len(node) > 0: self.last_added = (len(node)-1, node[-1])
            if self.is_goal(node):
                return {'state': node, 'added': self.last_added, 'found': True, 'progressed': True}
            if len(node) < self.ids_limit:
                childs = neighbors_partial(node, self.n)
                for child in reversed(childs): self.stack.append(child)
            return {'state': node, 'added': self.last_added, 'found': False, 'progressed': True}

        return {'state': self.cur_state, 'added': None, 'found': False, 'progressed': False}
