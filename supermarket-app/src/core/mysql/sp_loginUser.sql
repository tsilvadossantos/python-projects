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
