# test_error_handling.py

"""
Unit tests for error handling in Habit and DatabaseManager modules.

Author: Daniela de Sousa Silva
"""

import pytest
from models.habit_model import Habit

def test_load_nonexistent_habit(temp_db):
    """
    Test loading a habit that does not exist in the database.

    Verifies:
        - Attempting to load a non-existent habit raises a ValueError.
    """
    with pytest.raises(ValueError, match="No habit found with ID"):
        Habit.load(9999, temp_db)

def test_create_duplicate_habit(temp_db):
    """
    Test handling of duplicate habit creation.

    Verifies:
        - Creating a habit with the same task and periodicity raises an exception.
    """
    Habit.create("Exercise", "Daily", temp_db)
    with pytest.raises(ValueError, match="already exists"):
        Habit.create("Exercise", "Daily", temp_db)

def test_delete_nonexistent_habit(temp_db):
    """
    Test deleting a habit that doesn't exist.

    Verifies:
        - Attempting to delete a non-existent habit raises a ValueError.
    """
    with pytest.raises(ValueError, match="No habit found with ID"):
        habit = Habit(habit_id=9999)
        habit.delete(temp_db)

def test_invalid_periodicity(temp_db):
    """
    Test creating a habit with an invalid periodicity value.

    Verifies:
        - Creating a habit with an invalid periodicity raises a ValueError.
    """
    with pytest.raises(ValueError, match="Invalid periodicity"):
        Habit.create("Read Book", "Monthly", temp_db)

def test_invalid_input_format(temp_db):
    """
    Test handling of non-integer habit ID inputs.

    Verifies:
        - Passing a non-integer habit ID raises a ValueError.
    """
    with pytest.raises(ValueError, match="Habit ID must be an integer"):
        habit_id = "invalid_id"
        Habit.load(habit_id, temp_db)