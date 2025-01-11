# app.py

"""
This module serves as the main entry point for the Habit Tracker application.

Features:
    - Allows users to create and manage daily and weekly habits.
    - Enables marking habits as complete or deleting them.
    - Provides analytics on habits, including streaks, completion rates, and struggling habits.
    - Displays habits categorized as daily or weekly with interactive menus.

Dependencies:
    - Integrates with the database manager for persistent storage.
    - Uses the habit model for habit data representation.
    - Leverages the analytics module for data processing and metrics computation.

Author: Daniela de Sousa Silva
"""

from database.database_manager import DatabaseManager
from models.habit_model import Habit
from analytics.analytics_module import HabitAnalytics
from datetime import datetime, timedelta
from tabulate import tabulate

# Initialize database and analytics modules
db_manager = DatabaseManager()  # Database manager for storing and retrieving habit data.
analytics = HabitAnalytics(db_manager)  # Analytics module for processing habit metrics and insights.

# Helper Functions

def get_menu_choice(prompt, valid_choices):
    """
    Prompts the user to select a valid choice from a list of options.

    Args:
        prompt (str): The prompt message displayed to the user.
        valid_choices (set): A set of valid input options.

    Returns:
        str: The validated choice entered by the user.
    """
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print(f"Invalid choice. Please select from {', '.join(valid_choices)}.")

def get_non_empty_input(prompt):
    """
    Prompts the user until a non-empty input is provided.

    Args:
        prompt (str): The prompt message displayed to the user.

    Returns:
        str: The non-empty input provided by the user.
    """
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        print("Input cannot be empty. Please try again.")

def prompt_main_menu_or_exit():
    """
    Provides the user with the option to return to the main menu or exit the application.
    If the user types 'exit', the program terminates.
    """
    next_action = input("\nPress Enter to return to the main menu or type 'exit' to leave the app: ").strip().lower()
    if next_action == "exit":
        print("Exiting the Habit Tracker. Goodbye!")
        exit()

def prompt_analytics_menu_or_exit():
    """
    Provides the user with the option to return to the analytics menu or exit the application.
    If the user types 'exit', the program terminates.
    """
    next_action = input("\nPress Enter to return to the analytics menu or type 'exit' to leave the app: ").strip().lower()
    if next_action == "exit":
        print("Exiting the Habit Tracker. Goodbye!")
        exit()

# Analytics Functions

def view_longest_streaks_and_breaks(habits):
    """
    Displays the longest streaks and breaks for all habits in separate tables for daily and weekly habits.

    Args:
        habits (list): A list of all habits retrieved from the database. Each habit is a tuple
                       containing (id, task, periodicity, created_at).

    Behavior:
        - Separates habits into daily and weekly categories.
        - Calculates the longest streak and break for each habit using the analytics module.
        - Displays the results in tabular format for each category.
    """
    # Split habits into daily and weekly categories
    daily_habits = [habit for habit in habits if habit[2] == "Daily"]
    weekly_habits = [habit for habit in habits if habit[2] == "Weekly"]

    print("\n--- Longest Streaks and Breaks ---")

    # Display data for daily habits
    if daily_habits:
        daily_data = [
            [
                habit[1],  # Task name
                analytics.calculate_streaks(habit[0], habit[2], habit[3])['longest_streak'],  # Longest streak
                analytics.calculate_streaks(habit[0], habit[2], habit[3])['longest_break']  # Longest break
            ]
            for habit in daily_habits
        ]
        print("\nDaily Habits:")
        print(tabulate(daily_data, headers=["Task", "Longest Streak", "Longest Break"]))

    # Display data for weekly habits
    if weekly_habits:
        weekly_data = [
            [
                habit[1],  # Task name
                analytics.calculate_streaks(habit[0], habit[2], habit[3])['longest_streak'],  # Longest streak
                analytics.calculate_streaks(habit[0], habit[2], habit[3])['longest_break']  # Longest break
            ]
            for habit in weekly_habits
        ]
        print("\nWeekly Habits:")
        print(tabulate(weekly_data, headers=["Task", "Longest Streak", "Longest Break"]))

    # Prompt the user for the next action
    prompt_analytics_menu_or_exit()

