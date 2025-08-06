from core.restore_database import restore_custom_format_database
import subprocess


def test_restore_database_success(mocker, capsys):
    mock_run = mocker.patch("subprocess.run", return_value=None)

    restore_custom_format_database(
        database="mydb",
        dump="/some/path/mydb.dump",
        user="myuser",
        host="localhost",
        port="5432",
        password="secret"
    )

    mock_run.assert_called_once()
    args, kwargs = mock_run.call_args

    expected_cmd = [
        "pg_restore",
        "--no-owner",
        "--dbname=mydb",
        "--host=localhost",
        "--port=5432",
        "--username=myuser",
        "/some/path/mydb.dump"
    ]
    assert args[0] == expected_cmd

    assert kwargs["env"]["PGPASSWORD"] == "secret"

    out = capsys.readouterr().out
    assert "✔ Restore of mydb from /some/path/mydb.dump completed." in out


def test_restore_database_no_password(mocker, capsys):
    mock_run = mocker.patch("subprocess.run", return_value=None)

    restore_custom_format_database(
        database="mydb",
        dump="/some/path/mydb.dump",
        user="postgres"
    )

    args, kwargs = mock_run.call_args

    assert "PGPASSWORD" not in kwargs["env"]

    out = capsys.readouterr().out
    assert "✔ Restore of mydb from /some/path/mydb.dump completed." in out


def test_restore_database_failure(mocker, capsys):
    mock_run = mocker.patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "pg_restore"))

    restore_custom_format_database(
        database="faildb",
        dump="/bad/path/faildb.dump"
    )

    out = capsys.readouterr().out
    assert "❌ Restore failed" in out