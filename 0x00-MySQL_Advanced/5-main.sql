-- Show initial state of users table
SELECT * FROM users;

-- Update records to test the trigger
UPDATE users SET valid_email = 1 WHERE email = "bob@dylan.com";
UPDATE users SET email = "sylvie+new@dylan.com" WHERE email = "sylvie@dylan.com";
UPDATE users SET name = "Jannis" WHERE email = "jeanne@dylan.com";

-- Show updated state of users table
SELECT "--";
SELECT * FROM users;

-- Perform additional updates
UPDATE users SET email = "bob@dylan.com" WHERE email = "bob@dylan.com";

-- Show final state of users table
SELECT "--";
SELECT * FROM users;
