import pytest
from unittest.mock import MagicMock
from core.create_database import create_database  # Replace with your actual file path


def test_create_database_success(mocker):
    fake_cursor = MagicMock()

    # Call the function with fake values
    create_database(cursor=fake_cursor, database="test_db", owner="test_user")

    # Make sure the correct SQL command was executed
    fake_cursor.execute.assert_called_once_with("CREATE DATABASE test_db OWNER test_user")


def test_create_database_failure(mocker):
    fake_cursor = MagicMock()
    fake_cursor.execute.side_effect = Exception("Simulated DB error")

    # Optional: capture print output if needed
    with pytest.raises(Exception):
        # We'll let the function print the error but test the handling
        create_database(cursor=fake_cursor, database="fail_db", owner="bad_user")

    # Check that execute was attempted despite the failure
    fake_cursor.execute.assert_called_once_with("CREATE DATABASE fail_db OWNER bad_user")