# ValidateInputs Class:
# Uses methods to validate library IDs and publication dates
# Includes:
    # REGEX patterns
    # DateTime module

# UserInput Class:
# Uses methods to handle all user inputs
# Includes specific error raising

from book import Book
from user import User, UniqueIdGenerator
from author import Author
import re
import datetime

class ValidateInputs:
    def __init__(self):
        self.id_pattern = r"^(LID\-)\d+$"
        self.letters = r"[a-zA-Z]+"
        self.numbers = r"[0-9]+"
        self.year = datetime.datetime.now().year

    def check_library_id(self, library_id):
        if re.match(self.id_pattern, library_id):
            return True
        else:
            return False
        
    def format_library_id(self, library_id):
        letters = "".join(re.findall(self.letters, library_id))
        numbers = "".join(re.findall(self.numbers, library_id))
        letters = letters.upper()
        formatted_id = letters + '-' + numbers
        return formatted_id
    
    def validate_year(self, publication_date):
        if int(publication_date) <= self.year:
            return True
        else:
            return False
        

class UserInput:
    def __init__(self, library):
        self.validate_inputs = ValidateInputs()
        self.unique_id_generator = UniqueIdGenerator()
        self.library = library


     # User Operations Inputs
    def add_user(self):
        library_id = self.unique_id_generator.generate_id()
        name = input("\nEnter new user's name: ")
        user = User(library_id, name)
        self.library.add_user_to_library(user)
        return f"\n** New User Added: **\nLibrary ID: {library_id}\n- Name: {name}"
    
    def view_user_details(self):
        library_id = input("\nEnter Library ID to view details: ")
        if not self.validate_inputs.check_library_id(library_id):
            formatted_id = self.validate_inputs.format_library_id(library_id)
            if not self.validate_inputs.check_library_id(formatted_id):
                raise ValueError("\n* Invalid Library ID. Please try again. *")
            else:
                print(f"\n* Retrieving Details for Library ID: {formatted_id}... *")
                results = self.library._find_user_by_library_id(formatted_id)
                return results
        else:
            print(f"\n* Retrieving Details for Library ID: {library_id}... *")
            results = self.library._find_user_by_library_id(library_id)
            return results
        

    # Book Operations Inputs
    def add_book(self):
        title = input("\nEnter title of new book: ")
        author = input("Enter author's name: ")
        genre = input("Enter book genre: ")
        publication_date = input("Enter publication date (YYYY): ")
        if not self.validate_inputs.validate_year(publication_date):
            raise ValueError(f"* '{publication_date}' is not a valid publication year. Please try again. *")
        else:
            book = Book(title, author, genre, publication_date)
            self.library.add_book_to_library(book)
            print(f"\n** New Book Added to Library: **")
            print(f"* Title: {book.title}\n- Author: {book.author}\n- Genre: {book.genre}\n- Publication Date: {book.publication_date}")
            if author not in self.library.authors:
                return self.add_author(author)
        
    def borrow_book(self):
        book = input("\nEnter title of book to borrow: ")
        if book in self.library.books and self.library.books[book].get_availability() == "Available":
                library_id = input("Enter your Library ID: ")
                if not self.validate_inputs.check_library_id(library_id):
                    formatted_id = self.validate_inputs.format_library_id(library_id)
                    if not self.validate_inputs.check_library_id(formatted_id):
                        raise ValueError("\n* Invalid Library ID. Please try again. *")
                    else:
                        results = self.library.add_borrowed_book(formatted_id, book)
                        return results
                else:
                    results = self.library.add_borrowed_book(library_id, book)
                    return results
        raise LookupError("\n* Book not available or not found. *")
        
    def return_book(self):
        book = input("\nEnter title of book to return: ")
        library_id = input("Enter your Library ID: ")
        if not self.validate_inputs.check_library_id(library_id):
            formatted_id = self.validate_inputs.format_library_id(library_id)
            if not self.validate_inputs.check_library_id(formatted_id):
                raise ValueError("\n* Invalid Library ID. Please try again. *")
            else:     
                results = self.library.remove_returned_book(formatted_id, book)
                return results
        else:
            results = self.library.remove_returned_book(library_id, book)
            return results

    def search_for_book(self):
        book = input("\nEnter the book title to search for: ")
        print(f"\n* Searching for {book} in Library... *")
        results = self.library.find_book_by_title(book)
        return results
    

    # Author Operations Inputs
    def add_author(self, author_name=None):
        if author_name is None:
            author_name = input("\nEnter author's name: ")
        biography = input("Enter author's biography: ")
        author = Author(author_name, biography)
        self.library.add_author_to_library(author)
        print(f"\n** New Author Added: **\nAuthor: {author.name}\n- Biography: {author.biography}")

    def view_author_details(self):
        author = input("Enter author's name: ")
        print(f"\n* Retrieving Details for Author: {author}... *")
        details = self.library.find_author(author)
        return details
