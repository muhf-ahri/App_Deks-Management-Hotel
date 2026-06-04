-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 04 Jun 2026 pada 06.40
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_reservasi`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `bookings`
--

CREATE TABLE `bookings` (
  `id` int(11) NOT NULL,
  `guest_id` int(11) DEFAULT NULL,
  `room_id` int(11) DEFAULT NULL,
  `check_in` date DEFAULT NULL,
  `check_out` date DEFAULT NULL,
  `total_price` decimal(15,2) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Reserved'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `bookings`
--

INSERT INTO `bookings` (`id`, `guest_id`, `room_id`, `check_in`, `check_out`, `total_price`, `status`) VALUES
(1, 1, 1, '2026-04-09', '2026-04-11', 700000.00, 'Checked Out'),
(2, 2, 4, '2026-04-10', '2026-04-12', 1100000.00, 'Checked Out'),
(3, 3, 11, '2026-04-09', '2026-04-10', 1200000.00, 'Checked Out'),
(4, 5, 10, '2026-04-09', '0000-00-00', 400000.00, 'Checked Out'),
(5, 6, 13, '2026-04-16', '2026-05-07', 26250000.00, 'Checked Out'),
(6, 3, 2, '2026-04-16', '2026-04-17', 350000.00, 'Cancelled'),
(7, 1, 3, '2026-04-16', '2026-04-19', 350000.00, 'Checked Out'),
(8, 7, 6, '2026-04-21', '2026-04-30', 5400000.00, 'Checked Out'),
(9, 8, 18, '2026-04-24', '2026-04-25', 2500000.00, 'Checked Out'),
(10, 9, 14, '2026-04-30', '2026-05-07', 17500000.00, 'Checked Out'),
(11, 10, 20, '2026-04-30', '2026-05-01', 500000.00, 'Checked Out'),
(12, 1, 10, '2026-04-30', '2026-05-02', 800000.00, 'Checked Out'),
(13, 11, 2, '2026-05-07', '2026-05-07', 350000.00, 'Checked Out'),
(14, 7, 10, '2026-05-07', '2026-05-07', 400000.00, 'Checked Out'),
(15, 7, 4, '2026-05-21', '2026-05-22', 550000.00, 'Checked Out');

-- --------------------------------------------------------

--
-- Struktur dari tabel `guests`
--

CREATE TABLE `guests` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `id_number` varchar(50) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `nationality` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `guests`
--

INSERT INTO `guests` (`id`, `name`, `id_number`, `phone`, `email`, `nationality`) VALUES
(1, 'Fahri Muhammadani', '327301090800001', '08123456789', 'fahri@example.com', 'Indonesia'),
(2, 'Budi Santoso', '327301090800002', '08571234567', 'budi@gmail.com', 'Indonesia'),
(3, 'Siti Aminah', '327301090800003', '08991234567', 'siti@yahoo.com', 'Indonesia'),
(5, 'Hani Nuraeni', '327301090800004', '082130641298', 'hani@yahoo.com', 'Indonesia'),
(6, 'Anton Beni', '327301090800005', '090803017331', 'Antonbeni@gmail.com', 'Indonesia'),
(7, 'Ganjar Pranowo', '327301090800010', '082194714728', 'ganjar@gmail.com', 'Indonesia'),
(8, 'Zikri Kolin', '327301090800018', '083771273626', 'zikri@gmail.com', 'Indonesia'),
(9, 'Mikayla Rae Proudhita', '3273101090800018', '088612715725', 'mikayla123@gmail.com', 'Indonesia'),
(10, 'stefen', '00001', '087636366', 'setefen@gmail.com', 'Indonesia'),
(11, 'Gilang', '123819379174917', '0873545272362', 'gilang123@gmail.com', 'Malaysia');

-- --------------------------------------------------------

--
-- Struktur dari tabel `hotels`
--

CREATE TABLE `hotels` (
  `id` int(11) NOT NULL,
  `hotel_name` varchar(100) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `hotels`
--

INSERT INTO `hotels` (`id`, `hotel_name`, `password`, `location`) VALUES
(10, 'Moko Hotel', 'moko123', 'Bandung, Jawa Barat');

-- --------------------------------------------------------

--
-- Struktur dari tabel `payments`
--

CREATE TABLE `payments` (
  `id` int(11) NOT NULL,
  `booking_id` int(11) DEFAULT NULL,
  `amount` decimal(15,2) DEFAULT NULL,
  `method` varchar(50) DEFAULT NULL,
  `paid_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `rooms`
--

