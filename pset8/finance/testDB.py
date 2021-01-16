import sqlite3

dbFile = "finance.db"


def create_database(db: str) -> sqlite3.Connection:
    """
    Create sqlite3 database and return the connection
    to the database
    :param db: name of database file
    """
    connDB = None
    try:
        connDB = sqlite3.connect(db)
        return connDB
    except sqlite3.Error as e:
        print(e)


def insert(conn: sqlite3.Connection):
    """
    Create tables in the database through `conn`
    """
    try:
        conn.executescript(
            """INSERT INTO users (username, hash)
            VALUES ('fer','hash1');

            INSERT INTO users (username, hash)
            VALUES ('selma','hash2');

            INSERT INTO users (username, hash)
            VALUES ('flavio','hash3');

            INSERT INTO users (username, hash)
            VALUES ('jorge','hash4');
                           """
        )
        conn.commit()
    except sqlite3.Error as e:
        print(e)


if __name__ == "__main__":
    db = create_database(dbFile)
    insert(db)
