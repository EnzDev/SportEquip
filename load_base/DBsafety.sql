-- --------------------------------------------------------

--
-- Table structure for table `activite`
--

CREATE TABLE IF NOT EXISTS `activite` (
  `ActCode` varchar(10) NOT NULL,
  `ActLib` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `acti_equi`
--

CREATE TABLE IF NOT EXISTS `acti_equi` (
  `ActCode` varchar(10) NOT NULL,
  `EquipementId` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `commune`
--

CREATE TABLE IF NOT EXISTS `commune` (
  `ComInsee` varchar(5) NOT NULL,
  `ComLib` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `equipement`
--

CREATE TABLE IF NOT EXISTS `equipement` (
  `EquipementId` varchar(10) NOT NULL,
  `EquNom` varchar(40) NOT NULL,
  `InsNumeroInstall` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `installations`
--

CREATE TABLE IF NOT EXISTS `installations` (
  `InsNumeroInstall` int(10) NOT NULL,
  `Latitude`  DECIMAL(10,10) NOT NULL,
  `Longitude` DECIMAL(10,10) NOT NULL,
  `InsCodePostal` int(10) NOT NULL,
  `Nom` varchar(20) NOT NULL,
  `InsLibelleVoie` varchar(20) NOT NULL,
  `ComLib` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;