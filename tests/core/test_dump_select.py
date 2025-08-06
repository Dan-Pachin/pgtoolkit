import os
from unittest.mock import MagicMock
from core.dump_select import select_dump_file 
import pytest


def test_no_such_directory(mocker, capsys):
    mocker.patch("os.path.isdir", return_value=False)

    result = select_dump_file("/fake/path")

    assert result is None
    out = capsys.readouterr().out
    assert "❌ No such directory: /fake/path" in out


def test_no_matching_files(mocker, capsys):
    mocker.patch("os.path.isdir", return_value=True)
    mocker.patch("os.listdir", return_value=["file1.txt", "file2.sql"])

    result = select_dump_file("/mocked/dir")

    assert result is None
    out = capsys.readouterr().out
    assert "❌ No '.dump' files found in /mocked/dir" in out


def test_user_cancels_selection(mocker):
    mocker.patch("os.path.isdir", return_value=True)
    mocker.patch("os.listdir", return_value=["a.dump", "b.dump"])
    mock_select = mocker.patch("questionary.select")
    mock_select.return_value.ask.return_value = None

    result = select_dump_file("/mocked/dir")

    assert result is None


def test_successful_selection(mocker):
    mocker.patch("os.path.isdir", return_value=True)
    mocker.patch("os.listdir", return_value=["b.dump", "a.dump"])
    mock_select = mocker.patch("questionary.select")
    mock_select.return_value.ask.return_value = "a.dump"

    result = select_dump_file("/mocked/dir")

    assert result == os.path.join("/mocked/dir", "a.dump")