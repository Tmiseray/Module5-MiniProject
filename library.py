# Library class:
# Uses methods to handle all actions and dictionaries
# Includes specific error raising

class Library:
    def __init__(self):
        self.books = {}
        self.authors = {}
        self.users = {}


    # User actions
    def add_user_to_library(self, user):
        self.users[user.get_library_id()] = user

    def add_borrowed_book(self, library_id, title):
        user = self.users[library_id]
        book = self.books[title]
        user.assign_borrowed_book(book.title)
        book.mark_as_borrowed(True)
        return f"\n* Book '{book.title}' checked out to {user.get_user_name()} *"
    
    def remove_returned_book(self, library_id, title):
        user = self.users[library_id]
        book = self.books[title]
        user.return_borrowed_book(book.title)
        book.mark_as_borrowed(False)
        return f"\n* Book '{book.title}' returned by {user.get_user_name()}. *"
    
    def _find_user_by_library_id(self, library_id):
        if library_id in self.users:
            self.users[library_id].format_user()
        else:
            raise LookupError(f"Cannot find user with Library ID: {library_id}")

    def display_all_users(self):
        for library_id, user in self.users.items():
            name = user.get_user_name()
            print(f"\nLibrary ID: {library_id}\n- Name: {name}")


    # Book actions
    def add_book_to_library(self, book):
        if book.title not in self.books:
            self.books[book.title] = book

    def find_book_by_title(self, book):
        if book in self.books:
            return self.books[book].format_book()
        raise LookupError(f"Cannot find book with title: {book}")
        
    def display_all_books(self):
        for book in self.books.values():
            print(book.format_book())


    # Author actions
    def add_author_to_library(self, author):
        self.authors[author.name] = author

    def find_author(self, author_name):
        if author_name in self.authors:
            return self.authors[author_name].format_author()
        raise LookupError(f"Cannot find author: {author_name}")

    def display_all_authors(self):
        for author in self.authors.values():
            print(f"\n- Author: {author}")