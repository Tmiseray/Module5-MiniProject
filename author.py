# Author Class:
# Uses methods to handle all author data

class Author:
    def __init__(self, author_name, biography):
        self.name = author_name
        self.biography = biography

    def get_author_name(self):
        return self.name
    
    def get_biography(self):
        return self.biography
