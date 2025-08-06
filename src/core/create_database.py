from core.list_databases import list_databases
from core.list_users import list_users
from core.connect_to_database import connect_to_database
import questionary

def create_database(cursor, database, owner):
        cursor.execute(f"CREATE DATABASE {database} OWNER {owner}")
        print(f"\u2714 {database} created successfully with owner {owner}")


def main():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor = connection.cursor()
    database = input("Name the database: ")
    user_list = list_users(cursor)
    owner = questionary.select("Select the database owner: ", choices=user_list).ask()
    try:
        create_database(database=database, owner=owner, cursor=cursor)
    except Exception as e:
        print(f"\u274c Failed to create {database}: {e}")

if __name__ == "__main__":
    main()