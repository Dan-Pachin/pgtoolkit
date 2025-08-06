from core.connect_to_database import connect_to_database



def list_databases(cursor):
    cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
    database_list = [row[0] for row in cursor.fetchall()]
    return database_list

def main():
    connection = connect_to_database()
    cursor = connection.cursor()
    database_list = list_databases(cursor)
    print(database_list)


if __name__ == "__main__":
    main()

