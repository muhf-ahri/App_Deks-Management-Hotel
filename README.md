# 🏨 Hotel Management System (Moko Hotel)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)](https://docs.python.org/3/library/tkinter.html)
[![MySQL](https://img.shields.io/badge/Database-MySQL-4479A1.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> A modern desktop application for hotel management built with Python and Tkinter. Streamline your hotel operations with intuitive interfaces for room management, guest handling, reservations, and services.

![Hotel Management App](https://via.placeholder.com/800x400/4A90E2/FFFFFF?text=Hotel+Management+System+Screenshot)  
_Placeholder for app screenshot - Add your actual screenshot here_

## ✨ Features

### 🏠 Dashboard

- **Real-time Statistics**: View total rooms, occupied rooms, available rooms, and active guests
- **Recent Activities**: Monitor latest reservation activities with status updates
- **Quick Overview**: Get instant insights into hotel occupancy and performance

### 🛏️ Room Management

- **Add/Edit/Delete Rooms**: Full CRUD operations for room inventory
- **Room Details**: Store and view detailed descriptions for each room
- **Status Tracking**: Monitor room availability and maintenance status

### 👥 Guest Management

- **Guest Database**: Add, edit, and delete guest information
- **Advanced Search**: Search guests by name with instant results
- **Country Filtering**: Filter guests by nationality for better organization

### 📋 Reservation System

- **Create Reservations**: Book rooms for guests with check-in/check-out dates
- **Check-In/Check-Out**: Seamless guest arrival and departure management
- **Reservation Editing**: Modify reservations (restricted to unfinished bookings)
- **Cancellation**: Cancel reservations when needed
- **Auto Calculation**: Automatic total cost calculation including early check-out adjustments

### 🍽️ Service Management

- **Service Menu**: Manage available hotel services and amenities
- **Order Services**: Place service orders for checked-in guests
- **Service Tracking**: Mark services as completed/delivered
- **Master Services**: Maintain a comprehensive service catalog

## 🚀 Installation

### Prerequisites

- **Python 3.8 or higher**
- **MySQL Server** (for database storage)
- **Git** (for cloning the repository)

### Step-by-Step Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/muhf-ahri/App_Deks-Management-Hotel.git
   cd App_Deks-Management-Hotel
   ```

2. **Install Dependencies**

   ```bash
   pip install mysql-connector-python
   ```

3. **Setup MySQL Database**
   - Create a new database named `db_reservasi`

   ```sql
   CREATE DATABASE db_reservasi;
   ```

4. **Configure Database Connection**
   - Open `hotel_app/database/db_manager.py`
   - Update the connection parameters in `get_connection()` function:
     ```python
     def get_connection():
         return mysql.connector.connect(
             host="localhost",      # Change if needed
             user="root",           # Your MySQL username
             password="",           # Your MySQL password
             database="db_reservasi"
         )
     ```

5. **Seed Initial Data (Optional)**
   ```bash
   python hotel_app/seed_data.py
   ```
   > Note: Seed data uses SQLite by default. For MySQL integration, ensure database configuration matches.

## 🎯 Usage

### Running the Application

1. **Start the App**

   ```bash
   python hotel_app/main.py
   ```

2. **Navigate Through Features**
   - Use the left sidebar to switch between different modules
   - **Dashboard**: View statistics and recent activities
   - **Data Kamar**: Manage room inventory
   - **Data Tamu**: Handle guest information
   - **Reservasi**: Process bookings and check-ins/check-outs
   - **Master Layanan**: Configure available services
   - **Layanan Kamar**: Order and track guest services

### Basic Workflow

1. **Add Rooms**: Start by adding your hotel rooms to the system
2. **Register Guests**: Add guest information as they arrive
3. **Create Reservations**: Book rooms for guests with specific dates
4. **Check-In**: Process guest arrivals and assign rooms
5. **Manage Services**: Order additional services for guests
6. **Check-Out**: Calculate bills and process departures

## 🏗️ Project Structure

```
hotel_app/
├── main.py                 # Application entry point & navigation
├── seed_data.py           # Database seeding script
├── database/
│   └── db_manager.py      # Database connection & initialization
├── ui/
│   ├── widgets.py         # Reusable UI components
│   └── pages/
│       ├── dashboard.py   # Main dashboard page
│       ├── room_page.py   # Room management interface
│       ├── guest_page.py  # Guest management interface
│       ├── booking_page.py # Reservation system
│       ├── service_page.py # Service ordering
│       └── service_manage_page.py # Service catalog management
└── utils/
    ├── constants.py       # UI colors & fonts
    └── helpers.py         # Utility functions
```

## 🛠️ Technologies Used

- **Python 3.8+**: Core programming language
- **Tkinter**: GUI framework for desktop interface
- **MySQL**: Relational database for data persistence
- **MySQL Connector/Python**: Database connectivity

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

If you encounter any issues or have questions:

- Open an issue on GitHub
- Check the documentation in this README
- Ensure all dependencies are properly installed

---

**Built with ❤️ for efficient hotel management**

## Lisensi

Belum ada lisensi khusus.

epor