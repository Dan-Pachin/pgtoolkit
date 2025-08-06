import json
from scripts.migrate_block_content import process_table


def test_process_table_updates_rows(mocker):
    fake_cursor = mocker.Mock()

    fake_cursor.fetchall.return_value = [
        (1, [{"type": "p", "text": "Old"}]),
        (2, [{"type": "img", "src": "/a.png"}]),
    ]

    expected_transform_results = [
        [{"type": "paragraph", "children": [{"type": "text", "text": "Old"}]}],
        [{"type": "image", "src": "/a.png"}]
    ]

    mock_transform = mocker.patch("scripts.migrate_block_content.transform_content")
    mock_transform.side_effect = expected_transform_results

    process_table(fake_cursor, "my_table")

    fake_cursor.execute.assert_any_call("SELECT id, content FROM my_table WHERE content IS NOT NULL")

    assert fake_cursor.execute.call_count == 3

    update_calls = [
        mocker.call(
            "UPDATE my_table SET content = %s WHERE id = %s",
            [json.dumps(expected_transform_results[i]), row_id]
        )
        for i, (row_id, _) in enumerate(fake_cursor.fetchall.return_value)
    ]
    fake_cursor.execute.assert_has_calls(update_calls, any_order=False)