/*
 Navicat Premium Data Transfer

 Source Server         : db_ant
 Source Server Type    : MySQL
 Source Server Version : 50715
 Source Host           : localhost:3306
 Source Schema         : douban

 Target Server Type    : MySQL
 Target Server Version : 50715
 File Encoding         : 65001

 Date: 04/09/2019 23:29:10
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for books
-- ----------------------------
DROP TABLE IF EXISTS `books`;
CREATE TABLE `books` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `slug` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `sub_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `alt_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `cover` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `summary` text COLLATE utf8mb4_unicode_ci,
  `authors` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `author_intro` text COLLATE utf8mb4_unicode_ci,
  `translators` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `series` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `publisher` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `publish_date` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `pages` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `price` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `binding` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `isbn` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `tags` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `douban_id` int(10) unsigned NOT NULL DEFAULT '0',
  `douban_score` decimal(3,1) unsigned NOT NULL DEFAULT '0.0',
  `douban_votes` int(10) unsigned NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `books_slug_index` (`slug`),
  KEY `books_name_index` (`name`),
  KEY `books_douban_id_index` (`douban_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for comments
-- ----------------------------
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `douban_id` int(10) unsigned NOT NULL DEFAULT '0',
  `douban_comment_id` int(10) unsigned NOT NULL DEFAULT '0',
  `douban_user_nickname` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `douban_user_avatar` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `douban_user_url` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `content` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `votes` int(10) unsigned NOT NULL DEFAULT '0',
  `rating` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `comments_douban_id_index` (`douban_id`),
  KEY `comments_douban_comment_id_index` (`douban_comment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3460029 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for movies
-- ----------------------------
DROP TABLE IF EXISTS `movies`;
CREATE TABLE `movies` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `slug` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `alias` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `cover` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `year` smallint(5) unsigned NOT NULL DEFAULT '0',
  `regions` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `genres` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `languages` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `release_date` date DEFAULT NULL,
  `official_site` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `directors` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `actors` text COLLATE utf8mb4_unicode_ci,
  `storyline` text COLLATE utf8mb4_unicode_ci,
  `mins` smallint(5) unsigned NOT NULL DEFAULT '0',
  `recommend_tip` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `tags` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `avg_score` decimal(3,1) unsigned NOT NULL DEFAULT '0.0',
  `imdb_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `imdb_score` decimal(3,1) unsigned NOT NULL DEFAULT '0.0',
  `imdb_votes` int(10) unsigned NOT NULL DEFAULT '0',
  `douban_id` int(10) unsigned NOT NULL DEFAULT '0',
  `douban_score` decimal(3,1) unsigned NOT NULL DEFAULT '0.0',
  `douban_votes` int(10) unsigned NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `actor_ids` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `director_ids` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `movies_slug_index` (`slug`),
  KEY `movies_name_index` (`name`),
  KEY `movies_imdb_id_index` (`imdb_id`),
  KEY `movies_douban_id_index` (`douban_id`)
) ENGINE=InnoDB AUTO_INCREMENT=286399 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ----------------------------
-- Table structure for person
-- ----------------------------
DROP TABLE IF EXISTS `person`;
CREATE TABLE `person` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `person_id` int(10) unsigned NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `sex` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `birth` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `birthplace` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `biography` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `profession` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `constellatory` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `name_zh` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `name_en` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `person_index` (`person_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=123863 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for person_obj
-- ----------------------------
DROP TABLE IF EXISTS `person_obj`;
CREATE TABLE `person_obj` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `person_id` int(10) unsigned NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `person_id_index` (`person_id`) USING BTREE,
  KEY `name_index` (`name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=72978 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for proxys
-- ----------------------------
DROP TABLE IF EXISTS `proxys`;
CREATE TABLE `proxys` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `proxy_ip` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `valid` int(10) unsigned NOT NULL DEFAULT '1',
  `created_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `call_times` int(10) NOT NULL DEFAULT '0',
  `valid_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11407 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for subjects
-- ----------------------------
DROP TABLE IF EXISTS `subjects`;
CREATE TABLE `subjects` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `douban_id` int(10) unsigned NOT NULL DEFAULT '0',
  `type` enum('movie','book') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'movie',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `subjects_douban_id_unique` (`douban_id`)
) ENGINE=InnoDB AUTO_INCREMENT=239777 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
