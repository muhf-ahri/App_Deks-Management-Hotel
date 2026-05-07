import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector # Pastiin udah pip install mysql-connector-python
from utils.constants import *
from utils.helpers import fmt_currency
from ui.widgets import styled_btn, styled_entry, build_tree, card_frame
from database.db_manager import get_connection

class RoomPage(tk.Frame):
    def __init__(self, master, hotel_info=None):
        super().__init__(master, bg=BG)
        self.hotel_info = hotel_info or {}
        self.selected_id = None
        self._build()

    def _build(self):
        # ... (Kode UI Header lu tetep sama) ...
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=20, pady=14)
        tk.Label(top, text="🛏  Manajemen Kamar", bg=BG, fg=ACCENT, font=FONT_HEAD).pack(side="left")
        
        
        bf = tk.Frame(top, bg=BG)
        bf.pack(side="right")
        styled_btn(bf, "🔍 Detail", self._open_detail, color=SURFACE, fg=TEXT).pack(side="left", padx=4)
        styled_btn(bf, "+ Tambah", self._open_add).pack(side="left", padx=4)
        styled_btn(bf, "✏ Edit", self._edit, color=CARD, fg=ACCENT).pack(side="left", padx=4)
        styled_btn(bf, "🗑 Hapus", self._delete, color=DANGER, fg=TEXT).pack(side="left", padx=4)
        styled_btn(bf, "🔄 Refresh", self.refresh, color=SURFACE, fg=TEXT_DIM).pack(side="left", padx=4)

        cols = ("ID", "Nomor", "Tipe", "Lantai", "Kapasitas", "Harga", "Status")
        self.tree = build_tree(self, cols, cols, (40, 70, 100, 60, 80, 130, 100))
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.refresh()

    def _on_select(self, _):
        sel = self.tree.selection()
        if sel:
            # Ambil ID dari kolom pertama (index 0)
            self.selected_id = self.tree.item(sel[0])['values'][0]

    def _open_detail(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih kamar di tabel dulu!")
            return
        # Panggil dialog detail
        RoomDetailDialog(self, self.selected_id)

    def refresh(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        conn = get_connection()
        if not conn: return
        
        # Pake dictionary=True biar manggilnya gampang
        c = conn.cursor(dictionary=True)
        try:
            c.execute("SELECT id, number, type, floor, capacity, price, status FROM rooms ORDER BY number ASC")
            for row in c.fetchall():
                self.tree.insert("", "end", values=(
                    row['id'], row['number'], row['type'], row['floor'], 
                    row['capacity'], fmt_currency(row['price']), row['status']
                ))
        finally:
            c.close()
            conn.close()

    def _open_add(self): RoomDialog(self, None, self.refresh)
    def _edit(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih kamar dulu, Nyet!")
            return
        RoomDialog(self, room_id=self.selected_id, callback=self.refresh)

    def _delete(self):
        if not self.selected_id: return
        if messagebox.askyesno("Konfirmasi", "Yakin mau hapus kamar ini?"):
            conn = get_connection()
            c = conn.cursor()
            try:
                c.execute("DELETE FROM rooms WHERE id = %s", (self.selected_id,))
                conn.commit() # WAJIB DI MARIA DB
                self.refresh()
            finally:
                c.close()
                conn.close()

class RoomDetailDialog(tk.Toplevel):
    def __init__(self, master, room_id):
        super().__init__(master)
        self.room_id = room_id
        self.title("Detail Deskripsi Kamar")
        self.geometry("400x450")
        self.configure(bg=BG)
        self.grab_set()
        self._load_and_build()

    def _load_and_build(self):
        conn = get_connection()
        c = conn.cursor(dictionary=True)
        c.execute("SELECT * FROM rooms WHERE id = %s", (self.room_id,))
        room = c.fetchone()
        c.close()
        conn.close()

        if room:
            f = card_frame(self)
            f.pack(padx=20, pady=20, fill="both", expand=True)

            tk.Label(f, text=f"Kamar {room['number']} ({room['type']})", 
                     bg=CARD, fg=ACCENT, font=("Segoe UI Bold", 14)).pack(pady=10)
            
            # Area Deskripsi (Pake Text widget biar bisa wrap otomatis)
            txt_desc = tk.Text(f, bg=CARD, fg=TEXT, font=FONT_LABEL, 
                               relief="flat", wrap="word", height=10)
            txt_desc.insert("1.0", room['description'] if room['description'] else "Tidak ada deskripsi untuk kamar ini.")
            txt_desc.config(state="disabled") # Biar gak bisa diedit di sini
            txt_desc.pack(padx=15, pady=10, fill="both", expand=True)

        styled_btn(self, "Tutup", self.destroy).pack(pady=15)

# --- DIALOG POPUP UNTUK INPUT DATA ---
class RoomDialog(tk.Toplevel):
    def __init__(self, master, room_id=None, callback=None):
        super().__init__(master)
        self.room_id = room_id
        self.callback = callback
        self.title("Input Data Kamar")
        self.geometry("450x650") # Gua tinggiin biar muat semua field
        self.configure(bg=BG)
        self.grab_set()

        self._build()

        if self.room_id:
            self._fill_form()

    def _build(self):
        f = card_frame(self)
        f.pack(padx=20, pady=20, fill="both", expand=True)

        # 1. NOMOR KAMAR
        tk.Label(f, text="Nomor Kamar", bg=CARD, fg=TEXT_DIM).pack(pady=(15,0), anchor="w", padx=20)
        self.ent_num = styled_entry(f)
        self.ent_num.pack(pady=5, padx=20, fill="x")

        # 2. TIPE KAMAR (Pake Dropdown biar keren)
        tk.Label(f, text="Tipe Kamar", bg=CARD, fg=TEXT_DIM).pack(pady=(10,0), anchor="w", padx=20)
        self.var_type = tk.StringVar(self, "Standard")
        types = ["Standard", "Deluxe", "Family", "Suite", "Penthouse"]
        self.om_type = tk.OptionMenu(f, self.var_type, *types)
        self.om_type.config(bg=SURFACE, fg=TEXT, relief="flat")
        self.om_type.pack(pady=5, padx=20, fill="x")

        # 3. LANTAI
        tk.Label(f, text="Lantai", bg=CARD, fg=TEXT_DIM).pack(pady=(10,0), anchor="w", padx=20)
        self.ent_floor = styled_entry(f)
        self.ent_floor.pack(pady=5, padx=20, fill="x")

        # 4. KAPASITAS (Orang)
        tk.Label(f, text="Kapasitas (Orang)", bg=CARD, fg=TEXT_DIM).pack(pady=(10,0), anchor="w", padx=20)
        self.ent_cap = styled_entry(f)
        self.ent_cap.pack(pady=5, padx=20, fill="x")

        # 5. HARGA PER MALAM
        tk.Label(f, text="Harga / Malam", bg=CARD, fg=TEXT_DIM).pack(pady=(10,0), anchor="w", padx=20)
        self.ent_price = styled_entry(f)
        self.ent_price.pack(pady=5, padx=20, fill="x")

        # 6. DESKRIPSI
        tk.Label(f, text="Deskripsi Fasilitas", bg=CARD, fg=TEXT_DIM).pack(pady=(10,0), anchor="w", padx=20)
        self.txt_desc = tk.Text(f, height=4, bg=SURFACE, fg=TEXT, font=FONT_LABEL, relief="flat")
        self.txt_desc.pack(pady=5, padx=20, fill="x")

        # TOMBOL SIMPAN
        styled_btn(self, "💾 SIMPAN DATA", self._save).pack(pady=25)

    def _fill_form(self):
        """Mengambil data dari DB dan memasukkannya ke dalam form"""
        conn = get_connection()
        c = conn.cursor(dictionary=True)
        try:
            c.execute("SELECT * FROM rooms WHERE id = %s", (self.room_id,))
            data = c.fetchone()
            
            if data:
                # Masukkan data ke masing-masing widget
                self.ent_num.insert(0, data['number'])
                self.var_type.set(data['type'])
                self.ent_floor.insert(0, data['floor'])
                self.ent_cap.insert(0, data['capacity'])
                self.ent_price.insert(0, data['price'])
                
                # Masukkan deskripsi ke widget Text
                if data['description']:
                    self.txt_desc.insert("1.0", data['description'])
        finally:
            c.close()
            conn.close()

    def _save(self):
        num = self.ent_num.get()
        rtype = self.var_type.get()
        floor = self.ent_floor.get()
        cap = self.ent_cap.get()
        price = self.ent_price.get()
        desc = self.txt_desc.get("1.0", tk.END).strip()

        if not num or not price:
            messagebox.showwarning("Gagal", "Nomor Kamar dan Harga wajib diisi!")
            return

        conn = get_connection()
        c = conn.cursor()
        try:
            if self.room_id:
                # --- LOGIKA UPDATE ---
                query = """
                    UPDATE rooms 
                    SET number=%s, type=%s, floor=%s, capacity=%s, price=%s, description=%s
                    WHERE id=%s
                """
                c.execute(query, (num, rtype, floor, cap, price, desc, self.room_id))
                msg = f"Kamar {num} berhasil diperbarui!"
            else:
                # --- LOGIKA INSERT ---
                query = """
                    INSERT INTO rooms (number, type, floor, capacity, price, status, description) 
                    VALUES (%s, %s, %s, %s, %s, 'Available', %s)
                """
                c.execute(query, (num, rtype, floor, cap, price, desc))
                msg = f"Kamar {num} berhasil ditambah!"

            conn.commit()
            messagebox.showinfo("Sukses", msg)
            if self.callback: self.callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal simpan: {e}")
        finally:
            c.close()
            conn.close()