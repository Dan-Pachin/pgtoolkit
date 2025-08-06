import psycopg2
from unittest.mock import MagicMock
from core.connect_to_database import connect_to_database  


def test_successful_connection_first_try(mocker):
    fake_conn = MagicMock()
    mock_connect = mocker.patch("psycopg2.connect", return_value=fake_conn)

    conn = connect_to_database("mydb", "myuser")

    mock_connect.assert_called_once_with(
        dbname="mydb", user="myuser", host="127.0.0.1"
    )
    fake_conn.set_isolation_level.assert_called_once()
    assert conn == fake_conn


def test_connection_requires_password_then_succeeds(mocker):
    fake_conn = MagicMock()

    mock_connect = mocker.patch("psycopg2.connect", side_effect=[
        psycopg2.OperationalError("auth failed"),
        fake_conn
    ])

    mock_input = mocker.patch("builtins.input", return_value="secret")

    conn = connect_to_database("mydb", "myuser")

    assert mock_connect.call_count == 2
    mock_connect.assert_called_with(
        dbname="mydb", user="myuser", password="secret", host="127.0.0.1"
    )
    mock_input.assert_called_once()
    fake_conn.set_isolation_level.assert_called_once()
    assert conn == fake_conn


def test_connection_fails_completely(mocker):
    mocker.patch("psycopg2.connect", side_effect=Exception("something went wrong"))
    mocker.patch("builtins.input", return_value="irrelevant")

    conn = connect_to_database("mydb", "myuser")

    assert conn is None