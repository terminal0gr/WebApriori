-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Φιλοξενητής: 127.0.0.1
-- Χρόνος δημιουργίας: 15 Οκτ 2019 στις 21:18:23
-- Έκδοση διακομιστή: 10.1.37-MariaDB
-- Έκδοση PHP: 7.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Βάση δεδομένων: `aprioribase`
--

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `temp_usertable`
--

CREATE TABLE `temp_usertable` (
  `confirm_code` varchar(50) NOT NULL,
  `temail` varchar(30) NOT NULL,
  `tpasswd` varchar(60) NOT NULL,
  `toname` varchar(30) NOT NULL,
  `tfname` varchar(30) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `usertable`
--

CREATE TABLE `usertable` (
  `email` varchar(30) NOT NULL,
  `passwd` varchar(60) NOT NULL,
  `oname` varchar(30) NOT NULL,
  `fname` varchar(30) NOT NULL,
  `webAPIKey` varchar(64) NULL,
  `key_created_at` timestamp NULL,
  `administrator` bit NOT NULL DEFAULT 0,
  `grandPublicDatasets` bit NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Άδειασμα δεδομένων του πίνακα `usertable`
--

INSERT INTO `usertable` (`email`, `passwd`, `oname`, `fname`) VALUES
('terminal_gr@yahoo.com', '19d6a3cd17bb2d786533535403136163', 'Malliaridis', 'Konstantinos');

--
-- Ευρετήρια για άχρηστους πίνακες
--

--
-- Ευρετήρια για πίνακα `temp_usertable`
--
ALTER TABLE `temp_usertable`
  ADD PRIMARY KEY (`temail`);

--
-- Ευρετήρια για πίνακα `usertable`
--
ALTER TABLE `usertable`
  ADD PRIMARY KEY (`email`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
