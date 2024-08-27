# Library Database Class

import mysql.connector
from mysql.connector import Error

class LibraryDatabase:
    def __init__(self):
        # Database connection parameters
        self.db_name = "library_db"
        self.user = "root"
        self.password = "D!Vincenz022"
        self.host = "localhost"
        self.conn = None

    def connect(self):
        """ Connect to the MySQL Database """
        try:
            # Attempt to establish connection
            self.conn = mysql.connector.connect(
                database = self.db_name,
                user = self.user,
                password = self.password,
                host = self.host,
                consume_results = True
            )

            # Check for successful connection
            if self.conn.is_connected():
                print(f"\nSuccessfully connected to MySQL Database: {self.db_name}!")
            else:
                print(f"\nFailed to connect to the database: {self.db_name}")
        
        except Error as e:
            # Connection error handling
            print(f"Error while connecting to MySQL: {e}")
            return None
        
    def disconnect(self):
        # Disconnect from MySQL Database
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print(f"Disconnected from Database: {self.db_name}")

    def execute_query(self, query, params=None):
        if not self.conn or not self.conn.is_connected():
            print("Not connected to any database.")
            return None
        
        cursor = self.conn.cursor(dictionary=True, buffered=True)
        try:
            cursor.execute(query, params)
            self.conn.commit()
            print("Query executed successfully!")
            return cursor
        except Error as e:
            print(f"Error: '{e}' occurred")
            return None
        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        # Fetch all results for a given query
        cursor = self.execute_query(query, params)
        if cursor:
            results = cursor.fetchall()
            cursor.close()
            return results
        return []
    
    def fetch_one(self, query, params=None):
        # Fetch single result for a query
        cursor = self.execute_query(query, params)
        if cursor:
            result = cursor.fetchone()
            cursor.close()
            return result
        return None