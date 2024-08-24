# UniqueIdGenerator Class: 
# Uses methods to generate unique library IDs

# User Class:
# Uses methods to handle all user data including private attributes

"TODO Add borrow_date using " # DATETIME.TODAY
"TODO Add return_date using " # DATETIME.TODAY    

class UniqueIdGenerator:
    def __init__(self):
        self.counter = 0
        self.prefix = 'LID-'

    def generate_id(self):
        self.counter += 1
        return f"{self.prefix}{self.counter}"


class User:
    def __init__(self, library_id, user_name):
        self._library_id = library_id
        self._name = user_name
        self._borrowed_books = []

    def get_library_id(self):
        return self._library_id

    def get_user_name(self):
        return self._name
    
    def get_borrowed_books(self):
        return self._borrowed_books
    
    def assign_borrowed_book(self, book):
        self._borrowed_books.append(book)

    def return_borrowed_book(self, book):
        for borrowed_book in self._borrowed_books:
            if book == borrowed_book:
                self._borrowed_books.remove(book)
                return

    def format_user(self):
        print(f"\nLibrary ID: {self._library_id}\n- Name: {self._name}\n- Borrowed Books: ")
        if self._borrowed_books is None:
            print("\t~ No borrowed books.")
        else:
            for book in self._borrowed_books:
                print(f"\t~ {book}")