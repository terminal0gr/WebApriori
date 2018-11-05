-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Φιλοξενητής: 127.0.0.1
-- Χρόνος δημιουργίας: 23 Οκτ 2018 στις 23:41:16
-- Έκδοση διακομιστή: 10.1.36-MariaDB
-- Έκδοση PHP: 5.6.38

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Βάση δεδομένων: `flightsdata`
--

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `apicall`
--

CREATE TABLE `apicall` (
  `Id` bigint(20) NOT NULL,
  `CDate` datetime NOT NULL,
  `Url` text COLLATE utf8_unicode_ci NOT NULL,
  `State` tinyint(4) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `ib_flight`
--

CREATE TABLE `ib_flight` (
  `Id` bigint(20) NOT NULL,
  `Inbound_Id` bigint(20) NOT NULL,
  `departs_at` datetime NOT NULL,
  `arrives_at` datetime NOT NULL,
  `Origin_Airport` varchar(3) COLLATE utf8_unicode_ci NOT NULL,
  `destination_Airport` varchar(3) COLLATE utf8_unicode_ci NOT NULL,
  `marketing_airline` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  `operating_airline` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  `flight_number` varchar(5) COLLATE utf8_unicode_ci NOT NULL,
  `aircraft` varchar(5) COLLATE utf8_unicode_ci NOT NULL,
  `travel_class` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `booking_code` varchar(2) COLLATE utf8_unicode_ci DEFAULT NULL,
  `seats_remaining` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `inbound`
--

CREATE TABLE `inbound` (
  `Id` bigint(20) NOT NULL,
  `Iterenary_Id` bigint(20) NOT NULL,
  `Duration` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `itineraries`
--

CREATE TABLE `itineraries` (
  `Id` bigint(20) NOT NULL,
  `Result_Id` bigint(20) NOT NULL,
  `f_total_Price` decimal(10,2) NOT NULL,
  `f_adult_total_fare` decimal(10,2) NOT NULL DEFAULT '0.00',
  `f_adult_tax` decimal(10,2) NOT NULL DEFAULT '0.00',
  `f_child_total_fare` decimal(10,2) NOT NULL DEFAULT '0.00',
  `f_child_tax` decimal(10,2) NOT NULL DEFAULT '0.00',
  `f_infant_total_fare` decimal(10,2) NOT NULL DEFAULT '0.00',
  `f_infant_tax` decimal(10,2) NOT NULL DEFAULT '0.00',
  `restrictions_refundable` bit(1) NOT NULL DEFAULT b'0',
  `restrictions_change_penalties` bit(1) NOT NULL DEFAULT b'0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `ob_flight`
--

CREATE TABLE `ob_flight` (
  `Id` bigint(20) NOT NULL,
  `Outbound_Id` bigint(20) NOT NULL,
  `departs_at` datetime NOT NULL,
  `arrives_at` datetime NOT NULL,
  `Origin_Airport` varchar(3) COLLATE utf8_unicode_ci NOT NULL,
  `destination_Airport` varchar(3) COLLATE utf8_unicode_ci NOT NULL,
  `marketing_airline` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  `operating_airline` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  `flight_number` varchar(5) COLLATE utf8_unicode_ci NOT NULL,
  `aircraft` varchar(5) COLLATE utf8_unicode_ci NOT NULL,
  `travel_class` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `booking_code` varchar(2) COLLATE utf8_unicode_ci DEFAULT NULL,
  `seats_remaining` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `outbound`
--

CREATE TABLE `outbound` (
  `Id` bigint(20) NOT NULL,
  `Iterenary_Id` bigint(20) NOT NULL,
  `Duration` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `result`
--

CREATE TABLE `result` (
  `Id` bigint(20) NOT NULL,
  `currency` varchar(3) COLLATE utf8_unicode_ci NOT NULL,
  `apicall_Id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Ευρετήρια για άχρηστους πίνακες
--

--
-- Ευρετήρια για πίνακα `apicall`
--
ALTER TABLE `apicall`
  ADD PRIMARY KEY (`Id`);

--
-- Ευρετήρια για πίνακα `ib_flight`
--
ALTER TABLE `ib_flight`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `inbound_Id` (`Inbound_Id`);

--
-- Ευρετήρια για πίνακα `inbound`
--
ALTER TABLE `inbound`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `Iterenary_Id` (`Iterenary_Id`);

--
-- Ευρετήρια για πίνακα `itineraries`
--
ALTER TABLE `itineraries`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `itineraries_ibfk_1` (`Result_Id`);

--
-- Ευρετήρια για πίνακα `ob_flight`
--
ALTER TABLE `ob_flight`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `Outbound_Id` (`Outbound_Id`);

--
-- Ευρετήρια για πίνακα `outbound`
--
ALTER TABLE `outbound`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `Iterenary_Id` (`Iterenary_Id`);

--
-- Ευρετήρια για πίνακα `result`
--
ALTER TABLE `result`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `apicall_Id` (`apicall_Id`);

--
-- AUTO_INCREMENT για άχρηστους πίνακες
--

--
-- AUTO_INCREMENT για πίνακα `apicall`
--
ALTER TABLE `apicall`
  MODIFY `Id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT για πίνακα `ib_flight`
--
ALTER TABLE `ib_flight`
  MODIFY `Id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT για πίνακα `inbound`
--
ALTER TABLE `inbound`
  MODIFY `Id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT για πίνακα `itineraries`
--
ALTER TABLE `itineraries`
  MODIFY `Id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT για πίνακα `ob_flight`
--
ALTER TABLE `ob_flight`
  MODIFY `Id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT για πίνακα `outbound`
--
ALTER TABLE `outbound`
  MODIFY `Id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT για πίνακα `result`
--
ALTER TABLE `result`
  MODIFY `Id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- Περιορισμοί για άχρηστους πίνακες
--

--
-- Περιορισμοί για πίνακα `ib_flight`
--
ALTER TABLE `ib_flight`
  ADD CONSTRAINT `ib_flight_ibfk_1` FOREIGN KEY (`Inbound_Id`) REFERENCES `inbound` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `inbound`
--
ALTER TABLE `inbound`
  ADD CONSTRAINT `inbound_ibfk_1` FOREIGN KEY (`Iterenary_Id`) REFERENCES `itineraries` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `itineraries`
--
ALTER TABLE `itineraries`
  ADD CONSTRAINT `itineraries_ibfk_1` FOREIGN KEY (`Result_Id`) REFERENCES `result` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `ob_flight`
--
ALTER TABLE `ob_flight`
  ADD CONSTRAINT `ob_flight_ibfk_1` FOREIGN KEY (`Outbound_Id`) REFERENCES `outbound` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `outbound`
--
ALTER TABLE `outbound`
  ADD CONSTRAINT `outbound_ibfk_1` FOREIGN KEY (`Iterenary_Id`) REFERENCES `itineraries` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `result`
--
ALTER TABLE `result`
  ADD CONSTRAINT `result_ibfk_1` FOREIGN KEY (`apicall_Id`) REFERENCES `apicall` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
