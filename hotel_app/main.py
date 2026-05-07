import tkinter as tk
from utils.constants import *
from database.db_manager import init_db, seed_hotel_if_empty
# Import halaman
from ui.pages.dashboard import DashboardPage
from ui.pages.room_page import RoomPage
from ui.pages.guest_page import GuestPage
from ui.pages.booking_page import BookingPage
from ui.pages.service_page import ServicePage
from ui.pages.service_manage_page import ServiceManagePage
from ui.pages.login_page import LoginPage

class HotelApp(tk.Tk):
    def __init__(self, hotel_data):  # Menerima data dari login
        super().__init__()
        self.hotel_info = hotel_data  # Dict: {id, hotel_name, location}
        
        hotel_name = self.hotel_info.get('hotel_name', 'Hotel Management')
        location   = self.hotel_info.get('location', '')

        self.title(f"Management System - {hotel_name}")
        self.geometry("1200x750")
        self.configure(bg=BG)

        # --- SIDEBAR ---
        self.sidebar = tk.Frame(self, bg=CARD, width=260, highlightthickness=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Header Sidebar — Nama Hotel Dinamis dari Database
        tk.Frame(self.sidebar, bg=ACCENT, height=3).pack(fill="x")  # Garis atas accent
        
        lbl_frame = tk.Frame(self.sidebar, bg=CARD)
        lbl_frame.pack(pady=(30, 5), fill="x", padx=15)

        tk.Label(lbl_frame, text="🏨", bg=CARD, fg=ACCENT,
                 font=("Segoe UI", 28)).pack()
        tk.Label(lbl_frame, text=hotel_name, bg=CARD, fg=ACCENT,
                 font=("Segoe UI Bold", 16), wraplength=220,
                 justify="center").pack(pady=(5, 2))
        
        if location:
            tk.Label(lbl_frame, text=f"📍 {location}", bg=CARD, fg=TEXT_DIM,
                     font=("Segoe UI", 9), wraplength=220, justify="center").pack()

        tk.Label(self.sidebar, text="MANAGEMENT SYSTEM", bg=CARD, fg=TEXT_DIM,
                 font=("Segoe UI", 8, "bold")).pack(pady=(5, 0))

        # Garis separator
        tk.Frame(self.sidebar, bg=BORDER, height=1).pack(fill="x", padx=20, pady=18)

        # Container Navigasi
        self.nav_container = tk.Frame(self.sidebar, bg=CARD)
        self.nav_container.pack(fill="x", side="top")
        
        self._nav_btn("📊 Dashboard",      DashboardPage)
        self._nav_btn("🛏 Data Kamar",     RoomPage)
        self._nav_btn("👥 Data Tamu",      GuestPage)
        self._nav_btn("📋 Reservasi",       BookingPage)
        self._nav_btn("🍱 Master Layanan", ServiceManagePage)
        self._nav_btn("💼 Layanan Kamar",  ServicePage)

        # Tombol Logout di bawah
        tk.Frame(self.sidebar, bg=BORDER, height=1).pack(fill="x", padx=20, pady=(20, 10), side="bottom")
        tk.Button(self.sidebar, text="🚪  Logout", command=self._logout,
                  bg=CARD, fg=DANGER, font=("Segoe UI", 10),
                  relief="flat", cursor="hand2", pady=10,
                  activebackground=SURFACE, activeforeground=DANGER).pack(
                  side="bottom", fill="x", padx=0)

        # --- CONTAINER UTAMA ---
        self.container = tk.Frame(self, bg=BG)
        self.container.pack(side="right", fill="both", expand=True)

        self.show_page(DashboardPage)

    def _nav_btn(self, text, page_class):
        parts = text.split(" ", 1)
        icon  = parts[0]
        label_text = parts[1] if len(parts) > 1 else ""

        btn = tk.Button(self.nav_container,
                        text=f" {icon}  {label_text}",
                        command=lambda: self.show_page(page_class),
                        bg=CARD, fg=TEXT, font=FONT_LABEL,
                        relief="flat", bd=0, padx=25, pady=15,
                        anchor="w", cursor="hand2",
                        activebackground=SURFACE, activeforeground=ACCENT)
        btn.pack(fill="x", side="top")
        btn.bind("<Enter>", lambda e: btn.config(bg=SURFACE))
        btn.bind("<Leave>", lambda e: btn.config(bg=CARD))

    def show_page(self, page_class):
        for frame in self.container.winfo_children():
            frame.destroy()
        # Kirim hotel_info ke setiap page agar bisa akses nama hotel
        page = page_class(self.container, hotel_info=self.hotel_info)
        page.pack(fill="both", expand=True)

    def _logout(self):
        from tkinter import messagebox
        if messagebox.askyesno("Logout", "Apakah Anda yakin ingin keluar?"):
            self.destroy()
            # Restart login screen
            login_screen = LoginPage(on_success=launch_dashboard)
            login_screen.mainloop()

# --- FUNGSI STARTUP ---
def launch_dashboard(hotel_data):
    """Fungsi ini dipanggil saat login sukses"""
    app = HotelApp(hotel_data)
    app.mainloop()

if __name__ == "__main__":
    # 1. Inisialisasi DB & buat tabel jika belum ada
    try:
        init_db()
        seed_hotel_if_empty()  # Tambah akun hotel default jika tabel hotels kosong
    except Exception as e:
        print(f"Database Error: {e}")

    # 2. Jalankan Login Screen
    login_screen = LoginPage(on_success=launch_dashboard)
    login_screen.mainloop()