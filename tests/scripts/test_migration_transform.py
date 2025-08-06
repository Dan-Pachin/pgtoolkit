from scripts.migrate_block_content import convert_legacy_block, transform_content


def test_convert_heading_block():
    block = {"type": "h2", "text": "Title", "className": "my-heading"}
    result = convert_legacy_block(block)
    assert result == {
        "type": "heading",
        "children": [{"type": "text", "text": "Title"}],
        "className": "my-heading"
    }


def test_convert_paragraph_block():
    block = {"type": "p", "text": "Some paragraph", "className": "txt"}
    result = convert_legacy_block(block)
    assert result["type"] == "paragraph"
    assert result["children"][0]["text"] == "Some paragraph"


def test_convert_image_block():
    block = {"type": "img", "src": "/img.png", "alt": "An image"}
    result = convert_legacy_block(block)
    assert result["type"] == "image"
    assert result["src"] == "/img.png"
    assert result["alt"] == "An image"


def test_convert_unknown_block_returns_none():
    block = {"type": "unknown", "text": "..." }
    result = convert_legacy_block(block)
    assert result is None


def test_transform_content_filters_none():
    legacy = [
        {"type": "p", "text": "Hello"},
        {"type": "unknown", "text": "skip me"},
        {"type": "img", "src": "/pic.png"}
    ]
    result = transform_content(legacy)
    assert len(result) == 2
    assert result[0]["type"] == "paragraph"
    assert result[1]["type"] == "image"