def view_struggling_habits(habits):
    """
    Displays habits with a completion rate below 50% in separate tables for daily and weekly habits.

    Args:
        habits (list): A list of all habits retrieved from the database. Each habit is a tuple
                       containing (id, task, periodicity, created_at).

    Behavior:
        - Separates habits into daily and weekly categories.
        - Identifies habits with a completion rate below 50% using the analytics module.
        - Displays the results in tabular format for each category.
    """
    # Split habits into daily and weekly categories
    daily_habits = [habit for habit in habits if habit[2] == "Daily"]
    weekly_habits = [habit for habit in habits if habit[2] == "Weekly"]

    print("\n--- Struggling Habits ---")

    # Display data for struggling daily habits
    if daily_habits:
        daily_data = [
            [
                habit[1],  # Task name
                analytics.get_completion_stats(habit[0], habit[2], habit[3])['completion_rate']  # Completion rate
            ]
            for habit in daily_habits
            if analytics.get_completion_stats(habit[0], habit[2], habit[3])['completion_rate'] < 50
        ]
        if daily_data:
            print("\nDaily Habits:")
            print(tabulate(daily_data, headers=["Task", "Completion Rate (%)"]))

    # Display data for struggling weekly habits
    if weekly_habits:
        weekly_data = [
            [
                habit[1],  # Task name
                analytics.get_completion_stats(habit[0], habit[2], habit[3])['completion_rate']  # Completion rate
            ]
            for habit in weekly_habits
            if analytics.get_completion_stats(habit[0], habit[2], habit[3])['completion_rate'] < 50
        ]
        if weekly_data:
            print("\nWeekly Habits:")
            print(tabulate(weekly_data, headers=["Task", "Completion Rate (%)"]))

    # Prompt the user for the next action
    prompt_analytics_menu_or_exit()

def view_habits_due():
    """
    Displays a list of habits that are due today (for daily habits) or this week (for weekly habits).

    Behavior:
        - Retrieves habits marked as "due" using the `get_due_today` method from the analytics module.
        - Separates habits into daily and weekly categories.
        - Indicates the completion status (Completed or Pending) for each habit.
        - Displays results in tabular format.
        - Prompts the user for the next action after displaying the results.
    """
    # Fetch habits due today and this week
    daily_habits, weekly_habits = analytics.get_due_today()

    print("\n--- Habits Due Today/This Week ---")

    # Display daily habits due today
    if daily_habits:
        print("\nDaily Habits Due Today:")
        print(tabulate(
            [
                [habit[0], habit[1], "Completed" if habit[4] else "Pending"]  # ID, Task, Status
                for habit in daily_habits
            ],
            headers=["ID", "Task", "Status"]
        ))
    else:
        print("\nNo daily habits due today.")

    # Display weekly habits due this week
    if weekly_habits:
        print("\nWeekly Habits Due This Week:")
        print(tabulate(
            [
                [habit[0], habit[1], "Completed" if habit[4] else "Pending"]  # ID, Task, Status
                for habit in weekly_habits
            ],
            headers=["ID", "Task", "Status"]
        ))
    else:
        print("\nNo weekly habits due this week.")

    # Prompt the user for the next action
    prompt_analytics_menu_or_exit()


def view_completed_habits():
    """
    Displays a list of habits completed today or this week, including the timestamp of their last completion.

    Behavior:
        - Retrieves completed habits using the `get_completed_today_week` method from the analytics module.
        - Separates habits into daily and weekly categories.
        - Displays the "Last Completed At" timestamp for each habit in the format "DD.MM.YYYY at HH:MM".
        - Results are shown in tabular format.
        - Prompts the user for the next action after displaying the results.
    """
    # Fetch completed habits for today and this week
    completed_daily, completed_weekly = analytics.get_completed_today_week()

    print("\n--- Habits Completed Today/This Week ---")

    # Display daily habits completed today
    if completed_daily:
        print("\nDaily Habits Completed Today:")
        print(tabulate(
            [
                [habit[0], habit[1], datetime.fromisoformat(habit[3]).strftime("%d.%m.%Y at %H:%M")]  # ID, Task, Last Completed At
                for habit in completed_daily
            ],
            headers=["ID", "Task", "Last Completed At"]
        ))
    else:
        print("\nNo daily habits completed today.")

    # Display weekly habits completed this week
    if completed_weekly:
        print("\nWeekly Habits Completed This Week:")
        print(tabulate(
            [
                [habit[0], habit[1], datetime.fromisoformat(habit[3]).strftime("%d.%m.%Y at %H:%M")]  # ID, Task, Last Completed At
                for habit in completed_weekly
            ],
            headers=["ID", "Task", "Last Completed At"]
        ))
    else:
        print("\nNo weekly habits completed this week.")

    # Prompt the user for the next action
    prompt_analytics_menu_or_exit()

