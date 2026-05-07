import tkinter as tk
from tkinter import ttk
# Import konstanta biar warna & font-nya gak error
from utils.constants import *

def styled_entry(parent, width=25, **kw):
    e = tk.Entry(parent, width=width, bg=CARD, fg=TEXT,
                 insertbackground=ACCENT, relief="flat",
                 font=FONT_LABEL, bd=0, highlightthickness=1,
                 highlightbackground=BORDER, highlightcolor=ACCENT, **kw)
    return e

def styled_btn(parent, text, cmd, color=ACCENT, fg=BG, **kw):
    b = tk.Button(parent, text=text, command=cmd,
                  bg=color, fg=fg, font=FONT_BOLD,
                  relief="flat", bd=0, padx=14, pady=7,
                  activebackground=ACCENT2, activeforeground=BG,
                  cursor="hand2", **kw)
    b.bind("<Enter>", lambda e: b.config(bg=ACCENT2))
    b.bind("<Leave>", lambda e: b.config(bg=color))
    return b

def card_frame(parent, **kw):
    return tk.Frame(parent, bg=CARD, bd=0,
                    highlightthickness=1, highlightbackground=BORDER, **kw)

def section_label(parent, text):
    tk.Label(parent, text=text, bg=CARD, fg=ACCENT,
             font=FONT_SUBH).pack(anchor="w", padx=18, pady=(14, 4))
    tk.Frame(parent, bg=ACCENT, height=1).pack(fill="x", padx=18, pady=(0, 10))

def stat_card(parent, title, value, color=ACCENT, icon=""):
    f = card_frame(parent)
    f.pack(side="left", fill="both", expand=True, padx=8, pady=8)
    tk.Label(f, text=icon, bg=CARD, fg=color, font=("Segoe UI", 24)).pack(pady=(14, 0))
    tk.Label(f, text=value, bg=CARD, fg=color, font=FONT_HUGE).pack()
    tk.Label(f, text=title, bg=CARD, fg=TEXT_DIM, font=FONT_SMALL).pack(pady=(0, 14))
    return f

def build_tree(parent, columns, col_names, widths):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Hotel.Treeview",
        background=SURFACE, foreground=TEXT,
        fieldbackground=SURFACE, borderwidth=0,
        rowheight=34, font=FONT_LABEL)
    style.configure("Hotel.Treeview.Heading",
        background=CARD, foreground=ACCENT, font=FONT_BOLD,
        borderwidth=0, relief="flat")
    style.map("Hotel.Treeview",
        background=[("selected", ACCENT)],
        foreground=[("selected", BG)])

    frame = tk.Frame(parent, bg=BG)
    frame.pack(fill="both", expand=True, padx=12, pady=6)

    vsb = ttk.Scrollbar(frame, orient="vertical")
    vsb.pack(side="right", fill="y")
    hsb = ttk.Scrollbar(frame, orient="horizontal")
    hsb.pack(side="bottom", fill="x")

    tree = ttk.Treeview(frame, columns=columns, show="headings",
                        style="Hotel.Treeview",
                        yscrollcommand=vsb.set,
                        xscrollcommand=hsb.set)
    vsb.config(command=tree.yview)
    hsb.config(command=tree.xview)

    for col, name, w in zip(columns, col_names, widths):
        tree.heading(col, text=name)
        tree.column(col, width=w, minwidth=40, anchor="center")

    tree.pack(fill="both", expand=True)
    return tree