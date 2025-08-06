from core.list_databases import list_databases
from core.connect_to_database import connect_to_database
import questionary

def drop_database(cursor, database):
        cursor.execute(f"DROP DATABASE IF EXISTS {database}")
        print(f"\u2714 {database} drop successfull")


def main():
    connection = connect_to_database()
    cursor = connection.cursor()
    database_list = list_databases(cursor)
    database = questionary.select("Select the database to drop: ", choices=database_list).ask()
    try:
        drop_database(database=database,cursor=cursor)
    except Exception as e:
        print(f"\u274c Drop failed with Exception: {e}")

if __name__ == "__main__":
    main()