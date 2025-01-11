# test_habit.py

"""
This module tests the Habit model for functionality such as creation, retrieval, 
deletion, and marking a habit as complete.

Tests are executed using a temporary database to ensure isolation.

Author: Daniela de Sousa Silva
"""

import pytest
from models.habit_model import Habit

def test_create_habit(temp_db):
    """
    Test habit creation.
    
    Verifies:
        - A habit is created successfully.
        - The task and periodicity fields are correctly stored.
        - The habit ID is assigned.
    """
    habit = Habit.create("Drink Water", "Daily", temp_db)
    assert habit.task == "Drink Water"
    assert habit.periodicity == "Daily"
    assert habit.habit_id is not None

def test_load_habit(temp_db):
    """
    Test loading a habit by its ID.
    
    Verifies:
        - A habit is correctly retrieved from the database.
        - All fields match the originally created habit.
    """
    habit = Habit.create("Exercise", "Weekly", temp_db)
    loaded_habit = Habit.load(habit.habit_id, temp_db)
    assert loaded_habit.task == "Exercise"
    assert loaded_habit.periodicity == "Weekly"
    assert loaded_habit.habit_id == habit.habit_id

def test_delete_habit(temp_db):
    """
    Test deleting a habit.
    
    Verifies:
        - A habit is removed from the database.
        - Attempting to load the habit after deletion raises an error.
    """
    habit = Habit.create("Read Book", "Daily", temp_db)
    habit.delete(temp_db)
    with pytest.raises(ValueError):
        Habit.load(habit.habit_id, temp_db)

def test_mark_habit_as_complete(temp_db):
    """
    Test marking a habit as complete.
    
    Verifies:
        - A completion entry is added to the habit_completions table.
        - The entry is correctly associated with the habit ID.
    """
    habit = Habit.create("Meditate", "Daily", temp_db)
    habit.mark_as_complete(temp_db)
    completions = temp_db.execute_query(
        "SELECT * FROM habit_completions WHERE habit_id = ?", (habit.habit_id,), fetch_all=True
    )
    assert len(completions) == 1