def view_completion_and_break_counts(habits):
    """
    Displays completion and break counts for all habits within a chosen timeframe.

    Steps:
        - Prompts the user to select a timeframe (e.g., past week, past month, etc.).
        - Calculates statistics for daily and weekly habits within the specified timeframe.
        - Displays the results in tabulated form, categorized by habit type (daily/weekly).
        - Allows the user to return to the analytics menu or exit the app.
    """
    print("\n--- Completion and Break Counts ---")
    print("Choose a timeframe:")
    print("1. Past Week")
    print("2. Past 1 Month")
    print("3. Past 3 Months")
    print("4. Past 6 Months")
    print("5. Past Year")
    print("6. Overall")

    # Prompt the user to select a timeframe
    timeframe_choice = None
    while timeframe_choice is None:
        choice = input("Select an option (1-6): ").strip()
        if choice == "1":
            days = 7
            timeframe_choice = "Past Week"
        elif choice == "2":
            days = 30
            timeframe_choice = "Past 1 Month"
        elif choice == "3":
            days = 90
            timeframe_choice = "Past 3 Months"
        elif choice == "4":
            days = 180
            timeframe_choice = "Past 6 Months"
        elif choice == "5":
            days = 365
            timeframe_choice = "Past Year"
        elif choice == "6":
            days = None  # Overall
            timeframe_choice = "Overall"
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

    print(f"\nTimeframe: {timeframe_choice}")

    # Separate habits by periodicity
    daily_habits = [habit for habit in habits if habit[2] == "Daily"]
    weekly_habits = [habit for habit in habits if habit[2] == "Weekly"]

    # Display daily habits
    if daily_habits:
        daily_data = [
            [habit[1], stats["completed_intervals"], stats["broken_intervals"], stats["completion_rate"]]
            for habit in daily_habits if (stats := analytics.get_stats_within_timeframe(habit[0], habit[2], habit[3], days))
        ]
        print("\nDaily Habits:")
        print(tabulate(daily_data, headers=["Task", "Completed", "Broken", "Completion Rate (%)"]))

    # Display weekly habits
    if weekly_habits:
        weekly_data = [
            [habit[1], stats["completed_intervals"], stats["broken_intervals"], stats["completion_rate"]]
            for habit in weekly_habits if (stats := analytics.get_stats_within_timeframe(habit[0], habit[2], habit[3], days))
        ]
        print("\nWeekly Habits:")
        print(tabulate(weekly_data, headers=["Task", "Completed", "Broken", "Completion Rate (%)"]))

    # Prompt the user for the next action
    prompt_analytics_menu_or_exit()

def view_current_streaks(habits):
    """
    Displays the current streaks and breaks for all habits in tabular format.

    Behavior:
        - Separates habits into daily and weekly categories.
        - Calculates the current streak and current break for each habit.
        - Displays the results in separate tables for daily and weekly habits.
        - Prompts the user to return to the analytics menu or exit after displaying the results.

    Parameters:
        habits (list): List of habits retrieved from the database. Each habit is a tuple containing:
            - habit[0]: ID of the habit.
            - habit[1]: Name of the habit/task.
            - habit[2]: Periodicity ('Daily' or 'Weekly').
            - habit[3]: Date the habit was created.

    Returns:
        None
    """
    # Filter daily and weekly habits from the list
    daily_habits = [habit for habit in habits if habit[2] == "Daily"]
    weekly_habits = [habit for habit in habits if habit[2] == "Weekly"]

    print("\n--- Current Streaks and Breaks ---")

    # Display current streaks and breaks for daily habits
    if daily_habits:
        daily_data = [
            [habit[1], 
             analytics.calculate_current_streak_break(habit[0], habit[2], habit[3])['current_streak'],
             analytics.calculate_current_streak_break(habit[0], habit[2], habit[3])['current_break']]
            for habit in daily_habits
        ]
        print("\nDaily Habits:")
        print(tabulate(daily_data, headers=["Task", "Current Streak", "Current Break"]))

    # Display current streaks and breaks for weekly habits
    if weekly_habits:
        weekly_data = [
            [habit[1], 
             analytics.calculate_current_streak_break(habit[0], habit[2], habit[3])['current_streak'],
             analytics.calculate_current_streak_break(habit[0], habit[2], habit[3])['current_break']]
            for habit in weekly_habits
        ]
        print("\nWeekly Habits:")
        print(tabulate(weekly_data, headers=["Task", "Current Streak", "Current Break"]))

    # Prompt the user for the next action
    prompt_analytics_menu_or_exit()

