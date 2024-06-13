-- A SQL script that create a table named `users`
DROP TABLE IF EXISTS users;
-- Create the users 'table' with specified attributes
CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255)
);