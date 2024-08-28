# UserInterface Class:
# Uses methods to handle all user interface menus
# Includes specific error raising and exception handling

from library import Library
from user_input import UserInput

class UserInterface:
    welcome = "\n.~* Welcome to the Library Management System! *~."
    def __init__(self):
        self.library = Library()
        self.user_input = UserInput(self.library)

    def main_menu(self):
        while True:
            print("\n.~* MAIN MENU *~.")
            print("1. User Operations")
            print("2. Book Operations")
            print("3. Author Operations")
            print("4. Quit")
            choice = input("Enter your choice (1/2/3/4): ")
            try:
                if choice == '4':
                    print("\n.~* Thank you for using Library Management System! *~.\n\n\t* Exiting program... *")
                    self.library.db.disconnect()
                    break
                elif choice == '1':
                    self.user_operations()
                elif choice == '2':
                    self.book_operations()
                elif choice == '3':
                    self.author_operations()
                else:
                    print("\n* Invalid choice. Please enter the digit that corresponds with your selection. *")
            except ValueError as v:
                print(v)
            except TypeError:
                print("\n* An unexpected type error occurred. Please ensure you enter the digit that corresponds with your selection. *")
            except Exception as e:
                print(f"\n* An unexpected error occurred: *\n* {e} *")


    def user_operations(self):
        while True:
            print("\n.~* USER OPERATIONS *~.")
            print("1. Add a New User")
            print("2. View User Details")
            print("3. Display All Users")
            print("4. Return to Main Menu")
            choice = input("Enter your choice (1/2/3/4): ")
            try:
                if choice == '4':
                    print("\n* Returning to Main Menu... *")
                    self.main_menu()
                    break
                elif choice == '1':
                    results = self.user_input.add_user()
                    print(results)
                elif choice == '2':
                    results = self.user_input.view_user_details()
                    print(results)
                elif choice == '3':
                    print("\n** List of All Users **")
                    self.library.display_all_users()
                else:
                    print("\n* Invalid choice. Please enter the digit that corresponds with your selection. *")
            except ValueError as v:
                print(v)
            except LookupError as l:
                print(l)
            except RuntimeError as r:
                print(r)
            except TypeError:
                print("\n* An unexpected type error occurred. Please ensure you enter the digit that corresponds with your selection. *")
            except Exception as e:
                print(f"\n* An unexpected error occurred: *\n* {e} *")
            

    def book_operations(self):
        while True:
            print("\n.~* BOOK OPERATIONS *~.")
            print("1. Add a New Book")
            print("2. Borrow a Book")
            print("3. Return a Book")
            print("4. Search for a Book")
            print("5. Display All Books")
            print("6. Return to Main Menu")
            choice = input("Enter your choice (1/2/3/4/5/6): ")
            try:
                if choice == '6':
                    print("\n* Returning to Main Menu... *")
                    self.main_menu()
                    break
                elif choice == '1':
                    self.user_input.add_book()
                elif choice == '2':
                    results = self.user_input.borrow_book()
                    print(results)
                elif choice == '3':
                    results = self.user_input.return_book()
                    print(results)
                elif choice == '4':
                    results = self.user_input.search_for_book()
                    print(results)
                elif choice == '5':
                    print("\n** Full Library Collection: **")
                    self.library.display_all_books()
                else:
                    print("\n* Invalid choice. Please enter the digit that corresponds with your selection. *")
            except ValueError as v:
                print(v)
            except LookupError as l:
                print(l)
            except RuntimeError as r:
                print(r)
            except TypeError:
                print("\n* An unexpected type error occurred. Please ensure you enter the digit that corresponds with your selection. *")
            except Exception as e:
                print(f"\n* An unexpected error occurred: *\n* {e} *")


    def author_operations(self):
        while True:
            print("\n.~* AUTHOR OPERATIONS *~.")
            print("1. Add a New Author")
            print("2. View Author Details")
            print("3. Display All Authors")
            print("4. Return to Main Menu")
            choice = input("Enter your choice (1/2/3/4): ")
            try:
                if choice == '4':
                    print("\n* Returning to Main Menu... *")
                    self.main_menu()
                    break
                elif choice == '1':
                    self.user_input.add_author()
                elif choice == '2':
                    results = self.user_input.view_author_details()
                    print(results)
                elif choice == '3':
                    print("\n** All Authors in Library **")
                    self.library.display_all_authors()
                else:
                    print("\n* Invalid choice. Please enter the digit that corresponds with your selection. *")
            except ValueError as v:
                print(v)
            except LookupError as l:
                print(l)
            except RuntimeError as r:
                print(r)
            except TypeError:
                print("\n* An unexpected type error occurred. Please ensure you enter the digit that corresponds with your selection. *")
            except Exception as e:
                print(f"\n* An unexpected error occurred: *\n* {e} *")

if __name__ == "__main__":
    ui = UserInterface()
    print(ui.welcome)
    ui.main_menu()
