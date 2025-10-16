import os
import tkinter as tk
from PIL import Image, ImageTk

def taobanco_fixed(r, title, size=520):
    frame = tk.LabelFrame(r, text=title, padx=8, pady=8)
    frame.grid_propagate(False)
    banco = tk.Frame(frame, height=size, width=size, bg="white")
    banco.pack(fill="both", expand=True)
    cells = [[None for _ in range(8)] for _ in range(8)]
    for i in range(8):
        banco.grid_columnconfigure(i, weight=1, uniform="o")
        banco.grid_rowconfigure(i, weight=1, uniform="o")
        for j in range(8):
            color = "black" if (i+j) % 2 else "white"
            cell = tk.Frame(banco, bg=color, borderwidth=1, relief="solid")
            cell.grid(row=i, column=j, sticky="nsew")
            cell.grid_propagate(False)
            cells[i][j] = cell
    return frame, banco, cells

def veoco_fixed(cells, queens=None, queenimg=None, highlight=None):
    for i in range(8):
        for j in range(8):
            for w in cells[i][j].winfo_children(): w.destroy()
            cells[i][j]["highlightbackground"] = "black"
            cells[i][j]["highlightthickness"] = 1
    queens = set(queens or [])
    for (i, j) in queens:
        if 0 <= i < 8 and 0 <= j < 8:
            if queenimg is not None:
                tk.Label(cells[i][j], image=queenimg, bg=cells[i][j]["bg"]).pack(expand=True)
            else:
                color = cells[i][j]["bg"]
                fg = "white" if color == "black" else "black"
                tk.Label(cells[i][j], text="Q", font=("Arial", 28, "bold"), fg=fg, bg=color).pack(expand=True)
    if highlight:
        i, j = highlight
        if 0 <= i < 8 and 0 <= j < 8:
            cells[i][j]["highlightbackground"] = "yellow"
            cells[i][j]["highlightthickness"] = 3

def load_queen_image(path="assets/queen.jpg"):
    if os.path.exists(path):
        try:
            return ImageTk.PhotoImage(Image.open(path).resize((56, 56)))
        except Exception:
            return None
    return None
