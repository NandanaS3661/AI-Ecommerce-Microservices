CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;
CREATE TABLE IF NOT EXISTS users(id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(100) NOT NULL,email VARCHAR(255) UNIQUE NOT NULL);
CREATE TABLE IF NOT EXISTS products(id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(200) NOT NULL,category VARCHAR(100),description TEXT,price DECIMAL(10,2),stock INT DEFAULT 0);
CREATE TABLE IF NOT EXISTS orders(id INT AUTO_INCREMENT PRIMARY KEY,user_id INT,product_id INT,quantity INT,status VARCHAR(30) DEFAULT 'PLACED',created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
INSERT IGNORE INTO products(id,name,category,description,price,stock) VALUES
(1,'Wireless Mouse','Electronics','Ergonomic wireless mouse',799,30),
(2,'Mechanical Keyboard','Electronics','RGB mechanical keyboard',2499,15),
(3,'Running Shoes','Fashion','Lightweight running shoes',1999,25),
(4,'Water Bottle','Home','Reusable stainless steel bottle',499,40),
(5,'Laptop Stand','Electronics','Adjustable aluminium laptop stand',1299,18);
