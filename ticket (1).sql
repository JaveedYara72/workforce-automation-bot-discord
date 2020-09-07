-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 07, 2020 at 07:07 PM
-- Server version: 10.4.6-MariaDB
-- PHP Version: 7.3.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ticket`
--

-- --------------------------------------------------------

--
-- Table structure for table `career_at_koders`
--

CREATE TABLE `career_at_koders` (
  `Id` int(11) NOT NULL,
  `Name` varchar(100) NOT NULL DEFAULT 'NONE',
  `Address` varchar(100) NOT NULL DEFAULT 'NONE',
  `Gender` varchar(500) NOT NULL DEFAULT 'NONE',
  `DOB` varchar(500) NOT NULL DEFAULT 'NONE',
  `Joined_At` varchar(500) NOT NULL DEFAULT 'NONE',
  `Mail` varchar(500) NOT NULL DEFAULT 'NONE',
  `Phone` varchar(500) NOT NULL DEFAULT 'NONE',
  `Whatsapp` varchar(500) NOT NULL DEFAULT 'NONE'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `career_at_koders`
--

INSERT INTO `career_at_koders` (`Id`, `Name`, `Address`, `Gender`, `DOB`, `Joined_At`, `Mail`, `Phone`, `Whatsapp`) VALUES
(1, 'kanay', 'haldwani', 'Male', '1/2/1999', '2020-08-24 15:36:46.126000', 'kanay@mail.com', '9878786765', '9878786765'),
(2, 'akku', 'sikkim', 'Female', '12/1/1999', '2020-08-24 15:58:46.421000', 'akku@mail.com', '8978898767', '8978898767'),
(3, 'prerna', 'sikkim', 'Female', '1/2/1999', '2020-08-26 15:50:55.256000', 'prerna@gmail.com', '9878678767', '8798786798'),
(4, 'kush bhandari', 'haldwani', 'Male', '3/2/1999', '2020-08-26 17:32:05.566000', 'bhandarikanay2511@gmail.com', '8767879878', '7878679876');

-- --------------------------------------------------------

--
-- Table structure for table `client`
--

CREATE TABLE `client` (
  `Id` int(11) NOT NULL,
  `Name` varchar(100) NOT NULL DEFAULT 'NONE',
  `Address` varchar(100) NOT NULL DEFAULT 'NONE',
  `Gender` varchar(100) NOT NULL DEFAULT 'NONE',
  `DOB` varchar(500) NOT NULL DEFAULT 'NONE',
  `Discord_Username` varchar(500) NOT NULL DEFAULT 'NONE',
  `Mail` varchar(500) NOT NULL DEFAULT 'NONE',
  `Phone` varchar(500) NOT NULL DEFAULT 'NONE',
  `Whatsapp` varchar(500) NOT NULL DEFAULT 'NONE',
  `Notes` varchar(500) NOT NULL DEFAULT 'NONE'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `client`
--

INSERT INTO `client` (`Id`, `Name`, `Address`, `Gender`, `DOB`, `Discord_Username`, `Mail`, `Phone`, `Whatsapp`, `Notes`) VALUES
(1839, 'akshu', 'haldwani', 'Female', '8/2/1999', 'Kanay Bhandari', 'akshu@mail.com', '8978675676', '8767878935', 'this is a note'),
(1839, 'kanay', 'motahaldu', 'Male', '8/1/1898', 'Kanay Bhandari', 'kanay@mail.com', '8978678789', '7867898789', 'this is another one'),
(1839, 'kamalesh', 'jaipur', 'Male', '1/2/1999', 'Kanay Bhandari#1839', 'bhandarikanay2511@gmail.com', '8978678798', '8787678987', 'this is notes.'),
(1839, 'kapil', 'lalkuan', 'Male', '7/1/1999', 'Kanay Bhandari#1839', 'bhandarikanay2511@gmail.com', '8978678987', '7898568769', 'this is another.'),
(5594, 'Tets', 'Haldwani', 'Male', '12/12/2000', 'XHunter#5594', 'kartikmysterio@gmail.com', '9090909090', '9090909090', 'TEST'),
(1839, 'prerna', 'sikkim', 'Female', '1/2/1999', 'Kanay Bhandari#1839', 'prerna@gmail.com', '9878678987', '8927879878', 'this is a note'),
(1839, 'karan bhandari', 'haldwani', 'Male', '3/9/1999', 'Kanay Bhandari#1839', 'kan@mail.com', '8978678987', '8787987898', 'noote');

-- --------------------------------------------------------

--
-- Table structure for table `community`
--

CREATE TABLE `community` (
  `Id` int(11) NOT NULL,
  `Name` varchar(100) NOT NULL DEFAULT 'NONE',
  `Discord_Username` varchar(100) NOT NULL DEFAULT 'NONE',
  `Mail` varchar(100) NOT NULL DEFAULT 'NONE',
  `Phone` varchar(100) NOT NULL DEFAULT 'NONE',
  `Gender` varchar(100) NOT NULL DEFAULT 'NONE',
  `Joined_At` varchar(500) NOT NULL DEFAULT 'NONE'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `community`
--

INSERT INTO `community` (`Id`, `Name`, `Discord_Username`, `Mail`, `Phone`, `Gender`, `Joined_At`) VALUES
(1, 'anushka', 'Kanay Bhandari#1839', 'anush@gmail.com', '7857908978', 'Female', '2020-08-25 17:08:10.286000'),
(2, 'kanay', 'Kanay Bhandari#1839', 'kanay@gmail.com', '7898786789', 'Male', '2020-08-25 17:09:32.900000'),
(3, 'Kartikey', 'XHunter#5594', 'test@gmail.com', '7897897894', 'Male', '2020-08-25 18:35:46.258000'),
(4, 'prerna', 'Kanay Bhandari#1839', 'prerna@gmail.com', '7867987867', 'Female', '2020-08-26 15:51:41.307000'),
(5, 'kush bhandari', 'Kanay Bhandari#1839', 'bhandarikanay2511@gmai.com', '8978786787', 'Male', '2020-08-26 17:33:18.831000');

-- --------------------------------------------------------

--
-- Table structure for table `internal`
--

CREATE TABLE `internal` (
  `Internal_Id` int(11) NOT NULL,
  `Name` varchar(100) NOT NULL DEFAULT 'NONE',
  `Address` varchar(100) NOT NULL DEFAULT 'NONE',
  `DOB` varchar(500) NOT NULL DEFAULT 'NONE',
  `Gender` varchar(500) NOT NULL DEFAULT 'NONE',
  `Joined_At` varchar(500) NOT NULL DEFAULT 'NONE',
  `Mail` varchar(500) NOT NULL DEFAULT 'NONE',
  `Discord_Username` varchar(500) NOT NULL DEFAULT 'NONE',
  `Phone` varchar(500) NOT NULL DEFAULT 'NONE',
  `Whatsapp` varchar(500) NOT NULL DEFAULT 'NONE',
  `Type` varchar(500) NOT NULL DEFAULT 'NONE',
  `Is_Active` varchar(500) NOT NULL DEFAULT 'NONE',
  `Total_XP` int(11) NOT NULL,
  `Level` int(11) NOT NULL,
  `Notes` varchar(500) NOT NULL DEFAULT 'NONE'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `internal`
--

INSERT INTO `internal` (`Internal_Id`, `Name`, `Address`, `DOB`, `Gender`, `Joined_At`, `Mail`, `Discord_Username`, `Phone`, `Whatsapp`, `Type`, `Is_Active`, `Total_XP`, `Level`, `Notes`) VALUES
(1, 'kanay bhandari', 'haldwani', '8/1/1999', 'Male', '2020-08-31 13:27:17.034000', 'kanay@gmail.com', '<@!731484022823452702>', '9878987898', '7867987867', 'NONE', 'True', 1030, 5, 'notes');

-- --------------------------------------------------------

--
-- Table structure for table `partner`
--

CREATE TABLE `partner` (
  `Partner_Id` int(11) NOT NULL,
  `Name` varchar(100) NOT NULL DEFAULT 'NONE',
  `Discord_Username` varchar(100) NOT NULL DEFAULT 'NONE',
  `Address` varchar(100) NOT NULL DEFAULT 'NONE',
  `Mail` varchar(500) NOT NULL DEFAULT 'NONE',
  `Phone` varchar(500) NOT NULL DEFAULT 'NONE',
  `Gender` varchar(500) NOT NULL DEFAULT 'NONE',
  `Joined_At` varchar(500) NOT NULL DEFAULT 'NONE',
  `Reference` varchar(500) NOT NULL DEFAULT 'NONE',
  `Is_Active` varchar(500) NOT NULL DEFAULT 'NONE'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `partner`
--

INSERT INTO `partner` (`Partner_Id`, `Name`, `Discord_Username`, `Address`, `Mail`, `Phone`, `Gender`, `Joined_At`, `Reference`, `Is_Active`) VALUES
(1, 'lokesh', 'Kanay Bhandari#1839', 'bareilly', 'lokesh@gmail.com', '8978677867', 'Male', '2020-08-25 17:05:32.603000', 'TCS', 'True'),
(2, 'kanay', 'Kanay Bhandari#1839', 'halduchor', 'kanay@gmail.com', '7867897867', 'Male', '2020-08-25 17:07:11.179000', 'google', 'True'),
(3, 'kunal', 'Kanay Bhandari#1839', 'lalkuan', 'kunal@gmail.com', '8789878987', 'Male', '2020-08-26 07:06:49.005000', 'aiims', 'True'),
(4, 'himani', 'Kanay Bhandari#1839', 'halduchor', 'himani@gmail.com', '7867876789', 'Female', '2020-08-26 07:09:29.170000', 'TCSION', 'True'),
(5, 'anuj', 'Kanay Bhandari#1839', 'banaras', 'anuj@gmail.com', '7898678756', 'Male', '2020-08-26 07:26:14.692000', 'microsoft', 'True'),
(6, 'mandeep', 'Kanay Bhandari#1839', 'amritsar', 'mandeep@gmail.com', '7898786787', 'Male', '2020-08-26 07:28:51.916000', 'tcs', 'True'),
(7, 'ankit', 'Kanay Bhandari#1839', 'dehradun', 'ankit@gmail.com', '8978678987', 'Male', '2020-08-26 07:33:38.574000', 'tcs', 'True'),
(8, 'Test', 'XHunter#5594', 'Test', 'kartikmysterio@gmail.com', '7897897897', 'Male', '2020-08-26 07:37:41.106000', 'Test', 'True'),
(9, 'prerna', 'Kanay Bhandari#1839', 'sikkim', 'prerna@gmail.com', '8789876789', 'Female', '2020-08-26 15:49:15.473000', 'AIIMS', 'True'),
(10, 'kush bhandari', 'Kanay Bhandari#1839', 'haldwani', 'bhandarikanay2511@gmail.com', '8789878987', 'Male', '2020-08-26 17:30:33.030000', 'TCS', 'True'),
(11, 'akshada', 'Kanay Bhandari#1839', 'sikkim', 'akshu@gmail.com', '8978678987', 'Female', '2020-08-31 05:51:04.493000', 'CA', 'True'),
(12, 'prerna', 'Kanay Bhandari#1839', 'sikkim', 'prerna@gmail.com', '9878678987', 'Female', '2020-08-31 05:54:12.818000', 'AIIMS', 'True');

-- --------------------------------------------------------

--
-- Table structure for table `project`
--

CREATE TABLE `project` (
  `Id` int(11) NOT NULL,
  `Name` varchar(100) NOT NULL DEFAULT 'NONE',
  `Description` varchar(100) NOT NULL DEFAULT 'NONE',
  `Hand_In_Date` varchar(100) NOT NULL DEFAULT 'NONE',
  `Deadline` varchar(500) NOT NULL DEFAULT 'NONE',
  `Hand_Out_Date` varchar(500) NOT NULL DEFAULT 'NONE',
  `Client_Id` varchar(500) NOT NULL DEFAULT 'NONE',
  `Amount_Id` varchar(500) NOT NULL DEFAULT 'NONE',
  `Type` varchar(500) NOT NULL DEFAULT 'NONE',
  `Status` varchar(500) NOT NULL DEFAULT 'NONE',
  `Priority` varchar(500) NOT NULL DEFAULT 'NONE',
  `Estimated_Amount` varchar(500) NOT NULL DEFAULT 'NONE'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `project`
--

INSERT INTO `project` (`Id`, `Name`, `Description`, `Hand_In_Date`, `Deadline`, `Hand_Out_Date`, `Client_Id`, `Amount_Id`, `Type`, `Status`, `Priority`, `Estimated_Amount`) VALUES
(1, 'kanay', 'description', '2020-08-26', '8/2/2022', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '67000000'),
(2, 'akash', 'this is about discord bot', '2020-08-26', '8/1/2021', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '10 lakh'),
(3, 'discord bot', 'basic functionalities', '2020-08-26', '1/2/1999', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '600000'),
(4, 'kush bhandari', 'this is about games', '2020-08-26', '1/1/1999', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '7 lakh'),
(5, 'bot', 'hda', '2020-09-03', '2/1/2021', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '7lakh'),
(6, 'hsad', 'this is demo', '2020-09-03', '3/2/2022', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '8 lakh'),
(7, 'server', 'creation of server', '2020-09-03', '3/2/2022', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '7 lask'),
(8, 'cypher', 'bot', '2020-09-03', '8/1/2021', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '1 lakh'),
(9, 'pro evalu', 'has', '2020-09-03', '7/1/1999', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '7 lakh'),
(10, 'pom', 'main', '2020-09-03', '8/1/2212', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '2 lakh'),
(11, 'game', 'online game', '2020-09-03', '7/7/2021', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '4 lakhs'),
(12, 'alpha', 'hdjsa', '2020-09-03', '7/1/2021', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '3lakh'),
(13, 'kode', 'das', '2020-09-03', '9/1/2021', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '30 thousand'),
(14, 'dkjas', 'das', '2020-09-03', '8/2/2021', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '6 lakh'),
(15, 'prince of persia', 'game', '2020-09-04', '6/4/2021', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '2 lakh'),
(16, 'cod', 'game', '2020-09-04', '7/3/2021', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '1 lakh'),
(17, 'game', 'cod', '2020-09-04', '7/3/2021', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '7 lakj'),
(18, 'game', 'cod', '2020-09-04', '6/8/2021', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '4 lakh'),
(19, 'dajs', 'dasd', '2020-09-04', '7/12/2020', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '7 laks'),
(20, 'task 5', 'hsd', '2020-09-04', '8/3/2022', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '4 hudred'),
(21, 'anlds', 'dld', '2020-09-04', '7/9/2021', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '2 thousand'),
(22, 'houdajs', 'bjkadn', '2020-09-04', '9/9/2021', 'NONE', '1839', 'NONE', 'NONE', 'On Hold', 'High', '6 thousand');

-- --------------------------------------------------------

--
-- Table structure for table `suggestion`
--

CREATE TABLE `suggestion` (
  `author` varchar(100) NOT NULL DEFAULT 'NONE',
  `number` int(11) NOT NULL,
  `title` varchar(100) NOT NULL DEFAULT 'NONE',
  `description` varchar(500) NOT NULL DEFAULT 'NONE',
  `reason` varchar(500) NOT NULL DEFAULT 'NONE',
  `is_considered` int(11) NOT NULL DEFAULT 0,
  `considered_by` varchar(100) NOT NULL DEFAULT 'NONE'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `suggestion`
--

INSERT INTO `suggestion` (`author`, `number`, `title`, `description`, `reason`, `is_considered`, `considered_by`) VALUES
('Kanay Bhandari', 1, 'games', 'good for health', 'improves health', 1, 'Kanay Bhandari'),
('Kanay Bhandari', 2, 'train', 'good for travel', 'train fair is less', 1, 'Kanay Bhandari'),
('Kanay Bhandari', 3, 'plain', 'very fast', 'cost is very high', 2, 'Kanay Bhandari'),
('Kanay Bhandari', 4, 'ticket system', 'nice', 'good', 1, 'Kanay Bhandari'),
('Kanay Bhandari', 5, 'bus', 'bus for travel', 'very costly', 2, 'Kanay Bhandari'),
('Kanay Bhandari', 6, 'quiz', 'mental abiltiy', 'improves mental ability', 1, 'Kanay Bhandari'),
('Kanay Bhandari', 7, 'registration', 'good', 'nice', 1, 'Kanay Bhandari');

-- --------------------------------------------------------

--
-- Table structure for table `task`
--

CREATE TABLE `task` (
  `Id` int(11) NOT NULL,
  `Title` varchar(100) NOT NULL DEFAULT 'NONE',
  `Description` varchar(100) NOT NULL DEFAULT 'NONE',
  `Assigned_To` varchar(100) NOT NULL DEFAULT 'NONE',
  `Assigned_By` varchar(500) NOT NULL DEFAULT 'NONE',
  `Status` varchar(500) NOT NULL DEFAULT 'NONE',
  `Estimated_Time` varchar(500) NOT NULL DEFAULT 'NONE',
  `Time_Taken` varchar(500) NOT NULL DEFAULT 'NONE',
  `Estimated_XP` int(11) NOT NULL,
  `Given_XP` int(11) NOT NULL,
  `Project_Id` varchar(500) NOT NULL DEFAULT 'NONE'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `task`
--

INSERT INTO `task` (`Id`, `Title`, `Description`, `Assigned_To`, `Assigned_By`, `Status`, `Estimated_Time`, `Time_Taken`, `Estimated_XP`, `Given_XP`, `Project_Id`) VALUES
(1, 'abc', 'creation', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'Completed', '1hrs', '1hrs', 20, 20, '4'),
(2, 'task1', 'abc', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'Completed', '4hrs', '3hrs', 40, 40, '3'),
(3, 'task2', 'desc', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'completed', '6hrs', '7hrs', 50, 40, '6'),
(4, 'task3', 'abc', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'completed', '7hrs', '6hrs', 100, 100, '7'),
(5, 'task4', 'casad', '<@!731484022823452702>', 'Kanay Bhandari#1839', '1', '4hrs', '4hrs', 100, 100, '7'),
(6, 'task5', 'njads', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'Completed', '7hrs', '5hrs', 200, 200, '7'),
(7, 'task 6', 'this is description', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'Accepted', '4hrs', '3hrs', 50, 50, '6'),
(8, 'task 7', 'abc', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'Accepted', '7hrs', '6hrs', 100, 100, '8'),
(9, 'task 8', 'abcde', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'Accepted', '3hrs', '3hrs', 50, 50, '8'),
(10, 'task 10', 'abc description', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'Accepted', '8hrs', '5hrs', 200, 200, '7'),
(11, 'task 11', 'abc', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'In_Progress', '4hrs', 'NONE', 50, 0, '9'),
(12, 'task 15', 'abls', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'In_Progress', '6hrs', 'NONE', 60, 0, '8'),
(13, 'task 100', 'ansd', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'In_Progress', '5hrs', 'NONE', 60, 0, '8'),
(14, 'task 20', 'abc', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'In_Progress', '4', 'NONE', 50, 0, '3'),
(15, 'task 21', 'dsaln', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'In_Progress', '3hrs', 'NONE', 70, 0, '2'),
(16, 'task 32', 'sdlnas', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'In_Progress', '5hrs', 'NONE', 76, 0, '7'),
(17, 'task 11a', 'osadljn', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'In_Progress', '4min', 'NONE', 60, 0, '7'),
(18, 'task 6', 'alsjbd', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'In_Progress', '6hrs', 'NONE', 70, 0, '6'),
(19, 'tasl4', 'samknd', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'In_Progress', '7hrs', 'NONE', 80, 0, '8'),
(20, 'task 5', 'jads', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'In_Progress', '1', 'NONE', 80, 0, '7'),
(21, 'task 5', 'jndas', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'Accepted', '2', '1', 70, 70, '8'),
(22, 'server creation', 'test desc', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'In_Progress', '2', 'NONE', 60, 0, '3'),
(23, 'task9', 'dasnl', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'Accepted', '2', '1', 60, 60, '7'),
(24, 'task 01', 'creating games', '<@!731484022823452702>', 'Kanay Bhandari#1839', 'In_Progress', '5', 'NONE', 60, 0, '7');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `career_at_koders`
--
ALTER TABLE `career_at_koders`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `community`
--
ALTER TABLE `community`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `internal`
--
ALTER TABLE `internal`
  ADD PRIMARY KEY (`Internal_Id`);

--
-- Indexes for table `partner`
--
ALTER TABLE `partner`
  ADD PRIMARY KEY (`Partner_Id`);

--
-- Indexes for table `project`
--
ALTER TABLE `project`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `suggestion`
--
ALTER TABLE `suggestion`
  ADD PRIMARY KEY (`number`);

--
-- Indexes for table `task`
--
ALTER TABLE `task`
  ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `career_at_koders`
--
ALTER TABLE `career_at_koders`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `community`
--
ALTER TABLE `community`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `internal`
--
ALTER TABLE `internal`
  MODIFY `Internal_Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `partner`
--
ALTER TABLE `partner`
  MODIFY `Partner_Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `project`
--
ALTER TABLE `project`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `suggestion`
--
ALTER TABLE `suggestion`
  MODIFY `number` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `task`
--
ALTER TABLE `task`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
