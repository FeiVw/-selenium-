/*
SQLyog Ultimate v12.09 (64 bit)
MySQL - 5.7.40-log : Database - anime_website
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`anime_website` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `anime_website`;

/*Table structure for table `drf_animebigwuhureal` */

DROP TABLE IF EXISTS `drf_animebigwuhureal`;

CREATE TABLE `drf_animebigwuhureal` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `video_episodes_count` int(11) NOT NULL,
  `video_episodes` varchar(200) NOT NULL,
  `video_title` varchar(200) NOT NULL,
  `video_area` varchar(200) NOT NULL,
  `video_year` varchar(50) NOT NULL,
  `poster` varchar(1000) NOT NULL,
  `video_info` varchar(5000) NOT NULL,
  `video_update` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1806 DEFAULT CHARSET=utf8;

/*Table structure for table `drf_animesmallwuhureal` */

DROP TABLE IF EXISTS `drf_animesmallwuhureal`;

CREATE TABLE `drf_animesmallwuhureal` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `video_episode` varchar(10) NOT NULL,
  `video_title` varchar(200) NOT NULL,
  `video_area` varchar(200) NOT NULL,
  `video_year` varchar(200) NOT NULL,
  `video_url` varchar(5000) NOT NULL,
  `anime_key_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `drf_animesmallwuhure_anime_key_id_7fb7125f_fk_drf_anime` (`anime_key_id`),
  CONSTRAINT `drf_animesmallwuhure_anime_key_id_7fb7125f_fk_drf_anime` FOREIGN KEY (`anime_key_id`) REFERENCES `drf_animebigwuhureal` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22054 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
