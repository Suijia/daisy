CREATE TABLE `doc` (
  `docid` bigint(20) NOT NULL,
  `title` varchar(256) DEFAULT NULL,
  `snippet` text,
  `cover` varchar(512) DEFAULT NULL,
  `detailUrl` varchar(512) DEFAULT NULL,
  `author` varchar(64) DEFAULT NULL,
  `publishTime` timestamp NULL DEFAULT NULL,
  `publishStr` varchar(64) DEFAULT NULL,
  `createTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updateTime` timestamp NULL DEFAULT NULL,
  `source` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`docid`),
  UNIQUE KEY `docid_UNIQUE` (`docid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
