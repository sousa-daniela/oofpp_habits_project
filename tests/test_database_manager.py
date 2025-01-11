# test_database_manager.py

"""
Unit tests for the DatabaseManager class, verifying query execution functionality.

Author: Daniela de Sousa Silva
"""

import pytest
from database.database_manager import DatabaseManager

def test_execute_query(temp_db):
    """
    Test execution of a single query.

    Verifies:
        - Data is correctly inserted into the database.
        - Query results are accurately retrieved.
    """
    temp_db.execute_query("INSERT INTO habits (task, periodicity) VALUES (?, ?)", ("Yoga", "Daily"))
    result = temp_db.execute_query("SELECT * FROM habits WHERE task = ?", ("Yoga",), fetch_one=True)
    assert result is not None
    assert result[1] == "Yoga"

def test_execute_many(temp_db):
    """
    Test execution of multiple queries.

    Verifies:
        - Multiple records are successfully inserted.
        - All inserted records can be retrieved.
    """
    tasks = [("Run", "Daily"), ("Swim", "Weekly")]
    temp_db.execute_many("INSERT INTO habits (task, periodicity) VALUES (?, ?)", tasks)
    
    results = temp_db.execute_query("SELECT * FROM habits", fetch_all=True)
    assert len(results) == 2
    assert results[0][1] == "Run"
    assert results[1][1] == "Swim"