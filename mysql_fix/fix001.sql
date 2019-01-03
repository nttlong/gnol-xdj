SET @db_type ="date";
SET @dbname = DATABASE();
SET @tablename = "course_overviews_courseoverview";
SET @columnname = "certificate_available_date";
SET @preparedStatement = (SELECT IF(
  (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE
      (table_name = @tablename)
      AND (table_schema = @dbname)
      AND (column_name = @columnname)
  ) > 0,
  "SELECT 1",
  CONCAT("ALTER TABLE ", @tablename, " ADD ", @columnname, " ",@db_type,";")
));
PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;

CREATE TABLE 'entitlements_courseentitlement' (
  'id' int(11) NOT NULL AUTO_INCREMENT,
  'created' datetime(6) NOT NULL,
  'modified' datetime(6) NOT NULL,
  'uuid' char(32) NOT NULL,
  'course_uuid' char(32) NOT NULL,
  'expired_at' datetime(6) DEFAULT NULL,
  'mode' varchar(100) NOT NULL,
  'order_number' varchar(128) DEFAULT NULL,
  'enrollment_course_run_id' int(11) DEFAULT NULL,
  'user_id' int(11) NOT NULL,
  '_policy_id' int(11) DEFAULT NULL,
  'refund_locked' tinyint(1) NOT NULL,
  PRIMARY KEY ('id'),
  UNIQUE KEY 'entitlements_courseentitlement_uuid_a690dd005d0695b_uniq' ('uuid'),
  KEY 'entitlements_courseentit_user_id_a8df050144d72f8_fk_auth_user_id' ('user_id'),
  KEY 'fda6bce9129c5afc395658f36b9d444e' ('enrollment_course_run_id'),
  KEY 'entitlements_courseentitlement_36cddc86' ('_policy_id'),
  CONSTRAINT 'D2cebc0610e28b9b3a821c839e2fe01c' FOREIGN KEY ('_policy_id') REFERENCES 'entitlements_courseentitlementpolicy' ('id'),
  CONSTRAINT 'entitlements_courseentitlement_user_id_a518a225_fk' FOREIGN KEY ('user_id') REFERENCES 'auth_user' ('id'),
  CONSTRAINT 'fda6bce9129c5afc395658f36b9d444e' FOREIGN KEY ('enrollment_course_run_id') REFERENCES 'student_courseenrollment' ('id')
) ENGINE=InnoDB DEFAULT CHARSET=utf8;