def display_analytics_menu():
    """
    Displays the analytics menu and handles user input for various analytical options.

    Behavior:
        - Lists available analytics options for the user to choose from.
        - Invokes the appropriate function based on the user's choice.
        - If no habits exist in the database, prompts the user to create a habit first.
        - Allows the user to return to the main menu after exploring the analytics.

    Returns:
        None
    """
    # Fetch all habits from the database
    habits = Habit.list_all(db_manager)
    if not habits:
        print("\nNo habits found. Please create a habit first.")
        return

    # Loop for the analytics menu until the user chooses to return to the main menu
    while True:
        print("\n--- Analytics Menu ---")
        print("1. View Longest Streaks and Breaks")
        print("2. View Struggling Habits")
        print("3. View Habits Due Today/This Week")
        print("4. View Completed Habits Today/This Week")
        print("5. View Completion and Break Counts")
        print("6. View Current Streaks and Breaks")
        print("7. Return to Main Menu")

        # Prompt the user for a menu choice
        choice = input("Select an option (1-7): ").strip()
        if choice == "1":
            view_longest_streaks_and_breaks(habits)
        elif choice == "2":
            view_struggling_habits(habits)
        elif choice == "3":
            view_habits_due()
        elif choice == "4":
            view_completed_habits()
        elif choice == "5":
            view_completion_and_break_counts(habits)
        elif choice == "6":
            view_current_streaks(habits)
        elif choice == "7":
            print("Returning to the main menu...")
            break
        else:
            # Handle invalid input
            print("Invalid choice. Please enter a number between 1 and 7.")
            
def display_all_habits():
    """
    Displays all habits stored in the database.

    Behavior:
        - Fetches all habits from the database.
        - Separates habits into daily and weekly categories.
        - Displays the habits in tabular format using `tabulate`, showing:
            - ID: Unique identifier for the habit.
            - Task: Name of the habit/task.
            - Periodicity: Whether the habit is 'Daily' or 'Weekly'.
            - Created At: The timestamp when the habit was created, formatted as 'DD.MM.YYYY at HH:MM'.
        - If no habits are found, prompts the user to create a habit.

    Returns:
        bool: 
            - True if habits exist and are displayed successfully.
            - False if no habits are found.
    """
    # Fetch all habits from the database
    habits = Habit.list_all(db_manager)
    if not habits:
        print("\nNo habits found. Please create a habit first.")
        return False

    # Filter habits into daily and weekly categories
    daily_habits = [habit for habit in habits if habit[2] == "Daily"]
    weekly_habits = [habit for habit in habits if habit[2] == "Weekly"]

    # Display daily habits
    print("\n--- Your Habits: ---")
    if daily_habits:
        print("\nDaily Habits:")
        print(tabulate(
            [[h[0], h[1], h[2], datetime.fromisoformat(h[3]).strftime("%d.%m.%Y at %H:%M")] for h in daily_habits],
            headers=["ID", "Task", "Periodicity", "Created At"]
        ))

    # Display weekly habits
    if weekly_habits:
        print("\nWeekly Habits:")
        print(tabulate(
            [[h[0], h[1], h[2], datetime.fromisoformat(h[3]).strftime("%d.%m.%Y at %H:%M")] for h in weekly_habits],
            headers=["ID", "Task", "Periodicity", "Created At"]
        ))

    return True

def create_habit():
    """
    Handles the creation of a new habit.

    Behavior:
        - Prompts the user to input a task name.
        - Allows the user to cancel the process by typing 'cancel'.
        - Prompts the user to specify the periodicity ('Daily' or 'Weekly').
            - Ensures valid input and displays an error message for invalid choices.
        - Adds the habit to the database and confirms its creation.
        - After creating the habit, prompts the user to return to the main menu or exit the app.

    Returns:
        None
    """
    # Prompt for the task name
    task = get_non_empty_input("Enter the task (or type 'cancel' to cancel): ")
    if task.lower() == "cancel":
        print("Action canceled: Creating habit.")
        return

    # Prompt for the periodicity and validate the input
    while True:
        try:
            periodicity = input("Enter the periodicity (Daily/Weekly) (or type 'cancel' to cancel): ").strip().capitalize()
            if periodicity.lower() == "cancel":
                print("Action canceled: Creating habit.")
                return
            if periodicity not in ["Daily", "Weekly"]:
                raise ValueError("Invalid periodicity. Please enter 'Daily' or 'Weekly'.")
            
            # Create and save the habit in the database
            Habit.create(task, periodicity, db_manager)
            print(f"Habit '{task}' with periodicity '{periodicity}' created successfully!")
            break
        except ValueError:
            print("Please enter 'Daily' or 'Weekly'.")

    # Prompt the user to return to the main menu or exit
    prompt_main_menu_or_exit()

