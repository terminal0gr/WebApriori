-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Εξυπηρετητής: 127.0.0.1
-- Χρόνος δημιουργίας: 09 Ιαν 2024 στις 22:26:06
-- Έκδοση διακομιστή: 10.4.32-MariaDB
-- Έκδοση PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
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
-- Δομή πίνακα για τον πίνακα `datasetfeatures`
--

CREATE TABLE `datasetfeatures` (
  `name` text NOT NULL,
  `AvgOfDistinctValuesPerCol` float NOT NULL DEFAULT 0,
  `AvgOfDistinctValuesOverAll` float NOT NULL DEFAULT 0,
  `AvgOfDistinctValuesPerRow` float NOT NULL DEFAULT 0,
  `FreqoFTop1FreqValue` float NOT NULL DEFAULT 0,
  `FreqoFTop2FreqValue` float NOT NULL DEFAULT 0,
  `FreqoFTop3FreqValue` float NOT NULL DEFAULT 0,
  `NumberOfColumns` int(11) NOT NULL DEFAULT 0,
  `FreqOfNumberCol` float NOT NULL DEFAULT 0,
  `FreqOfDateCol` float NOT NULL DEFAULT 0,
  `FreqOfStringCol` float NOT NULL DEFAULT 0,
  `FreqOfBoolCol` float NOT NULL DEFAULT 0,
  `MinItemLen` int(11) NOT NULL DEFAULT 9999,
  `MaxItemLen` int(11) NOT NULL DEFAULT 0,
  `AvgItemLen` float NOT NULL DEFAULT 0,
  `Freq1CharColumns` float NOT NULL DEFAULT 0,
  `Freq2ValuesItemColumns` float NOT NULL DEFAULT 0,
  `hasHeader` tinyint(1) NOT NULL DEFAULT 0,
  `datasetType` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Άδειασμα δεδομένων του πίνακα `datasetfeatures`
--

INSERT INTO `datasetfeatures` (`name`, `AvgOfDistinctValuesPerCol`, `AvgOfDistinctValuesOverAll`, `AvgOfDistinctValuesPerRow`, `FreqoFTop1FreqValue`, `FreqoFTop2FreqValue`, `FreqoFTop3FreqValue`, `NumberOfColumns`, `FreqOfNumberCol`, `FreqOfDateCol`, `FreqOfStringCol`, `FreqOfBoolCol`, `MinItemLen`, `MaxItemLen`, `AvgItemLen`, `Freq1CharColumns`, `Freq2ValuesItemColumns`, `hasHeader`, `datasetType`) VALUES
('0Fake02.csv', 0.376667, 0.375, 0.881667, 0.168333, 0.05, 0.05, 6, 0.5, 0, 0.333333, 0.166667, 1, 14, 4.31667, 0.166667, 0, 1, 0),
('0Fake04.csv', 0.208571, 0.17, 0.571429, 0.142857, 0.12, 0.0971429, 7, 0.714286, 0.142857, 0, 0.142857, 1, 19, 8.55714, 0.142857, 0, 1, 0),
('0Fake04_1.csv', 0.208571, 0.17, 0.571429, 0.142857, 0.12, 0.0971429, 7, 0.714286, 0.142857, 0, 0.142857, 1, 19, 8.55714, 0.142857, 0, 0, 0),
('0glass1.csv', 0.483, 0.48, 0.933, 0.165, 0.07, 0.03, 10, 0, 0, 1, 0, 4, 11, 7.515, 0, 0.1, 1, 0),
('2invoice.csv', 0.132759, 0.131034, 0.981724, 0.0344828, 0.0341379, 0.0337931, 29, 0.206897, 0.103448, 0.689655, 0, 1, 51, 9.44759, 0.0344828, 0.137931, 1, 2),
('2OrderDetails.csv', 0.27875, 0.2775, 1, 0.1, 0.05625, 0.05375, 8, 0.5, 0.125, 0.375, 0, 1, 35, 10.0887, 0, 0.125, 1, 2),
('2Sales.csv', 0.2632, 0.2556, 0.9136, 0.0388, 0.0324, 0.0288, 25, 0.36, 0.04, 0.6, 0, 1, 40, 6.8672, 0.04, 0.04, 1, 2),
('3a2.csv', 0.4, 0.08, 0.36, 0.6, 0.4, 0, 5, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 3),
('3a2100.csv', 0.02, 0.004, 0.36, 0.6, 0.4, 0, 5, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 3),
('3grocery_timestamp.csv', 0.0610563, 0.0297887, 0.0621127, 0.888944, 0.0466197, 0.0120423, 142, 0.464789, 0.028169, -3.81639e-17, 0.507042, 1, 19, 1.55183, 0.950704, 0.352113, 1, 3),
('3saleshourly.csv', 0.141538, 0.11, 0.508462, 0.527692, 0.112308, 0.0769231, 13, 0.692308, 0.0769231, 0.0769231, 0.153846, 1, 19, 3.57385, 0.384615, 0, 1, 3),
('3supermarket.txt', 0.0147926, 0.000184332, 0.0138249, 0.906037, 0.0893548, 0.00308756, 217, 0, 0, 1, 0, 1, 4, 1.01074, 0.995392, 0.479263, 1, 3),
('4car.dat', 0.0228571, 0.0171429, 0.815714, 0.285714, 0.142857, 0.0942857, 7, 0, 0, 1, 0, 1, 5, 3.65857, 0, 0, 1, 4),
('4CarSales01.csv', 0.19, 0.19, 1, 0.11375, 0.1125, 0.1075, 8, 0.25, 0, 0.75, 0, 1, 49, 10.7037, 0, 0.25, 1, 4),
('4mammographic.dat', 0.11, 0.0866667, 0.868333, 0.166667, 0.128333, 0.121667, 6, 0.166667, 0, 0.666667, 0.166667, 1, 2, 1.16667, 0.833333, 0.166667, 1, 4),
('4titanic02.csv', 0.0125, 0.0125, 1, 0.25, 0.25, 0.25, 4, 0, 0, 1, 0, 2, 5, 3.6425, 0, 0.25, 1, 4),
('4titanic02WithoutHeader.csv', 0.0125, 0.0125, 1, 0.25, 0.25, 0.25, 4, 0, 0, 1, 0, 2, 5, 3.6425, 0, 0.25, 0, 4);

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
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `usertable`
--

CREATE TABLE `usertable` (
  `email` varchar(30) NOT NULL,
  `passwd` varchar(60) NOT NULL,
  `oname` varchar(30) NOT NULL,
  `fname` varchar(30) NOT NULL,
  `webAPIKey` varchar(64) DEFAULT NULL,
  `key_created_at` timestamp NULL DEFAULT NULL,
  `administrator` int(11) NOT NULL DEFAULT 0,
  `grandPublicDatasets` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Άδειασμα δεδομένων του πίνακα `usertable`
--

INSERT INTO `usertable` (`email`, `passwd`, `oname`, `fname`, `webAPIKey`, `key_created_at`, `administrator`, `grandPublicDatasets`) VALUES
('terminal_gr@yahoo.com', '9d1af8040f2d26ccb4cc345a2bc264bb', 'Malliaridis', 'Konstantinos', NULL, NULL, 1, 1);

--
-- Ευρετήρια για άχρηστους πίνακες
--

--
-- Ευρετήρια για πίνακα `datasetfeatures`
--
ALTER TABLE `datasetfeatures`
  ADD PRIMARY KEY (`name`(100));

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
