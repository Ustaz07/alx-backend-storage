-- Show current state of items and orders tables
SELECT * FROM items;
SELECT * FROM orders;

-- Insert orders into the orders table
INSERT INTO orders (item_name, number) VALUES ('apple', 1);
INSERT INTO orders (item_name, number) VALUES ('apple', 3);
INSERT INTO orders (item_name, number) VALUES ('pear', 2);

-- Show updated state of items and orders tables
SELECT "--";
SELECT * FROM items;
SELECT * FROM orders;
