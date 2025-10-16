import tkinter as tk
from collections import deque

from ui.boards import taobanco_fixed, veoco_fixed, load_queen_image
from core.nqueens_utils import generate_solution, pair_list_from_cols
from core.engine_registry import ALGO_BUTTONS, make_engine

# ===== Trạng thái chung =====
delay = 170
speed_fast = False
running = False
n = 8

def log_step(text):
    log_list.insert(tk.END, text)
    log_list.see(tk.END)

def toggle_speed():
    global delay, speed_fast
    speed_fast = not speed_fast
    delay = max(10, delay // 2) if speed_fast else 170
    status = "x2 tốc độ" if speed_fast else "tốc độ thường"
    log_step(f"[Speed] {status}. delay = {delay}ms")

# ===== Tkinter App =====
root = tk.Tk()
root.title("8 Hậu – Sidebar thuật toán + Nhật ký bước đi")
root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=1, uniform="boards")
root.grid_columnconfigure(2, weight=1, uniform="boards")
root.grid_rowconfigure(0, weight=1)

sidebar = tk.Frame(root, padx=8, pady=8); sidebar.grid(row=0, column=0, sticky="nsw")
algo_box = tk.LabelFrame(sidebar, text="Thuật toán", padx=6, pady=6); algo_box.pack(fill="x", anchor="n")
btn_container = tk.Frame(algo_box); btn_container.pack(fill="both", expand=True)
for i in range(9): btn_container.grid_rowconfigure(i, weight=0)
for j in range(2): btn_container.grid_columnconfigure(j, weight=1)

current_algo_var = tk.StringVar(value="(chưa chọn)")
log_box = tk.LabelFrame(sidebar, text="Các bước đã đi (tọa độ)", padx=6, pady=6)
log_box.pack(fill="both", expand=True, pady=(8,0))
log_list = tk.Listbox(log_box, height=20)
log_scroll = tk.Scrollbar(log_box, orient="vertical", command=log_list.yview)
log_list.config(yscrollcommand=log_scroll.set)
log_list.pack(side="left", fill="both", expand=True); log_scroll.pack(side="right", fill="y")
status_lbl = tk.Label(sidebar, textvariable=current_algo_var, fg="#777"); status_lbl.pack(anchor="w", pady=(6,0))

# Boards
khungtrai, bancotrai, cells_trai = taobanco_fixed(root, "Bàn cờ (quá trình)")
khungphai, bancophai, cells_phai = taobanco_fixed(root, "Bàn cờ mục tiêu")
khungtrai.grid(row=0, column=1, sticky="nsew", padx=(6,8), pady=10)
khungphai.grid(row=0, column=2, sticky="nsew", padx=(0,10), pady=10)

queen_img = load_queen_image("assets/queen.jpg")

# Target mặc định
muc_tieu = generate_solution(n)
veoco_fixed(cells_phai, queens=muc_tieu, queenimg=queen_img)
veoco_fixed(cells_trai, queens=[], queenimg=queen_img)

# Engine hiện hành
engine = None

def start_animation():
    global running
    running = True

    def tick():
        global running
        if not running: return

        if engine is not None:
            res = engine.step()

            cur_pairs = []
            state_cols = res.get('state', [])
            if isinstance(state_cols, list):
                cur_pairs = pair_list_from_cols(state_cols)

            veoco_fixed(cells_trai, queens=cur_pairs, queenimg=queen_img, highlight=res.get('added'))
            if res.get('added'):
                r, c = res['added']; log_step(f"({r}, {c})")

            if res.get('found'):
                running = False
                if getattr(engine, "goal_any_solution", False):
                    log_step("==> Tìm đủ 8 hậu (giải hợp lệ).")
                else:
                    log_step("==> Trùng trạng thái đích.")
                return

            if not res.get('progressed'):
                running = False
                log_step("==> Không còn bước tiến.")
                return

            root.after(delay, tick)
            return

    tick()

def reset_and_run(selected_algo: str):
    global engine, running, muc_tieu
    running = False
    current_algo_var.set(f"Đang chạy: {selected_algo}")
    log_list.delete(0, tk.END)

    if selected_algo == "Tăng tốc":
        toggle_speed()
        return

    # vẽ target/clear theo loại thuật toán (any-solution vs target-mode)
    if selected_algo in {"Hill Climbing", "Simulated Annealing"}:
        veoco_fixed(cells_phai, queens=[], queenimg=queen_img)
        veoco_fixed(cells_trai, queens=[], queenimg=queen_img)
    else:
        veoco_fixed(cells_phai, queens=muc_tieu, queenimg=queen_img)
        veoco_fixed(cells_trai, queens=[], queenimg=queen_img)

    engine = make_engine(selected_algo, n, target_pairs=muc_tieu)
    start_animation()

# Tạo các nút
for idx, name in enumerate(ALGO_BUTTONS):
    r = idx // 2; c = idx % 2
    cmd = toggle_speed if name == "Tăng tốc" else (lambda n=name: reset_and_run(n))
    tk.Button(btn_container, text=name, command=cmd).grid(row=r, column=c, sticky="ew", padx=2, pady=2)

root.minsize(1180, 720)
root.mainloop()
