# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: localhost (MySQL 5.6.15)
# Database: art17_consultation
# Generation Time: 2014-01-08 09:53:56 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table comments
# ------------------------------------------------------------

CREATE TABLE `comments` (
  `id` int(11) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `region` varchar(4) NOT NULL,
  `assesment_speciesname` varchar(50) NOT NULL,
  `user` varchar(25) NOT NULL,
  `MS` varchar(4) NOT NULL DEFAULT 'EU25',
  `comment` longtext,
  `author` varchar(25) NOT NULL,
  `post_date` varchar(16) NOT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table comments_read
# ------------------------------------------------------------

CREATE TABLE `comments_read` (
  `id_comment` int(11) unsigned zerofill NOT NULL,
  `reader_user_id` varchar(25) NOT NULL,
  KEY `comments_read_fk` (`id_comment`),
  KEY `reader_user_id` (`reader_user_id`),
  CONSTRAINT `comments_read_fk` FOREIGN KEY (`id_comment`) REFERENCES `comments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table dic_country_codes
# ------------------------------------------------------------

CREATE TABLE `dic_country_codes` (
  `code` varchar(2) NOT NULL DEFAULT '',
  `codeEU` varchar(2) DEFAULT '',
  `name` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table etc_data_habitattype_automatic_assessment
# ------------------------------------------------------------

CREATE TABLE `etc_data_habitattype_automatic_assessment` (
  `assessment_method` varchar(3) NOT NULL,
  `order` int(11) DEFAULT NULL,
  `habitatcode` varchar(4) NOT NULL,
  `region` varchar(4) NOT NULL,
  `range_surface_area` varchar(100) DEFAULT NULL,
  `percentage_range_surface_area` varchar(100) DEFAULT NULL,
  `range_trend` varchar(100) DEFAULT NULL,
  `range_yearly_magnitude` varchar(100) DEFAULT NULL,
  `complementary_favourable_range` varchar(100) DEFAULT NULL,
  `coverage_surface_area` varchar(100) DEFAULT NULL,
  `percentage_coverage_surface_area` varchar(100) DEFAULT NULL,
  `coverage_trend` varchar(100) DEFAULT NULL,
  `coverage_yearly_magnitude` varchar(100) DEFAULT NULL,
  `complementary_favourable_area` varchar(100) DEFAULT NULL,
  `conclusion_range` varchar(3) DEFAULT NULL,
  `conclusion_range_gis` varchar(3) DEFAULT NULL,
  `conclusion_coverage` varchar(3) DEFAULT NULL,
  `conclusion_coverage_gis` varchar(3) DEFAULT NULL,
  `percentage_structure` varchar(100) DEFAULT NULL,
  `conclusion_structure` varchar(3) DEFAULT NULL,
  `percentage_future` varchar(100) DEFAULT NULL,
  `conclusion_future` varchar(3) DEFAULT NULL,
  `percentage_assessment` varchar(100) DEFAULT NULL,
  `conclusion_assessment` varchar(3) DEFAULT NULL,
  `range_grid_area` varchar(100) DEFAULT NULL,
  `percentage_range_grid_area` varchar(100) DEFAULT NULL,
  `distribution_grid_area` varchar(100) DEFAULT NULL,
  `percentage_distribution_grid_area` varchar(100) DEFAULT NULL,
  `assessment_needed` int(11) DEFAULT NULL,
  PRIMARY KEY (`assessment_method`,`habitatcode`,`region`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table etc_data_habitattype_regions
# ------------------------------------------------------------

CREATE TABLE `etc_data_habitattype_regions` (
  `country` varchar(3) NOT NULL,
  `eu_country_code` varchar(2) NOT NULL,
  `delivery` tinyint(1) NOT NULL,
  `envelope` varchar(50) NOT NULL,
  `filename` varchar(60) NOT NULL,
  `region` varchar(4) NOT NULL,
  `region_ms` varchar(4) DEFAULT NULL,
  `region_changed` tinyint(1) DEFAULT NULL,
  `group` varchar(21) DEFAULT NULL,
  `annex` varchar(11) DEFAULT NULL,
  `annex_I` varchar(2) DEFAULT NULL,
  `priority` varchar(1) DEFAULT NULL,
  `code` varchar(4) DEFAULT NULL,
  `habitatcode` varchar(4) DEFAULT NULL,
  `habitattype_type` varchar(5) DEFAULT NULL,
  `habitattype_type_asses` tinyint(1) DEFAULT NULL,
  `range_surface_area` double DEFAULT NULL,
  `percentage_range_surface_area` double DEFAULT NULL,
  `range_trend` varchar(1) DEFAULT NULL,
  `range_yearly_magnitude` double DEFAULT NULL,
  `complementary_favourable_range_q` varchar(2) DEFAULT NULL,
  `complementary_favourable_range` double DEFAULT NULL,
  `coverage_surface_area` double DEFAULT NULL,
  `percentage_coverage_surface_area` double DEFAULT NULL,
  `coverage_trend` varchar(1) DEFAULT NULL,
  `coverage_yearly_magnitude` double DEFAULT NULL,
  `complementary_favourable_area_q` varchar(2) DEFAULT NULL,
  `complementary_favourable_area` double DEFAULT NULL,
  `conclusion_range` varchar(3) DEFAULT NULL,
  `conclusion_area` varchar(3) DEFAULT NULL,
  `conclusion_structure` varchar(3) DEFAULT NULL,
  `conclusion_future` varchar(3) DEFAULT NULL,
  `conclusion_assessment` varchar(3) DEFAULT NULL,
  `range_quality` varchar(13) DEFAULT NULL,
  `coverage_quality` varchar(13) DEFAULT NULL,
  `complementary_other_information` text,
  `complementary_other_information_english` text,
  `range_grid_area` double DEFAULT NULL,
  `percentage_range_grid_area` double DEFAULT NULL,
  `distribution_grid_area` double DEFAULT NULL,
  `percentage_distribution_grid_area` double DEFAULT NULL,
  PRIMARY KEY (`country`,`filename`,`region`),
  KEY `group` (`group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table etc_data_hcoverage_pressures
# ------------------------------------------------------------

CREATE TABLE `etc_data_hcoverage_pressures` (
  `eu_country_code` varchar(2) NOT NULL,
  `region` varchar(4) NOT NULL,
  `habitatcode` varchar(4) NOT NULL DEFAULT '0',
  `pressure` varchar(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`eu_country_code`,`region`,`habitatcode`,`pressure`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table etc_data_hcoverage_threats
# ------------------------------------------------------------

CREATE TABLE `etc_data_hcoverage_threats` (
  `eu_country_code` varchar(2) NOT NULL,
  `region` varchar(4) NOT NULL,
  `habitatcode` varchar(4) NOT NULL DEFAULT '0',
  `threat` varchar(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`eu_country_code`,`region`,`habitatcode`,`threat`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table etc_data_species_automatic_assessment
# ------------------------------------------------------------

CREATE TABLE `etc_data_species_automatic_assessment` (
  `assessment_method` varchar(3) NOT NULL,
  `order` int(11) DEFAULT NULL,
  `assesment_speciesname` varchar(60) NOT NULL,
  `region` varchar(4) NOT NULL,
  `range_surface_area` varchar(100) DEFAULT NULL,
  `percentage_range_surface_area` varchar(100) DEFAULT NULL,
  `range_trend` varchar(100) DEFAULT NULL,
  `range_yearly_magnitude` varchar(100) DEFAULT NULL,
  `complementary_favourable_range` varchar(100) DEFAULT NULL,
  `population_size` varchar(100) DEFAULT NULL,
  `percentage_population_mean_size` varchar(100) DEFAULT NULL,
  `population_trend` varchar(100) DEFAULT NULL,
  `population_yearly_magnitude` varchar(100) DEFAULT NULL,
  `complementary_favourable_population` varchar(100) DEFAULT NULL,
  `habitat_surface_area` varchar(100) DEFAULT NULL,
  `percentage_habitat_surface_area` varchar(100) DEFAULT NULL,
  `habitat_trend` varchar(100) DEFAULT NULL,
  `complementary_suitable_habitat` varchar(100) DEFAULT NULL,
  `percentage_future` varchar(100) DEFAULT NULL,
  `conclusion_range` varchar(3) DEFAULT NULL,
  `conclusion_range_gis` varchar(3) DEFAULT NULL,
  `conclusion_population` varchar(3) DEFAULT NULL,
  `conclusion_population_gis` varchar(3) DEFAULT NULL,
  `conclusion_habitat` varchar(3) DEFAULT NULL,
  `conclusion_habitat_gis` varchar(3) DEFAULT NULL,
  `conclusion_future` varchar(3) DEFAULT NULL,
  `percentage_assessment` varchar(100) DEFAULT NULL,
  `conclusion_assessment` varchar(3) DEFAULT NULL,
  `range_grid_area` varchar(100) DEFAULT NULL,
  `percentage_range_grid_area` varchar(100) DEFAULT NULL,
  `distribution_grid_area` varchar(100) DEFAULT NULL,
  `percentage_distribution_grid_area` varchar(100) DEFAULT NULL,
  `assessment_needed` int(11) DEFAULT NULL,
  PRIMARY KEY (`assessment_method`,`assesment_speciesname`,`region`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table etc_data_species_regions
# ------------------------------------------------------------

CREATE TABLE `etc_data_species_regions` (
  `country` varchar(3) NOT NULL,
  `eu_country_code` varchar(2) NOT NULL,
  `delivery` tinyint(1) NOT NULL,
  `envelope` varchar(50) NOT NULL,
  `filename` varchar(60) NOT NULL,
  `region` varchar(4) NOT NULL,
  `region_ms` varchar(4) DEFAULT NULL,
  `region_was_changed` tinyint(1) DEFAULT NULL,
  `group` varchar(21) DEFAULT NULL,
  `tax_group` varchar(20) DEFAULT NULL,
  `tax_order` int(11) DEFAULT NULL,
  `upper_group` varchar(30) DEFAULT NULL,
  `mid_group` varchar(20) DEFAULT NULL,
  `family` varchar(30) DEFAULT NULL,
  `annex` varchar(11) DEFAULT NULL,
  `annex_II` varchar(2) DEFAULT NULL,
  `annex_II_exception` int(11) DEFAULT NULL,
  `priority` varchar(1) DEFAULT NULL,
  `annex_IV` varchar(2) DEFAULT NULL,
  `annex_IV_exception` int(11) DEFAULT NULL,
  `annex_V` varchar(1) DEFAULT NULL,
  `annex_V_addition` int(11) DEFAULT NULL,
  `code` varchar(50) DEFAULT NULL,
  `speciescode` varchar(32) DEFAULT NULL,
  `speciesname` varchar(50) DEFAULT NULL,
  `species_name_different` tinyint(1) DEFAULT NULL,
  `eunis_species_code` int(20) DEFAULT NULL,
  `valid_speciesname` varchar(50) DEFAULT NULL,
  `n2000_species_code` int(11) DEFAULT NULL,
  `assesment_speciesname` varchar(60) DEFAULT NULL,
  `assesment_speciesname_changed` tinyint(1) DEFAULT NULL,
  `grouped_assesment` tinyint(1) DEFAULT NULL,
  `species_type` varchar(5) DEFAULT NULL,
  `species_type_asses` tinyint(1) DEFAULT NULL,
  `range_surface_area` double DEFAULT NULL,
  `percentage_range_surface_area` double DEFAULT NULL,
  `range_trend` varchar(1) DEFAULT NULL,
  `range_yearly_magnitude` double DEFAULT NULL,
  `complementary_favourable_range_q` varchar(2) DEFAULT NULL,
  `complementary_favourable_range` double DEFAULT NULL,
  `population_minimum_size` double DEFAULT NULL,
  `percentage_population_minimum_size` double DEFAULT NULL,
  `population_maximum_size` double DEFAULT NULL,
  `percentage_population_maximum_size` double DEFAULT NULL,
  `filled_population` varchar(3) DEFAULT NULL,
  `population_size_unit` varchar(6) DEFAULT NULL,
  `number_of_different_population_units` int(2) DEFAULT NULL,
  `different_population_percentage` tinyint(1) DEFAULT NULL,
  `percentage_population_mean_size` double DEFAULT NULL,
  `population_trend` varchar(1) DEFAULT NULL,
  `population_yearly_magnitude` double DEFAULT NULL,
  `complementary_favourable_population_q` varchar(2) DEFAULT NULL,
  `complementary_favourable_population` double DEFAULT NULL,
  `filled_complementary_favourable_population` varchar(3) DEFAULT NULL,
  `habitat_surface_area` double DEFAULT NULL,
  `percentage_habitat_surface_area` double DEFAULT NULL,
  `habitat_trend` varchar(1) DEFAULT NULL,
  `complementary_suitable_habitat` double DEFAULT NULL,
  `future_prospects` varchar(4) DEFAULT NULL,
  `conclusion_range` varchar(3) DEFAULT NULL,
  `conclusion_population` varchar(3) DEFAULT NULL,
  `conclusion_habitat` varchar(3) DEFAULT NULL,
  `conclusion_future` varchar(3) DEFAULT NULL,
  `conclusion_assessment` varchar(3) DEFAULT NULL,
  `range_quality` varchar(13) DEFAULT NULL,
  `population_quality` varchar(13) DEFAULT NULL,
  `habitat_quality` varchar(13) DEFAULT NULL,
  `complementary_other_information` text,
  `complementary_other_information_english` text,
  `range_grid_area` double DEFAULT NULL,
  `percentage_range_grid_area` double DEFAULT NULL,
  `distribution_grid_area` double DEFAULT NULL,
  `percentage_distribution_grid_area` double DEFAULT NULL,
  PRIMARY KEY (`country`,`filename`,`region`),
  KEY `group` (`group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table etc_data_spopulation_pressures
# ------------------------------------------------------------

CREATE TABLE `etc_data_spopulation_pressures` (
  `eu_country_code` varchar(2) NOT NULL,
  `region` varchar(4) NOT NULL,
  `n2000_species_code` int(11) NOT NULL DEFAULT '0',
  `assesment_speciesname` varchar(60) NOT NULL,
  `pressure` varchar(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`eu_country_code`,`region`,`n2000_species_code`,`pressure`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table etc_data_spopulation_threats
# ------------------------------------------------------------

CREATE TABLE `etc_data_spopulation_threats` (
  `eu_country_code` varchar(2) NOT NULL,
  `region` varchar(4) NOT NULL,
  `n2000_species_code` int(11) NOT NULL DEFAULT '0',
  `assesment_speciesname` varchar(60) NOT NULL,
  `threat` varchar(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`eu_country_code`,`region`,`n2000_species_code`,`threat`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table etc_dic_biogeoreg
# ------------------------------------------------------------

CREATE TABLE `etc_dic_biogeoreg` (
  `reg_code` varchar(4) NOT NULL,
  `reg_name` varchar(60) DEFAULT NULL,
  `ordine` int(11) DEFAULT NULL,
  `order` int(11) DEFAULT NULL,
  PRIMARY KEY (`reg_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table etc_dic_conclusion
# ------------------------------------------------------------

CREATE TABLE `etc_dic_conclusion` (
  `order` tinyint(4) DEFAULT NULL,
  `conclusion` varchar(3) NOT NULL,
  `details` varchar(90) DEFAULT NULL,
  PRIMARY KEY (`conclusion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table etc_dic_decision
# ------------------------------------------------------------

CREATE TABLE `etc_dic_decision` (
  `order` tinyint(4) DEFAULT NULL,
  `decision` varchar(4) NOT NULL,
  `details` varchar(70) DEFAULT NULL,
  PRIMARY KEY (`decision`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table etc_dic_hd_habitats
# ------------------------------------------------------------

CREATE TABLE `etc_dic_hd_habitats` (
  `habcode` varchar(4) NOT NULL DEFAULT '',
  `group` varchar(40) DEFAULT NULL,
  `priority` int(11) NOT NULL,
  `name` varchar(155) NOT NULL,
  `shortname` varchar(70) DEFAULT NULL,
  `annex_I_comments` varchar(30) DEFAULT NULL,
  `marine` int(11) DEFAULT NULL,
  PRIMARY KEY (`habcode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table etc_dic_method
# ------------------------------------------------------------

CREATE TABLE `etc_dic_method` (
  `order` tinyint(4) DEFAULT NULL,
  `method` varchar(3) NOT NULL,
  `details` varchar(125) DEFAULT NULL,
  PRIMARY KEY (`method`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table etc_dic_population_units
# ------------------------------------------------------------

CREATE TABLE `etc_dic_population_units` (
  `order` tinyint(4) DEFAULT NULL,
  `population_units` varchar(6) NOT NULL,
  `details` varchar(40) DEFAULT NULL,
  `code` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`population_units`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table etc_dic_species_type
# ------------------------------------------------------------

CREATE TABLE `etc_dic_species_type` (
  `SpeciesTypeID` int(11) NOT NULL,
  `SpeciesType` varchar(50) DEFAULT NULL,
  `Assesment` varchar(50) DEFAULT NULL,
  `Note` varchar(255) DEFAULT NULL,
  `abbrev` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`SpeciesTypeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table etc_dic_trend
# ------------------------------------------------------------

CREATE TABLE `etc_dic_trend` (
  `id` tinyint(4) NOT NULL,
  `trend` varchar(3) DEFAULT NULL,
  `details` varchar(125) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table etc_qa_errors_habitattype_manual_checked
# ------------------------------------------------------------

CREATE TABLE `etc_qa_errors_habitattype_manual_checked` (
  `country` varchar(3) NOT NULL,
  `eu_country_code` varchar(2) DEFAULT NULL,
  `filename` varchar(60) NOT NULL,
  `region` varchar(4) NOT NULL,
  `habitatcode` varchar(50) DEFAULT NULL,
  `suspect_value` varchar(150) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `error_code` int(11) NOT NULL,
  `error_description` text,
  `FlagField` varchar(40) DEFAULT NULL,
  `FlagText` varchar(65) DEFAULT NULL,
  PRIMARY KEY (`country`,`filename`,`region`,`error_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table etc_qa_errors_species_manual_checked
# ------------------------------------------------------------

CREATE TABLE `etc_qa_errors_species_manual_checked` (
  `country` varchar(3) NOT NULL,
  `eu_country_code` varchar(2) DEFAULT NULL,
  `filename` varchar(60) NOT NULL,
  `region` varchar(4) NOT NULL,
  `assesment_speciesname` varchar(60) DEFAULT NULL,
  `suspect_value` varchar(150) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `error_code` int(11) NOT NULL,
  `error_description` text,
  `FlagField` varchar(40) DEFAULT NULL,
  `FlagText` varchar(65) DEFAULT NULL,
  PRIMARY KEY (`country`,`filename`,`region`,`error_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table habitat_comments
# ------------------------------------------------------------

CREATE TABLE `habitat_comments` (
  `id` int(11) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `region` varchar(4) NOT NULL,
  `habitat` varchar(50) NOT NULL,
  `user` varchar(25) NOT NULL,
  `MS` varchar(4) NOT NULL DEFAULT 'EU25',
  `comment` longtext,
  `author` varchar(25) NOT NULL,
  `post_date` varchar(16) NOT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table habitat_comments_read
# ------------------------------------------------------------

CREATE TABLE `habitat_comments_read` (
  `id_comment` int(11) unsigned zerofill NOT NULL,
  `reader_user_id` varchar(25) NOT NULL,
  KEY `id_comment` (`id_comment`),
  CONSTRAINT `habitat_comments_read_fk` FOREIGN KEY (`id_comment`) REFERENCES `habitat_comments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table habitat_group
# ------------------------------------------------------------

CREATE TABLE `habitat_group` (
   `habitatcode` VARCHAR(4) NULL DEFAULT NULL,
   `group` VARCHAR(21) NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table habitats2eunis
# ------------------------------------------------------------

CREATE TABLE `habitats2eunis` (
  `CODE_2000` varchar(4) NOT NULL,
  `ID_HABITAT` int(11) DEFAULT NULL,
  PRIMARY KEY (`CODE_2000`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table habitattypes_manual_assessment
# ------------------------------------------------------------

CREATE TABLE `habitattypes_manual_assessment` (
  `MS` varchar(4) NOT NULL DEFAULT 'EU25',
  `region` varchar(4) NOT NULL,
  `habitatcode` varchar(50) NOT NULL,
  `range_surface_area` varchar(23) DEFAULT NULL,
  `range_trend` varchar(3) DEFAULT NULL,
  `range_yearly_magnitude` varchar(23) DEFAULT NULL,
  `complementary_favourable_range` varchar(23) DEFAULT NULL,
  `coverage_surface_area` varchar(23) DEFAULT NULL,
  `coverage_trend` varchar(3) DEFAULT NULL,
  `coverage_yearly_magnitude` varchar(23) DEFAULT NULL,
  `complementary_favourable_area` varchar(23) DEFAULT NULL,
  `method_range` varchar(3) DEFAULT NULL,
  `conclusion_range` varchar(2) DEFAULT NULL,
  `method_area` varchar(3) DEFAULT NULL,
  `conclusion_area` varchar(2) DEFAULT NULL,
  `method_structure` varchar(3) DEFAULT NULL,
  `conclusion_structure` varchar(2) DEFAULT NULL,
  `method_future` varchar(3) DEFAULT NULL,
  `conclusion_future` varchar(2) DEFAULT NULL,
  `method_assessment` varchar(3) DEFAULT NULL,
  `conclusion_assessment` varchar(2) DEFAULT NULL,
  `user` varchar(25) NOT NULL DEFAULT '',
  `last_update` varchar(16) DEFAULT NULL,
  `deleted_record` tinyint(1) DEFAULT NULL,
  `decision` varchar(3) DEFAULT NULL,
  `user_decision` varchar(25) DEFAULT NULL,
  `last_update_decision` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`region`,`habitatcode`,`user`,`MS`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table lu_hd_habitats
# ------------------------------------------------------------

CREATE TABLE `lu_hd_habitats` (
  `habcode` varchar(4) NOT NULL DEFAULT '',
  `group` varchar(40) DEFAULT NULL,
  `priority` int(11) NOT NULL,
  `name` varchar(155) NOT NULL,
  `annex_I_comments` varchar(30) DEFAULT NULL,
  `marine` int(11) DEFAULT NULL,
  PRIMARY KEY (`habcode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table photo_habitats
# ------------------------------------------------------------

CREATE TABLE `photo_habitats` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `habitatcode` varchar(4) NOT NULL DEFAULT '',
  `description` varchar(4096) DEFAULT NULL,
  `photographer` varchar(64) DEFAULT NULL,
  `location` varchar(64) DEFAULT NULL,
  `content_type` varchar(32) DEFAULT NULL,
  `picture_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `picture_data` mediumblob,
  `thumbnail` mediumblob,
  `user` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `habitatcode` (`habitatcode`),
  KEY `user` (`user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='InnoDB free: 4096 kB; (`assesment_speciesname`) REFER `artic';



# Dump of table photo_species
# ------------------------------------------------------------

CREATE TABLE `photo_species` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `assessment_speciesname` varchar(60) NOT NULL DEFAULT '',
  `description` varchar(255) DEFAULT NULL,
  `photographer` varchar(64) DEFAULT NULL,
  `location` varchar(64) DEFAULT NULL,
  `karma` tinyint(4) unsigned NOT NULL DEFAULT '0',
  `content_type` varchar(32) DEFAULT NULL,
  `picture_date` datetime DEFAULT NULL,
  `picture_data` blob,
  `thumbnail` blob,
  `user` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `assessment_speciesname` (`assessment_speciesname`),
  KEY `user` (`user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table registered_users
# ------------------------------------------------------------

CREATE TABLE `registered_users` (
  `user` varchar(50) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `institution` varchar(45) DEFAULT NULL,
  `abbrev` varchar(10) DEFAULT NULL,
  `MS` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `qualification` varchar(255) DEFAULT NULL,
  `account_date` varchar(16) NOT NULL,
  `show_assessment` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table restricted_habitats
# ------------------------------------------------------------

CREATE TABLE `restricted_habitats` (
  `habitatcode` varchar(4) DEFAULT NULL,
  `eu_country_code` varchar(2) NOT NULL DEFAULT '',
  `show_data` smallint(1) unsigned DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table restricted_species
# ------------------------------------------------------------

CREATE TABLE `restricted_species` (
  `assesment_speciesname` varchar(60) NOT NULL DEFAULT '',
  `eu_country_code` varchar(2) NOT NULL DEFAULT '',
  `show_data` smallint(1) unsigned DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table species_group
# ------------------------------------------------------------

CREATE TABLE `species_group` (
   `assesment_speciesname` VARCHAR(60) NULL DEFAULT NULL,
   `group` VARCHAR(21) NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table species_manual_assessment
# ------------------------------------------------------------

CREATE TABLE `species_manual_assessment` (
  `MS` varchar(4) NOT NULL DEFAULT 'EU25',
  `region` varchar(4) NOT NULL,
  `assesment_speciesname` varchar(60) NOT NULL,
  `range_surface_area` varchar(23) DEFAULT NULL,
  `range_trend` varchar(3) DEFAULT NULL,
  `range_yearly_magnitude` varchar(23) DEFAULT NULL,
  `complementary_favourable_range` varchar(23) DEFAULT NULL,
  `population_size` varchar(23) DEFAULT NULL,
  `population_size_unit` varchar(6) DEFAULT NULL,
  `population_trend` varchar(3) DEFAULT NULL,
  `population_yearly_magnitude` varchar(23) DEFAULT NULL,
  `complementary_favourable_population` varchar(23) DEFAULT NULL,
  `habitat_surface_area` varchar(23) DEFAULT NULL,
  `habitat_trend` varchar(3) DEFAULT NULL,
  `complementary_suitable_habitat` varchar(23) DEFAULT NULL,
  `method_range` varchar(3) DEFAULT NULL,
  `conclusion_range` varchar(2) DEFAULT NULL,
  `method_population` varchar(3) DEFAULT NULL,
  `conclusion_population` varchar(2) DEFAULT NULL,
  `method_habitat` varchar(3) DEFAULT NULL,
  `conclusion_habitat` varchar(2) DEFAULT NULL,
  `method_future` varchar(3) DEFAULT NULL,
  `conclusion_future` varchar(2) DEFAULT NULL,
  `method_assessment` varchar(3) DEFAULT NULL,
  `conclusion_assessment` varchar(2) DEFAULT NULL,
  `user` varchar(25) NOT NULL DEFAULT '',
  `last_update` varchar(16) DEFAULT NULL,
  `deleted_record` tinyint(1) DEFAULT NULL,
  `decision` varchar(3) DEFAULT NULL,
  `user_decision` varchar(25) DEFAULT NULL,
  `last_update_decision` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`region`,`assesment_speciesname`,`user`,`MS`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table species_name
# ------------------------------------------------------------

CREATE TABLE `species_name` (
   `priority` VARCHAR(1) NULL DEFAULT NULL,
   `assesment_speciesname` VARCHAR(60) NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table wiki
# ------------------------------------------------------------

CREATE TABLE `wiki` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `region` varchar(4) NOT NULL,
  `assesment_speciesname` varchar(60) DEFAULT NULL,
  `habitatcode` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table wiki_changes
# ------------------------------------------------------------

CREATE TABLE `wiki_changes` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `wiki_id` int(11) NOT NULL,
  `body` varchar(6000) DEFAULT NULL,
  `editor` varchar(60) NOT NULL,
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `active` tinyint(1) unsigned zerofill DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `id` (`wiki_id`),
  CONSTRAINT `wiki_changes_fk` FOREIGN KEY (`wiki_id`) REFERENCES `wiki` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table wiki_comments
# ------------------------------------------------------------

CREATE TABLE `wiki_comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `wiki_id` int(11) NOT NULL,
  `comment` longtext NOT NULL,
  `author` varchar(60) NOT NULL,
  `deleted` tinyint(1) unsigned zerofill DEFAULT NULL,
  `posted` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `wiki_id` (`wiki_id`),
  CONSTRAINT `wiki_comments_fk1` FOREIGN KEY (`wiki_id`) REFERENCES `wiki` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table wiki_comments_read
# ------------------------------------------------------------

CREATE TABLE `wiki_comments_read` (
  `comment_id` int(11) DEFAULT NULL,
  `reader_id` varchar(60) DEFAULT NULL,
  KEY `comment_id` (`comment_id`),
  CONSTRAINT `wiki_comments_read_fk` FOREIGN KEY (`comment_id`) REFERENCES `wiki_comments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table wiki_trail
# ------------------------------------------------------------

CREATE TABLE `wiki_trail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `region` varchar(4) NOT NULL,
  `assesment_speciesname` varchar(60) DEFAULT NULL,
  `habitatcode` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table wiki_trail_changes
# ------------------------------------------------------------

CREATE TABLE `wiki_trail_changes` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `wiki_id` int(11) NOT NULL,
  `body` varchar(6000) DEFAULT NULL,
  `editor` varchar(60) NOT NULL,
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `active` tinyint(1) unsigned zerofill DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `id` (`wiki_id`),
  CONSTRAINT `wiki_trail_changes_fk` FOREIGN KEY (`wiki_id`) REFERENCES `wiki_trail` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table wiki_trail_comments
# ------------------------------------------------------------

CREATE TABLE `wiki_trail_comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `wiki_id` int(11) NOT NULL,
  `comment` longtext NOT NULL,
  `author` varchar(60) NOT NULL,
  `deleted` tinyint(1) unsigned zerofill DEFAULT NULL,
  `posted` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `wiki_id` (`wiki_id`),
  CONSTRAINT `wiki_trail_comments_fk1` FOREIGN KEY (`wiki_id`) REFERENCES `wiki_trail` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;



# Dump of table wiki_trail_comments_read
# ------------------------------------------------------------

CREATE TABLE `wiki_trail_comments_read` (
  `comment_id` int(11) DEFAULT NULL,
  `reader_id` varchar(60) DEFAULT NULL,
  KEY `comment_id` (`comment_id`),
  CONSTRAINT `wiki_trail_comments_read_fk` FOREIGN KEY (`comment_id`) REFERENCES `wiki_trail_comments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;





# Replace placeholder table for habitat_group with correct view syntax
# ------------------------------------------------------------

DROP TABLE `habitat_group`;

CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `habitat_group`
AS SELECT
   distinct sql_no_cache `etc_data_habitattype_regions`.`habitatcode` AS `habitatcode`,
   `etc_data_habitattype_regions`.`group` AS `group`
FROM `etc_data_habitattype_regions`;


# Replace placeholder table for species_group with correct view syntax
# ------------------------------------------------------------

DROP TABLE `species_group`;

CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `species_group`
AS SELECT
   distinct `etc_data_species_regions`.`assesment_speciesname` AS `assesment_speciesname`,
   `etc_data_species_regions`.`group` AS `group`
FROM `etc_data_species_regions`;


# Replace placeholder table for species_name with correct view syntax
# ------------------------------------------------------------

DROP TABLE `species_name`;

CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `species_name`
AS SELECT
   `etc_data_species_regions`.`priority` AS `priority`,
   `etc_data_species_regions`.`assesment_speciesname` AS `assesment_speciesname`
FROM `etc_data_species_regions`;

/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
