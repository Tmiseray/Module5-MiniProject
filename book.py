# Book Class:
# Uses methods to handle all book data

class Book:
    def __init__(self, title, author, genre, publication_date):
        self.title = title
        self.author = author
        self.genre = genre
        self.publication_date = publication_date
        self.availability = True
    
    def get_title(self):
        return self.title

    def get_author(self):
        return self.author
    
    def get_genre(self):
        return self.genre
    
    def get_publication_date(self):
        return self.publication_date

    def get_availability(self):
        return self.availability
    
    # def mark_as_borrowed(self, is_borrowed):
    #     if is_borrowed:
    #         self.availability = "Borrowed"
            
    #     else:
    #         self.availability = "Available"        

    # def format_book(self):
    #     return f"\nTitle: {self.title}\n- Author: {self.author}\n- Genre: {self.genre}\n- Publication Date: {self.publication_date}\n- Availability: {self.availability}"