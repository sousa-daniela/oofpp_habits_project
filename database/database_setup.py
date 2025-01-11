# database_setup.py

"""
This script sets up the database schema for the Habit Tracker application.

Features:
    - Creates tables for storing habits and their completion records.
    - Ensures tables exist before inserting or querying data.

Execution:
    - This script can be run independently to set up the database.

Dependencies:
    - Uses SQLite for schema creation.
    - Handles paths dynamically to ensure compatibility.

Author: Daniela de Sousa Silva
"""

import sqlite3
import os

# Define the database path
db_name = DatabaseManager.get_database_path()

def setup_database():
    """
    Set up the database schema for the Habit Tracker application.

    This function creates two tables:
        1. `habits`: Stores details about each habit, including its ID, task, periodicity, and creation date.
        2. `habit_completions`: Logs when a habit is marked as complete, with a foreign key reference to the `habits` table.

    Tables are only created if they don't already exist.
    """
    conn = sqlite3.connect(db_name)  # Establish a connection to the SQLite database
    try:
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        cursor = conn.cursor()  # Create a cursor object for executing SQL commands

        # Create the `habits` table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            periodicity TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # Create the `habit_completions` table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS habit_completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            completed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
        )
        ''')

        conn.commit()  # Commit changes to the database
        print("Database setup completed successfully.")  # Log success
    except sqlite3.Error as e:
        print(f"Database setup failed: {e}")  # Log any database errors
    finally:
        conn.close()  # Ensure the connection is closed


# Run the setup function if this script is executed directly
if __name__ == "__main__":
    setup_database()
