drop database hybrid;
create database hybrid;
use hybrid;
CREATE TABLE `accessrequest` (
  `s_id` int(255) NOT NULL AUTO_INCREMENT,
  `searchbyId` varchar(255) DEFAULT NULL,
  `searchby` varchar(255) DEFAULT NULL,
  `datee` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT 'pending',
  PRIMARY KEY (`s_id`),
  UNIQUE KEY `searchbyId` (`searchbyId`),
  UNIQUE KEY `searchby` (`searchby`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

CREATE TABLE `download` (
  `d_id` int(255) NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) NOT NULL,
  `user` varchar(255) NOT NULL,
  `ownername` varchar(255) NOT NULL,
  `datee` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`d_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;


CREATE TABLE `files` (
  `f_id` int(255) NOT NULL AUTO_INCREMENT,
  `fname` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `oname` varchar(255) DEFAULT NULL,
  `descc` varchar(255) NOT NULL,
  `fdata` text,
  `etype` varchar(255) DEFAULT NULL,
  `edata` text,
  `aeskey` text,
  `aesctext` text,
  `aesiv` text,
  `authTag` text,
  `myiv` text,
  `mykey` text,
  `myEncrypted` text,
  `efrag1` text,
  `efrag2` text,
  `efrag3` text,
  `efrag4` text,
  `efrag5` text,
  `efrag6` text,
  `efrag7` text,
  `datee` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`f_id`),
  UNIQUE KEY `fname` (`fname`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;


CREATE TABLE `oregistration` (
  `o_id` int(255) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `pic` varchar(255) NOT NULL,
  `status` varchar(255) DEFAULT 'unauthorized',
  PRIMARY KEY (`o_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;


CREATE TABLE `request` (
  `r_id` int(255) NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) NOT NULL,
  `file_id` varchar(255) NOT NULL,
  `reqby` varchar(255) DEFAULT NULL,
  `ownername` varchar(255) NOT NULL,
  `datee` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT 'pending',
  `fkey` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`r_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;


CREATE TABLE `uregistration` (
  `o_id` int(255) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `pic` varchar(255) NOT NULL,
  `status` varchar(255) DEFAULT 'unauthorized',
  PRIMARY KEY (`o_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
