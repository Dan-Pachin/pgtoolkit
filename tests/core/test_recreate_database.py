from core.recreate_database import main


def test_recreate_main_flow(mocker):
    fake_cursor = mocker.Mock()
    fake_conn = mocker.Mock()
    fake_conn.cursor.return_value = fake_cursor
    mock_connect = mocker.patch("core.recreate_database.connect_to_database", return_value=fake_conn)

    mocker.patch("core.recreate_database.list_databases", return_value=["db1", "db2"])
    mocker.patch("core.recreate_database.list_users", return_value=["user1", "user2"])

    select_mock = mocker.patch("core.recreate_database.questionary.select")
    select_mock.side_effect = [
        mocker.Mock(ask=mocker.Mock(return_value="db1")),
        mocker.Mock(ask=mocker.Mock(return_value="user1"))
    ]

    mock_drop = mocker.patch("core.recreate_database.drop_database")
    mock_create = mocker.patch("core.recreate_database.create_database")

    main()

    mock_connect.assert_called_once()
    fake_conn.cursor.assert_called_once()
    select_mock.assert_any_call("Select the database to recreate: ", choices=["db1", "db2"])
    select_mock.assert_any_call("Select the owner: ", choices=["user1", "user2"])
    mock_drop.assert_called_once_with(database="db1", cursor=fake_cursor)
    mock_create.assert_called_once_with(database="db1", owner="user1", cursor=fake_cursor)