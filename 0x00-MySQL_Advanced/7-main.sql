-- Show initial state of tables
SELECT * FROM users;
SELECT * FROM corrections;

-- Compute average score for a specific user using the stored procedure
CALL ComputeAverageScoreForUser((SELECT id FROM users WHERE name = "Jeanne"));

-- Show updated state of tables
SELECT "--";
SELECT * FROM users;
