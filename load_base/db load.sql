-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Client :  127.0.0.1
-- Généré le :  Mar 04 Avril 2017 à 04:58
-- Version du serveur :  10.1.16-MariaDB
-- Version de PHP :  7.0.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `sportequip`
--

-- --------------------------------------------------------

--
-- Structure de la table `activite`
--

CREATE TABLE `activite` (
  `ComInsee` int(6) NOT NULL,
  `ComLib` text NOT NULL,
  `EquipementId` int(10) NOT NULL,
  `ActCode` int(10) NOT NULL,
  `ActLib` text NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `commune`
--

CREATE TABLE `commune` (
  `ComInsee` int(5) NOT NULL,
  `ComLib` text NOT NULL,
  `ComCode` int(5) NOT NULL,
  `EquGpsY` decimal(10,0) NOT NULL,
  `EquGpsX` decimal(10,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `equipement`
--

CREATE TABLE `equipement` (
  `ComInsee` int(6) NOT NULL,
  `InsNomInstall` text NOT NULL,
  `EquipementId` int(10) NOT NULL,
  `EquNom` text NOT NULL,
  `InsNumeroInstall` int(10) NOT NULL,
  `EquGpsY` decimal(15,10) NOT NULL,
  `EquGpsX` decimal(15,10) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `installation`
--

CREATE TABLE `installation` (
  `ComInsee` int(6) NOT NULL,
  `ComLib` text NOT NULL,
  `InsNumeroInstall` int(12) NOT NULL,
  `Adresse` text NOT NULL,
  `Latitude` decimal(15,10) NOT NULL,
  `Longitude` decimal(15,10) NOT NULL,
  `ComCode` int(6) NOT NULL,
  `NomInstall` text NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
