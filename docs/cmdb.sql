-- MySQL dump 10.13  Distrib 5.7.18, for macos10.12 (x86_64)
--
-- Host: 127.0.0.1    Database: cmdb
-- ------------------------------------------------------
-- Server version	5.7.36-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `acl_apps`
--

DROP TABLE IF EXISTS `acl_apps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acl_apps` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8_unicode_ci,
  `app_id` text COLLATE utf8_unicode_ci,
  `secret_key` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `ix_acl_apps_name` (`name`),
  KEY `ix_acl_apps_deleted` (`deleted`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acl_apps`
--

LOCK TABLES `acl_apps` WRITE;
/*!40000 ALTER TABLE `acl_apps` DISABLE KEYS */;
INSERT INTO `acl_apps` VALUES (NULL,0,NULL,'2021-11-24 13:21:18',1,'acl','ACL',NULL,NULL),(NULL,0,NULL,NULL,2,'cmdb',NULL,NULL,NULL),(NULL,0,'2023-06-01 14:28:20',NULL,9,'backend','backend','73027543764f4b558f7c07e990bbf45e','ldEOLD*q4TxoeS6zh%Hp?8wtG0^9VJmZ');
/*!40000 ALTER TABLE `acl_apps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `acl_audit_permission_logs`
--

DROP TABLE IF EXISTS `acl_audit_permission_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acl_audit_permission_logs` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_id` int(11) DEFAULT NULL,
  `operate_uid` int(11) DEFAULT NULL COMMENT '操作人uid',
  `operate_type` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '操作类型',
  `rid` int(11) DEFAULT NULL COMMENT '角色id',
  `resource_type_id` int(11) DEFAULT NULL COMMENT '资源类型id',
  `resource_ids` json DEFAULT NULL COMMENT '资源',
  `group_ids` json DEFAULT NULL COMMENT '资源组',
  `permission_ids` json DEFAULT NULL COMMENT '权限',
  `source` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '来源',
  PRIMARY KEY (`id`),
  KEY `ix_acl_audit_permission_logs_deleted` (`deleted`),
  KEY `ix_acl_audit_permission_logs_rid` (`rid`),
  KEY `ix_acl_audit_permission_logs_app_id` (`app_id`),
  KEY `ix_acl_audit_permission_logs_operate_uid` (`operate_uid`),
  KEY `ix_acl_audit_permission_logs_resource_type_id` (`resource_type_id`),
  KEY `ix_acl_audit_permission_logs_operate_type` (`operate_type`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acl_audit_permission_logs`
--

LOCK TABLES `acl_audit_permission_logs` WRITE;
/*!40000 ALTER TABLE `acl_audit_permission_logs` DISABLE KEYS */;
INSERT INTO `acl_audit_permission_logs` VALUES (NULL,0,'2023-07-11 16:55:04',NULL,1,2,1,'grant',57,1,'[1]','[]','[1, 2, 3, 4, 5]','acl'),(NULL,0,'2023-07-11 16:55:04',NULL,2,2,1,'grant',57,1,'[2]','[]','[1, 2, 3, 4, 5]','acl'),(NULL,0,'2023-07-11 16:55:04',NULL,3,2,1,'grant',57,1,'[3]','[]','[1, 2, 3, 4, 5]','acl'),(NULL,0,'2023-07-11 16:55:04',NULL,4,2,1,'grant',57,1,'[4]','[]','[1, 2, 3, 4, 5]','acl'),(NULL,0,'2023-07-11 16:55:05',NULL,5,2,1,'grant',57,1,'[5]','[]','[1, 2, 3, 4, 5]','acl'),(NULL,0,'2023-07-11 16:55:05',NULL,6,2,1,'grant',57,1,'[6]','[]','[1, 2, 3, 4, 5]','acl'),(NULL,0,'2023-07-11 16:55:05',NULL,7,2,1,'grant',57,1,'[7]','[]','[1, 2, 3, 4, 5]','acl'),(NULL,0,'2023-07-11 16:55:05',NULL,8,2,1,'grant',57,1,'[8]','[]','[1, 2, 3, 4, 5]','acl'),(NULL,0,'2023-07-11 16:55:05',NULL,9,2,1,'grant',57,1,'[9]','[]','[1, 2, 3, 4, 5]','acl'),(NULL,0,'2023-07-11 16:55:05',NULL,10,2,1,'grant',57,1,'[10]','[]','[1, 2, 3, 4, 5]','acl'),(NULL,0,'2023-07-11 16:55:05',NULL,11,2,1,'grant',57,1,'[11]','[]','[1, 2, 3, 4, 5]','acl'),(NULL,0,'2023-07-11 16:55:05',NULL,12,2,1,'grant',57,1,'[12]','[]','[1, 2, 3, 4, 5]','acl'),(NULL,0,'2023-07-11 16:55:05',NULL,13,2,1,'grant',57,1,'[13]','[]','[1, 2, 3, 4, 5]','acl'),(NULL,0,'2023-07-11 16:55:05',NULL,14,2,1,'grant',57,1,'[14]','[]','[1, 2, 3, 4, 5]','acl'),(NULL,0,'2023-07-11 16:55:05',NULL,15,2,1,'grant',57,1,'[15]','[]','[1, 2, 3, 4, 5]','acl'),(NULL,0,'2023-07-11 16:55:05',NULL,16,2,1,'grant',57,1,'[16]','[]','[1, 2, 3, 4, 5]','acl'),(NULL,0,'2023-07-11 16:55:05',NULL,17,2,1,'grant',57,1,'[17]','[]','[1, 2, 3, 4, 5]','acl'),(NULL,0,'2023-07-11 16:55:06',NULL,18,2,1,'grant',57,1,'[18]','[]','[1, 2, 3, 4, 5]','acl'),(NULL,0,'2023-07-11 16:55:06',NULL,19,2,1,'grant',57,1,'[19]','[]','[1, 2, 3, 4, 5]','acl'),(NULL,0,'2023-07-11 16:56:51',NULL,20,2,1,'grant',2,1,'[1]','[]','[1, 2, 3, 4, 5, 6]','acl'),(NULL,0,'2023-07-11 16:56:51',NULL,21,2,1,'grant',2,1,'[2]','[]','[1, 2, 3, 4, 5, 6]','acl'),(NULL,0,'2023-07-11 16:56:51',NULL,22,2,1,'grant',2,1,'[3]','[]','[1, 2, 3, 4, 5, 6]','acl'),(NULL,0,'2023-07-11 16:56:51',NULL,23,2,1,'grant',2,1,'[4]','[]','[1, 2, 3, 4, 5, 6]','acl'),(NULL,0,'2023-07-11 16:56:51',NULL,24,2,1,'grant',2,1,'[5]','[]','[1, 2, 3, 4, 5, 6]','acl'),(NULL,0,'2023-07-11 16:56:52',NULL,25,2,1,'grant',2,1,'[6]','[]','[1, 2, 3, 4, 5, 6]','acl'),(NULL,0,'2023-07-11 16:56:52',NULL,26,2,1,'grant',2,1,'[7]','[]','[1, 2, 3, 4, 5, 6]','acl'),(NULL,0,'2023-07-11 16:56:52',NULL,27,2,1,'grant',2,1,'[8]','[]','[1, 2, 3, 4, 5, 6]','acl'),(NULL,0,'2023-07-11 16:56:52',NULL,28,2,1,'grant',2,1,'[9]','[]','[1, 2, 3, 4, 5, 6]','acl'),(NULL,0,'2023-07-11 16:56:52',NULL,29,2,1,'grant',2,1,'[10]','[]','[1, 2, 3, 4, 5, 6]','acl'),(NULL,0,'2023-07-11 16:56:52',NULL,30,2,1,'grant',2,1,'[11]','[]','[1, 2, 3, 4, 5, 6]','acl'),(NULL,0,'2023-07-11 16:56:52',NULL,31,2,1,'grant',2,1,'[12]','[]','[1, 2, 3, 4, 5, 6]','acl'),(NULL,0,'2023-07-11 16:56:52',NULL,32,2,1,'grant',2,1,'[13]','[]','[1, 2, 3, 4, 5, 6]','acl'),(NULL,0,'2023-07-11 16:56:52',NULL,33,2,1,'grant',2,1,'[14]','[]','[1, 2, 3, 4, 5, 6]','acl'),(NULL,0,'2023-07-11 16:56:52',NULL,34,2,1,'grant',2,1,'[15]','[]','[1, 2, 3, 4, 5, 6]','acl'),(NULL,0,'2023-07-11 16:56:52',NULL,35,2,1,'grant',2,1,'[16]','[]','[1, 2, 3, 4, 5, 6]','acl'),(NULL,0,'2023-07-11 16:56:53',NULL,36,2,1,'grant',2,1,'[17]','[]','[1, 2, 3, 4, 5, 6]','acl'),(NULL,0,'2023-07-11 16:56:53',NULL,37,2,1,'grant',2,1,'[18]','[]','[1, 2, 3, 4, 5, 6]','acl'),(NULL,0,'2023-07-11 16:56:53',NULL,38,2,1,'grant',2,1,'[19]','[]','[1, 2, 3, 4, 5, 6]','acl'),(NULL,0,'2023-07-11 16:56:53',NULL,39,2,1,'grant',2,1,'[20]','[]','[1, 2, 3, 4, 5, 6]','acl'),(NULL,0,'2023-07-11 16:59:34',NULL,40,2,1,'grant',2,10,'[23]','[]','[12, 13, 14]','acl'),(NULL,0,'2023-07-11 16:59:44',NULL,41,2,1,'grant',2,10,'[24]','[]','[12, 13, 14]','acl'),(NULL,0,'2023-07-11 16:59:55',NULL,42,2,1,'grant',2,10,'[25]','[]','[12, 13, 14]','acl'),(NULL,0,'2023-07-11 17:00:16',NULL,43,2,1,'grant',2,10,'[26]','[]','[12, 13, 14]','acl'),(NULL,0,'2023-07-11 17:00:26',NULL,44,2,1,'grant',2,10,'[27]','[]','[12, 13, 14]','acl'),(NULL,0,'2023-07-11 17:00:34',NULL,45,2,1,'grant',2,10,'[28]','[]','[12, 13, 14]','acl'),(NULL,0,'2023-07-11 17:03:45',NULL,46,2,1,'grant',57,10,'[21]','[]','[12, 13]','acl'),(NULL,0,'2023-07-11 17:03:45',NULL,47,2,1,'grant',2,10,'[21]','[]','[12, 13]','acl'),(NULL,0,'2023-07-11 17:03:45',NULL,48,2,1,'grant',57,10,'[22]','[]','[12, 13]','acl'),(NULL,0,'2023-07-11 17:03:45',NULL,49,2,1,'grant',2,10,'[22]','[]','[12, 13]','acl'),(NULL,0,'2023-07-11 17:03:45',NULL,50,2,1,'grant',57,10,'[23]','[]','[12, 13]','acl'),(NULL,0,'2023-07-11 17:03:45',NULL,51,2,1,'grant',57,10,'[24]','[]','[12, 13]','acl'),(NULL,0,'2023-07-11 17:03:45',NULL,52,2,1,'grant',57,10,'[25]','[]','[12, 13]','acl'),(NULL,0,'2023-07-11 17:03:45',NULL,53,2,1,'grant',57,10,'[26]','[]','[12, 13]','acl'),(NULL,0,'2023-07-11 17:03:45',NULL,54,2,1,'grant',57,10,'[27]','[]','[12, 13]','acl'),(NULL,0,'2023-07-11 17:03:45',NULL,55,2,1,'grant',57,10,'[28]','[]','[12, 13]','acl');
/*!40000 ALTER TABLE `acl_audit_permission_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `acl_audit_resource_logs`
--

DROP TABLE IF EXISTS `acl_audit_resource_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acl_audit_resource_logs` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_id` int(11) DEFAULT NULL,
  `operate_uid` int(11) DEFAULT NULL COMMENT '操作人uid',
  `operate_type` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '操作类型',
  `scope` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '范围',
  `link_id` int(11) DEFAULT NULL COMMENT '资源名',
  `origin` json DEFAULT NULL COMMENT '原始数据',
  `current` json DEFAULT NULL COMMENT '当前数据',
  `extra` json DEFAULT NULL COMMENT '权限名',
  `source` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '来源',
  PRIMARY KEY (`id`),
  KEY `ix_acl_audit_resource_logs_operate_uid` (`operate_uid`),
  KEY `ix_acl_audit_resource_logs_operate_type` (`operate_type`),
  KEY `ix_acl_audit_resource_logs_deleted` (`deleted`),
  KEY `ix_acl_audit_resource_logs_app_id` (`app_id`),
  KEY `ix_acl_audit_resource_logs_link_id` (`link_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acl_audit_resource_logs`
--

LOCK TABLES `acl_audit_resource_logs` WRITE;
/*!40000 ALTER TABLE `acl_audit_resource_logs` DISABLE KEYS */;
INSERT INTO `acl_audit_resource_logs` VALUES (NULL,0,'2023-07-11 16:50:51',NULL,1,2,1,'create','resource',10,'{}','{\"id\": 10, \"uid\": 1, \"name\": \"switch\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-07-11 16:50:51\", \"deleted_at\": null, \"updated_at\": null, \"resource_type_id\": 1}','{}','acl'),(NULL,0,'2023-07-11 16:51:17',NULL,2,2,1,'create','resource',11,'{}','{\"id\": 11, \"uid\": 1, \"name\": \"router\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-07-11 16:51:17\", \"deleted_at\": null, \"updated_at\": null, \"resource_type_id\": 1}','{}','acl'),(NULL,0,'2023-07-11 16:51:23',NULL,3,2,1,'create','resource',12,'{}','{\"id\": 12, \"uid\": 1, \"name\": \"firewall\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-07-11 16:51:23\", \"deleted_at\": null, \"updated_at\": null, \"resource_type_id\": 1}','{}','acl'),(NULL,0,'2023-07-11 16:51:29',NULL,4,2,1,'create','resource',13,'{}','{\"id\": 13, \"uid\": 1, \"name\": \"load_balance\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-07-11 16:51:29\", \"deleted_at\": null, \"updated_at\": null, \"resource_type_id\": 1}','{}','acl'),(NULL,0,'2023-07-11 16:51:34',NULL,5,2,1,'create','resource',14,'{}','{\"id\": 14, \"uid\": 1, \"name\": \"mysql\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-07-11 16:51:34\", \"deleted_at\": null, \"updated_at\": null, \"resource_type_id\": 1}','{}','acl'),(NULL,0,'2023-07-11 16:51:39',NULL,6,2,1,'create','resource',15,'{}','{\"id\": 15, \"uid\": 1, \"name\": \"postgresql\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-07-11 16:51:39\", \"deleted_at\": null, \"updated_at\": null, \"resource_type_id\": 1}','{}','acl'),(NULL,0,'2023-07-11 16:51:50',NULL,7,2,1,'create','resource',16,'{}','{\"id\": 16, \"uid\": 1, \"name\": \"mongodb\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-07-11 16:51:50\", \"deleted_at\": null, \"updated_at\": null, \"resource_type_id\": 1}','{}','acl'),(NULL,0,'2023-07-11 16:51:56',NULL,8,2,1,'create','resource',17,'{}','{\"id\": 17, \"uid\": 1, \"name\": \"mssql\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-07-11 16:51:56\", \"deleted_at\": null, \"updated_at\": null, \"resource_type_id\": 1}','{}','acl'),(NULL,0,'2023-07-11 16:52:01',NULL,9,2,1,'create','resource',18,'{}','{\"id\": 18, \"uid\": 1, \"name\": \"nginx\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-07-11 16:52:01\", \"deleted_at\": null, \"updated_at\": null, \"resource_type_id\": 1}','{}','acl'),(NULL,0,'2023-07-11 16:52:07',NULL,10,2,1,'create','resource',19,'{}','{\"id\": 19, \"uid\": 1, \"name\": \"apache\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-07-11 16:52:07\", \"deleted_at\": null, \"updated_at\": null, \"resource_type_id\": 1}','{}','acl'),(NULL,0,'2023-07-11 16:52:12',NULL,11,2,1,'create','resource',20,'{}','{\"id\": 20, \"uid\": 1, \"name\": \"tomcat\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-07-11 16:52:12\", \"deleted_at\": null, \"updated_at\": null, \"resource_type_id\": 1}','{}','acl'),(NULL,0,'2023-07-11 16:54:04',NULL,12,2,1,'update','resource_type',1,'{\"id\": 1, \"name\": \"CIType\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2021-11-23 19:52:22\", \"deleted_at\": null, \"updated_at\": \"2022-10-28 17:55:15\", \"description\": \"数据模型\"}','{\"id\": 1, \"name\": \"CIType\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2021-11-23 19:52:22\", \"deleted_at\": null, \"updated_at\": \"2022-10-28 17:55:15\", \"description\": \"数据模型\"}','{\"permission_ids\": {\"origin\": [], \"current\": [1, 2, 3, 4, 5, 6]}}','acl'),(NULL,0,'2023-07-11 16:54:23',NULL,13,2,1,'update','resource_type',2,'{\"id\": 2, \"name\": \"RelationView\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2021-11-23 19:52:56\", \"deleted_at\": null, \"updated_at\": null, \"description\": \"关系视图\"}','{\"id\": 2, \"name\": \"RelationView\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2021-11-23 19:52:56\", \"deleted_at\": null, \"updated_at\": null, \"description\": \"关系视图\"}','{\"permission_ids\": {\"origin\": [], \"current\": [7, 8, 9, 10, 11]}}','acl'),(NULL,0,'2023-07-11 16:54:36',NULL,14,2,1,'update','resource_type',10,'{\"id\": 10, \"name\": \"CITypeRelation\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2022-10-17 16:50:42\", \"deleted_at\": null, \"updated_at\": \"2022-10-28 17:55:29\", \"description\": \"模型关联\"}','{\"id\": 10, \"name\": \"CITypeRelation\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2022-10-17 16:50:42\", \"deleted_at\": null, \"updated_at\": \"2022-10-28 17:55:29\", \"description\": \"模型关联\"}','{\"permission_ids\": {\"origin\": [], \"current\": [12, 13, 14]}}','acl'),(NULL,0,'2023-07-11 16:54:43',NULL,15,2,1,'update','resource_type',21,'{\"id\": 21, \"name\": \"CIFilter\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-05-23 15:17:22\", \"deleted_at\": null, \"updated_at\": null, \"description\": \"\"}','{\"id\": 21, \"name\": \"CIFilter\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-05-23 15:17:22\", \"deleted_at\": null, \"updated_at\": null, \"description\": \"\"}','{\"permission_ids\": {\"origin\": [], \"current\": [15]}}','acl'),(NULL,0,'2023-07-11 16:57:17',NULL,16,2,1,'create','resource',21,'{}','{\"id\": 21, \"uid\": 1, \"name\": \"bu -> product\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-07-11 16:57:17\", \"deleted_at\": null, \"updated_at\": null, \"resource_type_id\": 10}','{}','acl'),(NULL,0,'2023-07-11 16:58:34',NULL,17,2,1,'create','resource',22,'{}','{\"id\": 22, \"uid\": 1, \"name\": \"product -> project\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-07-11 16:58:34\", \"deleted_at\": null, \"updated_at\": null, \"resource_type_id\": 10}','{}','acl'),(NULL,0,'2023-07-11 16:59:34',NULL,18,2,1,'create','resource',23,'{}','{\"id\": 23, \"uid\": 1, \"name\": \"project -> server\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-07-11 16:59:34\", \"deleted_at\": null, \"updated_at\": null, \"resource_type_id\": 10}','{}','acl'),(NULL,0,'2023-07-11 16:59:43',NULL,19,2,1,'create','resource',24,'{}','{\"id\": 24, \"uid\": 1, \"name\": \"project -> vserver\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-07-11 16:59:43\", \"deleted_at\": null, \"updated_at\": null, \"resource_type_id\": 10}','{}','acl'),(NULL,0,'2023-07-11 16:59:55',NULL,20,2,1,'create','resource',25,'{}','{\"id\": 25, \"uid\": 1, \"name\": \"project -> docker\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-07-11 16:59:55\", \"deleted_at\": null, \"updated_at\": null, \"resource_type_id\": 10}','{}','acl'),(NULL,0,'2023-07-11 17:00:16',NULL,21,2,1,'create','resource',26,'{}','{\"id\": 26, \"uid\": 1, \"name\": \"server -> RAM\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-07-11 17:00:16\", \"deleted_at\": null, \"updated_at\": null, \"resource_type_id\": 10}','{}','acl'),(NULL,0,'2023-07-11 17:00:25',NULL,22,2,1,'create','resource',27,'{}','{\"id\": 27, \"uid\": 1, \"name\": \"server -> harddisk\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-07-11 17:00:25\", \"deleted_at\": null, \"updated_at\": null, \"resource_type_id\": 10}','{}','acl'),(NULL,0,'2023-07-11 17:00:33',NULL,23,2,1,'create','resource',28,'{}','{\"id\": 28, \"uid\": 1, \"name\": \"server -> NIC\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-07-11 17:00:33\", \"deleted_at\": null, \"updated_at\": null, \"resource_type_id\": 10}','{}','acl');
/*!40000 ALTER TABLE `acl_audit_resource_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `acl_audit_role_logs`
--

DROP TABLE IF EXISTS `acl_audit_role_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acl_audit_role_logs` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_id` int(11) DEFAULT NULL,
  `operate_uid` int(11) DEFAULT NULL COMMENT '操作人uid',
  `operate_type` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '操作类型',
  `scope` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '范围',
  `link_id` int(11) DEFAULT NULL COMMENT '资源id',
  `origin` json DEFAULT NULL COMMENT '原始数据',
  `current` json DEFAULT NULL COMMENT '当前数据',
  `extra` json DEFAULT NULL COMMENT '其他内容',
  `source` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '来源',
  PRIMARY KEY (`id`),
  KEY `ix_acl_audit_role_logs_app_id` (`app_id`),
  KEY `ix_acl_audit_role_logs_link_id` (`link_id`),
  KEY `ix_acl_audit_role_logs_operate_type` (`operate_type`),
  KEY `ix_acl_audit_role_logs_deleted` (`deleted`),
  KEY `ix_acl_audit_role_logs_operate_uid` (`operate_uid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acl_audit_role_logs`
--

LOCK TABLES `acl_audit_role_logs` WRITE;
/*!40000 ALTER TABLE `acl_audit_role_logs` DISABLE KEYS */;
INSERT INTO `acl_audit_role_logs` VALUES (NULL,0,'2023-07-11 16:59:05',NULL,1,2,1,'create','role',58,'{}','{\"id\": 58, \"key\": \"3000e19614174743ab5011dba42b215b\", \"uid\": null, \"name\": \"CMDB_READ_ALL\", \"app_id\": 2, \"deleted\": false, \"created_at\": \"2023-07-11 16:59:05\", \"deleted_at\": null, \"updated_at\": null, \"is_app_admin\": false}','{}','acl');
/*!40000 ALTER TABLE `acl_audit_role_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `acl_audit_trigger_logs`
--

DROP TABLE IF EXISTS `acl_audit_trigger_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acl_audit_trigger_logs` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_id` int(11) DEFAULT NULL,
  `trigger_id` int(11) DEFAULT NULL COMMENT 'trigger',
  `operate_uid` int(11) DEFAULT NULL COMMENT '操作人uid',
  `operate_type` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '操作类型',
  `origin` json DEFAULT NULL COMMENT '原始数据',
  `current` json DEFAULT NULL COMMENT '当前数据',
  `extra` json DEFAULT NULL COMMENT '权限名',
  `source` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '来源',
  PRIMARY KEY (`id`),
  KEY `ix_acl_audit_trigger_logs_operate_type` (`operate_type`),
  KEY `ix_acl_audit_trigger_logs_deleted` (`deleted`),
  KEY `ix_acl_audit_trigger_logs_trigger_id` (`trigger_id`),
  KEY `ix_acl_audit_trigger_logs_operate_uid` (`operate_uid`),
  KEY `ix_acl_audit_trigger_logs_app_id` (`app_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acl_audit_trigger_logs`
--

LOCK TABLES `acl_audit_trigger_logs` WRITE;
/*!40000 ALTER TABLE `acl_audit_trigger_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `acl_audit_trigger_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `acl_operation_records`
--

DROP TABLE IF EXISTS `acl_operation_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acl_operation_records` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `rolename` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `operate` enum('2','4','1','3','0') COLLATE utf8_unicode_ci NOT NULL,
  `obj` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_acl_operation_records_rolename` (`rolename`),
  KEY `ix_acl_operation_records_app` (`app`),
  KEY `ix_acl_operation_records_deleted` (`deleted`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acl_operation_records`
--


--
-- Table structure for table `acl_permissions`
--

DROP TABLE IF EXISTS `acl_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acl_permissions` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `resource_type_id` int(11) DEFAULT NULL,
  `app_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `resource_type_id` (`resource_type_id`),
  KEY `app_id` (`app_id`),
  KEY `ix_acl_permissions_deleted` (`deleted`),
  CONSTRAINT `acl_permissions_ibfk_1` FOREIGN KEY (`resource_type_id`) REFERENCES `acl_resource_types` (`id`),
  CONSTRAINT `acl_permissions_ibfk_2` FOREIGN KEY (`app_id`) REFERENCES `acl_apps` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acl_permissions`
--

LOCK TABLES `acl_permissions` WRITE;
/*!40000 ALTER TABLE `acl_permissions` DISABLE KEYS */;
INSERT INTO `acl_permissions` VALUES (NULL,0,'2023-07-11 16:54:04',NULL,1,'create',1,2),(NULL,0,'2023-07-11 16:54:04',NULL,2,'update',1,2),(NULL,0,'2023-07-11 16:54:04',NULL,3,'delete',1,2),(NULL,0,'2023-07-11 16:54:04',NULL,4,'read',1,2),(NULL,0,'2023-07-11 16:54:04',NULL,5,'config',1,2),(NULL,0,'2023-07-11 16:54:04',NULL,6,'grant',1,2),(NULL,0,'2023-07-11 16:54:23',NULL,7,'add',2,2),(NULL,0,'2023-07-11 16:54:23',NULL,8,'update',2,2),(NULL,0,'2023-07-11 16:54:23',NULL,9,'read',2,2),(NULL,0,'2023-07-11 16:54:23',NULL,10,'delete',2,2),(NULL,0,'2023-07-11 16:54:23',NULL,11,'grant',2,2),(NULL,0,'2023-07-11 16:54:36',NULL,12,'create',10,2),(NULL,0,'2023-07-11 16:54:36',NULL,13,'delete',10,2),(NULL,0,'2023-07-11 16:54:36',NULL,14,'grant',10,2),(NULL,0,'2023-07-11 16:54:43',NULL,15,'read',21,2);
/*!40000 ALTER TABLE `acl_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `acl_resource_group_items`
--

DROP TABLE IF EXISTS `acl_resource_group_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acl_resource_group_items` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `resource_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `group_id` (`group_id`),
  KEY `resource_id` (`resource_id`),
  KEY `ix_acl_resource_group_items_deleted` (`deleted`),
  CONSTRAINT `acl_resource_group_items_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `acl_resource_groups` (`id`),
  CONSTRAINT `acl_resource_group_items_ibfk_2` FOREIGN KEY (`resource_id`) REFERENCES `acl_resources` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acl_resource_group_items`
--

LOCK TABLES `acl_resource_group_items` WRITE;
/*!40000 ALTER TABLE `acl_resource_group_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `acl_resource_group_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `acl_resource_groups`
--

DROP TABLE IF EXISTS `acl_resource_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acl_resource_groups` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `resource_type_id` int(11) DEFAULT NULL,
  `uid` int(11) DEFAULT NULL,
  `app_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `resource_type_id` (`resource_type_id`),
  KEY `app_id` (`app_id`),
  KEY `ix_acl_resource_groups_name` (`name`),
  KEY `ix_acl_resource_groups_deleted` (`deleted`),
  KEY `ix_acl_resource_groups_uid` (`uid`),
  CONSTRAINT `acl_resource_groups_ibfk_1` FOREIGN KEY (`resource_type_id`) REFERENCES `acl_resource_types` (`id`),
  CONSTRAINT `acl_resource_groups_ibfk_2` FOREIGN KEY (`app_id`) REFERENCES `acl_apps` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acl_resource_groups`
--

LOCK TABLES `acl_resource_groups` WRITE;
/*!40000 ALTER TABLE `acl_resource_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `acl_resource_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `acl_resource_types`
--

DROP TABLE IF EXISTS `acl_resource_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acl_resource_types` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8_unicode_ci,
  `app_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `app_id` (`app_id`),
  KEY `ix_acl_resource_types_deleted` (`deleted`),
  KEY `ix_acl_resource_types_name` (`name`),
  CONSTRAINT `acl_resource_types_ibfk_1` FOREIGN KEY (`app_id`) REFERENCES `acl_apps` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acl_resource_types`
--

LOCK TABLES `acl_resource_types` WRITE;
/*!40000 ALTER TABLE `acl_resource_types` DISABLE KEYS */;
INSERT INTO `acl_resource_types` VALUES (NULL,0,'2021-11-23 19:52:22','2022-10-28 17:55:15',1,'CIType','数据模型',2),(NULL,0,'2021-11-23 19:52:56',NULL,2,'RelationView','关系视图',2),(NULL,0,'2022-10-17 16:50:42','2022-10-28 17:55:29',10,'CITypeRelation','模型关联',2),(NULL,0,'2023-05-23 15:17:22',NULL,21,'CIFilter','',2),(NULL,0,'2023-06-01 14:28:20',NULL,23,'操作权限','',9);
/*!40000 ALTER TABLE `acl_resource_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `acl_resources`
--

DROP TABLE IF EXISTS `acl_resources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acl_resources` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `resource_type_id` int(11) DEFAULT NULL,
  `uid` int(11) DEFAULT NULL,
  `app_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `resource_type_id` (`resource_type_id`),
  KEY `app_id` (`app_id`),
  KEY `ix_acl_resources_deleted` (`deleted`),
  KEY `ix_acl_resources_uid` (`uid`),
  CONSTRAINT `acl_resources_ibfk_1` FOREIGN KEY (`resource_type_id`) REFERENCES `acl_resource_types` (`id`),
  CONSTRAINT `acl_resources_ibfk_2` FOREIGN KEY (`app_id`) REFERENCES `acl_apps` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acl_resources`
--

LOCK TABLES `acl_resources` WRITE;
/*!40000 ALTER TABLE `acl_resources` DISABLE KEYS */;
INSERT INTO `acl_resources` VALUES (NULL,0,'2021-11-23 19:53:22',NULL,1,'bu',1,NULL,2),(NULL,0,'2021-11-23 19:56:40',NULL,2,'product',1,1,2),(NULL,0,'2021-11-23 19:58:15',NULL,3,'project',1,1,2),(NULL,0,'2021-11-23 20:06:53',NULL,4,'server',1,1,2),(NULL,0,'2021-11-23 20:08:52',NULL,5,'vserver',1,1,2),(NULL,0,'2021-11-23 20:36:55',NULL,6,'RAM',1,1,2),(NULL,0,'2021-11-23 21:38:17',NULL,7,'harddisk',1,1,2),(NULL,0,'2021-11-24 09:42:55',NULL,8,'NIC',1,1,2),(NULL,0,'2021-11-24 09:45:10',NULL,9,'docker',1,1,2),(NULL,0,'2023-07-11 16:50:51',NULL,10,'switch',1,1,2),(NULL,0,'2023-07-11 16:51:17',NULL,11,'router',1,1,2),(NULL,0,'2023-07-11 16:51:23',NULL,12,'firewall',1,1,2),(NULL,0,'2023-07-11 16:51:29',NULL,13,'load_balance',1,1,2),(NULL,0,'2023-07-11 16:51:34',NULL,14,'mysql',1,1,2),(NULL,0,'2023-07-11 16:51:39',NULL,15,'postgresql',1,1,2),(NULL,0,'2023-07-11 16:51:50',NULL,16,'mongodb',1,1,2),(NULL,0,'2023-07-11 16:51:56',NULL,17,'mssql',1,1,2),(NULL,0,'2023-07-11 16:52:01',NULL,18,'nginx',1,1,2),(NULL,0,'2023-07-11 16:52:07',NULL,19,'apache',1,1,2),(NULL,0,'2023-07-11 16:52:12',NULL,20,'tomcat',1,1,2),(NULL,0,'2023-07-11 16:57:17',NULL,21,'bu -> product',10,1,2),(NULL,0,'2023-07-11 16:58:34',NULL,22,'product -> project',10,1,2),(NULL,0,'2023-07-11 16:59:34',NULL,23,'project -> server',10,1,2),(NULL,0,'2023-07-11 16:59:43',NULL,24,'project -> vserver',10,1,2),(NULL,0,'2023-07-11 16:59:55',NULL,25,'project -> docker',10,1,2),(NULL,0,'2023-07-11 17:00:16',NULL,26,'server -> RAM',10,1,2),(NULL,0,'2023-07-11 17:00:25',NULL,27,'server -> harddisk',10,1,2),(NULL,0,'2023-07-11 17:00:33',NULL,28,'server -> NIC',10,1,2);
/*!40000 ALTER TABLE `acl_resources` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `acl_role_permissions`
--

DROP TABLE IF EXISTS `acl_role_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acl_role_permissions` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rid` int(11) DEFAULT NULL,
  `resource_id` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  `perm_id` int(11) DEFAULT NULL,
  `app_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `rid` (`rid`),
  KEY `resource_id` (`resource_id`),
  KEY `group_id` (`group_id`),
  KEY `perm_id` (`perm_id`),
  KEY `app_id` (`app_id`),
  KEY `ix_acl_role_permissions_deleted` (`deleted`),
  CONSTRAINT `acl_role_permissions_ibfk_1` FOREIGN KEY (`rid`) REFERENCES `acl_roles` (`id`),
  CONSTRAINT `acl_role_permissions_ibfk_2` FOREIGN KEY (`resource_id`) REFERENCES `acl_resources` (`id`),
  CONSTRAINT `acl_role_permissions_ibfk_3` FOREIGN KEY (`group_id`) REFERENCES `acl_resource_groups` (`id`),
  CONSTRAINT `acl_role_permissions_ibfk_4` FOREIGN KEY (`perm_id`) REFERENCES `acl_permissions` (`id`),
  CONSTRAINT `acl_role_permissions_ibfk_5` FOREIGN KEY (`app_id`) REFERENCES `acl_apps` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=260 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acl_role_permissions`
--

LOCK TABLES `acl_role_permissions` WRITE;
/*!40000 ALTER TABLE `acl_role_permissions` DISABLE KEYS */;
INSERT INTO `acl_role_permissions` VALUES (NULL,0,'2023-07-11 16:55:04',NULL,1,57,1,NULL,1,2),(NULL,0,'2023-07-11 16:55:04',NULL,2,57,1,NULL,4,2),(NULL,0,'2023-07-11 16:55:04',NULL,3,57,1,NULL,3,2),(NULL,0,'2023-07-11 16:55:04',NULL,4,57,1,NULL,2,2),(NULL,0,'2023-07-11 16:55:04',NULL,5,57,1,NULL,5,2),(NULL,0,'2023-07-11 16:55:04',NULL,6,57,2,NULL,1,2),(NULL,0,'2023-07-11 16:55:04',NULL,7,57,2,NULL,4,2),(NULL,0,'2023-07-11 16:55:04',NULL,8,57,2,NULL,3,2),(NULL,0,'2023-07-11 16:55:04',NULL,9,57,2,NULL,2,2),(NULL,0,'2023-07-11 16:55:04',NULL,10,57,2,NULL,5,2),(NULL,0,'2023-07-11 16:55:04',NULL,11,57,3,NULL,1,2),(NULL,0,'2023-07-11 16:55:04',NULL,12,57,3,NULL,4,2),(NULL,0,'2023-07-11 16:55:04',NULL,13,57,3,NULL,3,2),(NULL,0,'2023-07-11 16:55:04',NULL,14,57,3,NULL,2,2),(NULL,0,'2023-07-11 16:55:04',NULL,15,57,3,NULL,5,2),(NULL,0,'2023-07-11 16:55:04',NULL,16,57,4,NULL,1,2),(NULL,0,'2023-07-11 16:55:04',NULL,17,57,4,NULL,4,2),(NULL,0,'2023-07-11 16:55:04',NULL,18,57,4,NULL,3,2),(NULL,0,'2023-07-11 16:55:04',NULL,19,57,4,NULL,2,2),(NULL,0,'2023-07-11 16:55:04',NULL,20,57,4,NULL,5,2),(NULL,0,'2023-07-11 16:55:05',NULL,21,57,5,NULL,1,2),(NULL,0,'2023-07-11 16:55:05',NULL,22,57,5,NULL,4,2),(NULL,0,'2023-07-11 16:55:05',NULL,23,57,5,NULL,3,2),(NULL,0,'2023-07-11 16:55:05',NULL,24,57,5,NULL,2,2),(NULL,0,'2023-07-11 16:55:05',NULL,25,57,5,NULL,5,2),(NULL,0,'2023-07-11 16:55:05',NULL,26,57,6,NULL,1,2),(NULL,0,'2023-07-11 16:55:05',NULL,27,57,6,NULL,4,2),(NULL,0,'2023-07-11 16:55:05',NULL,28,57,6,NULL,3,2),(NULL,0,'2023-07-11 16:55:05',NULL,29,57,6,NULL,2,2),(NULL,0,'2023-07-11 16:55:05',NULL,30,57,6,NULL,5,2),(NULL,0,'2023-07-11 16:55:05',NULL,31,57,7,NULL,1,2),(NULL,0,'2023-07-11 16:55:05',NULL,32,57,7,NULL,4,2),(NULL,0,'2023-07-11 16:55:05',NULL,33,57,7,NULL,3,2),(NULL,0,'2023-07-11 16:55:05',NULL,34,57,7,NULL,2,2),(NULL,0,'2023-07-11 16:55:05',NULL,35,57,7,NULL,5,2),(NULL,0,'2023-07-11 16:55:05',NULL,36,57,8,NULL,1,2),(NULL,0,'2023-07-11 16:55:05',NULL,37,57,8,NULL,4,2),(NULL,0,'2023-07-11 16:55:05',NULL,38,57,8,NULL,3,2),(NULL,0,'2023-07-11 16:55:05',NULL,39,57,8,NULL,2,2),(NULL,0,'2023-07-11 16:55:05',NULL,40,57,8,NULL,5,2),(NULL,0,'2023-07-11 16:55:05',NULL,41,57,9,NULL,1,2),(NULL,0,'2023-07-11 16:55:05',NULL,42,57,9,NULL,4,2),(NULL,0,'2023-07-11 16:55:05',NULL,43,57,9,NULL,3,2),(NULL,0,'2023-07-11 16:55:05',NULL,44,57,9,NULL,2,2),(NULL,0,'2023-07-11 16:55:05',NULL,45,57,9,NULL,5,2),(NULL,0,'2023-07-11 16:55:05',NULL,46,57,10,NULL,1,2),(NULL,0,'2023-07-11 16:55:05',NULL,47,57,10,NULL,4,2),(NULL,0,'2023-07-11 16:55:05',NULL,48,57,10,NULL,3,2),(NULL,0,'2023-07-11 16:55:05',NULL,49,57,10,NULL,2,2),(NULL,0,'2023-07-11 16:55:05',NULL,50,57,10,NULL,5,2),(NULL,0,'2023-07-11 16:55:05',NULL,51,57,11,NULL,1,2),(NULL,0,'2023-07-11 16:55:05',NULL,52,57,11,NULL,4,2),(NULL,0,'2023-07-11 16:55:05',NULL,53,57,11,NULL,3,2),(NULL,0,'2023-07-11 16:55:05',NULL,54,57,11,NULL,2,2),(NULL,0,'2023-07-11 16:55:05',NULL,55,57,11,NULL,5,2),(NULL,0,'2023-07-11 16:55:05',NULL,56,57,12,NULL,1,2),(NULL,0,'2023-07-11 16:55:05',NULL,57,57,12,NULL,4,2),(NULL,0,'2023-07-11 16:55:05',NULL,58,57,12,NULL,3,2),(NULL,0,'2023-07-11 16:55:05',NULL,59,57,12,NULL,2,2),(NULL,0,'2023-07-11 16:55:05',NULL,60,57,12,NULL,5,2),(NULL,0,'2023-07-11 16:55:05',NULL,61,57,13,NULL,1,2),(NULL,0,'2023-07-11 16:55:05',NULL,62,57,13,NULL,4,2),(NULL,0,'2023-07-11 16:55:05',NULL,63,57,13,NULL,3,2),(NULL,0,'2023-07-11 16:55:05',NULL,64,57,13,NULL,2,2),(NULL,0,'2023-07-11 16:55:05',NULL,65,57,13,NULL,5,2),(NULL,0,'2023-07-11 16:55:05',NULL,66,57,14,NULL,1,2),(NULL,0,'2023-07-11 16:55:05',NULL,67,57,14,NULL,4,2),(NULL,0,'2023-07-11 16:55:05',NULL,68,57,14,NULL,3,2),(NULL,0,'2023-07-11 16:55:05',NULL,69,57,14,NULL,2,2),(NULL,0,'2023-07-11 16:55:05',NULL,70,57,14,NULL,5,2),(NULL,0,'2023-07-11 16:55:05',NULL,71,57,15,NULL,1,2),(NULL,0,'2023-07-11 16:55:05',NULL,72,57,15,NULL,4,2),(NULL,0,'2023-07-11 16:55:05',NULL,73,57,15,NULL,3,2),(NULL,0,'2023-07-11 16:55:05',NULL,74,57,15,NULL,2,2),(NULL,0,'2023-07-11 16:55:05',NULL,75,57,15,NULL,5,2),(NULL,0,'2023-07-11 16:55:05',NULL,76,57,16,NULL,1,2),(NULL,0,'2023-07-11 16:55:05',NULL,77,57,16,NULL,4,2),(NULL,0,'2023-07-11 16:55:05',NULL,78,57,16,NULL,3,2),(NULL,0,'2023-07-11 16:55:05',NULL,79,57,16,NULL,2,2),(NULL,0,'2023-07-11 16:55:05',NULL,80,57,16,NULL,5,2),(NULL,0,'2023-07-11 16:55:05',NULL,81,57,17,NULL,1,2),(NULL,0,'2023-07-11 16:55:05',NULL,82,57,17,NULL,4,2),(NULL,0,'2023-07-11 16:55:05',NULL,83,57,17,NULL,3,2),(NULL,0,'2023-07-11 16:55:05',NULL,84,57,17,NULL,2,2),(NULL,0,'2023-07-11 16:55:05',NULL,85,57,17,NULL,5,2),(NULL,0,'2023-07-11 16:55:05',NULL,86,57,18,NULL,1,2),(NULL,0,'2023-07-11 16:55:05',NULL,87,57,18,NULL,4,2),(NULL,0,'2023-07-11 16:55:06',NULL,88,57,18,NULL,3,2),(NULL,0,'2023-07-11 16:55:06',NULL,89,57,18,NULL,2,2),(NULL,0,'2023-07-11 16:55:06',NULL,90,57,18,NULL,5,2),(NULL,0,'2023-07-11 16:55:06',NULL,91,57,19,NULL,1,2),(NULL,0,'2023-07-11 16:55:06',NULL,92,57,19,NULL,4,2),(NULL,0,'2023-07-11 16:55:06',NULL,93,57,19,NULL,3,2),(NULL,0,'2023-07-11 16:55:06',NULL,94,57,19,NULL,2,2),(NULL,0,'2023-07-11 16:55:06',NULL,95,57,19,NULL,5,2),(NULL,0,'2023-07-11 16:55:06',NULL,96,57,20,NULL,1,2),(NULL,0,'2023-07-11 16:55:06',NULL,97,57,20,NULL,4,2),(NULL,0,'2023-07-11 16:55:06',NULL,98,57,20,NULL,3,2),(NULL,0,'2023-07-11 16:55:06',NULL,99,57,20,NULL,2,2),(NULL,0,'2023-07-11 16:55:06',NULL,100,57,20,NULL,5,2),(NULL,0,'2023-07-11 16:56:51',NULL,101,2,1,NULL,2,2),(NULL,0,'2023-07-11 16:56:51',NULL,102,2,1,NULL,5,2),(NULL,0,'2023-07-11 16:56:51',NULL,103,2,1,NULL,6,2),(NULL,0,'2023-07-11 16:56:51',NULL,104,2,1,NULL,3,2),(NULL,0,'2023-07-11 16:56:51',NULL,105,2,1,NULL,1,2),(NULL,0,'2023-07-11 16:56:51',NULL,106,2,1,NULL,4,2),(NULL,0,'2023-07-11 16:56:51',NULL,107,2,2,NULL,2,2),(NULL,0,'2023-07-11 16:56:51',NULL,108,2,2,NULL,5,2),(NULL,0,'2023-07-11 16:56:51',NULL,109,2,2,NULL,6,2),(NULL,0,'2023-07-11 16:56:51',NULL,110,2,2,NULL,3,2),(NULL,0,'2023-07-11 16:56:51',NULL,111,2,2,NULL,1,2),(NULL,0,'2023-07-11 16:56:51',NULL,112,2,2,NULL,4,2),(NULL,0,'2023-07-11 16:56:51',NULL,113,2,3,NULL,2,2),(NULL,0,'2023-07-11 16:56:51',NULL,114,2,3,NULL,5,2),(NULL,0,'2023-07-11 16:56:51',NULL,115,2,3,NULL,6,2),(NULL,0,'2023-07-11 16:56:51',NULL,116,2,3,NULL,3,2),(NULL,0,'2023-07-11 16:56:51',NULL,117,2,3,NULL,1,2),(NULL,0,'2023-07-11 16:56:51',NULL,118,2,3,NULL,4,2),(NULL,0,'2023-07-11 16:56:51',NULL,119,2,4,NULL,2,2),(NULL,0,'2023-07-11 16:56:51',NULL,120,2,4,NULL,5,2),(NULL,0,'2023-07-11 16:56:51',NULL,121,2,4,NULL,6,2),(NULL,0,'2023-07-11 16:56:51',NULL,122,2,4,NULL,3,2),(NULL,0,'2023-07-11 16:56:51',NULL,123,2,4,NULL,1,2),(NULL,0,'2023-07-11 16:56:51',NULL,124,2,4,NULL,4,2),(NULL,0,'2023-07-11 16:56:51',NULL,125,2,5,NULL,2,2),(NULL,0,'2023-07-11 16:56:51',NULL,126,2,5,NULL,5,2),(NULL,0,'2023-07-11 16:56:51',NULL,127,2,5,NULL,6,2),(NULL,0,'2023-07-11 16:56:51',NULL,128,2,5,NULL,3,2),(NULL,0,'2023-07-11 16:56:51',NULL,129,2,5,NULL,1,2),(NULL,0,'2023-07-11 16:56:51',NULL,130,2,5,NULL,4,2),(NULL,0,'2023-07-11 16:56:51',NULL,131,2,6,NULL,2,2),(NULL,0,'2023-07-11 16:56:51',NULL,132,2,6,NULL,5,2),(NULL,0,'2023-07-11 16:56:51',NULL,133,2,6,NULL,6,2),(NULL,0,'2023-07-11 16:56:51',NULL,134,2,6,NULL,3,2),(NULL,0,'2023-07-11 16:56:52',NULL,135,2,6,NULL,1,2),(NULL,0,'2023-07-11 16:56:52',NULL,136,2,6,NULL,4,2),(NULL,0,'2023-07-11 16:56:52',NULL,137,2,7,NULL,2,2),(NULL,0,'2023-07-11 16:56:52',NULL,138,2,7,NULL,5,2),(NULL,0,'2023-07-11 16:56:52',NULL,139,2,7,NULL,6,2),(NULL,0,'2023-07-11 16:56:52',NULL,140,2,7,NULL,3,2),(NULL,0,'2023-07-11 16:56:52',NULL,141,2,7,NULL,1,2),(NULL,0,'2023-07-11 16:56:52',NULL,142,2,7,NULL,4,2),(NULL,0,'2023-07-11 16:56:52',NULL,143,2,8,NULL,2,2),(NULL,0,'2023-07-11 16:56:52',NULL,144,2,8,NULL,5,2),(NULL,0,'2023-07-11 16:56:52',NULL,145,2,8,NULL,6,2),(NULL,0,'2023-07-11 16:56:52',NULL,146,2,8,NULL,3,2),(NULL,0,'2023-07-11 16:56:52',NULL,147,2,8,NULL,1,2),(NULL,0,'2023-07-11 16:56:52',NULL,148,2,8,NULL,4,2),(NULL,0,'2023-07-11 16:56:52',NULL,149,2,9,NULL,2,2),(NULL,0,'2023-07-11 16:56:52',NULL,150,2,9,NULL,5,2),(NULL,0,'2023-07-11 16:56:52',NULL,151,2,9,NULL,6,2),(NULL,0,'2023-07-11 16:56:52',NULL,152,2,9,NULL,3,2),(NULL,0,'2023-07-11 16:56:52',NULL,153,2,9,NULL,1,2),(NULL,0,'2023-07-11 16:56:52',NULL,154,2,9,NULL,4,2),(NULL,0,'2023-07-11 16:56:52',NULL,155,2,10,NULL,2,2),(NULL,0,'2023-07-11 16:56:52',NULL,156,2,10,NULL,5,2),(NULL,0,'2023-07-11 16:56:52',NULL,157,2,10,NULL,6,2),(NULL,0,'2023-07-11 16:56:52',NULL,158,2,10,NULL,3,2),(NULL,0,'2023-07-11 16:56:52',NULL,159,2,10,NULL,1,2),(NULL,0,'2023-07-11 16:56:52',NULL,160,2,10,NULL,4,2),(NULL,0,'2023-07-11 16:56:52',NULL,161,2,11,NULL,2,2),(NULL,0,'2023-07-11 16:56:52',NULL,162,2,11,NULL,5,2),(NULL,0,'2023-07-11 16:56:52',NULL,163,2,11,NULL,6,2),(NULL,0,'2023-07-11 16:56:52',NULL,164,2,11,NULL,3,2),(NULL,0,'2023-07-11 16:56:52',NULL,165,2,11,NULL,1,2),(NULL,0,'2023-07-11 16:56:52',NULL,166,2,11,NULL,4,2),(NULL,0,'2023-07-11 16:56:52',NULL,167,2,12,NULL,2,2),(NULL,0,'2023-07-11 16:56:52',NULL,168,2,12,NULL,5,2),(NULL,0,'2023-07-11 16:56:52',NULL,169,2,12,NULL,6,2),(NULL,0,'2023-07-11 16:56:52',NULL,170,2,12,NULL,3,2),(NULL,0,'2023-07-11 16:56:52',NULL,171,2,12,NULL,1,2),(NULL,0,'2023-07-11 16:56:52',NULL,172,2,12,NULL,4,2),(NULL,0,'2023-07-11 16:56:52',NULL,173,2,13,NULL,2,2),(NULL,0,'2023-07-11 16:56:52',NULL,174,2,13,NULL,5,2),(NULL,0,'2023-07-11 16:56:52',NULL,175,2,13,NULL,6,2),(NULL,0,'2023-07-11 16:56:52',NULL,176,2,13,NULL,3,2),(NULL,0,'2023-07-11 16:56:52',NULL,177,2,13,NULL,1,2),(NULL,0,'2023-07-11 16:56:52',NULL,178,2,13,NULL,4,2),(NULL,0,'2023-07-11 16:56:52',NULL,179,2,14,NULL,2,2),(NULL,0,'2023-07-11 16:56:52',NULL,180,2,14,NULL,5,2),(NULL,0,'2023-07-11 16:56:52',NULL,181,2,14,NULL,6,2),(NULL,0,'2023-07-11 16:56:52',NULL,182,2,14,NULL,3,2),(NULL,0,'2023-07-11 16:56:52',NULL,183,2,14,NULL,1,2),(NULL,0,'2023-07-11 16:56:52',NULL,184,2,14,NULL,4,2),(NULL,0,'2023-07-11 16:56:52',NULL,185,2,15,NULL,2,2),(NULL,0,'2023-07-11 16:56:52',NULL,186,2,15,NULL,5,2),(NULL,0,'2023-07-11 16:56:52',NULL,187,2,15,NULL,6,2),(NULL,0,'2023-07-11 16:56:52',NULL,188,2,15,NULL,3,2),(NULL,0,'2023-07-11 16:56:52',NULL,189,2,15,NULL,1,2),(NULL,0,'2023-07-11 16:56:52',NULL,190,2,15,NULL,4,2),(NULL,0,'2023-07-11 16:56:52',NULL,191,2,16,NULL,2,2),(NULL,0,'2023-07-11 16:56:52',NULL,192,2,16,NULL,5,2),(NULL,0,'2023-07-11 16:56:52',NULL,193,2,16,NULL,6,2),(NULL,0,'2023-07-11 16:56:52',NULL,194,2,16,NULL,3,2),(NULL,0,'2023-07-11 16:56:52',NULL,195,2,16,NULL,1,2),(NULL,0,'2023-07-11 16:56:52',NULL,196,2,16,NULL,4,2),(NULL,0,'2023-07-11 16:56:52',NULL,197,2,17,NULL,2,2),(NULL,0,'2023-07-11 16:56:52',NULL,198,2,17,NULL,5,2),(NULL,0,'2023-07-11 16:56:52',NULL,199,2,17,NULL,6,2),(NULL,0,'2023-07-11 16:56:52',NULL,200,2,17,NULL,3,2),(NULL,0,'2023-07-11 16:56:52',NULL,201,2,17,NULL,1,2),(NULL,0,'2023-07-11 16:56:53',NULL,202,2,17,NULL,4,2),(NULL,0,'2023-07-11 16:56:53',NULL,203,2,18,NULL,2,2),(NULL,0,'2023-07-11 16:56:53',NULL,204,2,18,NULL,5,2),(NULL,0,'2023-07-11 16:56:53',NULL,205,2,18,NULL,6,2),(NULL,0,'2023-07-11 16:56:53',NULL,206,2,18,NULL,3,2),(NULL,0,'2023-07-11 16:56:53',NULL,207,2,18,NULL,1,2),(NULL,0,'2023-07-11 16:56:53',NULL,208,2,18,NULL,4,2),(NULL,0,'2023-07-11 16:56:53',NULL,209,2,19,NULL,2,2),(NULL,0,'2023-07-11 16:56:53',NULL,210,2,19,NULL,5,2),(NULL,0,'2023-07-11 16:56:53',NULL,211,2,19,NULL,6,2),(NULL,0,'2023-07-11 16:56:53',NULL,212,2,19,NULL,3,2),(NULL,0,'2023-07-11 16:56:53',NULL,213,2,19,NULL,1,2),(NULL,0,'2023-07-11 16:56:53',NULL,214,2,19,NULL,4,2),(NULL,0,'2023-07-11 16:56:53',NULL,215,2,20,NULL,2,2),(NULL,0,'2023-07-11 16:56:53',NULL,216,2,20,NULL,5,2),(NULL,0,'2023-07-11 16:56:53',NULL,217,2,20,NULL,6,2),(NULL,0,'2023-07-11 16:56:53',NULL,218,2,20,NULL,3,2),(NULL,0,'2023-07-11 16:56:53',NULL,219,2,20,NULL,1,2),(NULL,0,'2023-07-11 16:56:53',NULL,220,2,20,NULL,4,2),(NULL,0,'2023-07-11 16:59:34',NULL,221,2,23,NULL,13,2),(NULL,0,'2023-07-11 16:59:34',NULL,222,2,23,NULL,12,2),(NULL,0,'2023-07-11 16:59:34',NULL,223,2,23,NULL,14,2),(NULL,0,'2023-07-11 16:59:43',NULL,224,2,24,NULL,13,2),(NULL,0,'2023-07-11 16:59:43',NULL,225,2,24,NULL,12,2),(NULL,0,'2023-07-11 16:59:43',NULL,226,2,24,NULL,14,2),(NULL,0,'2023-07-11 16:59:55',NULL,227,2,25,NULL,13,2),(NULL,0,'2023-07-11 16:59:55',NULL,228,2,25,NULL,12,2),(NULL,0,'2023-07-11 16:59:55',NULL,229,2,25,NULL,14,2),(NULL,0,'2023-07-11 17:00:16',NULL,230,2,26,NULL,13,2),(NULL,0,'2023-07-11 17:00:16',NULL,231,2,26,NULL,12,2),(NULL,0,'2023-07-11 17:00:16',NULL,232,2,26,NULL,14,2),(NULL,0,'2023-07-11 17:00:25',NULL,233,2,27,NULL,13,2),(NULL,0,'2023-07-11 17:00:26',NULL,234,2,27,NULL,12,2),(NULL,0,'2023-07-11 17:00:26',NULL,235,2,27,NULL,14,2),(NULL,0,'2023-07-11 17:00:34',NULL,236,2,28,NULL,13,2),(NULL,0,'2023-07-11 17:00:34',NULL,237,2,28,NULL,12,2),(NULL,0,'2023-07-11 17:00:34',NULL,238,2,28,NULL,14,2),(NULL,0,'2023-07-11 17:03:45',NULL,239,57,21,NULL,13,2),(NULL,0,'2023-07-11 17:03:45',NULL,240,2,21,NULL,13,2),(NULL,0,'2023-07-11 17:03:45',NULL,241,57,21,NULL,12,2),(NULL,0,'2023-07-11 17:03:45',NULL,242,2,21,NULL,12,2),(NULL,0,'2023-07-11 17:03:45',NULL,243,57,22,NULL,13,2),(NULL,0,'2023-07-11 17:03:45',NULL,244,2,22,NULL,13,2),(NULL,0,'2023-07-11 17:03:45',NULL,245,57,22,NULL,12,2),(NULL,0,'2023-07-11 17:03:45',NULL,246,2,22,NULL,12,2),(NULL,0,'2023-07-11 17:03:45',NULL,247,57,23,NULL,13,2),(NULL,0,'2023-07-11 17:03:45',NULL,248,57,23,NULL,12,2),(NULL,0,'2023-07-11 17:03:45',NULL,249,57,24,NULL,13,2),(NULL,0,'2023-07-11 17:03:45',NULL,250,57,24,NULL,12,2),(NULL,0,'2023-07-11 17:03:45',NULL,251,57,25,NULL,13,2),(NULL,0,'2023-07-11 17:03:45',NULL,252,57,25,NULL,12,2),(NULL,0,'2023-07-11 17:03:45',NULL,253,57,26,NULL,13,2),(NULL,0,'2023-07-11 17:03:45',NULL,254,57,26,NULL,12,2),(NULL,0,'2023-07-11 17:03:45',NULL,255,57,27,NULL,13,2),(NULL,0,'2023-07-11 17:03:45',NULL,256,57,27,NULL,12,2),(NULL,0,'2023-07-11 17:03:45',NULL,257,57,28,NULL,13,2),(NULL,0,'2023-07-11 17:03:45',NULL,258,57,28,NULL,12,2),(NULL,0,'2023-07-11 18:03:41',NULL,259,58,1,NULL,4,2);
/*!40000 ALTER TABLE `acl_role_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `acl_role_relations`
--

DROP TABLE IF EXISTS `acl_role_relations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acl_role_relations` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) DEFAULT NULL,
  `child_id` int(11) DEFAULT NULL,
  `app_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `parent_id` (`parent_id`),
  KEY `child_id` (`child_id`),
  KEY `app_id` (`app_id`),
  KEY `ix_acl_role_relations_deleted` (`deleted`),
  CONSTRAINT `acl_role_relations_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `acl_roles` (`id`),
  CONSTRAINT `acl_role_relations_ibfk_2` FOREIGN KEY (`child_id`) REFERENCES `acl_roles` (`id`),
  CONSTRAINT `acl_role_relations_ibfk_3` FOREIGN KEY (`app_id`) REFERENCES `acl_apps` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acl_role_relations`
--

LOCK TABLES `acl_role_relations` WRITE;
/*!40000 ALTER TABLE `acl_role_relations` DISABLE KEYS */;
INSERT INTO `acl_role_relations` VALUES (NULL,0,NULL,NULL,1,1,2,NULL);
/*!40000 ALTER TABLE `acl_role_relations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `acl_roles`
--

DROP TABLE IF EXISTS `acl_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acl_roles` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `is_app_admin` tinyint(1) DEFAULT NULL,
  `app_id` int(11) DEFAULT NULL,
  `uid` int(11) DEFAULT NULL,
  `key` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `secret` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `password` varchar(80) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `app_id` (`app_id`),
  KEY `ix_acl_roles_deleted` (`deleted`),
  KEY `ix_acl_roles_name` (`name`),
  CONSTRAINT `acl_roles_ibfk_1` FOREIGN KEY (`app_id`) REFERENCES `acl_apps` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acl_roles`
--

LOCK TABLES `acl_roles` WRITE;
/*!40000 ALTER TABLE `acl_roles` DISABLE KEYS */;
INSERT INTO `acl_roles` VALUES (NULL,0,NULL,NULL,1,'acl_admin',1,1,NULL,'5a7154fafd7c41eaba03d2053052a0bd','IqfETBw3!nxWNay9FH#P^x34d',NULL),(NULL,0,NULL,NULL,2,'admin',0,NULL,1,NULL,NULL,NULL),(NULL,0,'2021-11-23 19:46:44',NULL,3,'cmdb_admin',1,2,NULL,NULL,NULL,NULL),(NULL,0,'2023-07-10 16:19:01',NULL,57,'demo',0,NULL,46,'a2815ab62f7a49f9b86d1ec6c475e7e6','e235V8faYsAgy#nw^xLqJKdSD$6RtZiz',NULL),(NULL,0,'2023-07-11 16:59:05',NULL,58,'CMDB_READ_ALL',0,2,NULL,'3000e19614174743ab5011dba42b215b','VBfUShHsEm@q?rZ7KtneAJ2iaN0ybj%x',NULL),(NULL,0,NULL,NULL,59,'worker',NULL,NULL,3,NULL,NULL,NULL);
/*!40000 ALTER TABLE `acl_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `acl_triggers`
--

DROP TABLE IF EXISTS `acl_triggers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acl_triggers` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `wildcard` text COLLATE utf8_unicode_ci,
  `uid` text COLLATE utf8_unicode_ci,
  `resource_type_id` int(11) DEFAULT NULL,
  `roles` text COLLATE utf8_unicode_ci,
  `permissions` text COLLATE utf8_unicode_ci,
  `enabled` tinyint(1) DEFAULT NULL,
  `app_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `resource_type_id` (`resource_type_id`),
  KEY `app_id` (`app_id`),
  KEY `ix_acl_triggers_deleted` (`deleted`),
  CONSTRAINT `acl_triggers_ibfk_1` FOREIGN KEY (`resource_type_id`) REFERENCES `acl_resource_types` (`id`),
  CONSTRAINT `acl_triggers_ibfk_2` FOREIGN KEY (`app_id`) REFERENCES `acl_apps` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acl_triggers`
--

LOCK TABLES `acl_triggers` WRITE;
/*!40000 ALTER TABLE `acl_triggers` DISABLE KEYS */;
/*!40000 ALTER TABLE `acl_triggers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_ad_ci`
--

DROP TABLE IF EXISTS `c_ad_ci`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_ad_ci` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` int(11) DEFAULT NULL,
  `adt_id` int(11) DEFAULT NULL,
  `unique_value` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `instance` json DEFAULT NULL,
  `ci_id` int(11) DEFAULT NULL,
  `is_accept` tinyint(1) DEFAULT NULL,
  `accept_by` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `accept_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `type_id` (`type_id`),
  KEY `adt_id` (`adt_id`),
  KEY `ix_c_ad_ci_accept_by` (`accept_by`),
  KEY `ix_c_ad_ci_deleted` (`deleted`),
  KEY `ix_c_ad_ci_ci_id` (`ci_id`),
  KEY `ix_c_ad_ci_unique_value` (`unique_value`),
  CONSTRAINT `c_ad_ci_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `c_ci_types` (`id`),
  CONSTRAINT `c_ad_ci_ibfk_2` FOREIGN KEY (`adt_id`) REFERENCES `c_ad_ci_types` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_ad_ci`
--

LOCK TABLES `c_ad_ci` WRITE;
/*!40000 ALTER TABLE `c_ad_ci` DISABLE KEYS */;
/*!40000 ALTER TABLE `c_ad_ci` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_ad_ci_types`
--

DROP TABLE IF EXISTS `c_ad_ci_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_ad_ci_types` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` int(11) DEFAULT NULL,
  `adr_id` int(11) DEFAULT NULL,
  `attributes` json DEFAULT NULL,
  `relation` json DEFAULT NULL,
  `auto_accept` tinyint(1) DEFAULT NULL,
  `agent_id` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `query_expr` text COLLATE utf8_unicode_ci,
  `interval` int(11) DEFAULT NULL,
  `cron` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `extra_option` json DEFAULT NULL,
  `uid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `type_id` (`type_id`),
  KEY `adr_id` (`adr_id`),
  KEY `ix_c_ad_ci_types_uid` (`uid`),
  KEY `ix_c_ad_ci_types_agent_id` (`agent_id`),
  KEY `ix_c_ad_ci_types_deleted` (`deleted`),
  CONSTRAINT `c_ad_ci_types_ibfk2` FOREIGN KEY (`adr_id`) REFERENCES `c_ad_rules` (`id`),
  CONSTRAINT `c_ad_ci_types_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `c_ci_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_ad_ci_types`
--

--
-- Table structure for table `c_ad_rules`
--

DROP TABLE IF EXISTS `c_ad_rules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_ad_rules` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `type` enum('snmp','agent','http') COLLATE utf8_unicode_ci DEFAULT NULL,
  `is_inner` tinyint(1) DEFAULT NULL,
  `owner` int(11) DEFAULT NULL,
  `option` json DEFAULT NULL,
  `attributes` json DEFAULT NULL,
  `is_plugin` tinyint(1) DEFAULT NULL,
  `plugin_script` text COLLATE utf8_unicode_ci,
  `unique_key` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_c_ad_rules_type` (`type`),
  KEY `ix_c_ad_rules_deleted` (`deleted`),
  KEY `ix_c_ad_rules_is_inner` (`is_inner`),
  KEY `ix_c_ad_rules_owner` (`owner`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_ad_rules`
--

LOCK TABLES `c_ad_rules` WRITE;
/*!40000 ALTER TABLE `c_ad_rules` DISABLE KEYS */;
INSERT INTO `c_ad_rules` VALUES (NULL,0,'2023-07-11 16:57:01',NULL,1,'阿里云','http',1,NULL,'{\"icon\": {\"name\": \"caise-aliyun\"}}',NULL,0,NULL,NULL),(NULL,0,'2023-07-11 16:57:01',NULL,2,'腾讯云','http',1,NULL,'{\"icon\": {\"name\": \"caise-tengxunyun\"}}',NULL,0,NULL,NULL),(NULL,0,'2023-07-11 16:57:01',NULL,3,'华为云','http',1,NULL,'{\"icon\": {\"name\": \"caise-huaweiyun\"}}',NULL,0,NULL,NULL),(NULL,0,'2023-07-11 16:57:01',NULL,4,'AWS','http',1,NULL,'{\"icon\": {\"name\": \"caise-aws\"}}',NULL,0,NULL,NULL),(NULL,0,'2023-07-11 16:57:01',NULL,5,'交换机','snmp',1,NULL,'{\"icon\": {\"name\": \"caise-jiaohuanji\"}}',NULL,0,NULL,NULL),(NULL,0,'2023-07-11 16:57:01',NULL,6,'路由器','snmp',1,NULL,'{\"icon\": {\"name\": \"caise-luyouqi\"}}',NULL,0,NULL,NULL),(NULL,0,'2023-07-11 16:57:01',NULL,7,'防火墙','snmp',1,NULL,'{\"icon\": {\"name\": \"caise-fanghuoqiang\"}}',NULL,0,NULL,NULL),(NULL,0,'2023-07-11 16:57:01',NULL,8,'打印机','snmp',1,NULL,'{\"icon\": {\"name\": \"caise-dayinji\"}}',NULL,0,NULL,NULL),(NULL,0,'2023-07-11 17:10:11',NULL,9,'物理机','agent',1,NULL,'{\"icon\": {\"name\": \"caise-wuliji\", \"color\": \"\"}}','[]',0,NULL,NULL),(NULL,0,'2023-07-11 17:10:22',NULL,10,'虚拟机','agent',1,NULL,'{\"icon\": {\"name\": \"caise-xuniji\", \"color\": \"\"}}','[]',0,NULL,NULL),(NULL,0,'2023-07-11 17:10:30',NULL,11,'网卡','agent',1,NULL,'{\"icon\": {\"name\": \"caise-wangka\", \"color\": \"\"}}','[]',0,NULL,NULL);
/*!40000 ALTER TABLE `c_ad_rules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_attribute_histories`
--

DROP TABLE IF EXISTS `c_attribute_histories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_attribute_histories` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `operate_type` enum('1','2','0') COLLATE utf8_unicode_ci DEFAULT NULL,
  `record_id` int(11) NOT NULL,
  `ci_id` int(11) NOT NULL,
  `attr_id` int(11) DEFAULT NULL,
  `old` text COLLATE utf8_unicode_ci,
  `new` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `record_id` (`record_id`),
  KEY `ix_c_attribute_histories_attr_id` (`attr_id`),
  KEY `ix_c_attribute_histories_ci_id` (`ci_id`),
  KEY `ix_c_attribute_histories_deleted` (`deleted`),
  CONSTRAINT `c_attribute_histories_ibfk_1` FOREIGN KEY (`record_id`) REFERENCES `c_records` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_attribute_histories`
--

LOCK TABLES `c_attribute_histories` WRITE;
/*!40000 ALTER TABLE `c_attribute_histories` DISABLE KEYS */;
INSERT INTO `c_attribute_histories` VALUES (NULL,0,'2023-07-11 17:49:51',NULL,1,'0',1,1,1,NULL,'事业部1'),(NULL,0,'2023-07-11 17:50:30',NULL,2,'0',2,2,2,NULL,'产品1'),(NULL,0,'2023-07-11 17:50:36',NULL,3,'0',3,3,3,NULL,'应用1'),(NULL,0,'2023-07-11 17:51:01',NULL,4,'0',4,4,23,NULL,'物理机1'),(NULL,0,'2023-07-11 17:51:01',NULL,5,'0',4,4,25,NULL,'192.168.2.2'),(NULL,0,'2023-07-11 17:51:01',NULL,6,'0',4,4,4,NULL,'xxxxxxx'),(NULL,0,'2023-07-11 17:51:01',NULL,7,'0',4,4,37,NULL,'2');
/*!40000 ALTER TABLE `c_attribute_histories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_attributes`
--

DROP TABLE IF EXISTS `c_attributes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_attributes` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `alias` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `value_type` enum('4','6','2','1','5','3','0') COLLATE utf8_unicode_ci NOT NULL,
  `is_choice` tinyint(1) DEFAULT NULL,
  `is_list` tinyint(1) DEFAULT NULL,
  `is_unique` tinyint(1) DEFAULT NULL,
  `is_index` tinyint(1) DEFAULT NULL,
  `uid` int(11) DEFAULT NULL,
  `is_computed` tinyint(4) DEFAULT '0',
  `is_link` tinyint(1) DEFAULT NULL,
  `choice_web_hook` json DEFAULT NULL,
  `option` json DEFAULT NULL,
  `is_password` tinyint(1) DEFAULT NULL,
  `compute_script` text COLLATE utf8_unicode_ci,
  `compute_expr` text COLLATE utf8_unicode_ci,
  `is_sortable` tinyint(1) DEFAULT NULL,
  `default` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_c_attributes_deleted` (`deleted`),
  KEY `idx_c_attributes_uid` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_attributes`
--

LOCK TABLES `c_attributes` WRITE;
/*!40000 ALTER TABLE `c_attributes` DISABLE KEYS */;
INSERT INTO `c_attributes` VALUES ('2022-12-14 19:25:41',0,'2021-11-23 19:50:29','2022-12-14 19:25:41',1,'bu_name','事业部','2',0,0,1,1,NULL,0,0,NULL,NULL,0,NULL,NULL,1,NULL),('2022-12-14 19:25:41',0,'2021-11-23 19:56:36','2022-12-14 19:25:41',2,'product_name','产品名','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,1,NULL),('2022-12-14 19:25:41',0,'2021-11-23 19:58:08','2022-12-14 19:25:41',3,'project_name','应用名','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,1,NULL),('2022-12-14 19:25:41',0,'2021-11-23 20:06:49','2022-12-14 19:25:41',4,'sn','服务器序列号','2',0,0,1,1,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-23 20:08:47','2023-02-07 13:34:19',5,'uuid','UUID','2',0,0,1,1,NULL,0,0,NULL,'{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:42',0,'2021-11-23 20:36:46','2022-12-14 19:25:42',6,'ram_sn','内存序列号','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-23 21:38:12','2022-12-14 19:25:42',7,'hd_sn','硬盘序列号','2',0,0,1,1,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 09:42:50','2022-12-14 19:25:42',8,'nic_mac','网卡MAC','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 09:45:05','2022-12-14 19:25:42',9,'instance_id','实例ID','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:41',0,'2021-11-24 10:11:38','2022-12-14 19:25:41',10,'bu_owner','BU负责人','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,1,NULL),('2022-12-14 19:25:41',0,'2021-11-24 10:12:25','2022-12-14 19:25:41',11,'bu_owner_mobile','BU负责人电话','2',0,0,0,0,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:41',0,'2021-11-24 10:12:56','2022-12-14 19:25:41',12,'bu_owner_email','BU负责人邮箱','2',0,0,0,0,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:41',0,'2021-11-24 10:19:39','2022-12-14 19:25:41',13,'product_owner','产品负责人','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,1,NULL),('2022-12-14 19:25:41',0,'2021-11-24 10:20:02','2022-12-14 19:25:41',14,'product_owner_mobile','负责人电话','2',0,0,0,0,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:41',0,'2021-11-24 10:20:23','2022-12-14 19:25:41',15,'product_owner_email','负责人邮件组','2',0,0,0,0,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:41',0,'2021-11-24 10:20:51','2022-12-14 19:25:41',16,'product_op_duty','产品线应用运维','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,1,NULL),('2022-12-14 19:25:41',0,'2021-11-24 10:22:57','2022-12-14 19:25:41',17,'project_type','应用类型','2',1,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,1,NULL),('2022-12-14 19:25:41',0,'2021-11-24 10:23:40','2022-12-14 19:25:41',18,'project_status','应用状态','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,1,NULL),('2022-12-14 19:25:41',0,'2021-11-24 10:24:01','2022-12-14 19:25:41',19,'project_description','应用描述','2',0,0,0,0,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 10:24:35','2022-12-14 19:25:42',20,'rd_duty','开发负责人','2',0,1,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,1,NULL),('2022-12-14 19:25:41',0,'2021-11-24 10:25:01','2022-12-14 19:25:41',21,'qa_duty','QA负责人','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,1,NULL),('2022-12-14 19:25:44',0,'2021-11-24 10:25:25','2023-02-07 13:56:47',22,'op_duty','运维负责人','2',0,1,0,1,NULL,0,0,NULL,'{}',0,NULL,NULL,1,'{\"default\": null}'),('2022-12-14 19:25:41',0,'2021-11-24 10:40:03','2023-03-03 17:50:36',23,'server_name','服务器名','2',0,0,0,0,NULL,0,0,NULL,'{}',0,NULL,NULL,0,'{\"default\": \"10\"}'),('2022-12-14 19:25:42',0,'2021-11-24 10:40:56','2022-12-14 19:25:42',24,'oneagent_id','AgentID','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,1,NULL),('2022-12-14 19:25:42',0,'2021-11-24 10:41:47','2023-03-03 17:53:18',25,'private_ip','内网IP','2',0,0,0,1,NULL,0,0,NULL,'{\"fontOptions\": {\"color\": \"#606266\", \"fontStyle\": \"initial\", \"fontWeight\": \"bold\", \"textDecoration\": \"initial\"}}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:42',0,'2021-11-24 10:42:29','2022-12-14 19:25:42',26,'os_version','操作系统版本','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:41',0,'2021-11-24 10:43:06','2022-12-14 19:25:41',27,'ctc_ip','电信IP','2',0,0,1,1,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:41',0,'2021-11-24 10:49:30','2022-12-14 19:25:41',28,'cnc_ip','网通IP','2',0,0,1,1,NULL,0,0,NULL,NULL,0,NULL,NULL,1,NULL),('2022-12-14 19:25:41',0,'2021-11-24 10:49:55','2022-12-14 19:25:41',29,'cmc_ip','移动IP','2',0,0,1,1,NULL,0,0,NULL,NULL,0,NULL,NULL,1,NULL),('2022-12-14 19:25:42',0,'2021-11-24 10:50:19','2022-12-14 19:25:42',30,'kernel_version','内核版本','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 10:51:20','2022-12-14 19:25:42',31,'ssh_port','SSH端口','0',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 10:59:07','2022-12-14 19:25:42',32,'bu','BU','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,1,NULL),('2022-12-14 19:25:42',0,'2021-11-24 10:59:57','2022-12-14 19:25:42',33,'perm','perm','6',0,0,0,0,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:43',0,'2021-11-24 11:01:59','2022-12-14 19:25:43',34,'status','状态','2',1,0,0,1,NULL,0,0,NULL,'{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:42',0,'2021-11-24 11:03:04','2022-12-14 19:25:42',35,'env','环境','2',1,0,0,1,NULL,0,0,NULL,'{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:42',0,'2021-11-24 11:06:00','2022-12-14 19:25:42',36,'cpu','CPU型号','2',0,0,0,1,NULL,0,0,NULL,'{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:42',0,'2021-11-24 11:06:59','2022-12-14 19:25:42',37,'cpu_count','CPU数','0',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:41',0,'2021-11-24 11:09:18','2022-12-14 19:25:41',38,'logic_cpu_count','逻辑CPU数','0',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:12:24','2022-12-14 19:25:42',39,'ram_size','内存大小','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:12:48','2022-12-14 19:25:42',40,'ram','内存信息','2',0,0,0,0,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:13:11','2022-12-14 19:25:42',41,'vnc_port','VNC端口','0',0,0,0,0,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:41',0,'2021-11-24 11:13:37','2022-12-14 19:25:41',42,'manufacturer','服务器厂家','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,1,NULL),('2022-12-14 19:25:41',0,'2021-11-24 11:13:51','2022-12-14 19:25:41',43,'device_spec','服务器型号','2',0,0,0,0,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:41',0,'2021-11-24 11:14:07','2022-12-14 19:25:41',44,'raid','RAID','2',0,0,0,0,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:41',0,'2021-11-24 11:14:31','2022-12-14 19:25:41',45,'ilo_ip','ilo卡IP','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:41',0,'2021-11-24 11:14:57','2022-12-14 19:25:41',46,'ilo_mac','ilo卡MAC地址','2',0,0,0,0,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:43',0,'2021-11-24 11:15:27','2022-12-14 19:25:43',47,'idc','IDC','2',1,0,0,1,NULL,0,0,NULL,'{}',0,NULL,NULL,1,'{\"default\": null}'),('2022-12-14 19:25:43',0,'2021-11-24 11:15:58','2022-12-14 19:25:43',48,'server_room','机房','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:16:16','2022-12-14 19:25:42',49,'rack','机架位置','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:17:18','2022-12-14 19:25:42',50,'pos','位置编号','0',0,0,0,0,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:43',0,'2021-11-24 11:18:27','2022-12-14 19:25:43',51,'buy_date','采购日期','4',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,1,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:18:50','2022-12-14 19:25:42',52,'maintain_startdate','保修开始日期','4',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,1,NULL),('2022-12-14 19:25:43',0,'2021-11-24 11:19:08','2022-12-14 19:25:43',53,'maintain_enddate','过保日期','4',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,1,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:37:12','2022-12-14 19:25:42',54,'vserver_name','虚拟机名','2',0,0,1,1,NULL,0,0,NULL,NULL,0,NULL,NULL,1,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:40:33','2022-12-14 19:25:42',55,'net_open','网络开放状态','2',1,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:43:59','2022-12-14 19:25:42',56,'vserver_type','虚拟机类型','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:44:24','2022-12-14 19:25:42',57,'host_ip','宿主机IP','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:44:54','2022-12-14 19:25:42',58,'harddisk','硬盘信息','2',0,0,0,0,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:51:56','2022-12-14 19:25:42',59,'ram_type','内存类型','2',0,0,0,0,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:52:23','2022-12-14 19:25:42',60,'ram_speed','内存速度','2',0,0,0,0,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:54:21','2022-12-14 19:25:42',61,'hd_interface_type','接口类型','2',1,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:54:42','2022-12-14 19:25:42',62,'hd_size','硬盘空间','2',0,0,0,0,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:54:59','2022-12-14 19:25:42',63,'hd_vendor','硬盘厂商','2',0,0,0,0,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:55:24','2022-12-14 19:25:42',64,'hd_speed','接口速率','2',0,0,0,0,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:58:21','2022-12-14 19:25:42',65,'nic_ip','网卡IP','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:58:42','2022-12-14 19:25:42',66,'nic_status','网卡状态','2',0,0,0,1,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:59:03','2022-12-14 19:25:42',67,'nic_type','网卡型号','2',0,0,0,0,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:59:21','2022-12-14 19:25:42',68,'nic_interface','网卡接口','2',0,0,0,0,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:42',0,'2021-11-24 11:59:51','2022-12-14 19:25:42',69,'nic_speed','网卡速率','2',0,0,0,0,NULL,0,0,NULL,NULL,0,NULL,NULL,0,NULL),('2022-12-14 19:25:41',0,'2022-11-10 10:07:59','2022-12-14 19:25:41',70,'domain','cm','2',0,0,0,0,1,0,0,'null','{\"fontOptions\": {\"color\": \"#606266\", \"fontStyle\": \"initial\", \"fontWeight\": \"bold\", \"textDecoration\": \"initial\"}}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:42',0,'2022-12-02 13:18:11','2022-12-14 19:25:42',71,'switch_sn','序列号','2',0,0,1,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:43',0,'2022-12-02 13:20:31','2022-12-14 19:25:43',72,'router_sn','序列号','2',0,0,1,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:43',0,'2022-12-02 13:21:46','2022-12-14 19:25:43',73,'firewall_sn','序列号','2',0,0,1,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:43',0,'2022-12-02 13:28:01','2023-05-23 15:24:36',74,'netdev_status','状态','2',1,0,0,1,1,0,0,'null','{}',0,NULL,NULL,1,'{\"default\": null}'),('2022-12-14 19:25:43',0,'2022-12-02 13:29:28','2022-12-14 19:25:43',75,'netdev_cost','设备成本','0',0,0,0,1,1,0,0,'null','{}',0,NULL,NULL,1,'{\"default\": null}'),('2022-12-14 19:25:43',0,'2022-12-02 13:32:06','2022-12-14 19:25:43',76,'netdev_name','设备名称','2',0,0,0,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:43',0,'2022-12-02 13:32:35','2022-12-14 19:25:43',77,'netdev_type','设备类型','2',0,0,0,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:43',0,'2022-12-02 13:35:33','2022-12-14 19:25:43',78,'netdev_manufacturer','设备厂商','0',0,0,0,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:43',0,'2022-12-02 13:45:38','2022-12-14 19:25:43',79,'manage_ip','管理IP','2',0,0,0,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:43',0,'2022-12-02 13:47:47','2022-12-14 19:25:43',80,'load_balance_sn','序列号','2',0,0,1,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:44',0,'2022-12-02 13:53:25','2022-12-14 19:25:44',81,'db_name','DB名','2',0,0,1,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:44',0,'2022-12-02 13:58:19','2022-12-14 19:25:44',82,'db_port','端口','0',0,0,0,1,1,0,0,'null','{}',0,NULL,NULL,1,'{\"default\": null}'),('2022-12-14 19:25:44',0,'2022-12-02 13:58:44','2022-12-14 19:25:44',83,'db_version','数据库版本','2',0,0,0,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:44',0,'2022-12-02 14:01:15','2022-12-14 19:25:44',84,'db_ip','IP','2',0,0,0,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:44',0,'2022-12-02 14:02:45','2022-12-14 19:25:44',85,'max_connections','最大连接数','0',0,0,0,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:43',0,'2022-12-02 14:02:59','2022-12-14 19:25:43',86,'charset','字符集','2',0,0,0,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:43',0,'2022-12-02 14:07:45','2022-12-14 19:25:43',87,'binlog_opened','binlog是否开启','2',1,0,0,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:44',0,'2022-12-02 14:10:44','2022-12-14 19:25:44',88,'cluster_role','集群角色','2',0,0,0,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:44',0,'2022-12-02 14:20:03','2022-12-14 19:25:44',89,'middleware_name','实例名','2',0,0,1,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:44',0,'2022-12-02 14:25:33','2022-12-14 19:25:44',90,'middleware_ip','IP','2',0,0,0,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:44',0,'2022-12-02 14:25:54','2022-12-14 19:25:44',91,'middleware_port','监听端口','0',0,0,0,1,1,0,0,'null','{}',0,NULL,NULL,1,'{\"default\": null}'),('2022-12-14 19:25:44',0,'2022-12-02 14:26:17','2022-12-14 19:25:44',92,'middleware_version','版本号','2',0,0,0,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:44',0,'2022-12-02 14:27:09','2022-12-14 19:25:44',93,'log_path','日志路径','2',0,0,0,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),('2022-12-14 19:25:44',0,'2022-12-02 14:29:03','2022-12-14 19:25:44',94,'domain_name','域名','2',0,0,0,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),(NULL,0,'2023-01-11 17:25:50',NULL,95,'aaa','BU负责人电话','0',0,0,0,0,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),(NULL,0,'2023-01-11 18:14:03',NULL,97,'disk_model','硬盘型号','2',1,0,0,0,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),(NULL,0,'2023-03-08 16:50:34',NULL,98,'xxx_name','xxx','2',0,0,0,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),(NULL,0,'2023-05-23 14:59:07','2023-05-23 15:19:04',99,'description','描述','2',0,0,0,0,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),(NULL,0,'2023-05-23 14:59:21',NULL,100,'ips','IPs','2',0,1,0,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": []}'),(NULL,0,'2023-05-23 15:18:21',NULL,101,'netdev_manufacturer1','设备厂商','2',0,0,0,1,1,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}'),(NULL,0,'2023-07-11 15:13:59',NULL,102,'ldap','业务aza','2',1,0,0,0,46,0,0,'null','{}',0,NULL,NULL,0,'{\"default\": null}');
/*!40000 ALTER TABLE `c_attributes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_c_d`
--

DROP TABLE IF EXISTS `c_c_d`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_c_d` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `category` smallint(6) DEFAULT NULL,
  `enabled` tinyint(1) DEFAULT NULL,
  `order` int(11) DEFAULT NULL,
  `type_id` int(11) DEFAULT NULL,
  `attr_id` int(11) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `options` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `type_id` (`type_id`),
  KEY `attr_id` (`attr_id`),
  KEY `ix_c_custom_dashboard_deleted` (`deleted`),
  CONSTRAINT `c_c_d_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `c_ci_types` (`id`),
  CONSTRAINT `c_c_d_ibfk_2` FOREIGN KEY (`attr_id`) REFERENCES `c_attributes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_c_d`
--

LOCK TABLES `c_c_d` WRITE;
/*!40000 ALTER TABLE `c_c_d` DISABLE KEYS */;
INSERT INTO `c_c_d` (`deleted_at`, `deleted`, `created_at`, `updated_at`, `id`, `name`, `category`, `enabled`, `order`, `type_id`, `attr_id`, `level`, `options`)
VALUES
	(NULL, 0, '2024-03-20 10:39:42', '2024-03-20 10:54:16', 11, '物理机', 0, 0, 0, NULL, NULL, NULL, '{\"h\": 3, \"w\": 3, \"x\": 0, \"y\": 0, \"name\": \"物理机\", \"bgColor\": [\"#85EBC9\", \"#4AB8D8\"], \"isShadow\": false, \"showIcon\": true, \"type_ids\": [4], \"chartType\": \"count\", \"fontColor\": \"#ffffff\"}'),
	(NULL, 0, '2024-03-20 10:39:56', '2024-03-20 11:06:17', 12, '虚拟机', 0, 0, 0, NULL, NULL, NULL, '{\"h\": 3, \"w\": 3, \"x\": 0, \"y\": 3, \"name\": \"虚拟机\", \"bgColor\": [\"#6ABFFE\", \"#5375EB\"], \"isShadow\": false, \"showIcon\": true, \"type_ids\": [5], \"chartType\": \"count\", \"fontColor\": \"#ffffff\"}'),
	(NULL, 0, '2024-03-20 10:53:15', '2024-03-20 11:06:46', 15, 'IDC统计', 1, 0, 0, NULL, NULL, NULL, '{\"h\": 6, \"w\": 3, \"x\": 0, \"y\": 6, \"name\": \"IDC统计\", \"attr_ids\": [47], \"isShadow\": false, \"showIcon\": true, \"type_ids\": [4], \"chartType\": \"pie\", \"chartColor\": \"#9BA1F9,#0F2BA8,#A2EBFE,#4982F6,#FEB09C,#6C78E8,#FFDDAB,#4D66BD\"}'),
	(NULL, 0, '2024-03-20 10:55:12', '2024-03-20 10:55:49', 16, '事业部产品', 2, 0, 0, 1, NULL, 1, '{\"h\": 6, \"w\": 5, \"x\": 3, \"y\": 0, \"name\": \"事业部产品\", \"isShadow\": false, \"showIcon\": true, \"type_ids\": [2], \"chartType\": \"line\", \"chartColor\": \"#5DADF2,#86DFB7,#5A6F96,#7BD5FF,#FFB980,#4D58D6,#D9B6E9,#8054FF\"}'),
	(NULL, 0, '2024-03-20 10:55:44', '2024-03-20 10:56:01', 17, '物理机状态', 1, 0, 0, NULL, NULL, NULL, '{\"h\": 6, \"w\": 4, \"x\": 8, \"y\": 0, \"name\": \"物理机状态\", \"attr_ids\": [34], \"isShadow\": false, \"showIcon\": true, \"type_ids\": [4], \"chartType\": \"pie\", \"chartColor\": \"#9BA1F9,#0F2BA8,#A2EBFE,#4982F6,#FEB09C,#6C78E8,#FFDDAB,#4D66BD\"}'),
	(NULL, 0, '2024-03-20 10:56:54', '2024-03-20 11:06:50', 18, '事业部负责人', 1, 0, 0, NULL, NULL, NULL, '{\"h\": 6, \"w\": 3, \"x\": 3, \"y\": 6, \"name\": \"事业部负责人\", \"attr_ids\": [1, 10], \"barStack\": \"total\", \"isShadow\": false, \"showIcon\": true, \"type_ids\": [1], \"chartType\": \"bar\", \"chartColor\": \"#5DADF2,#86DFB7,#5A6F96,#7BD5FF,#FFB980,#4D58D6,#D9B6E9,#8054FF\", \"barDirection\": \"x\"}'),
	(NULL, 0, '2024-03-20 10:59:49', '2024-03-20 11:06:37', 19, '物理机负责人状态', 1, 0, 0, NULL, NULL, NULL, '{\"h\": 6, \"w\": 6, \"x\": 6, \"y\": 6, \"name\": \"物理机负责人状态\", \"attr_ids\": [20, 34], \"barStack\": \"total\", \"isShadow\": false, \"showIcon\": true, \"type_ids\": [4], \"chartType\": \"bar\", \"chartColor\": \"#5DADF2,#86DFB7,#5A6F96,#7BD5FF,#FFB980,#4D58D6,#D9B6E9,#8054FF\", \"barDirection\": \"y\"}'),
	(NULL, 0, '2024-03-20 11:00:36', '2024-03-20 11:00:47', 20, '状态统计', 1, 0, 0, NULL, NULL, NULL, '{\"h\": 5, \"w\": 6, \"x\": 0, \"y\": 12, \"name\": \"状态统计\", \"attr_ids\": [34], \"barStack\": \"total\", \"isShadow\": false, \"showIcon\": true, \"type_ids\": [4], \"chartType\": \"bar\", \"chartColor\": \"#5DADF2,#86DFB7,#5A6F96,#7BD5FF,#FFB980,#4D58D6,#D9B6E9,#8054FF\", \"barDirection\": \"x\"}'),
	(NULL, 0, '2024-03-20 11:01:05', '2024-03-20 11:06:27', 21, '物理机数量统计', 1, 0, 0, NULL, NULL, NULL, '{\"h\": 5, \"w\": 6, \"x\": 6, \"y\": 12, \"name\": \"物理机数量统计\", \"attr_ids\": [34], \"isShadow\": false, \"showIcon\": true, \"type_ids\": [4], \"chartType\": \"table\"}');
/*!40000 ALTER TABLE `c_c_d` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_c_t_t`
--

DROP TABLE IF EXISTS `c_c_t_t`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_c_t_t` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` int(11) NOT NULL,
  `attr_id` int(11) DEFAULT NULL,
  `notify` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `type_id` (`type_id`),
  KEY `attr_id` (`attr_id`),
  KEY `ix_c_ci_type_triggers_deleted` (`deleted`),
  CONSTRAINT `c_c_t_t_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `c_ci_types` (`id`),
  CONSTRAINT `c_c_t_t_ibfk_2` FOREIGN KEY (`attr_id`) REFERENCES `c_attributes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `c_ci_trigger_histories`
--

DROP TABLE IF EXISTS `c_ci_trigger_histories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_ci_trigger_histories` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `operate_type` enum('1','0','2') DEFAULT NULL,
  `record_id` int(11) DEFAULT NULL,
  `ci_id` int(11) NOT NULL,
  `trigger_id` int(11) DEFAULT NULL,
  `trigger_name` varchar(64) DEFAULT NULL,
  `is_ok` tinyint(1) DEFAULT NULL,
  `notify` text,
  `webhook` text,
  PRIMARY KEY (`id`),
  KEY `record_id` (`record_id`),
  KEY `trigger_id` (`trigger_id`),
  KEY `ix_c_ci_trigger_histories_ci_id` (`ci_id`),
  KEY `ix_c_ci_trigger_histories_deleted` (`deleted`),
  CONSTRAINT `c_ci_trigger_histories_ibfk_1` FOREIGN KEY (`record_id`) REFERENCES `c_records` (`id`),
  CONSTRAINT `c_ci_trigger_histories_ibfk_2` FOREIGN KEY (`trigger_id`) REFERENCES `c_c_t_t` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;

--
-- Table structure for table `c_c_t_u_c`
--

DROP TABLE IF EXISTS `c_c_t_u_c`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_c_t_u_c` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` int(11) NOT NULL,
  `attr_ids` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `type_id` (`type_id`),
  KEY `ix_c_ci_type_unique_constraints_deleted` (`deleted`),
  CONSTRAINT `c_c_t_u_c_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `c_ci_types` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_c_t_u_c`
--

LOCK TABLES `c_c_t_u_c` WRITE;
/*!40000 ALTER TABLE `c_c_t_u_c` DISABLE KEYS */;
/*!40000 ALTER TABLE `c_c_t_u_c` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_cfp`
--

DROP TABLE IF EXISTS `c_cfp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_cfp` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `a` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `b` int(11) DEFAULT NULL,
  `c` text COLLATE utf8_unicode_ci,
  `d` text COLLATE utf8_unicode_ci,
  `e` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `b` (`b`),
  KEY `ix_c_cfp_deleted` (`deleted`),
  KEY `ix_c_cfp_e` (`e`),
  KEY `ix_c_cfp_a` (`a`),
  CONSTRAINT `c_cfp_ibfk_1` FOREIGN KEY (`b`) REFERENCES `c_ci_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_cfp`
--

LOCK TABLES `c_cfp` WRITE;
/*!40000 ALTER TABLE `c_cfp` DISABLE KEYS */;
INSERT INTO `c_cfp` VALUES (NULL,0,'2023-05-23 17:30:00',NULL,1,NULL,4,NULL,'server_name,oneagent_id,private_ip,os_version,cnc_ip,ctc_ip,cmc_ip,kernel_version,ssh_port',42);
/*!40000 ALTER TABLE `c_cfp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_choice_floats`
--

DROP TABLE IF EXISTS `c_choice_floats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_choice_floats` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `attr_id` int(11) NOT NULL,
  `value` float NOT NULL,
  `option` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `attr_id` (`attr_id`),
  KEY `ix_c_choice_floats_deleted` (`deleted`),
  CONSTRAINT `c_choice_floats_ibfk_1` FOREIGN KEY (`attr_id`) REFERENCES `c_attributes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_choice_floats`
--

LOCK TABLES `c_choice_floats` WRITE;
/*!40000 ALTER TABLE `c_choice_floats` DISABLE KEYS */;
/*!40000 ALTER TABLE `c_choice_floats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_choice_integers`
--

DROP TABLE IF EXISTS `c_choice_integers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_choice_integers` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `attr_id` int(11) NOT NULL,
  `value` int(11) NOT NULL,
  `option` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `attr_id` (`attr_id`),
  KEY `ix_c_choice_integers_deleted` (`deleted`),
  CONSTRAINT `c_choice_integers_ibfk_1` FOREIGN KEY (`attr_id`) REFERENCES `c_attributes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_choice_integers`
--

LOCK TABLES `c_choice_integers` WRITE;
/*!40000 ALTER TABLE `c_choice_integers` DISABLE KEYS */;
/*!40000 ALTER TABLE `c_choice_integers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_choice_texts`
--

DROP TABLE IF EXISTS `c_choice_texts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_choice_texts` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `attr_id` int(11) NOT NULL,
  `value` text COLLATE utf8_unicode_ci NOT NULL,
  `option` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `attr_id` (`attr_id`),
  KEY `ix_c_choice_texts_deleted` (`deleted`),
  CONSTRAINT `c_choice_texts_ibfk_1` FOREIGN KEY (`attr_id`) REFERENCES `c_attributes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=153 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_choice_texts`
--

LOCK TABLES `c_choice_texts` WRITE;
/*!40000 ALTER TABLE `c_choice_texts` DISABLE KEYS */;
INSERT INTO `c_choice_texts` VALUES (NULL,0,'2022-12-14 19:25:41',NULL,51,17,'IQ','null'),(NULL,0,'2022-12-14 19:25:41',NULL,52,17,'web','null'),(NULL,0,'2022-12-14 19:25:41',NULL,53,17,'service','null'),(NULL,0,'2022-12-14 19:25:41',NULL,54,17,'job','null'),(NULL,0,'2022-12-14 19:25:41',NULL,55,17,'mq','null'),(NULL,0,'2022-12-14 19:25:41',NULL,56,17,'api','null'),(NULL,0,'2022-12-14 19:25:42',NULL,76,55,'公网','null'),(NULL,0,'2022-12-14 19:25:42',NULL,77,55,'仅内网','null'),(NULL,0,'2022-12-14 19:25:42',NULL,81,61,'SAS','null'),(NULL,0,'2022-12-14 19:25:42',NULL,82,61,'SATA','null'),(NULL,0,'2022-12-14 19:25:42',NULL,83,61,'Solid','null'),(NULL,0,'2022-12-14 19:25:42',NULL,84,61,'SolidStateSATA','null'),(NULL,0,'2022-12-14 19:25:42',NULL,85,61,'Solid State SATA','null'),(NULL,0,'2022-12-14 19:25:43',NULL,106,47,'南汇','{\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#305B09\", \"fontStyle\": \"italic\", \"fontWeight\": \"bold\"}}'),(NULL,0,'2022-12-14 19:25:43',NULL,107,47,'张江','{\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#05302A\", \"fontStyle\": \"italic\", \"fontWeight\": \"bold\"}}'),(NULL,0,'2022-12-14 19:25:43',NULL,108,47,'外高桥','{\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#0C2659\", \"fontStyle\": \"italic\", \"fontWeight\": \"bold\"}}'),(NULL,0,'2022-12-14 19:25:43',NULL,114,87,'是','{\"icon\": {}, \"style\": {\"color\": \"#417810\"}}'),(NULL,0,'2022-12-14 19:25:43',NULL,115,87,'否','{\"icon\": {}, \"style\": {\"color\": \"#9F1616\"}}'),(NULL,0,'2023-01-11 18:37:49',NULL,120,97,'A3','{\"icon\": {}, \"style\": {}}'),(NULL,0,'2023-01-11 18:37:49',NULL,121,97,'A4','{\"icon\": {}, \"style\": {}}'),(NULL,0,'2023-01-16 17:24:39',NULL,128,5,'6666','{\"icon\": {}, \"style\": {}}'),(NULL,0,'2023-01-16 17:24:39',NULL,129,5,'999','{\"icon\": {}, \"style\": {}}'),(NULL,0,'2023-01-16 17:24:39',NULL,130,5,'111','{\"icon\": {}, \"style\": {}}'),(NULL,0,'2023-01-16 17:24:39',NULL,131,5,'222','{\"icon\": {}, \"style\": {}}'),(NULL,0,'2023-01-16 17:24:39',NULL,132,5,'333','{\"icon\": {}, \"style\": {}}'),(NULL,0,'2023-01-16 17:24:39',NULL,133,5,'444','{\"icon\": {}, \"style\": {}}'),(NULL,0,'2023-03-03 17:50:49',NULL,134,34,'在线','{\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#065C30\", \"backgroundColor\": \"#D9F7BE\"}}'),(NULL,0,'2023-03-03 17:50:49',NULL,135,34,'下线','{\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#881111\", \"backgroundColor\": \"#FFCCC7\"}}'),(NULL,0,'2023-03-03 17:50:49',NULL,136,34,'待用','{\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#0A483F\", \"backgroundColor\": \"#BAE7FF\"}}'),(NULL,0,'2023-03-03 17:50:49',NULL,137,34,'维修','{\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#622C0A\", \"backgroundColor\": \"#FFD8BF\"}}'),(NULL,0,'2023-03-03 17:50:49',NULL,138,34,'重装','{\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#5C4D0E\", \"backgroundColor\": \"#FFF1B8\"}}'),(NULL,0,'2023-03-03 17:52:38',NULL,139,35,'test','{\"icon\": {\"name\": \"huiyiguanli\", \"color\": \"\"}, \"style\": {}}'),(NULL,0,'2023-03-03 17:52:38',NULL,140,35,'ppe','{\"icon\": {\"name\": \"renwuguanli\", \"color\": \"\"}, \"style\": {}}'),(NULL,0,'2023-03-03 17:52:38',NULL,141,35,'prod','{\"icon\": {\"name\": \"jiangbei\", \"color\": \"\"}, \"style\": {\"color\": \"#741717\"}}'),(NULL,0,'2023-05-23 15:24:36',NULL,142,74,'在线','{\"icon\": {\"name\": \"caise-zaixian\", \"color\": \"\"}, \"style\": {\"fontWeight\": \"bold\"}}'),(NULL,0,'2023-05-23 15:24:36',NULL,143,74,'下线','{\"icon\": {\"name\": \"caise-xiaxian\", \"color\": \"\"}, \"style\": {\"fontWeight\": \"bold\"}}'),(NULL,0,'2023-07-11 15:14:28',NULL,148,102,'1','{\"icon\": {}, \"style\": {}}'),(NULL,0,'2023-07-11 15:14:28',NULL,149,102,'aaa','{\"icon\": {\"name\": \"caise-zaixian\", \"color\": \"\"}, \"style\": {}}'),(NULL,0,'2023-07-11 15:14:28',NULL,150,102,'asdasda','{\"icon\": {}, \"style\": {}}'),(NULL,0,'2023-07-11 15:14:28',NULL,151,102,'assda','{\"icon\": {}, \"style\": {}}'),(NULL,0,'2023-07-11 15:14:28',NULL,152,102,'qqqq','{\"icon\": {}, \"style\": {}}');
/*!40000 ALTER TABLE `c_choice_texts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_ci_filter_perms`
--

DROP TABLE IF EXISTS `c_ci_filter_perms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_ci_filter_perms` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `type_id` int(11) DEFAULT NULL,
  `ci_filter` text COLLATE utf8_unicode_ci,
  `attr_filter` text COLLATE utf8_unicode_ci,
  `rid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `type_id` (`type_id`),
  KEY `ix_c_ci_filter_perms_rid` (`rid`),
  KEY `ix_c_ci_filter_perms_name` (`name`),
  KEY `ix_c_ci_filter_perms_deleted` (`deleted`),
  CONSTRAINT `c_ci_filter_perms_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `c_ci_types` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_ci_filter_perms`
--

LOCK TABLES `c_ci_filter_perms` WRITE;
/*!40000 ALTER TABLE `c_ci_filter_perms` DISABLE KEYS */;
/*!40000 ALTER TABLE `c_ci_filter_perms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_ci_relations`
--

DROP TABLE IF EXISTS `c_ci_relations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_ci_relations` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_ci_id` int(11) NOT NULL,
  `second_ci_id` int(11) NOT NULL,
  `relation_type_id` int(11) NOT NULL,
  `more` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `first_ci_id` (`first_ci_id`),
  KEY `second_ci_id` (`second_ci_id`),
  KEY `relation_type_id` (`relation_type_id`),
  KEY `more` (`more`),
  KEY `ix_c_ci_relations_deleted` (`deleted`),
  CONSTRAINT `c_ci_relations_ibfk_1` FOREIGN KEY (`first_ci_id`) REFERENCES `c_cis` (`id`),
  CONSTRAINT `c_ci_relations_ibfk_2` FOREIGN KEY (`second_ci_id`) REFERENCES `c_cis` (`id`),
  CONSTRAINT `c_ci_relations_ibfk_3` FOREIGN KEY (`relation_type_id`) REFERENCES `c_relation_types` (`id`),
  CONSTRAINT `c_ci_relations_ibfk_4` FOREIGN KEY (`more`) REFERENCES `c_cis` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_ci_relations`
--

LOCK TABLES `c_ci_relations` WRITE;
/*!40000 ALTER TABLE `c_ci_relations` DISABLE KEYS */;
INSERT INTO `c_ci_relations` VALUES (NULL,0,'2023-07-11 17:51:13',NULL,1,1,2,1,NULL),(NULL,0,'2023-07-11 17:51:24',NULL,2,2,3,1,NULL),(NULL,0,'2023-07-11 17:51:35',NULL,3,3,4,3,NULL);
/*!40000 ALTER TABLE `c_ci_relations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_ci_type_attribute_group_items`
--

DROP TABLE IF EXISTS `c_ci_type_attribute_group_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_ci_type_attribute_group_items` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `attr_id` int(11) NOT NULL,
  `order` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `group_id` (`group_id`),
  KEY `attr_id` (`attr_id`),
  KEY `ix_c_ci_type_attribute_group_items_deleted` (`deleted`),
  CONSTRAINT `c_ci_type_attribute_group_items_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `c_ci_type_attribute_groups` (`id`),
  CONSTRAINT `c_ci_type_attribute_group_items_ibfk_2` FOREIGN KEY (`attr_id`) REFERENCES `c_attributes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=386 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_ci_type_attribute_group_items`
--

LOCK TABLES `c_ci_type_attribute_group_items` WRITE;
/*!40000 ALTER TABLE `c_ci_type_attribute_group_items` DISABLE KEYS */;
INSERT INTO `c_ci_type_attribute_group_items` VALUES (NULL,0,'2021-11-24 10:51:43',NULL,1,1,23,0),(NULL,0,'2021-11-24 10:51:45',NULL,2,1,24,1),(NULL,0,'2021-11-24 10:51:47',NULL,3,1,25,2),(NULL,0,'2021-11-24 10:51:51',NULL,4,1,26,3),(NULL,0,'2021-11-24 10:51:53','2022-10-17 20:41:04',5,1,27,5),(NULL,0,'2021-11-24 10:51:57','2022-10-17 20:41:04',6,1,28,4),(NULL,0,'2021-11-24 10:51:59',NULL,7,1,29,6),(NULL,0,'2021-11-24 10:52:01',NULL,8,1,30,7),(NULL,0,'2021-11-24 10:52:03',NULL,9,1,31,8),(NULL,0,'2021-11-24 11:03:32',NULL,10,2,32,0),(NULL,0,'2021-11-24 11:03:39',NULL,11,2,20,1),(NULL,0,'2021-11-24 11:03:43',NULL,12,2,22,2),(NULL,0,'2021-11-24 11:03:46',NULL,13,2,33,3),(NULL,0,'2021-11-24 11:03:49',NULL,14,2,34,4),(NULL,0,'2021-11-24 11:03:52',NULL,15,2,35,5),(NULL,0,'2021-11-24 11:04:38',NULL,16,3,4,0),(NULL,0,'2021-11-24 11:06:30',NULL,17,3,36,1),(NULL,0,'2021-11-24 11:19:33',NULL,18,3,37,2),(NULL,0,'2021-11-24 11:19:36',NULL,19,3,38,3),(NULL,0,'2021-11-24 11:19:38',NULL,20,3,39,4),(NULL,0,'2021-11-24 11:19:40',NULL,21,3,40,5),(NULL,0,'2021-11-24 11:19:42',NULL,22,3,41,6),(NULL,0,'2021-11-24 11:19:47','2021-11-24 11:19:49',23,3,42,8),(NULL,0,'2021-11-24 11:19:49',NULL,24,3,43,7),(NULL,0,'2021-11-24 11:19:55',NULL,25,3,44,9),(NULL,0,'2021-11-24 11:19:58',NULL,26,3,45,10),(NULL,0,'2021-11-24 11:20:00',NULL,27,3,46,11),(NULL,0,'2021-11-24 11:24:06',NULL,28,4,47,0),(NULL,0,'2021-11-24 11:24:07',NULL,29,4,48,1),(NULL,0,'2021-11-24 11:24:09',NULL,30,4,49,2),(NULL,0,'2021-11-24 11:24:12',NULL,31,4,50,3),(NULL,0,'2021-11-24 11:45:14',NULL,32,5,54,0),(NULL,0,'2021-11-24 11:45:21',NULL,33,5,24,1),(NULL,0,'2021-11-24 11:45:35',NULL,34,5,34,2),(NULL,0,'2021-11-24 11:45:37',NULL,35,5,35,3),(NULL,0,'2021-11-24 11:45:43',NULL,36,5,20,4),(NULL,0,'2021-11-24 11:45:46',NULL,37,5,22,5),(NULL,0,'2021-11-24 11:45:50',NULL,38,5,33,6),(NULL,0,'2021-11-24 11:46:03',NULL,39,6,5,0),('2021-11-24 11:46:36',1,'2021-11-24 11:46:10','2021-11-24 11:46:36',40,5,1,7),(NULL,0,'2021-11-24 11:46:14',NULL,41,6,55,1),(NULL,0,'2021-11-24 11:46:17',NULL,42,6,25,2),(NULL,0,'2021-11-24 11:46:20',NULL,43,6,26,3),(NULL,0,'2021-11-24 11:46:22','2021-11-24 11:47:26',44,6,30,8),(NULL,0,'2021-11-24 11:46:24',NULL,45,6,31,5),(NULL,0,'2021-11-24 11:46:39',NULL,46,5,32,7),(NULL,0,'2021-11-24 11:46:56',NULL,47,7,36,0),(NULL,0,'2021-11-24 11:46:57',NULL,48,7,37,1),(NULL,0,'2021-11-24 11:46:59',NULL,49,7,40,2),(NULL,0,'2021-11-24 11:47:01',NULL,50,7,39,3),(NULL,0,'2021-11-24 11:47:04','2022-08-23 20:12:27',51,7,41,5),(NULL,0,'2021-11-24 11:47:13',NULL,52,8,47,0),(NULL,0,'2021-11-24 11:47:14',NULL,53,8,49,1),(NULL,0,'2021-11-24 11:47:16',NULL,54,8,50,2),(NULL,0,'2021-11-24 11:47:20',NULL,55,6,56,6),(NULL,0,'2021-11-24 11:47:26',NULL,56,6,57,7),(NULL,0,'2021-11-24 11:47:31','2022-08-23 20:12:27',57,7,58,4),(NULL,0,'2021-11-24 11:50:23',NULL,58,9,6,0),(NULL,0,'2021-11-24 11:52:45','2021-11-24 11:53:05',59,9,39,1),(NULL,0,'2021-11-24 11:52:45','2021-11-24 11:53:03',60,9,40,4),(NULL,0,'2021-11-24 11:53:00','2021-11-24 11:53:05',61,9,59,2),(NULL,0,'2021-11-24 11:53:03','2021-11-24 11:53:05',62,9,60,3),(NULL,0,'2021-11-24 11:53:34',NULL,63,10,7,0),(NULL,0,'2021-11-24 11:56:55',NULL,64,10,61,1),(NULL,0,'2021-11-24 11:56:57',NULL,65,10,62,2),(NULL,0,'2021-11-24 11:56:59',NULL,66,10,63,3),(NULL,0,'2021-11-24 11:57:02',NULL,67,10,64,4),(NULL,0,'2021-11-24 11:59:57',NULL,68,11,8,0),(NULL,0,'2021-11-24 11:59:59',NULL,69,11,65,1),(NULL,0,'2021-11-24 12:00:00',NULL,70,11,66,2),(NULL,0,'2021-11-24 12:00:03',NULL,71,11,67,3),(NULL,0,'2021-11-24 12:00:05',NULL,72,11,68,4),(NULL,0,'2021-11-24 12:00:09',NULL,73,11,69,5),(NULL,0,'2021-11-24 12:00:53',NULL,74,12,9,0),(NULL,0,'2021-11-24 12:01:45',NULL,75,12,25,1),(NULL,0,'2021-11-24 12:01:45',NULL,76,12,47,2),(NULL,0,'2021-11-24 12:01:45',NULL,77,12,35,3),(NULL,0,'2021-11-24 12:01:45',NULL,78,12,34,4),(NULL,0,'2021-11-24 12:01:45',NULL,79,12,57,5),(NULL,0,'2022-08-22 19:52:13',NULL,80,13,1,0),(NULL,0,'2022-08-22 19:52:18',NULL,81,13,10,1),(NULL,0,'2022-08-22 19:52:20',NULL,82,13,11,2),(NULL,0,'2022-08-22 19:52:23',NULL,83,13,12,3),(NULL,0,'2022-08-23 08:57:29',NULL,84,14,3,0),(NULL,0,'2022-08-23 08:57:32',NULL,85,14,17,1),(NULL,0,'2022-08-23 08:57:34',NULL,86,14,18,2),(NULL,0,'2022-08-23 08:57:38',NULL,87,14,19,3),(NULL,0,'2022-08-23 08:57:41',NULL,88,14,20,4),(NULL,0,'2022-08-23 08:57:43',NULL,89,14,21,5),(NULL,0,'2022-08-23 08:57:45',NULL,90,14,22,6),(NULL,0,'2022-08-23 20:12:27',NULL,91,7,62,6),(NULL,0,'2022-12-02 13:33:51',NULL,92,16,76,0),(NULL,0,'2022-12-02 13:33:56','2022-12-02 13:34:04',93,16,71,1),(NULL,0,'2022-12-02 13:33:59','2022-12-02 13:34:06',94,16,48,4),(NULL,0,'2022-12-02 13:34:01','2022-12-02 13:34:06',95,16,47,3),(NULL,0,'2022-12-02 13:34:06',NULL,96,16,74,2),(NULL,0,'2022-12-02 13:34:12','2022-12-02 13:45:43',97,16,77,9),(NULL,0,'2022-12-02 13:34:14','2022-12-02 13:45:43',98,16,75,8),(NULL,0,'2022-12-02 13:34:17','2022-12-02 13:45:43',99,16,51,10),(NULL,0,'2022-12-02 13:35:33','2022-12-02 13:45:43',100,16,78,7),(NULL,0,'2022-12-02 13:36:33',NULL,101,17,76,0),(NULL,0,'2022-12-02 13:36:35',NULL,102,17,72,1),(NULL,0,'2022-12-02 13:36:39',NULL,103,17,74,2),(NULL,0,'2022-12-02 13:36:42',NULL,104,17,47,3),(NULL,0,'2022-12-02 13:36:51',NULL,105,17,48,4),(NULL,0,'2022-12-02 13:36:56','2022-12-02 13:46:12',106,17,77,7),(NULL,0,'2022-12-02 13:36:58','2022-12-02 13:46:12',107,17,78,8),(NULL,0,'2022-12-02 13:37:01','2022-12-02 13:46:12',108,17,75,9),(NULL,0,'2022-12-02 13:37:17','2022-12-02 13:46:12',109,17,51,10),(NULL,0,'2022-12-02 13:37:17','2022-12-02 13:46:12',110,17,53,11),(NULL,0,'2022-12-02 13:37:31','2022-12-02 13:45:43',111,16,53,11),(NULL,0,'2022-12-02 13:38:29',NULL,112,18,73,0),(NULL,0,'2022-12-02 13:38:54','2022-12-02 13:46:31',113,18,78,8),(NULL,0,'2022-12-02 13:38:54','2022-12-02 13:39:04',114,18,77,2),(NULL,0,'2022-12-02 13:38:54','2022-12-02 13:39:01',115,18,76,1),(NULL,0,'2022-12-02 13:38:54','2022-12-02 13:46:31',116,18,75,9),(NULL,0,'2022-12-02 13:38:54','2022-12-02 13:39:10',117,18,74,3),(NULL,0,'2022-12-02 13:38:54','2022-12-02 13:46:31',118,18,47,6),(NULL,0,'2022-12-02 13:38:54','2022-12-02 13:46:31',119,18,48,7),(NULL,0,'2022-12-02 13:38:54','2022-12-02 13:46:31',120,18,51,10),(NULL,0,'2022-12-02 13:38:54','2022-12-02 13:46:31',121,18,53,11),(NULL,0,'2022-12-02 13:43:58','2022-12-02 13:44:04',122,16,22,5),(NULL,0,'2022-12-02 13:45:38','2022-12-02 13:45:43',123,16,79,6),(NULL,0,'2022-12-02 13:46:00','2022-12-02 13:46:12',124,17,79,6),(NULL,0,'2022-12-02 13:46:00','2022-12-02 13:46:09',125,17,22,5),(NULL,0,'2022-12-02 13:46:24','2022-12-02 13:46:31',126,18,79,5),(NULL,0,'2022-12-02 13:46:24','2022-12-02 13:46:28',127,18,22,4),(NULL,0,'2022-12-02 13:48:54',NULL,128,19,76,0),(NULL,0,'2022-12-02 13:49:03',NULL,129,19,80,1),(NULL,0,'2022-12-02 13:49:11',NULL,130,19,77,2),(NULL,0,'2022-12-02 13:49:15',NULL,131,19,74,3),(NULL,0,'2022-12-02 13:49:22',NULL,132,19,22,4),(NULL,0,'2022-12-02 13:49:25',NULL,133,19,79,5),(NULL,0,'2022-12-02 13:49:27','2022-12-02 13:49:48',134,19,78,8),(NULL,0,'2022-12-02 13:49:30','2022-12-02 13:49:48',135,19,75,9),(NULL,0,'2022-12-02 13:49:45',NULL,136,19,47,6),(NULL,0,'2022-12-02 13:49:48',NULL,137,19,48,7),(NULL,0,'2022-12-02 13:49:51',NULL,138,19,51,10),(NULL,0,'2022-12-02 13:49:52',NULL,139,19,53,11),(NULL,0,'2022-12-02 14:10:59',NULL,140,20,81,0),(NULL,0,'2022-12-02 14:11:08',NULL,141,20,84,1),(NULL,0,'2022-12-02 14:11:10',NULL,142,20,82,2),(NULL,0,'2022-12-02 14:11:13',NULL,143,20,83,3),(NULL,0,'2022-12-02 14:11:16',NULL,144,20,34,4),(NULL,0,'2022-12-02 14:11:20','2022-12-02 14:11:56',145,20,85,8),(NULL,0,'2022-12-02 14:11:24','2022-12-02 14:11:56',146,20,86,6),(NULL,0,'2022-12-02 14:11:27','2022-12-02 14:11:56',147,20,87,7),(NULL,0,'2022-12-02 14:11:33','2022-12-02 14:11:56',148,20,88,9),(NULL,0,'2022-12-02 14:11:51','2022-12-02 14:11:56',149,20,22,5),(NULL,0,'2022-12-02 14:13:48',NULL,150,21,81,0),(NULL,0,'2022-12-02 14:13:54',NULL,151,21,84,1),(NULL,0,'2022-12-02 14:13:57',NULL,152,21,82,2),(NULL,0,'2022-12-02 14:14:00',NULL,153,21,83,3),(NULL,0,'2022-12-02 14:14:04',NULL,154,21,22,4),(NULL,0,'2022-12-02 14:14:07',NULL,155,21,85,5),(NULL,0,'2022-12-02 14:14:09',NULL,156,21,86,6),(NULL,0,'2022-12-02 14:14:11',NULL,157,21,88,7),(NULL,0,'2022-12-02 14:15:37',NULL,158,22,81,0),(NULL,0,'2022-12-02 14:15:40',NULL,159,22,84,1),(NULL,0,'2022-12-02 14:15:42',NULL,160,22,82,2),(NULL,0,'2022-12-02 14:15:44',NULL,161,22,83,3),(NULL,0,'2022-12-02 14:15:48',NULL,162,22,22,4),(NULL,0,'2022-12-02 14:15:50',NULL,163,22,85,5),(NULL,0,'2022-12-02 14:15:52',NULL,164,22,88,6),(NULL,0,'2022-12-02 14:17:32',NULL,165,23,81,0),(NULL,0,'2022-12-02 14:17:35',NULL,166,23,84,1),(NULL,0,'2022-12-02 14:17:37',NULL,167,23,82,2),(NULL,0,'2022-12-02 14:17:41',NULL,168,23,83,3),(NULL,0,'2022-12-02 14:17:47',NULL,169,23,22,4),(NULL,0,'2022-12-02 14:17:48',NULL,170,23,85,5),(NULL,0,'2022-12-02 14:20:16',NULL,171,24,89,0),(NULL,0,'2022-12-02 14:25:33',NULL,172,24,90,1),(NULL,0,'2022-12-02 14:25:54',NULL,173,24,91,2),(NULL,0,'2022-12-02 14:26:18','2022-12-02 14:29:10',174,24,92,4),(NULL,0,'2022-12-02 14:27:09','2022-12-02 14:29:10',175,24,93,5),(NULL,0,'2022-12-02 14:27:26','2022-12-02 14:29:10',176,24,22,6),(NULL,0,'2022-12-02 14:29:03','2022-12-02 14:29:10',177,24,94,3),(NULL,0,'2022-12-02 14:30:31',NULL,178,25,89,0),(NULL,0,'2022-12-02 14:30:33',NULL,179,25,90,1),(NULL,0,'2022-12-02 14:30:36',NULL,180,25,91,2),(NULL,0,'2022-12-02 14:30:38',NULL,181,25,92,3),(NULL,0,'2022-12-02 14:30:44',NULL,182,25,93,4),(NULL,0,'2022-12-02 14:30:46',NULL,183,25,22,5),(NULL,0,'2022-12-02 14:31:09',NULL,184,26,89,0),(NULL,0,'2022-12-02 14:31:10',NULL,185,26,90,1),(NULL,0,'2022-12-02 14:31:13',NULL,186,26,91,2),(NULL,0,'2022-12-02 14:31:16',NULL,187,26,92,3),(NULL,0,'2022-12-02 14:31:19',NULL,188,26,93,4),(NULL,0,'2022-12-02 14:31:21',NULL,189,26,22,5),(NULL,0,'2022-12-14 19:25:45','2023-01-06 09:36:12',190,27,1,0),('2023-07-10 18:43:16',1,'2022-12-14 19:25:45','2023-07-10 18:43:16',191,27,10,1),(NULL,0,'2022-12-14 19:25:45','2023-07-10 18:43:28',192,27,11,3),(NULL,0,'2022-12-14 19:25:45','2023-07-10 18:43:28',193,27,12,2),(NULL,0,'2022-12-14 19:25:45',NULL,194,28,3,0),(NULL,0,'2022-12-14 19:25:45',NULL,195,28,17,1),(NULL,0,'2022-12-14 19:25:45',NULL,196,28,18,2),(NULL,0,'2022-12-14 19:25:45',NULL,197,28,19,3),(NULL,0,'2022-12-14 19:25:45',NULL,198,28,20,4),(NULL,0,'2022-12-14 19:25:45',NULL,199,28,21,5),(NULL,0,'2022-12-14 19:25:45',NULL,200,28,22,6),(NULL,0,'2022-12-14 19:25:46',NULL,201,29,23,0),(NULL,0,'2022-12-14 19:25:46',NULL,202,29,24,1),(NULL,0,'2022-12-14 19:25:46',NULL,203,29,25,2),(NULL,0,'2022-12-14 19:25:46',NULL,204,29,26,3),(NULL,0,'2022-12-14 19:25:46',NULL,205,29,28,4),(NULL,0,'2022-12-14 19:25:46',NULL,206,29,27,5),(NULL,0,'2022-12-14 19:25:46',NULL,207,29,29,6),(NULL,0,'2022-12-14 19:25:46',NULL,208,29,30,7),(NULL,0,'2022-12-14 19:25:46',NULL,209,29,31,8),(NULL,0,'2022-12-14 19:25:46','2023-05-23 16:39:24',210,30,32,1),(NULL,0,'2022-12-14 19:25:46','2023-05-23 16:39:24',211,30,20,2),(NULL,0,'2022-12-14 19:25:46','2023-05-23 16:39:24',212,30,22,3),(NULL,0,'2022-12-14 19:25:46','2023-05-23 16:39:24',213,30,33,4),(NULL,0,'2022-12-14 19:25:46','2023-05-23 16:39:24',214,30,34,0),(NULL,0,'2022-12-14 19:25:46',NULL,215,30,35,5),(NULL,0,'2022-12-14 19:25:46','2023-01-06 09:51:55',216,31,4,1),(NULL,0,'2022-12-14 19:25:46','2023-01-06 09:51:54',217,31,36,2),(NULL,0,'2022-12-14 19:25:46','2023-01-06 09:51:53',218,31,37,3),(NULL,0,'2022-12-14 19:25:46','2023-01-06 09:51:55',219,31,38,0),(NULL,0,'2022-12-14 19:25:46',NULL,220,31,39,4),(NULL,0,'2022-12-14 19:25:46',NULL,221,31,40,5),(NULL,0,'2022-12-14 19:25:46',NULL,222,31,41,6),(NULL,0,'2022-12-14 19:25:46',NULL,223,31,43,7),(NULL,0,'2022-12-14 19:25:46',NULL,224,31,42,8),(NULL,0,'2022-12-14 19:25:46',NULL,225,31,44,9),(NULL,0,'2022-12-14 19:25:46',NULL,226,31,45,10),(NULL,0,'2022-12-14 19:25:46',NULL,227,31,46,11),('2023-01-05 18:54:04',1,'2022-12-14 19:25:46','2023-01-05 18:54:04',228,32,47,0),(NULL,0,'2022-12-14 19:25:46','2023-01-05 18:54:04',229,32,48,0),(NULL,0,'2022-12-14 19:25:46','2023-01-05 18:54:04',230,32,49,1),('2023-01-05 18:54:26',1,'2022-12-14 19:25:46','2023-01-05 18:54:26',231,32,50,2),(NULL,0,'2022-12-14 19:25:46',NULL,232,33,54,0),(NULL,0,'2022-12-14 19:25:46',NULL,233,33,24,1),(NULL,0,'2022-12-14 19:25:46',NULL,234,33,34,2),(NULL,0,'2022-12-14 19:25:46',NULL,235,33,35,3),(NULL,0,'2022-12-14 19:25:46',NULL,236,33,20,4),(NULL,0,'2022-12-14 19:25:46',NULL,237,33,22,5),(NULL,0,'2022-12-14 19:25:46',NULL,238,33,33,6),(NULL,0,'2022-12-14 19:25:46',NULL,239,33,32,7),(NULL,0,'2022-12-14 19:25:46',NULL,240,34,5,0),(NULL,0,'2022-12-14 19:25:46',NULL,241,34,55,1),(NULL,0,'2022-12-14 19:25:46',NULL,242,34,25,2),(NULL,0,'2022-12-14 19:25:46',NULL,243,34,26,3),(NULL,0,'2022-12-14 19:25:46','2023-01-04 10:57:00',244,34,31,4),(NULL,0,'2022-12-14 19:25:46','2023-01-04 10:57:00',245,34,56,5),(NULL,0,'2022-12-14 19:25:46',NULL,246,34,57,6),(NULL,0,'2022-12-14 19:25:46',NULL,247,34,30,7),(NULL,0,'2022-12-14 19:25:46',NULL,248,35,36,0),(NULL,0,'2022-12-14 19:25:46',NULL,249,35,37,1),(NULL,0,'2022-12-14 19:25:46',NULL,250,35,40,2),(NULL,0,'2022-12-14 19:25:46','2023-01-11 18:35:49',251,35,39,3),(NULL,0,'2022-12-14 19:25:46','2023-01-11 18:35:49',252,35,58,4),(NULL,0,'2022-12-14 19:25:46','2023-01-11 18:35:49',253,35,41,5),(NULL,0,'2022-12-14 19:25:46','2023-01-11 18:35:49',254,35,62,6),(NULL,0,'2022-12-14 19:25:46',NULL,255,36,47,0),(NULL,0,'2022-12-14 19:25:46',NULL,256,36,49,1),(NULL,0,'2022-12-14 19:25:46',NULL,257,36,50,2),(NULL,0,'2022-12-14 19:25:46',NULL,258,37,6,0),(NULL,0,'2022-12-14 19:25:46',NULL,259,37,39,1),(NULL,0,'2022-12-14 19:25:46',NULL,260,37,59,2),(NULL,0,'2022-12-14 19:25:46',NULL,261,37,60,3),(NULL,0,'2022-12-14 19:25:46',NULL,262,37,40,4),(NULL,0,'2022-12-14 19:25:46',NULL,263,38,7,0),(NULL,0,'2022-12-14 19:25:46',NULL,264,38,61,1),(NULL,0,'2022-12-14 19:25:46',NULL,265,38,62,2),(NULL,0,'2022-12-14 19:25:46',NULL,266,38,63,3),(NULL,0,'2022-12-14 19:25:46',NULL,267,38,64,4),(NULL,0,'2022-12-14 19:25:46',NULL,268,39,8,0),(NULL,0,'2022-12-14 19:25:46',NULL,269,39,65,1),(NULL,0,'2022-12-14 19:25:46',NULL,270,39,66,2),(NULL,0,'2022-12-14 19:25:46',NULL,271,39,67,3),(NULL,0,'2022-12-14 19:25:46',NULL,272,39,68,4),(NULL,0,'2022-12-14 19:25:46',NULL,273,39,69,5),(NULL,0,'2022-12-14 19:25:46',NULL,274,40,9,0),(NULL,0,'2022-12-14 19:25:46',NULL,275,40,25,1),(NULL,0,'2022-12-14 19:25:46',NULL,276,40,47,2),(NULL,0,'2022-12-14 19:25:46',NULL,277,40,35,3),(NULL,0,'2022-12-14 19:25:46',NULL,278,40,34,4),(NULL,0,'2022-12-14 19:25:46',NULL,279,40,57,5),(NULL,0,'2022-12-14 19:25:46',NULL,280,41,76,0),(NULL,0,'2022-12-14 19:25:46',NULL,281,41,71,1),(NULL,0,'2022-12-14 19:25:46',NULL,282,41,74,2),(NULL,0,'2022-12-14 19:25:46',NULL,283,41,47,3),(NULL,0,'2022-12-14 19:25:46',NULL,284,41,48,4),('2023-01-04 18:25:54',1,'2022-12-14 19:25:46','2023-01-04 18:25:54',285,41,22,5),(NULL,0,'2022-12-14 19:25:46','2023-01-04 18:25:54',286,41,79,5),('2023-05-23 15:18:03',1,'2022-12-14 19:25:46','2023-05-23 15:18:03',287,41,78,6),(NULL,0,'2022-12-14 19:25:46','2023-05-23 15:18:03',288,41,75,6),(NULL,0,'2022-12-14 19:25:46','2023-05-23 15:18:03',289,41,77,7),(NULL,0,'2022-12-14 19:25:46','2023-05-23 15:18:03',290,41,51,8),(NULL,0,'2022-12-14 19:25:46','2023-05-23 15:18:03',291,41,53,9),(NULL,0,'2022-12-14 19:25:46',NULL,292,42,76,0),(NULL,0,'2022-12-14 19:25:46',NULL,293,42,72,1),(NULL,0,'2022-12-14 19:25:46',NULL,294,42,74,2),(NULL,0,'2022-12-14 19:25:46',NULL,295,42,47,3),(NULL,0,'2022-12-14 19:25:46',NULL,296,42,48,4),(NULL,0,'2022-12-14 19:25:46',NULL,297,42,22,5),(NULL,0,'2022-12-14 19:25:46',NULL,298,42,79,6),(NULL,0,'2022-12-14 19:25:46',NULL,299,42,77,7),(NULL,0,'2022-12-14 19:25:46',NULL,300,42,78,8),(NULL,0,'2022-12-14 19:25:46',NULL,301,42,75,9),(NULL,0,'2022-12-14 19:25:46',NULL,302,42,51,10),(NULL,0,'2022-12-14 19:25:46',NULL,303,42,53,11),(NULL,0,'2022-12-14 19:25:46',NULL,304,43,73,0),(NULL,0,'2022-12-14 19:25:46',NULL,305,43,76,1),(NULL,0,'2022-12-14 19:25:46',NULL,306,43,77,2),(NULL,0,'2022-12-14 19:25:46',NULL,307,43,74,3),(NULL,0,'2022-12-14 19:25:46',NULL,308,43,22,4),(NULL,0,'2022-12-14 19:25:46',NULL,309,43,79,5),(NULL,0,'2022-12-14 19:25:46',NULL,310,43,47,6),(NULL,0,'2022-12-14 19:25:46',NULL,311,43,48,7),(NULL,0,'2022-12-14 19:25:46',NULL,312,43,78,8),(NULL,0,'2022-12-14 19:25:46',NULL,313,43,75,9),(NULL,0,'2022-12-14 19:25:46',NULL,314,43,51,10),(NULL,0,'2022-12-14 19:25:46',NULL,315,43,53,11),(NULL,0,'2022-12-14 19:25:46',NULL,316,44,76,0),(NULL,0,'2022-12-14 19:25:46',NULL,317,44,80,1),(NULL,0,'2022-12-14 19:25:46',NULL,318,44,77,2),(NULL,0,'2022-12-14 19:25:46',NULL,319,44,74,3),(NULL,0,'2022-12-14 19:25:46',NULL,320,44,22,4),(NULL,0,'2022-12-14 19:25:46',NULL,321,44,79,5),(NULL,0,'2022-12-14 19:25:46',NULL,322,44,47,6),(NULL,0,'2022-12-14 19:25:46',NULL,323,44,48,7),(NULL,0,'2022-12-14 19:25:46',NULL,324,44,78,8),(NULL,0,'2022-12-14 19:25:46',NULL,325,44,75,9),(NULL,0,'2022-12-14 19:25:46',NULL,326,44,51,10),(NULL,0,'2022-12-14 19:25:46',NULL,327,44,53,11),(NULL,0,'2022-12-14 19:25:46',NULL,328,45,81,0),(NULL,0,'2022-12-14 19:25:46',NULL,329,45,84,1),(NULL,0,'2022-12-14 19:25:46',NULL,330,45,82,2),(NULL,0,'2022-12-14 19:25:46',NULL,331,45,83,3),(NULL,0,'2022-12-14 19:25:46',NULL,332,45,34,4),(NULL,0,'2022-12-14 19:25:46',NULL,333,45,22,5),(NULL,0,'2022-12-14 19:25:46',NULL,334,45,86,6),(NULL,0,'2022-12-14 19:25:46',NULL,335,45,87,7),(NULL,0,'2022-12-14 19:25:46',NULL,336,45,85,8),(NULL,0,'2022-12-14 19:25:46',NULL,337,45,88,9),(NULL,0,'2022-12-14 19:25:46',NULL,338,46,81,0),(NULL,0,'2022-12-14 19:25:46',NULL,339,46,84,1),(NULL,0,'2022-12-14 19:25:46',NULL,340,46,82,2),(NULL,0,'2022-12-14 19:25:46',NULL,341,46,83,3),(NULL,0,'2022-12-14 19:25:46',NULL,342,46,22,4),(NULL,0,'2022-12-14 19:25:46',NULL,343,46,85,5),(NULL,0,'2022-12-14 19:25:46',NULL,344,46,86,6),(NULL,0,'2022-12-14 19:25:46',NULL,345,46,88,7),(NULL,0,'2022-12-14 19:25:46',NULL,346,47,81,0),(NULL,0,'2022-12-14 19:25:46',NULL,347,47,84,1),(NULL,0,'2022-12-14 19:25:46',NULL,348,47,82,2),(NULL,0,'2022-12-14 19:25:46',NULL,349,47,83,3),(NULL,0,'2022-12-14 19:25:46',NULL,350,47,22,4),(NULL,0,'2022-12-14 19:25:46',NULL,351,47,85,5),(NULL,0,'2022-12-14 19:25:46',NULL,352,47,88,6),(NULL,0,'2022-12-14 19:25:46',NULL,353,48,81,0),(NULL,0,'2022-12-14 19:25:46',NULL,354,48,84,1),(NULL,0,'2022-12-14 19:25:46',NULL,355,48,82,2),(NULL,0,'2022-12-14 19:25:46',NULL,356,48,83,3),(NULL,0,'2022-12-14 19:25:46',NULL,357,48,22,4),(NULL,0,'2022-12-14 19:25:46',NULL,358,48,85,5),(NULL,0,'2022-12-14 19:25:46',NULL,359,49,89,0),(NULL,0,'2022-12-14 19:25:46',NULL,360,49,90,1),(NULL,0,'2022-12-14 19:25:46',NULL,361,49,91,2),(NULL,0,'2022-12-14 19:25:46',NULL,362,49,94,3),(NULL,0,'2022-12-14 19:25:46',NULL,363,49,92,4),(NULL,0,'2022-12-14 19:25:46',NULL,364,49,93,5),(NULL,0,'2022-12-14 19:25:46',NULL,365,49,22,6),(NULL,0,'2022-12-14 19:25:46',NULL,366,50,89,0),(NULL,0,'2022-12-14 19:25:46',NULL,367,50,90,1),(NULL,0,'2022-12-14 19:25:46',NULL,368,50,91,2),(NULL,0,'2022-12-14 19:25:46',NULL,369,50,92,3),(NULL,0,'2022-12-14 19:25:46',NULL,370,50,93,4),(NULL,0,'2022-12-14 19:25:46',NULL,371,50,22,5),(NULL,0,'2022-12-14 19:25:46',NULL,372,51,89,0),(NULL,0,'2022-12-14 19:25:46',NULL,373,51,90,1),(NULL,0,'2022-12-14 19:25:46',NULL,374,51,91,2),(NULL,0,'2022-12-14 19:25:46',NULL,375,51,92,3),(NULL,0,'2022-12-14 19:25:46',NULL,376,51,93,4),(NULL,0,'2022-12-14 19:25:46',NULL,377,51,22,5),(NULL,0,'2023-01-11 17:25:51','2023-07-10 18:43:28',378,27,95,4),('2023-01-11 21:21:47',1,'2023-01-11 18:14:03','2023-01-11 21:21:47',379,35,97,7),('2023-05-23 15:20:09',1,'2023-05-23 14:59:07','2023-05-23 15:20:09',380,41,99,10),(NULL,0,'2023-05-23 14:59:21','2023-05-23 15:20:09',381,41,100,10),(NULL,0,'2023-05-23 15:18:22','2023-05-23 15:20:09',382,41,101,11),(NULL,0,'2023-05-23 15:20:18',NULL,383,41,99,12),(NULL,0,'2023-07-10 18:43:28',NULL,384,27,10,1),(NULL,0,'2023-07-11 15:13:59',NULL,385,46,102,8);
/*!40000 ALTER TABLE `c_ci_type_attribute_group_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_ci_type_attribute_groups`
--

DROP TABLE IF EXISTS `c_ci_type_attribute_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_ci_type_attribute_groups` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `type_id` int(11) NOT NULL,
  `order` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `type_id` (`type_id`),
  KEY `ix_c_ci_type_attribute_groups_deleted` (`deleted`),
  CONSTRAINT `c_ci_type_attribute_groups_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `c_ci_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_ci_type_attribute_groups`
--

LOCK TABLES `c_ci_type_attribute_groups` WRITE;
/*!40000 ALTER TABLE `c_ci_type_attribute_groups` DISABLE KEYS */;
INSERT INTO `c_ci_type_attribute_groups` VALUES ('2022-12-14 19:25:45',1,'2021-11-24 10:51:36','2022-12-14 19:25:45',1,'系统',4,1),('2022-12-14 19:25:45',1,'2021-11-24 11:03:27','2022-12-14 19:25:45',2,'业务',4,2),('2022-12-14 19:25:46',1,'2021-11-24 11:04:35','2022-12-14 19:25:46',3,'硬件',4,3),('2022-12-14 19:25:46',1,'2021-11-24 11:24:02','2022-12-14 19:25:46',4,'位置',4,4),('2022-12-14 19:25:46',1,'2021-11-24 11:45:05','2022-12-14 19:25:46',5,'业务',5,1),('2022-12-14 19:25:46',1,'2021-11-24 11:45:59','2022-12-14 19:25:46',6,'系统',5,2),('2022-12-14 19:25:46',1,'2021-11-24 11:46:53','2022-12-14 19:25:46',7,'硬件',5,3),('2022-12-14 19:25:46',1,'2021-11-24 11:47:10','2022-12-14 19:25:46',8,'位置',5,4),('2022-12-14 19:25:46',1,'2021-11-24 11:50:20','2022-12-14 19:25:46',9,'默认',6,1),('2022-12-14 19:25:46',1,'2021-11-24 11:53:31','2022-12-14 19:25:46',10,'默认',7,1),('2022-12-14 19:25:46',1,'2021-11-24 11:57:52','2022-12-14 19:25:46',11,'默认',8,1),('2022-12-14 19:25:46',1,'2021-11-24 12:00:51','2022-12-14 19:25:46',12,'默认',9,1),('2022-12-14 19:25:45',1,'2022-08-22 19:52:07','2022-12-14 19:25:45',13,'默认',1,0),('2022-12-14 19:25:45',1,'2022-08-23 08:57:24','2022-12-14 19:25:45',14,'默认',3,1),('2022-11-23 11:19:56',1,'2022-11-23 11:19:36','2022-11-23 11:19:56',15,'test',1,2),('2022-12-14 19:25:46',1,'2022-12-02 13:33:46','2022-12-14 19:25:46',16,'默认',28,1),('2022-12-14 19:25:46',1,'2022-12-02 13:36:24','2022-12-14 19:25:46',17,'默认',29,1),('2022-12-14 19:25:46',1,'2022-12-02 13:38:26','2022-12-14 19:25:46',18,'默认',30,1),('2022-12-14 19:25:46',1,'2022-12-02 13:48:47','2022-12-14 19:25:46',19,'默认',31,1),('2022-12-14 19:25:46',1,'2022-12-02 14:10:53','2022-12-14 19:25:46',20,'默认',32,1),('2022-12-14 19:25:46',1,'2022-12-02 14:13:45','2022-12-14 19:25:46',21,'默认',33,1),('2022-12-14 19:25:46',1,'2022-12-02 14:15:33','2022-12-14 19:25:46',22,'默认',34,1),('2022-12-14 19:25:46',1,'2022-12-02 14:17:30','2022-12-14 19:25:46',23,'默认',35,1),('2022-12-14 19:25:46',1,'2022-12-02 14:20:13','2022-12-14 19:25:46',24,'默认',36,1),('2022-12-14 19:25:46',1,'2022-12-02 14:30:29','2022-12-14 19:25:46',25,'默认',37,1),('2022-12-14 19:25:46',1,'2022-12-02 14:31:07','2022-12-14 19:25:46',26,'默认',38,1),(NULL,0,'2022-08-22 19:52:07','2022-11-23 11:19:56',27,'默认',1,0),(NULL,0,'2022-08-23 08:57:24','2022-08-23 08:57:24',28,'默认',3,1),(NULL,0,'2021-11-24 10:51:36','2023-01-09 15:56:43',29,'系统',4,1),(NULL,0,'2021-11-24 11:03:27','2023-01-09 15:56:43',30,'业务',4,2),(NULL,0,'2021-11-24 11:04:35','2023-01-09 15:55:57',31,'硬件',4,3),(NULL,0,'2021-11-24 11:24:02','2023-01-09 15:55:57',32,'位置',4,4),(NULL,0,'2021-11-24 11:45:05','2021-11-24 11:45:05',33,'业务',5,1),(NULL,0,'2021-11-24 11:45:59','2021-11-24 11:45:59',34,'系统',5,2),(NULL,0,'2021-11-24 11:46:53','2021-11-24 11:46:53',35,'硬件',5,3),(NULL,0,'2021-11-24 11:47:10','2023-01-05 18:54:49',36,'555',5,4),(NULL,0,'2021-11-24 11:50:20','2021-11-24 11:50:20',37,'默认',6,1),(NULL,0,'2021-11-24 11:53:31','2021-11-24 11:53:31',38,'默认',7,1),(NULL,0,'2021-11-24 11:57:52','2021-11-24 11:57:52',39,'默认',8,1),(NULL,0,'2021-11-24 12:00:51','2021-11-24 12:00:51',40,'默认',9,1),(NULL,0,'2022-12-02 13:33:46','2022-12-02 13:33:46',41,'默认',28,1),(NULL,0,'2022-12-02 13:36:24','2022-12-02 13:36:24',42,'默认',29,1),(NULL,0,'2022-12-02 13:38:26','2022-12-02 13:38:26',43,'默认',30,1),(NULL,0,'2022-12-02 13:48:47','2022-12-02 13:48:47',44,'默认',31,1),(NULL,0,'2022-12-02 14:10:53','2022-12-15 10:39:37',45,'默认1',32,1),(NULL,0,'2022-12-02 14:13:45','2022-12-02 14:13:45',46,'默认',33,1),(NULL,0,'2022-12-02 14:15:33','2022-12-02 14:15:33',47,'默认',34,1),(NULL,0,'2022-12-02 14:17:30','2022-12-02 14:17:30',48,'默认',35,1),(NULL,0,'2022-12-02 14:20:13','2022-12-02 14:20:13',49,'默认',36,1),(NULL,0,'2022-12-02 14:30:29','2022-12-02 14:30:29',50,'默认',37,1),(NULL,0,'2022-12-02 14:31:07','2022-12-02 14:31:07',51,'默认',38,1),(NULL,0,'2022-12-26 22:07:48','2022-12-26 22:07:48',52,'test',7,2);
/*!40000 ALTER TABLE `c_ci_type_attribute_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_ci_type_attributes`
--

DROP TABLE IF EXISTS `c_ci_type_attributes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_ci_type_attributes` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` int(11) NOT NULL,
  `attr_id` int(11) NOT NULL,
  `order` int(11) DEFAULT NULL,
  `is_required` tinyint(1) DEFAULT NULL,
  `default_show` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `type_id` (`type_id`),
  KEY `attr_id` (`attr_id`),
  KEY `ix_c_ci_type_attributes_deleted` (`deleted`),
  CONSTRAINT `c_ci_type_attributes_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `c_ci_types` (`id`),
  CONSTRAINT `c_ci_type_attributes_ibfk_2` FOREIGN KEY (`attr_id`) REFERENCES `c_attributes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=432 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_ci_type_attributes`
--

LOCK TABLES `c_ci_type_attributes` WRITE;
/*!40000 ALTER TABLE `c_ci_type_attributes` DISABLE KEYS */;
INSERT INTO `c_ci_type_attributes` VALUES (NULL,0,'2022-12-14 19:25:44',NULL,222,1,1,0,1,1),(NULL,0,'2022-12-14 19:25:44',NULL,223,1,10,1,0,1),(NULL,0,'2022-12-14 19:25:44',NULL,224,1,11,2,0,1),(NULL,0,'2022-12-14 19:25:44',NULL,225,1,12,3,0,1),(NULL,0,'2022-12-14 19:25:44',NULL,226,2,2,0,1,1),(NULL,0,'2022-12-14 19:25:44',NULL,227,2,13,0,0,1),(NULL,0,'2022-12-14 19:25:44',NULL,228,2,14,0,0,1),(NULL,0,'2022-12-14 19:25:44',NULL,229,2,15,0,0,1),(NULL,0,'2022-12-14 19:25:44',NULL,230,2,16,0,0,1),(NULL,0,'2022-12-14 19:25:44',NULL,231,3,3,0,1,1),(NULL,0,'2022-12-14 19:25:44',NULL,232,3,17,1,0,1),(NULL,0,'2022-12-14 19:25:44',NULL,233,3,18,2,0,1),(NULL,0,'2022-12-14 19:25:44',NULL,234,3,19,3,0,1),(NULL,0,'2022-12-14 19:25:44',NULL,235,3,20,4,0,1),(NULL,0,'2022-12-14 19:25:44',NULL,236,3,21,5,0,1),(NULL,0,'2022-12-14 19:25:44',NULL,237,3,22,6,0,1),(NULL,0,'2022-12-14 19:25:44',NULL,238,4,23,0,1,1),(NULL,0,'2022-12-14 19:25:44',NULL,239,4,24,1,0,1),(NULL,0,'2022-12-14 19:25:44',NULL,240,4,25,2,1,1),(NULL,0,'2022-12-14 19:25:44',NULL,241,4,26,3,0,1),(NULL,0,'2022-12-14 19:25:44',NULL,242,4,27,4,0,0),(NULL,0,'2022-12-14 19:25:44',NULL,243,4,28,5,0,0),(NULL,0,'2022-12-14 19:25:44',NULL,244,4,29,6,0,0),(NULL,0,'2022-12-14 19:25:44',NULL,245,4,30,7,0,0),(NULL,0,'2022-12-14 19:25:44',NULL,246,4,31,8,0,0),(NULL,0,'2022-12-14 19:25:44',NULL,247,4,32,9,0,0),(NULL,0,'2022-12-14 19:25:44',NULL,248,4,20,10,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,249,4,22,11,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,250,4,33,12,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,251,4,34,13,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,252,4,35,14,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,253,4,4,15,1,1),(NULL,0,'2022-12-14 19:25:45',NULL,254,4,36,16,0,0),(NULL,0,'2022-12-14 19:25:45',NULL,255,4,37,17,0,0),(NULL,0,'2022-12-14 19:25:45',NULL,256,4,38,18,0,0),(NULL,0,'2022-12-14 19:25:45',NULL,257,4,39,19,0,0),(NULL,0,'2022-12-14 19:25:45',NULL,258,4,40,20,0,0),(NULL,0,'2022-12-14 19:25:45',NULL,259,4,41,21,0,0),(NULL,0,'2022-12-14 19:25:45',NULL,260,4,43,22,0,0),(NULL,0,'2022-12-14 19:25:45',NULL,261,4,42,23,0,0),(NULL,0,'2022-12-14 19:25:45',NULL,262,4,44,24,0,0),(NULL,0,'2022-12-14 19:25:45',NULL,263,4,45,25,0,0),(NULL,0,'2022-12-14 19:25:45',NULL,264,4,46,26,0,0),(NULL,0,'2022-12-14 19:25:45',NULL,266,4,48,28,0,0),(NULL,0,'2022-12-14 19:25:45',NULL,267,4,49,29,0,0),(NULL,0,'2022-12-14 19:25:45',NULL,269,4,51,31,0,0),(NULL,0,'2022-12-14 19:25:45',NULL,272,5,54,0,1,1),(NULL,0,'2022-12-14 19:25:45',NULL,273,5,62,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,274,5,24,1,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,275,5,34,2,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,276,5,35,3,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,277,5,20,4,0,1),(NULL,0,'2022-12-14 19:25:45','2023-02-07 13:53:38',278,5,22,5,0,0),(NULL,0,'2022-12-14 19:25:45',NULL,279,5,33,6,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,280,5,32,7,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,281,5,5,8,1,1),(NULL,0,'2022-12-14 19:25:45',NULL,282,5,55,9,0,0),(NULL,0,'2022-12-14 19:25:45',NULL,283,5,25,10,1,1),(NULL,0,'2022-12-14 19:25:45',NULL,284,5,26,11,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,285,5,31,12,0,0),(NULL,0,'2022-12-14 19:25:45',NULL,286,5,56,13,0,0),(NULL,0,'2022-12-14 19:25:45',NULL,287,5,57,14,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,288,5,30,15,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,289,5,36,16,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,290,5,37,17,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,291,5,40,18,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,292,5,39,19,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,293,5,58,20,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,294,5,41,21,0,0),(NULL,0,'2022-12-14 19:25:45',NULL,295,5,47,22,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,296,5,49,23,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,297,5,50,24,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,298,6,6,0,1,1),(NULL,0,'2022-12-14 19:25:45',NULL,299,6,39,1,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,300,6,59,2,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,301,6,60,3,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,302,6,40,4,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,303,7,7,0,1,1),(NULL,0,'2022-12-14 19:25:45',NULL,304,7,61,1,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,305,7,62,2,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,306,7,63,3,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,307,7,64,4,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,308,8,8,0,1,1),(NULL,0,'2022-12-14 19:25:45',NULL,309,8,65,1,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,310,8,66,2,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,311,8,67,3,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,312,8,68,4,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,313,8,69,5,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,314,9,9,0,1,1),(NULL,0,'2022-12-14 19:25:45',NULL,315,9,25,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,316,9,47,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,317,9,35,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,318,9,34,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,319,9,57,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,320,28,71,0,1,1),(NULL,0,'2022-12-14 19:25:45',NULL,321,28,48,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,322,28,47,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,323,28,74,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,324,28,75,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,325,28,76,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,326,28,77,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,327,28,51,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,329,28,53,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,331,28,79,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,332,29,72,0,1,1),(NULL,0,'2022-12-14 19:25:45',NULL,333,29,74,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,334,29,75,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,335,29,76,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,336,29,77,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,337,29,78,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,338,29,47,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,339,29,48,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,340,29,51,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,341,29,53,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,342,29,22,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,343,29,79,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,344,30,73,0,1,1),(NULL,0,'2022-12-14 19:25:45',NULL,345,30,74,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,346,30,75,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,347,30,76,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,348,30,77,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,349,30,78,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,350,30,47,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,351,30,48,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,352,30,51,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,353,30,53,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,354,30,22,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,355,30,79,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,356,31,80,0,1,1),(NULL,0,'2022-12-14 19:25:45',NULL,357,31,74,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,358,31,75,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,359,31,76,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,360,31,77,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,361,31,78,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,362,31,79,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,363,31,51,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,364,31,53,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,365,31,22,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,366,31,48,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,367,31,47,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,368,32,81,0,1,1),(NULL,0,'2022-12-14 19:25:45',NULL,369,32,82,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,370,32,83,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,371,32,84,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,372,32,34,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,373,32,85,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,374,32,86,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,375,32,87,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,376,32,88,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,377,32,22,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,378,33,81,0,1,1),(NULL,0,'2022-12-14 19:25:45',NULL,379,33,82,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,380,33,83,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,381,33,84,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,382,33,85,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,383,33,22,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,384,33,86,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,385,33,88,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,386,34,81,0,1,1),(NULL,0,'2022-12-14 19:25:45',NULL,387,34,82,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,388,34,83,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,389,34,84,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,390,34,85,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,391,34,22,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,392,34,88,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,393,35,81,0,1,1),(NULL,0,'2022-12-14 19:25:45',NULL,394,35,82,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,395,35,83,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,396,35,84,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,397,35,85,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,398,35,22,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,399,36,89,0,1,1),(NULL,0,'2022-12-14 19:25:45',NULL,400,36,90,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,401,36,91,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,402,36,92,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,403,36,93,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,404,36,22,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,405,36,94,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,406,37,89,0,1,1),(NULL,0,'2022-12-14 19:25:45',NULL,407,37,22,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,408,37,90,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,409,37,91,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,410,37,92,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,411,37,93,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,412,38,89,0,1,1),(NULL,0,'2022-12-14 19:25:45',NULL,413,38,22,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,414,38,90,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,415,38,91,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,416,38,92,0,0,1),(NULL,0,'2022-12-14 19:25:45',NULL,417,38,93,0,0,1),(NULL,0,'2023-01-11 17:25:50','2023-01-11 17:25:50',420,1,95,0,0,0),(NULL,0,'2023-05-23 14:59:21','2023-05-23 14:59:21',428,28,100,0,0,0),(NULL,0,'2023-05-23 15:18:21','2023-05-23 15:18:21',429,28,101,0,0,0),(NULL,0,'2023-05-23 15:20:18',NULL,430,28,99,0,0,1),(NULL,0,'2023-07-11 15:13:59','2023-07-11 15:13:59',431,33,102,0,1,0),(NULL, 0, '2024-03-20 10:51:55', '2024-03-20 10:52:55', 432, 4, 47, 27, 0, 1);
/*!40000 ALTER TABLE `c_ci_type_attributes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_ci_type_group_items`
--

DROP TABLE IF EXISTS `c_ci_type_group_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_ci_type_group_items` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  `order` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `group_id` (`group_id`),
  KEY `type_id` (`type_id`),
  KEY `ix_c_ci_type_group_items_deleted` (`deleted`),
  CONSTRAINT `c_ci_type_group_items_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `c_ci_type_groups` (`id`),
  CONSTRAINT `c_ci_type_group_items_ibfk_2` FOREIGN KEY (`type_id`) REFERENCES `c_ci_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_ci_type_group_items`
--

LOCK TABLES `c_ci_type_group_items` WRITE;
/*!40000 ALTER TABLE `c_ci_type_group_items` DISABLE KEYS */;
INSERT INTO `c_ci_type_group_items` VALUES (NULL,0,'2022-12-14 19:25:44',NULL,23,1,1,0),(NULL,0,'2022-12-14 19:25:44','2023-07-11 12:21:17',24,1,2,1),(NULL,0,'2022-12-14 19:25:44','2023-07-11 12:21:17',25,1,3,2),(NULL,0,'2022-12-14 19:25:44','2023-07-10 18:37:44',26,2,4,3),(NULL,0,'2022-12-14 19:25:44','2023-07-10 18:37:44',27,2,5,2),(NULL,0,'2022-12-14 19:25:44','2023-07-10 18:37:44',28,2,7,4),(NULL,0,'2022-12-14 19:25:44','2023-07-10 18:37:44',29,2,8,6),(NULL,0,'2022-12-14 19:25:44','2023-07-10 18:37:44',30,2,6,1),(NULL,0,'2022-12-14 19:25:44','2023-07-10 18:35:53',31,4,28,1),(NULL,0,'2022-12-14 19:25:44','2023-07-10 18:35:53',32,4,29,2),('2023-07-10 18:35:07',1,'2022-12-14 19:25:44','2023-07-10 18:35:07',33,4,30,3),(NULL,0,'2022-12-14 19:25:44','2023-07-10 18:35:03',34,4,31,0),(NULL,0,'2022-12-14 19:25:44',NULL,35,5,32,0),(NULL,0,'2022-12-14 19:25:44','2023-01-04 18:22:47',36,5,33,1),(NULL,0,'2022-12-14 19:25:44','2023-01-04 18:22:47',37,5,34,2),(NULL,0,'2022-12-14 19:25:44','2023-01-04 18:22:47',38,5,35,3),(NULL,0,'2022-12-14 19:25:44',NULL,39,6,36,0),(NULL,0,'2022-12-14 19:25:44',NULL,40,6,37,1),(NULL,0,'2022-12-14 19:25:44',NULL,41,6,38,2),(NULL,0,'2022-12-14 19:25:44',NULL,42,3,9,0),(NULL,0,'2023-07-10 18:35:07','2023-07-10 18:35:21',47,2,30,0);
/*!40000 ALTER TABLE `c_ci_type_group_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_ci_type_groups`
--

DROP TABLE IF EXISTS `c_ci_type_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_ci_type_groups` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `order` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_c_ci_type_groups_deleted` (`deleted`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_ci_type_groups`
--

LOCK TABLES `c_ci_type_groups` WRITE;
/*!40000 ALTER TABLE `c_ci_type_groups` DISABLE KEYS */;
INSERT INTO `c_ci_type_groups` VALUES (NULL,0,'2021-11-23 19:49:05','2022-10-19 14:43:24',1,'业务',0),(NULL,0,'2021-11-23 20:06:10','2022-12-02 13:11:27',2,'服务器',1),(NULL,0,'2021-11-24 09:43:46','2022-12-02 13:50:51',3,'容器',5),(NULL,0,'2022-12-02 13:11:36','2022-12-02 13:11:40',4,'网络设备',2),(NULL,0,'2022-12-02 13:50:33','2022-12-02 13:50:39',5,'数据库',3),(NULL,0,'2022-12-02 13:50:48','2022-12-02 13:50:51',6,'中间件',4),('2023-01-03 18:37:05',1,'2023-01-03 18:36:55','2023-01-03 18:37:05',7,'123',0);
/*!40000 ALTER TABLE `c_ci_type_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_ci_type_histories`
--

DROP TABLE IF EXISTS `c_ci_type_histories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_ci_type_histories` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `operate_type` enum('1','12','11','9','0','10','4','13','6','2','5','3','7','8') COLLATE utf8_unicode_ci DEFAULT NULL,
  `type_id` int(11) NOT NULL,
  `attr_id` int(11) DEFAULT NULL,
  `trigger_id` int(11) DEFAULT NULL,
  `unique_constraint_id` int(11) DEFAULT NULL,
  `uid` int(11) DEFAULT NULL,
  `change` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_c_ci_type_histories_uid` (`uid`),
  KEY `ix_c_ci_type_histories_deleted` (`deleted`),
  KEY `ix_c_ci_type_histories_type_id` (`type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=367 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_ci_type_histories`
--

LOCK TABLES `c_ci_type_histories` WRITE;
/*!40000 ALTER TABLE `c_ci_type_histories` DISABLE KEYS */;
INSERT INTO `c_ci_type_histories` VALUES (NULL,0,'2022-10-17 17:05:07',NULL,1,'4',4,34,NULL,NULL,1,'{\"new\": {\"id\": 34, \"uid\": null, \"name\": \"status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:01:59\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 17:05:07\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"在线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#065C30\", \"backgroundColor\": \"#D9F7BE\"}}], [\"下线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#881111\", \"backgroundColor\": \"#FFCCC7\"}}], [\"待用\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#0A483F\", \"backgroundColor\": \"#BAE7FF\"}}], [\"维修\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#622C0A\", \"backgroundColor\": \"#FFD8BF\"}}], [\"重装\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#5C4D0E\", \"backgroundColor\": \"#FFF1B8\"}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 34, \"uid\": null, \"name\": \"status\", \"alias\": \"状态\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:01:59\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"在线\", null], [\"备用\", null], [\"下线\", null], [\"待用\", null], [\"维修\", null], [\"重装\", null]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2022-10-17 17:05:07',NULL,2,'4',5,34,NULL,NULL,1,'{\"new\": {\"id\": 34, \"uid\": null, \"name\": \"status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:01:59\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 17:05:07\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"在线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#065C30\", \"backgroundColor\": \"#D9F7BE\"}}], [\"下线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#881111\", \"backgroundColor\": \"#FFCCC7\"}}], [\"待用\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#0A483F\", \"backgroundColor\": \"#BAE7FF\"}}], [\"维修\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#622C0A\", \"backgroundColor\": \"#FFD8BF\"}}], [\"重装\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#5C4D0E\", \"backgroundColor\": \"#FFF1B8\"}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 34, \"uid\": null, \"name\": \"status\", \"alias\": \"状态\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:01:59\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"在线\", null], [\"备用\", null], [\"下线\", null], [\"待用\", null], [\"维修\", null], [\"重装\", null]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2022-10-17 17:05:07',NULL,3,'4',9,34,NULL,NULL,1,'{\"new\": {\"id\": 34, \"uid\": null, \"name\": \"status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:01:59\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 17:05:07\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"在线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#065C30\", \"backgroundColor\": \"#D9F7BE\"}}], [\"下线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#881111\", \"backgroundColor\": \"#FFCCC7\"}}], [\"待用\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#0A483F\", \"backgroundColor\": \"#BAE7FF\"}}], [\"维修\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#622C0A\", \"backgroundColor\": \"#FFD8BF\"}}], [\"重装\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#5C4D0E\", \"backgroundColor\": \"#FFF1B8\"}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 34, \"uid\": null, \"name\": \"status\", \"alias\": \"状态\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:01:59\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"在线\", null], [\"备用\", null], [\"下线\", null], [\"待用\", null], [\"维修\", null], [\"重装\", null]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2022-10-17 17:08:17',NULL,4,'4',4,35,NULL,NULL,1,'{\"new\": {\"id\": 35, \"uid\": null, \"name\": \"env\", \"alias\": \"环境\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:03:04\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 17:08:17\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"test\", {\"icon\": {\"name\": \"huiyiguanli\", \"color\": \"\"}, \"style\": {}}], [\"ppe\", {\"icon\": {\"name\": \"renwuguanli\", \"color\": \"\"}, \"style\": {}}], [\"prod\", {\"icon\": {\"name\": \"jiangbei\", \"color\": \"\"}, \"style\": {}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 35, \"uid\": null, \"name\": \"env\", \"alias\": \"环境\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:03:04\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"test\", null], [\"ppe\", null], [\"prod\", null], [\"测试\", null], [\"生产\", null]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2022-10-17 17:08:17',NULL,5,'4',5,35,NULL,NULL,1,'{\"new\": {\"id\": 35, \"uid\": null, \"name\": \"env\", \"alias\": \"环境\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:03:04\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 17:08:17\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"test\", {\"icon\": {\"name\": \"huiyiguanli\", \"color\": \"\"}, \"style\": {}}], [\"ppe\", {\"icon\": {\"name\": \"renwuguanli\", \"color\": \"\"}, \"style\": {}}], [\"prod\", {\"icon\": {\"name\": \"jiangbei\", \"color\": \"\"}, \"style\": {}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 35, \"uid\": null, \"name\": \"env\", \"alias\": \"环境\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:03:04\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"test\", null], [\"ppe\", null], [\"prod\", null], [\"测试\", null], [\"生产\", null]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2022-10-17 17:08:17',NULL,6,'4',9,35,NULL,NULL,1,'{\"new\": {\"id\": 35, \"uid\": null, \"name\": \"env\", \"alias\": \"环境\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:03:04\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 17:08:17\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"test\", {\"icon\": {\"name\": \"huiyiguanli\", \"color\": \"\"}, \"style\": {}}], [\"ppe\", {\"icon\": {\"name\": \"renwuguanli\", \"color\": \"\"}, \"style\": {}}], [\"prod\", {\"icon\": {\"name\": \"jiangbei\", \"color\": \"\"}, \"style\": {}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 35, \"uid\": null, \"name\": \"env\", \"alias\": \"环境\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:03:04\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"test\", null], [\"ppe\", null], [\"prod\", null], [\"测试\", null], [\"生产\", null]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2022-10-17 17:09:31',NULL,7,'4',4,47,NULL,NULL,1,'{\"new\": {\"id\": 47, \"uid\": null, \"name\": \"idc\", \"alias\": \"IDC\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:15:27\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 17:09:31\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"choice_value\": [[\"南汇\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#305B09\", \"fontStyle\": \"italic\", \"fontWeight\": \"bold\"}}], [\"张江\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#05302A\", \"fontStyle\": \"italic\", \"fontWeight\": \"bold\"}}], [\"外高桥\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#0C2659\", \"fontStyle\": \"italic\", \"fontWeight\": \"bold\"}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 47, \"uid\": null, \"name\": \"idc\", \"alias\": \"IDC\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:15:27\", \"deleted_at\": null, \"updated_at\": \"2022-08-22 20:02:36\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"choice_value\": [[\"南汇\", null], [\"张江\", null], [\"外高桥\", null]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2022-10-17 17:09:31',NULL,8,'4',5,47,NULL,NULL,1,'{\"new\": {\"id\": 47, \"uid\": null, \"name\": \"idc\", \"alias\": \"IDC\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:15:27\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 17:09:31\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"choice_value\": [[\"南汇\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#305B09\", \"fontStyle\": \"italic\", \"fontWeight\": \"bold\"}}], [\"张江\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#05302A\", \"fontStyle\": \"italic\", \"fontWeight\": \"bold\"}}], [\"外高桥\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#0C2659\", \"fontStyle\": \"italic\", \"fontWeight\": \"bold\"}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 47, \"uid\": null, \"name\": \"idc\", \"alias\": \"IDC\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:15:27\", \"deleted_at\": null, \"updated_at\": \"2022-08-22 20:02:36\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"choice_value\": [[\"南汇\", null], [\"张江\", null], [\"外高桥\", null]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2022-10-17 17:09:31',NULL,9,'4',9,47,NULL,NULL,1,'{\"new\": {\"id\": 47, \"uid\": null, \"name\": \"idc\", \"alias\": \"IDC\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:15:27\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 17:09:31\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"choice_value\": [[\"南汇\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#305B09\", \"fontStyle\": \"italic\", \"fontWeight\": \"bold\"}}], [\"张江\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#05302A\", \"fontStyle\": \"italic\", \"fontWeight\": \"bold\"}}], [\"外高桥\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#0C2659\", \"fontStyle\": \"italic\", \"fontWeight\": \"bold\"}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 47, \"uid\": null, \"name\": \"idc\", \"alias\": \"IDC\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:15:27\", \"deleted_at\": null, \"updated_at\": \"2022-08-22 20:02:36\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"choice_value\": [[\"南汇\", null], [\"张江\", null], [\"外高桥\", null]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2022-10-17 21:48:43',NULL,10,'1',1,NULL,NULL,NULL,1,'{\"new\": {\"id\": 1, \"uid\": null, \"icon\": \"weibiaoti-6$$\", \"name\": \"bu\", \"alias\": \"事业部\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 1, \"created_at\": \"2021-11-23 19:50:34\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 21:48:43\", \"is_attached\": false}, \"old\": {\"id\": 1, \"uid\": null, \"icon\": null, \"name\": \"bu\", \"alias\": \"事业部\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 1, \"created_at\": \"2021-11-23 19:50:34\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}}'),(NULL,0,'2022-10-17 21:49:31',NULL,11,'1',2,NULL,NULL,NULL,1,'{\"new\": {\"id\": 2, \"uid\": null, \"icon\": \"camear$$\", \"name\": \"product\", \"alias\": \"产品\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 2, \"created_at\": \"2021-11-23 19:56:40\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 21:49:31\", \"is_attached\": false}, \"old\": {\"id\": 2, \"uid\": null, \"icon\": null, \"name\": \"product\", \"alias\": \"产品\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 2, \"created_at\": \"2021-11-23 19:56:40\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}}'),(NULL,0,'2022-10-17 21:50:00',NULL,12,'1',3,NULL,NULL,NULL,1,'{\"new\": {\"id\": 3, \"uid\": null, \"icon\": \"renwuguanli$$\", \"name\": \"project\", \"alias\": \"应用\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 3, \"created_at\": \"2021-11-23 19:58:15\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 21:50:00\", \"is_attached\": false}, \"old\": {\"id\": 3, \"uid\": null, \"icon\": null, \"name\": \"project\", \"alias\": \"应用\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 3, \"created_at\": \"2021-11-23 19:58:15\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}}'),(NULL,0,'2022-10-19 14:53:05',NULL,13,'3',10,4,NULL,NULL,9,'{\"id\": 4, \"uid\": null, \"name\": \"sn\", \"alias\": \"服务器序列号\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 20:06:49\", \"deleted_at\": null, \"updated_at\": \"2021-11-24 11:04:21\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 14:53:05',NULL,14,'0',10,NULL,NULL,NULL,9,'{\"id\": 10, \"uid\": 9, \"icon\": \"\", \"name\": \"server01\", \"alias\": \"server01\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 14:53:05\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-10-19 14:56:56',NULL,15,'3',11,4,NULL,NULL,9,'{\"id\": 4, \"uid\": null, \"name\": \"sn\", \"alias\": \"服务器序列号\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 20:06:49\", \"deleted_at\": null, \"updated_at\": \"2021-11-24 11:04:21\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 14:56:56',NULL,16,'0',11,NULL,NULL,NULL,9,'{\"id\": 11, \"uid\": 9, \"icon\": \"\", \"name\": \"server002\", \"alias\": \"server002\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 14:56:56\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-10-19 14:57:09',NULL,17,'2',11,NULL,NULL,NULL,9,'{\"id\": 11, \"uid\": 9, \"icon\": \"\", \"name\": \"server002\", \"alias\": \"server002\", \"order\": 0, \"deleted\": true, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 14:56:56\", \"deleted_at\": \"2022-10-19 14:57:09\", \"updated_at\": \"2022-10-19 14:57:09\", \"is_attached\": false}'),(NULL,0,'2022-10-19 14:57:13',NULL,18,'2',10,NULL,NULL,NULL,9,'{\"id\": 10, \"uid\": 9, \"icon\": \"\", \"name\": \"server01\", \"alias\": \"server01\", \"order\": 0, \"deleted\": true, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 14:53:05\", \"deleted_at\": \"2022-10-19 14:57:13\", \"updated_at\": \"2022-10-19 14:57:13\", \"is_attached\": false}'),(NULL,0,'2022-10-19 14:57:39',NULL,19,'3',12,4,NULL,NULL,9,'{\"id\": 4, \"uid\": null, \"name\": \"sn\", \"alias\": \"服务器序列号\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 20:06:49\", \"deleted_at\": null, \"updated_at\": \"2021-11-24 11:04:21\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 14:57:39',NULL,20,'0',12,NULL,NULL,NULL,9,'{\"id\": 12, \"uid\": 9, \"icon\": \"\", \"name\": \"server01\", \"alias\": \"server01\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 14:57:39\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-10-19 14:58:53',NULL,21,'2',12,NULL,NULL,NULL,9,'{\"id\": 12, \"uid\": 9, \"icon\": \"\", \"name\": \"server01\", \"alias\": \"server01\", \"order\": 0, \"deleted\": true, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 14:57:39\", \"deleted_at\": \"2022-10-19 14:58:53\", \"updated_at\": \"2022-10-19 14:58:53\", \"is_attached\": false}'),(NULL,0,'2022-10-19 14:59:02',NULL,22,'3',13,4,NULL,NULL,9,'{\"id\": 4, \"uid\": null, \"name\": \"sn\", \"alias\": \"服务器序列号\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 20:06:49\", \"deleted_at\": null, \"updated_at\": \"2021-11-24 11:04:21\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 14:59:02',NULL,23,'0',13,NULL,NULL,NULL,9,'{\"id\": 13, \"uid\": 9, \"icon\": \"\", \"name\": \"server003\", \"alias\": \"server003\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 14:59:01\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-10-19 14:59:32',NULL,24,'2',13,NULL,NULL,NULL,9,'{\"id\": 13, \"uid\": 9, \"icon\": \"\", \"name\": \"server003\", \"alias\": \"server003\", \"order\": 0, \"deleted\": true, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 14:59:01\", \"deleted_at\": \"2022-10-19 14:59:32\", \"updated_at\": \"2022-10-19 14:59:32\", \"is_attached\": false}'),(NULL,0,'2022-10-19 15:01:46',NULL,25,'3',14,4,NULL,NULL,9,'{\"id\": 4, \"uid\": null, \"name\": \"sn\", \"alias\": \"服务器序列号\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 20:06:49\", \"deleted_at\": null, \"updated_at\": \"2021-11-24 11:04:21\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 15:01:46',NULL,26,'0',14,NULL,NULL,NULL,9,'{\"id\": 14, \"uid\": 9, \"icon\": \"\", \"name\": \"server002\", \"alias\": \"server002\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:01:46\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-10-19 15:02:14',NULL,27,'3',15,4,NULL,NULL,9,'{\"id\": 4, \"uid\": null, \"name\": \"sn\", \"alias\": \"服务器序列号\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 20:06:49\", \"deleted_at\": null, \"updated_at\": \"2021-11-24 11:04:21\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 15:02:14',NULL,28,'0',15,NULL,NULL,NULL,9,'{\"id\": 15, \"uid\": 9, \"icon\": \"\", \"name\": \"server003\", \"alias\": \"server003\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:02:14\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-10-19 15:03:25',NULL,29,'2',15,NULL,NULL,NULL,9,'{\"id\": 15, \"uid\": 9, \"icon\": \"\", \"name\": \"server003\", \"alias\": \"server003\", \"order\": 0, \"deleted\": true, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:02:14\", \"deleted_at\": \"2022-10-19 15:03:25\", \"updated_at\": \"2022-10-19 15:03:25\", \"is_attached\": false}'),(NULL,0,'2022-10-19 15:03:28',NULL,30,'2',14,NULL,NULL,NULL,9,'{\"id\": 14, \"uid\": 9, \"icon\": \"\", \"name\": \"server002\", \"alias\": \"server002\", \"order\": 0, \"deleted\": true, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:01:46\", \"deleted_at\": \"2022-10-19 15:03:28\", \"updated_at\": \"2022-10-19 15:03:28\", \"is_attached\": false}'),(NULL,0,'2022-10-19 15:04:01',NULL,31,'3',16,4,NULL,NULL,9,'{\"id\": 4, \"uid\": null, \"name\": \"sn\", \"alias\": \"服务器序列号\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 20:06:49\", \"deleted_at\": null, \"updated_at\": \"2021-11-24 11:04:21\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 15:04:01',NULL,32,'0',16,NULL,NULL,NULL,9,'{\"id\": 16, \"uid\": 9, \"icon\": \"\", \"name\": \"server03\", \"alias\": \"server03\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:04:01\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-10-19 15:04:56',NULL,33,'3',17,4,NULL,NULL,9,'{\"id\": 4, \"uid\": null, \"name\": \"sn\", \"alias\": \"服务器序列号\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 20:06:49\", \"deleted_at\": null, \"updated_at\": \"2021-11-24 11:04:21\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 15:04:56',NULL,34,'0',17,NULL,NULL,NULL,9,'{\"id\": 17, \"uid\": 9, \"icon\": \"\", \"name\": \"server003\", \"alias\": \"server003\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:04:56\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-10-19 15:06:00',NULL,35,'3',18,4,NULL,NULL,9,'{\"id\": 4, \"uid\": null, \"name\": \"sn\", \"alias\": \"服务器序列号\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 20:06:49\", \"deleted_at\": null, \"updated_at\": \"2021-11-24 11:04:21\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 15:06:00',NULL,36,'0',18,NULL,NULL,NULL,9,'{\"id\": 18, \"uid\": 9, \"icon\": \"\", \"name\": \"server0001\", \"alias\": \"server0001\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:06:00\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-10-19 15:06:38',NULL,37,'3',19,4,NULL,NULL,9,'{\"id\": 4, \"uid\": null, \"name\": \"sn\", \"alias\": \"服务器序列号\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 20:06:49\", \"deleted_at\": null, \"updated_at\": \"2021-11-24 11:04:21\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 15:06:38',NULL,38,'0',19,NULL,NULL,NULL,9,'{\"id\": 19, \"uid\": 9, \"icon\": \"\", \"name\": \"xxxxx\", \"alias\": \"xxxxx\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:06:38\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-10-19 15:06:56',NULL,39,'3',20,4,NULL,NULL,9,'{\"id\": 4, \"uid\": null, \"name\": \"sn\", \"alias\": \"服务器序列号\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 20:06:49\", \"deleted_at\": null, \"updated_at\": \"2021-11-24 11:04:21\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 15:06:56',NULL,40,'0',20,NULL,NULL,NULL,9,'{\"id\": 20, \"uid\": 9, \"icon\": \"\", \"name\": \"dfdfdfdff\", \"alias\": \"dfdfdfdff\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:06:56\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-10-19 15:07:16',NULL,41,'3',21,4,NULL,NULL,9,'{\"id\": 4, \"uid\": null, \"name\": \"sn\", \"alias\": \"服务器序列号\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 20:06:49\", \"deleted_at\": null, \"updated_at\": \"2021-11-24 11:04:21\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 15:07:16',NULL,42,'0',21,NULL,NULL,NULL,9,'{\"id\": 21, \"uid\": 9, \"icon\": \"\", \"name\": \"sdfsafdsaff\", \"alias\": \"sdfsafdsaff\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:07:16\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-10-19 15:07:21',NULL,43,'2',16,NULL,NULL,NULL,9,'{\"id\": 16, \"uid\": 9, \"icon\": \"\", \"name\": \"server03\", \"alias\": \"server03\", \"order\": 0, \"deleted\": true, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:04:01\", \"deleted_at\": \"2022-10-19 15:07:21\", \"updated_at\": \"2022-10-19 15:07:21\", \"is_attached\": false}'),(NULL,0,'2022-10-19 15:07:24',NULL,44,'2',17,NULL,NULL,NULL,9,'{\"id\": 17, \"uid\": 9, \"icon\": \"\", \"name\": \"server003\", \"alias\": \"server003\", \"order\": 0, \"deleted\": true, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:04:56\", \"deleted_at\": \"2022-10-19 15:07:24\", \"updated_at\": \"2022-10-19 15:07:24\", \"is_attached\": false}'),(NULL,0,'2022-10-19 15:07:26',NULL,45,'2',18,NULL,NULL,NULL,9,'{\"id\": 18, \"uid\": 9, \"icon\": \"\", \"name\": \"server0001\", \"alias\": \"server0001\", \"order\": 0, \"deleted\": true, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:06:00\", \"deleted_at\": \"2022-10-19 15:07:26\", \"updated_at\": \"2022-10-19 15:07:26\", \"is_attached\": false}'),(NULL,0,'2022-10-19 15:07:30',NULL,46,'2',19,NULL,NULL,NULL,9,'{\"id\": 19, \"uid\": 9, \"icon\": \"\", \"name\": \"xxxxx\", \"alias\": \"xxxxx\", \"order\": 0, \"deleted\": true, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:06:38\", \"deleted_at\": \"2022-10-19 15:07:30\", \"updated_at\": \"2022-10-19 15:07:30\", \"is_attached\": false}'),(NULL,0,'2022-10-19 15:07:33',NULL,47,'2',20,NULL,NULL,NULL,9,'{\"id\": 20, \"uid\": 9, \"icon\": \"\", \"name\": \"dfdfdfdff\", \"alias\": \"dfdfdfdff\", \"order\": 0, \"deleted\": true, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:06:56\", \"deleted_at\": \"2022-10-19 15:07:33\", \"updated_at\": \"2022-10-19 15:07:33\", \"is_attached\": false}'),(NULL,0,'2022-10-19 15:07:35',NULL,48,'2',21,NULL,NULL,NULL,9,'{\"id\": 21, \"uid\": 9, \"icon\": \"\", \"name\": \"sdfsafdsaff\", \"alias\": \"sdfsafdsaff\", \"order\": 0, \"deleted\": true, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:07:16\", \"deleted_at\": \"2022-10-19 15:07:35\", \"updated_at\": \"2022-10-19 15:07:35\", \"is_attached\": false}'),(NULL,0,'2022-10-19 15:07:47',NULL,49,'3',22,4,NULL,NULL,9,'{\"id\": 4, \"uid\": null, \"name\": \"sn\", \"alias\": \"服务器序列号\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 20:06:49\", \"deleted_at\": null, \"updated_at\": \"2021-11-24 11:04:21\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 15:07:47',NULL,50,'0',22,NULL,NULL,NULL,9,'{\"id\": 22, \"uid\": 9, \"icon\": \"\", \"name\": \"server999\", \"alias\": \"server999\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:07:47\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-10-19 15:08:30',NULL,51,'2',22,NULL,NULL,NULL,9,'{\"id\": 22, \"uid\": 9, \"icon\": \"\", \"name\": \"server999\", \"alias\": \"server999\", \"order\": 0, \"deleted\": true, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:07:47\", \"deleted_at\": \"2022-10-19 15:08:30\", \"updated_at\": \"2022-10-19 15:08:30\", \"is_attached\": false}'),(NULL,0,'2022-10-19 15:12:48',NULL,52,'3',23,4,NULL,NULL,9,'{\"id\": 4, \"uid\": null, \"name\": \"sn\", \"alias\": \"服务器序列号\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 20:06:49\", \"deleted_at\": null, \"updated_at\": \"2021-11-24 11:04:21\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 15:12:48',NULL,53,'0',23,NULL,NULL,NULL,9,'{\"id\": 23, \"uid\": 9, \"icon\": \"\", \"name\": \"dfdsfd\", \"alias\": \"dfdsfd\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:12:48\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-10-19 15:13:12',NULL,54,'2',23,NULL,NULL,NULL,9,'{\"id\": 23, \"uid\": 9, \"icon\": \"\", \"name\": \"dfdsfd\", \"alias\": \"dfdsfd\", \"order\": 0, \"deleted\": true, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:12:48\", \"deleted_at\": \"2022-10-19 15:13:12\", \"updated_at\": \"2022-10-19 15:13:12\", \"is_attached\": false}'),(NULL,0,'2022-10-19 15:14:54',NULL,55,'3',24,1,NULL,NULL,9,'{\"id\": 1, \"uid\": null, \"name\": \"bu_name\", \"alias\": \"事业部\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 19:50:29\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 15:14:54',NULL,56,'0',24,NULL,NULL,NULL,9,'{\"id\": 24, \"uid\": 9, \"icon\": \"\", \"name\": \"ghfgh\", \"alias\": \"ghfgh\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 1, \"created_at\": \"2022-10-19 15:14:54\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-10-19 15:15:53',NULL,57,'2',24,NULL,NULL,NULL,9,'{\"id\": 24, \"uid\": 9, \"icon\": \"\", \"name\": \"ghfgh\", \"alias\": \"ghfgh\", \"order\": 0, \"deleted\": true, \"enabled\": true, \"unique_id\": 1, \"created_at\": \"2022-10-19 15:14:54\", \"deleted_at\": \"2022-10-19 15:15:53\", \"updated_at\": \"2022-10-19 15:15:53\", \"is_attached\": false}'),(NULL,0,'2022-10-19 15:22:44',NULL,58,'3',25,4,NULL,NULL,9,'{\"id\": 4, \"uid\": null, \"name\": \"sn\", \"alias\": \"服务器序列号\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 20:06:49\", \"deleted_at\": null, \"updated_at\": \"2021-11-24 11:04:21\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 15:22:44',NULL,59,'0',25,NULL,NULL,NULL,9,'{\"id\": 25, \"uid\": 9, \"icon\": \"\", \"name\": \"dsfdsfd\", \"alias\": \"dsfdsfd\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:22:44\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-10-19 18:12:27',NULL,60,'2',25,NULL,NULL,NULL,9,'{\"id\": 25, \"uid\": 9, \"icon\": \"\", \"name\": \"dsfdsfd\", \"alias\": \"dsfdsfd\", \"order\": 0, \"deleted\": true, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 15:22:44\", \"deleted_at\": \"2022-10-19 18:12:27\", \"updated_at\": \"2022-10-19 18:12:27\", \"is_attached\": false}'),(NULL,0,'2022-10-19 18:12:41',NULL,61,'3',26,4,NULL,NULL,9,'{\"id\": 4, \"uid\": null, \"name\": \"sn\", \"alias\": \"服务器序列号\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 20:06:49\", \"deleted_at\": null, \"updated_at\": \"2021-11-24 11:04:21\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 18:12:41',NULL,62,'0',26,NULL,NULL,NULL,9,'{\"id\": 26, \"uid\": 9, \"icon\": \"\", \"name\": \"server001\", \"alias\": \"server001\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 18:12:41\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-10-19 18:12:45',NULL,63,'2',26,NULL,NULL,NULL,9,'{\"id\": 26, \"uid\": 9, \"icon\": \"\", \"name\": \"server001\", \"alias\": \"server001\", \"order\": 0, \"deleted\": true, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 18:12:41\", \"deleted_at\": \"2022-10-19 18:12:45\", \"updated_at\": \"2022-10-19 18:12:45\", \"is_attached\": false}'),(NULL,0,'2022-10-19 18:13:23',NULL,64,'3',27,4,NULL,NULL,7,'{\"id\": 4, \"uid\": null, \"name\": \"sn\", \"alias\": \"服务器序列号\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 20:06:49\", \"deleted_at\": null, \"updated_at\": \"2021-11-24 11:04:21\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 18:13:23',NULL,65,'0',27,NULL,NULL,NULL,7,'{\"id\": 27, \"uid\": 7, \"icon\": \"\", \"name\": \"server01\", \"alias\": \"server01\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 18:13:23\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-10-19 18:14:00',NULL,66,'3',27,1,NULL,NULL,7,'{\"id\": 1, \"uid\": null, \"name\": \"bu_name\", \"alias\": \"事业部\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 19:50:29\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 18:14:00',NULL,67,'3',27,2,NULL,NULL,7,'{\"id\": 2, \"uid\": null, \"name\": \"product_name\", \"alias\": \"产品名\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-23 19:56:36\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 18:14:00',NULL,68,'3',27,3,NULL,NULL,7,'{\"id\": 3, \"uid\": null, \"name\": \"project_name\", \"alias\": \"应用名\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-23 19:58:08\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 18:14:00',NULL,69,'3',27,6,NULL,NULL,7,'{\"id\": 6, \"uid\": null, \"name\": \"ram_sn\", \"alias\": \"内存序列号\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-23 20:36:46\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 18:14:00',NULL,70,'3',27,7,NULL,NULL,7,'{\"id\": 7, \"uid\": null, \"name\": \"hd_sn\", \"alias\": \"硬盘序列号\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 21:38:12\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 18:14:00',NULL,71,'3',27,9,NULL,NULL,7,'{\"id\": 9, \"uid\": null, \"name\": \"instance_id\", \"alias\": \"实例ID\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 09:45:05\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-10-19 18:14:18',NULL,72,'2',27,NULL,NULL,NULL,7,'{\"id\": 27, \"uid\": 7, \"icon\": \"\", \"name\": \"server01\", \"alias\": \"server01\", \"order\": 0, \"deleted\": true, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2022-10-19 18:13:23\", \"deleted_at\": \"2022-10-19 18:14:18\", \"updated_at\": \"2022-10-19 18:14:18\", \"is_attached\": false}'),(NULL,0,'2022-10-26 15:03:53',NULL,73,'13',3,NULL,NULL,NULL,1,'{\"child\": {\"id\": 5, \"uid\": null, \"icon\": null, \"name\": \"vserver\", \"alias\": \"虚拟机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 5, \"created_at\": \"2021-11-23 20:08:52\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}, \"parent_id\": {\"id\": 3, \"uid\": null, \"icon\": \"renwuguanli$$\", \"name\": \"project\", \"alias\": \"应用\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 3, \"created_at\": \"2021-11-23 19:58:15\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 21:50:00\", \"is_attached\": false}, \"relation_type_id\": 3}'),(NULL,0,'2022-10-26 15:06:21',NULL,74,'1',4,NULL,NULL,NULL,1,'{\"new\": {\"id\": 4, \"uid\": null, \"icon\": \"icon-xuniji1$$\", \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": \"2022-10-26 15:06:21\", \"is_attached\": false}, \"old\": {\"id\": 4, \"uid\": null, \"icon\": null, \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}}'),(NULL,0,'2022-10-27 19:23:04',NULL,75,'13',1,NULL,NULL,NULL,1,'{\"child\": {\"id\": 2, \"uid\": null, \"icon\": \"camear$$\", \"name\": \"product\", \"alias\": \"产品\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 2, \"created_at\": \"2021-11-23 19:56:40\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 21:49:31\", \"is_attached\": false}, \"parent_id\": {\"id\": 1, \"uid\": null, \"icon\": \"weibiaoti-6$$\", \"name\": \"bu\", \"alias\": \"事业部\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 1, \"created_at\": \"2021-11-23 19:50:34\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 21:48:43\", \"is_attached\": false}, \"relation_type_id\": 1}'),(NULL,0,'2022-10-27 19:23:12',NULL,76,'12',1,NULL,NULL,NULL,1,'{\"child\": {\"id\": 2, \"uid\": null, \"icon\": \"camear$$\", \"name\": \"product\", \"alias\": \"产品\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 2, \"created_at\": \"2021-11-23 19:56:40\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 21:49:31\", \"is_attached\": false}, \"parent\": {\"id\": 1, \"uid\": null, \"icon\": \"weibiaoti-6$$\", \"name\": \"bu\", \"alias\": \"事业部\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 1, \"created_at\": \"2021-11-23 19:50:34\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 21:48:43\", \"is_attached\": false}, \"relation_type_id\": 1}'),(NULL,0,'2022-10-27 19:23:19',NULL,77,'13',2,NULL,NULL,NULL,1,'{\"child\": {\"id\": 3, \"uid\": null, \"icon\": \"renwuguanli$$\", \"name\": \"project\", \"alias\": \"应用\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 3, \"created_at\": \"2021-11-23 19:58:15\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 21:50:00\", \"is_attached\": false}, \"parent_id\": {\"id\": 2, \"uid\": null, \"icon\": \"camear$$\", \"name\": \"product\", \"alias\": \"产品\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 2, \"created_at\": \"2021-11-23 19:56:40\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 21:49:31\", \"is_attached\": false}, \"relation_type_id\": 1}'),(NULL,0,'2022-10-27 19:23:29',NULL,78,'12',2,NULL,NULL,NULL,1,'{\"child\": {\"id\": 3, \"uid\": null, \"icon\": \"renwuguanli$$\", \"name\": \"project\", \"alias\": \"应用\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 3, \"created_at\": \"2021-11-23 19:58:15\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 21:50:00\", \"is_attached\": false}, \"parent\": {\"id\": 2, \"uid\": null, \"icon\": \"camear$$\", \"name\": \"product\", \"alias\": \"产品\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 2, \"created_at\": \"2021-11-23 19:56:40\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 21:49:31\", \"is_attached\": false}, \"relation_type_id\": 1}'),(NULL,0,'2022-10-27 19:25:04',NULL,79,'13',3,NULL,NULL,NULL,1,'{\"child\": {\"id\": 9, \"uid\": null, \"icon\": null, \"name\": \"docker\", \"alias\": \"docker\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 9, \"created_at\": \"2021-11-24 09:45:10\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}, \"parent_id\": {\"id\": 3, \"uid\": null, \"icon\": \"renwuguanli$$\", \"name\": \"project\", \"alias\": \"应用\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 3, \"created_at\": \"2021-11-23 19:58:15\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 21:50:00\", \"is_attached\": false}, \"relation_type_id\": 3}'),(NULL,0,'2022-10-27 19:25:06',NULL,80,'13',3,NULL,NULL,NULL,1,'{\"child\": {\"id\": 4, \"uid\": null, \"icon\": \"icon-xuniji1$$\", \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": \"2022-10-26 15:06:21\", \"is_attached\": false}, \"parent_id\": {\"id\": 3, \"uid\": null, \"icon\": \"renwuguanli$$\", \"name\": \"project\", \"alias\": \"应用\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 3, \"created_at\": \"2021-11-23 19:58:15\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 21:50:00\", \"is_attached\": false}, \"relation_type_id\": 3}'),(NULL,0,'2022-10-27 19:25:14',NULL,81,'12',3,NULL,NULL,NULL,1,'{\"child\": {\"id\": 4, \"uid\": null, \"icon\": \"icon-xuniji1$$\", \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": \"2022-10-26 15:06:21\", \"is_attached\": false}, \"parent\": {\"id\": 3, \"uid\": null, \"icon\": \"renwuguanli$$\", \"name\": \"project\", \"alias\": \"应用\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 3, \"created_at\": \"2021-11-23 19:58:15\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 21:50:00\", \"is_attached\": false}, \"relation_type_id\": 3}'),(NULL,0,'2022-10-27 19:25:21',NULL,82,'13',4,NULL,NULL,NULL,1,'{\"child\": {\"id\": 6, \"uid\": null, \"icon\": null, \"name\": \"RAM\", \"alias\": \"内存\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 6, \"created_at\": \"2021-11-23 20:36:55\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}, \"parent_id\": {\"id\": 4, \"uid\": null, \"icon\": \"icon-xuniji1$$\", \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": \"2022-10-26 15:06:21\", \"is_attached\": false}, \"relation_type_id\": 1}'),(NULL,0,'2022-10-27 19:25:24',NULL,83,'13',4,NULL,NULL,NULL,1,'{\"child\": {\"id\": 7, \"uid\": null, \"icon\": null, \"name\": \"harddisk\", \"alias\": \"硬盘\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 7, \"created_at\": \"2021-11-23 21:38:17\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}, \"parent_id\": {\"id\": 4, \"uid\": null, \"icon\": \"icon-xuniji1$$\", \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": \"2022-10-26 15:06:21\", \"is_attached\": false}, \"relation_type_id\": 1}'),(NULL,0,'2022-10-27 19:25:25',NULL,84,'13',4,NULL,NULL,NULL,1,'{\"child\": {\"id\": 8, \"uid\": null, \"icon\": null, \"name\": \"NIC\", \"alias\": \"网卡\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 8, \"created_at\": \"2021-11-24 09:42:55\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}, \"parent_id\": {\"id\": 4, \"uid\": null, \"icon\": \"icon-xuniji1$$\", \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": \"2022-10-26 15:06:21\", \"is_attached\": false}, \"relation_type_id\": 1}'),(NULL,0,'2022-10-27 19:25:35',NULL,85,'12',4,NULL,NULL,NULL,1,'{\"child\": {\"id\": 6, \"uid\": null, \"icon\": null, \"name\": \"RAM\", \"alias\": \"内存\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 6, \"created_at\": \"2021-11-23 20:36:55\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}, \"parent\": {\"id\": 4, \"uid\": null, \"icon\": \"icon-xuniji1$$\", \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": \"2022-10-26 15:06:21\", \"is_attached\": false}, \"relation_type_id\": 1}'),(NULL,0,'2022-10-27 19:25:42',NULL,86,'12',4,NULL,NULL,NULL,1,'{\"child\": {\"id\": 7, \"uid\": null, \"icon\": null, \"name\": \"harddisk\", \"alias\": \"硬盘\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 7, \"created_at\": \"2021-11-23 21:38:17\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}, \"parent\": {\"id\": 4, \"uid\": null, \"icon\": \"icon-xuniji1$$\", \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": \"2022-10-26 15:06:21\", \"is_attached\": false}, \"relation_type_id\": 1}'),(NULL,0,'2022-10-27 19:25:50',NULL,87,'12',4,NULL,NULL,NULL,1,'{\"child\": {\"id\": 8, \"uid\": null, \"icon\": null, \"name\": \"NIC\", \"alias\": \"网卡\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 8, \"created_at\": \"2021-11-24 09:42:55\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}, \"parent\": {\"id\": 4, \"uid\": null, \"icon\": \"icon-xuniji1$$\", \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": \"2022-10-26 15:06:21\", \"is_attached\": false}, \"relation_type_id\": 1}'),(NULL,0,'2022-10-28 10:12:10',NULL,88,'12',3,NULL,NULL,NULL,1,'{\"child\": {\"id\": 5, \"uid\": null, \"icon\": null, \"name\": \"vserver\", \"alias\": \"虚拟机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 5, \"created_at\": \"2021-11-23 20:08:52\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}, \"parent\": {\"id\": 3, \"uid\": null, \"icon\": \"renwuguanli$$\", \"name\": \"project\", \"alias\": \"应用\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 3, \"created_at\": \"2021-11-23 19:58:15\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 21:50:00\", \"is_attached\": false}, \"relation_type_id\": 3}'),(NULL,0,'2022-10-31 10:40:28',NULL,89,'13',3,NULL,NULL,NULL,1,'{\"child\": {\"id\": 5, \"uid\": null, \"icon\": null, \"name\": \"vserver\", \"alias\": \"虚拟机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 5, \"created_at\": \"2021-11-23 20:08:52\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}, \"parent_id\": {\"id\": 3, \"uid\": null, \"icon\": \"renwuguanli$$\", \"name\": \"project\", \"alias\": \"应用\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 3, \"created_at\": \"2021-11-23 19:58:15\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 21:50:00\", \"is_attached\": false}, \"relation_type_id\": 3}'),(NULL,0,'2022-11-23 11:28:32',NULL,90,'4',4,36,NULL,NULL,1,'{\"new\": {\"id\": 36, \"uid\": null, \"name\": \"cpu\", \"alias\": \"CPU型号\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 11:06:00\", \"deleted_at\": null, \"updated_at\": \"2022-11-23 11:28:32\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 36, \"uid\": null, \"name\": \"cpu\", \"alias\": \"CPU型号\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 11:06:00\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2022-11-23 11:28:32',NULL,91,'4',5,36,NULL,NULL,1,'{\"new\": {\"id\": 36, \"uid\": null, \"name\": \"cpu\", \"alias\": \"CPU型号\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 11:06:00\", \"deleted_at\": null, \"updated_at\": \"2022-11-23 11:28:32\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 36, \"uid\": null, \"name\": \"cpu\", \"alias\": \"CPU型号\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 11:06:00\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2022-12-02 13:18:17',NULL,92,'3',28,71,NULL,NULL,1,'{\"id\": 71, \"uid\": 1, \"name\": \"switch_sn\", \"alias\": \"序列号\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2022-12-02 13:18:11\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:18:17',NULL,93,'0',28,NULL,NULL,NULL,1,'{\"id\": 28, \"uid\": 1, \"icon\": \"icon-mianxing-xiangmu$$\", \"name\": \"switch\", \"alias\": \"交换机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 71, \"created_at\": \"2022-12-02 13:18:17\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-12-02 13:20:36',NULL,94,'3',29,72,NULL,NULL,1,'{\"id\": 72, \"uid\": 1, \"name\": \"router_sn\", \"alias\": \"序列号\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2022-12-02 13:20:31\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:20:36',NULL,95,'0',29,NULL,NULL,NULL,1,'{\"id\": 29, \"uid\": 1, \"icon\": \"\", \"name\": \"router\", \"alias\": \"路由器\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 72, \"created_at\": \"2022-12-02 13:20:36\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-12-02 13:21:51',NULL,96,'3',30,73,NULL,NULL,1,'{\"id\": 73, \"uid\": 1, \"name\": \"firewall_sn\", \"alias\": \"序列号\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2022-12-02 13:21:46\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:21:51',NULL,97,'0',30,NULL,NULL,NULL,1,'{\"id\": 30, \"uid\": 1, \"icon\": \"\", \"name\": \"firewall\", \"alias\": \"防火墙\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 73, \"created_at\": \"2022-12-02 13:21:51\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-12-02 13:27:06',NULL,98,'3',28,48,NULL,NULL,1,'{\"id\": 48, \"uid\": null, \"name\": \"server_room\", \"alias\": \"机房\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 11:15:58\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:27:06',NULL,99,'3',28,47,NULL,NULL,1,'{\"id\": 47, \"uid\": null, \"name\": \"idc\", \"alias\": \"IDC\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:15:27\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 17:09:31\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:28:02',NULL,100,'3',28,74,NULL,NULL,1,'{\"id\": 74, \"uid\": 1, \"name\": \"netdev_status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:28:01\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:28:02',NULL,101,'4',28,74,NULL,NULL,1,'{\"new\": {\"id\": 129, \"order\": 0, \"attr_id\": 74, \"deleted\": false, \"type_id\": 28, \"created_at\": \"2022-12-02 13:28:02\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}, \"old\": {\"id\": 129, \"order\": 0, \"attr_id\": 74, \"deleted\": false, \"type_id\": 28, \"created_at\": \"2022-12-02 13:28:02\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2022-12-02 13:29:28',NULL,102,'3',28,75,NULL,NULL,1,'{\"id\": 75, \"uid\": 1, \"name\": \"netdev_cost\", \"alias\": \"设备成本\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:29:28\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:29:28',NULL,103,'4',28,75,NULL,NULL,1,'{\"new\": {\"id\": 130, \"order\": 0, \"attr_id\": 75, \"deleted\": false, \"type_id\": 28, \"created_at\": \"2022-12-02 13:29:28\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}, \"old\": {\"id\": 130, \"order\": 0, \"attr_id\": 75, \"deleted\": false, \"type_id\": 28, \"created_at\": \"2022-12-02 13:29:28\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2022-12-02 13:32:06',NULL,104,'3',28,76,NULL,NULL,1,'{\"id\": 76, \"uid\": 1, \"name\": \"netdev_name\", \"alias\": \"设备名称\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:32:06\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:32:06',NULL,105,'4',28,76,NULL,NULL,1,'{\"new\": {\"id\": 131, \"order\": 0, \"attr_id\": 76, \"deleted\": false, \"type_id\": 28, \"created_at\": \"2022-12-02 13:32:06\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}, \"old\": {\"id\": 131, \"order\": 0, \"attr_id\": 76, \"deleted\": false, \"type_id\": 28, \"created_at\": \"2022-12-02 13:32:06\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2022-12-02 13:32:35',NULL,106,'3',28,77,NULL,NULL,1,'{\"id\": 77, \"uid\": 1, \"name\": \"netdev_type\", \"alias\": \"设备类型\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:32:35\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:32:35',NULL,107,'4',28,77,NULL,NULL,1,'{\"new\": {\"id\": 132, \"order\": 0, \"attr_id\": 77, \"deleted\": false, \"type_id\": 28, \"created_at\": \"2022-12-02 13:32:35\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}, \"old\": {\"id\": 132, \"order\": 0, \"attr_id\": 77, \"deleted\": false, \"type_id\": 28, \"created_at\": \"2022-12-02 13:32:35\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2022-12-02 13:33:20',NULL,108,'3',28,51,NULL,NULL,1,'{\"id\": 51, \"uid\": null, \"name\": \"buy_date\", \"alias\": \"采购日期\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 11:18:27\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"4\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:35:33',NULL,109,'3',28,78,NULL,NULL,1,'{\"id\": 78, \"uid\": 1, \"name\": \"netdev_manufacturer\", \"alias\": \"设备厂商\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:35:33\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:35:33',NULL,110,'4',28,78,NULL,NULL,1,'{\"new\": {\"id\": 134, \"order\": 0, \"attr_id\": 78, \"deleted\": false, \"type_id\": 28, \"created_at\": \"2022-12-02 13:35:33\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}, \"old\": {\"id\": 134, \"order\": 0, \"attr_id\": 78, \"deleted\": false, \"type_id\": 28, \"created_at\": \"2022-12-02 13:35:33\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2022-12-02 13:36:18',NULL,111,'3',29,74,NULL,NULL,1,'{\"id\": 74, \"uid\": 1, \"name\": \"netdev_status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:28:01\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:36:18',NULL,112,'3',29,75,NULL,NULL,1,'{\"id\": 75, \"uid\": 1, \"name\": \"netdev_cost\", \"alias\": \"设备成本\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:29:28\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:36:18',NULL,113,'3',29,76,NULL,NULL,1,'{\"id\": 76, \"uid\": 1, \"name\": \"netdev_name\", \"alias\": \"设备名称\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:32:06\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:36:18',NULL,114,'3',29,77,NULL,NULL,1,'{\"id\": 77, \"uid\": 1, \"name\": \"netdev_type\", \"alias\": \"设备类型\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:32:35\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:36:18',NULL,115,'3',29,78,NULL,NULL,1,'{\"id\": 78, \"uid\": 1, \"name\": \"netdev_manufacturer\", \"alias\": \"设备厂商\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:35:33\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:36:18',NULL,116,'3',29,47,NULL,NULL,1,'{\"id\": 47, \"uid\": null, \"name\": \"idc\", \"alias\": \"IDC\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:15:27\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 17:09:31\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:36:18',NULL,117,'3',29,48,NULL,NULL,1,'{\"id\": 48, \"uid\": null, \"name\": \"server_room\", \"alias\": \"机房\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 11:15:58\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:37:17',NULL,118,'3',29,51,NULL,NULL,1,'{\"id\": 51, \"uid\": null, \"name\": \"buy_date\", \"alias\": \"采购日期\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 11:18:27\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"4\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:37:17',NULL,119,'3',29,53,NULL,NULL,1,'{\"id\": 53, \"uid\": null, \"name\": \"maintain_enddate\", \"alias\": \"过保日期\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 11:19:08\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"4\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:37:30',NULL,120,'3',28,53,NULL,NULL,1,'{\"id\": 53, \"uid\": null, \"name\": \"maintain_enddate\", \"alias\": \"过保日期\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 11:19:08\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"4\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:38:54',NULL,121,'3',30,74,NULL,NULL,1,'{\"id\": 74, \"uid\": 1, \"name\": \"netdev_status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:28:01\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:38:54',NULL,122,'3',30,75,NULL,NULL,1,'{\"id\": 75, \"uid\": 1, \"name\": \"netdev_cost\", \"alias\": \"设备成本\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:29:28\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:38:54',NULL,123,'3',30,76,NULL,NULL,1,'{\"id\": 76, \"uid\": 1, \"name\": \"netdev_name\", \"alias\": \"设备名称\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:32:06\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:38:54',NULL,124,'3',30,77,NULL,NULL,1,'{\"id\": 77, \"uid\": 1, \"name\": \"netdev_type\", \"alias\": \"设备类型\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:32:35\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:38:54',NULL,125,'3',30,78,NULL,NULL,1,'{\"id\": 78, \"uid\": 1, \"name\": \"netdev_manufacturer\", \"alias\": \"设备厂商\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:35:33\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:38:54',NULL,126,'3',30,47,NULL,NULL,1,'{\"id\": 47, \"uid\": null, \"name\": \"idc\", \"alias\": \"IDC\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:15:27\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 17:09:31\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:38:54',NULL,127,'3',30,48,NULL,NULL,1,'{\"id\": 48, \"uid\": null, \"name\": \"server_room\", \"alias\": \"机房\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 11:15:58\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:38:54',NULL,128,'3',30,51,NULL,NULL,1,'{\"id\": 51, \"uid\": null, \"name\": \"buy_date\", \"alias\": \"采购日期\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 11:18:27\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"4\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:38:54',NULL,129,'3',30,53,NULL,NULL,1,'{\"id\": 53, \"uid\": null, \"name\": \"maintain_enddate\", \"alias\": \"过保日期\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 11:19:08\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"4\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:43:58',NULL,130,'3',28,22,NULL,NULL,1,'{\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:45:38',NULL,131,'3',28,79,NULL,NULL,1,'{\"id\": 79, \"uid\": 1, \"name\": \"manage_ip\", \"alias\": \"管理IP\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:45:38\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:45:38',NULL,132,'4',28,79,NULL,NULL,1,'{\"new\": {\"id\": 155, \"order\": 0, \"attr_id\": 79, \"deleted\": false, \"type_id\": 28, \"created_at\": \"2022-12-02 13:45:38\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}, \"old\": {\"id\": 155, \"order\": 0, \"attr_id\": 79, \"deleted\": false, \"type_id\": 28, \"created_at\": \"2022-12-02 13:45:38\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2022-12-02 13:45:59',NULL,133,'3',29,22,NULL,NULL,1,'{\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:45:59',NULL,134,'3',29,79,NULL,NULL,1,'{\"id\": 79, \"uid\": 1, \"name\": \"manage_ip\", \"alias\": \"管理IP\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:45:38\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:46:24',NULL,135,'3',30,22,NULL,NULL,1,'{\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:46:24',NULL,136,'3',30,79,NULL,NULL,1,'{\"id\": 79, \"uid\": 1, \"name\": \"manage_ip\", \"alias\": \"管理IP\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:45:38\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:47:54',NULL,137,'3',31,80,NULL,NULL,1,'{\"id\": 80, \"uid\": 1, \"name\": \"load_balance_sn\", \"alias\": \"序列号\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2022-12-02 13:47:47\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:47:54',NULL,138,'0',31,NULL,NULL,NULL,1,'{\"id\": 31, \"uid\": 1, \"icon\": \"\", \"name\": \"load_balance\", \"alias\": \"负载均衡\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 80, \"created_at\": \"2022-12-02 13:47:54\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-12-02 13:48:23',NULL,139,'3',31,74,NULL,NULL,1,'{\"id\": 74, \"uid\": 1, \"name\": \"netdev_status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:28:01\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:48:23',NULL,140,'3',31,75,NULL,NULL,1,'{\"id\": 75, \"uid\": 1, \"name\": \"netdev_cost\", \"alias\": \"设备成本\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:29:28\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:48:23',NULL,141,'3',31,76,NULL,NULL,1,'{\"id\": 76, \"uid\": 1, \"name\": \"netdev_name\", \"alias\": \"设备名称\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:32:06\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:48:23',NULL,142,'3',31,77,NULL,NULL,1,'{\"id\": 77, \"uid\": 1, \"name\": \"netdev_type\", \"alias\": \"设备类型\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:32:35\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:48:23',NULL,143,'3',31,78,NULL,NULL,1,'{\"id\": 78, \"uid\": 1, \"name\": \"netdev_manufacturer\", \"alias\": \"设备厂商\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:35:33\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:48:23',NULL,144,'3',31,79,NULL,NULL,1,'{\"id\": 79, \"uid\": 1, \"name\": \"manage_ip\", \"alias\": \"管理IP\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:45:38\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:48:23',NULL,145,'3',31,51,NULL,NULL,1,'{\"id\": 51, \"uid\": null, \"name\": \"buy_date\", \"alias\": \"采购日期\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 11:18:27\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"4\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:48:23',NULL,146,'3',31,53,NULL,NULL,1,'{\"id\": 53, \"uid\": null, \"name\": \"maintain_enddate\", \"alias\": \"过保日期\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 11:19:08\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"4\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:48:23',NULL,147,'3',31,22,NULL,NULL,1,'{\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:48:39',NULL,148,'3',31,48,NULL,NULL,1,'{\"id\": 48, \"uid\": null, \"name\": \"server_room\", \"alias\": \"机房\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 11:15:58\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:48:39',NULL,149,'3',31,47,NULL,NULL,1,'{\"id\": 47, \"uid\": null, \"name\": \"idc\", \"alias\": \"IDC\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:15:27\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 17:09:31\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:53:30',NULL,150,'3',32,81,NULL,NULL,1,'{\"id\": 81, \"uid\": 1, \"name\": \"db_name\", \"alias\": \"DB名\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2022-12-02 13:53:25\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:53:30',NULL,151,'0',32,NULL,NULL,NULL,1,'{\"id\": 32, \"uid\": 1, \"icon\": \"\", \"name\": \"mysql\", \"alias\": \"MySQL\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 81, \"created_at\": \"2022-12-02 13:53:30\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-12-02 13:54:13',NULL,152,'3',33,81,NULL,NULL,1,'{\"id\": 81, \"uid\": 1, \"name\": \"db_name\", \"alias\": \"DB名\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2022-12-02 13:53:25\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:54:13',NULL,153,'0',33,NULL,NULL,NULL,1,'{\"id\": 33, \"uid\": 1, \"icon\": \"\", \"name\": \"postgresql\", \"alias\": \"PostgreSQL\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 81, \"created_at\": \"2022-12-02 13:54:13\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-12-02 13:54:31',NULL,154,'3',34,81,NULL,NULL,1,'{\"id\": 81, \"uid\": 1, \"name\": \"db_name\", \"alias\": \"DB名\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2022-12-02 13:53:25\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:54:31',NULL,155,'0',34,NULL,NULL,NULL,1,'{\"id\": 34, \"uid\": 1, \"icon\": \"\", \"name\": \"mongodb\", \"alias\": \"MongoDB\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 81, \"created_at\": \"2022-12-02 13:54:31\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-12-02 13:56:01',NULL,156,'3',35,81,NULL,NULL,1,'{\"id\": 81, \"uid\": 1, \"name\": \"db_name\", \"alias\": \"DB名\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2022-12-02 13:53:25\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:56:01',NULL,157,'0',35,NULL,NULL,NULL,1,'{\"id\": 35, \"uid\": 1, \"icon\": \"\", \"name\": \"mssql\", \"alias\": \"MSSQL\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 81, \"created_at\": \"2022-12-02 13:56:01\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-12-02 13:58:19',NULL,158,'3',32,82,NULL,NULL,1,'{\"id\": 82, \"uid\": 1, \"name\": \"db_port\", \"alias\": \"端口\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:58:19\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:58:20',NULL,159,'4',32,82,NULL,NULL,1,'{\"new\": {\"id\": 176, \"order\": 0, \"attr_id\": 82, \"deleted\": false, \"type_id\": 32, \"created_at\": \"2022-12-02 13:58:19\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}, \"old\": {\"id\": 176, \"order\": 0, \"attr_id\": 82, \"deleted\": false, \"type_id\": 32, \"created_at\": \"2022-12-02 13:58:19\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2022-12-02 13:58:44',NULL,160,'3',32,83,NULL,NULL,1,'{\"id\": 83, \"uid\": 1, \"name\": \"db_version\", \"alias\": \"数据库版本\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:58:44\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 13:58:44',NULL,161,'4',32,83,NULL,NULL,1,'{\"new\": {\"id\": 177, \"order\": 0, \"attr_id\": 83, \"deleted\": false, \"type_id\": 32, \"created_at\": \"2022-12-02 13:58:44\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}, \"old\": {\"id\": 177, \"order\": 0, \"attr_id\": 83, \"deleted\": false, \"type_id\": 32, \"created_at\": \"2022-12-02 13:58:44\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2022-12-02 14:01:15',NULL,162,'3',32,84,NULL,NULL,1,'{\"id\": 84, \"uid\": 1, \"name\": \"db_ip\", \"alias\": \"IP\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:01:15\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:01:16',NULL,163,'4',32,84,NULL,NULL,1,'{\"new\": {\"id\": 178, \"order\": 0, \"attr_id\": 84, \"deleted\": false, \"type_id\": 32, \"created_at\": \"2022-12-02 14:01:15\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}, \"old\": {\"id\": 178, \"order\": 0, \"attr_id\": 84, \"deleted\": false, \"type_id\": 32, \"created_at\": \"2022-12-02 14:01:15\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2022-12-02 14:01:48',NULL,164,'3',32,34,NULL,NULL,1,'{\"id\": 34, \"uid\": null, \"name\": \"status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:01:59\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 17:05:07\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:02:45',NULL,165,'3',32,85,NULL,NULL,1,'{\"id\": 85, \"uid\": 1, \"name\": \"max_connections\", \"alias\": \"最大连接数\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:02:45\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:02:45',NULL,166,'4',32,85,NULL,NULL,1,'{\"new\": {\"id\": 180, \"order\": 0, \"attr_id\": 85, \"deleted\": false, \"type_id\": 32, \"created_at\": \"2022-12-02 14:02:45\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}, \"old\": {\"id\": 180, \"order\": 0, \"attr_id\": 85, \"deleted\": false, \"type_id\": 32, \"created_at\": \"2022-12-02 14:02:45\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2022-12-02 14:03:00',NULL,167,'3',32,86,NULL,NULL,1,'{\"id\": 86, \"uid\": 1, \"name\": \"charset\", \"alias\": \"字符集\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:02:59\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:03:00',NULL,168,'4',32,86,NULL,NULL,1,'{\"new\": {\"id\": 181, \"order\": 0, \"attr_id\": 86, \"deleted\": false, \"type_id\": 32, \"created_at\": \"2022-12-02 14:03:00\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}, \"old\": {\"id\": 181, \"order\": 0, \"attr_id\": 86, \"deleted\": false, \"type_id\": 32, \"created_at\": \"2022-12-02 14:03:00\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2022-12-02 14:07:46',NULL,169,'3',32,87,NULL,NULL,1,'{\"id\": 87, \"uid\": 1, \"name\": \"binlog_opened\", \"alias\": \"binlog是否开启\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2022-12-02 14:07:45\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:07:46',NULL,170,'4',32,87,NULL,NULL,1,'{\"new\": {\"id\": 182, \"order\": 0, \"attr_id\": 87, \"deleted\": false, \"type_id\": 32, \"created_at\": \"2022-12-02 14:07:46\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}, \"old\": {\"id\": 182, \"order\": 0, \"attr_id\": 87, \"deleted\": false, \"type_id\": 32, \"created_at\": \"2022-12-02 14:07:46\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2022-12-02 14:10:44',NULL,171,'3',32,88,NULL,NULL,1,'{\"id\": 88, \"uid\": 1, \"name\": \"cluster_role\", \"alias\": \"集群角色\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:10:44\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:10:45',NULL,172,'4',32,88,NULL,NULL,1,'{\"new\": {\"id\": 183, \"order\": 0, \"attr_id\": 88, \"deleted\": false, \"type_id\": 32, \"created_at\": \"2022-12-02 14:10:44\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}, \"old\": {\"id\": 183, \"order\": 0, \"attr_id\": 88, \"deleted\": false, \"type_id\": 32, \"created_at\": \"2022-12-02 14:10:44\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2022-12-02 14:11:50',NULL,173,'3',32,22,NULL,NULL,1,'{\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:13:40',NULL,174,'3',33,82,NULL,NULL,1,'{\"id\": 82, \"uid\": 1, \"name\": \"db_port\", \"alias\": \"端口\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:58:19\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:13:40',NULL,175,'3',33,83,NULL,NULL,1,'{\"id\": 83, \"uid\": 1, \"name\": \"db_version\", \"alias\": \"数据库版本\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:58:44\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:13:40',NULL,176,'3',33,84,NULL,NULL,1,'{\"id\": 84, \"uid\": 1, \"name\": \"db_ip\", \"alias\": \"IP\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:01:15\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:13:40',NULL,177,'3',33,85,NULL,NULL,1,'{\"id\": 85, \"uid\": 1, \"name\": \"max_connections\", \"alias\": \"最大连接数\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:02:45\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:13:40',NULL,178,'3',33,22,NULL,NULL,1,'{\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:13:40',NULL,179,'3',33,86,NULL,NULL,1,'{\"id\": 86, \"uid\": 1, \"name\": \"charset\", \"alias\": \"字符集\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:02:59\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:13:40',NULL,180,'3',33,88,NULL,NULL,1,'{\"id\": 88, \"uid\": 1, \"name\": \"cluster_role\", \"alias\": \"集群角色\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:10:44\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:15:26',NULL,181,'3',34,82,NULL,NULL,1,'{\"id\": 82, \"uid\": 1, \"name\": \"db_port\", \"alias\": \"端口\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:58:19\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:15:26',NULL,182,'3',34,83,NULL,NULL,1,'{\"id\": 83, \"uid\": 1, \"name\": \"db_version\", \"alias\": \"数据库版本\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:58:44\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:15:26',NULL,183,'3',34,84,NULL,NULL,1,'{\"id\": 84, \"uid\": 1, \"name\": \"db_ip\", \"alias\": \"IP\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:01:15\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:15:26',NULL,184,'3',34,85,NULL,NULL,1,'{\"id\": 85, \"uid\": 1, \"name\": \"max_connections\", \"alias\": \"最大连接数\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:02:45\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:15:26',NULL,185,'3',34,22,NULL,NULL,1,'{\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:15:26',NULL,186,'3',34,88,NULL,NULL,1,'{\"id\": 88, \"uid\": 1, \"name\": \"cluster_role\", \"alias\": \"集群角色\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:10:44\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:17:24',NULL,187,'3',35,82,NULL,NULL,1,'{\"id\": 82, \"uid\": 1, \"name\": \"db_port\", \"alias\": \"端口\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:58:19\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:17:24',NULL,188,'3',35,83,NULL,NULL,1,'{\"id\": 83, \"uid\": 1, \"name\": \"db_version\", \"alias\": \"数据库版本\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:58:44\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:17:24',NULL,189,'3',35,84,NULL,NULL,1,'{\"id\": 84, \"uid\": 1, \"name\": \"db_ip\", \"alias\": \"IP\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:01:15\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:17:24',NULL,190,'3',35,85,NULL,NULL,1,'{\"id\": 85, \"uid\": 1, \"name\": \"max_connections\", \"alias\": \"最大连接数\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:02:45\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:17:24',NULL,191,'3',35,22,NULL,NULL,1,'{\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:20:07',NULL,192,'3',36,89,NULL,NULL,1,'{\"id\": 89, \"uid\": 1, \"name\": \"middleware_name\", \"alias\": \"实例名\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2022-12-02 14:20:03\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:20:08',NULL,193,'0',36,NULL,NULL,NULL,1,'{\"id\": 36, \"uid\": 1, \"icon\": \"\", \"name\": \"nginx\", \"alias\": \"Nginx\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 89, \"created_at\": \"2022-12-02 14:20:07\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-12-02 14:20:49',NULL,194,'3',37,89,NULL,NULL,1,'{\"id\": 89, \"uid\": 1, \"name\": \"middleware_name\", \"alias\": \"实例名\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2022-12-02 14:20:03\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:20:49',NULL,195,'0',37,NULL,NULL,NULL,1,'{\"id\": 37, \"uid\": 1, \"icon\": \"\", \"name\": \"apache\", \"alias\": \"Apache\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 89, \"created_at\": \"2022-12-02 14:20:49\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-12-02 14:21:04',NULL,196,'3',38,89,NULL,NULL,1,'{\"id\": 89, \"uid\": 1, \"name\": \"middleware_name\", \"alias\": \"实例名\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2022-12-02 14:20:03\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:21:04',NULL,197,'0',38,NULL,NULL,NULL,1,'{\"id\": 38, \"uid\": 1, \"icon\": \"\", \"name\": \"tomcat\", \"alias\": \"Tomcat\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 89, \"created_at\": \"2022-12-02 14:21:04\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2022-12-02 14:25:33',NULL,198,'3',36,90,NULL,NULL,1,'{\"id\": 90, \"uid\": 1, \"name\": \"middleware_ip\", \"alias\": \"IP\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:25:33\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:25:33',NULL,199,'4',36,90,NULL,NULL,1,'{\"new\": {\"id\": 206, \"order\": 0, \"attr_id\": 90, \"deleted\": false, \"type_id\": 36, \"created_at\": \"2022-12-02 14:25:33\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}, \"old\": {\"id\": 206, \"order\": 0, \"attr_id\": 90, \"deleted\": false, \"type_id\": 36, \"created_at\": \"2022-12-02 14:25:33\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2022-12-02 14:25:54',NULL,200,'3',36,91,NULL,NULL,1,'{\"id\": 91, \"uid\": 1, \"name\": \"middleware_port\", \"alias\": \"监听端口\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:25:54\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:25:54',NULL,201,'4',36,91,NULL,NULL,1,'{\"new\": {\"id\": 207, \"order\": 0, \"attr_id\": 91, \"deleted\": false, \"type_id\": 36, \"created_at\": \"2022-12-02 14:25:54\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}, \"old\": {\"id\": 207, \"order\": 0, \"attr_id\": 91, \"deleted\": false, \"type_id\": 36, \"created_at\": \"2022-12-02 14:25:54\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2022-12-02 14:26:17',NULL,202,'3',36,92,NULL,NULL,1,'{\"id\": 92, \"uid\": 1, \"name\": \"middleware_version\", \"alias\": \"版本号\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:26:17\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:26:18',NULL,203,'4',36,92,NULL,NULL,1,'{\"new\": {\"id\": 208, \"order\": 0, \"attr_id\": 92, \"deleted\": false, \"type_id\": 36, \"created_at\": \"2022-12-02 14:26:17\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}, \"old\": {\"id\": 208, \"order\": 0, \"attr_id\": 92, \"deleted\": false, \"type_id\": 36, \"created_at\": \"2022-12-02 14:26:17\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2022-12-02 14:27:09',NULL,204,'3',36,93,NULL,NULL,1,'{\"id\": 93, \"uid\": 1, \"name\": \"log_path\", \"alias\": \"日志路径\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:27:09\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:27:09',NULL,205,'4',36,93,NULL,NULL,1,'{\"new\": {\"id\": 209, \"order\": 0, \"attr_id\": 93, \"deleted\": false, \"type_id\": 36, \"created_at\": \"2022-12-02 14:27:09\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}, \"old\": {\"id\": 209, \"order\": 0, \"attr_id\": 93, \"deleted\": false, \"type_id\": 36, \"created_at\": \"2022-12-02 14:27:09\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2022-12-02 14:27:26',NULL,206,'3',36,22,NULL,NULL,1,'{\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:29:03',NULL,207,'3',36,94,NULL,NULL,1,'{\"id\": 94, \"uid\": 1, \"name\": \"domain_name\", \"alias\": \"域名\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:29:03\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:29:03',NULL,208,'4',36,94,NULL,NULL,1,'{\"new\": {\"id\": 211, \"order\": 0, \"attr_id\": 94, \"deleted\": false, \"type_id\": 36, \"created_at\": \"2022-12-02 14:29:03\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}, \"old\": {\"id\": 211, \"order\": 0, \"attr_id\": 94, \"deleted\": false, \"type_id\": 36, \"created_at\": \"2022-12-02 14:29:03\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2022-12-02 14:30:22',NULL,209,'3',37,22,NULL,NULL,1,'{\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:30:22',NULL,210,'3',37,90,NULL,NULL,1,'{\"id\": 90, \"uid\": 1, \"name\": \"middleware_ip\", \"alias\": \"IP\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:25:33\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:30:22',NULL,211,'3',37,91,NULL,NULL,1,'{\"id\": 91, \"uid\": 1, \"name\": \"middleware_port\", \"alias\": \"监听端口\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:25:54\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:30:22',NULL,212,'3',37,92,NULL,NULL,1,'{\"id\": 92, \"uid\": 1, \"name\": \"middleware_version\", \"alias\": \"版本号\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:26:17\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:30:22',NULL,213,'3',37,93,NULL,NULL,1,'{\"id\": 93, \"uid\": 1, \"name\": \"log_path\", \"alias\": \"日志路径\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:27:09\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:31:03',NULL,214,'3',38,22,NULL,NULL,1,'{\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": false, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:31:03',NULL,215,'3',38,90,NULL,NULL,1,'{\"id\": 90, \"uid\": 1, \"name\": \"middleware_ip\", \"alias\": \"IP\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:25:33\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:31:03',NULL,216,'3',38,91,NULL,NULL,1,'{\"id\": 91, \"uid\": 1, \"name\": \"middleware_port\", \"alias\": \"监听端口\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:25:54\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:31:03',NULL,217,'3',38,92,NULL,NULL,1,'{\"id\": 92, \"uid\": 1, \"name\": \"middleware_version\", \"alias\": \"版本号\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:26:17\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2022-12-02 14:31:03',NULL,218,'3',38,93,NULL,NULL,1,'{\"id\": 93, \"uid\": 1, \"name\": \"log_path\", \"alias\": \"日志路径\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:27:09\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-01-03 18:47:04',NULL,219,'3',39,93,NULL,NULL,1,'{\"id\": 93, \"uid\": 1, \"name\": \"log_path\", \"alias\": \"日志路径\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:27:09\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2022-12-14 19:25:44\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-01-03 18:47:04',NULL,220,'0',39,NULL,NULL,NULL,1,'{\"id\": 39, \"uid\": 1, \"icon\": \"\", \"name\": \"ssss123\", \"alias\": \"ssss123\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 93, \"created_at\": \"2023-01-03 18:47:04\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2023-01-03 18:47:47',NULL,221,'2',39,NULL,NULL,NULL,1,'{\"id\": 39, \"uid\": 1, \"icon\": \"\", \"name\": \"ssss123\", \"alias\": \"ssss123\", \"order\": 0, \"deleted\": true, \"enabled\": true, \"unique_id\": 93, \"created_at\": \"2023-01-03 18:47:04\", \"deleted_at\": \"2023-01-03 18:47:47\", \"updated_at\": \"2023-01-03 18:47:47\", \"is_attached\": false}'),(NULL,0,'2023-01-04 14:50:18',NULL,222,'4',4,23,NULL,NULL,1,'{\"new\": {\"id\": 23, \"uid\": null, \"name\": \"server_name\", \"alias\": \"服务器名5\", \"option\": {}, \"default\": {\"default\": \"10\"}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:40:03\", \"deleted_at\": \"2022-12-14 19:25:41\", \"updated_at\": \"2023-01-04 14:50:16\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 23, \"uid\": null, \"name\": \"server_name\", \"alias\": \"服务器名\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-24 10:40:03\", \"deleted_at\": \"2022-12-14 19:25:41\", \"updated_at\": \"2022-12-14 19:25:41\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-01-04 14:50:18',NULL,223,'4',4,23,NULL,NULL,1,'{\"new\": {\"id\": 23, \"uid\": null, \"name\": \"server_name\", \"alias\": \"服务器名5\", \"option\": {}, \"default\": {\"default\": \"10\"}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:40:03\", \"deleted_at\": \"2022-12-14 19:25:41\", \"updated_at\": \"2023-01-04 14:50:16\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 23, \"uid\": null, \"name\": \"server_name\", \"alias\": \"服务器名5\", \"option\": {}, \"default\": {\"default\": \"10\"}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:40:03\", \"deleted_at\": \"2022-12-14 19:25:41\", \"updated_at\": \"2023-01-04 14:50:16\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-01-04 18:22:47',NULL,224,'3',40,93,NULL,NULL,1,'{\"id\": 93, \"uid\": 1, \"name\": \"log_path\", \"alias\": \"日志路径\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 14:27:09\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2022-12-14 19:25:44\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-01-04 18:22:47',NULL,225,'0',40,NULL,NULL,NULL,1,'{\"id\": 40, \"uid\": 1, \"icon\": \"\", \"name\": \"test\", \"alias\": \"test\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 93, \"created_at\": \"2023-01-04 18:22:47\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2023-01-04 18:23:11',NULL,226,'2',40,NULL,NULL,NULL,1,'{\"id\": 40, \"uid\": 1, \"icon\": \"\", \"name\": \"test\", \"alias\": \"test\", \"order\": 0, \"deleted\": true, \"enabled\": true, \"unique_id\": 93, \"created_at\": \"2023-01-04 18:22:47\", \"deleted_at\": \"2023-01-04 18:23:11\", \"updated_at\": \"2023-01-04 18:23:11\", \"is_attached\": false}'),(NULL,0,'2023-01-04 18:25:54',NULL,227,'5',28,22,NULL,NULL,1,'{\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2022-12-14 19:25:44\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-01-05 18:54:25',NULL,228,'5',4,53,NULL,NULL,1,'{\"id\": 53, \"uid\": null, \"name\": \"maintain_enddate\", \"alias\": \"过保日期\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 11:19:08\", \"deleted_at\": \"2022-12-14 19:25:43\", \"updated_at\": \"2022-12-14 19:25:43\", \"value_type\": \"4\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-01-05 18:54:29',NULL,229,'5',4,52,NULL,NULL,1,'{\"id\": 52, \"uid\": null, \"name\": \"maintain_startdate\", \"alias\": \"保修开始日期\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 11:18:50\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2022-12-14 19:25:42\", \"value_type\": \"4\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-01-05 18:54:49',NULL,230,'5',4,50,NULL,NULL,1,'{\"id\": 50, \"uid\": null, \"name\": \"pos\", \"alias\": \"位置编号\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 11:17:18\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2022-12-14 19:25:42\", \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-01-09 14:53:47',NULL,231,'6',4,NULL,1,NULL,1,'{\"id\": 1, \"notify\": {\"body\": \"bbb\", \"wx_to\": [], \"subject\": \"aaa\", \"notify_at\": \"08:00\", \"before_days\": 1}, \"attr_id\": 51, \"deleted\": false, \"type_id\": 4, \"created_at\": \"2023-01-09 14:53:47\", \"deleted_at\": null, \"updated_at\": null}'),(NULL,0,'2023-01-11 17:25:50',NULL,232,'3',1,95,NULL,NULL,1,'{\"id\": 95, \"uid\": 1, \"name\": \"aaa\", \"alias\": \"BU负责人电话\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2023-01-11 17:25:50\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-01-11 17:25:50',NULL,233,'4',1,95,NULL,NULL,1,'{\"new\": {\"id\": 420, \"order\": 0, \"attr_id\": 95, \"deleted\": false, \"type_id\": 1, \"created_at\": \"2023-01-11 17:25:50\", \"deleted_at\": null, \"updated_at\": \"2023-01-11 17:25:50\", \"is_required\": false, \"default_show\": false}, \"old\": {\"id\": 420, \"order\": 0, \"attr_id\": 95, \"deleted\": false, \"type_id\": 1, \"created_at\": \"2023-01-11 17:25:50\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2023-01-11 17:35:37',NULL,234,'7',4,NULL,1,NULL,1,'{\"new\": {\"id\": 1, \"notify\": {\"body\": \"bbb\", \"wx_to\": [], \"subject\": \"aaa\", \"notify_at\": \"08:00\", \"before_days\": 1}, \"attr_id\": 51, \"deleted\": false, \"type_id\": 4, \"created_at\": \"2023-01-09 14:53:47\", \"deleted_at\": null, \"updated_at\": null}, \"old\": {\"id\": 1, \"notify\": {\"body\": \"bbb\", \"wx_to\": [], \"subject\": \"aaa\", \"notify_at\": \"08:00\", \"before_days\": 1}, \"attr_id\": 51, \"deleted\": false, \"type_id\": 4, \"created_at\": \"2023-01-09 14:53:47\", \"deleted_at\": null, \"updated_at\": null}}'),(NULL,0,'2023-01-11 18:14:03',NULL,235,'3',5,97,NULL,NULL,1,'{\"id\": 97, \"uid\": 1, \"name\": \"disk_model\", \"alias\": \"硬盘型号\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2023-01-11 18:14:03\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-01-11 18:14:03',NULL,236,'4',5,97,NULL,NULL,1,'{\"new\": {\"id\": 421, \"order\": 0, \"attr_id\": 97, \"deleted\": false, \"type_id\": 5, \"created_at\": \"2023-01-11 18:14:03\", \"deleted_at\": null, \"updated_at\": \"2023-01-11 18:14:03\", \"is_required\": false, \"default_show\": false}, \"old\": {\"id\": 421, \"order\": 0, \"attr_id\": 97, \"deleted\": false, \"type_id\": 5, \"created_at\": \"2023-01-11 18:14:03\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2023-01-11 18:36:58',NULL,237,'4',5,97,NULL,NULL,1,'{\"new\": {\"id\": 97, \"uid\": 1, \"name\": \"disk_model\", \"alias\": \"硬盘型号\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2023-01-11 18:14:03\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"A3\", {\"icon\": {}, \"style\": {}}], [\"A4\", {\"icon\": {}, \"style\": {}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 97, \"uid\": 1, \"name\": \"disk_model\", \"alias\": \"硬盘型号\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2023-01-11 18:14:03\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"A3\", {\"icon\": {}, \"style\": {}}], [\"A4\", {\"icon\": {}, \"style\": {}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-01-11 18:37:49',NULL,238,'4',5,97,NULL,NULL,1,'{\"new\": {\"id\": 97, \"uid\": 1, \"name\": \"disk_model\", \"alias\": \"硬盘型号\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2023-01-11 18:14:03\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"A3\", {\"icon\": {}, \"style\": {}}], [\"A4\", {\"icon\": {}, \"style\": {}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 97, \"uid\": 1, \"name\": \"disk_model\", \"alias\": \"硬盘型号\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2023-01-11 18:14:03\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"A3\", {\"icon\": {}, \"style\": {}}], [\"A4\", {\"icon\": {}, \"style\": {}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-01-11 18:43:09',NULL,239,'12',5,NULL,NULL,NULL,1,'{\"child\": {\"id\": 4, \"uid\": null, \"icon\": \"icon-xuniji1$$\", \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": \"2022-10-26 15:06:21\", \"is_attached\": false}, \"parent\": {\"id\": 5, \"uid\": null, \"icon\": null, \"name\": \"vserver\", \"alias\": \"虚拟机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 5, \"created_at\": \"2021-11-23 20:08:52\", \"deleted_at\": null, \"updated_at\": \"2022-12-14 19:25:44\", \"is_attached\": false}, \"relation_type_id\": 1}'),(NULL,0,'2023-01-11 21:21:47',NULL,240,'5',5,97,NULL,NULL,1,'{\"id\": 97, \"uid\": 1, \"name\": \"disk_model\", \"alias\": \"硬盘型号\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2023-01-11 18:14:03\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-01-12 09:52:48',NULL,241,'7',4,NULL,1,NULL,1,'{\"new\": {\"id\": 1, \"notify\": {\"body\": \"bbb\", \"wx_to\": [], \"subject\": \"aaa\", \"notify_at\": \"08:00\", \"before_days\": 1}, \"attr_id\": 51, \"deleted\": false, \"type_id\": 4, \"created_at\": \"2023-01-09 14:53:47\", \"deleted_at\": null, \"updated_at\": null}, \"old\": {\"id\": 1, \"notify\": {\"body\": \"bbb\", \"wx_to\": [], \"subject\": \"aaa\", \"notify_at\": \"08:00\", \"before_days\": 1}, \"attr_id\": 51, \"deleted\": false, \"type_id\": 4, \"created_at\": \"2023-01-09 14:53:47\", \"deleted_at\": null, \"updated_at\": null}}'),(NULL,0,'2023-01-12 09:53:22',NULL,242,'7',4,NULL,1,NULL,1,'{\"new\": {\"id\": 1, \"notify\": {\"body\": \"bbb\", \"wx_to\": [], \"subject\": \"aaa\", \"notify_at\": \"08:00\", \"before_days\": 1}, \"attr_id\": 51, \"deleted\": false, \"type_id\": 4, \"created_at\": \"2023-01-09 14:53:47\", \"deleted_at\": null, \"updated_at\": null}, \"old\": {\"id\": 1, \"notify\": {\"body\": \"bbb\", \"wx_to\": [], \"subject\": \"aaa\", \"notify_at\": \"08:00\", \"before_days\": 1}, \"attr_id\": 51, \"deleted\": false, \"type_id\": 4, \"created_at\": \"2023-01-09 14:53:47\", \"deleted_at\": null, \"updated_at\": null}}'),(NULL,0,'2023-01-16 17:24:29',NULL,243,'4',5,5,NULL,NULL,1,'{\"new\": {\"id\": 5, \"uid\": null, \"name\": \"uuid\", \"alias\": \"UUID\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": true, \"created_at\": \"2021-11-23 20:08:47\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2023-01-16 17:24:29\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"6666\", {\"icon\": {}, \"style\": {}}], [\"999\", {\"icon\": {}, \"style\": {}}], [\"111\", {\"icon\": {}, \"style\": {}}], [\"222\", {\"icon\": {}, \"style\": {}}], [\"333\", {\"icon\": {}, \"style\": {}}], [\"444\", {\"icon\": {}, \"style\": {}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 5, \"uid\": null, \"name\": \"uuid\", \"alias\": \"UUID\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 20:08:47\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2022-12-14 19:25:42\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-01-16 17:24:39',NULL,244,'4',5,5,NULL,NULL,1,'{\"new\": {\"id\": 5, \"uid\": null, \"name\": \"uuid\", \"alias\": \"UUID\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": true, \"created_at\": \"2021-11-23 20:08:47\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2023-01-16 17:24:29\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"6666\", {\"icon\": {}, \"style\": {}}], [\"999\", {\"icon\": {}, \"style\": {}}], [\"111\", {\"icon\": {}, \"style\": {}}], [\"222\", {\"icon\": {}, \"style\": {}}], [\"333\", {\"icon\": {}, \"style\": {}}], [\"444\", {\"icon\": {}, \"style\": {}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 5, \"uid\": null, \"name\": \"uuid\", \"alias\": \"UUID\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": true, \"created_at\": \"2021-11-23 20:08:47\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2023-01-16 17:24:29\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"6666\", {\"icon\": {}, \"style\": {}}], [\"999\", {\"icon\": {}, \"style\": {}}], [\"111\", {\"icon\": {}, \"style\": {}}], [\"222\", {\"icon\": {}, \"style\": {}}], [\"333\", {\"icon\": {}, \"style\": {}}], [\"444\", {\"icon\": {}, \"style\": {}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:34:19',NULL,245,'4',5,5,NULL,NULL,1,'{\"new\": {\"id\": 5, \"uid\": null, \"name\": \"uuid\", \"alias\": \"UUID\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": true, \"created_at\": \"2021-11-23 20:08:47\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2023-02-07 13:34:19\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 5, \"uid\": null, \"name\": \"uuid\", \"alias\": \"UUID\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": true, \"created_at\": \"2021-11-23 20:08:47\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2023-01-16 17:24:29\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"6666\", {\"icon\": {}, \"style\": {}}], [\"999\", {\"icon\": {}, \"style\": {}}], [\"111\", {\"icon\": {}, \"style\": {}}], [\"222\", {\"icon\": {}, \"style\": {}}], [\"333\", {\"icon\": {}, \"style\": {}}], [\"444\", {\"icon\": {}, \"style\": {}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:53:38',NULL,246,'4',5,22,NULL,NULL,1,'{\"new\": {\"id\": 278, \"order\": 5, \"attr_id\": 22, \"deleted\": false, \"type_id\": 5, \"created_at\": \"2022-12-14 19:25:45\", \"deleted_at\": null, \"updated_at\": \"2023-02-07 13:53:38\", \"is_required\": false, \"default_show\": false}, \"old\": {\"id\": 278, \"order\": 5, \"attr_id\": 22, \"deleted\": false, \"type_id\": 5, \"created_at\": \"2022-12-14 19:25:45\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2023-02-07 13:53:38',NULL,247,'4',3,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2022-12-14 19:25:44\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:53:38',NULL,248,'4',4,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2022-12-14 19:25:44\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:53:38',NULL,249,'4',5,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2022-12-14 19:25:44\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:53:38',NULL,250,'4',29,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2022-12-14 19:25:44\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:53:38',NULL,251,'4',30,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2022-12-14 19:25:44\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:53:38',NULL,252,'4',31,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2022-12-14 19:25:44\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:53:38',NULL,253,'4',32,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2022-12-14 19:25:44\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:53:38',NULL,254,'4',33,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2022-12-14 19:25:44\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:53:38',NULL,255,'4',34,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2022-12-14 19:25:44\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:53:38',NULL,256,'4',35,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2022-12-14 19:25:44\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:53:38',NULL,257,'4',36,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2022-12-14 19:25:44\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:53:38',NULL,258,'4',37,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2022-12-14 19:25:44\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:53:38',NULL,259,'4',38,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2022-12-14 19:25:44\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:54:20',NULL,260,'4',3,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:54:20',NULL,261,'4',4,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:54:20',NULL,262,'4',5,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:54:20',NULL,263,'4',29,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:54:20',NULL,264,'4',30,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:54:20',NULL,265,'4',31,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:54:20',NULL,266,'4',32,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:54:20',NULL,267,'4',33,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:54:20',NULL,268,'4',34,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:54:20',NULL,269,'4',35,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:54:20',NULL,270,'4',36,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:54:20',NULL,271,'4',37,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:54:20',NULL,272,'4',38,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:53:38\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:55:56',NULL,273,'4',3,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:55:56',NULL,274,'4',4,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:55:56',NULL,275,'4',5,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:55:56',NULL,276,'4',29,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:55:56',NULL,277,'4',30,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:55:56',NULL,278,'4',31,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:55:56',NULL,279,'4',32,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:55:56',NULL,280,'4',33,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:55:56',NULL,281,'4',34,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:55:56',NULL,282,'4',35,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:55:56',NULL,283,'4',36,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:55:56',NULL,284,'4',37,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:55:56',NULL,285,'4',38,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:54:20\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": true, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:56:47',NULL,286,'4',3,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:56:47\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:56:47',NULL,287,'4',4,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:56:47\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:56:47',NULL,288,'4',5,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:56:47\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:56:47',NULL,289,'4',29,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:56:47\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:56:47',NULL,290,'4',30,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:56:47\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:56:47',NULL,291,'4',31,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:56:47\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:56:47',NULL,292,'4',32,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:56:47\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:56:47',NULL,293,'4',33,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:56:47\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:56:47',NULL,294,'4',34,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:56:47\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:56:47',NULL,295,'4',35,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:56:47\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:56:47',NULL,296,'4',36,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:56:47\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:56:47',NULL,297,'4',37,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:56:47\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-02-07 13:56:47',NULL,298,'4',38,22,NULL,NULL,1,'{\"new\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:56:47\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": true, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:55:56\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-03-03 17:46:17',NULL,299,'1',4,NULL,NULL,NULL,1,'{\"new\": {\"id\": 4, \"uid\": null, \"icon\": \"caise-wuliji$$\", \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:46:17\", \"is_attached\": false}, \"old\": {\"id\": 4, \"uid\": null, \"icon\": \"icon-xuniji1$$\", \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": \"2022-10-26 15:06:21\", \"is_attached\": false}}'),(NULL,0,'2023-03-03 17:46:29',NULL,300,'1',5,NULL,NULL,NULL,1,'{\"new\": {\"id\": 5, \"uid\": null, \"icon\": \"caise-xuniji$$\", \"name\": \"vserver\", \"alias\": \"虚拟机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 5, \"created_at\": \"2021-11-23 20:08:52\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:46:29\", \"is_attached\": false}, \"old\": {\"id\": 5, \"uid\": null, \"icon\": null, \"name\": \"vserver\", \"alias\": \"虚拟机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 5, \"created_at\": \"2021-11-23 20:08:52\", \"deleted_at\": null, \"updated_at\": \"2022-12-14 19:25:44\", \"is_attached\": false}}'),(NULL,0,'2023-03-03 17:46:40',NULL,301,'1',7,NULL,NULL,NULL,1,'{\"new\": {\"id\": 7, \"uid\": null, \"icon\": \"caise-yingpan$$\", \"name\": \"harddisk\", \"alias\": \"硬盘\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 7, \"created_at\": \"2021-11-23 21:38:17\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:46:40\", \"is_attached\": false}, \"old\": {\"id\": 7, \"uid\": null, \"icon\": null, \"name\": \"harddisk\", \"alias\": \"硬盘\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 7, \"created_at\": \"2021-11-23 21:38:17\", \"deleted_at\": null, \"updated_at\": \"2022-12-14 19:25:44\", \"is_attached\": false}}'),(NULL,0,'2023-03-03 17:46:51',NULL,302,'1',8,NULL,NULL,NULL,1,'{\"new\": {\"id\": 8, \"uid\": null, \"icon\": \"caise-wangka$$\", \"name\": \"NIC\", \"alias\": \"网卡\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 8, \"created_at\": \"2021-11-24 09:42:55\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:46:51\", \"is_attached\": false}, \"old\": {\"id\": 8, \"uid\": null, \"icon\": null, \"name\": \"NIC\", \"alias\": \"网卡\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 8, \"created_at\": \"2021-11-24 09:42:55\", \"deleted_at\": null, \"updated_at\": \"2022-12-14 19:25:44\", \"is_attached\": false}}'),(NULL,0,'2023-03-03 17:47:18',NULL,303,'1',6,NULL,NULL,NULL,1,'{\"new\": {\"id\": 6, \"uid\": null, \"icon\": \"caise-neicun$$\", \"name\": \"RAM\", \"alias\": \"内存\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 6, \"created_at\": \"2021-11-23 20:36:55\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:47:18\", \"is_attached\": false}, \"old\": {\"id\": 6, \"uid\": null, \"icon\": null, \"name\": \"RAM\", \"alias\": \"内存\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 6, \"created_at\": \"2021-11-23 20:36:55\", \"deleted_at\": null, \"updated_at\": \"2022-12-14 19:25:44\", \"is_attached\": false}}'),(NULL,0,'2023-03-03 17:47:32',NULL,304,'1',28,NULL,NULL,NULL,1,'{\"new\": {\"id\": 28, \"uid\": 1, \"icon\": \"caise-jiaohuanji$$\", \"name\": \"switch\", \"alias\": \"交换机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 71, \"created_at\": \"2022-12-02 13:18:17\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:47:32\", \"is_attached\": false}, \"old\": {\"id\": 28, \"uid\": 1, \"icon\": \"icon-mianxing-xiangmu$$\", \"name\": \"switch\", \"alias\": \"交换机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 71, \"created_at\": \"2022-12-02 13:18:17\", \"deleted_at\": null, \"updated_at\": \"2022-12-14 19:25:44\", \"is_attached\": false}}'),(NULL,0,'2023-03-03 17:47:43',NULL,305,'1',29,NULL,NULL,NULL,1,'{\"new\": {\"id\": 29, \"uid\": 1, \"icon\": \"caise-luyouqi$$\", \"name\": \"router\", \"alias\": \"路由器\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 72, \"created_at\": \"2022-12-02 13:20:36\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:47:43\", \"is_attached\": false}, \"old\": {\"id\": 29, \"uid\": 1, \"icon\": \"\", \"name\": \"router\", \"alias\": \"路由器\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 72, \"created_at\": \"2022-12-02 13:20:36\", \"deleted_at\": null, \"updated_at\": \"2022-12-14 19:25:44\", \"is_attached\": false}}'),(NULL,0,'2023-03-03 17:47:55',NULL,306,'1',30,NULL,NULL,NULL,1,'{\"new\": {\"id\": 30, \"uid\": 1, \"icon\": \"caise-fanghuoqiang$$\", \"name\": \"firewall\", \"alias\": \"防火墙\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 73, \"created_at\": \"2022-12-02 13:21:51\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:47:55\", \"is_attached\": false}, \"old\": {\"id\": 30, \"uid\": 1, \"icon\": \"\", \"name\": \"firewall\", \"alias\": \"防火墙\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 73, \"created_at\": \"2022-12-02 13:21:51\", \"deleted_at\": null, \"updated_at\": \"2022-12-14 19:25:44\", \"is_attached\": false}}'),(NULL,0,'2023-03-03 17:48:07',NULL,307,'1',31,NULL,NULL,NULL,1,'{\"new\": {\"id\": 31, \"uid\": 1, \"icon\": \"caise-fuzaijunheng$$\", \"name\": \"load_balance\", \"alias\": \"负载均衡\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 80, \"created_at\": \"2022-12-02 13:47:54\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:48:07\", \"is_attached\": false}, \"old\": {\"id\": 31, \"uid\": 1, \"icon\": \"\", \"name\": \"load_balance\", \"alias\": \"负载均衡\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 80, \"created_at\": \"2022-12-02 13:47:54\", \"deleted_at\": null, \"updated_at\": \"2022-12-14 19:25:44\", \"is_attached\": false}}'),(NULL,0,'2023-03-03 17:48:20',NULL,308,'1',1,NULL,NULL,NULL,1,'{\"new\": {\"id\": 1, \"uid\": null, \"icon\": \"caise-bumen$$\", \"name\": \"bu\", \"alias\": \"事业部\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 1, \"created_at\": \"2021-11-23 19:50:34\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:48:20\", \"is_attached\": false}, \"old\": {\"id\": 1, \"uid\": null, \"icon\": \"weibiaoti-6$$\", \"name\": \"bu\", \"alias\": \"事业部\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 1, \"created_at\": \"2021-11-23 19:50:34\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 21:48:43\", \"is_attached\": false}}'),(NULL,0,'2023-03-03 17:48:29',NULL,309,'1',2,NULL,NULL,NULL,1,'{\"new\": {\"id\": 2, \"uid\": null, \"icon\": \"caise-chanpin$$\", \"name\": \"product\", \"alias\": \"产品\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 2, \"created_at\": \"2021-11-23 19:56:40\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:48:29\", \"is_attached\": false}, \"old\": {\"id\": 2, \"uid\": null, \"icon\": \"camear$$\", \"name\": \"product\", \"alias\": \"产品\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 2, \"created_at\": \"2021-11-23 19:56:40\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 21:49:31\", \"is_attached\": false}}'),(NULL,0,'2023-03-03 17:48:36',NULL,310,'1',3,NULL,NULL,NULL,1,'{\"new\": {\"id\": 3, \"uid\": null, \"icon\": \"caise-yingyong$$\", \"name\": \"project\", \"alias\": \"应用\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 3, \"created_at\": \"2021-11-23 19:58:15\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:48:36\", \"is_attached\": false}, \"old\": {\"id\": 3, \"uid\": null, \"icon\": \"renwuguanli$$\", \"name\": \"project\", \"alias\": \"应用\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 3, \"created_at\": \"2021-11-23 19:58:15\", \"deleted_at\": null, \"updated_at\": \"2022-10-17 21:50:00\", \"is_attached\": false}}'),(NULL,0,'2023-03-03 17:48:53',NULL,311,'1',32,NULL,NULL,NULL,1,'{\"new\": {\"id\": 32, \"uid\": 1, \"icon\": \"caise-mySQL$$\", \"name\": \"mysql\", \"alias\": \"MySQL\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 81, \"created_at\": \"2022-12-02 13:53:30\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:48:53\", \"is_attached\": false}, \"old\": {\"id\": 32, \"uid\": 1, \"icon\": \"\", \"name\": \"mysql\", \"alias\": \"MySQL\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 81, \"created_at\": \"2022-12-02 13:53:30\", \"deleted_at\": null, \"updated_at\": \"2022-12-14 19:25:44\", \"is_attached\": false}}'),(NULL,0,'2023-03-03 17:49:06',NULL,312,'1',33,NULL,NULL,NULL,1,'{\"new\": {\"id\": 33, \"uid\": 1, \"icon\": \"caise-PostgreSQL$$\", \"name\": \"postgresql\", \"alias\": \"PostgreSQL\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 81, \"created_at\": \"2022-12-02 13:54:13\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:49:06\", \"is_attached\": false}, \"old\": {\"id\": 33, \"uid\": 1, \"icon\": \"\", \"name\": \"postgresql\", \"alias\": \"PostgreSQL\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 81, \"created_at\": \"2022-12-02 13:54:13\", \"deleted_at\": null, \"updated_at\": \"2022-12-14 19:25:44\", \"is_attached\": false}}'),(NULL,0,'2023-03-03 17:49:15',NULL,313,'1',34,NULL,NULL,NULL,1,'{\"new\": {\"id\": 34, \"uid\": 1, \"icon\": \"caise-mongodb$$\", \"name\": \"mongodb\", \"alias\": \"MongoDB\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 81, \"created_at\": \"2022-12-02 13:54:31\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:49:15\", \"is_attached\": false}, \"old\": {\"id\": 34, \"uid\": 1, \"icon\": \"\", \"name\": \"mongodb\", \"alias\": \"MongoDB\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 81, \"created_at\": \"2022-12-02 13:54:31\", \"deleted_at\": null, \"updated_at\": \"2022-12-14 19:25:44\", \"is_attached\": false}}'),(NULL,0,'2023-03-03 17:49:31',NULL,314,'1',35,NULL,NULL,NULL,1,'{\"new\": {\"id\": 35, \"uid\": 1, \"icon\": \"caise-SQLServer$$\", \"name\": \"mssql\", \"alias\": \"MSSQL\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 81, \"created_at\": \"2022-12-02 13:56:01\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:49:31\", \"is_attached\": false}, \"old\": {\"id\": 35, \"uid\": 1, \"icon\": \"\", \"name\": \"mssql\", \"alias\": \"MSSQL\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 81, \"created_at\": \"2022-12-02 13:56:01\", \"deleted_at\": null, \"updated_at\": \"2022-12-14 19:25:44\", \"is_attached\": false}}'),(NULL,0,'2023-03-03 17:49:46',NULL,315,'1',36,NULL,NULL,NULL,1,'{\"new\": {\"id\": 36, \"uid\": 1, \"icon\": \"caise-nginx$$\", \"name\": \"nginx\", \"alias\": \"Nginx\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 89, \"created_at\": \"2022-12-02 14:20:07\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:49:46\", \"is_attached\": false}, \"old\": {\"id\": 36, \"uid\": 1, \"icon\": \"\", \"name\": \"nginx\", \"alias\": \"Nginx\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 89, \"created_at\": \"2022-12-02 14:20:07\", \"deleted_at\": null, \"updated_at\": \"2022-12-14 19:25:44\", \"is_attached\": false}}'),(NULL,0,'2023-03-03 17:49:58',NULL,316,'1',37,NULL,NULL,NULL,1,'{\"new\": {\"id\": 37, \"uid\": 1, \"icon\": \"caise-apache$$\", \"name\": \"apache\", \"alias\": \"Apache\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 89, \"created_at\": \"2022-12-02 14:20:49\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:49:58\", \"is_attached\": false}, \"old\": {\"id\": 37, \"uid\": 1, \"icon\": \"\", \"name\": \"apache\", \"alias\": \"Apache\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 89, \"created_at\": \"2022-12-02 14:20:49\", \"deleted_at\": null, \"updated_at\": \"2022-12-14 19:25:44\", \"is_attached\": false}}'),(NULL,0,'2023-03-03 17:50:08',NULL,317,'1',38,NULL,NULL,NULL,1,'{\"new\": {\"id\": 38, \"uid\": 1, \"icon\": \"caise-tomcat$$\", \"name\": \"tomcat\", \"alias\": \"Tomcat\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 89, \"created_at\": \"2022-12-02 14:21:04\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:50:08\", \"is_attached\": false}, \"old\": {\"id\": 38, \"uid\": 1, \"icon\": \"\", \"name\": \"tomcat\", \"alias\": \"Tomcat\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 89, \"created_at\": \"2022-12-02 14:21:04\", \"deleted_at\": null, \"updated_at\": \"2022-12-14 19:25:44\", \"is_attached\": false}}'),(NULL,0,'2023-03-03 17:50:21',NULL,318,'1',9,NULL,NULL,NULL,1,'{\"new\": {\"id\": 9, \"uid\": null, \"icon\": \"caise-docker$$\", \"name\": \"docker\", \"alias\": \"docker\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 9, \"created_at\": \"2021-11-24 09:45:10\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:50:21\", \"is_attached\": false}, \"old\": {\"id\": 9, \"uid\": null, \"icon\": null, \"name\": \"docker\", \"alias\": \"docker\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 9, \"created_at\": \"2021-11-24 09:45:10\", \"deleted_at\": null, \"updated_at\": \"2022-12-14 19:25:44\", \"is_attached\": false}}'),(NULL,0,'2023-03-03 17:50:36',NULL,319,'4',4,23,NULL,NULL,1,'{\"new\": {\"id\": 23, \"uid\": null, \"name\": \"server_name\", \"alias\": \"服务器名\", \"option\": {}, \"default\": {\"default\": \"10\"}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:40:03\", \"deleted_at\": \"2022-12-14 19:25:41\", \"updated_at\": \"2023-03-03 17:50:36\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 23, \"uid\": null, \"name\": \"server_name\", \"alias\": \"服务器名5\", \"option\": {}, \"default\": {\"default\": \"10\"}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:40:03\", \"deleted_at\": \"2022-12-14 19:25:41\", \"updated_at\": \"2023-01-04 14:50:16\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-03-03 17:50:49',NULL,320,'4',4,34,NULL,NULL,1,'{\"new\": {\"id\": 34, \"uid\": null, \"name\": \"status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:01:59\", \"deleted_at\": \"2022-12-14 19:25:43\", \"updated_at\": \"2022-12-14 19:25:43\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"在线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#065C30\", \"backgroundColor\": \"#D9F7BE\"}}], [\"下线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#881111\", \"backgroundColor\": \"#FFCCC7\"}}], [\"待用\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#0A483F\", \"backgroundColor\": \"#BAE7FF\"}}], [\"维修\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#622C0A\", \"backgroundColor\": \"#FFD8BF\"}}], [\"重装\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#5C4D0E\", \"backgroundColor\": \"#FFF1B8\"}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 34, \"uid\": null, \"name\": \"status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:01:59\", \"deleted_at\": \"2022-12-14 19:25:43\", \"updated_at\": \"2022-12-14 19:25:43\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"在线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#065C30\", \"backgroundColor\": \"#D9F7BE\"}}], [\"下线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#881111\", \"backgroundColor\": \"#FFCCC7\"}}], [\"待用\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#0A483F\", \"backgroundColor\": \"#BAE7FF\"}}], [\"维修\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#622C0A\", \"backgroundColor\": \"#FFD8BF\"}}], [\"重装\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#5C4D0E\", \"backgroundColor\": \"#FFF1B8\"}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-03-03 17:50:49',NULL,321,'4',5,34,NULL,NULL,1,'{\"new\": {\"id\": 34, \"uid\": null, \"name\": \"status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:01:59\", \"deleted_at\": \"2022-12-14 19:25:43\", \"updated_at\": \"2022-12-14 19:25:43\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"在线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#065C30\", \"backgroundColor\": \"#D9F7BE\"}}], [\"下线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#881111\", \"backgroundColor\": \"#FFCCC7\"}}], [\"待用\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#0A483F\", \"backgroundColor\": \"#BAE7FF\"}}], [\"维修\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#622C0A\", \"backgroundColor\": \"#FFD8BF\"}}], [\"重装\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#5C4D0E\", \"backgroundColor\": \"#FFF1B8\"}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 34, \"uid\": null, \"name\": \"status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:01:59\", \"deleted_at\": \"2022-12-14 19:25:43\", \"updated_at\": \"2022-12-14 19:25:43\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"在线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#065C30\", \"backgroundColor\": \"#D9F7BE\"}}], [\"下线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#881111\", \"backgroundColor\": \"#FFCCC7\"}}], [\"待用\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#0A483F\", \"backgroundColor\": \"#BAE7FF\"}}], [\"维修\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#622C0A\", \"backgroundColor\": \"#FFD8BF\"}}], [\"重装\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#5C4D0E\", \"backgroundColor\": \"#FFF1B8\"}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-03-03 17:50:49',NULL,322,'4',9,34,NULL,NULL,1,'{\"new\": {\"id\": 34, \"uid\": null, \"name\": \"status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:01:59\", \"deleted_at\": \"2022-12-14 19:25:43\", \"updated_at\": \"2022-12-14 19:25:43\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"在线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#065C30\", \"backgroundColor\": \"#D9F7BE\"}}], [\"下线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#881111\", \"backgroundColor\": \"#FFCCC7\"}}], [\"待用\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#0A483F\", \"backgroundColor\": \"#BAE7FF\"}}], [\"维修\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#622C0A\", \"backgroundColor\": \"#FFD8BF\"}}], [\"重装\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#5C4D0E\", \"backgroundColor\": \"#FFF1B8\"}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 34, \"uid\": null, \"name\": \"status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:01:59\", \"deleted_at\": \"2022-12-14 19:25:43\", \"updated_at\": \"2022-12-14 19:25:43\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"在线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#065C30\", \"backgroundColor\": \"#D9F7BE\"}}], [\"下线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#881111\", \"backgroundColor\": \"#FFCCC7\"}}], [\"待用\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#0A483F\", \"backgroundColor\": \"#BAE7FF\"}}], [\"维修\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#622C0A\", \"backgroundColor\": \"#FFD8BF\"}}], [\"重装\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#5C4D0E\", \"backgroundColor\": \"#FFF1B8\"}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-03-03 17:50:49',NULL,323,'4',32,34,NULL,NULL,1,'{\"new\": {\"id\": 34, \"uid\": null, \"name\": \"status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:01:59\", \"deleted_at\": \"2022-12-14 19:25:43\", \"updated_at\": \"2022-12-14 19:25:43\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"在线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#065C30\", \"backgroundColor\": \"#D9F7BE\"}}], [\"下线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#881111\", \"backgroundColor\": \"#FFCCC7\"}}], [\"待用\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#0A483F\", \"backgroundColor\": \"#BAE7FF\"}}], [\"维修\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#622C0A\", \"backgroundColor\": \"#FFD8BF\"}}], [\"重装\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#5C4D0E\", \"backgroundColor\": \"#FFF1B8\"}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 34, \"uid\": null, \"name\": \"status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:01:59\", \"deleted_at\": \"2022-12-14 19:25:43\", \"updated_at\": \"2022-12-14 19:25:43\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"在线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#065C30\", \"backgroundColor\": \"#D9F7BE\"}}], [\"下线\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#881111\", \"backgroundColor\": \"#FFCCC7\"}}], [\"待用\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#0A483F\", \"backgroundColor\": \"#BAE7FF\"}}], [\"维修\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#622C0A\", \"backgroundColor\": \"#FFD8BF\"}}], [\"重装\", {\"icon\": {\"color\": \"\"}, \"style\": {\"color\": \"#5C4D0E\", \"backgroundColor\": \"#FFF1B8\"}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-03-03 17:52:38',NULL,324,'4',4,35,NULL,NULL,1,'{\"new\": {\"id\": 35, \"uid\": null, \"name\": \"env\", \"alias\": \"环境\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:03:04\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2022-12-14 19:25:42\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"test\", {\"icon\": {\"name\": \"huiyiguanli\", \"color\": \"\"}, \"style\": {}}], [\"ppe\", {\"icon\": {\"name\": \"renwuguanli\", \"color\": \"\"}, \"style\": {}}], [\"prod\", {\"icon\": {\"name\": \"jiangbei\", \"color\": \"\"}, \"style\": {\"color\": \"#741717\"}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 35, \"uid\": null, \"name\": \"env\", \"alias\": \"环境\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:03:04\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2022-12-14 19:25:42\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"test\", {\"icon\": {\"name\": \"huiyiguanli\", \"color\": \"\"}, \"style\": {}}], [\"ppe\", {\"icon\": {\"name\": \"renwuguanli\", \"color\": \"\"}, \"style\": {}}], [\"prod\", {\"icon\": {\"name\": \"jiangbei\", \"color\": \"\"}, \"style\": {}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-03-03 17:52:38',NULL,325,'4',5,35,NULL,NULL,1,'{\"new\": {\"id\": 35, \"uid\": null, \"name\": \"env\", \"alias\": \"环境\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:03:04\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2022-12-14 19:25:42\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"test\", {\"icon\": {\"name\": \"huiyiguanli\", \"color\": \"\"}, \"style\": {}}], [\"ppe\", {\"icon\": {\"name\": \"renwuguanli\", \"color\": \"\"}, \"style\": {}}], [\"prod\", {\"icon\": {\"name\": \"jiangbei\", \"color\": \"\"}, \"style\": {\"color\": \"#741717\"}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 35, \"uid\": null, \"name\": \"env\", \"alias\": \"环境\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:03:04\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2022-12-14 19:25:42\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"test\", {\"icon\": {\"name\": \"huiyiguanli\", \"color\": \"\"}, \"style\": {}}], [\"ppe\", {\"icon\": {\"name\": \"renwuguanli\", \"color\": \"\"}, \"style\": {}}], [\"prod\", {\"icon\": {\"name\": \"jiangbei\", \"color\": \"\"}, \"style\": {}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-03-03 17:52:38',NULL,326,'4',9,35,NULL,NULL,1,'{\"new\": {\"id\": 35, \"uid\": null, \"name\": \"env\", \"alias\": \"环境\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:03:04\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2022-12-14 19:25:42\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"test\", {\"icon\": {\"name\": \"huiyiguanli\", \"color\": \"\"}, \"style\": {}}], [\"ppe\", {\"icon\": {\"name\": \"renwuguanli\", \"color\": \"\"}, \"style\": {}}], [\"prod\", {\"icon\": {\"name\": \"jiangbei\", \"color\": \"\"}, \"style\": {\"color\": \"#741717\"}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 35, \"uid\": null, \"name\": \"env\", \"alias\": \"环境\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2021-11-24 11:03:04\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2022-12-14 19:25:42\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"test\", {\"icon\": {\"name\": \"huiyiguanli\", \"color\": \"\"}, \"style\": {}}], [\"ppe\", {\"icon\": {\"name\": \"renwuguanli\", \"color\": \"\"}, \"style\": {}}], [\"prod\", {\"icon\": {\"name\": \"jiangbei\", \"color\": \"\"}, \"style\": {}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-03-03 17:53:18',NULL,327,'4',4,25,NULL,NULL,1,'{\"new\": {\"id\": 25, \"uid\": null, \"name\": \"private_ip\", \"alias\": \"内网IP\", \"option\": {\"fontOptions\": {\"color\": \"#606266\", \"fontStyle\": \"initial\", \"fontWeight\": \"bold\", \"textDecoration\": \"initial\"}}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:41:47\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2023-03-03 17:53:18\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 25, \"uid\": null, \"name\": \"private_ip\", \"alias\": \"内网IP\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:41:47\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2022-12-14 19:25:42\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-03-03 17:53:18',NULL,328,'4',5,25,NULL,NULL,1,'{\"new\": {\"id\": 25, \"uid\": null, \"name\": \"private_ip\", \"alias\": \"内网IP\", \"option\": {\"fontOptions\": {\"color\": \"#606266\", \"fontStyle\": \"initial\", \"fontWeight\": \"bold\", \"textDecoration\": \"initial\"}}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:41:47\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2023-03-03 17:53:18\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 25, \"uid\": null, \"name\": \"private_ip\", \"alias\": \"内网IP\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:41:47\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2022-12-14 19:25:42\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-03-03 17:53:18',NULL,329,'4',9,25,NULL,NULL,1,'{\"new\": {\"id\": 25, \"uid\": null, \"name\": \"private_ip\", \"alias\": \"内网IP\", \"option\": {\"fontOptions\": {\"color\": \"#606266\", \"fontStyle\": \"initial\", \"fontWeight\": \"bold\", \"textDecoration\": \"initial\"}}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:41:47\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2023-03-03 17:53:18\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 25, \"uid\": null, \"name\": \"private_ip\", \"alias\": \"内网IP\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:41:47\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2022-12-14 19:25:42\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-03-08 16:50:52',NULL,330,'3',41,98,NULL,NULL,1,'{\"id\": 98, \"uid\": 1, \"name\": \"xxx_name\", \"alias\": \"xxx\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2023-03-08 16:50:34\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-03-08 16:50:52',NULL,331,'0',41,NULL,NULL,NULL,1,'{\"id\": 41, \"uid\": 1, \"icon\": \"caise-oracle$$\", \"name\": \"xxx\", \"alias\": \"xxx\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 98, \"created_at\": \"2023-03-08 16:50:52\", \"deleted_at\": null, \"updated_at\": null, \"is_attached\": false}'),(NULL,0,'2023-03-08 16:59:50',NULL,332,'3',41,33,NULL,NULL,1,'{\"id\": 33, \"uid\": null, \"name\": \"perm\", \"alias\": \"perm\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:59:57\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2022-12-14 19:25:42\", \"value_type\": \"6\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-03-08 16:59:50',NULL,333,'3',41,20,NULL,NULL,1,'{\"id\": 20, \"uid\": null, \"name\": \"rd_duty\", \"alias\": \"开发负责人\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:24:35\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2022-12-14 19:25:42\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-03-08 16:59:50',NULL,334,'3',41,22,NULL,NULL,1,'{\"id\": 22, \"uid\": null, \"name\": \"op_duty\", \"alias\": \"运维负责人\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": true, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:25:25\", \"deleted_at\": \"2022-12-14 19:25:44\", \"updated_at\": \"2023-02-07 13:56:47\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-03-08 16:59:59',NULL,335,'3',41,24,NULL,NULL,1,'{\"id\": 24, \"uid\": null, \"name\": \"oneagent_id\", \"alias\": \"AgentID\", \"option\": null, \"default\": null, \"deleted\": true, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2021-11-24 10:40:56\", \"deleted_at\": \"2022-12-14 19:25:42\", \"updated_at\": \"2022-12-14 19:25:42\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-05-23 14:59:07',NULL,336,'3',28,99,NULL,NULL,1,'{\"id\": 99, \"uid\": 1, \"name\": \"description\", \"alias\": \"描述\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2023-05-23 14:59:07\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-05-23 14:59:07',NULL,337,'4',28,99,NULL,NULL,1,'{\"new\": {\"id\": 427, \"order\": 0, \"attr_id\": 99, \"deleted\": false, \"type_id\": 28, \"created_at\": \"2023-05-23 14:59:07\", \"deleted_at\": null, \"updated_at\": \"2023-05-23 14:59:07\", \"is_required\": false, \"default_show\": false}, \"old\": {\"id\": 427, \"order\": 0, \"attr_id\": 99, \"deleted\": false, \"type_id\": 28, \"created_at\": \"2023-05-23 14:59:07\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2023-05-23 14:59:21',NULL,338,'3',28,100,NULL,NULL,1,'{\"id\": 100, \"uid\": 1, \"name\": \"ips\", \"alias\": \"IPs\", \"option\": {}, \"default\": {\"default\": []}, \"deleted\": false, \"is_link\": false, \"is_list\": true, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2023-05-23 14:59:21\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-05-23 14:59:21',NULL,339,'4',28,100,NULL,NULL,1,'{\"new\": {\"id\": 428, \"order\": 0, \"attr_id\": 100, \"deleted\": false, \"type_id\": 28, \"created_at\": \"2023-05-23 14:59:21\", \"deleted_at\": null, \"updated_at\": \"2023-05-23 14:59:21\", \"is_required\": false, \"default_show\": false}, \"old\": {\"id\": 428, \"order\": 0, \"attr_id\": 100, \"deleted\": false, \"type_id\": 28, \"created_at\": \"2023-05-23 14:59:21\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2023-05-23 15:18:03',NULL,340,'5',28,78,NULL,NULL,1,'{\"id\": 78, \"uid\": 1, \"name\": \"netdev_manufacturer\", \"alias\": \"设备厂商\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:35:33\", \"deleted_at\": \"2022-12-14 19:25:43\", \"updated_at\": \"2022-12-14 19:25:43\", \"value_type\": \"0\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-05-23 15:18:21',NULL,341,'3',28,101,NULL,NULL,1,'{\"id\": 101, \"uid\": 1, \"name\": \"netdev_manufacturer1\", \"alias\": \"设备厂商\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2023-05-23 15:18:21\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-05-23 15:18:21',NULL,342,'4',28,101,NULL,NULL,1,'{\"new\": {\"id\": 429, \"order\": 0, \"attr_id\": 101, \"deleted\": false, \"type_id\": 28, \"created_at\": \"2023-05-23 15:18:21\", \"deleted_at\": null, \"updated_at\": \"2023-05-23 15:18:21\", \"is_required\": false, \"default_show\": false}, \"old\": {\"id\": 429, \"order\": 0, \"attr_id\": 101, \"deleted\": false, \"type_id\": 28, \"created_at\": \"2023-05-23 15:18:21\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2023-05-23 15:19:04',NULL,343,'4',28,99,NULL,NULL,1,'{\"new\": {\"id\": 99, \"uid\": 1, \"name\": \"description\", \"alias\": \"描述\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2023-05-23 14:59:07\", \"deleted_at\": null, \"updated_at\": \"2023-05-23 15:19:04\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 99, \"uid\": 1, \"name\": \"description\", \"alias\": \"描述\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2023-05-23 14:59:07\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-05-23 15:19:58',NULL,344,'4',28,99,NULL,NULL,1,'{\"new\": {\"id\": 99, \"uid\": 1, \"name\": \"description\", \"alias\": \"描述\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2023-05-23 14:59:07\", \"deleted_at\": null, \"updated_at\": \"2023-05-23 15:19:04\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 99, \"uid\": 1, \"name\": \"description\", \"alias\": \"描述\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2023-05-23 14:59:07\", \"deleted_at\": null, \"updated_at\": \"2023-05-23 15:19:04\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-05-23 15:20:09',NULL,345,'5',28,99,NULL,NULL,1,'{\"id\": 99, \"uid\": 1, \"name\": \"description\", \"alias\": \"描述\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2023-05-23 14:59:07\", \"deleted_at\": null, \"updated_at\": \"2023-05-23 15:19:04\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-05-23 15:20:18',NULL,346,'3',28,99,NULL,NULL,1,'{\"id\": 99, \"uid\": 1, \"name\": \"description\", \"alias\": \"描述\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2023-05-23 14:59:07\", \"deleted_at\": null, \"updated_at\": \"2023-05-23 15:19:04\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-05-23 15:24:36',NULL,347,'4',28,74,NULL,NULL,1,'{\"new\": {\"id\": 74, \"uid\": 1, \"name\": \"netdev_status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2022-12-02 13:28:01\", \"deleted_at\": \"2022-12-14 19:25:43\", \"updated_at\": \"2023-05-23 15:24:36\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"choice_value\": [[\"在线\", {\"icon\": {\"name\": \"caise-zaixian\", \"color\": \"\"}, \"style\": {\"fontWeight\": \"bold\"}}], [\"下线\", {\"icon\": {\"name\": \"caise-xiaxian\", \"color\": \"\"}, \"style\": {\"fontWeight\": \"bold\"}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 74, \"uid\": 1, \"name\": \"netdev_status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:28:01\", \"deleted_at\": \"2022-12-14 19:25:43\", \"updated_at\": \"2022-12-14 19:25:43\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-05-23 15:24:36',NULL,348,'4',29,74,NULL,NULL,1,'{\"new\": {\"id\": 74, \"uid\": 1, \"name\": \"netdev_status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2022-12-02 13:28:01\", \"deleted_at\": \"2022-12-14 19:25:43\", \"updated_at\": \"2023-05-23 15:24:36\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"choice_value\": [[\"在线\", {\"icon\": {\"name\": \"caise-zaixian\", \"color\": \"\"}, \"style\": {\"fontWeight\": \"bold\"}}], [\"下线\", {\"icon\": {\"name\": \"caise-xiaxian\", \"color\": \"\"}, \"style\": {\"fontWeight\": \"bold\"}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 74, \"uid\": 1, \"name\": \"netdev_status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:28:01\", \"deleted_at\": \"2022-12-14 19:25:43\", \"updated_at\": \"2022-12-14 19:25:43\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-05-23 15:24:36',NULL,349,'4',30,74,NULL,NULL,1,'{\"new\": {\"id\": 74, \"uid\": 1, \"name\": \"netdev_status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2022-12-02 13:28:01\", \"deleted_at\": \"2022-12-14 19:25:43\", \"updated_at\": \"2023-05-23 15:24:36\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"choice_value\": [[\"在线\", {\"icon\": {\"name\": \"caise-zaixian\", \"color\": \"\"}, \"style\": {\"fontWeight\": \"bold\"}}], [\"下线\", {\"icon\": {\"name\": \"caise-xiaxian\", \"color\": \"\"}, \"style\": {\"fontWeight\": \"bold\"}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 74, \"uid\": 1, \"name\": \"netdev_status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:28:01\", \"deleted_at\": \"2022-12-14 19:25:43\", \"updated_at\": \"2022-12-14 19:25:43\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-05-23 15:24:36',NULL,350,'4',31,74,NULL,NULL,1,'{\"new\": {\"id\": 74, \"uid\": 1, \"name\": \"netdev_status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2022-12-02 13:28:01\", \"deleted_at\": \"2022-12-14 19:25:43\", \"updated_at\": \"2023-05-23 15:24:36\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"choice_value\": [[\"在线\", {\"icon\": {\"name\": \"caise-zaixian\", \"color\": \"\"}, \"style\": {\"fontWeight\": \"bold\"}}], [\"下线\", {\"icon\": {\"name\": \"caise-xiaxian\", \"color\": \"\"}, \"style\": {\"fontWeight\": \"bold\"}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 74, \"uid\": 1, \"name\": \"netdev_status\", \"alias\": \"状态\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": true, \"is_choice\": false, \"is_unique\": false, \"created_at\": \"2022-12-02 13:28:01\", \"deleted_at\": \"2022-12-14 19:25:43\", \"updated_at\": \"2022-12-14 19:25:43\", \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": true, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-07-11 15:13:59',NULL,351,'3',33,102,NULL,NULL,46,'{\"id\": 102, \"uid\": 46, \"name\": \"ldap\", \"alias\": \"业务aza\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2023-07-11 15:13:59\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}'),(NULL,0,'2023-07-11 15:13:59',NULL,352,'4',33,102,NULL,NULL,46,'{\"new\": {\"id\": 431, \"order\": 0, \"attr_id\": 102, \"deleted\": false, \"type_id\": 33, \"created_at\": \"2023-07-11 15:13:59\", \"deleted_at\": null, \"updated_at\": \"2023-07-11 15:13:59\", \"is_required\": true, \"default_show\": false}, \"old\": {\"id\": 431, \"order\": 0, \"attr_id\": 102, \"deleted\": false, \"type_id\": 33, \"created_at\": \"2023-07-11 15:13:59\", \"deleted_at\": null, \"updated_at\": null, \"is_required\": false, \"default_show\": true}}'),(NULL,0,'2023-07-11 15:14:28',NULL,353,'4',33,102,NULL,NULL,46,'{\"new\": {\"id\": 102, \"uid\": 46, \"name\": \"ldap\", \"alias\": \"业务aza\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2023-07-11 15:13:59\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"1\", {\"icon\": {}, \"style\": {}}], [\"aaa\", {\"icon\": {\"name\": \"caise-zaixian\", \"color\": \"\"}, \"style\": {}}], [\"asdasda\", {\"icon\": {}, \"style\": {}}], [\"assda\", {\"icon\": {}, \"style\": {}}], [\"qqqq\", {\"icon\": {}, \"style\": {}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}, \"old\": {\"id\": 102, \"uid\": 46, \"name\": \"ldap\", \"alias\": \"业务aza\", \"option\": {}, \"default\": {\"default\": null}, \"deleted\": false, \"is_link\": false, \"is_list\": false, \"is_index\": false, \"is_choice\": true, \"is_unique\": false, \"created_at\": \"2023-07-11 15:13:59\", \"deleted_at\": null, \"updated_at\": null, \"value_type\": \"2\", \"is_computed\": false, \"is_password\": false, \"is_sortable\": false, \"choice_value\": [[\"1\", {\"icon\": {}, \"style\": {}}], [\"aaa\", {\"icon\": {\"name\": \"caise-zaixian\", \"color\": \"\"}, \"style\": {}}], [\"asdasda\", {\"icon\": {}, \"style\": {}}], [\"assda\", {\"icon\": {}, \"style\": {}}]], \"compute_expr\": null, \"compute_script\": null, \"choice_web_hook\": null}}'),(NULL,0,'2023-07-11 16:57:08',NULL,354,'13',1,NULL,NULL,NULL,1,'{\"child\": {\"id\": 2, \"uid\": null, \"icon\": \"caise-chanpin$$\", \"name\": \"product\", \"alias\": \"产品\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 2, \"created_at\": \"2021-11-23 19:56:40\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:48:29\", \"is_attached\": false, \"default_order_attr\": null}, \"parent_id\": {\"id\": 1, \"uid\": null, \"icon\": \"caise-bumen$$\", \"name\": \"bu\", \"alias\": \"事业部\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 1, \"created_at\": \"2021-11-23 19:50:34\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:48:20\", \"is_attached\": false, \"default_order_attr\": null}, \"relation_type_id\": 1}'),(NULL,0,'2023-07-11 16:58:25',NULL,355,'13',2,NULL,NULL,NULL,1,'{\"child\": {\"id\": 3, \"uid\": null, \"icon\": \"caise-yingyong$$\", \"name\": \"project\", \"alias\": \"应用\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 3, \"created_at\": \"2021-11-23 19:58:15\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:48:36\", \"is_attached\": false, \"default_order_attr\": null}, \"parent_id\": {\"id\": 2, \"uid\": null, \"icon\": \"caise-chanpin$$\", \"name\": \"product\", \"alias\": \"产品\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 2, \"created_at\": \"2021-11-23 19:56:40\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:48:29\", \"is_attached\": false, \"default_order_attr\": null}, \"relation_type_id\": 1}'),(NULL,0,'2023-07-11 16:59:15',NULL,356,'13',3,NULL,NULL,NULL,1,'{\"child\": {\"id\": 4, \"uid\": null, \"icon\": \"caise-wuliji$$\", \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:46:17\", \"is_attached\": false, \"default_order_attr\": null}, \"parent_id\": {\"id\": 3, \"uid\": null, \"icon\": \"caise-yingyong$$\", \"name\": \"project\", \"alias\": \"应用\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 3, \"created_at\": \"2021-11-23 19:58:15\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:48:36\", \"is_attached\": false, \"default_order_attr\": null}, \"relation_type_id\": 3}'),(NULL,0,'2023-07-11 16:59:34',NULL,357,'12',3,NULL,NULL,NULL,1,'{\"child\": {\"id\": 4, \"uid\": null, \"icon\": \"caise-wuliji$$\", \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:46:17\", \"is_attached\": false, \"default_order_attr\": null}, \"parent\": {\"id\": 3, \"uid\": null, \"icon\": \"caise-yingyong$$\", \"name\": \"project\", \"alias\": \"应用\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 3, \"created_at\": \"2021-11-23 19:58:15\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:48:36\", \"is_attached\": false, \"default_order_attr\": null}, \"relation_type_id\": 3}'),(NULL,0,'2023-07-11 16:59:44',NULL,358,'12',3,NULL,NULL,NULL,1,'{\"child\": {\"id\": 5, \"uid\": null, \"icon\": \"caise-xuniji$$\", \"name\": \"vserver\", \"alias\": \"虚拟机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 5, \"created_at\": \"2021-11-23 20:08:52\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:46:29\", \"is_attached\": false, \"default_order_attr\": null}, \"parent\": {\"id\": 3, \"uid\": null, \"icon\": \"caise-yingyong$$\", \"name\": \"project\", \"alias\": \"应用\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 3, \"created_at\": \"2021-11-23 19:58:15\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:48:36\", \"is_attached\": false, \"default_order_attr\": null}, \"relation_type_id\": 3}'),(NULL,0,'2023-07-11 16:59:55',NULL,359,'12',3,NULL,NULL,NULL,1,'{\"child\": {\"id\": 9, \"uid\": null, \"icon\": \"caise-docker$$\", \"name\": \"docker\", \"alias\": \"docker\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 9, \"created_at\": \"2021-11-24 09:45:10\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:50:21\", \"is_attached\": false, \"default_order_attr\": null}, \"parent\": {\"id\": 3, \"uid\": null, \"icon\": \"caise-yingyong$$\", \"name\": \"project\", \"alias\": \"应用\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 3, \"created_at\": \"2021-11-23 19:58:15\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:48:36\", \"is_attached\": false, \"default_order_attr\": null}, \"relation_type_id\": 3}'),(NULL,0,'2023-07-11 17:00:03',NULL,360,'13',4,NULL,NULL,NULL,1,'{\"child\": {\"id\": 6, \"uid\": null, \"icon\": \"caise-neicun$$\", \"name\": \"RAM\", \"alias\": \"内存\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 6, \"created_at\": \"2021-11-23 20:36:55\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:47:18\", \"is_attached\": false, \"default_order_attr\": null}, \"parent_id\": {\"id\": 4, \"uid\": null, \"icon\": \"caise-wuliji$$\", \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:46:17\", \"is_attached\": false, \"default_order_attr\": null}, \"relation_type_id\": 1}'),(NULL,0,'2023-07-11 17:00:04',NULL,361,'13',4,NULL,NULL,NULL,1,'{\"child\": {\"id\": 7, \"uid\": null, \"icon\": \"caise-yingpan$$\", \"name\": \"harddisk\", \"alias\": \"硬盘\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 7, \"created_at\": \"2021-11-23 21:38:17\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:46:40\", \"is_attached\": false, \"default_order_attr\": null}, \"parent_id\": {\"id\": 4, \"uid\": null, \"icon\": \"caise-wuliji$$\", \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:46:17\", \"is_attached\": false, \"default_order_attr\": null}, \"relation_type_id\": 1}'),(NULL,0,'2023-07-11 17:00:06',NULL,362,'13',4,NULL,NULL,NULL,1,'{\"child\": {\"id\": 8, \"uid\": null, \"icon\": \"caise-wangka$$\", \"name\": \"NIC\", \"alias\": \"网卡\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 8, \"created_at\": \"2021-11-24 09:42:55\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:46:51\", \"is_attached\": false, \"default_order_attr\": null}, \"parent_id\": {\"id\": 4, \"uid\": null, \"icon\": \"caise-wuliji$$\", \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:46:17\", \"is_attached\": false, \"default_order_attr\": null}, \"relation_type_id\": 1}'),(NULL,0,'2023-07-11 17:00:16',NULL,363,'12',4,NULL,NULL,NULL,1,'{\"child\": {\"id\": 6, \"uid\": null, \"icon\": \"caise-neicun$$\", \"name\": \"RAM\", \"alias\": \"内存\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 6, \"created_at\": \"2021-11-23 20:36:55\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:47:18\", \"is_attached\": false, \"default_order_attr\": null}, \"parent\": {\"id\": 4, \"uid\": null, \"icon\": \"caise-wuliji$$\", \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:46:17\", \"is_attached\": false, \"default_order_attr\": null}, \"relation_type_id\": 1}'),(NULL,0,'2023-07-11 17:00:26',NULL,364,'12',4,NULL,NULL,NULL,1,'{\"child\": {\"id\": 7, \"uid\": null, \"icon\": \"caise-yingpan$$\", \"name\": \"harddisk\", \"alias\": \"硬盘\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 7, \"created_at\": \"2021-11-23 21:38:17\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:46:40\", \"is_attached\": false, \"default_order_attr\": null}, \"parent\": {\"id\": 4, \"uid\": null, \"icon\": \"caise-wuliji$$\", \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:46:17\", \"is_attached\": false, \"default_order_attr\": null}, \"relation_type_id\": 1}'),(NULL,0,'2023-07-11 17:00:34',NULL,365,'12',4,NULL,NULL,NULL,1,'{\"child\": {\"id\": 8, \"uid\": null, \"icon\": \"caise-wangka$$\", \"name\": \"NIC\", \"alias\": \"网卡\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 8, \"created_at\": \"2021-11-24 09:42:55\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:46:51\", \"is_attached\": false, \"default_order_attr\": null}, \"parent\": {\"id\": 4, \"uid\": null, \"icon\": \"caise-wuliji$$\", \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:46:17\", \"is_attached\": false, \"default_order_attr\": null}, \"relation_type_id\": 1}'),(NULL,0,'2023-07-11 17:03:02',NULL,366,'13',5,NULL,NULL,NULL,1,'{\"child\": {\"id\": 4, \"uid\": null, \"icon\": \"caise-wuliji$$\", \"name\": \"server\", \"alias\": \"物理机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 4, \"created_at\": \"2021-11-23 20:06:53\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:46:17\", \"is_attached\": false, \"default_order_attr\": null}, \"parent_id\": {\"id\": 5, \"uid\": null, \"icon\": \"caise-xuniji$$\", \"name\": \"vserver\", \"alias\": \"虚拟机\", \"order\": 0, \"deleted\": false, \"enabled\": true, \"unique_id\": 5, \"created_at\": \"2021-11-23 20:08:52\", \"deleted_at\": null, \"updated_at\": \"2023-03-03 17:46:29\", \"is_attached\": false, \"default_order_attr\": null}, \"relation_type_id\": 1}');
/*!40000 ALTER TABLE `c_ci_type_histories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_ci_type_relations`
--

DROP TABLE IF EXISTS `c_ci_type_relations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_ci_type_relations` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  `child_id` int(11) NOT NULL,
  `relation_type_id` int(11) NOT NULL,
  `constraint` enum('0','1','2') COLLATE utf8_unicode_ci DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `parent_id` (`parent_id`),
  KEY `child_id` (`child_id`),
  KEY `relation_type_id` (`relation_type_id`),
  KEY `ix_c_ci_type_relations_deleted` (`deleted`),
  CONSTRAINT `c_ci_type_relations_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `c_ci_types` (`id`),
  CONSTRAINT `c_ci_type_relations_ibfk_2` FOREIGN KEY (`child_id`) REFERENCES `c_ci_types` (`id`),
  CONSTRAINT `c_ci_type_relations_ibfk_3` FOREIGN KEY (`relation_type_id`) REFERENCES `c_relation_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_ci_type_relations`
--

LOCK TABLES `c_ci_type_relations` WRITE;
/*!40000 ALTER TABLE `c_ci_type_relations` DISABLE KEYS */;
INSERT INTO `c_ci_type_relations` VALUES (NULL,0,'2023-07-11 16:57:17',NULL,17,1,2,1,'0'),(NULL,0,'2023-07-11 16:58:34',NULL,18,2,3,1,'0'),(NULL,0,'2023-07-11 16:59:34',NULL,19,3,4,3,'0'),(NULL,0,'2023-07-11 16:59:43',NULL,20,3,5,3,'0'),(NULL,0,'2023-07-11 16:59:55',NULL,21,3,9,3,'0'),(NULL,0,'2023-07-11 17:00:16',NULL,22,4,6,1,'0'),(NULL,0,'2023-07-11 17:00:25',NULL,23,4,7,1,'0'),(NULL,0,'2023-07-11 17:00:33',NULL,24,4,8,1,'0');
/*!40000 ALTER TABLE `c_ci_type_relations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_ci_types`
--

DROP TABLE IF EXISTS `c_ci_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_ci_types` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `alias` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `unique_id` int(11) NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  `is_attached` tinyint(1) NOT NULL,
  `order` smallint(6) NOT NULL,
  `uid` int(11) DEFAULT NULL,
  `icon` text COLLATE utf8_unicode_ci,
  `default_order_attr` varchar(33) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `unique_id` (`unique_id`),
  KEY `ix_c_ci_types_deleted` (`deleted`),
  KEY `c_ci_types_uid` (`uid`),
  CONSTRAINT `c_ci_types_ibfk_1` FOREIGN KEY (`unique_id`) REFERENCES `c_attributes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_ci_types`
--

LOCK TABLES `c_ci_types` WRITE;
/*!40000 ALTER TABLE `c_ci_types` DISABLE KEYS */;
INSERT INTO `c_ci_types` VALUES (NULL,0,'2021-11-23 19:50:34','2023-03-03 17:48:20',1,'bu','事业部',1,1,0,0,NULL,'caise-bumen$$',NULL),(NULL,0,'2021-11-23 19:56:40','2023-03-03 17:48:29',2,'product','产品',2,1,0,0,NULL,'caise-chanpin$$',NULL),(NULL,0,'2021-11-23 19:58:15','2023-03-03 17:48:36',3,'project','应用',3,1,0,0,NULL,'caise-yingyong$$',NULL),(NULL,0,'2021-11-23 20:06:53','2023-03-03 17:46:17',4,'server','物理机',4,1,0,0,NULL,'caise-wuliji$$',NULL),(NULL,0,'2021-11-23 20:08:52','2023-03-03 17:46:29',5,'vserver','虚拟机',5,1,0,0,NULL,'caise-xuniji$$',NULL),(NULL,0,'2021-11-23 20:36:55','2023-03-03 17:47:18',6,'RAM','内存',6,1,0,0,NULL,'caise-neicun$$',NULL),(NULL,0,'2021-11-23 21:38:17','2023-03-03 17:46:40',7,'harddisk','硬盘',7,1,0,0,NULL,'caise-yingpan$$',NULL),(NULL,0,'2021-11-24 09:42:55','2023-03-03 17:46:51',8,'NIC','网卡',8,1,0,0,NULL,'caise-wangka$$',NULL),(NULL,0,'2021-11-24 09:45:10','2023-03-03 17:50:21',9,'docker','docker',9,1,0,0,NULL,'caise-docker$$',NULL),(NULL,0,'2022-12-02 13:18:17','2023-03-03 17:47:32',28,'switch','交换机',71,1,0,0,1,'caise-jiaohuanji$$',NULL),(NULL,0,'2022-12-02 13:20:36','2023-03-03 17:47:43',29,'router','路由器',72,1,0,0,1,'caise-luyouqi$$',NULL),(NULL,0,'2022-12-02 13:21:51','2023-03-03 17:47:55',30,'firewall','防火墙',73,1,0,0,1,'caise-fanghuoqiang$$',NULL),(NULL,0,'2022-12-02 13:47:54','2023-03-03 17:48:07',31,'load_balance','负载均衡',80,1,0,0,1,'caise-fuzaijunheng$$',NULL),(NULL,0,'2022-12-02 13:53:30','2023-03-03 17:48:53',32,'mysql','MySQL',81,1,0,0,1,'caise-mySQL$$',NULL),(NULL,0,'2022-12-02 13:54:13','2023-03-03 17:49:06',33,'postgresql','PostgreSQL',81,1,0,0,1,'caise-PostgreSQL$$',NULL),(NULL,0,'2022-12-02 13:54:31','2023-03-03 17:49:15',34,'mongodb','MongoDB',81,1,0,0,1,'caise-mongodb$$',NULL),(NULL,0,'2022-12-02 13:56:01','2023-03-03 17:49:31',35,'mssql','MSSQL',81,1,0,0,1,'caise-SQLServer$$',NULL),(NULL,0,'2022-12-02 14:20:07','2023-03-03 17:49:46',36,'nginx','Nginx',89,1,0,0,1,'caise-nginx$$',NULL),(NULL,0,'2022-12-02 14:20:49','2023-03-03 17:49:58',37,'apache','Apache',89,1,0,0,1,'caise-apache$$',NULL),(NULL,0,'2022-12-02 14:21:04','2023-03-03 17:50:08',38,'tomcat','Tomcat',89,1,0,0,1,'caise-tomcat$$',NULL);
/*!40000 ALTER TABLE `c_ci_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_cis`
--

DROP TABLE IF EXISTS `c_cis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_cis` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` int(11) NOT NULL,
  `status` enum('1','0') COLLATE utf8_unicode_ci DEFAULT NULL,
  `heartbeat` datetime DEFAULT NULL,
  `a` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `type_id` (`type_id`),
  KEY `ix_c_cis_deleted` (`deleted`),
  CONSTRAINT `c_cis_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `c_ci_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_cis`
--

LOCK TABLES `c_cis` WRITE;
/*!40000 ALTER TABLE `c_cis` DISABLE KEYS */;
INSERT INTO `c_cis` VALUES (NULL,0,'2023-07-11 17:49:51',NULL,1,1,NULL,'2023-07-11 17:49:51',0),(NULL,0,'2023-07-11 17:50:29',NULL,2,2,NULL,'2023-07-11 17:50:29',0),(NULL,0,'2023-07-11 17:50:36',NULL,3,3,NULL,'2023-07-11 17:50:36',0),(NULL,0,'2023-07-11 17:51:01',NULL,4,4,NULL,'2023-07-11 17:51:01',0);
/*!40000 ALTER TABLE `c_cis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_prv`
--

DROP TABLE IF EXISTS `c_prv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_prv` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `cr_ids` json DEFAULT NULL,
  `is_public` tinyint(4) DEFAULT '0',
  `uid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_c_preference_relation_views_name` (`name`),
  KEY `ix_c_preference_relation_views_deleted` (`deleted`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_prv`
--

LOCK TABLES `c_prv` WRITE;
/*!40000 ALTER TABLE `c_prv` DISABLE KEYS */;
INSERT INTO `c_prv` VALUES (NULL, 0, '2023-05-23 17:21:33', NULL, 18, '服务树', '[{\"child_id\": 2, \"parent_id\": 1}, {\"child_id\": 3, \"parent_id\": 2}]', 0, 1);
/*!40000 ALTER TABLE `c_prv` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_psa`
--

DROP TABLE IF EXISTS `c_psa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_psa` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  `attr_id` int(11) DEFAULT NULL,
  `order` smallint(6) DEFAULT NULL,
  `is_fixed` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `type_id` (`type_id`),
  KEY `attr_id` (`attr_id`),
  KEY `ix_c_preference_show_attributes_deleted` (`deleted`),
  KEY `ix_c_preference_show_attributes_uid` (`uid`),
  CONSTRAINT `c_psa_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `c_ci_types` (`id`),
  CONSTRAINT `c_psa_ibfk_2` FOREIGN KEY (`attr_id`) REFERENCES `c_attributes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1062 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_psa`
--

LOCK TABLES `c_psa` WRITE;
/*!40000 ALTER TABLE `c_psa` DISABLE KEYS */;
INSERT INTO `c_psa` VALUES (NULL, 0, '2022-10-27 11:50:52', NULL, 275, 1, 3, 3, 0, 0),
	(NULL, 0, '2022-10-27 11:50:52', NULL, 276, 1, 3, 17, 1, 0),
	(NULL, 0, '2022-10-27 11:50:52', NULL, 277, 1, 3, 18, 2, 0),
	(NULL, 0, '2022-10-27 11:50:52', NULL, 278, 1, 3, 19, 3, 0),
	(NULL, 0, '2022-10-27 11:50:52', NULL, 279, 1, 3, 20, 4, 0),
	(NULL, 0, '2022-10-27 11:50:52', NULL, 280, 1, 3, 21, 5, 0),
	(NULL, 0, '2022-10-27 11:50:52', NULL, 281, 1, 3, 22, 6, 0),
	(NULL, 0, '2022-12-01 20:59:47', '2023-01-09 10:33:37', 488, 1, 4, 4, 1, 0),
	(NULL, 0, '2022-12-02 13:44:37', '2023-03-03 17:22:55', 489, 1, 1, 11, 3, 0),
	(NULL, 0, '2022-12-02 13:44:37', '2023-03-03 17:22:55', 490, 1, 1, 12, 4, 0),
	(NULL, 0, '2022-12-08 14:16:32', '2023-07-06 16:49:13', 530, 1, 4, 35, 2, 0),
	(NULL, 0, '2022-12-08 14:16:32', '2023-04-12 14:42:32', 533, 1, 4, 25, 0, 1),
	(NULL, 0, '2022-12-08 20:46:57', '2023-07-06 16:49:13', 633, 1, 4, 20, 5, 0),
	(NULL, 0, '2022-12-08 20:46:57', '2023-07-06 16:49:13', 634, 1, 4, 22, 4, 0),
	(NULL, 0, '2022-12-08 20:46:57', '2023-07-06 16:49:13', 635, 1, 4, 34, 3, 0),
	(NULL, 0, '2023-02-02 16:36:46', '2023-07-06 16:49:13', 714, 1, 4, 51, 12, 0),
	(NULL, 0, '2023-03-03 17:22:55', NULL, 740, 1, 1, 1, 0, 0),
	(NULL, 0, '2023-03-03 17:22:55', NULL, 741, 1, 1, 95, 1, 0),
	(NULL, 0, '2023-03-03 17:22:55', NULL, 742, 1, 1, 10, 2, 0),
	(NULL, 0, '2023-04-12 14:43:05', '2023-07-06 16:49:13', 956, 1, 4, 27, 11, 0),
	(NULL, 0, '2023-04-12 14:43:05', '2023-07-06 16:49:13', 957, 1, 4, 31, 9, 0),
	(NULL, 0, '2023-04-12 14:43:05', '2023-07-06 16:49:13', 958, 1, 4, 30, 8, 0),
	(NULL, 0, '2023-04-12 14:43:05', NULL, 959, 1, 4, 32, 10, 0),
	(NULL, 0, '2023-07-06 16:49:13', NULL, 1000, 1, 4, 26, 6, 0),
	(NULL, 0, '2023-07-06 16:49:13', NULL, 1001, 1, 4, 42, 7, 0),
	(NULL, 0, '2023-07-06 16:49:13', NULL, 1002, 1, 4, 24, 13, 0),
	(NULL, 0, '2023-07-11 17:50:20', NULL, 1060, 1, 2, 15, 3, 0),
	(NULL, 0, '2023-07-11 17:50:20', NULL, 1059, 1, 2, 14, 2, 0),
	(NULL, 0, '2023-07-11 17:50:20', NULL, 1058, 1, 2, 13, 1, 0),
	(NULL, 0, '2023-07-11 17:50:20', NULL, 1057, 1, 2, 2, 0, 0),
	(NULL, 0, '2023-07-11 17:50:20', NULL, 1061, 1, 2, 16, 4, 0),
	(NULL, 0, '2023-07-10 16:26:19', NULL, 1008, 46, 4, 22, 5, 0),
	(NULL, 0, '2023-07-10 16:26:19', NULL, 1009, 46, 4, 33, 6, 0),
	(NULL, 0, '2023-07-10 16:26:19', NULL, 1010, 46, 4, 34, 7, 0),
	(NULL, 0, '2023-07-10 16:26:19', NULL, 1011, 46, 4, 35, 8, 0),
	(NULL, 0, '2023-07-10 16:26:19', NULL, 1012, 46, 4, 4, 9, 0),
	(NULL, 0, '2023-07-10 16:26:24', NULL, 1013, 46, 5, 62, 0, 0),
	(NULL, 0, '2023-07-10 16:26:24', NULL, 1014, 46, 5, 54, 1, 0),
	(NULL, 0, '2023-07-10 16:26:24', NULL, 1015, 46, 5, 24, 2, 0),
	(NULL, 0, '2023-07-10 16:26:24', NULL, 1016, 46, 5, 34, 3, 0),
	(NULL, 0, '2023-07-10 16:26:24', NULL, 1017, 46, 5, 35, 4, 0),
	(NULL, 0, '2023-07-10 16:26:24', NULL, 1018, 46, 5, 20, 5, 0),
	(NULL, 0, '2023-07-10 16:26:19', NULL, 1007, 46, 4, 20, 4, 0),
	(NULL, 0, '2023-07-10 16:26:24', NULL, 1020, 46, 5, 32, 7, 0),
	(NULL, 0, '2023-07-10 16:26:24', NULL, 1021, 46, 5, 5, 8, 0),
	(NULL, 0, '2023-07-10 16:26:24', NULL, 1022, 46, 5, 25, 9, 0),
	(NULL, 0, '2023-07-10 16:26:24', NULL, 1023, 46, 5, 26, 10, 0),
	(NULL, 0, '2023-07-10 16:26:24', NULL, 1024, 46, 5, 57, 11, 0),
	(NULL, 0, '2023-07-10 16:26:24', NULL, 1025, 46, 5, 30, 12, 0),
	(NULL, 0, '2023-07-10 16:26:24', NULL, 1026, 46, 5, 36, 13, 0),
	(NULL, 0, '2023-07-10 16:26:24', NULL, 1027, 46, 5, 37, 14, 0),
	(NULL, 0, '2023-07-10 16:26:24', NULL, 1028, 46, 5, 40, 15, 0),
	(NULL, 0, '2023-07-10 16:26:24', NULL, 1029, 46, 5, 39, 16, 0),
	(NULL, 0, '2023-07-10 16:26:24', NULL, 1030, 46, 5, 58, 17, 0),
	(NULL, 0, '2023-07-10 16:26:24', NULL, 1031, 46, 5, 47, 18, 0),
	(NULL, 0, '2023-07-10 16:26:24', NULL, 1032, 46, 5, 49, 19, 0),
	(NULL, 0, '2023-07-10 16:26:24', NULL, 1033, 46, 5, 50, 20, 0),
	(NULL, 0, '2023-07-11 11:15:00', NULL, 1034, 46, 30, 73, 0, 0),
	(NULL, 0, '2023-07-11 11:15:00', NULL, 1035, 46, 30, 74, 1, 0),
	(NULL, 0, '2023-07-11 11:15:00', NULL, 1036, 46, 30, 75, 2, 0),
	(NULL, 0, '2023-07-11 11:15:00', NULL, 1037, 46, 30, 76, 3, 0),
	(NULL, 0, '2023-07-11 11:15:00', NULL, 1038, 46, 30, 77, 4, 0),
	(NULL, 0, '2023-07-11 11:15:00', NULL, 1039, 46, 30, 78, 5, 0),
	(NULL, 0, '2023-07-11 11:15:00', NULL, 1040, 46, 30, 47, 6, 0),
	(NULL, 0, '2023-07-11 11:15:00', NULL, 1041, 46, 30, 48, 7, 0),
	(NULL, 0, '2023-07-11 11:15:00', NULL, 1042, 46, 30, 51, 8, 0),
	(NULL, 0, '2023-07-11 11:15:00', NULL, 1043, 46, 30, 53, 9, 0),
	(NULL, 0, '2023-07-11 11:15:00', NULL, 1044, 46, 30, 22, 10, 0),
	(NULL, 0, '2023-07-11 11:15:00', NULL, 1045, 46, 30, 79, 11, 0),
	(NULL, 0, '2023-07-11 12:20:44', NULL, 1046, 46, 28, 71, 0, 0),
	(NULL, 0, '2023-07-11 12:20:44', NULL, 1047, 46, 28, 48, 1, 0),
	(NULL, 0, '2023-07-11 12:20:44', NULL, 1048, 46, 28, 47, 2, 0),
	(NULL, 0, '2023-07-11 12:20:44', NULL, 1049, 46, 28, 74, 3, 0),
	(NULL, 0, '2023-07-11 12:20:44', NULL, 1050, 46, 28, 75, 4, 0),
	(NULL, 0, '2023-07-11 12:20:44', NULL, 1051, 46, 28, 76, 5, 0),
	(NULL, 0, '2023-07-11 12:20:44', NULL, 1052, 46, 28, 77, 6, 0),
	(NULL, 0, '2023-07-11 12:20:44', NULL, 1053, 46, 28, 51, 7, 0),
	(NULL, 0, '2023-07-11 12:20:44', NULL, 1054, 46, 28, 53, 8, 0),
	(NULL, 0, '2023-07-11 12:20:44', NULL, 1055, 46, 28, 79, 9, 0),
	(NULL, 0, '2023-07-11 12:20:44', NULL, 1056, 46, 28, 99, 10, 0),
	(NULL, 0, '2023-07-10 16:26:19', NULL, 1006, 46, 4, 26, 3, 0),
	(NULL, 0, '2023-07-10 16:26:19', NULL, 1005, 46, 4, 25, 2, 0),
	(NULL, 0, '2023-07-10 16:26:19', NULL, 1004, 46, 4, 24, 1, 0),
	(NULL, 0, '2023-07-10 16:26:19', NULL, 1003, 46, 4, 23, 0, 0),
	(NULL, 0, '2023-07-10 16:26:24', NULL, 1019, 46, 5, 33, 6, 0);
/*!40000 ALTER TABLE `c_psa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_pso`
--

DROP TABLE IF EXISTS `c_pso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_pso` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `prv_id` int(11) DEFAULT NULL,
  `ptv_id` int(11) DEFAULT NULL,
  `type_id` int(11) DEFAULT NULL,
  `uid` int(11) DEFAULT NULL,
  `option` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `prv_id` (`prv_id`),
  KEY `ptv_id` (`ptv_id`),
  KEY `type_id` (`type_id`),
  KEY `ix_c_pso_uid` (`uid`),
  KEY `ix_c_pso_deleted` (`deleted`),
  CONSTRAINT `c_pso_ibfk_1` FOREIGN KEY (`prv_id`) REFERENCES `c_prv` (`id`),
  CONSTRAINT `c_pso_ibfk_2` FOREIGN KEY (`ptv_id`) REFERENCES `c_ptv` (`id`),
  CONSTRAINT `c_pso_ibfk_3` FOREIGN KEY (`type_id`) REFERENCES `c_ci_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `c_ptv`
--

DROP TABLE IF EXISTS `c_ptv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_ptv` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  `levels` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `type_id` (`type_id`),
  KEY `ix_c_preference_tree_views_uid` (`uid`),
  KEY `ix_c_preference_tree_views_deleted` (`deleted`),
  CONSTRAINT `c_ptv_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `c_ci_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_ptv`
--

LOCK TABLES `c_ptv` WRITE;
/*!40000 ALTER TABLE `c_ptv` DISABLE KEYS */;
INSERT INTO `c_ptv` VALUES (NULL, 0, '2022-10-17 17:24:02', '2023-01-10 14:33:55', 4, 1, 4, '[\"idc\", 35, 34]'),
	(NULL, 0, '2023-07-10 16:28:11', '2023-07-10 16:28:56', 32, 46, 4, '[35, 34]');
/*!40000 ALTER TABLE `c_ptv` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_records`
--

DROP TABLE IF EXISTS `c_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_records` (
  `created_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `origin` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ticket_id` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `reason` text COLLATE utf8_unicode_ci,
  `type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_c_records_created_at` (`created_at`),
  KEY `ix_c_records_type_id` (`type_id`),
  KEY `ix_c_records_uid` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_records`
--

LOCK TABLES `c_records` WRITE;
/*!40000 ALTER TABLE `c_records` DISABLE KEYS */;
INSERT INTO `c_records` VALUES ('2023-07-11 17:49:51',1,1,NULL,NULL,NULL,1),('2023-07-11 17:50:29',2,1,NULL,NULL,NULL,2),('2023-07-11 17:50:36',3,1,NULL,NULL,NULL,3),('2023-07-11 17:51:01',4,1,NULL,NULL,NULL,4),('2023-07-11 17:51:13',5,1,NULL,NULL,NULL,NULL),('2023-07-11 17:51:24',6,1,NULL,NULL,NULL,NULL),('2023-07-11 17:51:35',7,1,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `c_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_relation_histories`
--

DROP TABLE IF EXISTS `c_relation_histories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_relation_histories` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `operate_type` enum('0','1') COLLATE utf8_unicode_ci DEFAULT NULL,
  `record_id` int(11) NOT NULL,
  `first_ci_id` int(11) DEFAULT NULL,
  `second_ci_id` int(11) DEFAULT NULL,
  `relation_type_id` int(11) DEFAULT NULL,
  `relation_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `record_id` (`record_id`),
  KEY `relation_type_id` (`relation_type_id`),
  KEY `ix_c_relation_histories_deleted` (`deleted`),
  CONSTRAINT `c_relation_histories_ibfk_1` FOREIGN KEY (`record_id`) REFERENCES `c_records` (`id`),
  CONSTRAINT `c_relation_histories_ibfk_2` FOREIGN KEY (`relation_type_id`) REFERENCES `c_relation_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_relation_histories`
--

LOCK TABLES `c_relation_histories` WRITE;
/*!40000 ALTER TABLE `c_relation_histories` DISABLE KEYS */;
INSERT INTO `c_relation_histories` VALUES (NULL,0,'2023-07-11 17:51:13',NULL,1,'0',5,1,2,1,1),(NULL,0,'2023-07-11 17:51:24',NULL,2,'0',6,2,3,1,2),(NULL,0,'2023-07-11 17:51:35',NULL,3,'0',7,3,4,3,3);
/*!40000 ALTER TABLE `c_relation_histories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_relation_types`
--

DROP TABLE IF EXISTS `c_relation_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_relation_types` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(16) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_c_relation_types_name` (`name`),
  KEY `ix_c_relation_types_deleted` (`deleted`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_relation_types`
--

LOCK TABLES `c_relation_types` WRITE;
/*!40000 ALTER TABLE `c_relation_types` DISABLE KEYS */;
INSERT INTO `c_relation_types` VALUES (NULL,0,'2021-11-24 10:13:23','2022-12-14 19:25:44',1,'contain'),('2021-11-24 10:13:28',1,'2021-11-24 10:13:23','2021-11-24 10:13:28',2,'contain'),(NULL,0,'2021-11-24 10:13:39','2022-12-14 19:25:44',3,'deploy'),(NULL,0,'2021-11-24 10:13:48','2022-12-14 19:25:44',4,'install'),(NULL,0,'2021-11-24 10:13:53','2022-12-14 19:25:44',5,'connect');
/*!40000 ALTER TABLE `c_relation_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_sc`
--

DROP TABLE IF EXISTS `c_sc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_sc` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `option` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_c_sc_name` (`name`),
  KEY `ix_c_sc_deleted` (`deleted`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_sc`
--

LOCK TABLES `c_sc` WRITE;
/*!40000 ALTER TABLE `c_sc` DISABLE KEYS */;
INSERT INTO `c_sc` VALUES (NULL,0,'2022-12-08 19:56:27','2023-07-11 17:03:10',1,'ci_type_relation_layout','[{\"x\": 564, \"y\": 74, \"id\": \"2\"}, {\"x\": 558, \"y\": -59, \"id\": \"1\"}, {\"x\": 545, \"y\": 175, \"id\": \"3\"}, {\"x\": 690, \"y\": 357, \"id\": \"4\"}, {\"x\": 496, \"y\": 372, \"id\": \"5\"}, {\"x\": 245, \"y\": 317, \"id\": \"9\"}, {\"x\": 812, \"y\": 168, \"id\": \"6\"}, {\"x\": 730, \"y\": 451, \"id\": \"7\"}, {\"x\": 805, \"y\": 337, \"id\": \"8\"}]');
/*!40000 ALTER TABLE `c_sc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_value_datetime`
--

DROP TABLE IF EXISTS `c_value_datetime`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_value_datetime` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ci_id` int(11) NOT NULL,
  `attr_id` int(11) NOT NULL,
  `value` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ci_id` (`ci_id`),
  KEY `attr_id` (`attr_id`),
  KEY `ix_c_value_datetime_deleted` (`deleted`),
  CONSTRAINT `c_value_datetime_ibfk_1` FOREIGN KEY (`ci_id`) REFERENCES `c_cis` (`id`),
  CONSTRAINT `c_value_datetime_ibfk_2` FOREIGN KEY (`attr_id`) REFERENCES `c_attributes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_value_datetime`
--

LOCK TABLES `c_value_datetime` WRITE;
/*!40000 ALTER TABLE `c_value_datetime` DISABLE KEYS */;
/*!40000 ALTER TABLE `c_value_datetime` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_value_floats`
--

DROP TABLE IF EXISTS `c_value_floats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_value_floats` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ci_id` int(11) NOT NULL,
  `attr_id` int(11) NOT NULL,
  `value` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ci_id` (`ci_id`),
  KEY `attr_id` (`attr_id`),
  KEY `ix_c_value_floats_deleted` (`deleted`),
  CONSTRAINT `c_value_floats_ibfk_1` FOREIGN KEY (`ci_id`) REFERENCES `c_cis` (`id`),
  CONSTRAINT `c_value_floats_ibfk_2` FOREIGN KEY (`attr_id`) REFERENCES `c_attributes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_value_floats`
--

LOCK TABLES `c_value_floats` WRITE;
/*!40000 ALTER TABLE `c_value_floats` DISABLE KEYS */;
/*!40000 ALTER TABLE `c_value_floats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_value_index_datetime`
--

DROP TABLE IF EXISTS `c_value_index_datetime`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_value_index_datetime` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ci_id` int(11) NOT NULL,
  `attr_id` int(11) NOT NULL,
  `value` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ci_id` (`ci_id`),
  KEY `datetime_attr_value_index` (`attr_id`,`value`),
  KEY `ix_c_value_index_datetime_deleted` (`deleted`),
  CONSTRAINT `c_value_index_datetime_ibfk_1` FOREIGN KEY (`ci_id`) REFERENCES `c_cis` (`id`),
  CONSTRAINT `c_value_index_datetime_ibfk_2` FOREIGN KEY (`attr_id`) REFERENCES `c_attributes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_value_index_datetime`
--

LOCK TABLES `c_value_index_datetime` WRITE;
/*!40000 ALTER TABLE `c_value_index_datetime` DISABLE KEYS */;
/*!40000 ALTER TABLE `c_value_index_datetime` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_value_index_floats`
--

DROP TABLE IF EXISTS `c_value_index_floats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_value_index_floats` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ci_id` int(11) NOT NULL,
  `attr_id` int(11) NOT NULL,
  `value` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ci_id` (`ci_id`),
  KEY `float_attr_value_index` (`attr_id`,`value`),
  KEY `ix_c_value_index_floats_deleted` (`deleted`),
  CONSTRAINT `c_value_index_floats_ibfk_1` FOREIGN KEY (`ci_id`) REFERENCES `c_cis` (`id`),
  CONSTRAINT `c_value_index_floats_ibfk_2` FOREIGN KEY (`attr_id`) REFERENCES `c_attributes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_value_index_floats`
--

LOCK TABLES `c_value_index_floats` WRITE;
/*!40000 ALTER TABLE `c_value_index_floats` DISABLE KEYS */;
/*!40000 ALTER TABLE `c_value_index_floats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_value_index_integers`
--

DROP TABLE IF EXISTS `c_value_index_integers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_value_index_integers` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ci_id` int(11) NOT NULL,
  `attr_id` int(11) NOT NULL,
  `value` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ci_id` (`ci_id`),
  KEY `integer_attr_value_index` (`attr_id`,`value`),
  KEY `ix_c_value_index_integers_deleted` (`deleted`),
  CONSTRAINT `c_value_index_integers_ibfk_1` FOREIGN KEY (`ci_id`) REFERENCES `c_cis` (`id`),
  CONSTRAINT `c_value_index_integers_ibfk_2` FOREIGN KEY (`attr_id`) REFERENCES `c_attributes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_value_index_integers`
--

LOCK TABLES `c_value_index_integers` WRITE;
/*!40000 ALTER TABLE `c_value_index_integers` DISABLE KEYS */;
INSERT INTO `c_value_index_integers` VALUES (NULL,0,'2023-07-11 17:51:01',NULL,1,4,37,2);
/*!40000 ALTER TABLE `c_value_index_integers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_value_index_texts`
--

DROP TABLE IF EXISTS `c_value_index_texts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_value_index_texts` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ci_id` int(11) NOT NULL,
  `attr_id` int(11) NOT NULL,
  `value` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ci_id` (`ci_id`),
  KEY `ix_c_value_index_texts_deleted` (`deleted`),
  KEY `text_attr_value_index` (`attr_id`,`value`),
  CONSTRAINT `c_value_index_texts_ibfk_1` FOREIGN KEY (`ci_id`) REFERENCES `c_cis` (`id`),
  CONSTRAINT `c_value_index_texts_ibfk_2` FOREIGN KEY (`attr_id`) REFERENCES `c_attributes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_value_index_texts`
--

LOCK TABLES `c_value_index_texts` WRITE;
/*!40000 ALTER TABLE `c_value_index_texts` DISABLE KEYS */;
INSERT INTO `c_value_index_texts` (`deleted_at`, `deleted`, `created_at`, `updated_at`, `ci_id`, `attr_id`, `value`)
VALUES
	(NULL, 0, '2023-07-11 17:49:51', NULL, 1, 1, '事业部1'),
	(NULL, 0, '2023-07-11 17:50:29', NULL, 2, 2, '产品1'),
	(NULL, 0, '2023-07-11 17:50:36', NULL, 3, 3, '应用1'),
	(NULL, 0, '2023-07-11 17:51:01', NULL, 4, 25, '192.168.2.2'),
	(NULL, 0, '2023-07-11 17:51:01', NULL, 4, 4, 'xxxxxxx'),
	(NULL, 0, '2024-03-20 11:43:53', NULL, 4, 35, 'prod'),
	(NULL, 0, '2024-03-20 11:44:01', '2024-03-20 11:44:04', 4, 34, '在线'),
	(NULL, 0, '2024-03-20 11:44:12', NULL, 4, 47, '张江'),
	(NULL, 0, '2024-03-20 11:45:34', NULL, 4, 22, '张三'),
	(NULL, 0, '2024-03-20 11:45:34', NULL, 4, 20, '李四'),
	(NULL, 0, '2024-03-20 11:49:10', NULL, 1, 10, '王五');

/*!40000 ALTER TABLE `c_value_index_texts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_value_integers`
--

DROP TABLE IF EXISTS `c_value_integers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_value_integers` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ci_id` int(11) NOT NULL,
  `attr_id` int(11) NOT NULL,
  `value` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ci_id` (`ci_id`),
  KEY `attr_id` (`attr_id`),
  KEY `ix_c_value_integers_deleted` (`deleted`),
  CONSTRAINT `c_value_integers_ibfk_1` FOREIGN KEY (`ci_id`) REFERENCES `c_cis` (`id`),
  CONSTRAINT `c_value_integers_ibfk_2` FOREIGN KEY (`attr_id`) REFERENCES `c_attributes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_value_integers`
--

LOCK TABLES `c_value_integers` WRITE;
/*!40000 ALTER TABLE `c_value_integers` DISABLE KEYS */;
/*!40000 ALTER TABLE `c_value_integers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_value_json`
--

DROP TABLE IF EXISTS `c_value_json`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_value_json` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ci_id` int(11) NOT NULL,
  `attr_id` int(11) NOT NULL,
  `value` json NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ci_id` (`ci_id`),
  KEY `attr_id` (`attr_id`),
  KEY `ix_c_value_json_deleted` (`deleted`),
  CONSTRAINT `c_value_json_ibfk_1` FOREIGN KEY (`ci_id`) REFERENCES `c_cis` (`id`),
  CONSTRAINT `c_value_json_ibfk_2` FOREIGN KEY (`attr_id`) REFERENCES `c_attributes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_value_json`
--

LOCK TABLES `c_value_json` WRITE;
/*!40000 ALTER TABLE `c_value_json` DISABLE KEYS */;
/*!40000 ALTER TABLE `c_value_json` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_value_texts`
--

DROP TABLE IF EXISTS `c_value_texts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_value_texts` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ci_id` int(11) NOT NULL,
  `attr_id` int(11) NOT NULL,
  `value` text COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ci_id` (`ci_id`),
  KEY `attr_id` (`attr_id`),
  KEY `ix_c_value_texts_deleted` (`deleted`),
  CONSTRAINT `c_value_texts_ibfk_1` FOREIGN KEY (`ci_id`) REFERENCES `c_cis` (`id`),
  CONSTRAINT `c_value_texts_ibfk_2` FOREIGN KEY (`attr_id`) REFERENCES `c_attributes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_value_texts`
--

LOCK TABLES `c_value_texts` WRITE;
/*!40000 ALTER TABLE `c_value_texts` DISABLE KEYS */;
INSERT INTO `c_value_texts` VALUES (NULL,0,'2023-07-11 17:51:01',NULL,1,4,23,'物理机1');
/*!40000 ALTER TABLE `c_value_texts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `common_company_info_json`
--

DROP TABLE IF EXISTS `common_company_info_json`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `common_company_info_json` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `info` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_common_company_info_json_deleted` (`deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `common_company_info_json`
--

LOCK TABLES `common_company_info_json` WRITE;
/*!40000 ALTER TABLE `common_company_info_json` DISABLE KEYS */;
/*!40000 ALTER TABLE `common_company_info_json` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `common_department`
--

DROP TABLE IF EXISTS `common_department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `common_department` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `department_id` int(11) NOT NULL AUTO_INCREMENT,
  `department_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '部门名称',
  `department_director_id` int(11) DEFAULT NULL COMMENT '部门负责人ID',
  `department_parent_id` int(11) DEFAULT NULL COMMENT '上级部门ID',
  `sort_value` int(11) DEFAULT NULL COMMENT '排序值',
  `acl_rid` int(11) DEFAULT NULL COMMENT 'ACL中rid',
  PRIMARY KEY (`department_id`),
  KEY `ix_common_department_deleted` (`deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `common_department`
--

LOCK TABLES `common_department` WRITE;
/*!40000 ALTER TABLE `common_department` DISABLE KEYS */;
INSERT INTO `common_department` VALUES (NULL,0,'2023-07-11 16:28:21','2023-07-11 16:28:21',0,'全公司',0,-1,0,0);
/*!40000 ALTER TABLE `common_department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `common_employee`
--

DROP TABLE IF EXISTS `common_employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `common_employee` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `employee_id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '邮箱',
  `username` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '用户名',
  `nickname` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '姓名',
  `sex` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '性别',
  `position_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '职位名称',
  `mobile` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '电话号码',
  `avatar` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '头像',
  `direct_supervisor_id` int(11) DEFAULT NULL COMMENT '直接上级ID',
  `department_id` int(11) DEFAULT NULL COMMENT '部门ID',
  `acl_uid` int(11) DEFAULT NULL COMMENT 'ACL中uid',
  `acl_rid` int(11) DEFAULT NULL COMMENT 'ACL中rid',
  `acl_virtual_rid` int(11) DEFAULT NULL COMMENT 'ACL中虚拟角色rid',
  `last_login` timestamp NULL DEFAULT NULL COMMENT '上次登录时间',
  `block` int(11) DEFAULT NULL COMMENT '锁定状态',
  `notice_info` json DEFAULT NULL,
  PRIMARY KEY (`employee_id`),
  KEY `department_id` (`department_id`),
  KEY `ix_common_employee_deleted` (`deleted`),
  CONSTRAINT `common_employee_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `common_department` (`department_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `common_employee`
--

LOCK TABLES `common_employee` WRITE;
/*!40000 ALTER TABLE `common_employee` DISABLE KEYS */;
INSERT INTO `common_employee` VALUES (NULL,0,'2023-07-11 16:28:25',NULL,1,'demo@veops.cn','demo','demo','','','','',0,0,46,0,0,'2023-07-11 08:28:24',0, null),(NULL,0,'2023-07-11 16:34:08',NULL,2,'admin@one-ops.com','admin','admin','','','','',0,0,1,0,0,'2023-07-11 08:34:08',0, null);
/*!40000 ALTER TABLE `common_employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `common_employee_info`
--

DROP TABLE IF EXISTS `common_employee_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `common_employee_info` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `info` json DEFAULT NULL COMMENT '员工信息',
  `employee_id` int(11) DEFAULT NULL COMMENT '员工ID',
  PRIMARY KEY (`id`),
  KEY `employee_id` (`employee_id`),
  KEY `ix_common_employee_info_deleted` (`deleted`),
  CONSTRAINT `common_employee_info_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `common_employee` (`employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `common_employee_info`
--

LOCK TABLES `common_employee_info` WRITE;
/*!40000 ALTER TABLE `common_employee_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `common_employee_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `common_internal_message`
--

DROP TABLE IF EXISTS `common_internal_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `common_internal_message` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '标题',
  `content` text COLLATE utf8_unicode_ci COMMENT '内容',
  `path` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '跳转路径',
  `is_read` tinyint(1) DEFAULT NULL COMMENT '是否已读',
  `app_name` varchar(128) COLLATE utf8_unicode_ci NOT NULL COMMENT '应用名称',
  `category` varchar(128) COLLATE utf8_unicode_ci NOT NULL COMMENT '分类',
  `message_data` json DEFAULT NULL COMMENT '数据',
  `employee_id` int(11) DEFAULT NULL COMMENT 'ID',
  PRIMARY KEY (`id`),
  KEY `employee_id` (`employee_id`),
  KEY `ix_common_internal_message_deleted` (`deleted`),
  CONSTRAINT `common_internal_message_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `common_employee` (`employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `common_internal_message`
--

LOCK TABLES `common_internal_message` WRITE;
/*!40000 ALTER TABLE `common_internal_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `common_internal_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `nickname` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `department` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `catalog` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `email` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `mobile` varchar(14) COLLATE utf8_unicode_ci DEFAULT NULL,
  `password` varchar(80) COLLATE utf8_unicode_ci DEFAULT NULL,
  `key` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `secret` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `date_joined` datetime DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `block` tinyint(1) DEFAULT NULL,
  `has_logined` tinyint(1) DEFAULT NULL,
  `wx_id` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `employee_id` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `avatar` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `apps` json DEFAULT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `mobile` (`mobile`),
  KEY `ix_users_employee_id` (`employee_id`),
  KEY `ix_users_deleted` (`deleted`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (NULL,0,1,'admin','admin',NULL,NULL,'admin@one-ops.com',NULL,'e10adc3949ba59abbe56e057f20f883e','','',NULL,'2023-07-11 18:03:55',0,1,NULL,'0001',NULL,NULL),(NULL,0,2,'cmdb_agent','cmdb_agent',NULL,NULL,'cmdb_agent@one-ops.com',NULL,NULL,'ef086550acb543828d9930d15b21a037','U~83O&PT2Qxsd1$H9df2v#*FcsiG1l?n',NULL,NULL,0,NULL,NULL,'0002',NULL,NULL),(NULL,0,3,'worker','worker',NULL,NULL,'worker@one-ops.com',NULL,'b34cd51b4a6e2f96547e4aeb81566a83','0577dfa24e4547ad91bfb23b62951845','~0g7tkFG$@wdHKe*r2rYu2RC2v1?d8I5',NULL,NULL,0,NULL,NULL,'0003',NULL,NULL),(NULL,0,46,'demo','demo',NULL,NULL,'demo@veops.cn',NULL,'e10adc3949ba59abbe56e057f20f883e','0ec692fb318b47e4b739c241d56c12e7','JDcAc563I4L47ji2R?fah1dZ6KPb!Ty0','2023-07-10 08:19:01','2023-07-11 16:30:42',0,1,NULL,'0004',NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-11 18:04:17
