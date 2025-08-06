from unittest.mock import MagicMock
from core.drop_database import drop_database  # Adjust to your actual path


def test_drop_database_success(mocker, capsys):
    fake_cursor = MagicMock()

    drop_database(cursor=fake_cursor, database="test_db")

    fake_cursor.execute.assert_called_once_with("DROP DATABASE IF EXISTS test_db")

    out = capsys.readouterr().out
    assert "✔ test_db drop successfull" in out


def test_drop_database_failure_handling(mocker, capsys):
    fake_cursor = MagicMock()
    fake_cursor.execute.side_effect = Exception("simulated error")

    try:
        drop_database(cursor=fake_cursor, database="bad_db")
    except Exception:
        pass

    fake_cursor.execute.assert_called_once_with("DROP DATABASE IF EXISTS bad_db")