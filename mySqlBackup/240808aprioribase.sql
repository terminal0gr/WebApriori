-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Εξυπηρετητής: 127.0.0.1
-- Χρόνος δημιουργίας: 09 Σεπ 2024 στις 16:32:26
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
CREATE DATABASE IF NOT EXISTS `aprioribase` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `aprioribase`;

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
  `FreqOfIntegerCol` float NOT NULL DEFAULT 0,
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
  `datasetType` int(11) NOT NULL DEFAULT 0,
  `type2Words` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Άδειασμα δεδομένων του πίνακα `datasetfeatures`
--

INSERT INTO `datasetfeatures` (`name`, `AvgOfDistinctValuesPerCol`, `AvgOfDistinctValuesOverAll`, `AvgOfDistinctValuesPerRow`, `FreqoFTop1FreqValue`, `FreqoFTop2FreqValue`, `FreqoFTop3FreqValue`, `NumberOfColumns`, `FreqOfIntegerCol`, `FreqOfNumberCol`, `FreqOfDateCol`, `FreqOfStringCol`, `FreqOfBoolCol`, `MinItemLen`, `MaxItemLen`, `AvgItemLen`, `Freq1CharColumns`, `Freq2ValuesItemColumns`, `hasHeader`, `datasetType`, `type2Words`) VALUES
('0abalone.data', 0.375111, 0.248222, 0.997333, 0.046, 0.0442222, 0.0208889, 9, 0.111111, 0.777778, 0, 0.111111, 0, 1, 6, 4.07667, 0.111111, 0, 0, 0, 0),
('0academic_detail.csv', 0.292824, 0.291667, 0.972222, 0.111111, 0.0555556, 0.0555556, 4, 0.25, 0, 0, 0.75, 0, 3, 29, 8.63194, 0, 0, 1, 0, 0),
('0All_Data_Aldi.csv', 0.21225, 0.20525, 0.99225, 0.125, 0.125, 0.1025, 8, 0.125, 0.25, 0, 0.5, 0.125, 1, 55, 9.8405, 0, 0.375, 1, 0, 0),
('0apple_quality.csv', 0.889333, 0.889333, 1, 0.0562222, 0.0548889, 0.000222222, 9, 0.111111, 0.777778, 0, 0.111111, 0, 1, 12, 9.554, 0, 0.111111, 1, 0, 0),
('0beer.csv', 0.273333, 0.242222, 0.986667, 0.0622222, 0.0611111, 0.0555556, 6, 0.166667, 0.666667, 0, 0.166667, 0, 1, 13, 4.20889, 0, 0, 1, 0, 0),
('0books_data.csv', 0.643678, 0.609195, 0.998851, 0.12069, 0.0218391, 0.016092, 6, 0.166667, 0.166667, 0, 0.666667, 0, 1, 72, 9.5569, 0, 0, 1, 0, 0),
('0CarSales01.csv', 0.1575, 0.1575, 1, 0.114, 0.105, 0.06275, 8, 0.25, 0, 0, 0.75, 0, 1, 49, 10.877, 0, 0.125, 1, 0, 0),
('0chord-fingers.csv', 0.276, 0.276, 1, 0.0536, 0.0504, 0.0328, 5, 0, 0, 0, 1, 0, 1, 19, 7.2772, 0, 0, 1, 0, 0),
('0classification_in_asteroseismology.csv', 0.5685, 0.568, 0.999, 0.174, 0.077, 0.0065, 4, 0, 0.75, 0, 0, 0.25, 1, 9, 5.1415, 0.25, 0.25, 1, 0, 0),
('0COVID-19 Coronavirus.csv', 0.88, 0.781778, 0.906667, 0.0257778, 0.0217778, 0.0213333, 10, 0.5, 0.1, 0, 0.4, 0, 1, 52, 6.88267, 0, 0, 1, 0, 0),
('0data_balita.csv', 0.253, 0.253, 1, 0.25, 0.25, 0.1305, 4, 0, 0.25, 0, 0.5, 0.25, 1, 16, 8.307, 0.25, 0.5, 1, 0, 0),
('0ETH-USD_data.csv', 1, 0.989, 0.990333, 0.000666667, 0.000666667, 0.000666667, 6, 0.166667, 0.666667, 0.166667, 0, 0, 6, 11, 10.4893, 0, 0, 1, 0, 0),
('0Fake02.csv', 0.308333, 0.292, 0.929667, 0.150333, 0.017, 0.01, 6, 0.5, 0, 0, 0.333333, 0.166667, 1, 20, 4.149, 0.166667, 0.166667, 1, 0, 0),
('0Fake04.csv', 0.165143, 0.154, 0.571429, 0.138286, 0.0891429, 0.0857143, 7, 0.142857, 0.714286, 0.142857, 0, 0, 1, 10, 6.45629, 0, 0, 1, 0, 0),
('0Fake04_1.csv', 0.19, 0.181, 0.530333, 0.104, 0.0866667, 0.075, 6, 0, 0, 0, 1, 0, 3, 20, 8.147, 0, 0, 0, 0, 0),
('0fakeNews.csv', 0.5615, 0.5615, 1, 0.25, 0.0045, 0.0045, 4, 0, 0, 0.25, 0.75, 0, 4, 6942, 642.601, 0, 0.25, 1, 0, 0),
('0field_of_study.csv', 0.264, 0.26, 0.9355, 0.048, 0.0445, 0.033, 4, 0.25, 0, 0, 0.75, 0, 3, 52, 14.5065, 0, 0, 1, 0, 0),
('0glass.data', 0.492353, 0.452421, 0.920986, 0.166525, 0.0331351, 0.031011, 11, 0.181818, 0.818182, 0, 0, 0, 1, 7, 3.82795, 0.0909091, 0, 0, 0, 0),
('0glass1.csv', 0.423832, 0.42243, 0.913551, 0.183178, 0.064486, 0.035514, 10, 0, 0.9, 0, 0.1, 0, 3, 10, 6.63692, 0, 0.1, 1, 0, 0),
('0global_education_data.csv', 0.477586, 0.25069, 0.607241, 0.362414, 0.0189655, 0.0165517, 29, 0.758621, 0.206897, 0, 0.034483, 0, 1, 32, 2.56448, 0, 0, 1, 0, 0),
('0name_gender_dataset.csv', 0.7495, 0.7495, 1, 0.135, 0.115, 0.001, 4, 0.25, 0.25, 0, 0.5, 0, 1, 11, 5.9295, 0.25, 0.25, 1, 0, 0),
('0new2.csv', 0.5175, 0.5, 0.808, 0.2885, 0.154, 0.0225, 4, 0.5, 0, 0, 0.25, 0.25, 1, 1440, 25.0905, 0.25, 0.25, 1, 0, 0),
('0NY-House-Dataset.csv', 0.468941, 0.465059, 0.972706, 0.0704706, 0.0387059, 0.0316471, 17, 0.117647, 0.235294, 0, 0.647059, 0, 1, 87, 15.2751, 0, 0, 1, 0, 0),
('0Raisin_Dataset.arff', 0.874722, 0.874306, 1, 0.0625, 0.0625, 0.000277778, 8, 0.25, 0.625, 0, 0.125, 0, 4, 11, 8.96278, 0, 0.125, 1, 0, 0),
('0RT_IOT2022', 0.342212, 0.229906, 0.6176, 0.187788, 0.0584706, 0.0325647, 85, 0.317647, 0.482353, 0, 0.035294, 0.164706, 1, 18, 6.95932, 0.141176, 0.376471, 1, 0, 0),
('0source_of_fund.csv', 0.1852, 0.1852, 1, 0.0896, 0.0884, 0.0576, 5, 0.2, 0, 0, 0.8, 0, 1, 32, 9.8392, 0, 0, 1, 0, 0),
('0status.csv', 1, 0.99375, 0.99375, 0.0125, 0.00625, 0.00625, 10, 0.9, 0, 0, 0.1, 0, 7, 9, 7.55625, 0, 0, 1, 0, 0),
('0targets.csv', 0.337333, 0.224444, 0.988222, 0.0308889, 0.0291111, 0.0271111, 9, 0.666667, 0, 0, 0.333333, 0, 1, 40, 6.89378, 0.111111, 0, 1, 0, 0),
('0top_chess_players.csv', 0.368, 0.368, 0.993, 0.2435, 0.0185, 0.017, 4, 0, 0, 0, 1, 0, 2, 31, 8.714, 0, 0.25, 1, 0, 0),
('0trueNews.csv', 0.516, 0.516, 1, 0.25, 0.0225, 0.0185, 4, 0, 0, 0.25, 0.75, 0, 12, 8181, 620.786, 0, 0.25, 1, 0, 0),
('0u.data', 0.5235, 0.4735, 0.9985, 0.086, 0.067, 0.0555, 4, 1, 0, 0, 0, 0, 1, 9, 3.885, 0.25, 0, 1, 0, 0),
('0wine.data', 0.513242, 0.32504, 0.99077, 0.032504, 0.0244783, 0.0244783, 14, 0.214286, 0.785714, 0, 0, 0, 1, 8, 3.5634, 0.0714286, 0, 0, 0, 0),
('0_Dry_Bean_Dataset.arff', 0.916223, 0.905137, 1, 0.015325, 0.0113922, 0.00876022, 17, 0.117647, 0.823529, 0, 0.058824, 0, 4, 21, 15.7182, 0, 0, 1, 0, 0),
('0_iris.data', 0.168, 0.102667, 1, 0.0666667, 0.0666667, 0.0666667, 5, 0, 0.8, 0, 0.2, 0, 3, 15, 5.06667, 0, 0, 0, 0, 0),
('2invoice.csv', 0.0965517, 0.096, 0.992828, 0.0344828, 0.033931, 0.0337931, 29, 0.103448, 0.103448, 0.103448, 0.689655, 0, 1, 60, 9.29, 0.0344828, 0.137931, 1, 2, 12),
('2OrderDetails.csv', 0.222, 0.222, 1, 0.116, 0.02225, 0.021, 8, 0.25, 0.125, 0.125, 0.5, 0, 1, 35, 9.59025, 0, 0, 1, 2, 4),
('2Sales.csv', 0.146348, 0.144435, 0.963739, 0.0415652, 0.0335652, 0.028, 23, 0.304348, 0.0869565, 0.0434783, 0.565217, 0, 1, 42, 7.02061, 0.0434783, 0, 1, 2, 7),
('2_L-0003_2019.csv', 0.157556, 0.150444, 0.997556, 0.106222, 0.0546667, 0.0362222, 9, 0.444444, 0.111111, 0.111111, 0.333333, 0, 3, 47, 11.7418, 0, 0, 1, 2, 1),
('2_L-0003_2021.csv', 0.220625, 0.191125, 0.94275, 0.059625, 0.030375, 0.02725, 16, 0.25, 0.5, 0.0625, 0.1875, 0, 3, 48, 8.70875, 0, 0, 1, 2, 1),
('2_L-0004_2021.csv', 0.281798, 0.236568, 0.857456, 0.125411, 0.0623629, 0.0153509, 16, 0.3125, 0.375, 0.0625, 0.25, 0, 3, 59, 7.8813, 0, 0.1875, 1, 2, 1),
('2_L-0005_2014.csv', 0.211429, 0.203143, 0.835857, 0.146143, 0.0685714, 0.0274286, 14, 0.428571, 0.285714, 0.0714286, 0.214286, 0, 3, 60, 9.72329, 0, 0.142857, 1, 2, 1),
('2_L-0005_2015.csv', 0.221571, 0.209, 0.823571, 0.145143, 0.0705714, 0.0245714, 14, 0.428571, 0.285714, 0.0714286, 0.214286, 0, 3, 60, 9.58614, 0, 0.142857, 1, 2, 1),
('2_L-0005_2019.csv', 0.204571, 0.194429, 0.77, 0.147714, 0.0687143, 0.0334286, 14, 0.428571, 0.285714, 0.0714286, 0.214286, 0, 3, 60, 9.601, 0, 0.142857, 1, 2, 1),
('2_L-0006.csv', 0.2335, 0.2015, 0.872125, 0.139875, 0.053125, 0.02475, 16, 0.375, 0.375, 0.0625, 0.1875, 0, 3, 99, 8.563, 0, 0, 1, 2, 1),
('2_L-0006_SRV2_2016.csv', 0.3215, 0.3215, 0.98875, 0.03225, 0.031, 0.02875, 8, 0.5, 0.125, 0.125, 0.25, 0, 3, 54, 11.1077, 0, 0, 1, 2, 1),
('2_L-0006_SRV2_2019.csv', 0.203, 0.203, 1, 0.0433333, 0.0413333, 0.034, 6, 0.5, 0, 0.166667, 0.333333, 0, 3, 41, 12.2733, 0, 0, 1, 2, 1),
('2_L-0006_SRV5_2013.csv', 0.330667, 0.330667, 1, 0.102, 0.03, 0.03, 6, 0.5, 0, 0.166667, 0.333333, 0, 3, 39, 12.3347, 0, 0, 1, 2, 1),
('2_L-0006_SRV6_2017.csv', 0.365111, 0.359111, 0.997333, 0.107333, 0.0197778, 0.0197778, 9, 0.444444, 0.222222, 0.111111, 0.222222, 0, 3, 38, 10.5191, 0, 0, 1, 2, 2),
('2_L-0008.csv', 0.21725, 0.21675, 1, 0.096, 0.05175, 0.02425, 8, 0.5, 0, 0.125, 0.375, 0, 4, 40, 10.435, 0, 0, 1, 2, 2),
('2_L-0010_2017.csv', 0.194375, 0.167125, 0.757625, 0.20125, 0.0255, 0.018625, 16, 0.3125, 0.375, 0.0625, 0.25, 0, 3, 42, 8.02825, 0, 0.125, 1, 2, 1),
('2_L-0010_2021.csv', 0.2525, 0.208625, 0.765125, 0.236875, 0.0305, 0.025875, 16, 0.1875, 0.5, 0.0625, 0.25, 0, 3, 47, 8.3885, 0, 0, 1, 2, 1),
('2_L-0011_2020.csv', 0.406545, 0.347818, 0.903818, 0.112182, 0.0909091, 0.0109091, 11, 0.181818, 0.454545, 0.0909091, 0.272727, 0, 3, 36, 8.01764, 0, 0.0909091, 1, 2, 1),
('2_L-0011_2022.csv', 0.4545, 0.441333, 0.987167, 0.0833333, 0.083, 0.014, 12, 0.333333, 0.333333, 0.0833333, 0.25, 0, 4, 44, 8.1295, 0, 0.166667, 1, 2, 1),
('2_L-0012_2017.csv', 0.267375, 0.211625, 0.850375, 0.1245, 0.0625, 0.02475, 16, 0.1875, 0.5, 0.0625, 0.25, 0, 4, 52, 8.902, 0, 0.0625, 1, 2, 1),
('2_L-0012_2023.csv', 0.26875, 0.21, 0.819, 0.125, 0.0625, 0.0225, 16, 0.3125, 0.375, 0.0625, 0.25, 0, 3, 60, 8.699, 0, 0.1875, 1, 2, 1),
('2_L-0023.csv', 0.2705, 0.21775, 0.88525, 0.098625, 0.0625, 0.022625, 16, 0.3125, 0.375, 0.0625, 0.25, 0, 4, 67, 8.47612, 0, 0.0625, 1, 2, 1),
('2_L-0023_2014.csv', 0.2192, 0.2184, 1, 0.2, 0.1384, 0.012, 5, 0.4, 0.2, 0, 0.4, 0, 4, 11, 6.3908, 0, 0.2, 1, 2, 1),
('2_L-0023_2017.csv', 0.299, 0.22825, 0.8635, 0.117875, 0.0625, 0.01925, 16, 0.3125, 0.375, 0.0625, 0.25, 0, 4, 61, 8.36375, 0, 0.0625, 1, 2, 1),
('2_L-0023_2020.csv', 0.266125, 0.210125, 0.866625, 0.121625, 0.058625, 0.013375, 16, 0.3125, 0.375, 0.0625, 0.25, 0, 4, 59, 8.38113, 0, 0.0625, 1, 2, 1),
('2_l-0031_2014.csv', 0.488, 0.488, 1, 0.081, 0.014, 0.012, 2, 1, 0, 0, 0, 0, 8, 10, 9, 0, 0, 1, 2, 2),
('2_l-0031_2017.csv', 0.349333, 0.349333, 0.994, 0.044, 0.0333333, 0.0333333, 3, 1, 0, 0, 0, 0, 3, 11, 9.75733, 0, 0, 1, 2, 1),
('2_l-0031_2020.csv', 0.3316, 0.3316, 1, 0.2, 0.0256, 0.0152, 5, 0.8, 0.2, 0, 0, 0, 4, 10, 7.3216, 0, 0.2, 1, 2, 1),
('2_l-0031_2023.csv', 0.37675, 0.303875, 0.869625, 0.121, 0.0625, 0.009125, 16, 0.1875, 0.5, 0.0625, 0.25, 0, 4, 39, 8.59163, 0, 0.125, 1, 2, 1),
('3a2.csv', 0.4, 0.08, 0.36, 0.6, 0.4, 0, 5, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 3, 0),
('3a2100.csv', 0.02, 0.004, 0.36, 0.6, 0.4, 0, 5, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 3, 0),
('3grocery_timestamp.csv', 0.0416479, 0.0275915, 0.0655211, 0.887634, 0.0452676, 0.0111831, 142, 0.697183, 0, 0.028169, 0, 0.274648, 1, 7, 1.21349, 0.929577, 0.28169, 1, 3, 4),
('3invoice.csv', 0.00220482, 0.0000240964, 0.0120482, 0.992831, 0.00716867, 0, 166, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 3, 0),
('3invoice01.csv', 0.00220482, 0.0000240964, 0.0120482, 0.992831, 0.00716867, 0, 166, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 3, 0),
('3OrderDetails.csv', 0.0034198, 0.000248588, 0.0007831, 0.994277, 0.00531319, 0.000143945, 4071, 0.0668141, 0, 0, 0, 0.933186, 1, 6, 1.00123, 0.999754, 0.936379, 1, 3, 1),
('3OrderDetails01.csv', 0.00304226, 0.000000982801, 0.0004914, 0.994521, 0.00547912, 0, 4070, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 3, 0),
('3Sales.csv', 0.00651466, 0.0000597675, 0.0183486, 0.915638, 0.0843618, 0, 109, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 3, 0),
('3Sales01.csv', 0.0155463, 0.00915013, 0.0272727, 0.907314, 0.0835949, 0.0000296121, 110, 0.00909091, 0, 0, 0.990909, 0, 1, 5, 1.03636, 0.990909, 0.990909, 1, 3, 1),
('3saleshourly.csv', 0.130889, 0.122222, 0.328222, 0.749111, 0.0711111, 0.024, 9, 0.333333, 0.555556, 0.111111, 0, 0, 1, 15, 3.58778, 0.222222, 0, 1, 3, 0),
('3supermarket.txt', 0.00307834, 0.0000368664, 0.0138249, 0.908673, 0.0867189, 0.00296774, 217, 0, 0, 0, 1, 0, 1, 4, 1.01086, 0.995392, 1, 1, 3, 1),
('3u.data', 0.00392152, 0.00000237812, 0.00118906, 0.932497, 0.067503, 0, 1682, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 3, 0),
('3u01.data', 0.0065098, 0.00259418, 0.00377897, 0.930212, 0.0671967, 0.00000118835, 1683, 0.998812, 0, 0, 0.000594, 0.000594177, 1, 7, 1.00575, 0.00534759, 0.040404, 0, 3, 0),
('3_L-0003_2019.csv', 0.00368504, 0.0000472441, 0.0161732, 0.974095, 0.0251181, 0.000787402, 127, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0.897638, 1, 3, 0),
('3_L-0003_2021.csv', 0.00331915, 0.0000425532, 0.0142695, 0.97861, 0.021305, 0.0000851064, 141, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0.978723, 1, 3, 0),
('3_L-0004_2021.csv', 0.0120486, 0.000108873, 0.0123027, 0.983705, 0.0160769, 0.000217746, 165, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0.987879, 1, 3, 0),
('3_L-0005_2014.csv', 0.00325532, 0.0000638298, 0.0212766, 0.983277, 0.0167021, 0.0000212766, 94, 0, 0, 0, 0.617021, 0.382979, 1, 1, 1, 1, 0.989362, 1, 3, 0),
('3_L-0005_2015.csv', 0.0033253, 0.0000722892, 0.0241205, 0.98147, 0.018506, 0.0000240964, 83, 0.0120482, 0, 0, 0, 0.987952, 1, 1, 1, 1, 0.987952, 1, 3, 0),
('3_L-0006_SRV2_2016.csv', 0.0026771, 0.00000782779, 0.00391389, 0.996536, 0.0034638, 0, 511, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 3, 0),
('3_L-0006_SRV5_2013.csv', 0.00289558, 0.00000803213, 0.00401606, 0.995422, 0.00457831, 0, 498, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 3, 0),
('3_L-0010_2017.csv', 0.004, 0.0000625, 0.03125, 0.975719, 0.0242813, 0, 64, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 3, 0),
('3_L-0010_2021.csv', 0.00984569, 0.00442936, 0.0132159, 0.98262, 0.0129751, 0.0000120363, 227, 0.00440529, 0, 0, 0, 0.995595, 1, 6, 1.02203, 0.995595, 0.995595, 1, 3, 0),
('3_L-0011_2022.csv', 0.00269618, 0.00000804829, 0.00402414, 0.996382, 0.00361771, 0, 497, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 3, 0),
('3_L-0012_2017.csv', 0.00245813, 0.00000328407, 0.00164204, 0.997864, 0.00213629, 0, 1218, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 3, 0),
('3_L-0012_2023.csv', 0.00381146, 0.00127898, 0.00382166, 0.996247, 0.00247898, 0.00000254777, 785, 0.00127389, 0, 0, 0, 0.998726, 1, 7, 1.00764, 0.998726, 0.998726, 1, 3, 0),
('3_L-0023_2014.csv', 0.00292146, 0.00000280505, 0.00140252, 0.995781, 0.00421879, 0, 1426, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 3, 0),
('3_L-0023_2014a.csv', 0.00292146, 0.00000280505, 0.00140252, 0.995781, 0.00421879, 0, 1426, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 3, 0),
('3_L-0023_2020.csv', 0.00340098, 0.000448815, 0.00134108, 0.995731, 0.00382208, 0.000000894055, 2237, 0.000447027, 0, 0, 0.999553, 0, 1, 7, 1.00268, 0.999553, 0.999553, 1, 3, 0),
('3_L-0031_2017.csv', 0.00372692, 0.000652796, 0.00195059, 0.997036, 0.00231339, 0.00000130039, 1538, 0.000650195, 0, 0, 0.99935, 0, 1, 7, 1.0039, 0.99935, 0.99935, 1, 3, 0),
('3_l-0031_2023.csv', 0.00282491, 0.00000470035, 0.000790443, 0.998589, 0.00138895, 0.0000141011, 2553, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0.992558, 1, 3, 0),
('4balance-scale.data', 0.0088, 0.0032, 0.7904, 0.17, 0.17, 0.17, 5, 0.8, 0, 0, 0.2, 0, 1, 1, 1, 1, 0, 1, 4, 0),
('4breast-cancer-dataset.csv', 0.129321, 0.0960307, 0.788732, 0.201878, 0.172429, 0.0512164, 11, 0.454545, 0, 0, 0.272727, 0.272727, 1, 12, 4.20017, 0.0909091, 0.545455, 1, 4, 0),
('4car.dat', 0.006, 0.00371429, 0.884571, 0.173714, 0.126286, 0.122286, 7, 0, 0, 0, 1, 0, 1, 5, 3.47657, 0, 0.285714, 1, 4, 0),
('4crx.data', 0.12275, 0.098625, 0.787625, 0.102375, 0.100125, 0.087375, 16, 0.1875, 0.1875, 0, 0.4375, 0.1875, 1, 6, 1.99413, 0.25, 0.3125, 1, 4, 0),
('4Dataset-Mental-Disorders.csv', 0.0820175, 0.0614035, 0.478509, 0.281579, 0.244298, 0.0741228, 19, 0, 0, 0, 0.526316, 0.473684, 2, 14, 5.51447, 0, 0.473684, 1, 4, 1),
('4decks_URM_train.csv', 0.083, 0.082, 0.980667, 0.176333, 0.176333, 0.147333, 6, 0.333333, 0, 0.166667, 0.166667, 0.333333, 1, 10, 5.044, 0, 0.5, 1, 4, 0),
('4Electric_Vehicle_Population_Data.csv', 0.216235, 0.213294, 0.975412, 0.0778823, 0.0585882, 0.0427059, 17, 0.411765, 0, 0, 0.588235, 0, 1, 85, 12.9622, 0, 0.0588235, 1, 4, 0),
('4heart.csv', 0.0942951, 0.0719, 0.56082, 0.302452, 0.22513, 0.105139, 14, 0.642857, 0.0714286, 0, 0, 0.285714, 1, 3, 1.6405, 0.642857, 0.285714, 1, 4, 0),
('4horse.csv', 0.142857, 0.118571, 0.688571, 0.0775, 0.0542857, 0.0528571, 28, 0.214286, 0.142857, 0, 0.5, 0.142857, 1, 13, 4.79429, 0.0357143, 0.214286, 1, 4, 0),
('4house-votes-84.data', 0.0045977, 0.000540906, 0.176335, 0.478567, 0.46261, 0.0361055, 17, 0, 0, 0, 0.058824, 0.941176, 1, 10, 1.4572, 0.941176, 1, 1, 4, 0),
('4housing_price_dataset.csv', 0.336, 0.328667, 0.971667, 0.0993333, 0.093, 0.059, 6, 0.666667, 0.166667, 0, 0.166667, 0, 1, 18, 5.45933, 0.333333, 0, 1, 4, 0),
('4imports-85.csv', 0.182609, 0.171156, 0.977094, 0.0579003, 0.042842, 0.0392365, 23, 0.347826, 0.217391, 0, 0.434783, 0, 1, 13, 3.97052, 0, 0.173913, 1, 4, 0),
('4kba_data.csv', 0.0324, 0.0322, 0.9832, 0.1126, 0.1, 0.0884, 10, 0.2, 0, 0.2, 0.6, 0, 3, 32, 7.467, 0, 0.2, 1, 4, 0),
('4loan_data.csv', 0.204926, 0.19786, 0.948718, 0.0965072, 0.0629921, 0.059358, 13, 0.230769, 0.0769231, 0, 0.384615, 0.307692, 1, 17, 4.31799, 0.0769231, 0.461538, 1, 4, 0),
('4mammographic.dat', 0.0293333, 0.0246667, 0.793333, 0.209333, 0.185, 0.166667, 6, 0.833333, 0, 0, 0, 0.166667, 1, 4, 2.83267, 0.166667, 0.166667, 1, 4, 0),
('4MobileClassification.csv', 0.199524, 0.14781, 0.700857, 0.194095, 0.157048, 0.0327619, 21, 0.619048, 0.0952381, 0, 0, 0.285714, 1, 4, 1.91771, 0.380952, 0.285714, 1, 4, 0),
('4nursery.data', 0.00533333, 0.00466667, 0.906, 0.111111, 0.111111, 0.0993333, 9, 0, 0, 0, 1, 0, 1, 13, 7.39978, 0, 0.333333, 1, 4, 0),
('4ObesityDataSet_raw_and_data_sinthetic.csv', 0.0269412, 0.0232941, 0.728471, 0.171765, 0.0869412, 0.0852941, 17, 0.176471, 0.294118, 0, 0.294118, 0.235294, 1, 21, 4.83494, 0.176471, 0.294118, 1, 4, 0),
('4student-por.csv', 0.0104848, 0.0029697, 0.572727, 0.126545, 0.115879, 0.0864242, 33, 0.484848, 0, 0, 0.272727, 0.242424, 1, 10, 2.19958, 0.424242, 0.393939, 1, 4, 0),
('4student_data.csv', 0.0421714, 0.0200571, 0.442343, 0.273714, 0.209829, 0.0595429, 35, 0.6, 0.142857, 0, 0.028571, 0.228571, 1, 18, 2.03989, 0.342857, 0.228571, 1, 4, 1),
('4Thyroid_Diff.csv', 0.0185839, 0.0175088, 0.801567, 0.248349, 0.056059, 0.0511442, 17, 0.0588235, 0, 0, 0.705882, 0.235294, 1, 27, 5.61266, 0.0588235, 0.411765, 1, 4, 0),
('4tic-tac-toe.data', 0.0056, 0.0008, 0.3876, 0.3984, 0.2984, 0.2032, 10, 0, 0, 0, 1, 0, 1, 8, 1.7, 0.9, 0.1, 1, 4, 0),
('4titanic02.csv', 0.004, 0.004, 1, 0.247, 0.174, 0.1625, 4, 0, 0, 0, 0.75, 0.25, 2, 6, 3.764, 0, 1, 1, 4, 0),
('4titanic02WithoutHeader.csv', 0.004, 0.004, 1, 0.247, 0.174, 0.1625, 4, 0, 0, 0, 0.75, 0.25, 2, 6, 3.764, 0, 1, 0, 4, 0),
('4train.csv', 0.328, 0.315571, 0.837286, 0.151571, 0.144571, 0.0442857, 14, 0.428571, 0.142857, 0, 0.214286, 0.214286, 1, 16, 4.16371, 0.142857, 0.285714, 1, 4, 2),
('4_adult_NoHead.csv', 0.0994667, 0.0930667, 0.936133, 0.1244, 0.0593333, 0.0554667, 15, 0.4, 0, 0, 0.6, 0, 1, 22, 6.7996, 0, 0.133333, 0, 4, 0),
('4_agaricus-lepiota.data', 0.00556522, 0.00191304, 0.581826, 0.163043, 0.112, 0.101565, 23, 0, 0, 0, 0.913043, 0.0869565, 1, 1, 1, 1, 0.521739, 1, 4, 0),
('4_breast-cancer.data', 0.015035, 0.0143357, 0.921329, 0.153846, 0.0744755, 0.0702797, 10, 0.1, 0, 0, 0.7, 0.2, 1, 20, 5.52867, 0.1, 0.4, 1, 4, 0),
('4_NH_agaricus-lepiota.data', 0.00556522, 0.00191304, 0.581826, 0.163043, 0.112, 0.101565, 23, 0, 0, 0, 0.913043, 0.0869565, 1, 1, 1, 1, 0.521739, 0, 4, 0),
('4_NH_german.data', 0.060381, 0.057619, 0.891619, 0.119048, 0.061619, 0.0455238, 21, 0.380952, 0, 0, 0.619048, 0, 1, 5, 2.79914, 0.238095, 0.190476, 0, 4, 0),
('4_ΝΗ_breast-cancer.data', 0.015035, 0.0143357, 0.921329, 0.153846, 0.0744755, 0.0702797, 10, 0.1, 0, 0, 0.7, 0.2, 1, 20, 5.52867, 0.1, 0.4, 0, 4, 0);

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `datasetwrongclassification`
--

