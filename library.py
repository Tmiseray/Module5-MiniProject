# Library class:
# Uses methods to handle all actions and dictionaries
# Includes specific error raising

from library_database import LibraryDatabase
import mysql.connector
from datetime import datetime

class Library:
    def __init__(self):
        self.db = LibraryDatabase()
        self.db.connect()
        self.datetime = datetime.now()

    # User actions
    def add_user_to_library(self, user):
        name = user.get_user_name()
        library_id = user.get_library_id()

        # Check if user already exists
        check_query = "SELECT id, library_id, name FROM Users WHERE library_id = %s AND name = %s"
        check_result = self.db.fetch_one(check_query, (library_id, name))

        if check_result:
            user_id = check_result['id']
            raise ValueError(f"\n* User already exists: *\nUser ID: {user_id}\n- Library ID: {library_id}\n- Name: {name}")
        try:
            query = "INSERT INTO Users (library_id, name) VALUES (%s, %s)"
            self.db.execute_query(query, (library_id, name))
            print(f"\n** New User Added: **\nLibrary ID: {library_id}\n- Name: {name}")
        except mysql.connector.Error as e:
            print(f"\n* Error inserting new user into database: {e} *")
            raise RuntimeError("\n* Failed to add user to library. *") from e


    def find_user_details_by_library_id(self, library_id):
        query = """
            SELECT
                U.id AS user_id,
                U.library_id,
                U.name,
                BB.id AS borrowed_book_id,
                BB.book_id,
                BB.borrow_date,
                BB.return_date,
                B.title AS book_title
            FROM
                Users U
            INNER JOIN
                BorrowedBooks BB ON U.id = BB.user_id
            INNER JOIN
                Books B ON BB.book_id = B.id
            WHERE
                U.library_id = %s AND BB.return_date IS NULL
        """
        results = self.db.fetch_all(query, (library_id,))

        if not results:
            raise LookupError(f"\n* Cannot find user with Library ID: {library_id} *")
        
        output = []
        user_info = None

        for row in results:
            if not user_info:
                # Extract & store user data only once
                user_id = row['user_id']
                lib_id = row['library_id']
                name = row['name']
                user_info = f"\nUser ID: {user_id}\n- Library ID: {lib_id}\n- Name: {name}\n ~ Borrowed Books: ~\n"
                output.append(user_info)

            # Extract and format book details
            borrowed_book_id = row['borrowed_book_id']
            book_id = row['book_id']
            borrow_date = row['borrow_date']
            return_date = row['return_date']
            book_title = row['book_title']

            book_info = (
                f" * Borrowed Book ID: {borrowed_book_id}\n"
                f"\t- Title: {book_title}\n"
                f"\t- Borrow Date: {borrow_date}\n"
                f"\t- Return Date: {'Currently borrowed (no return date)' if return_date is None else return_date}\n"
            )
            output.append(book_info)

        return "\n".join(output)


    def display_all_users(self):
        user_query = "SELECT id, library_id, name FROM Users"
        rows = self.db.fetch_all(user_query)
        if rows:
            for row in rows:
                id = row['id']
                library_id = row['library_id']
                name = row['name']
                print(f"\nUser Id: {id}\n- Library ID: {library_id}\n- Name: {name}")
        else:
            raise LookupError("\n* No users found in the database. *")


    # Book actions
    def add_book_to_library(self, book, author_id):
        # Check if the book already exists
        check_query = """
            SELECT B.id, B.title, A.id, A.name 
            FROM Books B
            INNER JOIN Authors A ON B.author_id = A.id
            WHERE B.title = %s AND A.name = %s
            """
        check_results = self.db.fetch_one(check_query, (book.title, book.author))
        if check_results:
            title = check_results['title']
            author = check_results['name']
            raise ValueError(f"\n* Database already contains book: *\n- Title: {title}\n- Author: {author}")
        try:
            query = """
                INSERT INTO Books (title, author_id, genre, publication_date)
                VALUES (%s, %s, %s, %s)
                """
            self.db.execute_query(query, (book.title, author_id, book.genre, book.publication_date))
            print(f"\n** New Book Added to Library: **\n* Title: {book.title}\n- Author: {book.author}\n- Genre: {book.genre}\n- Publication Date: {book.publication_date}")
        except mysql.connector.Error as e:
            print(f"\n* Error inserting book into database: {e} *")
            raise RuntimeError("\n* Failed to add book to library. *") from e


    def find_book_by_title(self, book_title):
        book_query = """
            SELECT
                B.id AS book_id, 
                B.title, 
                B.author_id, 
                B.genre, 
                B.publication_date, 
                B.availability, 
                A.id AS author_id, 
                A.name AS author_name
            FROM
                Books B
            INNER JOIN
                Authors A on B.author_id = A.id
            WHERE
                B.title = %s
        """
        row = self.db.fetch_one(book_query, (book_title,))

        if row:
            book_id = row['book_id']
            title = row['title']
            author_id = row['author_id']
            author_name = row['author_name']
            genre = row['genre']
            publication_date = row['publication_date']
            availability = row['availability']
            return f"\nBook ID: {book_id}\n- Title: {title}\n- Author Details: \n\t~ ID: {author_id}\n\t~ Name: {author_name}\n- Genre: {genre}\n- Publication Date: {publication_date}\n- Availability: {availability}"
        else:
            raise LookupError(f"\n* Cannot find book with Title: {book_title} *")
        
    def query_book_and_availability(self, book):
        query = "SELECT * FROM Books WHERE title = %s AND availability = %s"
        row = self.db.fetch_one(query, (book, True))
        if row:
            return True
        else:
            return False


    def display_all_books(self):
        book_query = """
            SELECT
                B.id AS book_id,
                B.title,
                B.author_id,
                B.genre,
                B.publication_date, 
                B.availability, 
                A.id AS author_id, 
                A.name AS name
            FROM 
                Books B
            INNER JOIN
                Authors A ON B.author_id = A.id
            ORDER BY
                B.id
        """
        rows = self.db.fetch_all(book_query)
        if rows:
            for row in rows:
                book_id = row['book_id']
                title = row['title']
                author_id = row['author_id']
                author_name = row['name']
                genre = row['genre']
                publication_date = row['publication_date']
                availability = row['availability']
                print(f"\nBook ID: {book_id}\n- Title: {title}\n- Author Details: \n\t~ ID: {author_id}\n\t~ Name: {author_name}\n- Genre: {genre}\n- Publication Date: {publication_date}\n- Availability: {availability}")
        else:
            raise LookupError("\n* No books in database. *")


    # Borrowed Books actions
    def add_borrowed_book(self, library_id, title):
        try:
            self.db.conn.start_transaction()

            # Check & update book availability
            update_availability_query = "UPDATE Books SET availability = %s WHERE title = %s"
            self.db.execute_query(update_availability_query, (False, title))

            # Retrieve user ID & name based on library_id
            user_query = "SELECT id, name FROM Users WHERE library_id = %s"
            user_result = self.db.fetch_one(user_query, (library_id,))
            if user_result is None:
                raise LookupError(f"\n* No user found with Library ID: {library_id} *")
            
            user_id = user_result['id']
            user_name = user_result['name']

            # Retrieve book ID based on title
            book_query = "SELECT id FROM Books WHERE title = %s"
            book_result = self.db.fetch_one(book_query, (title,))
            if book_result is None:
                raise LookupError(f"\n* No book found with title: {title} *")
            
            book_id = book_result['id']

            # Insert record into BorrowedBooks table
            insert_borrowed_query = """
                INSERT INTO BorrowedBooks (user_id, book_id, borrow_date) 
                VALUES (%s, %s, %s)
                """
            self.db.execute_query(insert_borrowed_query, (user_id, book_id, self.datetime))
            self.db.conn.commit()
            return f"\n* Book '{title}' checked out to {user_name} *"
        
        except mysql.connector.Error as e:
            self.db.conn.rollback()
            print(f"\n* Error: {e} *")
            raise RuntimeError("\n* An error occurred while adding the borrowed book. *") from e

    
    def update_returned_book(self, library_id, title):
        try:
            self.db.conn.start_transaction()

            # Check & update book availability
            update_availability_query = "UPDATE Books SET availability = %s WHERE title = %s"
            self.db.execute_query(update_availability_query, (True, title))

            # Retrieve user ID and name based on library_id
            user_query = "SELECT id, name FROM Users WHERE library_id = %s"
            user_result = self.db.fetch_one(user_query, (library_id,))
            if user_result is None:
                raise LookupError(f"\n* No user found with Library ID: {library_id} *")
            
            user_id = user_result['id']
            user_name = user_result['name']

            # Retrieve book ID based on title
            book_id_query = "SELECT id FROM Books WHERE title = %s"
            book_result = self.db.fetch_one(book_id_query, (title,))
            if book_result is None:
                raise LookupError(f"\n* No book found with title: {title} *")
            
            book_id = book_result['id']

            # Update record in BorrowedBooks table
            update_borrowed_query = "UPDATE BorrowedBooks SET return_date = %s WHERE user_id = %s AND book_id = %s"
            self.db.execute_query(update_borrowed_query, (self.datetime, user_id, book_id))
            self.db.conn.commit()
            return f"\n* Book '{title}' returned by {user_name} *"
        
        except mysql.connector.Error as e:
            self.db.conn.rollback()
            print(f"\n* Error: {e} *")
            raise RuntimeError("\n* An Error occurred while updating the borrowed book. *") from e


    # Author actions
    def add_author_to_library(self, author):
        try:
            query = "INSERT INTO Authors (name, biography) VALUES (%s, %s)"
            self.db.execute_query(query, (author.name, author.biography))
            print(f"\n** New Author Added: **\nAuthor: {author.name}\n- Biography: {author.biography}")
        except mysql.connector.Error as e:
            print(f"\n* Error inserting author into database: {e} *")
            raise RuntimeError("\n* Failed to add author to library. *") from e

    def author_query(self, author_name):
        query = "SELECT id FROM Authors WHERE name = %s"
        row = self.db.fetch_one(query, (author_name,))
        if row:
            author_id = row['id']
            return author_id
        else:
            return False


    def find_author(self, author_name):
        author_query = "SELECT id, name, biography FROM Authors WHERE name = %s"
        row = self.db.fetch_one(author_query, (author_name,))
        if row:
            id = row['id']
            name = row['name']
            biography = row['biography']
            return f"\nAuthor ID: {id}\n- Name: {name}\n- Biography: {biography}"
        else:
            raise LookupError(f"Cannot find author with name: {author_name}")


    def display_all_authors(self):
        query = "SELECT id, name FROM Authors"
        rows = self.db.fetch_all(query)
        if rows:
            for row in rows:
                id = row['id']
                name = row['name']
                print(f"\nAuthor ID: {id}\n- Name: {name}")
        else:
            raise LookupError("\n* No authors found in the database. *")


    def close(self):
        self.db.disconnect()