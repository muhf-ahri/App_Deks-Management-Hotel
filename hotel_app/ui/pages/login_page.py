import tkinter as tk
from tkinter import messagebox
from utils.constants import *
from database.db_manager import verify_hotel_login

class LoginPage(tk.Tk):
    def __init__(self, on_success):
        super().__init__()
        self.title("Login - Hotel Management System")
        self.geometry("420x580") # Sedikit lebih tinggi untuk menampung teks info
        self.resizable(False, False)
        self.configure(bg=BG)
        self.on_success = on_success  # Callback untuk pindah ke HotelApp

        self._build_ui()
        
        # Shortcut Enter untuk login langsung
        self.bind("<Return>", lambda e: self._handle_login())

    def _build_ui(self):
        # Container utama agar semua elemen berada di tengah
        frame = tk.Frame(self, bg=BG)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # 1. Branding Section
        tk.Label(frame, text="🏨", bg=BG, font=("Segoe UI", 42)).pack(pady=(0, 5))
        tk.Label(frame, text="HOTEL MANAGEMENT", bg=BG, fg=ACCENT,
                 font=("Segoe UI Bold", 20)).pack()
        tk.Label(frame, text="Silahkan login dengan akun hotel Anda", bg=BG, fg=TEXT_DIM,
                 font=("Segoe UI", 10)).pack(pady=(5, 30))

        # Separator Line
        tk.Frame(frame, bg=BORDER, height=1, width=320).pack(pady=(0, 20))

        # 2. Input Section: Nama Hotel
        tk.Label(frame, text="Nama Hotel", bg=BG, fg=TEXT_DIM,
                 font=("Segoe UI", 10)).pack(anchor="w")
        self.user_ent = tk.Entry(frame, bg=SURFACE, fg=TEXT, insertbackground=ACCENT,
                                 relief="flat", font=("Segoe UI", 12), width=32,
                                 highlightthickness=1, highlightcolor=ACCENT,
                                 highlightbackground=BORDER)
        self.user_ent.pack(pady=(5, 15), ipady=9)
        self.user_ent.focus()

        # 3. Input Section: Password
        tk.Label(frame, text="Password", bg=BG, fg=TEXT_DIM,
                 font=("Segoe UI", 10)).pack(anchor="w")
        self.pass_ent = tk.Entry(frame, bg=SURFACE, fg=TEXT, insertbackground=ACCENT,
                                 relief="flat", font=("Segoe UI", 12), width=32, show="●",
                                 highlightthickness=1, highlightcolor=ACCENT,
                                 highlightbackground=BORDER)
        self.pass_ent.pack(pady=(5, 25), ipady=9)

        # 4. Action Button
        self.login_btn = tk.Button(frame, text="   LOGIN   ", command=self._handle_login,
                                   bg=ACCENT, fg=BG, font=("Segoe UI Bold", 11),
                                   relief="flat", cursor="hand2", width=34)
        self.login_btn.pack(ipady=10)
        
        # Hover effect
        self.login_btn.bind("<Enter>", lambda e: self.login_btn.config(bg=ACCENT2))
        self.login_btn.bind("<Leave>", lambda e: self.login_btn.config(bg=ACCENT))

        # 5. INFO AKUN DEMO (Teks bantuan yang kamu minta)
        hint_frame = tk.Frame(frame, bg=BG)
        hint_frame.pack(pady=(25, 0))
        
        tk.Label(hint_frame, text="Gunakan akun dari database untuk masuk:", 
                 bg=BG, fg=TEXT_DIM, font=("Segoe UI", 8, "italic")).pack()
        
        # Menampilkan contoh data dari tabel hotels kamu
        acc_info = tk.Label(hint_frame, text="Moko Hotel  |  Pass: moko123", 
                            bg=BG, fg=ACCENT, font=("Segoe UI Bold", 9))
        acc_info.pack(pady=2)

        # 6. Footer
        tk.Label(frame, text="© 2026 Hotel Management System", bg=BG, fg=TEXT_DIM,
                 font=("Segoe UI", 8)).pack(pady=(30, 0))

    def _handle_login(self):
        """Proses pengecekan login ke database"""
        name = self.user_ent.get().strip()
        pwd  = self.pass_ent.get().strip()

        # Validasi input kosong
        if not name or not pwd:
            messagebox.showwarning("Peringatan", "Nama Hotel dan Password tidak boleh kosong!")
            return

        # Pengecekan ke database MariaDB via db_manager
        hotel = verify_hotel_login(name, pwd)

        if hotel:
            # Jika sukses: Tutup Login, jalankan HotelApp dengan data hotel
            self.destroy()
            self.on_success(hotel)
        else:
            # Jika gagal: Beri tahu user dan reset input password
            messagebox.showerror("Login Gagal", "Nama Hotel atau Password salah!\nPeriksa kembali data Anda.")
            self.pass_ent.delete(0, tk.END)
            self.pass_ent.focus()