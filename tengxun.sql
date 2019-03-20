/*
 Navicat Premium Data Transfer

 Source Server         : 本地数据库
 Source Server Type    : MySQL
 Source Server Version : 50637
 Source Host           : localhost:3306
 Source Schema         : newssenti

 Target Server Type    : MySQL
 Target Server Version : 50637
 File Encoding         : 65001

 Date: 18/03/2019 20:49:13
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tengxun
-- ----------------------------
DROP TABLE IF EXISTS `tengxun`;
CREATE TABLE `tengxun`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `urlState` char(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT 'False',
  `Hcontent` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `Mcontent` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `Tcontent` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `Acontent` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `newdate` char(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `number` int(11) NULL DEFAULT NULL,
  `fromWhere` char(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `hadmix` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'False',
  `category` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `title`(`title`) USING BTREE,
  UNIQUE INDEX `title_2`(`title`) USING BTREE,
  UNIQUE INDEX `url`(`url`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4076 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
