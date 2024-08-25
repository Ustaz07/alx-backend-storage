-- Set the delimiter for creating the procedure
DELIMITER $$

-- Create the stored procedure
CREATE PROCEDURE AddBonus(
    IN user_id INT,
    IN project_name VARCHAR(255),
    IN score INT
)
BEGIN
    DECLARE project_id INT;

    -- Check if the project exists and get its ID
    SELECT id INTO project_id
    FROM projects
    WHERE name = project_name;

    -- If the project does not exist, insert it
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;

    -- Insert or update the correction
    INSERT INTO corrections (user_id, project_id, score)
    VALUES (user_id, project_id, score)
    ON DUPLICATE KEY UPDATE score = VALUES(score);
END$$

-- Reset the delimiter to default
DELIMITER ;
