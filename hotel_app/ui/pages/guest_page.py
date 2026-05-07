import tkinter as tk
from tkinter import messagebox
from utils.constants import *
from ui.widgets import styled_btn, styled_entry, build_tree, card_frame
from database.db_manager import get_connection

class GuestPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.selected_id = None
        self._build()

    def _build(self):
        # --- HEADER ---
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=20, pady=15)
        tk.Label(top, text="👥  Data Tamu", bg=BG, fg=ACCENT, font=FONT_HEAD).pack(side="left")
        
        btn_f = tk.Frame(top, bg=BG)
        btn_f.pack(side="right")
        styled_btn(btn_f, "+ Tambah Tamu", self._open_add).pack(side="left", padx=5)
        styled_btn(btn_f, "✏ Edit", self._open_edit, color=CARD, fg=ACCENT).pack(side="left", padx=5)
        styled_btn(btn_f, "🗑 Hapus", self._delete, color=DANGER).pack(side="left", padx=5)
        styled_btn(btn_f, "🔄 Refresh", self.refresh, color=SURFACE, fg=TEXT).pack(side="left", padx=5)

        # --- AREA FILTER & SEARCH ---
        filter_f = tk.Frame(self, bg=BG)
        filter_f.pack(fill="x", padx=20, pady=(0, 10))

        # 1. Search Nama
        tk.Label(filter_f, text="Cari Nama:", bg=BG, fg=TEXT_DIM).pack(side="left", padx=(0, 5))
        self.ent_search = styled_entry(filter_f)
        self.ent_search.pack(side="left", padx=5)
        self.ent_search.bind("<KeyRelease>", lambda e: self.refresh()) # Auto search pas ngetik

        # 2. Filter Urutan (A-Z)
        tk.Label(filter_f, text="Urutan:", bg=BG, fg=TEXT_DIM).pack(side="left", padx=(15, 5))
        self.var_sort = tk.StringVar(value="Terbaru")
        sort_opt = tk.OptionMenu(filter_f, self.var_sort, "Terbaru", "Nama A-Z", "Nama Z-A", command=lambda _: self.refresh())
        sort_opt.config(bg=SURFACE, fg=TEXT, relief="flat", highlightthickness=0)
        sort_opt.pack(side="left", padx=5)

        # 3. Filter Kewarganegaraan
        tk.Label(filter_f, text="Negara:", bg=BG, fg=TEXT_DIM).pack(side="left", padx=(15, 5))
        self.var_nation = tk.StringVar(value="Semua")
        self.nation_opt = tk.OptionMenu(filter_f, self.var_nation, "Semua", command=lambda _: self.refresh())
        self.nation_opt.config(bg=SURFACE, fg=TEXT, relief="flat", highlightthickness=0)
        self.nation_opt.pack(side="left", padx=5)
        
        # Update list negara di dropdown
        self._update_nation_list()

        # --- TABEL (TREEVIEW) ---
        cols = ("ID", "Nama", "No. Identitas", "Telepon", "Email", "Negara")
        self.tree = build_tree(self, cols, cols, [50, 200, 150, 120, 150, 100])
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        
        self.refresh()

    def _update_nation_list(self):
        """Mengambil daftar negara unik dari database untuk isi dropdown"""
        conn = get_connection()
        if not conn: return
        c = conn.cursor()
        try:
            c.execute("SELECT DISTINCT nationality FROM guests WHERE nationality IS NOT NULL")
            nations = [row[0] for row in c.fetchall()]
            
            # Reset menu
            menu = self.nation_opt["menu"]
            menu.delete(0, "end")
            menu.add_command(label="Semua", command=lambda: [self.var_nation.set("Semua"), self.refresh()])
            
            for n in sorted(nations):
                menu.add_command(label=n, command=lambda val=n: [self.var_nation.set(val), self.refresh()])
        finally:
            c.close()
            conn.close()

    def _on_select(self, _):
        sel = self.tree.selection()
        if sel: 
            self.selected_id = self.tree.item(sel[0])['values'][0]

    def _open_edit(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih tamu yang mau diedit dulu!")
            return
        self._open_add(self.selected_id)

    def refresh(self):
        for row in self.tree.get_children(): 
            self.tree.delete(row)
            
        conn = get_connection()
        if not conn: return
        c = conn.cursor(dictionary=True)
        try:
            # Ambil nilai dari filter
            search_val = self.ent_search.get()
            sort_val = self.var_sort.get()
            nation_val = self.var_nation.get()

            # Query Dasar
            query = "SELECT * FROM guests WHERE 1=1"
            params = []

            # Tambah Filter Search
            if search_val:
                query += " AND name LIKE %s"
                params.append(f"%{search_val}%")

            # Tambah Filter Negara
            if nation_val != "Semua":
                query += " AND nationality = %s"
                params.append(nation_val)

            # Tambah Logika Urutan (Sorting)
            if sort_val == "Nama A-Z":
                query += " ORDER BY name ASC"
            elif sort_val == "Nama Z-A":
                query += " ORDER BY name DESC"
            else:
                query += " ORDER BY id DESC"

            c.execute(query, tuple(params))
            for row in c.fetchall():
                self.tree.insert("", "end", values=(
                    row['id'], row['name'], row['id_number'], 
                    row['phone'] or "-", row['email'] or "-", 
                    row['nationality'] or "-"
                ))
        finally:
            c.close()
            conn.close()

    def _open_add(self, guest_id=None): 
        win = tk.Toplevel(self)
        win.title("Edit Data Tamu" if guest_id else "Tambah Tamu Baru")
        win.geometry("450x600")
        win.configure(bg=BG)
        win.grab_set()
        
        f = card_frame(win)
        f.pack(padx=20, pady=20, fill="both", expand=True)
        
        # --- FIELD INPUT ---
        tk.Label(f, text="Nama Lengkap", bg=CARD, fg=TEXT_DIM).pack(pady=(10,0))
        ent_name = styled_entry(f); ent_name.pack(pady=5, padx=10, fill="x")
        
        tk.Label(f, text="No. KTP / Passport", bg=CARD, fg=TEXT_DIM).pack(pady=(10,0))
        ent_id = styled_entry(f); ent_id.pack(pady=5, padx=10, fill="x")

        tk.Label(f, text="Nomor Telepon", bg=CARD, fg=TEXT_DIM).pack(pady=(10,0))
        ent_phone = styled_entry(f); ent_phone.pack(pady=5, padx=10, fill="x")

        tk.Label(f, text="Email", bg=CARD, fg=TEXT_DIM).pack(pady=(10,0))
        ent_email = styled_entry(f); ent_email.pack(pady=5, padx=10, fill="x")

        tk.Label(f, text="Negara", bg=CARD, fg=TEXT_DIM).pack(pady=(10,0))
        ent_nation = styled_entry(f); ent_nation.pack(pady=5, padx=10, fill="x")

        if guest_id:
            conn = get_connection()
            c = conn.cursor(dictionary=True)
            c.execute("SELECT * FROM guests WHERE id = %s", (guest_id,))
            g = c.fetchone()
            if g:
                ent_name.insert(0, g['name'])
                ent_id.insert(0, g['id_number'])
                ent_phone.insert(0, g['phone'] or "")
                ent_email.insert(0, g['email'] or "")
                ent_nation.delete(0, tk.END) # Hapus default "Indonesia"
                ent_nation.insert(0, g['nationality'] or "")
            c.close()
            conn.close()
        else:
            ent_nation.insert(0, "Indonesia")
        
        def save():
            name, id_num = ent_name.get(), ent_id.get()
            phone, email, nation = ent_phone.get(), ent_email.get(), ent_nation.get()

            if not name or not id_num:
                messagebox.showwarning("Input Salah", "Nama dan No. Identitas wajib diisi!")
                return

            conn = get_connection()
            if not conn: return
            c = conn.cursor()
            try:
                if guest_id:
                    # LOGIKA UPDATE
                    query = """
                        UPDATE guests SET name=%s, id_number=%s, phone=%s, email=%s, nationality=%s 
                        WHERE id=%s
                    """
                    c.execute(query, (name, id_num, phone, email, nation, guest_id))
                    msg = "Data tamu berhasil diperbarui!"
                else:
                    # LOGIKA INSERT
                    query = "INSERT INTO guests (name, id_number, phone, email, nationality) VALUES (%s, %s, %s, %s, %s)"
                    c.execute(query, (name, id_num, phone, email, nation))
                    msg = "Data tamu berhasil ditambahkan!"

                conn.commit()
                self.refresh()
                win.destroy()
                messagebox.showinfo("Sukses", msg)
            except Exception as e:
                messagebox.showerror("Gagal", f"Error: {e}")
            finally:
                c.close()
                conn.close()
                
        styled_btn(win, "💾  SIMPAN", save).pack(pady=20)

    def _delete(self):
        """Hapus data tamu yang dipilih"""
        if not self.selected_id:
            messagebox.showwarning("Pilih Data", "Pilih tamu yang mau dihapus dulu!")
            return
            
        if messagebox.askyesno("Konfirmasi Hapus", "Yakin mau hapus tamu ini?"):
            conn = get_connection()
            if not conn: return
            c = conn.cursor()
            try:
                c.execute("DELETE FROM guests WHERE id = %s", (self.selected_id,))
                conn.commit()
                messagebox.showinfo("Berhasil", "Tamu telah dihapus.")
                self.refresh()
                self.selected_id = None
            except Exception as e:
                messagebox.showerror("Gagal", f"Tidak bisa menghapus tamu (Mungkin masih ada reservasi aktif): {e}")
            finally:
                c.close()
                conn.close()