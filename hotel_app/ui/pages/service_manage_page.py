import tkinter as tk
from tkinter import messagebox
from utils.constants import *
from ui.widgets import styled_btn, styled_entry, build_tree, card_frame
from database.db_manager import get_connection

class ServiceManagePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.selected_id = None
        self._build()

    def _build(self):
        # --- HEADER ---
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=20, pady=15)
        tk.Label(top, text="🛠️  Master Layanan", bg=BG, fg=ACCENT, font=FONT_HEAD).pack(side="left")
        
        btn_f = tk.Frame(top, bg=BG)
        btn_f.pack(side="right")
        
        styled_btn(btn_f, "+ Tambah Menu", self._open_add).pack(side="left", padx=5)
        styled_btn(btn_f, "🗑 Hapus", self._delete, color=DANGER).pack(side="left", padx=5)
        styled_btn(btn_f, "🔄 Refresh", self.refresh, color=SURFACE, fg=TEXT).pack(side="left", padx=5)

        # --- TABEL DAFTAR LAYANAN ---
        cols = ("ID", "Nama Layanan", "Kategori", "Harga")
        self.tree = build_tree(self, cols, cols, [50, 250, 150, 150])
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.refresh()

    def _on_select(self, _):
        sel = self.tree.selection()
        if sel: self.selected_id = self.tree.item(sel[0])['values'][0]

    def refresh(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        conn = get_connection()
        if not conn: return
        c = conn.cursor(dictionary=True)
        try:
            c.execute("SELECT * FROM services ORDER BY category, name")
            for row in c.fetchall():
                self.tree.insert("", "end", values=(
                    row['id'], row['name'], row['category'], 
                    f"Rp {int(row['price']):,}"
                ))
        finally:
            c.close()
            conn.close()

    def _open_add(self):
        """Dialog Tambah Menu Baru"""
        win = tk.Toplevel(self)
        win.title("Tambah Layanan/Menu")
        win.geometry("400x500")
        win.configure(bg=BG)
        win.grab_set()

        f = card_frame(win)
        f.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(f, text="Nama Layanan (Makanan/Jasa)", bg=CARD, fg=TEXT_DIM).pack(pady=(10,0))
        ent_name = styled_entry(f); ent_name.pack(pady=5, fill="x", padx=15)

        tk.Label(f, text="Kategori", bg=CARD, fg=TEXT_DIM).pack(pady=(10,0))
        var_cat = tk.StringVar(win, "Food")
        opt_cat = tk.OptionMenu(f, var_cat, "Food", "Beverage", "Laundry", "Other")
        opt_cat.config(bg=SURFACE, fg=TEXT, relief="flat")
        opt_cat.pack(pady=5, fill="x", padx=15)

        tk.Label(f, text="Harga (Rp)", bg=CARD, fg=TEXT_DIM).pack(pady=(10,0))
        ent_price = styled_entry(f); ent_price.pack(pady=5, fill="x", padx=15)

        def save():
            name = ent_name.get()
            cat = var_cat.get()
            price = ent_price.get()

            if not name or not price:
                messagebox.showwarning("Gagal", "Nama dan Harga harus diisi!")
                return

            conn = get_connection()
            c = conn.cursor()
            try:
                c.execute("INSERT INTO services (name, category, price) VALUES (%s, %s, %s)", 
                          (name, cat, price))
                conn.commit()
                self.refresh()
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

        styled_btn(win, "💾 SIMPAN MENU", save).pack(pady=20)

    def _delete(self):
        if not self.selected_id: return
        if messagebox.askyesno("Hapus", "Hapus layanan ini?"):
            conn = get_connection()
            c = conn.cursor()
            c.execute("DELETE FROM services WHERE id = %s", (self.selected_id,))
            conn.commit()
            conn.close()
            self.refresh()