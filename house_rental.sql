-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 10 Feb 2025 pada 10.53
-- Versi server: 10.4.28-MariaDB
-- Versi PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `house_rental`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `maintenance_requests`
--

CREATE TABLE `maintenance_requests` (
  `request_id` int(11) NOT NULL,
  `property_id` int(11) DEFAULT NULL,
  `tenant_id` int(11) DEFAULT NULL,
  `issue_type` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `priority` enum('Low','Medium','High','Emergency') DEFAULT 'Medium',
  `status` enum('Pending','In Progress','Completed','Cancelled') DEFAULT 'Pending',
  `request_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `completion_date` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `owners`
--

CREATE TABLE `owners` (
  `owner_id` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `address` text DEFAULT NULL,
  `identity_number` varchar(50) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `payments`
--

CREATE TABLE `payments` (
  `payment_id` int(11) NOT NULL,
  `agreement_id` int(11) DEFAULT NULL,
  `amount` decimal(12,2) NOT NULL,
  `payment_date` date NOT NULL,
  `payment_method` enum('Cash','Bank Transfer','Credit Card','Digital Wallet') NOT NULL,
  `payment_status` enum('Pending','Completed','Failed') DEFAULT 'Pending',
  `payment_reference` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `properties`
--

CREATE TABLE `properties` (
  `property_id` int(11) NOT NULL,
  `property_name` varchar(100) NOT NULL,
  `address` text NOT NULL,
  `city` varchar(50) NOT NULL,
  `postal_code` varchar(10) DEFAULT NULL,
  `property_type` enum('House','Apartment','Villa','Townhouse') NOT NULL,
  `bedrooms` int(11) NOT NULL,
  `bathrooms` int(11) NOT NULL,
  `size_sqm` decimal(10,2) NOT NULL,
  `monthly_rent` decimal(12,2) NOT NULL,
  `is_furnished` tinyint(1) DEFAULT 0,
  `description` text DEFAULT NULL,
  `status` enum('Available','Rented','Maintenance') DEFAULT 'Available',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `property_images`
--

CREATE TABLE `property_images` (
  `image_id` int(11) NOT NULL,
  `property_id` int(11) DEFAULT NULL,
  `image_url` varchar(255) NOT NULL,
  `image_type` enum('Exterior','Interior','Floor Plan','Other') NOT NULL,
  `is_primary` tinyint(1) DEFAULT 0,
  `uploaded_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `property_ownership`
--

CREATE TABLE `property_ownership` (
  `property_id` int(11) NOT NULL,
  `owner_id` int(11) NOT NULL,
  `ownership_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `rental_agreements`
--

CREATE TABLE `rental_agreements` (
  `agreement_id` int(11) NOT NULL,
  `property_id` int(11) DEFAULT NULL,
  `tenant_id` int(11) DEFAULT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `monthly_rent` decimal(12,2) NOT NULL,
  `security_deposit` decimal(12,2) NOT NULL,
  `payment_due_day` int(11) NOT NULL,
  `status` enum('Active','Expired','Terminated') DEFAULT 'Active',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `tenants`
--

CREATE TABLE `tenants` (
  `tenant_id` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `identity_number` varchar(50) NOT NULL,
  `emergency_contact` varchar(100) DEFAULT NULL,
  `emergency_phone` varchar(20) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `maintenance_requests`
--
ALTER TABLE `maintenance_requests`
  ADD PRIMARY KEY (`request_id`),
  ADD KEY `property_id` (`property_id`),
  ADD KEY `tenant_id` (`tenant_id`);

--
-- Indeks untuk tabel `owners`
--
ALTER TABLE `owners`
  ADD PRIMARY KEY (`owner_id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `identity_number` (`identity_number`);

--
-- Indeks untuk tabel `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`payment_id`),
  ADD KEY `agreement_id` (`agreement_id`);

--
-- Indeks untuk tabel `properties`
--
ALTER TABLE `properties`
  ADD PRIMARY KEY (`property_id`);

--
-- Indeks untuk tabel `property_images`
--
ALTER TABLE `property_images`
  ADD PRIMARY KEY (`image_id`),
  ADD KEY `property_id` (`property_id`);

--
-- Indeks untuk tabel `property_ownership`
--
ALTER TABLE `property_ownership`
  ADD PRIMARY KEY (`property_id`,`owner_id`),
  ADD KEY `owner_id` (`owner_id`);

--
-- Indeks untuk tabel `rental_agreements`
--
ALTER TABLE `rental_agreements`
  ADD PRIMARY KEY (`agreement_id`),
  ADD KEY `property_id` (`property_id`),
  ADD KEY `tenant_id` (`tenant_id`);

--
-- Indeks untuk tabel `tenants`
--
ALTER TABLE `tenants`
  ADD PRIMARY KEY (`tenant_id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `identity_number` (`identity_number`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `maintenance_requests`
--
ALTER TABLE `maintenance_requests`
  MODIFY `request_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `owners`
--
ALTER TABLE `owners`
  MODIFY `owner_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `payments`
--
ALTER TABLE `payments`
  MODIFY `payment_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `properties`
--
ALTER TABLE `properties`
  MODIFY `property_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `property_images`
--
ALTER TABLE `property_images`
  MODIFY `image_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `rental_agreements`
--
ALTER TABLE `rental_agreements`
  MODIFY `agreement_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `tenants`
--
ALTER TABLE `tenants`
  MODIFY `tenant_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `maintenance_requests`
--
ALTER TABLE `maintenance_requests`
  ADD CONSTRAINT `maintenance_requests_ibfk_1` FOREIGN KEY (`property_id`) REFERENCES `properties` (`property_id`),
  ADD CONSTRAINT `maintenance_requests_ibfk_2` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`);

--
-- Ketidakleluasaan untuk tabel `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`agreement_id`) REFERENCES `rental_agreements` (`agreement_id`);

--
-- Ketidakleluasaan untuk tabel `property_images`
--
ALTER TABLE `property_images`
  ADD CONSTRAINT `property_images_ibfk_1` FOREIGN KEY (`property_id`) REFERENCES `properties` (`property_id`);

--
-- Ketidakleluasaan untuk tabel `property_ownership`
--
ALTER TABLE `property_ownership`
  ADD CONSTRAINT `property_ownership_ibfk_1` FOREIGN KEY (`property_id`) REFERENCES `properties` (`property_id`),
  ADD CONSTRAINT `property_ownership_ibfk_2` FOREIGN KEY (`owner_id`) REFERENCES `owners` (`owner_id`);

--
-- Ketidakleluasaan untuk tabel `rental_agreements`
--
ALTER TABLE `rental_agreements`
  ADD CONSTRAINT `rental_agreements_ibfk_1` FOREIGN KEY (`property_id`) REFERENCES `properties` (`property_id`),
  ADD CONSTRAINT `rental_agreements_ibfk_2` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
