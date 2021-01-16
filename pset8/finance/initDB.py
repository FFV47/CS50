import sqlite3

dbFile = "finance.db"


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
                 CREATE TABLE IF NOT EXISTS users (
                     id INTEGER PRIMARY KEY,
                     username TEXT NOT NULL,
                     hash TEXT NOT NULL,
                     cash REAL NOT NULL DEFAULT 10000.0
                 );

                 CREATE TABLE IF NOT EXISTS stocks (
                     user_id INTEGER NOT NULL,
                     symbol TEXT NOT NULL,
                     name TEXT NOT NULL,
                     shares INTEGER NOT NULL,
                     price REAL NOT NULL,
                     FOREIGN KEY (user_id)
                        REFERENCES users (id)
                 );

                 CREATE TABLE IF NOT EXISTS history (
                     user_id INTEGER NOT NULL,
                     symbol TEXT NOY NULL,
                     shares INTEGER NOT NULL,
                     price REAL NOT NULL,
                     trans_time TEXT NOT NULL,
                     FOREIGN KEY (user_id)
                        REFERENCES stocks (user_id)
                 );

                 CREATE UNIQUE INDEX IF NOT EXISTS username_idx ON users (username);
                 CREATE INDEX IF NOT EXISTS sym_idx ON stocks (symbol);
                 CREATE INDEX IF NOT EXISTS userid_idx ON stocks (user_id);
                 CREATE INDEX IF NOT EXISTS hist_idx ON history (user_id);
                 """
        )
        conn.commit()
    except sqlite3.Error as e:
        print(e)


if __name__ == "__main__":
    db = create_database(dbFile)
    create_tables(db)
