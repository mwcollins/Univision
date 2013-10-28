drop database if exists univision;
create database univision;
use univision;

--
-- Table structure for table `Shows`
--
CREATE TABLE `Shows` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=latin1;

--
-- Table structure for table `MovieClips`
--
CREATE TABLE `MovieClips` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `start` time NOT NULL,
  `stop` time NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1003 DEFAULT CHARSET=latin1;

--
-- Table structure for table `Producers`
--
CREATE TABLE `Producers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1003 DEFAULT CHARSET=latin1;

--
-- Table structure for table `MovieClipsInShows`
--
CREATE TABLE `MovieClipsInShows` (
  `showId` int(11) NOT NULL,
  `movieClipId` int(11) NOT NULL,
  PRIMARY KEY (`showId`,`movieClipId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `ShowHasProducers`
--
CREATE TABLE `ShowHasProducers` (
  `showId` int(11) NOT NULL,
  `producerId` int(11) NOT NULL,
  PRIMARY KEY (`showId`,`producerId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

grant all on univision.* to 'univision'@'localhost' identified by 'univision';

