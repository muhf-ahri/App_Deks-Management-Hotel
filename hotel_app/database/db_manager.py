import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='db_reservasi'
        )
        return conn
    except Error as e:
        print(f"❌ Koneksi SQLyog Gagal: {e}")
        return None

def verify_hotel_login(hotel_name, password):
    """Verifikasi login berdasarkan nama hotel dan password dari tabel hotels"""
    conn = get_connection()
    if not conn:
        return None
    
    c = conn.cursor(dictionary=True)
    try:
        query = "SELECT id, hotel_name, location FROM hotels WHERE hotel_name = %s AND password = %s"
        c.execute(query, (hotel_name, password))
        return c.fetchone()  # Mengembalikan dict {id, hotel_name, location} atau None
    except Exception as e:
        print(f"Login Error: {e}")
        return None
    finally:
        c.close()
        conn.close()

def init_db():
    conn = get_connection()
    if not conn: return
    
    cursor = conn.cursor(dictionary=True)
    try:
        # Tabel Hotels (untuk login multi-hotel)
        cursor.execute('''CREATE TABLE IF NOT EXISTS hotels (
            id INT AUTO_INCREMENT PRIMARY KEY,
            hotel_name VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            location VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB''')

        # Tabel Tamu
        cursor.execute('''CREATE TABLE IF NOT EXISTS guests (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            id_number VARCHAR(50) UNIQUE,
            phone VARCHAR(20),
            email VARCHAR(100),
            nationality VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB''')

        # Tabel Kamar
        cursor.execute('''CREATE TABLE IF NOT EXISTS rooms (
            id INT AUTO_INCREMENT PRIMARY KEY,
            number VARCHAR(10) UNIQUE NOT NULL,
            type VARCHAR(50),
            floor VARCHAR(10),
            capacity INT,
            price DECIMAL(15,2),
            status VARCHAR(20) DEFAULT 'Available',
            description TEXT
        ) ENGINE=InnoDB''')

        # Tabel Booking
        cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            guest_id INT,
            room_id INT,
            check_in DATE,
            check_out DATE,
            total_price DECIMAL(15,2),
            status VARCHAR(20) DEFAULT 'Reserved',
            CONSTRAINT fk_guest FOREIGN KEY (guest_id) REFERENCES guests(id) ON DELETE CASCADE,
            CONSTRAINT fk_room FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE
        ) ENGINE=InnoDB''')

        conn.commit()
        print("✅ Database db_reservasi Ready!")
    except Error as e:
        print(f"❌ Error Pas Bikin Tabel: {e}")
    finally:
        cursor.close()
        conn.close()

def seed_hotel_if_empty():
    """Tambahkan data hotel default jika tabel hotels masih kosong"""
    conn = get_connection()
    if not conn: return
    c = conn.cursor(dictionary=True)
    try:
        c.execute("SELECT COUNT(*) as total FROM hotels")
        total = c.fetchone()['total']
        if total == 0:
            c.execute(
                "INSERT INTO hotels (hotel_name, password, location) VALUES (%s, %s, %s)",
                ("Moko Hotel", "moko123", "Bandung, Jawa Barat")
            )
            conn.commit()
            print("✅ Data hotel default berhasil ditambahkan! (Moko Hotel / moko123)")
    except Exception as e:
        print(f"Seed hotel error: {e}")
    finally:
        c.close()
        conn.close()