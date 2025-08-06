import psycopg2
import psycopg2.extensions



def connect_to_database(database_input="postgres", user_input="postgres"):
    try: 
        connection = psycopg2.connect(dbname=database_input, user=user_input) 
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        print(f"\u2714 Database conntection successfully established {connection}")
        return connection
    except psycopg2.OperationalError as e:
        password_input = input("Please enter password for user 'postgres': ")
        connection = psycopg2.connect(dbname=database_input, user=user_input, password = password_input) 
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        print(f"\u2714 Database conntection successfully established via password {connection}")
        return connection
    except Exception as e:
        print(f"Connection failed with Exception: {e}")
        return None

def main():
    connection = connect_to_database()
    print(connection.cursor())
    connection.close()
    

    
if __name__ == "__main__":
    main()