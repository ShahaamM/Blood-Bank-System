-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 07, 2023 at 06:23 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bloodbank`
--

-- --------------------------------------------------------

--
-- Table structure for table `adminprofile`
--

CREATE TABLE `adminprofile` (
  `username` varchar(50) NOT NULL,
  `password` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `adminprofile`
--

INSERT INTO `adminprofile` (`username`, `password`) VALUES
('admin', 'jello'),
('root', 'yellow');

-- --------------------------------------------------------

--
-- Table structure for table `donationhistory`
--

CREATE TABLE `donationhistory` (
  `donationno` int(11) NOT NULL,
  `donorusername` varchar(50) DEFAULT NULL,
  `datedonated` date DEFAULT NULL,
  `donatedatcity` varchar(50) DEFAULT NULL,
  `bloodgroupdonated` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `donationhistory`
--

INSERT INTO `donationhistory` (`donationno`, `donorusername`, `datedonated`, `donatedatcity`, `bloodgroupdonated`) VALUES
(83, 'patriot', '2023-02-02', 'bangalore', 'O-'),
(84, 'patriot', '2022-11-03', 'hyderabad', 'O-'),
(85, 'mindhack', '2023-01-04', 'hyderabad', 'B+'),
(86, 'mindhack', '2022-05-06', 'mumbai', 'B+'),
(87, 'angel', '2022-07-08', 'mumbai', 'B-'),
(88, 'krazy', '2022-12-03', 'bangalore', 'AB-'),
(89, 'krazy', '2022-08-05', 'hyderabad', 'AB-'),
(93, 'max123', '2023-01-06', 'mumbai', 'A+'),
(94, 'angel', '2023-01-05', 'hyderabad', 'B-');

-- --------------------------------------------------------

--
-- Table structure for table `donordirectory`
--

CREATE TABLE `donordirectory` (
  `username` varchar(50) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `phoneno` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `bloodgroup` varchar(10) DEFAULT NULL,
  `healthissues` varchar(100) DEFAULT NULL,
  `lastdonateddate` date DEFAULT NULL,
  `availability` varchar(20) DEFAULT 'Available'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `donordirectory`
--

INSERT INTO `donordirectory` (`username`, `name`, `gender`, `phoneno`, `email`, `dob`, `city`, `bloodgroup`, `healthissues`, `lastdonateddate`, `availability`) VALUES
('angel', 'abel', 'M', '76543', 'angel@example.com', '1999-07-05', 'chennai', 'B-', 'asthma', '2023-01-05', 'Available'),
('binary', 'grace', 'F', '98345', 'binary@example.com', '1989-06-04', 'hyderabad', 'B+', NULL, NULL, 'Available'),
('divinity', 'mia', 'F', '76478', 'divinity@pretty.com', '2002-05-04', 'bangalore', 'A+', NULL, NULL, 'Not Available'),
('krazy', 'sweetie', 'F', '88976', 'krazy@pretty.com', '1990-12-12', 'mumbai', 'AB-', NULL, '2022-12-03', 'Available'),
('max123', 'greg', 'M', '9842156', 'max@yahoo.com', '1988-04-03', 'mumbai', 'A+', 'bp', '2023-01-06', 'Available'),
('mindhack', 'isabella', 'F', '77777', 'mindhack@pretty.com', '2001-05-04', 'chennai', 'B+', NULL, '2023-01-04', 'Available'),
('patriot', 'noah', 'M', '6667', 'patriot@pretty.com', '1988-08-09', 'hyderabad', 'O-', NULL, '2023-02-02', 'Available');

-- --------------------------------------------------------

--
-- Table structure for table `patientregister`
--

CREATE TABLE `patientregister` (
  `patientid` int(11) NOT NULL,
  `patientname` varchar(50) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `phno` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `bloodgroup` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `patientregister`
--

INSERT INTO `patientregister` (`patientid`, `patientname`, `gender`, `dob`, `phno`, `email`, `city`, `bloodgroup`) VALUES
(14, 'jenny', 'F', '1982-07-05', '893944', 'jen@yahoo.com', 'hyderabad', 'B+'),
(15, 'arnold', 'M', '1977-03-02', '738484', 'arnold@yahoo.com', 'chennai', 'B+'),
(16, 'tom', 'M', '1976-06-03', '83484', 'cruise@yahoo.com', 'bangalore', 'A+'),
(18, 'lovy', 'F', '1985-09-08', '7777777', 'lovylovy@yahoo.com', 'chennai', 'A+'),
(19, 'danielle', 'F', '1955-07-05', '89777', 'dan@yahoo.com', 'hyderabad', 'O-');

-- --------------------------------------------------------

--
-- Table structure for table `userprofile`
--

CREATE TABLE `userprofile` (
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `dob` date NOT NULL,
  `regdate` date DEFAULT curdate()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `userprofile`
--

INSERT INTO `userprofile` (`username`, `email`, `password`, `dob`, `regdate`) VALUES
('angel', 'angel@example.com', 'egotrip', '1999-07-05', '2023-02-15'),
('binary', 'binary@example.com', 'fiddle', '1989-06-04', '2023-02-15'),
('divinity', 'divinity@pretty.com', 'armor', '2002-05-04', '2023-02-15'),
('krazy', 'krazy@pretty.com', 'wagon', '1990-12-12', '2023-02-15'),
('max123', 'max@yahoo.com', 'craig', '1988-04-03', '2023-02-27'),
('mindhack', 'mindhack@pretty.com', 'sugar', '2001-05-04', '2023-02-15'),
('patriot', 'patriot@pretty.com', 'throne', '1988-08-09', '2023-02-15');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `adminprofile`
--
ALTER TABLE `adminprofile`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `donationhistory`
--
ALTER TABLE `donationhistory`
  ADD PRIMARY KEY (`donationno`),
  ADD KEY `fk_uname` (`donorusername`);

--
-- Indexes for table `donordirectory`
--
ALTER TABLE `donordirectory`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `patientregister`
--
ALTER TABLE `patientregister`
  ADD PRIMARY KEY (`patientid`);

--
-- Indexes for table `userprofile`
--
ALTER TABLE `userprofile`
  ADD PRIMARY KEY (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `donationhistory`
--
ALTER TABLE `donationhistory`
  MODIFY `donationno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=95;

--
-- AUTO_INCREMENT for table `patientregister`
--
ALTER TABLE `patientregister`
  MODIFY `patientid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `donationhistory`
--
ALTER TABLE `donationhistory`
  ADD CONSTRAINT `fk_uname` FOREIGN KEY (`donorusername`) REFERENCES `donordirectory` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `donordirectory`
--
ALTER TABLE `donordirectory`
  ADD CONSTRAINT `fk_usrname` FOREIGN KEY (`username`) REFERENCES `userprofile` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
