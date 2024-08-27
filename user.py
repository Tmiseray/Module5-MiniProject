# UniqueIdGenerator Class: 
# Uses methods to generate unique library IDs

# User Class:
# Uses methods to handle all user data including private attributes
 

class UniqueIdGenerator:
    def __init__(self, db):
        self.prefix = 'LID-'
        self.db = db

    def generate_id(self):
        # Query database to find highest existing Library ID
        max_id_query = "SELECT MAX(library_id) as max_id FROM Users"
        result = self.db.fetch_one(max_id_query)
        if result and result['max_id']:
            max_id = result['max_id']
            current_max_number = int(max_id.split('-')[1])
        else:
            current_max_number = 0
        # Increment current max ID number by 1
        new_id_number = current_max_number + 1
        return f"{self.prefix}{new_id_number}"


class User:
    def __init__(self, library_id, user_name):
        self._library_id = library_id
        self._name = user_name
        # self._borrowed_books = []

    def get_library_id(self):
        return self._library_id

    def get_user_name(self):
        return self._name
    
    def get_borrowed_books(self):
        return self._borrowed_books
