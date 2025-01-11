# test_analytics.py

"""
Unit tests for the HabitAnalytics class, verifying its behavior and calculations.

Author: Daniela de Sousa Silva
"""

import pytest
from analytics.analytics_module import HabitAnalytics
from models.habit_model import Habit

@pytest.fixture
def habit_analytics(temp_db):
    """
    Fixture for initializing HabitAnalytics with a temporary database.
    
    Returns:
        HabitAnalytics: Instance of analytics module connected to temp_db.
    """
    return HabitAnalytics(temp_db)

def test_calculate_streaks(temp_db, habit_analytics):
    """
    Test streak calculations for a daily habit.

    Verifies:
        - Longest streak is correctly calculated after one completion.
        - Longest break is zero when there are no gaps.
    """
    habit = Habit.create("Walk", "Daily", temp_db)
    habit.mark_as_complete(temp_db)
    
    streaks = habit_analytics.calculate_streaks(habit.habit_id, "Daily", habit.created_at)
    assert streaks['longest_streak'] == 1
    assert streaks['longest_break'] == 0

def test_completion_stats(temp_db, habit_analytics):
    """
    Test completion statistics calculation.

    Verifies:
        - Completions are correctly recorded.
        - Completion rate is accurate.
    """
    habit = Habit.create("Stretch", "Daily", temp_db)
    habit.mark_as_complete(temp_db)
    
    completions = temp_db.execute_query(
        "SELECT * FROM habit_completions WHERE habit_id = ?", (habit.habit_id,), fetch_all=True
    )
    assert len(completions) == 1  # One completion recorded

    stats = habit_analytics.get_completion_stats(habit.habit_id, "Daily", habit.created_at)
    assert stats["completion_rate"] == 100

def test_get_due_today(temp_db, habit_analytics):
    """
    Test retrieval of habits due today.

    Verifies:
        - Daily and weekly habits are correctly identified as due.
    """
    daily_habit = Habit.create("Water Plants", "Daily", temp_db)
    weekly_habit = Habit.create("Clean House", "Weekly", temp_db)
    
    daily_due, weekly_due = habit_analytics.get_due_today()
    assert daily_habit.task in [habit[1] for habit in daily_due]
    assert weekly_habit.task in [habit[1] for habit in weekly_due]