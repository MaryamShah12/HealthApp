-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 07, 2025 at 07:19 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `healthapp`
--

-- --------------------------------------------------------

--
-- Table structure for table `exercise`
--

CREATE TABLE `exercise` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `activity` varchar(100) NOT NULL,
  `duration_mins` int(11) NOT NULL,
  `calories_b` int(11) NOT NULL,
  `timestamp` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `exercise`
--

INSERT INTO `exercise` (`id`, `user_id`, `activity`, `duration_mins`, `calories_b`, `timestamp`) VALUES
(1, 6, 'Jogging', 25, 200, '2025-06-19 16:00:00'),
(2, 6, 'Pilates', 30, 150, '2025-06-20 15:00:00'),
(3, 6, 'Hiking', 60, 400, '2025-06-21 14:00:00'),
(4, 6, 'Rowing', 40, 300, '2025-06-22 17:00:00'),
(5, 6, 'Bodyweight Training', 45, 250, '2025-06-23 18:30:00'),
(6, 6, 'Jogging', 30, 220, '2025-06-24 15:30:00'),
(7, 6, 'Pilates', 35, 180, '2025-06-25 16:00:00'),
(8, 6, 'Hiking', 55, 380, '2025-06-26 13:00:00'),
(9, 6, 'Rowing', 45, 320, '2025-06-27 17:30:00'),
(10, 6, 'Bodyweight Training', 50, 280, '2025-06-28 18:00:00'),
(11, 6, 'Jogging', 35, 250, '2025-06-29 16:15:00'),
(12, 6, 'Pilates', 40, 200, '2025-06-30 15:00:00'),
(13, 6, 'Hiking', 50, 360, '2025-07-01 14:30:00'),
(14, 6, 'Rowing', 35, 280, '2025-07-02 17:00:00'),
(15, 6, 'Bodyweight Training', 55, 300, '2025-07-03 18:30:00'),
(16, 7, 'Running', 45, 400, '2025-06-22 16:00:00'),
(17, 7, 'Cycling', 50, 450, '2025-06-23 15:30:00'),
(18, 7, 'Swimming', 40, 350, '2025-06-24 17:00:00'),
(19, 7, 'Weightlifting', 60, 500, '2025-06-25 18:15:00'),
(20, 7, 'Jogging', 55, 420, '2025-06-26 16:30:00'),
(21, 7, 'HIIT', 45, 400, '2025-06-27 17:45:00'),
(22, 7, 'Running', 50, 430, '2025-06-28 15:00:00'),
(23, 7, 'Cycling', 55, 470, '2025-06-29 16:15:00'),
(24, 7, 'Swimming', 40, 360, '2025-06-30 17:30:00'),
(25, 7, 'Weightlifting', 65, 520, '2025-07-01 18:00:00'),
(26, 7, 'Jogging', 50, 410, '2025-07-02 16:00:00'),
(27, 7, 'HIIT', 45, 390, '2025-07-03 17:15:00'),
(28, 7, 'Running', 55, 440, '2025-07-04 14:00:00'),
(29, 5, 'Walking', 20, 100, '2025-06-25 15:00:00'),
(30, 5, 'Stretching', 15, 50, '2025-06-26 14:30:00'),
(31, 5, 'None', 0, 0, '2025-06-27 00:00:00'),
(32, 5, 'Light Jog', 25, 120, '2025-06-28 16:00:00'),
(33, 5, 'None', 0, 0, '2025-06-29 00:00:00'),
(34, 5, 'Stretching', 20, 70, '2025-06-30 15:15:00'),
(35, 5, 'Walking', 30, 150, '2025-07-01 14:00:00'),
(36, 5, 'None', 0, 0, '2025-07-02 00:00:00'),
(37, 5, 'Light Jog', 20, 90, '2025-07-03 15:30:00'),
(38, 5, 'None', 0, 0, '2025-07-04 00:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `meals`
--

CREATE TABLE `meals` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `food_name` varchar(100) NOT NULL,
  `calories` int(11) NOT NULL,
  `carbs` decimal(5,2) DEFAULT NULL,
  `protein` decimal(5,2) DEFAULT NULL,
  `fat` decimal(5,2) DEFAULT NULL,
  `timestamp` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `meals`
--

INSERT INTO `meals` (`id`, `user_id`, `food_name`, `calories`, `carbs`, `protein`, `fat`, `timestamp`) VALUES
(1, 6, 'Scrambled Eggs', 280, 2.00, 18.00, 20.00, '2025-06-19 07:30:00'),
(2, 6, 'Vegetarian Pizza', 700, 90.00, 25.00, 25.00, '2025-06-20 19:00:00'),
(3, 6, 'Quinoa Salad', 350, 50.00, 12.00, 10.00, '2025-06-21 12:30:00'),
(4, 6, 'Sushi Roll', 450, 60.00, 15.00, 15.00, '2025-06-22 18:45:00'),
(5, 6, 'Lentil Soup', 300, 40.00, 15.00, 5.00, '2025-06-23 13:00:00'),
(6, 6, 'Avocado Toast', 250, 30.00, 5.00, 15.00, '2025-06-24 08:15:00'),
(7, 6, 'Lamb Kebab', 600, 20.00, 40.00, 40.00, '2025-06-25 18:30:00'),
(8, 6, 'Mushroom Risotto', 400, 55.00, 10.00, 15.00, '2025-06-26 19:15:00'),
(9, 6, 'Chicken Salad', 320, 10.00, 25.00, 15.00, '2025-06-27 12:00:00'),
(10, 6, 'Noodle Soup', 500, 70.00, 15.00, 10.00, '2025-06-28 17:30:00'),
(11, 6, 'Tofu Stir-fry', 350, 40.00, 20.00, 10.00, '2025-06-29 13:45:00'),
(12, 6, 'Cheese Burger', 650, 40.00, 30.00, 40.00, '2025-06-30 18:00:00'),
(13, 6, 'Spinach Wrap', 400, 50.00, 15.00, 10.00, '2025-07-01 12:30:00'),
(14, 6, 'Yogurt Parfait', 220, 35.00, 8.00, 5.00, '2025-07-02 09:30:00'),
(15, 6, 'Shrimp Pasta', 550, 60.00, 25.00, 20.00, '2025-07-03 19:00:00'),
(16, 7, 'Plain Toast', 150, 25.00, 5.00, 3.00, '2025-06-22 07:45:00'),
(17, 7, 'Vegetable Soup', 200, 30.00, 6.00, 4.00, '2025-06-23 12:30:00'),
(18, 7, 'Chicken Nuggets', 300, 20.00, 15.00, 15.00, '2025-06-24 18:00:00'),
(19, 7, 'Rice Porridge', 180, 35.00, 4.00, 2.00, '2025-06-25 13:15:00'),
(20, 7, 'Grilled Veggies', 220, 25.00, 5.00, 10.00, '2025-06-26 12:00:00'),
(21, 7, 'Egg Salad', 250, 10.00, 12.00, 18.00, '2025-06-27 17:30:00'),
(22, 7, 'Boiled Potato', 150, 30.00, 3.00, 1.00, '2025-06-28 11:45:00'),
(23, 7, 'Tuna Sandwich', 280, 30.00, 15.00, 10.00, '2025-06-29 13:00:00'),
(24, 7, 'Oatmeal', 200, 35.00, 6.00, 3.00, '2025-06-30 08:30:00'),
(25, 7, 'Cucumber Salad', 120, 15.00, 2.00, 5.00, '2025-07-01 12:15:00'),
(26, 7, 'Fish Fillet', 250, 5.00, 20.00, 15.00, '2025-07-02 18:00:00'),
(27, 7, 'Plain Rice', 180, 40.00, 4.00, 1.00, '2025-07-03 13:30:00'),
(28, 7, 'Fruit Cup', 150, 35.00, 2.00, 1.00, '2025-07-04 12:00:00'),
(29, 5, 'Fried Chicken', 600, 20.00, 30.00, 45.00, '2025-06-25 18:00:00'),
(30, 5, 'Pizza Slice', 800, 90.00, 25.00, 35.00, '2025-06-26 19:30:00'),
(31, 5, 'Burger', 700, 50.00, 20.00, 40.00, '2025-06-27 17:15:00'),
(32, 5, 'Ice Cream', 500, 60.00, 5.00, 25.00, '2025-06-28 20:00:00'),
(33, 5, 'French Fries', 450, 55.00, 5.00, 20.00, '2025-06-29 18:45:00'),
(34, 5, 'Cheese Pasta', 650, 70.00, 15.00, 30.00, '2025-06-30 19:00:00'),
(35, 5, 'Donuts', 550, 65.00, 6.00, 28.00, '2025-07-01 16:30:00'),
(36, 5, 'BBQ Ribs', 750, 15.00, 35.00, 50.00, '2025-07-02 18:15:00'),
(37, 5, 'Chocolate Cake', 600, 80.00, 5.00, 30.00, '2025-07-03 20:00:00'),
(38, 5, 'Nachos', 700, 70.00, 10.00, 40.00, '2025-07-04 17:30:00'),
(39, 5, 'Fried Chicken', 600, 20.00, 30.00, 45.00, '2025-06-25 18:00:00'),
(40, 5, 'Pizza Slice', 800, 90.00, 25.00, 35.00, '2025-06-26 19:30:00'),
(41, 5, 'Burger', 700, 50.00, 20.00, 40.00, '2025-06-27 17:15:00'),
(42, 5, 'Ice Cream', 500, 60.00, 5.00, 25.00, '2025-06-28 20:00:00'),
(43, 5, 'French Fries', 450, 55.00, 5.00, 20.00, '2025-06-29 18:45:00'),
(44, 5, 'Cheese Pasta', 650, 70.00, 15.00, 30.00, '2025-06-30 19:00:00'),
(45, 5, 'Donuts', 550, 65.00, 6.00, 28.00, '2025-07-01 16:30:00'),
(46, 5, 'BBQ Ribs', 750, 15.00, 35.00, 50.00, '2025-07-02 18:15:00'),
(47, 5, 'Chocolate Cake', 600, 80.00, 5.00, 30.00, '2025-07-03 20:00:00'),
(48, 5, 'Nachos', 700, 70.00, 10.00, 40.00, '2025-07-04 17:30:00'),
(49, 5, 'Fried Chicken', 600, 20.00, 30.00, 45.00, '2025-06-25 18:00:00'),
(50, 5, 'Pizza Slice', 800, 90.00, 25.00, 35.00, '2025-06-26 19:30:00'),
(51, 5, 'Burger', 700, 50.00, 20.00, 40.00, '2025-06-27 17:15:00'),
(52, 5, 'Ice Cream', 500, 60.00, 5.00, 25.00, '2025-06-28 20:00:00'),
(53, 5, 'French Fries', 450, 55.00, 5.00, 20.00, '2025-06-29 18:45:00'),
(54, 5, 'Cheese Pasta', 650, 70.00, 15.00, 30.00, '2025-06-30 19:00:00'),
(55, 5, 'Donuts', 550, 65.00, 6.00, 28.00, '2025-07-01 16:30:00'),
(56, 5, 'BBQ Ribs', 750, 15.00, 35.00, 50.00, '2025-07-02 18:15:00'),
(57, 5, 'Chocolate Cake', 600, 80.00, 5.00, 30.00, '2025-07-03 20:00:00'),
(58, 5, 'Nachos', 700, 70.00, 10.00, 40.00, '2025-07-04 17:30:00');

-- --------------------------------------------------------

--
-- Table structure for table `mood`
--

CREATE TABLE `mood` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `rating` varchar(50) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `note` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mood`
--

INSERT INTO `mood` (`id`, `user_id`, `rating`, `date`, `note`) VALUES
(1, 6, 'Happy', '2025-06-19 00:00:00', 'Great workout'),
(2, 6, 'Neutral', '2025-06-20 00:00:00', 'Average day'),
(3, 6, 'Overwhelmed', '2025-06-21 00:00:00', 'Work deadline'),
(4, 6, 'Sad', '2025-06-22 00:00:00', 'Bad weather'),
(5, 6, 'Anxious', '2025-06-23 00:00:00', 'Meeting nerves'),
(6, 6, 'Angry', '2025-06-24 00:00:00', 'Tech issues'),
(7, 6, 'Happy', '2025-06-25 00:00:00', 'Family call'),
(8, 6, 'Neutral', '2025-06-26 00:00:00', 'Quiet evening'),
(9, 6, 'Sad', '2025-06-27 00:00:00', 'Lost item'),
(10, 6, 'Anxious', '2025-06-28 00:00:00', 'Presentation'),
(11, 6, 'Overwhelmed', '2025-06-29 00:00:00', 'Busy schedule'),
(12, 6, 'Happy', '2025-06-30 00:00:00', 'New book'),
(13, 6, 'Neutral', '2025-07-01 00:00:00', 'Restful day'),
(14, 6, 'Angry', '2025-07-02 00:00:00', 'Delayed flight'),
(15, 6, 'Sad', '2025-07-03 00:00:00', 'Tired afternoon'),
(16, 7, 'Sad', '2025-06-22 00:00:00', 'Feeling down'),
(17, 7, 'Anxious', '2025-06-23 00:00:00', 'Worried about work'),
(18, 7, 'Overwhelmed', '2025-06-24 00:00:00', 'Too much stress'),
(19, 7, 'Sad', '2025-06-25 00:00:00', 'Lonely day'),
(20, 7, 'Anxious', '2025-06-26 00:00:00', 'Health concerns'),
(21, 7, 'Sad', '2025-06-27 00:00:00', 'Bad news'),
(22, 7, 'Overwhelmed', '2025-06-28 00:00:00', 'Overloaded'),
(23, 7, 'Sad', '2025-06-29 00:00:00', 'Tough week'),
(24, 7, 'Anxious', '2025-06-30 00:00:00', 'Uncertain future'),
(25, 7, 'Overwhelmed', '2025-07-01 00:00:00', 'Exhausted'),
(26, 7, 'Sad', '2025-07-02 00:00:00', 'Missed friends'),
(27, 7, 'Anxious', '2025-07-03 00:00:00', 'Financial stress'),
(28, 7, 'Sad', '2025-07-04 00:00:00', 'Tired and low'),
(29, 5, 'Sad', '2025-06-25 00:00:00', 'Feeling unwell'),
(30, 5, 'Anxious', '2025-06-26 00:00:00', 'Sleep issues'),
(31, 5, 'Sad', '2025-06-27 00:00:00', 'Low energy'),
(32, 5, 'Neutral', '2025-06-28 00:00:00', 'Better sleep'),
(33, 5, 'Anxious', '2025-06-29 00:00:00', 'Health worries'),
(34, 5, 'Sad', '2025-06-30 00:00:00', 'Exhausted'),
(35, 5, 'Overwhelmed', '2025-07-01 00:00:00', 'Too tired'),
(36, 5, 'Neutral', '2025-07-02 00:00:00', 'Restful night'),
(37, 5, 'Sad', '2025-07-03 00:00:00', 'Poor health'),
(38, 5, 'Anxious', '2025-07-04 00:00:00', 'Unwell today'),
(39, 5, 'Sad', '2025-06-25 00:00:00', 'Feeling unwell'),
(40, 5, 'Anxious', '2025-06-26 00:00:00', 'Sleep issues'),
(41, 5, 'Sad', '2025-06-27 00:00:00', 'Low energy'),
(42, 5, 'Neutral', '2025-06-28 00:00:00', 'Better sleep'),
(43, 5, 'Anxious', '2025-06-29 00:00:00', 'Health worries'),
(44, 5, 'Sad', '2025-06-30 00:00:00', 'Exhausted'),
(45, 5, 'Overwhelmed', '2025-07-01 00:00:00', 'Too tired'),
(46, 5, 'Neutral', '2025-07-02 00:00:00', 'Restful night'),
(47, 5, 'Sad', '2025-07-03 00:00:00', 'Poor health'),
(48, 5, 'Anxious', '2025-07-04 00:00:00', 'Unwell today');

-- --------------------------------------------------------

--
-- Table structure for table `sleep`
--

CREATE TABLE `sleep` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `hours` decimal(4,2) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `quality_rating` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sleep`
--

INSERT INTO `sleep` (`id`, `user_id`, `hours`, `date`, `quality_rating`) VALUES
(1, 6, 7.00, '2025-06-19 00:00:00', 'Good'),
(2, 6, 6.50, '2025-06-20 00:00:00', 'Fair'),
(3, 6, 7.20, '2025-06-21 00:00:00', 'Good'),
(4, 6, 6.00, '2025-06-22 00:00:00', 'Poor'),
(5, 6, 7.50, '2025-06-23 00:00:00', 'Excellent'),
(6, 6, 6.80, '2025-06-24 00:00:00', 'Fair'),
(7, 6, 7.10, '2025-06-25 00:00:00', 'Good'),
(8, 6, 6.30, '2025-06-26 00:00:00', 'Fair'),
(9, 6, 7.40, '2025-06-27 00:00:00', 'Good'),
(10, 6, 6.70, '2025-06-28 00:00:00', 'Fair'),
(11, 6, 7.00, '2025-06-29 00:00:00', 'Good'),
(12, 6, 6.50, '2025-06-30 00:00:00', 'Fair'),
(13, 6, 7.30, '2025-07-01 00:00:00', 'Good'),
(14, 6, 6.90, '2025-07-02 00:00:00', 'Fair'),
(15, 6, 7.20, '2025-07-03 00:00:00', 'Good'),
(16, 7, 5.50, '2025-06-22 00:00:00', 'Poor'),
(17, 7, 6.00, '2025-06-23 00:00:00', 'Fair'),
(18, 7, 5.80, '2025-06-24 00:00:00', 'Poor'),
(19, 7, 6.20, '2025-06-25 00:00:00', 'Fair'),
(20, 7, 5.30, '2025-06-26 00:00:00', 'Poor'),
(21, 7, 6.10, '2025-06-27 00:00:00', 'Fair'),
(22, 7, 5.70, '2025-06-28 00:00:00', 'Poor'),
(23, 7, 6.00, '2025-06-29 00:00:00', 'Fair'),
(24, 7, 5.40, '2025-06-30 00:00:00', 'Poor'),
(25, 7, 6.30, '2025-07-01 00:00:00', 'Fair'),
(26, 7, 5.60, '2025-07-02 00:00:00', 'Poor'),
(27, 7, 6.00, '2025-07-03 00:00:00', 'Fair'),
(28, 7, 5.50, '2025-07-04 00:00:00', 'Poor'),
(29, 5, 3.50, '2025-06-25 00:00:00', 'Poor'),
(30, 5, 4.00, '2025-06-26 00:00:00', 'Poor'),
(31, 5, 3.80, '2025-06-27 00:00:00', 'Poor'),
(32, 5, 7.00, '2025-06-28 00:00:00', 'Good'),
(33, 5, 4.20, '2025-06-29 00:00:00', 'Poor'),
(34, 5, 3.50, '2025-06-30 00:00:00', 'Poor'),
(35, 5, 4.50, '2025-07-01 00:00:00', 'Fair'),
(36, 5, 7.00, '2025-07-02 00:00:00', 'Good'),
(37, 5, 3.70, '2025-07-03 00:00:00', 'Poor'),
(38, 5, 4.00, '2025-07-04 00:00:00', 'Poor'),
(39, 5, 3.50, '2025-06-25 00:00:00', 'Poor'),
(40, 5, 4.00, '2025-06-26 00:00:00', 'Poor'),
(41, 5, 3.80, '2025-06-27 00:00:00', 'Poor'),
(42, 5, 7.00, '2025-06-28 00:00:00', 'Good'),
(43, 5, 4.20, '2025-06-29 00:00:00', 'Poor'),
(44, 5, 3.50, '2025-06-30 00:00:00', 'Poor'),
(45, 5, 4.50, '2025-07-01 00:00:00', 'Fair'),
(46, 5, 7.00, '2025-07-02 00:00:00', 'Good'),
(47, 5, 3.70, '2025-07-03 00:00:00', 'Poor'),
(48, 5, 4.00, '2025-07-04 00:00:00', 'Poor');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password_hash`) VALUES
(5, 'maryam', 'maryamshah.990@gmail.com', '$2b$12$PvQDUZUrAlOoiqGau3FatOZUZDPAHkZRt6gv2qiC1f6KvQK9y9de.'),
(6, 'zsam', 'zsam@gmail.com', '$2b$12$.h7xSpMTw1.mSEhW7WZx/exy/ukeHAeAt8Et5Q93Y/aPtAAEDGYz.'),
(7, 'user1', 'user1@gmail.com', '$2b$12$aaSoJg//FecPr0Rsse6Xw.YEFMB924WK0yGOHrSFz5OZ5vkJbVD4W'),
(9, 'user2', 'user2@gmail.com', '$2b$12$zWdPfVPY3gpavfaDh.2RX.hzHf0AJLsrq8yTJ8XvIwIAhIZYFjbZO');

-- --------------------------------------------------------

--
-- Table structure for table `water`
--

CREATE TABLE `water` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `amount_ml` int(11) NOT NULL,
  `timestamp` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `water`
--

INSERT INTO `water` (`id`, `user_id`, `amount_ml`, `timestamp`) VALUES
(1, 6, 700, '2025-06-19 08:00:00'),
(2, 6, 800, '2025-06-20 10:00:00'),
(3, 6, 650, '2025-06-21 09:15:00'),
(4, 6, 900, '2025-06-22 11:30:00'),
(5, 6, 750, '2025-06-23 10:15:00'),
(6, 6, 850, '2025-06-24 09:45:00'),
(7, 6, 700, '2025-06-25 08:30:00'),
(8, 6, 950, '2025-06-26 11:15:00'),
(9, 6, 800, '2025-06-27 10:00:00'),
(10, 6, 900, '2025-06-28 09:30:00'),
(11, 6, 750, '2025-06-29 08:45:00'),
(12, 6, 850, '2025-06-30 11:00:00'),
(13, 6, 700, '2025-07-01 09:15:00'),
(14, 6, 800, '2025-07-02 10:30:00'),
(15, 6, 750, '2025-07-03 08:00:00'),
(16, 7, 600, '2025-06-22 09:00:00'),
(17, 7, 700, '2025-06-23 10:15:00'),
(18, 7, 650, '2025-06-24 08:30:00'),
(19, 7, 800, '2025-06-25 11:00:00'),
(20, 7, 700, '2025-06-26 09:45:00'),
(21, 7, 750, '2025-06-27 10:30:00'),
(22, 7, 600, '2025-06-28 08:15:00'),
(23, 7, 850, '2025-06-29 11:30:00'),
(24, 7, 700, '2025-06-30 09:00:00'),
(25, 7, 800, '2025-07-01 10:15:00'),
(26, 7, 650, '2025-07-02 08:45:00'),
(27, 7, 750, '2025-07-03 11:00:00'),
(28, 7, 700, '2025-07-04 09:30:00'),
(29, 5, 300, '2025-06-25 09:00:00'),
(30, 5, 400, '2025-06-26 10:15:00'),
(31, 5, 250, '2025-06-27 08:30:00'),
(32, 5, 500, '2025-06-28 11:00:00'),
(33, 5, 350, '2025-06-29 09:45:00'),
(34, 5, 300, '2025-06-30 10:00:00'),
(35, 5, 400, '2025-07-01 09:15:00'),
(36, 5, 450, '2025-07-02 10:30:00'),
(37, 5, 300, '2025-07-03 08:45:00'),
(38, 5, 350, '2025-07-04 09:00:00');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `exercise`
--
ALTER TABLE `exercise`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `meals`
--
ALTER TABLE `meals`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `mood`
--
ALTER TABLE `mood`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `sleep`
--
ALTER TABLE `sleep`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `water`
--
ALTER TABLE `water`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `exercise`
--
ALTER TABLE `exercise`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT for table `meals`
--
ALTER TABLE `meals`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=59;

--
-- AUTO_INCREMENT for table `mood`
--
ALTER TABLE `mood`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT for table `sleep`
--
ALTER TABLE `sleep`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `water`
--
ALTER TABLE `water`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `exercise`
--
ALTER TABLE `exercise`
  ADD CONSTRAINT `exercise_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `meals`
--
ALTER TABLE `meals`
  ADD CONSTRAINT `meals_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `mood`
--
ALTER TABLE `mood`
  ADD CONSTRAINT `mood_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `sleep`
--
ALTER TABLE `sleep`
  ADD CONSTRAINT `sleep_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `water`
--
ALTER TABLE `water`
  ADD CONSTRAINT `water_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
