import csv
import sqlite3
from sys import argv, exit

if len(argv) != 2:
    print("Usage: python import.py csvfile.csv")
    exit(1)

with open(argv[1], "r", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    # Create a object to represent the database
    db = sqlite3.connect("students.db")

    for row in reader:
        name = row["name"].split()
        if len(name) == 2:
            sql = (name[0], None, name[1], row["house"], row["birth"])
            db.execute(
                """INSERT INTO students (first, middle, last, house, birth)
                VALUES (?, ?, ?, ?, ?)""",
                sql,
            )
        else:
            sql = (name[0], name[1], name[2], row["house"], row["birth"])
            db.execute(
                """INSERT INTO students (first, middle, last, house, birth)
                VALUES (?, ?, ?, ?, ?)""",
                sql,
            )

    # Write all the changes to the database
    db.commit()

    # Close the database the object 'db' was accessing
    db.close()