def mark_habit_complete():
    """
    Handles marking a habit as complete.

    Behavior:
        - Displays all habits to the user.
        - If no habits exist, informs the user and returns to the main menu.
        - Prompts the user to input the ID of the habit to mark as complete.
            - Allows cancellation by typing 'cancel'.
            - Ensures the input is a valid numeric habit ID.
        - Loads the selected habit and marks it as complete in the database.
        - Confirms the action to the user.
        - After completing the action, prompts the user to return to the main menu or exit the app.

    Returns:
        None
    """
    # Display all habits and handle cases with no habits
    if not display_all_habits():
        print("No habits to mark as complete. Returning to the main menu.")
        return

    # Loop for user input until a valid ID or cancellation
    while True:
        try:
            habit_id_input = get_non_empty_input("Enter the ID of the habit to mark as complete (or type 'cancel' to cancel): ").lower()
            if habit_id_input == "cancel":
                print("Action canceled: Marking habit as complete.")
                break
            habit_id = int(habit_id_input)
            habit = Habit.load(habit_id, db_manager)
            habit.mark_as_complete(db_manager)
            print(f"Habit '{habit.task}' marked as complete successfully!")
            break
        except ValueError:
            print("Please enter a valid numeric habit ID.")

    # Prompt the user to return to the main menu or exit
    prompt_main_menu_or_exit()

def delete_habit():
    """
    Handles deleting a habit.

    Behavior:
        - Displays all habits to the user.
        - If no habits exist, informs the user and returns to the main menu.
        - Prompts the user to input the ID of the habit to delete.
            - Allows cancellation by typing 'cancel'.
            - Ensures the input is a valid numeric habit ID.
        - Loads the selected habit and deletes it from the database.
        - Confirms the deletion to the user.
        - After completing the action, prompts the user to return to the main menu or exit the app.

    Returns:
        None
    """
    # Display all habits and handle cases with no habits
    if not display_all_habits():
        print("No habits to delete. Returning to the main menu.")
        return

    # Loop for user input until a valid ID or cancellation
    while True:
        try:
            habit_id_input = get_non_empty_input("Enter the ID of the habit to delete (or type 'cancel' to cancel): ").lower()
            if habit_id_input == "cancel":
                print("Action canceled: Deleting habit.")
                break
            habit_id = int(habit_id_input)
            habit = Habit.load(habit_id, db_manager)
            habit.delete(db_manager)
            print(f"Habit '{habit.task}' deleted successfully!")
            break
        except ValueError:
            print("Please enter a valid numeric habit ID.")

    # Prompt the user to return to the main menu or exit
    prompt_main_menu_or_exit()

def display_main_menu():
    """
    Displays the main menu for the Habit Tracker and handles user input.

    Behavior:
        - Continuously displays the main menu options until the user exits the program.
        - Prompts the user to select one of the available menu options.
        - Calls the appropriate function based on the user's choice:
            1. `create_habit` - Allows the user to create a new habit.
            2. `display_all_habits` - Displays all habits stored in the database.
            3. `mark_habit_complete` - Allows the user to mark a habit as completed.
            4. `delete_habit` - Deletes a habit from the database.
            5. `display_analytics_menu` - Displays the analytics menu for detailed habit analysis.
            6. Exit - Ends the program and provides a farewell message.

    Input:
        - User is prompted to select a menu option (1-6).

    Returns:
        None
    """
    while True:
        # Display menu options
        print("\n--- Habit Tracker Menu ---")
        print("1. Create a Habit")
        print("2. View Habits")
        print("3. Mark Habit as Complete")
        print("4. Delete Habit")
        print("5. View Analytics")
        print("6. Exit")

        # Prompt user for choice and validate
        choice = get_menu_choice("Select an option (1-6): ", {"1", "2", "3", "4", "5", "6"})

        # Route to the appropriate functionality
        if choice == "1":
            create_habit()
        elif choice == "2":
            display_all_habits()
        elif choice == "3":
            mark_habit_complete()
        elif choice == "4":
            delete_habit()
        elif choice == "5":
            display_analytics_menu()
        elif choice == "6":
            print("Exiting the Habit Tracker. Goodbye!")
            break

if __name__ == "__main__":
    display_main_menu()