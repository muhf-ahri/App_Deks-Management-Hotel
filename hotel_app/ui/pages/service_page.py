import tkinter as tk
from tkinter import messagebox
from utils.constants import *
from utils.helpers import fmt_currency
from ui.widgets import styled_btn, build_tree, card_frame
from database.db_manager import get_connection

class ServicePage(tk.Frame):
    def __init__(self, master, hotel_info=None):
        super().__init__(master, bg=BG)
        self.hotel_info = hotel_info or {}
        self.selected_id = None
        self._build()

    def _build(self):
        # --- HEADER ---
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=20, pady=15)
        tk.Label(top, text="🛎️  Layanan Kamar", bg=BG, fg=ACCENT, font=FONT_HEAD).pack(side="left")
        
        btn_f = tk.Frame(top, bg=BG)
        btn_f.pack(side="right")
        
        styled_btn(btn_f, "+ Pesan Layanan", self._open_order).pack(side="left", padx=5)
        styled_btn(btn_f, "✅ Selesai", self._mark_delivered, color=SUCCESS).pack(side="left", padx=5)
        styled_btn(btn_f, "🔄 Refresh", self.refresh, color=SURFACE, fg=TEXT).pack(side="left", padx=5)

        # --- TABEL PESANAN ---
        cols = ("ID", "Kamar", "Tamu", "Layanan", "Qty", "Total", "Status")
        self.tree = build_tree(self, cols, cols, [50, 80, 150, 180, 50, 120, 100])
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
            query = """
                SELECT so.id, r.number, g.name as guest_name, s.name as service_name, 
                       so.quantity, (s.price * so.quantity) as total, so.status
                FROM service_orders so
                JOIN bookings b ON so.booking_id = b.id
                JOIN guests g ON b.guest_id = g.id
                JOIN rooms r ON b.room_id = r.id
                JOIN services s ON so.service_id = s.id
                ORDER BY so.id DESC
            """
            c.execute(query)
            for row in c.fetchall():
                self.tree.insert("", "end", values=(
                    row['id'], row['number'], row['guest_name'],
                    row['service_name'], row['quantity'], 
                    fmt_currency(row['total']), row['status']
                ))
        finally:
            c.close()
            conn.close()

    def _open_order(self):
        # Popup buat pesan layanan baru
        OrderDialog(self, self.refresh)

    def _mark_delivered(self):
        if not self.selected_id: return
        conn = get_connection()
        c = conn.cursor()
        c.execute("UPDATE service_orders SET status = 'Delivered' WHERE id = %s", (self.selected_id,))
        conn.commit()
        conn.close()
        self.refresh()

# --- DIALOG POPUP PESAN LAYANAN ---
class OrderDialog(tk.Toplevel):
    def __init__(self, master, callback):
        super().__init__(master)
        self.callback = callback
        self.title("Pesan Layanan")
        self.geometry("400x500")
        self.configure(bg=BG)
        self.booking_map = {}
        self.service_map = {}
        self._build()
        self._load_data()

    def _build(self):
        f = card_frame(self)
        f.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(f, text="Pilih Kamar (Tamu Aktif)", bg=CARD, fg=TEXT_DIM).pack(pady=(10,0))
        self.var_booking = tk.StringVar(self, "Pilih...")
        self.om_booking = tk.OptionMenu(f, self.var_booking, "")
        self.om_booking.pack(fill="x", pady=5)

        tk.Label(f, text="Pilih Layanan", bg=CARD, fg=TEXT_DIM).pack(pady=(10,0))
        self.var_service = tk.StringVar(self, "Pilih...")
        self.om_service = tk.OptionMenu(f, self.var_service, "")
        self.om_service.pack(fill="x", pady=5)

        tk.Label(f, text="Jumlah (Qty)", bg=CARD, fg=TEXT_DIM).pack(pady=(10,0))
        self.ent_qty = tk.Entry(f, bg=SURFACE, fg=TEXT, insertbackground=TEXT, relief="flat")
        self.ent_qty.insert(0, "1")
        self.ent_qty.pack(pady=5, fill="x", padx=20)

        styled_btn(self, "🚀 PESAN SEKARANG", self._save).pack(pady=20)

    def _load_data(self):
        conn = get_connection()
        c = conn.cursor(dictionary=True)
        # Ambil booking yang statusnya 'Checked In'
        c.execute("SELECT b.id, r.number, g.name FROM bookings b JOIN rooms r ON b.room_id = r.id JOIN guests g ON b.guest_id = g.id WHERE b.status = 'Checked In'")
        for r in c.fetchall():
            lbl = f"Kamar {r['number']} - {r['name']}"
            self.booking_map[lbl] = r['id']
            self.om_booking['menu'].add_command(label=lbl, command=tk._setit(self.var_booking, lbl))

        c.execute("SELECT id, name, price FROM services")
        for s in c.fetchall():
            lbl = f"{s['name']} ({fmt_currency(s['price'])})"
            self.service_map[lbl] = s['id']
            self.om_service['menu'].add_command(label=lbl, command=tk._setit(self.var_service, lbl))
        c.close()
        conn.close()

    def _save(self):
        try:
            b_id = self.booking_map[self.var_booking.get()]
            s_id = self.service_map[self.var_service.get()]
            qty = int(self.ent_qty.get())
            
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO service_orders (booking_id, service_id, quantity) VALUES (%s, %s, %s)", (b_id, s_id, qty))
            conn.commit()
            conn.close()
            self.callback()
            self.destroy()
        except:
            messagebox.showerror("Error", "Isi data dengan benar!")