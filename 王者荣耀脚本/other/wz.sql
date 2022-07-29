-- --------------------------------------------------------
-- 主机:                           106.55.231.58
-- 服务器版本:                        5.6.50-log - Source distribution
-- 服务器操作系统:                      Linux
-- HeidiSQL 版本:                  11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- 导出 study_crawler 的数据库结构
CREATE DATABASE IF NOT EXISTS `study_crawler_77` /*!40100 DEFAULT CHARACTER SET armscii8 COLLATE armscii8_bin */;
USE `study_crawler_77`;

-- 导出  表 study_crawler.battle 结构
CREATE TABLE IF NOT EXISTS `battle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_seq` text COLLATE utf8mb4_bin,
  `game_type` text COLLATE utf8mb4_bin,
  `game_svr_entity` text COLLATE utf8mb4_bin,
  `relay_svr_entity` text COLLATE utf8mb4_bin,
  `dt_event_time` text COLLATE utf8mb4_bin,
  `blue_kill_cnt` text COLLATE utf8mb4_bin,
  `red_kill_cnt` text COLLATE utf8mb4_bin,
  `is_blue` text COLLATE utf8mb4_bin,
  `game_time` text COLLATE utf8mb4_bin,
  `is_victory` text COLLATE utf8mb4_bin,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4487 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- 数据导出被取消选择。

-- 导出  表 study_crawler.hero 结构
CREATE TABLE IF NOT EXISTS `hero` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hero_id` text COLLATE utf8mb4_bin,
  `game_hero_id` text COLLATE utf8mb4_bin,
  `icon` text COLLATE utf8mb4_bin,
  `brief_name` text COLLATE utf8mb4_bin,
  `category` text COLLATE utf8mb4_bin,
  `category_id` text COLLATE utf8mb4_bin,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- 数据导出被取消选择。

-- 导出  表 study_crawler.user 结构
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `open_id` text COLLATE utf8mb4_bin,
  `zone_area_id` text COLLATE utf8mb4_bin,
  `nick_name` text COLLATE utf8mb4_bin,
  `head_img_url` text COLLATE utf8mb4_bin,
  `game_name` text COLLATE utf8mb4_bin,
  `service_name` text COLLATE utf8mb4_bin,
  `rank_desc` text COLLATE utf8mb4_bin,
  `winning_percentage` text COLLATE utf8mb4_bin,
  `rank_lift` text COLLATE utf8mb4_bin,
  `win_desc` text COLLATE utf8mb4_bin,
  `rank_star` text COLLATE utf8mb4_bin,
  `ladder_score` text COLLATE utf8mb4_bin,
  `fetched` text COLLATE utf8mb4_bin,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3609 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- 数据导出被取消选择。

-- 导出  表 study_crawler.user_battle_detail 结构
CREATE TABLE IF NOT EXISTS `user_battle_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `open_id` text COLLATE utf8mb4_bin,
  `name` text COLLATE utf8mb4_bin,
  `game_name` text COLLATE utf8mb4_bin,
  `hero_id` text COLLATE utf8mb4_bin,
  `game_seq` text COLLATE utf8mb4_bin,
  `game_svr_entity` text COLLATE utf8mb4_bin,
  `relay_svr_entity` text COLLATE utf8mb4_bin,
  `game_type` text COLLATE utf8mb4_bin,
  `hero_name` text COLLATE utf8mb4_bin,
  `total_hurt` text COLLATE utf8mb4_bin,
  `total_hurt_hero` text COLLATE utf8mb4_bin,
  `suffer_hurt` text COLLATE utf8mb4_bin,
  `total_hurt_percent` text COLLATE utf8mb4_bin,
  `total_hurt_hero_percent` text COLLATE utf8mb4_bin,
  `suffer_hurt_percent` text COLLATE utf8mb4_bin,
  `kill_cnt` text COLLATE utf8mb4_bin,
  `dead_cnt` text COLLATE utf8mb4_bin,
  `assist_cnt` text COLLATE utf8mb4_bin,
  `is_blue` text COLLATE utf8mb4_bin,
  `grade_of_rank` text COLLATE utf8mb4_bin,
  `lose_mvp` text COLLATE utf8mb4_bin,
  `is_mvp` text COLLATE utf8mb4_bin,
  `pvp_level` text COLLATE utf8mb4_bin,
  `total_in_battle_coin` text COLLATE utf8mb4_bin,
  `used_time` text COLLATE utf8mb4_bin,
  `mvp_score_tth` text COLLATE utf8mb4_bin,
  `zone_area_id` text COLLATE utf8mb4_bin,
  `is_low_score` text COLLATE utf8mb4_bin,
  `is_victory` text COLLATE utf8mb4_bin,
  `acnt_camp` text COLLATE utf8mb4_bin,
  `is_five_army` text COLLATE utf8mb4_bin,
  `game_result` text COLLATE utf8mb4_bin,
  `six_kill` text COLLATE utf8mb4_bin,
  `seven_kill` text COLLATE utf8mb4_bin,
  `eight_kill` text COLLATE utf8mb4_bin,
  `game_score` text COLLATE utf8mb4_bin,
  `multi_camp_rank` text COLLATE utf8mb4_bin,
  `is_ai_pvp` text COLLATE utf8mb4_bin,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=29973 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- 数据导出被取消选择。

-- 导出  表 study_crawler.user_hero 结构
CREATE TABLE IF NOT EXISTS `user_hero` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hero_id` text COLLATE utf8mb4_bin,
  `open_id` text COLLATE utf8mb4_bin,
  `zone_area_id` text COLLATE utf8mb4_bin,
  `hero_name` text COLLATE utf8mb4_bin,
  `combat_power` text COLLATE utf8mb4_bin,
  `winning_percentage` text COLLATE utf8mb4_bin,
  `pro_level` text COLLATE utf8mb4_bin,
  `category` text COLLATE utf8mb4_bin,
  `battle_cnt` text COLLATE utf8mb4_bin,
  `total_win_rate` text COLLATE utf8mb4_bin,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=13500 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- 数据导出被取消选择。

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
