-- Show initial state of tables
SELECT * FROM projects;
SELECT * FROM corrections;

-- Add new corrections using the stored procedure
CALL AddBonus((SELECT id FROM users WHERE name = "Jeanne"), "Python is cool", 100);
CALL AddBonus((SELECT id FROM users WHERE name = "Jeanne"), "Bonus project", 100);
CALL AddBonus((SELECT id FROM users WHERE name = "Bob"), "Bonus project", 10);
CALL AddBonus((SELECT id FROM users WHERE name = "Jeanne"), "New bonus", 90);

-- Show updated state of tables
SELECT "--";
SELECT * FROM projects;
SELECT * FROM corrections;
