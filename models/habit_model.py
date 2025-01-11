# habit_model.py

"""
This module defines the `Habit` class, which represents a habit in the Habit Tracker application.

Features:
    - Encapsulates attributes like task, periodicity (daily/weekly), and creation timestamp.
    - Provides methods to create, load, delete, and mark habits as complete.
    - Supports querying all stored habits from the database.

Dependencies:
    - Relies on the database manager for executing SQL queries.
    - Uses Python's `datetime` for managing timestamps.

Author: Daniela de Sousa Silva
"""

import sqlite3
from datetime import datetime
import os
from database.database_manager import DatabaseManager

# Define the database path
db_manager = DatabaseManager()
db_name = db_manager.get_database_path()

class Habit:
    """
    Represents a habit with its associated properties and methods for database interaction.

    Attributes:
        habit_id (int): The unique identifier of the habit in the database.
        task (str): The description or name of the habit.
        periodicity (str): The frequency of the habit, either 'Daily' or 'Weekly'.
        created_at (datetime): The timestamp when the habit was created.
    """
    def __init__(self, habit_id=None, task=None, periodicity=None, created_at=None):
        """
        Initialize a Habit instance.

        Args:
            habit_id (int): The unique ID of the habit.
            task (str): The task name of the habit.
            periodicity (str): The frequency ('Daily' or 'Weekly') of the habit.
            created_at (datetime): The timestamp of creation, defaults to current time if not provided.
        """
        self.habit_id = habit_id
        self.task = task
        self.periodicity = periodicity
        self.created_at = created_at or datetime.now()

    @classmethod
    def create(cls, task, periodicity, db_manager):
        """
        Create and save a new habit in the database.

        Args:
            task (str): The task description of the habit.
            periodicity (str): The frequency ('Daily' or 'Weekly') of the habit.
            db_manager (DatabaseManager): An instance of DatabaseManager for database interactions.

        Returns:
            Habit: An instance of the Habit class with the newly created habit.

        Raises:
            ValueError: If the periodicity is invalid or a duplicate habit is found.
        """
        # Validate periodicity
        if periodicity not in ["Daily", "Weekly"]:
            raise ValueError("Invalid periodicity. Choose 'Daily' or 'Weekly'.")

        # Check for duplicate habits
        existing_habit = db_manager.execute_query(
            "SELECT id FROM habits WHERE task = ? AND periodicity = ?",
            (task, periodicity), fetch_one=True
        )
        if existing_habit:
            raise ValueError(f"Habit '{task}' with periodicity '{periodicity}' already exists.")

        created_at = datetime.now()  # Get the current timestamp

        # Insert the new habit into the database
        db_manager.execute_query(
            "INSERT INTO habits (task, periodicity, created_at) VALUES (?, ?, ?)",
            (task, periodicity, created_at)
        )

        # Retrieve the habit ID
        row = db_manager.execute_query(
            "SELECT id FROM habits WHERE task = ? AND periodicity = ? AND created_at = ?",
            (task, periodicity, created_at), fetch_one=True
        )
        if not row:
            raise ValueError("Failed to retrieve habit after creation.")

        habit_id = row[0]
        return cls(habit_id, task, periodicity, created_at)

    @classmethod
    def load(cls, habit_id, db_manager):
        """
        Load a habit by its ID.

        Args:
            habit_id (int): The unique ID of the habit to load.
            db_manager (DatabaseManager): An instance of DatabaseManager for database interactions.

        Returns:
            Habit: An instance of the Habit class representing the loaded habit.

        Raises:
            ValueError: If the habit ID is invalid or the habit is not found.
        """
        if not isinstance(habit_id, int):
            raise ValueError("Habit ID must be an integer.")

        row = db_manager.execute_query(
            "SELECT id, task, periodicity, created_at FROM habits WHERE id = ?",
            (habit_id,), fetch_one=True
        )
        if not row:
            raise ValueError(f"No habit found with ID {habit_id}")
        return cls(*row)

    def delete(self, db_manager):
        """
        Delete the habit from the database.

        Args:
            db_manager (DatabaseManager): An instance of DatabaseManager for database interactions.

        Raises:
            ValueError: If the habit does not exist in the database.
        """
        row = db_manager.execute_query(
            "SELECT id FROM habits WHERE id = ?", (self.habit_id,), fetch_one=True
        )
        if not row:
            raise ValueError(f"No habit found with ID {self.habit_id}")

        db_manager.execute_query("DELETE FROM habits WHERE id = ?", (self.habit_id,))

    def mark_as_complete(self, db_manager):
        """
        Mark the habit as complete by adding an entry to the habit_completions table.

        Args:
            db_manager (DatabaseManager): An instance of DatabaseManager for database interactions.
        """
        db_manager.execute_query(
            "INSERT INTO habit_completions (habit_id, completed_at) VALUES (?, ?)",
            (self.habit_id, datetime.now())
        )

    @staticmethod
    def list_all(db_manager):
        """
        Retrieve all habits from the database.

        Args:
            db_manager (DatabaseManager): An instance of DatabaseManager for database interactions.

        Returns:
            list: A list of tuples representing all habits in the database.
        """
        return db_manager.execute_query("SELECT * FROM habits", fetch_all=True)
