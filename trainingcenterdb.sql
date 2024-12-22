-- MySQL dump 10.13  Distrib 8.1.0, for Win64 (x86_64)
--
-- Host: localhost    Database: trainingcenterdb
-- ------------------------------------------------------
-- Server version	8.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_0900_as_cs NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'An ninh Mang'),(4,'Lập trình web'),(3,'Quan tri he thong'),(2,'Quan tri Mang');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `content` varchar(255) COLLATE utf8mb4_0900_as_cs NOT NULL,
  `user_id` int NOT NULL,
  `course_id` int NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `active` tinyint(1) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES ('123',1,1,1,1,'2024-12-16 15:22:05'),('456',2,1,2,1,'2024-12-16 15:22:05');
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_0900_as_cs NOT NULL,
  `price` float DEFAULT NULL,
  `image` varchar(100) COLLATE utf8mb4_0900_as_cs DEFAULT NULL,
  `category_id` int NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_0900_as_cs DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `course_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (1,'Quan tri he thong server',1500000,'https://res.cloudinary.com/dn0kj5rfm/image/upload/v1734333167/afftm5knvqdq28ydmdlb.png',4,'132sfwqgryjrncvb'),(2,'Lap trinh web cơ bản',3000000,'https://res.cloudinary.com/dn0kj5rfm/image/upload/v1734610997/rn2lgxc2smq8jvv4apic.jpg',2,'Giúp người học hiểu được lập trình web cơ bản'),(3,'Thông thạo các bước quản trị hệ thống',2500000,'https://res.cloudinary.com/dn0kj5rfm/image/upload/v1734613720/aba2yfkstldgyxpckrnf.webp',3,'Với 3 tháng sẽ giúp học viên tốt hơn trong việc quản trị hệ thống của mình');
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receipt`
--

DROP TABLE IF EXISTS `receipt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receipt` (
  `user_id` int NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `active` tinyint(1) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `receipt_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receipt`
--

LOCK TABLES `receipt` WRITE;
/*!40000 ALTER TABLE `receipt` DISABLE KEYS */;
INSERT INTO `receipt` VALUES (1,1,1,'2024-12-18 14:47:27'),(2,2,1,'2024-12-18 14:47:27'),(1,3,1,'2024-12-19 20:06:09'),(1,4,1,'2024-12-19 20:06:09');
/*!40000 ALTER TABLE `receipt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receipt_details`
--

DROP TABLE IF EXISTS `receipt_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receipt_details` (
  `receipt_id` int NOT NULL,
  `course_id` int NOT NULL,
  `time_table` varchar(255) COLLATE utf8mb4_0900_as_cs DEFAULT NULL,
  `school_start_date` date DEFAULT NULL,
  `school_end_date` date DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `active` tinyint(1) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `receipt_id` (`receipt_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `receipt_details_ibfk_1` FOREIGN KEY (`receipt_id`) REFERENCES `receipt` (`id`),
  CONSTRAINT `receipt_details_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receipt_details`
--

LOCK TABLES `receipt_details` WRITE;
/*!40000 ALTER TABLE `receipt_details` DISABLE KEYS */;
INSERT INTO `receipt_details` VALUES (1,1,'357','2024-12-18','2025-03-18',1,1,'2024-12-18 14:47:27'),(2,1,'T7CN','2024-12-28','2025-03-28',2,1,'2024-12-18 14:47:27'),(3,2,'246','2024-12-23','2025-03-23',5,1,'2024-12-19 20:06:09'),(4,2,'246','2024-12-23','2025-03-23',6,1,'2024-12-19 20:06:09');
/*!40000 ALTER TABLE `receipt_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_0900_as_cs DEFAULT NULL,
  `avatar` varchar(100) COLLATE utf8mb4_0900_as_cs DEFAULT NULL,
  `username` varchar(50) COLLATE utf8mb4_0900_as_cs DEFAULT NULL,
  `password` varchar(150) COLLATE utf8mb4_0900_as_cs DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_0900_as_cs DEFAULT NULL,
  `user_role` enum('USER','ADMIN') COLLATE utf8mb4_0900_as_cs DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','https://res.cloudinary.com/dn0kj5rfm/image/upload/v1732265835/user_avatars/tzqmihffavxyn6joa8px.jpg','admin','e10adc3949ba59abbe56e057f20f883e','xyz@gmail.com','ADMIN'),(2,'demo','https://res.cloudinary.com/dxxwcby8l/image/upload/v1679731974/jlad6jqdc69cjrh9zggq.jpg','demo','e10adc3949ba59abbe56e057f20f883e',NULL,'USER'),(3,'Nguyen van a','https://res.cloudinary.com/dn0kj5rfm/image/upload/v1732262524/user_avatars/oduvhrsyktq2dogwpad6.webp','test1','123456','abc@gmail.com','ADMIN');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-22 18:37:54
