import tkinter as tk
from utils.constants import *
# 1. Import fungsi database
from database.db_manager import init_db
# 2. Import semua halaman
from ui.pages.dashboard import DashboardPage
from ui.pages.room_page import RoomPage
from ui.pages.guest_page import GuestPage
from ui.pages.booking_page import BookingPage
from ui.pages.service_page import ServicePage
from ui.pages.service_manage_page import ServiceManagePage

class HotelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hotel Management System - SMK Medikacom")
        self.geometry("1200x750")
        self.configure(bg=BG)

        # --- SIDEBAR ---
        # Kita tambahin sedikit highlightthickness biar ada garis pemisah tipis
        self.sidebar = tk.Frame(self, bg=CARD, width=260, highlightthickness=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Judul Sidebar 
        tk.Label(self.sidebar, text="Moko Hotel", bg=CARD, fg=ACCENT, 
                 font=("Segoe UI Bold", 20)).pack(pady=(40, 5))
        tk.Label(self.sidebar, text="MANAGEMENT", bg=CARD, fg=TEXT_DIM, 
                 font=("Segoe UI", 10, "bold")).pack(pady=(0, 30))

        # Container khusus untuk tombol navigasi biar gampang diatur
        self.nav_container = tk.Frame(self.sidebar, bg=CARD)
        self.nav_container.pack(fill="x", side="top")
        
        self._nav_btn("📊 Dashboard", DashboardPage)
        self._nav_btn("🛏 Data Kamar", RoomPage)
        self._nav_btn("👥 Data Tamu", GuestPage)
        self._nav_btn("📋 Reservasi", BookingPage)
        self._nav_btn("🍱 Master Layanan", ServiceManagePage)
        self._nav_btn("💼 Layanan Kamar", ServicePage)

        # --- CONTAINER UTAMA ---
        # Tempat halaman muncul
        self.container = tk.Frame(self, bg=BG)
        self.container.pack(side="right", fill="both", expand=True)

        # Load halaman pertama kali
        self.show_page(DashboardPage)

    def _nav_btn(self, text, page_class):
        """Fungsi navigasi dengan jarak emoji-teks yang rapat & konsisten"""
        
        # 1. Kita pisahin Emoji dan Teksnya
        # Anggap format text adalah "🛎️ Layanan Kamar"
        parts = text.split(" ", 1)
        icon = parts[0]
        label_text = parts[1] if len(parts) > 1 else ""

        btn = tk.Button(self.nav_container, 
                        text=f" {icon}  {label_text}", # Cukup kasih 2 spasi biar rapat
                        command=lambda: self.show_page(page_class),
                        bg=CARD, 
                        fg=TEXT, 
                        font=FONT_LABEL,
                        relief="flat", 
                        bd=0, 
                        padx=25, # Jarak icon dari dinding kiri sidebar
                        pady=15, 
                        anchor="w", # Tetap rata kiri
                        cursor="hand2",
                        activebackground=SURFACE, 
                        activeforeground=ACCENT,
                        justify="left")
        
        btn.pack(fill="x", side="top") 

        # Bind event hover
        btn.bind("<Enter>", lambda e: btn.config(bg=SURFACE))
        btn.bind("<Leave>", lambda e: btn.config(bg=CARD))

    def show_page(self, page_class):
        """Fungsi ganti halaman"""
        # Hapus halaman lama
        for frame in self.container.winfo_children():
            frame.destroy()
        
        # Munculkan halaman baru
        page = page_class(self.container)
        page.pack(fill="both", expand=True)

# --- JALANKAN PROGRAM ---
if __name__ == "__main__":
    # Inisialisasi Database (Memastikan tabel sudah ada)
    try:
        init_db() 
    except Exception as e:
        print(f"Database Error: {e}")

    # Jalankan App
    app = HotelApp() 
    app.mainloop()