SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `shop`
-- ----------------------------
DROP TABLE IF EXISTS `shop`;
CREATE TABLE `shop` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `shop_id` varchar(20) NOT NULL,
  `shop_name` varchar(200) NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of shop
-- ----------------------------
INSERT INTO `shop` VALUES ('1', '44794', '茶', '2018-12-05 13:26:16');

DROP TABLE IF EXISTS `item`;
CREATE TABLE `item` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `item_id` varchar(20) NOT NULL,
  `title` varchar(300) DEFAULT NULL,
  `comment_count` int(10) unsigned zerofill DEFAULT NULL,
  `really_price` varchar(50) DEFAULT NULL,
  `original_price` varchar(50) DEFAULT NULL,
  `address` varchar(300) DEFAULT NULL,
  `if_express` varchar(200) DEFAULT NULL,
  `coupon` varchar(600) DEFAULT NULL,
  `poor_rateshow` varchar(50) DEFAULT NULL,
  `poor_count` int(10) DEFAULT NULL,
  `general_count` int(10) DEFAULT NULL,
  `good_count` int(10) DEFAULT NULL,
  `good_rateshow` varchar(50) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=338 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for `comment`
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `item_id` varchar(20) NOT NULL,
  `cm_id` varchar(100) DEFAULT NULL,
  `level` varchar(20) DEFAULT NULL,
  `score` varchar(20) DEFAULT NULL,
  `content` varchar(2000) DEFAULT NULL,
  `user` varchar(100) DEFAULT NULL,
  `comment_time` varchar(200) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11874 DEFAULT CHARSET=utf8;