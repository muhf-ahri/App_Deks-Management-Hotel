import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from utils.constants import *
from utils.helpers import fmt_currency
from ui.widgets import styled_btn, styled_entry, build_tree, card_frame
from database.db_manager import get_connection
from tkinter import ttk 
from datetime import timedelta

class BookingPage(tk.Frame): # <--- INI YANG DICARI main.py
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.selected_id = None
        self._build()

    def _build(self):
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=20, pady=15)
        tk.Label(top, text="📋  Data Reservasi", bg=BG, fg=ACCENT, font=FONT_HEAD).pack(side="left")
        
        btn_f = tk.Frame(top, bg=BG)
        btn_f.pack(side="right")
        
        # Tombol Aksi
        # Buat frame khusus untuk tombol agar lebih mudah diatur
        action_frame = tk.Frame(btn_f, bg=BG)
        action_frame.pack(side="right", pady=5)

        # ---------------------------------------------------------
        # GROUP 1: Aksi Utama (Tambah & Refresh)
        # ---------------------------------------------------------
        styled_btn(action_frame, "➕ Tambah", self._open_add).pack(side="left", padx=(0, 5))
        # Refresh ditaruh bersebelahan dengan tambah, gunakan warna netral
        styled_btn(action_frame, "🔄 Refresh", self.refresh, color=SURFACE, fg=TEXT).pack(side="left", padx=(0, 20))

        # ---------------------------------------------------------
        # GROUP 2: Aksi Operasional (Check-In & Check-Out)
        # Diberi jarak lebih (padx 20 di kiri) agar terpisah dari Group 1
        # ---------------------------------------------------------
        styled_btn(action_frame, "🔑 Check-In", self._check_in, color=SUCCESS).pack(side="left", padx=(0, 5))
        styled_btn(action_frame, "📤 Check-Out", self._check_out, color="#17a2b8").pack(side="left", padx=(0, 20))

        # ---------------------------------------------------------
        # GROUP 3: Aksi Modifikasi (Edit & Batal)
        # ---------------------------------------------------------
        # Ubah Edit menjadi warna netral (SURFACE) agar tidak terlalu banyak warna warni
        styled_btn(action_frame, "📝 Edit", self._open_edit, color=SURFACE, fg=TEXT).pack(side="left", padx=(0, 5))
        styled_btn(action_frame, "❌ Batalkan", self._cancel_booking, color=DANGER).pack(side="left", padx=(0, 0))

        cols = ("ID", "Tamu", "Kamar", "Check-In", "Check-Out", "Status", "Total")
        self.tree = build_tree(self, cols, cols, [50, 180, 80, 110, 110, 100, 130])
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.refresh()

    def _auto_update_status(self):
        """Otomatis ubah status ke Checked Out jika sudah waktunya"""
        conn = get_connection()
        if not conn: return
        c = conn.cursor()
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            
            # 1. Cari booking yang statusnya 'Checked In' tapi tanggal out <= hari ini
            # Kita ambil room_id-nya juga buat balikin status kamar
            query_find = "SELECT id, room_id FROM bookings WHERE status = 'Checked In' AND check_out <= %s"
            c.execute(query_find, (today,))
            to_update = c.fetchall()

            for b_id, r_id in to_update:
                # 2. Update status booking jadi Checked Out
                c.execute("UPDATE bookings SET status = 'Checked Out' WHERE id = %s", (b_id,))
                # 3. Balikin status kamar jadi Available
                c.execute("UPDATE rooms SET status = 'Available' WHERE id = %s", (r_id,))
            
            conn.commit()
        except Exception as e:
            print(f"Error auto-update: {e}")
        finally:
            c.close()
            conn.close()

    def _on_select(self, _):
        sel = self.tree.selection()
        if sel:
            # Simpan data baris yang dipilih buat dipake Check-In
            self.selected_id = self.tree.item(sel[0])['values']

    def refresh(self):
        # 1. Update status otomatis di DB sebelum data ditarik
        self._auto_update_status()
        
        # 2. Bersihkan isi tabel Treeview
        for row in self.tree.get_children(): 
            self.tree.delete(row)
            
        # 3. Tarik data terbaru
        conn = get_connection()
        if not conn: return
        c = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT b.id, g.name, r.number, b.check_in, b.check_out, b.status, b.total_price
                FROM bookings b
                LEFT JOIN guests g ON b.guest_id = g.id
                LEFT JOIN rooms r ON b.room_id = r.id
                ORDER BY b.id DESC
            """
            c.execute(query)
            for row in c.fetchall():
                self.tree.insert("", "end", values=(
                    row['id'], row['name'] or "---", row['number'] or "---",
                    row['check_in'], row['check_out'], row['status'],
                    fmt_currency(row['total_price'])
                ))
        finally:
            c.close()
            conn.close()

    def _open_add(self):
        # Buka popup tambah reservasi
        BookingDialog(self, self.refresh)

    def _open_edit(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data dulu!")
            return
            
        # Proteksi: Kalau sudah Checked Out, jangan kasih edit!
        if self.selected_id[5] == "Checked Out":
            messagebox.showwarning("Dilarang", "Data yang sudah Checked Out tidak bisa diedit!")
            return
            
        BookingDialog(self, self.refresh, edit_data=self.selected_id)

    def _check_in(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data reservasi dari tabel dulu!")
            return
            
        b_id = self.selected_id[0]
        r_num = self.selected_id[2]

        if messagebox.askyesno("Konfirmasi", f"Proses Check-In untuk Kamar {r_num}?"):
            conn = get_connection()
            if not conn: return
            c = conn.cursor()
            try:
                # 1. Update status booking
                c.execute("UPDATE bookings SET status = 'Checked In' WHERE id = %s", (b_id,))
                # 2. Update status kamar jadi Occupied
                c.execute("UPDATE rooms SET status = 'Occupied' WHERE number = %s", (r_num,))
                
                conn.commit()
                messagebox.showinfo("Sukses", "Tamu berhasil Check-In!")
                self.refresh()
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Gagal", f"Error: {e}")
            finally:
                c.close()
                conn.close()

    # fungsi check-out
    def _check_out(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data reservasi dari tabel dulu!")
            return
            
        b_id = self.selected_id[0]
        r_num = self.selected_id[2]
        status_skrg = self.selected_id[5]

        # Proteksi: Hanya yang berstatus Checked In yang bisa Check-Out
        if status_skrg != 'Checked In':
            messagebox.showwarning("Peringatan", "Hanya tamu dengan status 'Checked In' yang bisa melakukan Check-Out!")
            return

        conn = get_connection()
        if not conn: return
        c = conn.cursor(dictionary=True)
        
        try:
            # 1. Ambil data reservasi dan harga kamar
            c.execute("""
                SELECT b.check_in, b.check_out, b.total_price, r.price 
                FROM bookings b
                JOIN rooms r ON b.room_id = r.id
                WHERE b.id = %s
            """, (b_id,))
            data = c.fetchone()

            # Format string tanggal ke tipe datetime untuk dihitung
            check_in_date = datetime.strptime(str(data['check_in']), "%Y-%m-%d")
            original_check_out = datetime.strptime(str(data['check_out']), "%Y-%m-%d")
            
            # Waktu hari ini
            today = datetime.now()
            today_str = today.strftime("%Y-%m-%d")
            today_date = datetime.strptime(today_str, "%Y-%m-%d")

            room_price = data['price']
            original_total = data['total_price']

            # 2. Hitung jumlah hari aktual tamu menginap
            actual_days = (today_date - check_in_date).days
            if actual_days <= 0: 
                actual_days = 1 # Minimal dihitung 1 hari walaupun check-out di hari yang sama

            # 3. Hitung total bayar aktual
            actual_total = room_price * actual_days

            # 4. Buat pesan konfirmasi
            msg = f"Proses Check-Out untuk Kamar {r_num}?\n"
            
            # Jika Check-out lebih awal dari jadwal
            if today_date < original_check_out:
                selisih_uang = original_total - actual_total
                if selisih_uang > 0:
                    msg += f"\n[INFO] Tamu Check-Out lebih awal!\n"
                    msg += f"Tagihan disesuaikan untuk {actual_days} malam.\n"
                    msg += f"Total Baru: {fmt_currency(actual_total)}\n"
                    msg += f"Uang yang dikembalikan (Refund): {fmt_currency(selisih_uang)}"

            # Tampilkan pop-up konfirmasi
            if messagebox.askyesno("Konfirmasi Check-Out", msg):
                # 5. Eksekusi Update ke Database
                # Update status jadi Checked Out, sesuaikan tanggal out dan total harganya
                c.execute("""
                    UPDATE bookings 
                    SET status = 'Checked Out', check_out = %s, total_price = %s 
                    WHERE id = %s
                """, (today_str, actual_total, b_id))
                
                # Kosongkan kamar
                c.execute("UPDATE rooms SET status = 'Available' WHERE number = %s", (r_num,))
                
                conn.commit()
                messagebox.showinfo("Sukses", "Proses Check-Out berhasil!")
                self.refresh()

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
        finally:
            c.close()
            conn.close()

    #code untuk cancel
    def _cancel_booking(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih reservasi yang mau dibatalkan!")
            return
            
        b_id = self.selected_id[0]
        r_num = self.selected_id[2]
        status_skrg = self.selected_id[5]

        # PROTEKSI TAMBAHAN
        if status_skrg == 'Checked In':
            messagebox.showerror("Gagal", "Tamu sudah Check-In, tidak bisa dibatalkan!")
            return
        
        if status_skrg in ['Checked Out', 'Cancelled']:
            messagebox.showwarning("Peringatan", f"Reservasi ini sudah {status_skrg}!")
            return

        if messagebox.askyesno("Konfirmasi", f"Batalkan reservasi ID {b_id} (Kamar {r_num})?"):
            conn = get_connection()
            if not conn: return
            c = conn.cursor()
            try:
                # 1. Update status booking jadi Cancelled
                c.execute("UPDATE bookings SET status = 'Cancelled' WHERE id = %s", (b_id,))
                
                # 2. Balikin status kamar jadi Available
                c.execute("UPDATE rooms SET status = 'Available' WHERE number = %s", (r_num,))
                
                conn.commit()
                messagebox.showinfo("Sukses", "Reservasi telah dibatalkan!")
                self.refresh() # Refresh tabel
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", str(e))
            finally:
                c.close()
                conn.close()

# --- DIALOG POPUP TAMBAH RESERVASI ---
class BookingDialog(tk.Toplevel):
    # TAMBAHKAN edit_data=None di argumen fungsi ini
    def __init__(self, master, callback, edit_data=None): 
        super().__init__(master)
        self.callback = callback
        self.edit_data = edit_data # <--- HARUS DISIMPAN KE SELF
        
        # Biar judulnya dinamis
        self.title("Edit Reservasi" if edit_data else "Tambah Reservasi")
        self.geometry("450x650") # Agak tinggiin dikit biar gak kepotong
        self.configure(bg=BG)
        self.grab_set()
        
        self.guest_list = [] 
        self.room_data = [] 
        
        self._build()
        self._load_data()

        # Sekarang pengecekan ini bakal jalan karena self.edit_data sudah ada
        if self.edit_data:
            self._fill_form()

    def _build(self):
        f = card_frame(self)
        f.pack(padx=20, pady=20, fill="both", expand=True)

        # --- INPUT TAMU ---
        tk.Label(f, text="Ketik Nama Tamu", bg=CARD, fg=TEXT_DIM).pack(pady=(10,0))
        self.cb_guest = ttk.Combobox(f, font=FONT_LABEL)
        self.cb_guest.pack(fill="x", pady=5, padx=15)
        self.cb_guest.bind("<KeyRelease>", self._filter_guests)

        # --- INPUT KAMAR ---
        tk.Label(f, text="Pilih Kamar Tersedia", bg=CARD, fg=TEXT_DIM).pack(pady=(10,0))
        self.cb_room = ttk.Combobox(f, font=FONT_LABEL, state="readonly")
        self.cb_room.pack(fill="x", pady=5, padx=15)
        # Bind ketika kamar dipilih untuk hitung harga awal
        self.cb_room.bind("<<ComboboxSelected>>", lambda e: self._update_total_price())

        # --- INPUT TANGGAL ---
        tk.Label(f, text="Check-in (YYYY-MM-DD)", bg=CARD, fg=TEXT_DIM).pack(pady=(10,0))
        self.ent_in = styled_entry(f)
        self.ent_in.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.ent_in.pack(pady=5)
        # Bind ketika user selesai ngetik tanggal atau pindah kolom
        self.ent_in.bind("<FocusOut>", lambda e: self._auto_set_checkout())

        tk.Label(f, text="Check-out (YYYY-MM-DD)", bg=CARD, fg=TEXT_DIM).pack(pady=(10,0))
        self.ent_out = styled_entry(f)
        self.ent_out.pack(pady=5)
        self.ent_out.bind("<FocusOut>", lambda e: self._update_total_price())

        # --- DISPLAY TOTAL HARGA (VISUAL SAJA) ---
        self.lbl_total = tk.Label(f, text="Total: Rp 0", bg=CARD, fg=ACCENT, font=("Segoe UI Bold", 12))
        self.lbl_total.pack(pady=10)

        styled_btn(self, "💾 SIMPAN RESERVASI", self._save).pack(pady=20)
        
        # Jalankan set default pertama kali
        self._auto_set_checkout()

    def _auto_set_checkout(self):
        """Otomatis set check-out 1 hari setelah check-in"""
        try:
            date_in = datetime.strptime(self.ent_in.get(), "%Y-%m-%d")
            date_out = date_in + timedelta(days=1)
            
            self.ent_out.delete(0, tk.END)
            self.ent_out.insert(0, date_out.strftime("%Y-%m-%d"))
            
            self._update_total_price()
        except:
            pass

    

    def _update_total_price(self):
        """Hitung harga: (Harga Kamar * Selisih Hari)"""
        try:
            # Ambil harga kamar dari data yang di-load
            sel_room = self.cb_room.get()
            r_num = sel_room.split("Room ")[1].split(" -")[0]
            room_info = next(item for item in self.room_data if str(item['number']) == r_num)
            price_per_night = room_info['price']

            # Hitung selisih hari
            d1 = datetime.strptime(self.ent_in.get(), "%Y-%m-%d")
            d2 = datetime.strptime(self.ent_out.get(), "%Y-%m-%d")
            days = (d2 - d1).days

            if days <= 0: days = 1 # Minimal hitung 1 hari jika salah input
            
            self.current_total = price_per_night * days
            self.lbl_total.config(text=f"Total ({days} Malam): {fmt_currency(self.current_total)}")
        except:
            self.current_total = 0

    def _fill_form(self):
        """Isi form berdasarkan data yang dipilih di tabel"""
        # edit_data format: (ID, Tamu, Kamar, Check-In, Check-Out, Status, Total)
        self.cb_guest.set(self.edit_data[1]) # Set Nama Tamu
        self.cb_room.set(f"Room {self.edit_data[2]}") # Set Nomor Kamar
        
        self.ent_in.delete(0, tk.END)
        self.ent_in.insert(0, self.edit_data[3])
        
        self.ent_out.delete(0, tk.END)
        self.ent_out.insert(0, self.edit_data[4])
        
        self._update_total_price()

    def _load_data(self):
        conn = get_connection()
        c = conn.cursor(dictionary=True)
        
        # Load Tamu ke list master
        c.execute("SELECT id, name FROM guests")
        rows = c.fetchall()
        self.guest_list = [f"{g['name']} (ID:{g['id']})" for g in rows]
        self.cb_guest['values'] = self.guest_list

        # Load Kamar Available
        c.execute("SELECT id, number, price FROM rooms WHERE status = 'Available'")
        self.room_data = c.fetchall()
        self.cb_room['values'] = [f"Room {r['number']} - Rp {r['price']:,}" for r in self.room_data]
        
        c.close()
        conn.close()

    def _filter_guests(self, event):
        """Fungsi nyaring nama dengan delay agar tidak macet"""
        # 1. Abaikan tombol navigasi
        if event.keysym in ("Up", "Down", "Return", "Escape", "Tab", "Shift_L", "Control_L"):
            return

        # 2. Batalkan pencarian sebelumnya (biar gak numpuk pas ngetik cepet)
        if hasattr(self, '_after_id'):
            self.after_cancel(self._after_id)

        # 3. Jalankan filter setelah user berhenti ngetik selama 300ms
        self._after_id = self.after(300, self._do_filter)

    def _do_filter(self):
        """Logika filter yang dipisah agar tidak memberatkan thread utama"""
        value = self.cb_guest.get().lower()
        
        if len(value) < 1:
            self.cb_guest['values'] = self.guest_list
            return

        filtered_data = [item for item in self.guest_list if value in item.lower()]
        self.cb_guest['values'] = filtered_data
        
        try:
            # Gunakan post() alih-alih event_generate biar lebih stabil
            self.cb_guest.post() 
            # Kembalikan fokus dan kursor ke posisi paling akhir
            self.cb_guest.focus_set()
            self.cb_guest.icursor(tk.END)
        except:
            pass

    def _save(self):
        try:
            # 1. Ambil data dari form
            sel_guest = self.cb_guest.get()
            g_id = int(sel_guest.split("(ID:")[1].split(")")[0])

            sel_room = self.cb_room.get()
            r_num = sel_room.split("Room ")[1].split(" -")[0] if " -" in sel_room else sel_room.replace("Room ", "")
            
            room_info = next(item for item in self.room_data if str(item['number']) == str(r_num))
            r_id = room_info['id']
            price_per_night = room_info['price']

            d_in = self.ent_in.get()
            d_out = self.ent_out.get()
            
            days = (datetime.strptime(d_out, "%Y-%m-%d") - datetime.strptime(d_in, "%Y-%m-%d")).days
            if days <= 0: days = 1
            total_bayar = price_per_night * days

            conn = get_connection()
            c = conn.cursor()
            
            try:
                # --- LOGIKA VALIDASI: CEK APAKAH TAMU MASIH PUNYA RESERVASI AKTIF ---
                # Jika sedang EDIT, kita kecualikan ID booking yang sedang diedit ini
                check_query = """
                    SELECT id FROM bookings 
                    WHERE guest_id = %s 
                    AND status IN ('Reserved', 'Checked In')
                """
                check_params = [g_id]
                
                if self.edit_data:
                    check_query += " AND id != %s"
                    check_params.append(self.edit_data[0])
                
                c.execute(check_query, tuple(check_params))
                active_booking = c.fetchone()

                if active_booking:
                    messagebox.showerror("Akses Ditolak", 
                        "Tamu ini masih memiliki reservasi aktif atau belum Check-out!\n"
                        "Selesaikan transaksi sebelumnya terlebih dahulu.")
                    return # Hentikan proses simpan

                # --- PROSES SIMPAN (LANJUTAN KODE LAMA) ---
                if self.edit_data:
                    # Logika Update
                    b_id = self.edit_data[0]
                    old_room_num = self.edit_data[2]

                    c.execute("""
                        UPDATE bookings 
                        SET guest_id=%s, room_id=%s, check_in=%s, check_out=%s, total_price=%s
                        WHERE id=%s
                    """, (g_id, r_id, d_in, d_out, total_bayar, b_id))

                    if str(old_room_num) != str(r_num):
                        c.execute("UPDATE rooms SET status = 'Available' WHERE number = %s", (old_room_num,))
                        c.execute("UPDATE rooms SET status = 'Reserved' WHERE id = %s", (r_id,))
                else:
                    # Logika Insert Baru
                    c.execute("""
                        INSERT INTO bookings (guest_id, room_id, check_in, check_out, total_price, status)
                        VALUES (%s, %s, %s, %s, %s, 'Reserved')
                    """, (g_id, r_id, d_in, d_out, total_bayar))
                    c.execute("UPDATE rooms SET status = 'Reserved' WHERE id = %s", (r_id,))

                conn.commit()
                self.callback()
                self.destroy()
                messagebox.showinfo("Sukses", "Data berhasil diperbarui!" if self.edit_data else "Reservasi Berhasil!")

            except Exception as e:
                conn.rollback()
                messagebox.showerror("Database Error", str(e))
            finally:
                conn.close()

        except Exception as e:
            messagebox.showerror("Error", "Pastikan semua data dipilih dengan benar!")