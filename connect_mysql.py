import mysql.connector
from mysql.connector import Error

def connect_database():
    """ Connect to the MySQL Database """
    # Database connection parameters
    db_name = "library_db"
    user = "root"
    password = "D!Vincenz022"
    host = "localhost"

    try:
        # Attempt to establish connection
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            password = password,
            host = host
        )

        # Check for successful connection
        print("Successfully connected to MySQL Database!")
        return conn
    
    except Error as e:
        # Connection error handling
        print(f"Error: {e}")
        return None