CREATE TABLE `datasetwrongclassification` (
  `datasetName` varchar(100) NOT NULL,
  `realClass` int(11) NOT NULL,
  `predictedClass` int(11) NOT NULL,
  `instances` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Άδειασμα δεδομένων του πίνακα `datasetwrongclassification`
--

INSERT INTO `datasetwrongclassification` (`datasetName`, `realClass`, `predictedClass`, `instances`) VALUES
('0academic_detail.csv', 0, 4, 4),
('0All_Data_Aldi.csv', 0, 4, 97),
('0beer.csv', 0, 4, 3),
('0data_balita.csv', 0, 4, 38),
('0Fake02.csv', 0, 4, 7),
('0Fake04.csv', 0, 4, 82),
('0Fake04_1.csv', 0, 4, 28),
('0field_of_study.csv', 0, 4, 16),
('0new2.csv', 0, 4, 2),
('0RT_IOT2022', 0, 4, 61),
('0source_of_fund.csv', 0, 4, 203),
('0status.csv', 0, 2, 1),
('0targets.csv', 0, 4, 1),
('0_iris.data', 0, 4, 94),
('2invoice.csv', 2, 4, 85),
('2Sales.csv', 2, 4, 8),
('2u.data', 2, 0, 327),
('2u.data', 2, 4, 5),
('2_L-0023_2014.csv', 2, 0, 6),
('2_l-0031_2014.csv', 2, 0, 2),
('2_l-0031_2020.csv', 2, 0, 1),
('3a2.csv', 3, 4, 15),
('3a2100.csv', 3, 4, 21),
('3saleshourly.csv', 3, 0, 57),
('3saleshourly.csv', 3, 4, 69),
('4CarSales01.csv', 4, 0, 277),
('4chord-fingers.csv', 4, 0, 262),
('4Electric_Vehicle_Population_Data.csv', 4, 0, 147),
('4housing_price_dataset.csv', 4, 0, 269),
('4imports-85.csv', 4, 0, 49),
('4kba_data.csv', 4, 0, 1),
('4loan_data.csv', 4, 0, 17),
('4NY-House-Dataset.csv', 4, 0, 260),
('4train.csv', 4, 0, 4),
('4train.csv', 4, 2, 96),
('4zoo.data', 4, 3, 255);

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
-- Ευρετήρια για πίνακα `datasetwrongclassification`
--
ALTER TABLE `datasetwrongclassification`
  ADD PRIMARY KEY (`datasetName`,`realClass`,`predictedClass`);

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