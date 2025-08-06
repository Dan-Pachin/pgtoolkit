from core.list_users import list_users
from unittest.mock import MagicMock


def test_list_users(mocker):
    fake_cursor = MagicMock()

    fake_cursor.fetchall.return_value = [
        ("user1",), ("user2",), ("user3",)
    ]

    result = list_users(fake_cursor)

    expected_query = """
        SELECT rolname
        FROM pg_roles
        WHERE rolcanlogin = true;
    """
    fake_cursor.execute.assert_called_once_with(expected_query)

    fake_cursor.fetchall.assert_called_once()

    assert result == ["user1", "user2", "user3"]