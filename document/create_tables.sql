delimiter $$

CREATE TABLE `inv_user` (
  `userId` int(11) NOT NULL AUTO_INCREMENT,
  `userName` varchar(50) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`userId`)
)

delimiter $$

CREATE TABLE `inv_item` (
  `userId` int(11) NOT NULL,
  `itemId` int(11) NOT NULL,
  `title` varchar(50) DEFAULT NULL,
  `barcode` varchar(30) DEFAULT NULL,
  `category` varchar(20) DEFAULT NULL,
  `condition` varchar(20) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `size` varchar(20) DEFAULT NULL,
  `weight` varchar(20) DEFAULT NULL,
  `latitude` decimal(10,7) DEFAULT NULL,
  `longitude` decimal(10,7) DEFAULT NULL,
  `desc` text,
  `photoname1` varchar(20) DEFAULT NULL,
  `photoname2` varchar(20) DEFAULT NULL,
  `photoname3` varchar(20) DEFAULT NULL,
  `createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updateDate` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`userId`,`itemId`),
  KEY `inv_item_fk1_idx` (`userId`),
  CONSTRAINT `inv_item_fk1` FOREIGN KEY (`userId`) REFERENCES `inv_user` (`userId`) ON DELETE NO ACTION ON UPDATE NO ACTION
)