CREATE TABLE `rooms` (
  `id` int(11) NOT NULL,
  `number` varchar(10) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `floor` varchar(10) DEFAULT NULL,
  `capacity` int(11) DEFAULT NULL,
  `price` decimal(15,2) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Available',
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `rooms`
--

INSERT INTO `rooms` (`id`, `number`, `type`, `floor`, `capacity`, `price`, `status`, `description`) VALUES
(1, '101', 'Standard', '1', 2, 350000.00, 'Available', 'Kamar nyaman dengan kasur Queen Size'),
(2, '102', 'Standard', '1', 2, 350000.00, 'Available', 'Kamar nyaman dengan kasur Queen Size'),
(3, '103', 'Standard', '1', 2, 350000.00, 'Available', 'Kamar nyaman dengan kasur Queen Size'),
(4, '104', 'Deluxe', '1', 2, 550000.00, 'Available', 'Kamar luas dengan City View'),
(5, '105', 'Deluxe', '1', 2, 550000.00, 'Available', 'Kamar luas dengan City View'),
(6, '201', 'Deluxe', '2', 2, 600000.00, 'Available', 'Pemandangan taman dan balkon pribadi'),
(7, '202', 'Deluxe', '2', 2, 600000.00, 'Available', 'Pemandangan taman dan balkon pribadi'),
(8, '203', 'Family', '2', 4, 850000.00, 'Available', 'Cocok untuk keluarga, 2 Queen Beds'),
(9, '204', 'Family', '2', 4, 850000.00, 'Available', 'Cocok untuk keluarga, 2 Queen Beds'),
(10, '205', 'Standard', '2', 2, 400000.00, 'Available', 'Kamar standar lantai atas'),
(11, '301', 'Suite', '3', 2, 1200000.00, 'Available', 'Fasilitas mewah, Bathtub, & Minibar'),
(12, '302', 'Suite', '3', 2, 1200000.00, 'Available', 'Fasilitas mewah, Bathtub, & Minibar'),
(13, '303', 'Suite', '3', 2, 1250000.00, 'Available', 'King Size Bed dengan Smart TV 55 inch'),
(14, '304', 'Penthouse', '3', 4, 2500000.00, 'Available', 'Lantai paling atas, fasilitas paling lengkap'),
(15, '305', 'Standard', '3', 2, 450000.00, 'Available', 'Kamar standar dengan view terbaik'),
(16, '306', 'Standard', '4', 2, 200000.00, 'Available', NULL),
(18, '310', 'Penthouse', '4', 5, 2500000.00, 'Available', 'ABCDE'),
(20, '400', 'Family', '1', 2, 500000.00, 'Available', '');

-- --------------------------------------------------------

--
-- Struktur dari tabel `services`
--

CREATE TABLE `services` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `category` enum('Food','Beverage','Laundry','Other') DEFAULT 'Food',
  `price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `services`
--

INSERT INTO `services` (`id`, `name`, `category`, `price`) VALUES
(1, 'Mie ayam Spesial', 'Food', 80000.00),
(2, 'Jasa Laundry', 'Laundry', 100000.00),
(3, 'Pijat Terapi', 'Other', 100000.00),
(4, 'Laundry Luar/Dalam', 'Other', 200000.00);

-- --------------------------------------------------------

--
-- Struktur dari tabel `service_orders`
--

CREATE TABLE `service_orders` (
  `id` int(11) NOT NULL,
  `booking_id` int(11) DEFAULT NULL,
  `service_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT 1,
  `order_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `status` enum('Pending','Processing','Delivered') DEFAULT 'Pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `service_orders`
--

INSERT INTO `service_orders` (`id`, `booking_id`, `service_id`, `quantity`, `order_date`, `status`) VALUES
(1, 1, 1, 100, '2026-04-16 05:10:37', 'Delivered'),
(2, 3, 2, 10, '2026-04-16 06:03:34', 'Delivered'),
(3, 10, 1, 8, '2026-04-30 04:21:50', 'Delivered'),
(4, 5, 4, 1, '2026-04-30 04:23:31', 'Delivered');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `guest_id` (`guest_id`),
  ADD KEY `room_id` (`room_id`);

--
-- Indeks untuk tabel `guests`
--
ALTER TABLE `guests`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_number` (`id_number`);

--
-- Indeks untuk tabel `hotels`
--
ALTER TABLE `hotels`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_booking` (`booking_id`);

--
-- Indeks untuk tabel `rooms`
--
ALTER TABLE `rooms`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `number` (`number`);

--
-- Indeks untuk tabel `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `service_orders`
--
ALTER TABLE `service_orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_id` (`booking_id`),
  ADD KEY `service_id` (`service_id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `bookings`
--
ALTER TABLE `bookings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT untuk tabel `guests`
--
ALTER TABLE `guests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT untuk tabel `hotels`
--
ALTER TABLE `hotels`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT untuk tabel `payments`
--
ALTER TABLE `payments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `rooms`
--
ALTER TABLE `rooms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT untuk tabel `services`
--
ALTER TABLE `services`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT untuk tabel `service_orders`
--
ALTER TABLE `service_orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`guest_id`) REFERENCES `guests` (`id`),
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`);

--
-- Ketidakleluasaan untuk tabel `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `fk_booking` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `service_orders`
--
ALTER TABLE `service_orders`
  ADD CONSTRAINT `service_orders_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `service_orders_ibfk_2` FOREIGN KEY (`service_id`) REFERENCES `services` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
