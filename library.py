# Library class:
# Uses methods to handle all actions and dictionaries
# Includes specific error raising

from library_database import LibraryDatabase
from datetime import datetime

class Library:
    def __init__(self):
        # self.books = {}
        # self.authors = {}
        # self.users = {}
        self.db = LibraryDatabase()
        self.db.connect()
        self.datetime = datetime.now()

    # User actions
    def add_user_to_library(self, user):
        # self.users[user.get_library_id()] = user
        name = user.get_user_name()
        library_id = user.get_library_id()
        # Check if user already exists
        check_query = "SELECT id, library_id, name FROM Users WHERE library_id = %s AND name = %s"
        check_result = self.db.fetch_one(check_query, (library_id, name))
        if check_result:
            user_id = check_result['id']
            raise ValueError(f"User already exists:\nUser ID: {user_id}\n- Library ID: {library_id}\n- Name: {name}")
        query = "INSERT INTO Users (library_id, name) VALUES (%s, %s)"
        self.db.execute_query(query, (library_id, name))

    def add_borrowed_book(self, library_id, title):
        # user = self.users[library_id]
        # book = self.books[title]
        # user.assign_borrowed_book(book.title)
        # book.mark_as_borrowed(True)
        available = False
        # Update book availability
        book_query = "UPDATE Books SET availability = %s WHERE title = %s"
        self.db.execute_query(book_query, (available, title))
        # Retrieve user ID and name based on library_id
        user_id_query = "SELECT id, name FROM Users WHERE library_id = %s"
        user_result = self.db.fetch_one(user_id_query, (library_id,))
        if user_result is None:
            raise LookupError(f"No user found with Library ID: {library_id}")
        user_id = user_result['id']
        user_name = user_result['name']
        # Retrieve book ID based on title
        book_id_query = "SELECT id FROM Books WHERE title = %s"
        book_result = self.db.fetch_one(book_id_query, (title,))
        if book_result is None:
            raise LookupError(f"No book found with title: {title}")
        book_id = book_result['id']
        # Insert record into BorrowedBooks table
        borrowed_books_query = "INSERT INTO BorrowedBooks (user_id, book_id, borrow_date) VALUES (%s, %s, %s)"
        self.db.execute_query(borrowed_books_query, (user_id, book_id, self.datetime))
        return f"\n* Book '{title}' checked out to {user_name} *"
    
    def remove_returned_book(self, library_id, title):
        # user = self.users[library_id]
        # book = self.books[title]
        # user.return_borrowed_book(book.title)
        # book.mark_as_borrowed(False)
        available = True
        # Update book availability
        book_query = "UPDATE Books SET availability = %s WHERE title = %s"
        self.db.execute_query(book_query, (available, title))
        # Retrieve user ID and name based on library_id
        user_id_query = "SELECT id, name FROM Users WHERE library_id = %s"
        user_result = self.db.fetch_one(user_id_query, (library_id,))
        if user_result is None:
            raise LookupError(f"No user found with Library ID: {library_id}")
        user_id = user_result['id']
        user_name = user_result['name']
        # Retrieve book ID based on title
        book_id_query = "SELECT id FROM Books WHERE title = %s"
        book_result = self.db.fetch_one(book_id_query, (title,))
        if book_result is None:
            raise LookupError(f"No book found with title: {title}")
        book_id = book_result['id']
        # Insert record into BorrowedBooks table
        borrowed_books_query = "UPDATE BorrowedBooks SET return_date = %s WHERE user_id = %s AND book_id = %s"
        self.db.execute_query(borrowed_books_query, (self.datetime, user_id, book_id))
        return f"\n* Book '{title}' returned by {user_name} *"
    
    # def _find_user_by_library_id(self, library_id):
    #     if library_id in self.users:
    #         self.users[library_id].format_user()
    #     else:
    #         raise LookupError(f"Cannot find user with Library ID: {library_id}")
        
    def find_user_by_library_id(self, library_id):
        user_query = "SELECT id, library_id, name FROM Users WHERE library_id = %s"
        row = self.db.fetch_one(user_query, (library_id,))
        if row:
            id = row['id']
            library_id = row['library_id']
            name = row['name']
            print(f"\nUser ID: {id}\n- Library ID: {library_id}\n- Name: {name}")
        else:
            raise LookupError(f"Cannot find user with Library ID: {library_id}")

    # def display_all_users(self):
    #     for library_id, user in self.users.items():
    #         name = user.get_user_name()
    #         print(f"\nLibrary ID: {library_id}\n- Name: {name}")

    def display_all_users(self):
        user_query = "SELECT id, library_id, name FROM Users"
        rows = self.db.fetch_all(user_query)
        if rows:
            for row in rows:
                id = row['id']
                library_id = row['library_id']
                name = row['name']
                print(f"User Id: {id}\n- Library ID: {library_id}\n- Name: {name}")
        else:
            raise LookupError("No users found in the database.")


    # Book actions
    def add_book_to_library(self, book):
        # Check if the book already exists
        check_query = "SELECT B.id, B.title, B.author_id, B.genre, A.id, A.name FROM Books B, Authors A WHERE B.title = %s AND A.name = %s AND B.author_id = A.id "
        check_results = self.db.fetch_one(check_query, (book.title, book.author))
        if check_results:
            title = check_results['B.title']
            author = check_results['A.name']
            raise ValueError(f"Database already contains book with title: {title} & author: {author}")
        # if book.title not in self.books:
        #     self.books[book.title] = book
        author_query = "SELECT id FROM Authors WHERE name = %s"
        author_results = self.db.fetch_one(author_query, (book.author,))
        author_id = author_results['id']
        query = "INSERT INTO Books (title, author_id, genre, publication_date) VALUES (%s, %s, %s, %s)"
        self.db.execute_query(query, (book.title, author_id, book.genre,  book.publication_date))

    # def find_book_by_title(self, book):
    #     if book in self.books:
    #         return self.books[book].format_book()
    #     raise LookupError(f"Cannot find book with title: {book}")
    
    def find_book_by_title(self, book):
        book_query = "SELECT B.id, B.title, B.author_id, B.genre, B.publication_date, B.availability, A.id, A.name FROM Books B, Authors A WHERE B.title = %s AND B.author_id = A.id"
        row = self.db.fetch_one(book_query, (book,))
        if row:
            id = row['B.id']
            title = row['B.title']
            author_id = row['B.author_id']
            author_name = row['A.name']
            genre = row['B.genre']
            publication_date = row['B.publication_date']
            availability = row['B.availability']
            print(f"\nBook ID: {id}\n- Title: {title}\n- Author Details: \n\t~ ID: {author_id}\n\t~ Name: {author_name}\n- Genre: {genre}\n- Publication Date: {publication_date}\n- Availability: {availability}")
        else:
            raise LookupError(f"Cannot find book with Title: {book}")
        
    # def display_all_books(self):
    #     for book in self.books.values():
    #         print(book.format_book())

    def display_all_books(self):
        book_query = "SELECT B.id, B.title, B.author_id, B.genre, B.publication_date, B.availability, A.id, A.name FROM Books B, Authors A WHERE B.author_id = A.id"
        rows = self.db.fetch_all(book_query)
        if rows:
            for row in rows:
                id = row['B.id']
                title = row['B.title']
                author_id = row['B.author_id']
                author_name = row['A.name']
                genre = row['B.genre']
                publication_date = row['B.publication_date']
                availability = row['B.availability']
                print(f"\nBook ID: {id}\n- Title: {title}\n- Author Details: \n\t~ ID: {author_id}\n\t~ Name: {author_name}\n- Genre: {genre}\n- Publication Date: {publication_date}\n- Availability: {availability}")
        else:
            raise LookupError("No books in database.")


    # Author actions
    def add_author_to_library(self, author):
        # self.authors[author.name] = author
        query = "INSERT INTO Authors (name, biography) VALUES (%s, %s)"
        self.db.execute_query(query, (author.name, author.biography))

    # def find_author(self, author_name):
    #     if author_name in self.authors:
    #         return self.authors[author_name].format_author()
    #     raise LookupError(f"Cannot find author: {author_name}")
    
    def find_author(self, author_name):
        author_query = "SELECT id, name, biography FROM Authors WHERE name = %s"
        row = self.db.fetch_one(author_query, (author_name,))
        if row:
            id = row['id']
            name = row['name']
            biography = row['biography']
            print(f"\nAuthor ID: {id}\n- Name: {name}\n- Biography: {biography}")
        else:
            raise LookupError(f"Cannot find author with name: {author_name}")

    # def display_all_authors(self):
    #     for author in self.authors.values():
    #         print(f"\n- Author: {author}")

    def display_all_authors(self):
        query = "SELECT id, name FROM Authors"
        rows = self.db.fetch_all(query)
        if rows:
            for row in rows:
                id = row['id']
                name = row['name']
                print(f"\nAuthor ID: {id}\n- Name: {name}")


    def close(self):
        self.db.disconnect()