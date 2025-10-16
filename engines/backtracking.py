# engines/backtracking.py
from typing import Callable, Optional

class StepBacktracking:
    """
    Backtracking chuẩn cho N-Queens (từng-bước/step-by-step):
    - Mỗi lần step(): hoặc đặt 1 quân (place) hoặc backtrack gỡ 1 quân (remove).
    - Có logger để in ra từng bước (try/place/backtrack).
    - Khi đủ n hàng -> found=True, trả về nghiệm đầy đủ.

    Keys trả về từ step():
      - 'state'      : danh sách cột đã đặt theo hàng hiện tại (partial), VD: [0,4,7]
      - 'added'      : (r, c) nếu vừa đặt 1 quân; None nếu không
      - 'removed'    : (r, c) nếu vừa backtrack gỡ 1 quân; None nếu không
      - 'action'     : 'place' | 'backtrack' | 'done'
      - 'found'      : True nếu đã hoàn tất lời giải
      - 'progressed' : True nếu có hành động trong step này
    """

    def __init__(self, n=8, target_pairs=None):
        self.n = n
        self._logger: Optional[Callable[[str], None]] = None
        self.reset()

    # ====== Public helpers ======
    def set_logger(self, fn: Callable[[str], None]):
        """Gắn hàm log, ví dụ: engine.set_logger(log_message1)"""
        self._logger = fn

    def reset(self):
        self.cols = [-1] * self.n   # cols[r] = c nếu đã đặt, -1 nếu chưa
        self.row = 0                # hàng hiện đang xét
        self.next_c = 0             # cột tiếp theo sẽ thử ở hàng hiện tại
        self.done = False
        self.solution = None
        self._last_added = None

    # ====== Internal helpers ======
    def _log(self, msg: str):
        if self._logger:
            self._logger(msg)

    @staticmethod
    def _is_safe(cols, r, c):
        # Kiểm tra xung đột với các hàng [0..r-1]
        for rr in range(r):
            cc = cols[rr]
            if cc == -1:
                continue
            if cc == c or abs(rr - r) == abs(cc - c):
                return False
        return True

    # ====== One visible step per call ======
    def step(self):
        if self.done:
            return {
                'state': self.solution[:] if self.solution else [c for c in self.cols if c != -1],
                'added': None,
                'removed': None,
                'action': 'done',
                'found': self.solution is not None,
                'progressed': False
            }

        n = self.n

        # 1) Nếu đã đặt đủ n hàng -> hoàn tất
        if self.row == n:
            self.solution = self.cols[:]
            self.done = True
            self._log("✔ ĐÃ TÌM THẤY LỜI GIẢI: " + str(self.solution))
            return {
                'state': self.solution[:],
                'added': None,
                'removed': None,
                'action': 'done',
                'found': True,
                'progressed': True
            }

        # 2) Thử các cột từ next_c..n-1 tại hàng self.row
        r = self.row
        for c in range(self.next_c, n):
            self._log(f"Thử r={r}, c={c} ...")
            if self._is_safe(self.cols, r, c):
                # Đặt quân tại (r, c)
                self.cols[r] = c
                self._last_added = (r, c)
                self._log(f"→ ĐẶT (r={r}, c={c}) ✓")
                # Chuẩn bị sang hàng tiếp theo
                self.row = r + 1
                self.next_c = 0
                return {
                    'state': [self.cols[i] for i in range(self.row)],  # partial để vẽ
                    'added': (r, c),
                    'removed': None,
                    'action': 'place',
                    'found': (self.row == n),
                    'progressed': True
                }

        # 3) Không có cột hợp lệ ở hàng r -> backtrack
        #    Quay về hàng r-1, tăng next_c để thử cột kế tiếp
        if r == 0:
            # vô nghiệm (n=8 thì không xảy ra), đánh dấu done
            self.done = True
            self._log("✖ HẾT NHÁNH: vô nghiệm.")
            return {
                'state': [],
                'added': None,
                'removed': None,
                'action': 'done',
                'found': False,
                'progressed': False
            }

        # Gỡ quân hàng r-1
        prev_r = r - 1
        prev_c = self.cols[prev_r]
        self.cols[prev_r] = -1
        self.row = prev_r
        self.next_c = prev_c + 1
        self._log(f"↩ BACKTRACK: gỡ (r={prev_r}, c={prev_c}), quay lại thử cột {self.next_c}...")

        return {
            'state': [self.cols[i] for i in range(self.row)],  # partial sau khi gỡ
            'added': None,
            'removed': (prev_r, prev_c),
            'action': 'backtrack',
            'found': False,
            'progressed': True
        }
