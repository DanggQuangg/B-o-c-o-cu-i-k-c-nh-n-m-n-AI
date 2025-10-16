# ui/widgets.py
"""
widgets.py – Xây dựng Sidebar (các nút thuật toán, log, trạng thái).
Trả về các widget cần thiết để main.py kết nối và sử dụng.
"""

import tkinter as tk
from core.engine_registry import ALGO_BUTTONS


def create_sidebar(root, on_select_algo, on_toggle_speed):
    """
    Tạo toàn bộ sidebar bên trái giao diện.
    Parameters
    ----------
    root : tk.Tk hoặc tk.Frame
        Gốc (root) của giao diện Tkinter.
    on_select_algo : function(str) -> None
        Hàm callback khi nhấn một nút thuật toán.
    on_toggle_speed : function() -> None
        Hàm callback khi nhấn nút 'Tăng tốc'.
    Returns
    -------
    dict: {
        'frame': sidebar frame,
        'current_algo_var': tk.StringVar,
        'log_list': tk.Listbox,
        'log_step': function(str)
    }
    """
    sidebar = tk.Frame(root, padx=8, pady=8)
    sidebar.grid(row=0, column=0, sticky="nsw")

    # --- khung thuật toán ---
    algo_box = tk.LabelFrame(sidebar, text="Thuật toán", padx=6, pady=6)
    algo_box.pack(fill="x", anchor="n")

    btn_container = tk.Frame(algo_box)
    btn_container.pack(fill="both", expand=True)

    for i in range(9):
        btn_container.grid_rowconfigure(i, weight=0)
    for j in range(2):
        btn_container.grid_columnconfigure(j, weight=1)

    # --- nhật ký log ---
    log_box = tk.LabelFrame(sidebar, text="Các bước đã đi (tọa độ)", padx=6, pady=6)
    log_box.pack(fill="both", expand=True, pady=(8, 0))

    log_list = tk.Listbox(log_box, height=20)
    log_scroll = tk.Scrollbar(log_box, orient="vertical", command=log_list.yview)
    log_list.config(yscrollcommand=log_scroll.set)
    log_list.pack(side="left", fill="both", expand=True)
    log_scroll.pack(side="right", fill="y")

    # --- trạng thái hiện tại ---
    current_algo_var = tk.StringVar(value="(chưa chọn)")
    status_lbl = tk.Label(sidebar, textvariable=current_algo_var, fg="#777")
    status_lbl.pack(anchor="w", pady=(6, 0))

    # --- hàm ghi log ---
    def log_step(text):
        log_list.insert(tk.END, text)
        log_list.see(tk.END)

    # --- tạo nút ---
    for idx, name in enumerate(ALGO_BUTTONS):
        r, c = divmod(idx, 2)
        if name == "Tăng tốc":
            cmd = on_toggle_speed
        else:
            cmd = lambda n=name: on_select_algo(n)
        btn = tk.Button(btn_container, text=name, command=cmd)
        btn.grid(row=r, column=c, sticky="ew", padx=2, pady=2)

    return {
        "frame": sidebar,
        "current_algo_var": current_algo_var,
        "log_list": log_list,
        "log_step": log_step,
    }
