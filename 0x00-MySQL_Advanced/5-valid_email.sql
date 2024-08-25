-- Set the delimiter for creating the trigger
DELIMITER $$

-- Create the trigger
CREATE TRIGGER reset_valid_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    -- Check if the email has been changed
    IF OLD.email <> NEW.email THEN
        -- Reset valid_email if email has been changed
        SET NEW.valid_email = 0;
    END IF;
END$$

-- Reset the delimiter to default
DELIMITER ;
