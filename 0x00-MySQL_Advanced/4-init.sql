-- Drop tables if they already exist
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS orders;

-- Create items table
CREATE TABLE IF NOT EXISTS items (
    name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL DEFAULT 10
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    item_name VARCHAR(255) NOT NULL,
    number INT NOT NULL
);

-- Insert initial data into items table
INSERT INTO items (name) VALUES ("apple"), ("pineapple"), ("pear");
