CREATE DATABASE IF NOT EXISTS supermarket;

USE supermarket;

CREATE TABLE IF NOT EXISTS `supermarket`.`tbl_user` (
  `user_id` BIGINT UNIQUE AUTO_INCREMENT,
  `user_name` VARCHAR(45),
  `user_username` VARCHAR(45) UNIQUE,
  `user_password` VARCHAR(100),
  PRIMARY KEY (`user_id`));

 DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(20),
    IN p_username VARCHAR(20),
    IN p_password VARCHAR(100)
)
BEGIN
    if ( select exists (select 1 from tbl_user where user_username = p_username) ) THEN

        select 'Username Exists !!';

    ELSE

        insert into tbl_user
        (
            user_name,
            user_username,
            user_password
        )
        values
        (
            p_name,
            p_username,
            p_password
        );

    END IF;
END//
DELIMITER ;


DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_LoginUser`(
    IN p_username VARCHAR(100),
    IN p_password VARCHAR(100)
)
BEGIN

    if ( select exists (select 1 from tbl_user where user_username = p_username and user_password = p_password) ) THEN

        select 'User found';

    END IF;
    
END//
DELIMITER ;

