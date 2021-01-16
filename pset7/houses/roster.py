import sqlite3
from sys import argv, exit

db = sqlite3.connect("students.db")

houses = []
for i in db.execute("SELECT DISTINCT house FROM students"):
    houses.append(i[0])

if len(argv) != 2:
    print("Usage: python roster.py HOUSE")
    exit(1)
if argv[1].lower().capitalize() not in houses:
    print("Usage: python roster.py HOUSE")
    exit(1)

for row in db.execute(
    """SELECT first, middle, last, birth FROM students WHERE house = ?
    ORDER BY last, first""",
    (argv[1].lower().capitalize(),),
):
    first, middle, last, birth = row
    if middle is None:
        print(f"{first} {last}, born {birth}")
    else:
        print(f"{first} {middle} {last}, born {birth}")

db.close()
