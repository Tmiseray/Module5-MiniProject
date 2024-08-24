# MySQL Commands for initial creation of tables

create_books_table = """CREATE TABLE books (
id INT AUTO_INCREMENT PRIMARY KEY,
title VARCHAR(255) NOT NULL,
author_id INT,
publication_date YEAR,
availability BOOLEAN DEFAULT 1,
FOREIGN KEY (author_id) REFERENCES authors(id)
)"""

create_authors_table = """CREATE TABLE authors (
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(255) NOT NULL,
biography TEXT
)"""

create_users_table = """CREATE TABLE users (
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(255) NOT NULL,
library_id VARCHAR(13) NOT NULL UNIQUE
)"""

create_borrowed_books_table = """CREATE TABLE borrowed_books (
id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT,
book_id INT,
borrow_date DATE NOT NULL.
return_date DATE,
FOREIGN KEY (user_id) REFERENCES users(id),
FOREIGN KEY (book_id) REFERENCES books(id)
)"""

