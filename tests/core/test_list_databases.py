from core.list_databases import list_databases
from unittest.mock import MagicMock


def test_list_databases(mocker):
    fake_cursor = MagicMock()

    fake_cursor.fetchall.return_value = [
        ("db1",), ("db2",), ("db3",)
    ]

    result = list_databases(fake_cursor)

    fake_cursor.execute.assert_called_once_with("SELECT datname FROM pg_database WHERE datistemplate = false;")


    fake_cursor.fetchall.assert_called_once()

    assert result == ["db1", "db2", "db3"]