-- Set the delimiter for creating the procedure
DELIMITER $$

-- Create the stored procedure
CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE avg_score FLOAT;

    -- Compute the average score for the given user
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE user_id = user_id;

    -- Update the user's average_score with the computed value
    UPDATE users
    SET average_score = COALESCE(avg_score, 0)
    WHERE id = user_id;
END$$

-- Reset the delimiter to default
DELIMITER ;
