# Postgres manipulation tools

## Project description

This is a set of Postgres database manipulation tools written in python, consisting of two modules:

1. Core - universal tools that can be used in any project
2. Scripts - one-off, project-specific scripts

## Requirements

-   Python 3.12.3 +
-   prompt_toolkit==3.0.51
-   psycopg2==2.9.10
-   questionary==2.1.0
-   pytest==8.4.1
-   pytest-mock==3.14.1

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Tests

This project uses pytest for testing. To run all tests:

```bash
pytest
```

to run only core tests:

```bash
pytest tests/core
```

to run only scripts tests:

```bash
pytest tests/scripts
```

## Configuration

Before using tools that load .dump files (e.g., restore), you must configure the root directory where dumps are stored.

Open src/core/config.py and set the path like this:

```bash
DUMP_ROOT = "/absolute/path/to/dump/files"
```

.dump files should be placed inside their corresponding subdirectory:

```bash
/path/to/dump/files/
├── my_database/
│ ├── my_database.dump
│ └── ...
└── another_database/
│ ├── another_database.dump
│ └── ...
```

## Core

1. config - For project specific configuration, currently only used for local path
2. connect_to_database - Used to establish connection to Postgres, takes database_input, user_input params, defaults = "postgres" for both
3. list_databases - Provides a list of existing databases
4. list_users - Provides a list of existing login-enabled users
5. drop_database - Allows to drop selected database
6. create_database - Creates a new database with a choice of existing users as owner
7. restore_database - Restores a database from a .dump file created with pg_dump --format=custom to selected database
8. recreate_database - Drops and Creates back selected database

## Scripts

1. migrate_block_content - Project specific migration protocol to update data structure of content field to a new block format

## How to use

### List databases

```bash
python -m core.list_databases
```

### List Users

```bash
python -m core.list_users
```

### Create Database

```bash
python -m core.create_database
Name the database: "Your_database_name"
Select the database owner: <Select from list of available roles>
```

### Drop Database

```bash
python -m core.drop_database
Select the database to drop: <Select from list of available databases>
```

### Recreate Database (removes ALL data!)

```bash
python -m core.recreate_database
Select the database to recreate:  <Select from list of available databases>
Select the owner:  <Select from list of available roles>
```

### Restore Database from custom format pg_dump

The root path must be set in config:
DUMP_ROOT = "/path/to/dump/files"
.dump files should be placed inside their corresponding subdirectory:

```bash
/path/to/dump/files/
├── my_database/
│ ├── my_database.dump
│ └── ...
└── another_database/
│ ├── another_database.dump
│ └── ...
```

Run:

```bash
python -m core.restore_database
Select database  <Select from list of available databases>
Select a dump file:  <Select from list of available dump files>
```
