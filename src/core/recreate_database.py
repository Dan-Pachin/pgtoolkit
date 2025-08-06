from core.connect_to_database import connect_to_database
from core.list_databases import list_databases
from core.list_users import list_users
from core.drop_database import drop_database
from core.create_database import create_database
import questionary

def main():
    connection = connect_to_database()
    cursor = connection.cursor()
    database_list = list_databases(cursor)
    database = questionary.select("Select the database to recreate: ", choices=database_list).ask() 
    user_list = list_users(cursor)
    owner = questionary.select("Select the owner: ", choices=user_list).ask()
    drop_database(database=database, cursor=cursor)
    create_database(database=database, owner=owner, cursor=cursor)

if __name__ == "__main__":
    main()

