# Habit Tracker App
**Author**: Daniela de Sousa Silva  

## Description
The Habit Tracker App is a command-line application designed to help users create, manage, and analyze their daily and weekly habits. It features:
- Habit creation and deletion.
- Marking habits as complete.
- Viewing habits with detailed analytics (streaks, completions, etc.).
- Support for daily and weekly periodicity.
- Uses SQLite for database storage, ensuring a lightweight and portable solution.
- Includes pytest-based tests to ensure the application’s functionality and reliability.

The app is cross-platform and automatically handles database creation and maintenance.

---

## Requirements
- Python 3.6 or higher  
- Supported operating systems: Windows, macOS, Linux  

Dependencies:
- `pytest` (for testing)
- `tabulate` (for tabular displays)

---

## Installation
### 1. Clone the Repository
Clone the repository to your local system using:
```
git clone https://github.com/sousa-daniela/oofpp_habits_project.git
cd habit-tracker-app
```
### 2. Install Dependencies
The app includes a setup.py file that simplifies the installation process. Run:
```
python setup.py install
```
This command:
- Installs necessary dependencies (pytest, tabulate).
- Ensures the app is ready to run.

---

## Directory Structure
The project directory is organized as follows:
```
habit-tracker-app/
│
├── setup.py                     # Installation script
├── app.py                       # Main entry point of the application
├── database/
│   ├── habit_tracker.db         # Predefined database (can be deleted)
│   ├── database_manager.py      # Database operations handler
│   ├── database_setup.py        # Database setup and table creation
│
├── models/
│   ├── habit_model.py           # Defines the Habit class
│
├── analytics/
│   ├── analytics_module.py      # Handles analytics-related computations
│
├── tests/
│   ├── conftest.py              # Test fixtures and database setup for testing
│   ├── test_habit.py            # Unit tests for Habit functionality
│   ├── test_analytics.py        # Unit tests for analytics functionality
│   ├── test_database_manager.py # Unit tests for database operations
│   ├── test_error_handling.py   # Tests for error handling
│
├── README.md                    # Project documentation
├── MANIFEST.in                  # Specifies additional files to include in the package
```

---

## Usage Instructions
Run the App.

To launch the Habit Tracker, navigate to the project directory and execute:
```
python app.py
```
### Features:
#### 1. Create a Habit
Add a new habit with a specified task and periodicity (Daily/Weekly).
#### 2. View Habits
Displays all habits categorized as Daily or Weekly.
#### 3.	Mark Habit as Complete
Mark any habit as completed for the current date.
#### 4.	Delete Habit
Permanently removes a habit from the database.
#### 5.	View Analytics
Explore detailed insights:
- Longest streaks and breaks.
- Struggling habits (completion rate below 50%).
- Habits due today or this week.
- Completed habits today or this week (with last completion timestamp).
- Completion and break counts across timeframes.
- Current streaks and breaks.
#### 6. Automatic Database Handling
If no database exists, the app will automatically create a new one.

---

## Testing Instructions
Run Tests

The app uses pytest for testing. To run all tests, execute:
```
pytest
```
This will run unit tests for:
- Habit creation, deletion, and completion.
- Analytics computations.
- Database operations and error handling.

Alternatively, if pytest is installed in a specific Python environment, you can use:
```
python -m pytest
```

---

## Database Information
- The app includes a predefined database (habit_tracker.db) with some sample data for quick testing.
- If you want to start with a fresh database:
1. Delete the habit_tracker.db file from the database/ directory.
2. Run the app again. A new database will be automatically created.

---

## Additional Notes
- Cross-Platform Compatibility: The app dynamically handles file paths, ensuring seamless operation across Windows, macOS, and Linux.
- Extensibility: The modular structure makes it easy to add new features or integrate with external systems in the future. 
