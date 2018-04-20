CREATE TABLE user
(
  id             INT PRIMARY KEY  AUTO_INCREMENT,
  username       VARCHAR(30) NOT NULL,
  password       VARCHAR(32) NOT NULL,
  lock_until     TIMESTAMP   NULL DEFAULT NULL,
  login_attempts TINYINT          DEFAULT 0
);
CREATE UNIQUE INDEX username_uindex
  ON user (username);