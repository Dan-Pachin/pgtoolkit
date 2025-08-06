from core.connect_to_database import connect_to_database

def list_users(cursor):
    cursor.execute("""
        SELECT rolname
        FROM pg_roles
        WHERE rolcanlogin = true;
    """)
    user_list = [row[0] for row in cursor.fetchall()]
    return user_list

def main():
    connection = connect_to_database()
    cursor = connection.cursor()
    users_list = list_users(cursor)
    print(users_list)

if __name__ == "__main__":
    main()