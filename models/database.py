import sqlite3  # Imports the sqlite3 module


class Database(object):
    def __init__(self, path):
        self.path = path  # Ask for the database file path whenever Database() is called
        self.connection = None  # Store database connection which is empty when initialized

    def connect_db(self):
        self.connection = sqlite3.connect(self.path)  # Make a connection with the database stored in path
        self.connection.row_factory = sqlite3.Row  # Save results in rows instead of a tuple
        cursor = self.connection.cursor()  # Cursor for executing SQL statements
        return cursor, self.connection  # Return the cursor and the db connection

    def close_connection(self):
        if self.connection:  # Check if there's an open connection
            self.connection.close()  # Close the connection
            self.connection = None  # Reset the connection attribute to None
