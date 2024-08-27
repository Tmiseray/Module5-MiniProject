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
                print(f"\n.~* Successfully connected to MySQL Database: {self.db_name}! *~.")
            else:
                print(f"\n* Failed to connect to the database: {self.db_name} *")
        
        except Error as e:
            # Connection error handling
            print(f"\n* Error occurred while connecting to MySQL: {e} *")
            return None
        
    def disconnect(self):
        # Disconnect from MySQL Database
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print(f"\n.~* Disconnected from Database: {self.db_name} *~.")

    def execute_query(self, query, params=None):
        if not self.conn or not self.conn.is_connected():
            print("\n* Not connected to any database. *")
            return None
        
        cursor = self.conn.cursor(dictionary=True, buffered=True)
        try:
            cursor.execute(query, params)
            self.conn.commit()
            return cursor
        except Error as e:
            print(f"\n* Error executing query: '{e}' *")
            return None
        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        # Fetch all results for a given query
        cursor = None
        try:
            cursor = self.execute_query(query, params)
            if cursor:
                return cursor.fetchall()
            else:
                return []
        except Error as e:
            print(f"\n* Error fetching data: '{e}' *")
            return []
        finally:
            if cursor:
                cursor.close()
                
    def fetch_one(self, query, params=None):
        # Fetch single result for a query or None if no rows
        cursor = None
        try:
            cursor = self.execute_query(query, params)
            if cursor:
                return cursor.fetchone()
            else:
                return None
        except Error as e:
            print(f"\n* Error fetching data: {e} *")
            return None
        finally:
            if cursor:
                cursor.close()