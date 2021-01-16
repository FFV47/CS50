import sqlite3

dbFile = "iexcloud.db"


def create_database(db: str) -> sqlite3.Connection:
    """
    Create sqlite3 database and return the connection
    to the database
    :param db: name of database file
    """
    try:
        connDB = sqlite3.connect(db)
        return connDB
    except sqlite3.Error as e:
        print(e)


def create_tables(conn: sqlite3.Connection):
    """
    Create tables in the database through `conn`
    """
    try:
        conn.executescript(
            """
                 CREATE TABLE IF NOT EXISTS companies (
                     id INTEGER PRIMARY KEY,
                     name TEXT NOT NULL,
                     symbol TEXT NOT NULL
                 );
                 """
        )
        conn.commit()
    except sqlite3.Error as e:
        print(e)


if __name__ == "__main__":
    db = create_database(dbFile)
    create_tables(db)
