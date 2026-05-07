import tkinter as tk
from datetime import datetime
from utils.constants import *
from utils.helpers import fmt_currency
from ui.widgets import card_frame, section_label, build_tree, stat_card
from database.db_manager import get_connection

class DashboardPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self._build()

    def _build(self):
        # --- HEADER SECTION ---
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=25, pady=(25, 0))
        
        tk.Label(hdr, text="Moko Hotel", bg=BG, fg=ACCENT,
                 font=("Segoe UI Bold", 22)).pack(side="left")
        
        self.date_lbl = tk.Label(hdr, text="", bg=BG, fg=TEXT_DIM, font=FONT_LABEL)
        self.date_lbl.pack(side="right", pady=10)
        self._tick()

        # Separator Line
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=25, pady=15)

        # --- STATISTICS ROW ---
        self.stat_row = tk.Frame(self, bg=BG)
        self.stat_row.pack(fill="x", padx=17)

        # --- RECENT ACTIVITY TABLE ---
        content = tk.Frame(self, bg=BG)
        content.pack(fill="both", expand=True, padx=25, pady=(10, 25))
        
        rc = card_frame(content)
        rc.pack(fill="both", expand=True)
        
        # Header di dalam Card (Table Title & Refresh Button)
        tbl_hdr = tk.Frame(rc, bg=CARD)
        tbl_hdr.pack(fill="x", padx=15, pady=10)
        
        # FIX: Panggil section_label tanpa .pack() di luar karena di widgets.py biasanya sudah di-pack
        section_label(tbl_hdr, "📋  Aktivitas Reservasi Terbaru")
        
        tk.Button(tbl_hdr, text="🔄 Refresh Manual", command=self.refresh, 
                  bg=SURFACE, fg=ACCENT, font=("Segoe UI", 9),
                  relief="flat", cursor="hand2").pack(side="right")

        cols = ("ID", "Tamu", "Kamar", "Check-in", "Check-out", "Status", "Total")
        self.tree = build_tree(rc, cols, cols, [50, 180, 80, 110, 110, 100, 140])
        
        # Jalankan data loading
        self.refresh()
        self._auto_refresh()

    def _tick(self):
        """Update jam digital setiap detik"""
        now = datetime.now().strftime("%A, %d %B %Y  |  %H:%M:%S")
        self.date_lbl.config(text=now)
        self.after(1000, self._tick)

    def _auto_refresh(self):
        """Auto update data tiap 30 detik"""
        self.refresh()
        self.after(30000, self._auto_refresh)

    def refresh(self):
        """Ambil data terbaru (Update: Akurasi Pendapatan pasca Refund)"""
        # 1. Bersihkan widget statistik lama agar tidak tumpang tindih
        for w in self.stat_row.winfo_children():
            w.destroy()

        conn = get_connection()
        if not conn:
            return
        
        c = conn.cursor(dictionary=True)

        try:
            # --- 1. LOAD STATISTIK OPERASIONAL ---
            c.execute("SELECT COUNT(*) as total FROM rooms WHERE status='Available'")
            avail = c.fetchone()['total']
            
            c.execute("SELECT COUNT(*) as total FROM rooms WHERE status='Occupied'")
            occ = c.fetchone()['total']
            
            c.execute("SELECT COUNT(*) as total FROM bookings WHERE status='Checked In'")
            checkin = c.fetchone()['total']

            # --- 2. LOGIKA PENDAPATAN AKURAT (TERMASUK ADJUSTMENT REFUND) ---
            
            # A. Pendapatan Kamar: 
            # Mengambil total_price dari status 'Checked In' & 'Checked Out'.
            # Karena pada proses Check-Out di BookingPage kita sudah me-UPDATE total_price 
            # jika tamu pulang awal, maka SUM() di sini otomatis sudah nilai setelah dipotong (net).
            query_room = """
                SELECT COALESCE(SUM(total_price), 0) as total 
                FROM bookings 
                WHERE status IN ('Checked In', 'Checked Out')
            """
            c.execute(query_room)
            room_income = c.fetchone()['total']

            # B. Pendapatan Layanan (Room Service):
            # Mengambil total harga layanan yang sudah berhasil dikirim (Delivered).
            service_query = """
                SELECT COALESCE(SUM(s.price * so.quantity), 0) as total 
                FROM service_orders so 
                JOIN services s ON so.service_id = s.id 
                WHERE so.status = 'Delivered'
            """
            c.execute(service_query)
            service_income = c.fetchone()['total']

            # C. Kalkulasi Total Akhir
            total_income = room_income + service_income

            # --- 3. TAMPILKAN KE UI ---
            stat_card(self.stat_row, "Kamar Ready", str(avail), SUCCESS, "🛏")
            stat_card(self.stat_row, "Terisi",       str(occ),   DANGER,  "🔑")
            stat_card(self.stat_row, "Tamu Aktif",   str(checkin), ACCENT, "👥")
            # Card pendapatan sekarang menampilkan nilai net setelah refund
            stat_card(self.stat_row, "Pendapatan",   fmt_currency(total_income), ACCENT2, "💰")

            # --- 4. REFRESH TABEL AKTIVITAS TERBARU ---
            for row in self.tree.get_children():
                self.tree.delete(row)

            query_table = """
                SELECT b.id, g.name, r.number, b.check_in, b.check_out, b.status, b.total_price
                FROM bookings b
                LEFT JOIN guests g ON b.guest_id = g.id
                LEFT JOIN rooms r ON b.room_id = r.id
                ORDER BY b.id DESC LIMIT 15
            """
            c.execute(query_table)
            
            for row in c.fetchall():
                tamu = row['name'] if row['name'] else "---"
                kamar = row['number'] if row['number'] else "???"
                # Tag warna untuk membedakan baris yang masih aktif dan selesai
                tag = "active" if row['status'] in ("Checked In", "Reserved") else "done"
                
                self.tree.insert("", "end", values=(
                    row['id'], tamu, kamar, 
                    row['check_in'], row['check_out'], row['status'],
                    fmt_currency(row['total_price'])
                ), tags=(tag,))

            self.tree.tag_configure("active", foreground=TEXT)
            self.tree.tag_configure("done", foreground=TEXT_DIM)

        except Exception as e:
            print(f"🔥 Error Dashboard: {e}")
        finally:
            c.close()
            conn.close()