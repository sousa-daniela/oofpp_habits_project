# conftest.py

"""
This module defines shared fixtures for pytest, including a temporary database setup.
The temporary database is used to isolate tests and avoid affecting production data.

Author: Daniela de Sousa Silva
"""

import pytest
import os
import sqlite3
from database.database_manager import DatabaseManager

@pytest.fixture
def temp_db(tmpdir):
    """
    Creates a temporary SQLite database for testing.
    
    Returns:
        DatabaseManager: A manager instance for interacting with the temporary database.
    """
    db_path = tmpdir.join("test_habit_tracker.db")
    db_manager = DatabaseManager(str(db_path))
    
    # Create necessary tables
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                periodicity TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habit_completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER,
                completed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (habit_id) REFERENCES habits(id)
            )
        ''')
        conn.commit()
    
    yield db_manager
