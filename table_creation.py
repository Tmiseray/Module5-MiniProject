# MySQL Commands for initial creation of tables

create_books_table = """CREATE TABLE Books (
id INT AUTO_INCREMENT PRIMARY KEY,
title VARCHAR(255) NOT NULL,
author_id INT,
genre VARCHAR(100),
publication_date YEAR,
availability BOOLEAN DEFAULT 1,
FOREIGN KEY (author_id) REFERENCES authors(id)
)"""

create_authors_table = """CREATE TABLE Authors (
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(255) NOT NULL,
biography TEXT
)"""

create_users_table = """CREATE TABLE Users (
id INT AUTO_INCREMENT PRIMARY KEY,
library_id VARCHAR(13) NOT NULL UNIQUE,
name VARCHAR(255) NOT NULL
)"""

create_borrowed_books_table = """CREATE TABLE BorrowedBooks (
id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT,
book_id INT,
borrow_date DATE NOT NULL,
return_date DATE,
FOREIGN KEY (user_id) REFERENCES Users(id),
FOREIGN KEY (book_id) REFERENCES Books(id)
)"""

