"""
Package ui – chứa các thành phần giao diện (User Interface) của chương trình 8 quân hậu.

Gồm hai module chính:
- boards.py  : Tạo và vẽ bàn cờ, hiển thị quân hậu, tô sáng ô.
- widgets.py : Sidebar giao diện (nút chọn thuật toán, nút tăng tốc, log các bước).
"""

from .boards import taobanco_fixed, veoco_fixed, load_queen_image
# Nếu bạn có widgets.py thì import luôn (để tiện sau này):
# from .widgets import create_sidebar

__all__ = [
    "taobanco_fixed",
    "veoco_fixed",
    "load_queen_image",
    # "create_sidebar",  # bỏ comment nếu có widgets.py
]
