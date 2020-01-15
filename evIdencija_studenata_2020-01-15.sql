# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.18-0ubuntu0.16.04.1)
# Database: evIdencija_studenata
# Generation Time: 2020-01-15 03:34:40 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table korisnici
# ------------------------------------------------------------

DROP TABLE IF EXISTS `korisnici`;

CREATE TABLE `korisnici` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ime` varchar(100) NOT NULL,
  `prezime` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `lozinka` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `korisnici` WRITE;
/*!40000 ALTER TABLE `korisnici` DISABLE KEYS */;

INSERT INTO `korisnici` (`id`, `ime`, `prezime`, `email`, `lozinka`)
VALUES
	(2,'John','Ortiz','scmj@vts.srb','pbkdf2:sha256:150000$iFToHgeC$8324937816225766bc98d1dc84d65c70fd57b0dedc0c9f132367583e8b52204c'),
	(3,'Bob','Wulff','lele@be.gov','pbkdf2:sha256:150000$JmJxK0Qs$3c82b8bfddfb710b058c1f095f0dac5166f68a72e788c68fa36f978d43fae294'),
	(5,'idk','test','hes@vts','pbkdf2:sha256:150000$HDfavpPE$c324cf29385118f3bda77a3a37bc4a76a65b39213bf29e5da7af16bf89cb3d0f');

/*!40000 ALTER TABLE `korisnici` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table ocene
# ------------------------------------------------------------

DROP TABLE IF EXISTS `ocene`;

CREATE TABLE `ocene` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `predmet_id` int(11) NOT NULL,
  `ocena` smallint(6) NOT NULL,
  `datum` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student` (`student_id`),
  KEY `predmet` (`predmet_id`),
  CONSTRAINT `predmet` FOREIGN KEY (`predmet_id`) REFERENCES `predmeti` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `student` FOREIGN KEY (`student_id`) REFERENCES `studenti` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `ocene` WRITE;
/*!40000 ALTER TABLE `ocene` DISABLE KEYS */;

INSERT INTO `ocene` (`id`, `student_id`, `predmet_id`, `ocena`, `datum`)
VALUES
	(9,2,3,10,'0001-01-01'),
	(14,3,3,9,'0001-01-01'),
	(15,3,5,5,'1563-01-05'),
	(16,2,5,6,'4789-01-01'),
	(17,3,4,9,'3210-04-06'),
	(18,2,4,10,'2020-01-17');

/*!40000 ALTER TABLE `ocene` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table predmeti
# ------------------------------------------------------------

DROP TABLE IF EXISTS `predmeti`;

CREATE TABLE `predmeti` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sifra` varchar(30) NOT NULL,
  `naziv` varchar(50) NOT NULL,
  `godina_studija` smallint(6) NOT NULL,
  `espb` int(11) NOT NULL,
  `obavezni_izborni` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `predmeti` WRITE;
/*!40000 ALTER TABLE `predmeti` DISABLE KEYS */;

INSERT INTO `predmeti` (`id`, `sifra`, `naziv`, `godina_studija`, `espb`, `obavezni_izborni`)
VALUES
	(3,'WP','Web programiranje',3,6,'Izborni'),
	(4,'RM','Mreze',2,8,'Obavezni'),
	(5,'idk','Digitalna elektronika',2,4,'Izborni');

/*!40000 ALTER TABLE `predmeti` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table studenti
# ------------------------------------------------------------

DROP TABLE IF EXISTS `studenti`;

CREATE TABLE `studenti` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ime` varchar(100) NOT NULL,
  `ime_roditelja` varchar(100) NOT NULL,
  `prezime` varchar(100) NOT NULL,
  `broj_indeksa` varchar(10) NOT NULL,
  `godina_studija` smallint(6) NOT NULL,
  `JMBG` bigint(20) NOT NULL,
  `datum_rodjenja` date NOT NULL,
  `espb` int(11) DEFAULT NULL,
  `prosek_ocena` float DEFAULT NULL,
  `broj_telefona` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `studenti` WRITE;
/*!40000 ALTER TABLE `studenti` DISABLE KEYS */;

INSERT INTO `studenti` (`id`, `ime`, `ime_roditelja`, `prezime`, `broj_indeksa`, `godina_studija`, `JMBG`, `datum_rodjenja`, `espb`, `prosek_ocena`, `broj_telefona`, `email`)
VALUES
	(2,'Goran','Zoran','Djukic','SEr 38/17',3,730013,'1998-11-08',18,8.66667,'064','gorandjukic2000@live.com'),
	(3,'Filip','Milos','Stojanovic','REr 1/20',1,735069,'1001-01-01',18,7.66667,'666','fica@vtsnis.edu.rs');

/*!40000 ALTER TABLE `studenti` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
