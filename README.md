# Hotel Management System (Moko Hotel)

Sistem manajemen hotel berbasis **Python (Tkinter)** untuk mengelola data **Kamar**, **Tamu**, **Reservasi**, dan **Layanan Kamar**. Proyek ini dibuat untuk kebutuhan aplikasi desktop.

---

## Fitur Utama

- **Dashboard**: ringkasan statistik (kamar ready/terisi/tamu aktif) dan daftar aktivitas reservasi terbaru.
- **Manajemen Kamar**: tambah, edit, hapus, dan lihat detail deskripsi kamar.
- **Manajemen Tamu**: tambah, edit, hapus, pencarian nama, dan filter negara.
- **Reservasi**:
  - tambah reservasi
  - edit reservasi (dibatasi untuk reservasi yang belum selesai)
  - **Check-In** dan **Check-Out**
  - pembatalan reservasi
  - perhitungan total menginap pada saat **Check-Out** (termasuk penyesuaian jika check-out lebih awal)
- **Master Layanan & Layanan Kamar**:
  - master layanan/menu
  - pesan layanan untuk tamu pada booking status **Checked In**
  - tandai layanan **Selesai/Delivered**

---

## Teknologi yang Digunakan

- **Python**
- **Tkinter** (GUI)
- **MySQL** (untuk koneksi data via `mysql.connector`)

> Catatan: ada file `seed_data.py` yang melakukan seed menggunakan **SQLite**. Pastikan database yang digunakan sesuai dengan konfigurasi aplikasi.

---

## Struktur Proyek (Ringkas)

- `hotel_app/main.py` : entry point aplikasi dan sidebar navigasi
- `hotel_app/database/db_manager.py` : inisialisasi tabel di MySQL (`guests`, `rooms`, `bookings`)
- `hotel_app/ui/pages/` : halaman aplikasi (dashboard, room, guest, booking, service)
- `hotel_app/ui/widgets.py` : komponen UI reusable (styled button/entry, treeview, card)
- `hotel_app/utils/constants.py` : konstanta warna & font
- `hotel_app/utils/helpers.py` : helper format currency, dll.

---

## Cara Menjalankan

1. Pastikan Python terpasang.
2. Siapkan database **MySQL** bernama `db_reservasi`.
3. Jalankan aplikasi:

```bash
python hotel_app/main.py
```

Aplikasi akan memanggil `init_db()` untuk memastikan tabel yang diperlukan sudah tersedia.

---

## Konfigurasi Database

Koneksi MySQL ada di `hotel_app/database/db_manager.py` / fungsi `get_connection()`:

- host: `localhost`
- user: `root`
- password: _(kosong pada kode saat ini)_
- database: `db_reservasi`

Jika environment kamu berbeda, silakan sesuaikan kredensial di file terkait.

---

## Seed Data

File `hotel_app/seed_data.py` berfungsi untuk mengisi data dummy. Jalankan dengan:

```bash
python hotel_app/seed_data.py
```

Namun, karena seed ini memakai **SQLite** (`database/db_reservasi.db`) sementara aplikasi menggunakan **MySQL**, seed hanya akan bekerja jika kamu menjalankan skema/engine yang sama (SQLite vs MySQL) sesuai kebutuhan proyek.

---

## Requirement Tambahan

- MySQL Connector/Python:

```bash
pip install mysql-connector-python
```

---

## Screenshot / Demo

Jika kamu ingin, tambahkan screenshot hasil UI di sini.

---

## Lisensi

Belum ada lisensi khusus.
