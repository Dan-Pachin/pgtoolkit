import subprocess
import os
from core.config import DUMP_ROOT
from core.list_databases import list_databases
from core.list_users import list_users
import questionary
from core.connect_to_database import connect_to_database
from core.dump_select import select_dump_file


def restore_custom_format_database(
    database,
    dump,
    user="postgres",
    host="localhost",
    port="5432",
    password=None,
):
    env = os.environ.copy()
    if password:
        env["PGPASSWORD"] = password

    cmd = [
        "pg_restore",              
        "--no-owner",
        f"--dbname={database}",
        f"--host={host}",
        f"--port={port}",
        f"--username={user}",
        dump
    ]

    try:
        subprocess.run(cmd, env=env, check=True)
        print(f"\u2714 Restore of {database} from {dump} completed.")
    except subprocess.CalledProcessError as e:
        print(f"\u274c Restore failed: {e}")

def main():
    connection = connect_to_database()
    cursor = connection.cursor()
    database_list = list_databases(cursor=cursor)
    database = questionary.select("Select database",choices=database_list).ask()
    dump_path = DUMP_ROOT + database
    dump = select_dump_file(dump_dir=dump_path)
    user_list = list_users(cursor=cursor)
    user = questionary.select("Select user",choices=user_list).ask()
    restore_custom_format_database(database=database, dump=dump, user=user)

if __name__ == "__main__":
    main()
