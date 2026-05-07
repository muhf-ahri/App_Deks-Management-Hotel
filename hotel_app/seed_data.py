import sqlite3
from datetime import datetime, timedelta

def seed():
    conn = sqlite3.connect('database/db_reservasi.db') # Pastiin path-nya bener
    c = conn.cursor()

    try:
        # 1. Masukin Data Tamu (Guests)
        guests = [
            ('Fahri Muhammadani', '3273010101010001', '08123456789', 'fahri@email.com', 'Indonesia'),
            ('Budi Santoso', '3273010101010002', '08571234567', 'budi@email.com', 'Indonesia'),
            ('Siti Aminah', '3273010101010003', '08998765432', 'siti@email.com', 'Malaysia')
        ]
        c.executemany("INSERT INTO guests (name, id_number, phone, email, nationality) VALUES (?,?,?,?,?)", guests)

        # 2. Masukin Data Kamar (Rooms)
        rooms = [
            ('101', 'Standard', '1', 2, 350000, 'Available', 'Single bed, AC'),
            ('102', 'Standard', '1', 2, 350000, 'Occupied', 'Single bed, AC'),
            ('201', 'Deluxe', '2', 2, 550000, 'Available', 'Queen bed, Wifi, TV'),
            ('301', 'Suite', '3', 4, 120000, 'Reserved', 'King bed, Mini bar, Bathup')
        ]
        c.executemany("INSERT INTO rooms (number, type, floor, capacity, price, status, description) VALUES (?,?,?,?,?,?,?)", rooms)

        # 3. Masukin Data Booking (Biar Tabel Dashboard Isi)
        today = datetime.now().strftime('%Y-%m-%d')
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        bookings = [
            (1, 2, today, tomorrow, 350000, 'Checked In'), # Tamu 1 di Kamar 2
            (2, 4, today, tomorrow, 1200000, 'Reserved')   # Tamu 2 di Kamar 4
        ]
        c.executemany("INSERT INTO bookings (guest_id, room_id, check_in, check_out, total_price, status) VALUES (?,?,?,?,?,?)", bookings)

        # 4. Masukin Data Pembayaran (Biar "Omzet Hari Ini" gak Rp 0)
        c.execute("INSERT INTO payments (booking_id, amount, method, paid_at) VALUES (1, 350000, 'Cash', DATETIME('now'))")

        conn.commit()
        print("✅ Mantap! Data dummy berhasil disuntik. Sekarang buka main.py lagi!")
    except Exception as e:
        print(f"❌ Waduh Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    seed()