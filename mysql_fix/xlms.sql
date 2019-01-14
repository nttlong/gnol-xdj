CREATE TABLE courseware_authors (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NULL,
  `course_id` VARCHAR(100) NULL,
  `created_on` DATETIME NULL,
  PRIMARY KEY (`id`));

CREATE TABLE `courseware_orgs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `OrgCode` VARCHAR(45) NOT NULL,
  `OrgName` VARCHAR(200) NULL ,
  `OrgFName` VARCHAR(200) NULL,
  `OrgAddress` VARCHAR(200) NULL,
  `OrgWebSite` VARCHAR(2000) NULL,
  `OrgDescription` VARCHAR(2000) NULL,
  `RegisteredBy` INT,
  `RegisteredOn` DATETIME NULL,
  `CreatedOn` DATETIME NULL,
  `CreatedBy` VARCHAR(45) NULL,
  `ModifiedOn` DATETIME NULL,
  `ModifiedBy` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `OrgCode_UNIQUE` (`OrgCode` ASC)) DEFAULT CHARSET=utf8;
CREATE TABLE `courseware_subjects` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `SubjectCode` VARCHAR(45) NOT NULL,
  `SubjectName` VARCHAR(300) NOT NULL,
  `SubjectFName` VARCHAR(300) NULL,
  `SubjectDescription` VARCHAR(2000) NULL,
  `CreatedBy` VARCHAR(45) NULL,
  `CreatedOn` DATETIME NULL,
  `ModifiedBy` VARCHAR(45) NULL,
  `ModifiedOn` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `SubjectCode_UNIQUE` (`SubjectCode` ASC)) DEFAULT CHARSET=utf8;

CREATE TABLE `courseware_user_orgs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Org_id` INT NULL,
  `User_id` INT NULL,
  PRIMARY KEY (`id`)) DEFAULT CHARSET=utf8;

CREATE TABLE `libraries` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NULL,
  `name` VARCHAR(450) NULL,
  `description` VARCHAR(2000) NULL,
  `created_on` DATETIME NULL,
  `key` VARCHAR(450) NULL,
  PRIMARY KEY (`id`))
DEFAULT CHARACTER SET = utf8;

CREATE TABLE `courseware_chapters` (
  `course_id` VARCHAR(255) NULL,
  `display_name` VARCHAR(245) NULL,
  `chapter_id` VARCHAR(255) NULL,
  `created_on` DATETIME NULL,
  `creator_id` VARCHAR(150) NULL,
  `modified_on` DATETIME NULL,
  `modifier_id` VARCHAR(150) NULL,
  PRIMARY KEY (`chapter_id`))
DEFAULT CHARACTER SET = utf8;

CREATE TABLE `courseware_sequential` (
  `sequential_id` VARCHAR(255) NULL,
  `chapter_id` VARCHAR(255) NULL,
  `course_id` VARCHAR(255) NULL,
  `display_name` VARCHAR(245) NULL,
  `created_on` DATETIME NULL,
  `creator_id` VARCHAR(150) NULL,
  `modified_on` DATETIME NULL,
  `modifier_id` VARCHAR(150) NULL,
  PRIMARY KEY (`sequential_id`))
DEFAULT CHARACTER SET = utf8;


CREATE TABLE `courseware_vertical` (
	`vertical_id` VARCHAR(255) NULL,
  `sequential_id` VARCHAR(255) NULL,
  `chapter_id` VARCHAR(255) NULL,
  `course_id` VARCHAR(255) NULL,
  `display_name` VARCHAR(245) NULL,
  `created_on` DATETIME NULL,
  `creator_id` VARCHAR(150) NULL,
  `modified_on` DATETIME NULL,
  `modifier_id` VARCHAR(150) NULL,
  PRIMARY KEY (`vertical_id`))
DEFAULT CHARACTER SET = utf8;

CREATE TABLE `courseware_xblocks` (
  `xblock_id` VARCHAR(255) NULL,
  `xblock_type` VARCHAR(255) NULL,
  `vertical_id` VARCHAR(255) NULL,
  `course_id` VARCHAR(255) NULL,
  `display_name` VARCHAR(245) NULL,
  `created_on` DATETIME NULL,
  `creator_id` VARCHAR(150) NULL,
  `modified_on` DATETIME NULL,
  `modifier_id` VARCHAR(150) NULL,
  PRIMARY KEY (`xblock_id`))
DEFAULT CHARACTER SET = utf8;

CREATE TABLE `django_comment_common_discussionsidmapping` (
  `course_id` varchar(255) NOT NULL,
  `mapping` longtext NOT NULL,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;