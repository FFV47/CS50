import sqlite3
from flask import Flask, redirect, render_template, g, request

app = Flask(__name__)


# ######################## GENERAL FUNCTIONS ########################
# connect to DB and stores on the 'g' object (only exists during context)
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("lecture.db")
        g.db.row_factory = sqlite3.Row

    return g.db


# Query func that returns a list with dict on each row
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rowValues = cur.fetchall()
    # cur.close()
    return (rowValues[0] if rowValues else None) if one else rowValues


# Closes the DB after query is returned (context is closed and 'g' object destroyed)
@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)

    if db is not None:
        db.close()


# ######################## ROUTES ########################
@app.route("/")
def index():
    rows = query_db("select * from registrants")
    return render_template("index.html", rows=rows)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("name", type=str)
        email = request.form.get("email", type=str)

        if not name:
            return render_template("apology.html", msg="You must provide a name")
        elif not email:
            return render_template("apology.html", msg="You must provide a email")

        cur = get_db().execute(
            "INSERT INTO registrants (name, email) VALUES (?, ?)", (name, email)
        )
        # After 'Cursor' has been closed no changes can be made
        cur.close()

        # Write all the changes to the database
        get_db().commit()

        return redirect("/")
