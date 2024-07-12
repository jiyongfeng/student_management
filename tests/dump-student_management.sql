-- MySQL dump 10.13  Distrib 8.3.0, for macos14.2 (arm64)
--
-- Host: synology.yunnote.cn    Database: student_management
-- ------------------------------------------------------
-- Server version	9.0.0
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */
;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */
;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */
;
/*!50503 SET NAMES utf8mb4 */
;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */
;
/*!40103 SET TIME_ZONE='+08:00' */
;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */
;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */
;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */
;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */
;
--
-- Table structure for table `tb_course`
--

DROP TABLE IF EXISTS `tb_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */
;
/*!50503 SET character_set_client = utf8mb4 */
;
CREATE TABLE `tb_course` (
  `cou_id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(100) NOT NULL,
  `create_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `create_by` varchar(50) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`cou_id`)
) ENGINE = InnoDB AUTO_INCREMENT = 16 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */
;
--
-- Dumping data for table `tb_course`
--

LOCK TABLES `tb_course` WRITE;
/*!40000 ALTER TABLE `tb_course` DISABLE KEYS */
;
INSERT INTO `tb_course`
VALUES (
    1,
    '语文',
    '2024-07-11 04:31:34',
    'Ethan',
    '2024-07-11 15:13:53',
    '333333'
  ),
(
    2,
    '数学',
    '2024-07-11 06:01:31',
    '',
    '2024-07-11 09:45:47',
    'admin'
  ),
(
    3,
    '英语',
    '2024-07-11 06:01:37',
    '',
    '2024-07-11 09:45:47',
    'admin'
  ),
(
    4,
    '化学',
    '2024-07-11 06:01:42',
    '',
    '2024-07-11 09:45:47',
    'admin'
  ),
(
    5,
    '物理',
    '2024-07-11 06:01:50',
    '',
    '2024-07-11 09:45:47',
    'admin'
  ),
(
    6,
    '地理',
    '2024-07-11 06:02:27',
    '',
    '2024-07-11 09:45:47',
    'admin'
  ),
(
    7,
    '生物',
    '2024-07-11 08:25:05',
    NULL,
    '2024-07-11 09:45:47',
    'admin'
  ),
(
    10,
    '历史',
    '2024-07-11 10:19:56',
    'Jimmy',
    '2024-07-11 10:19:56',
    NULL
  ),
(
    11,
    '政治',
    '2024-07-11 10:20:28',
    'Jimmy',
    '2024-07-11 10:20:28',
    NULL
  ),
(
    12,
    '信息技术1',
    '2024-07-11 11:26:53',
    '',
    '2024-07-11 15:01:26',
    '1'
  );
/*!40000 ALTER TABLE `tb_course` ENABLE KEYS */
;
UNLOCK TABLES;
--
-- Table structure for table `tb_exam`
--

DROP TABLE IF EXISTS `tb_exam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */
;
/*!50503 SET character_set_client = utf8mb4 */
;
CREATE TABLE `tb_exam` (
  `exam_id` int NOT NULL AUTO_INCREMENT,
  `exam_name` varchar(100) NOT NULL,
  `create_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `create_by` varchar(50) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`exam_id`)
) ENGINE = InnoDB AUTO_INCREMENT = 4 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */
;
--
-- Dumping data for table `tb_exam`
--

LOCK TABLES `tb_exam` WRITE;
/*!40000 ALTER TABLE `tb_exam` DISABLE KEYS */
;
INSERT INTO `tb_exam`
VALUES (
    1,
    '1210高一下期末考试',
    '2024-07-11 04:31:24',
    'Ethan',
    '2024-07-11 06:26:47',
    ''
  ),
(
    2,
    '1205高一下期末考试',
    '2024-07-11 06:08:53',
    '',
    '2024-07-11 06:27:01',
    ''
  ),
(
    3,
    '1105高一下期中考试',
    '2024-07-11 08:25:04',
    NULL,
    '2024-07-11 08:25:04',
    NULL
  );
/*!40000 ALTER TABLE `tb_exam` ENABLE KEYS */
;
UNLOCK TABLES;
--
-- Table structure for table `tb_scores`
--

DROP TABLE IF EXISTS `tb_scores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */
;
/*!50503 SET character_set_client = utf8mb4 */
;
CREATE TABLE `tb_scores` (
  `score_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int DEFAULT NULL,
  `exam_id` int DEFAULT NULL,
  `course_id` int DEFAULT NULL,
  `score` float DEFAULT NULL,
  `create_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `create_by` varchar(50) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`score_id`),
  KEY `student_id` (`student_id`),
  KEY `course_id` (`course_id`),
  KEY `exam_id` (`exam_id`),
  CONSTRAINT `tb_scores_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `tb_student` (`stu_id`),
  CONSTRAINT `tb_scores_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `tb_course` (`cou_id`),
  CONSTRAINT `tb_scores_ibfk_3` FOREIGN KEY (`exam_id`) REFERENCES `tb_exam` (`exam_id`)
) ENGINE = InnoDB AUTO_INCREMENT = 8 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */
;
--
-- Dumping data for table `tb_scores`
--

LOCK TABLES `tb_scores` WRITE;
/*!40000 ALTER TABLE `tb_scores` DISABLE KEYS */
;
INSERT INTO `tb_scores`
VALUES (
    1,
    1,
    1,
    1,
    62.5,
    '2024-07-11 04:32:11',
    'Ethan',
    '2024-07-11 04:32:11',
    NULL
  ),
(
    2,
    1,
    1,
    2,
    67,
    '2024-07-11 06:02:53',
    '',
    '2024-07-11 06:02:53',
    NULL
  ),
(
    3,
    1,
    2,
    2,
    81,
    '2024-07-11 06:09:15',
    '',
    '2024-07-11 06:09:15',
    NULL
  ),
(
    6,
    1,
    3,
    7,
    81,
    '2024-07-11 08:25:05',
    NULL,
    '2024-07-11 08:25:05',
    NULL
  ),
(
    7,
    1,
    3,
    7,
    81,
    '2024-07-12 02:20:29',
    NULL,
    '2024-07-12 02:20:29',
    NULL
  );
/*!40000 ALTER TABLE `tb_scores` ENABLE KEYS */
;
UNLOCK TABLES;
--
-- Table structure for table `tb_student`
--

DROP TABLE IF EXISTS `tb_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */
;
/*!50503 SET character_set_client = utf8mb4 */
;
CREATE TABLE `tb_student` (
  `stu_id` int NOT NULL AUTO_INCREMENT,
  `student_name` varchar(100) NOT NULL,
  `create_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `create_by` varchar(50) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`stu_id`)
) ENGINE = InnoDB AUTO_INCREMENT = 3 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */
;
--
-- Dumping data for table `tb_student`
--

LOCK TABLES `tb_student` WRITE;
/*!40000 ALTER TABLE `tb_student` DISABLE KEYS */
;
INSERT INTO `tb_student`
VALUES (
    1,
    '张季涵',
    '2024-07-11 04:31:58',
    'Ethan',
    '2024-07-11 04:31:58',
    NULL
  ),
(
    2,
    '111',
    '2024-07-12 02:01:34',
    'test',
    '2024-07-12 02:01:45',
    '222'
  );
/*!40000 ALTER TABLE `tb_student` ENABLE KEYS */
;
UNLOCK TABLES;
--
-- Dumping routines for database 'student_management'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */
;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */
;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */
;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */
;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */
;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */
;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */
;
-- Dump completed on 2024-07-12 12:19:14