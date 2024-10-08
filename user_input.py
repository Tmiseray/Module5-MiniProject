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
        self.library = library
        self.validate_inputs = ValidateInputs()
        self.unique_id_generator = UniqueIdGenerator(self.library.db)
        

    # User Operations Inputs
    def add_user(self):
        library_id = self.unique_id_generator.generate_id()
        name = input("\nEnter new user's name: ")
        user = User(library_id, name)
        self.library.add_user_to_library(user)
    
    def view_user_details(self):
        library_id = input("\nEnter Library ID to view details: ")
        if not self.validate_inputs.check_library_id(library_id):
            formatted_id = self.validate_inputs.format_library_id(library_id)
            if not self.validate_inputs.check_library_id(formatted_id):
                raise ValueError("\n* Invalid Library ID. Please try again. *")
            else:
                print(f"\n* Retrieving Details for Library ID: {formatted_id}... *")
                results = self.library.find_user_details_by_library_id(formatted_id)
                return results
        else:
            print(f"\n* Retrieving Details for Library ID: {library_id}... *")
            results = self.library.find_user_details_by_library_id(library_id)
            return results
        

    # Book Operations Inputs
    def add_book(self):
        title = input("\nEnter title of new book: ")
        author = input("\nEnter author's name: ")
        genre = input("\nEnter book genre: ")
        publication_date = input("\nEnter publication date (YYYY): ")
        if not self.validate_inputs.validate_year(publication_date):
            raise ValueError(f"\n* '{publication_date}' is not a valid publication year. Please try again. *")
        else:
            book = Book(title, author, genre, publication_date)
            author_id = self.library.author_query(book.author)
            if not author_id:
                self.add_author(book.author)
                author_id = self.library.author_query(book.author)
            self.library.add_book_to_library(book, author_id)
        
    def borrow_book(self):
        book = input("\nEnter title of book to borrow: ")
        if self.library.query_book_and_availability(book):
            library_id = input("\nEnter your Library ID: ")
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
        library_id = input("\nEnter your Library ID: ")
        if not self.validate_inputs.check_library_id(library_id):
            formatted_id = self.validate_inputs.format_library_id(library_id)
            if not self.validate_inputs.check_library_id(formatted_id):
                raise ValueError("\n* Invalid Library ID. Please try again. *")
            else:     
                results = self.library.update_returned_book(formatted_id, book)
                return results
        else:
            results = self.library.update_returned_book(library_id, book)
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
        biography = input("\nEnter author's biography: ")
        author = Author(author_name, biography)
        self.library.add_author_to_library(author)

    def view_author_details(self):
        author = input("\nEnter author's name: ")
        print(f"\n* Retrieving Details for Author: {author}... *")
        details = self.library.find_author(author)
        return details
