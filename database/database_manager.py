# database_manager.py

"""
This module provides the `DatabaseManager` class, which handles database operations for the Habit Tracker application.

Features:
    - Simplifies execution of SQL queries and fetching results.
    - Supports both single and batch query execution.
    - Ensures database integrity with foreign key constraints.

Dependencies:
    - Relies on SQLite for database operations.
    - Handles paths dynamically to ensure portability.

Author: Daniela de Sousa Silva
"""

import sqlite3
import os

class DatabaseManager:
    """
    A utility class to handle database interactions for the Habit Tracker application.

    Attributes:
        db_path (str): The path to the SQLite database file.
    """
    def __init__(self, db_path=None):
        """
        Initialize the DatabaseManager with a specified database path.

        Args:
            db_path (str, optional): Path to the SQLite database file. Defaults to the `habit_tracker.db` in the current directory.
        """
        self.db_path = db_path or self.get_database_path()

    @staticmethod
    def get_database_path():
        """
        Constructs and returns the path to the database file.
        Ensures compatibility across operating systems.

        Returns:
            str: Absolute path to the database file.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
        return os.path.join(base_dir, 'habit_tracker.db')

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        """
        Execute a single SQL query with optional result fetching.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to bind to the query. Defaults to None.
            fetch_one (bool, optional): If True, fetch a single row from the query result. Defaults to False.
            fetch_all (bool, optional): If True, fetch all rows from the query result. Defaults to False.

        Returns:
            Any: The fetched result(s) if `fetch_one` or `fetch_all` is specified, otherwise None.

        Raises:
            sqlite3.Error: If an error occurs during query execution.
        """
        conn = sqlite3.connect(self.db_path)  # Establish a database connection
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        cursor = conn.cursor()  # Create a cursor for executing queries
        params = params or ()  # Default to an empty tuple if no parameters are provided

        try:
            cursor.execute(query, params)  # Execute the query
            result = None

            # Fetch results based on the flags
            if fetch_one:
                result = cursor.fetchone() or None  # Return a single row or None if no result
            elif fetch_all:
                result = cursor.fetchall() or []  # Return all rows or an empty list if no result

            conn.commit()  # Commit changes to the database
            return result
        except sqlite3.Error as e:
            print(f"Database error: {e}")  # Log the error
        finally:
            conn.close()  # Ensure the connection is closed

    def execute_many(self, query, params_list):
        """
        Execute a SQL query with multiple parameter sets.

        Args:
            query (str): The SQL query to execute.
            params_list (list of tuple): A list of parameter tuples to execute the query multiple times.

        Raises:
            sqlite3.Error: If an error occurs during query execution.
        """
        conn = sqlite3.connect(self.db_path)  # Establish a database connection
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        cursor = conn.cursor()  # Create a cursor for executing queries

        try:
            cursor.executemany(query, params_list)  # Execute the query with multiple parameter sets
            conn.commit()  # Commit changes to the database
        except sqlite3.Error as e:
            print(f"Database error: {e}")  # Log the error
        finally:
            conn.close()  # Ensure the connection is closed
