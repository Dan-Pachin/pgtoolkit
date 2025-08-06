import json
from core.connect_to_database import connect_to_database
from core.list_databases import list_databases
import questionary

def convert_legacy_block(block):
    btype = block.get("type")

    if btype in {"h1", "h2", "h3", "h4"}:
        return {
            "type": "heading",
            "children": [{"type": "text", "text": block["text"]}],
            "className": block.get("className"),
        }

    if btype == "p":
        return {
            "type": "paragraph",
            "children": [{"type": "text", "text": block["text"]}],
            "className": block.get("className"),
        }

    if btype == "div":
        children = [convert_legacy_block(child) for child in block.get("children", [])]
        return {
            "type": "paragraph",
            "children": [{"type": "text", "text": json.dumps([c for c in children if c])}],
            "className": block.get("className"),
        }

    if btype == "img":
        return {
            "type": "image",
            "src": block["src"],
            "alt": block.get("alt"),
            "className": block.get("className"),
        }

    if btype == "a":
        return {
            "type": "paragraph",
            "children": [
                {
                    "type": "link",
                    "href": block["href"],
                    "text": block["text"],
                    "className": block.get("className"),
                    "target": block.get("target"),
                    "rel": block.get("rel"),
                }
            ]
        }

    if btype == "table":
        rows = []

        if "headers" in block:
            rows.append({
                "type": "row",
                "className": "content-table-header",
                "cells": [
                    {"type": "header-cell", "content": h}
                    for h in block["headers"]
                ]
            })

        for r in block.get("rows", []):
            row = {
                "type": "row",
                "cells": []
            }
            for cell in r:
                if isinstance(cell, str):
                    row["cells"].append({
                        "type": "cell",
                        "content": cell
                    })
                else:
                    row["cells"].append({
                        "type": "cell",
                        "content": cell["content"],
                        "colspan": cell.get("colspan"),
                        "rowspan": cell.get("rowspan"),
                    })
            rows.append(row)

        return {
            "type": "table",
            "caption": block.get("caption"),
            "className": block.get("className"),
            "rows": rows
        }

    return None  # fallback: skip unknown types

def transform_content(content):
    if not isinstance(content, list):
        return None
    return [b for b in (convert_legacy_block(block) for block in content) if b]

def process_table(cursor, table):
    print(f"→ Processing {table}...")
    cursor.execute(f"SELECT id, content FROM {table} WHERE content IS NOT NULL")
    rows = cursor.fetchall()

    for row_id, old_content in rows:
        try:
            new_content = transform_content(old_content)
            if new_content is not None:
                cursor.execute(
                    f"UPDATE {table} SET content = %s WHERE id = %s",
                    [json.dumps(new_content), row_id]
                )
                print(f"✔ Updated row {row_id}")
        except Exception as e:
            print(f"✖ Error in {table}, ID {row_id}: {e}")

def main():
    TABLES_TO_UPDATE = [
    "news_newsentry",
    "products_product",
    "technologies_technology",
    ]   
    preconnection = connect_to_database()
    precursor = preconnection.cursor()
    database_list = list_databases(precursor)
    database = questionary.select("Select the database: ", choices=database_list).ask()
    connection = connect_to_database(database_input=database)
    cursor = connection.cursor()

    for table in TABLES_TO_UPDATE:
        process_table(cursor, table)

    connection.commit()
    cursor.close()
    connection.close()
    print("✅ All done!")

if __name__ == "__main__":
    main()
