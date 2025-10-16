import random

def generate_solution(n=8):
    cols = [-1]*n
    used_cols, used_d1, used_d2 = set(), set(), set()
    def place(r):
        if r == n: return True
        cs = list(range(n)); random.shuffle(cs)
        for c in cs:
            if (c in used_cols) or ((r-c) in used_d1) or ((r+c) in used_d2):
                continue
            cols[r] = c
            used_cols.add(c); used_d1.add(r-c); used_d2.add(r+c)
            if place(r+1): return True
            used_cols.remove(c); used_d1.remove(r-c); used_d2.remove(r+c)
            cols[r] = -1
        return False
    place(0)
    return [(r, cols[r]) for r in range(n)]

def cols_from_pairs(pairs, n=8):
    cols = [-1]*n
    for (r,c) in pairs: cols[r] = c
    return cols

def pair_list_from_cols(cols):
    return [(r, cols[r]) for r in range(len(cols)) if cols[r] != -1]

def is_safe_partial(state_cols, row, c):
    for r_prev, c_prev in enumerate(state_cols):
        if (c == c_prev) or (abs(row - r_prev) == abs(c - c_prev)):
            return False
    return True

def neighbors_partial(state_cols, n):
    row = len(state_cols)
    if row >= n: return []
    res = []
    for c in range(n):
        if is_safe_partial(state_cols, row, c):
            res.append(state_cols + [c])
    return res

def random_permutation(n=8):
    arr = list(range(n))
    random.shuffle(arr)
    return arr

def diag_conflicts(cols):
    n = len(cols)
    cnt = 0
    for i in range(n):
        for j in range(i+1, n):
            if abs(i-j) == abs(cols[i] - cols[j]):
                cnt += 1
    return cnt
