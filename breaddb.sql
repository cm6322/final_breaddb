-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 23, 2023 at 02:36 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `breaddb`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `DeleteUserWithRollsData` (IN `user_id_param` INT)   BEGIN
    -- Get rolls data for the user
    SELECT * FROM rolls WHERE user_id = user_id_param;

    -- If you need to perform actions or capture rolls data, you can do it here
    
    -- Delete rolls data associated with the user
    DELETE FROM rolls WHERE user_id = user_id_param;

    -- Delete the user
    DELETE FROM users WHERE id = user_id_param;
    
    -- Optionally, you might want to COMMIT the changes here if you're in a transaction

    -- Output a success message or any specific response as needed
    SELECT 'User and associated rolls data deleted successfully' AS Message;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Stand-in structure for view `getallrollsdata`
-- (See below for the actual view)
--
CREATE TABLE `getallrollsdata` (
`roll_id` int(11)
,`user_id` int(10) unsigned
,`tix_10` int(11)
,`tix_1` int(11)
,`gems` int(11)
,`total` decimal(10,2)
);

-- --------------------------------------------------------

--
-- Table structure for table `rolls`
--

CREATE TABLE `rolls` (
  `roll_id` int(11) NOT NULL,
  `user_id` int(10) UNSIGNED DEFAULT NULL,
  `tix_10` int(11) DEFAULT 0,
  `tix_1` int(11) DEFAULT 0,
  `gems` int(11) DEFAULT 0,
  `total` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rolls`
--

INSERT INTO `rolls` (`roll_id`, `user_id`, `tix_10`, `tix_1`, `gems`, `total`) VALUES
(15, 1, 2, 2, 234, '23.95'),
(21, 8, 2, 3, 4, '23.03');

--
-- Triggers `rolls`
--
DELIMITER $$
CREATE TRIGGER `calculate_total_insert` BEFORE INSERT ON `rolls` FOR EACH ROW BEGIN
    SET NEW.total = (NEW.tix_10 * 10) + NEW.tix_1 + (NEW.gems / 120);
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `calculate_total_update` BEFORE UPDATE ON `rolls` FOR EACH ROW BEGIN
    SET NEW.total = (NEW.tix_10 * 10) + NEW.tix_1 + (NEW.gems / 120);
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(10) UNSIGNED NOT NULL,
  `username` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`) VALUES
(1, 'admin', '123'),
(7, 'admin2', '123'),
(8, 'user1', '123');

-- --------------------------------------------------------

--
-- Structure for view `getallrollsdata`
--
DROP TABLE IF EXISTS `getallrollsdata`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `getallrollsdata`  AS SELECT `rolls`.`roll_id` AS `roll_id`, `rolls`.`user_id` AS `user_id`, `rolls`.`tix_10` AS `tix_10`, `rolls`.`tix_1` AS `tix_1`, `rolls`.`gems` AS `gems`, `rolls`.`total` AS `total` FROM `rolls` WHERE `rolls`.`user_id` <> 11  ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `rolls`
--
ALTER TABLE `rolls`
  ADD PRIMARY KEY (`roll_id`),
  ADD KEY `fk_user_id_new` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `rolls`
--
ALTER TABLE `rolls`
  MODIFY `roll_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `rolls`
--
ALTER TABLE `rolls`
  ADD CONSTRAINT `fk_user_id_new` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
