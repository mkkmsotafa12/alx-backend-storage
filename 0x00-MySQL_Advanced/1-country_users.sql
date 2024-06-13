-- A SQL script that creates a table users
DROP TABLE IF EXISTS users;

-- Create the users 'table' with specified attributes
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT,

    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),

    country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US',

    PRIMARY KEY (id),

    UNIQUE (email)
);