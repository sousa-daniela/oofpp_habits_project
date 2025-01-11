# analytics_module.py

"""
This module provides the `HabitAnalytics` class for computing metrics and insights on habit data.

Features:
    - Calculates streaks, completion rates, and breaks for habits.
    - Identifies habits due today or this week.
    - Retrieves habits completed within specific timeframes.
    - Supports both daily and weekly periodicity for habits.

Dependencies:
    - Relies on the database manager for querying completion data.
    - Uses Python's `datetime` for date and time calculations.
    - Formats outputs with `tabulate` for improved readability.

Author: Daniela de Sousa Silva
"""

from datetime import datetime, timedelta
from tabulate import tabulate

class HabitAnalytics:
    """
    A class to handle analytics for habits stored in the database.
    
    Provides functionality to compute streaks, breaks, completions, and other metrics
    for daily and weekly habits using the data stored in the database.
    """

    def __init__(self, db_manager):
        """
        Initialize the HabitAnalytics instance.

        Args:
            db_manager (DatabaseManager): An instance of DatabaseManager to interact with the database.
        """
        self.db_manager = db_manager

    @staticmethod
    def _parse_date(date_str):
        """
        Convert a date string or datetime object into a date object.

        Args:
            date_str (str | datetime): ISO-formatted date string (e.g., '2023-01-06') or a datetime object.

        Returns:
            datetime.date: Corresponding date object.
        """
        if isinstance(date_str, datetime):
            return date_str.date()  # Extract date from datetime
        elif isinstance(date_str, str):
            return datetime.fromisoformat(date_str).date()  # Parse string to datetime and extract date
        else:
            raise TypeError("Input must be a string or datetime object.")

    @staticmethod
    def _get_start_of_week(date):
        """
        Get the start of the week (Monday) for a given date.

        Args:
            date (datetime.date): The date for which the week's start is to be calculated.

        Returns:
            datetime.date: The start of the week (Monday) for the given date.
        """
        return date - timedelta(days=date.weekday())

    def get_stats_within_timeframe(self, habit_id, periodicity, created_at, days=None):
        """
        Calculate completion and break statistics for a habit within a specified timeframe.

        Args:
            habit_id (int): The ID of the habit.
            periodicity (str): The periodicity of the habit ('Daily' or 'Weekly').
            created_at (str): The creation date of the habit in ISO format.
            days (int, optional): The number of days for the timeframe. If None, calculate stats for the overall timeframe.

        Returns:
            dict: A dictionary containing completed intervals, broken intervals, and the completion rate.
        """
        today = datetime.now().date()
        created_date = self._parse_date(created_at)

        if days is not None:
            start_date = today - timedelta(days=days)
            created_date = max(created_date, start_date)

        # Calculate total intervals based on periodicity
        if periodicity == "Daily":
            total_intervals = (today - created_date).days + 1
        elif periodicity == "Weekly":
            total_intervals = ((today - created_date).days // 7) + 1
        else:
            raise ValueError("Invalid periodicity.")

        # Filter completions within the specified timeframe
        completions = [
            date for date in self.get_habit_completions(habit_id) if created_date <= date <= today
        ]
        completion_count = len(completions)
        broken_intervals = total_intervals - completion_count
        completion_rate = (completion_count / total_intervals * 100) if total_intervals > 0 else 0

        return {
            "completed_intervals": completion_count,
            "broken_intervals": max(0, broken_intervals),
            "completion_rate": round(completion_rate, 2),
        }

    def get_habit_completions(self, habit_id):
        """
        Retrieve all completion dates for a specific habit.

        Args:
            habit_id (int): The ID of the habit.

        Returns:
            list[datetime.date]: A list of completion dates for the habit.
        """
        completions = self.db_manager.execute_query(
            "SELECT completed_at FROM habit_completions WHERE habit_id = ?",
            (habit_id,), fetch_all=True
        )
        return [self._parse_date(c[0]) for c in completions]

    def calculate_streaks(self, habit_id, periodicity, created_at):
        """
        Calculate the longest streaks and breaks for a specific habit.

        Args:
            habit_id (int): The ID of the habit.
            periodicity (str): The periodicity of the habit ('Daily' or 'Weekly').
            created_at (str): The creation date of the habit in ISO format.

        Returns:
            dict: A dictionary containing:
                - "longest_streak": The length of the longest streak (int).
                - "longest_break": The length of the longest break (int).
        """
        # Fetch all completion dates for the habit
        completion_dates = self.get_habit_completions(habit_id)
        created_date = self._parse_date(created_at)

        # Return 0 for streaks and breaks if no completions exist
        if not completion_dates:
            return {"longest_streak": 0, "longest_break": 0}

        # Sort completion dates for sequential analysis
        completion_dates.sort()
        longest_streak = 0
        current_streak = 1
        longest_break = 0
        current_break = 0

        prev_date = created_date  # Start with the habit's creation date

        # Iterate over completion dates to calculate streaks and breaks
        for date in completion_dates:
            if periodicity == "Daily" and (date - prev_date).days == 1:
                current_streak += 1
            elif periodicity == "Weekly" and (date - prev_date).days <= 7:
                current_streak += 1
            else:
                # Update the longest streak and calculate the break
                longest_streak = max(longest_streak, current_streak)
                current_break = (
                    (date - prev_date).days - 1 if periodicity == "Daily"
                    else (date - prev_date).days // 7 - 1
                )
                longest_break = max(longest_break, current_break)
                current_streak = 1  # Reset the current streak
            prev_date = date

        # Final check to ensure the longest streak is updated
        longest_streak = max(longest_streak, current_streak)
        return {"longest_streak": longest_streak, "longest_break": longest_break}

    def calculate_current_streak_break(self, habit_id, periodicity, created_at):
        """
        Calculate the current streak or break count for a given habit.
        
        Args:
            habit_id (int): The ID of the habit.
            periodicity (str): The periodicity of the habit ('Daily' or 'Weekly').
            created_at (str): The creation date of the habit in ISO format.
            
        Returns:
            dict: A dictionary containing:
                - "current_streak": The length of the current streak (int).
                - "current_break": The length of the current break (int).
        """
        today = datetime.now().date()
        created_date = self._parse_date(created_at) # Convert the creation date to a date object

        # Fetch and sort completion dates for the habit
        completion_dates = self.get_habit_completions(habit_id)
        completion_dates.sort()

        # If no completions exist, calculate break from creation date
        if not completion_dates:
            return {"current_streak": 0, "current_break": (today - created_date).days}

         # Handle daily habits
        if periodicity == "Daily":
            last_date = completion_dates[-1] # Most recent completion date
            # Check if the habit was completed today
            if (today - last_date).days == 0:
                current_streak = 1
                # Count consecutive days in the streak
                for i in range(len(completion_dates) - 2, -1, -1):
                    if (completion_dates[i + 1] - completion_dates[i]).days == 1:
                        current_streak += 1
                    else:
                        break
                return {"current_streak": current_streak, "current_break": 0}
            else:
                # Calculate break as days since the last completion
                current_break = (today - last_date).days
                return {"current_streak": 0, "current_break": current_break}

        # Handle weekly habits
        elif periodicity == "Weekly":
            start_of_week = self._get_start_of_week(today)
            last_week = self._get_start_of_week(completion_dates[-1]) # Start of the last completion's week
            # Check if the habit was completed in the current week
            if start_of_week == last_week:
                current_streak = 1
                # Count consecutive weeks in the streak
                for i in range(len(completion_dates) - 2, -1, -1):
                    if (self._get_start_of_week(completion_dates[i + 1]) - self._get_start_of_week(completion_dates[i])).days == 7:
                        current_streak += 1
                    else:
                        break
                return {"current_streak": current_streak, "current_break": 0}
            else:
                # Calculate break as weeks since the last completion
                current_break = (start_of_week - last_week).days // 7
                return {"current_streak": 0, "current_break": current_break}

        # Default return for unsupported periodicity (should not occur)
        return {"current_streak": 0, "current_break": 0}

    def get_due_today(self):
        """
        Retrieve habits that are due today (for daily habits) and this week (for weekly habits),
        including their completion status.
        
        Returns:
           tuple: A tuple containing two lists:
              - daily_habits_with_status (list): Each entry is a tuple of the habit details with an added
                boolean indicating if it was completed today.
              - weekly_habits_with_status (list): Each entry is a tuple of the habit details with an added
                boolean indicating if it was completed this week.
        """
        # Get the current date and the start of the week
        today = datetime.now().date()
        start_of_week = self._get_start_of_week(today)

        # Fetch all daily habits from the database
        daily_habits = self.db_manager.execute_query(
            "SELECT id, task, periodicity, created_at FROM habits WHERE periodicity = 'Daily'", fetch_all=True
        )

        # Fetch all weekly habits from the database
        weekly_habits = self.db_manager.execute_query(
            "SELECT id, task, periodicity, created_at FROM habits WHERE periodicity = 'Weekly'", fetch_all=True
        )

        # Fetch IDs of habits that were completed today
        completed_today_ids = {
            row[0] for row in self.db_manager.execute_query(
                "SELECT habit_id FROM habit_completions WHERE DATE(completed_at) = DATE('now')", fetch_all=True
            )
        }

        # Fetch IDs of habits that were completed this week (starting from the start of the week)
        completed_this_week_ids = {
            row[0] for row in self.db_manager.execute_query(
                "SELECT habit_id FROM habit_completions WHERE completed_at >= ?", (start_of_week,), fetch_all=True
            )
        }

        # Add a boolean to daily habits indicating if they were completed today
        daily_habits_with_status = [
            habit + (habit[0] in completed_today_ids,) for habit in daily_habits
        ]

        # Add a boolean to weekly habits indicating if they were completed this week
        weekly_habits_with_status = [
            habit + (habit[0] in completed_this_week_ids,) for habit in weekly_habits
        ]

        return daily_habits_with_status, weekly_habits_with_status

    def get_completed_today_week(self):
        """
        Retrieve habits completed today and this week along with their last completion time.
        
        Returns:
           tuple: Two lists containing:
              - completed_daily (list): A list of daily habits completed today. Each entry includes:
                (habit_id, task, periodicity, last_completed_at).
              - completed_weekly (list): A list of weekly habits completed this week. Each entry includes:
                (habit_id, task, periodicity, last_completed_at).
        """
        # Get the current date and the start of the week
        today = datetime.now().date()
        start_of_week = self._get_start_of_week(today)

        # Fetch daily habits completed today, including their last completion timestamp
        completed_daily = self.db_manager.execute_query(
            """
            SELECT DISTINCT habits.id, habits.task, habits.periodicity, 
                        MAX(habit_completions.completed_at) AS last_completed_at
                        FROM habits
                        JOIN habit_completions ON habits.id = habit_completions.habit_id
                        WHERE habits.periodicity = 'Daily' AND DATE(habit_completions.completed_at) = DATE('now')
                        GROUP BY habits.id, habits.task, habits.periodicity
            """,
            fetch_all=True
        )

        # Fetch weekly habits completed this week, including their last completion timestamp
        completed_weekly = self.db_manager.execute_query(
                """
                SELECT DISTINCT habits.id, habits.task, habits.periodicity, 
                        MAX(habit_completions.completed_at) AS last_completed_at
                FROM habits
                JOIN habit_completions ON habits.id = habit_completions.habit_id 
                WHERE habits.periodicity = 'Weekly' AND habit_completions.completed_at >= ?
                GROUP BY habits.id, habits.task, habits.periodicity?
                """,
                (start_of_week,), fetch_all=True
        )

        return completed_daily, completed_weekly

    def get_completion_stats(self, habit_id, periodicity, created_at, timeframe="Overall"):
        """
        Calculate completion statistics for a habit over a given timeframe.
        
        Args:
           habit_id (int): The ID of the habit.
           periodicity (str): The periodicity of the habit ('Daily' or 'Weekly').
           created_at (str): The creation date of the habit in ISO format.
           timeframe (str): The timeframe for the statistics. Defaults to "Overall".
                         Options: "1 Week", "1 Month", "3 Months", "6 Months", "1 Year", "Overall".
                         
        Returns:
           dict: A dictionary containing:
              - completed_intervals (int): The number of completed intervals.
              - broken_intervals (int): The number of missed intervals.
              - completion_rate (float): The completion rate as a percentage.
        """
        # Get the current date
        today = datetime.now().date()
        created_date = self._parse_date(created_at)

        # Adjust the start date based on the specified timeframe
        if timeframe != "Overall":
            delta_days = {
                "1 Week": 7,
                "1 Month": 30,
                "3 Months": 90,
                "6 Months": 180,
                "1 Year": 365,
            }.get(timeframe, 0)
            created_date = max(created_date, today - timedelta(days=delta_days))

        # Calculate the total number of intervals based on periodicity
        if periodicity == "Daily":
            total_intervals = (today - created_date).days + 1
        elif periodicity == "Weekly":
            total_intervals = ((today - created_date).days // 7) + 1
        else:
            raise ValueError("Invalid periodicity.")

        # Fetch completion dates and filter them based on the timeframe
        completions = [c for c in self.get_habit_completions(habit_id) if created_date <= c <= today]
        completion_count = len(completions)

        # Calculate broken intervals and completion rate
        broken_intervals = total_intervals - completion_count
        completion_rate = (completion_count / total_intervals * 100) if total_intervals > 0 else 0

        return {
            "completed_intervals": completion_count,
            "broken_intervals": max(0, broken_intervals),
            "completion_rate": round(completion_rate, 2),
        }
