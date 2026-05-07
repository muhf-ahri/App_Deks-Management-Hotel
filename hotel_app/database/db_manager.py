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

def init_db():
    conn = get_connection()
    if not conn: return
    
    # Pake dictionary=True biar init_db juga konsisten
    cursor = conn.cursor(dictionary=True) 
    try:
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
        print("✅ Database db_reservasi Ready, Nyet!")
    except Error as e:
        print(f"❌ Error Pas Bikin Tabel: {e}")
    finally:
        cursor.close()
        conn.close()