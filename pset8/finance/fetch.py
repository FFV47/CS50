import os
import sqlite3
import requests

dbFile = "iexcloud.db"
api_key = os.environ.get("API_KEY")
print(api_key)
payload = {"token": api_key}


def conn_database(db: str) -> sqlite3.Connection:
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


def fetch_data(db: sqlite3.Connection):
    c = 0
    try:
        resp = requests.get(
            "https://cloud.iexapis.com/beta/ref-data/symbols", params=payload
        )
        print(resp.status_code)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(e)
        return None

    try:
        data = resp.json()
        for company in data:
            db.execute(
                "INSERT INTO companies (name, symbol) VALUES (?, ?)",
                (company["name"], company["symbol"]),
            )
            c = c + 1
        db.commit()
        db.close()
    except sqlite3.Error as e:
        print(e)
        return None


if __name__ == "__main__":
    db = conn_database(dbFile)
    fetch_data(db)
