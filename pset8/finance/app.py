import os
from tempfile import mkdtemp

from flask import Flask, flash, g, redirect, render_template, request, session
from flask_session import Session
from werkzeug.exceptions import HTTPException, InternalServerError, default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

import initDB
from helpers import apology, get_iexdb, login_required, lookup, mod_db, query_db, usd

# Create database if not already
db = initDB.create_database("finance.db")
initDB.create_tables(db)

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# DB is closed after request is done
@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)

    if db is not None:
        db.close()


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():

    stocks_table = query_db(
        """
        SELECT * FROM stocks
        JOIN users ON users.id = stocks.user_id
        WHERE users.id = ?
        ORDER BY name""",
        (session["user_id"],),
    )

    # update the prices on page refresh
    for row in stocks_table:
        quote = lookup(row["symbol"])
        row["price"] = quote["price"]
        date = quote["date"]

    # get total value of the user stocks
    stocks_value = 0
    for value in stocks_table:
        stocks_value += value["shares"] * value["price"]

    rows = query_db("SELECT cash FROM users WHERE id = ?", (session["user_id"],))

    return render_template(
        "index.html",
        stocks_table=stocks_table,
        cash=rows[0]["cash"],
        stocks_value=stocks_value,
        date=date,
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Quote the stock from the market symbol provided
        quote = lookup(symbol)

        # Symbol form validation
        if quote is None:
            return apology("please try again", "stock not found")
        if symbol == "" or shares == "" or shares == "0" or int(shares) < 0:
            return apology("please try again", "missing symbol or shares")

        # Set and update some variables
        shares = int(shares)
        symbol = quote["symbol"]
        buyout = quote["price"] * shares

        # Get the current cash the user owns
        rows = query_db("SELECT cash FROM users WHERE id = ?", (session["user_id"],))
        current_cash = rows[0]["cash"]

        # Checks if the user have enough funds to buy the stocks
        if buyout > current_cash:
            return apology("buyout denied", "not enough funds")

        # checks if there is some shares of the same stock buyout in the wallet
        # If the user already have shares update the database with new values
        # If they don't, add new row with the buyout data
        rows = query_db(
            "SELECT * FROM stocks WHERE symbol = ? AND user_id = ?",
            (symbol, session["user_id"]),
        )
        if rows:
            mod_db(
                """UPDATE stocks
                SET shares = shares + ?, price = ?
                WHERE symbol = ? AND user_id = ?""",
                (shares, quote["price"], symbol, session["user_id"]),
            )
        else:
            mod_db(
                "INSERT INTO stocks VALUES (?, ?, ?, ?, ?)",
                (session["user_id"], symbol, quote["name"], shares, quote["price"],),
            )

        # Record the buyout data into history
        mod_db(
            """INSERT INTO history
            VALUES (?, ?, ?, ?, datetime('now','localtime'))""",
            (session["user_id"], symbol, shares, quote["price"]),
        )

        # Update the user cash
        new_cash = current_cash - buyout
        mod_db(
            """
               UPDATE users
               SET cash = ?
               WHERE id = ?
               """,
            (new_cash, session["user_id"]),
        )

        flash(
            f"You just bought {shares} shares of {quote['name']} at {usd(quote['price'])} each."
        )

        return redirect("/")


@app.route("/history")
@login_required
def history():
    rows = query_db(
        "SELECT symbol, shares, price, trans_time FROM history WHERE user_id = ?",
        (session["user_id"],),
    )
    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = query_db(
            "SELECT * FROM users WHERE username = ?", (request.form.get("username"),)
        )

        # Ensure username exists and password is correct
        if not rows or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash("You were successfully logged in!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        if symbol == "":
            return apology("please try again", "no symbol provided")
        if symbol is None:
            return apology("please try again", "stock not found")

        quote = lookup(symbol)

        return render_template("quote.html", quote=quote)


@app.route("/companyname", methods=["POST"])
@login_required
def company_name():
    company = request.form.get("companyname")

    if company == "":
        return apology("Please try again", "no name provided")
    company = "%" + company + "%"

    cur = get_iexdb().execute(
        "SELECT name, symbol FROM companies WHERE name LIKE ?", (company,)
    )
    # Create a list with dicts for each row from que query
    rows = [dict(row) for row in cur.fetchall()]
    return render_template("quote.html", rows=rows)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        user = request.form.get("username")
        passwd = request.form.get("password")
        passwd_confirm = request.form.get("confirmation")

        # Form Validation
        if user == "":
            return apology("", "You must provide a username")
        elif passwd == "" or passwd_confirm == "":
            return apology("", "You must provide a password")
        elif passwd != passwd_confirm:
            return apology("", "Password don't match")
        elif user in (
            row["username"] for row in query_db("SELECT username FROM users")
        ):
            return apology("", "This name is already taken")

        # Insert the new user into the DB
        mod_db(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            (user, generate_password_hash(passwd)),
        )

        # Get the new user id and assign to the session
        rows = query_db("SELECT id FROM users WHERE username = ?", (user,))
        session["user_id"] = rows[0]["id"]

        flash("Registration was successful. Enjoy!!!")

        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        symbols = query_db(
            "SELECT symbol FROM stocks WHERE user_id = ?", (session["user_id"],)
        )
        return render_template("sell.html", symbols=symbols)
    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Form Validation
        if symbol is None:
            return apology("please try again", "no symbol provided")
        if shares == "" or shares == "0":
            return apology("please try again", "missing shares")

        rows = query_db(
            "SELECT shares FROM stocks WHERE symbol = ? AND user_id = ?",
            (symbol, session["user_id"]),
        )
        if int(shares) > rows[0]["shares"]:
            return apology("please try again", "too many shares")

        quote = lookup(symbol)

        # Variable updates
        shares = int(shares)
        symbol = quote["symbol"]
        sellout = shares * quote["price"]

        # Database updates after sellout
        mod_db(
            """UPDATE stocks
               SET shares = shares - ?, price = ?
               WHERE user_id = ? AND symbol = ?""",
            (shares, quote["price"], session["user_id"], symbol),
        )
        mod_db(
            "UPDATE users SET cash = cash + ? WHERE id = ?",
            (sellout, session["user_id"]),
        )

        # Record the sellout data into history
        mod_db(
            """INSERT INTO history (user_id, symbol, shares, price, trans_time)
               VALUES (?, ?, ?, ?, datetime('now','localtime'))""",
            (session["user_id"], symbol, -shares, quote["price"]),
        )

        # If you the user sell every share, remove stock from database
        rows = query_db(
            "SELECT * FROM stocks WHERE symbol = ? AND user_id = ?",
            (symbol, session["user_id"]),
        )
        if rows[0]["shares"] == 0:
            mod_db(
                "DELETE FROM stocks WHERE user_id = ? AND symbol = ?",
                (session["user_id"], symbol),
            )

        flash(
            f"You just sold {shares} shares of {quote['name']} at {usd(quote['price'])} each."
        )

        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
