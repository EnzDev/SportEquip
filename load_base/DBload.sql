-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 24, 2017 at 03:09 PM
-- Server version: 5.7.14
-- PHP Version: 5.6.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sportequip`
--

-- --------------------------------------------------------

--
-- Table structure for table `activite_eq`
--

CREATE TABLE `activite_eq` (
  `ComInsee` int(6) NOT NULL,
  `ComLib` varchar(30) NOT NULL,
  `EquipementId` int(10) NOT NULL,
  `ActCode` int(10) NOT NULL,
  `ActLib` varchar(50) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `equipement`
--

CREATE TABLE `equipement` (
  `ComInsee` int(6) NOT NULL,
  `InsNumeroInstall` int(12) NOT NULL,
  `InsNomInstall` varchar(25) NOT NULL,
  `EquipementId` int(10) NOT NULL,
  `EquNom` varchar(25) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `installation`
--

CREATE TABLE `installation` (
  `ComInsee` int(6) NOT NULL,
  `ComLib` int(30) NOT NULL,
  `InsNumeroInstall` int(12) NOT NULL,
  `Adress` text NOT NULL,
  `Latitude` decimal(10,0) NOT NULL,
  `Longitude` decimal(10,0) NOT NULL,
  `ComCode` int(6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
