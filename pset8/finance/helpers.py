import os
import sqlite3
from functools import wraps
from urllib.parse import quote_plus

import requests
from flask import g, redirect, render_template, request, session
from flask.helpers import flash


def apology(message: str, code: int = 400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def lookup(symbol: str) -> dict or None:
    """Look up quote for symbol.

    :param symbol: stock symbol to be quoted
    :return:
    ```
    {
        name: companyName,
        price: latestPrice,
        symbol: symbol,
        date: latestTime,
    }
    ```
    """

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(
            f"https://cloud-sse.iexapis.com/stable/stock/{quote_plus(symbol)}/quote?token={api_key}"
        )
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"],
            "date": quote["latestTime"],
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value: float) -> str:
    """Format value as USD."""
    return f"${value:,.2f}"


def get_db() -> sqlite3.Connection:
    """
    connect to DB and stores on the 'g' object (only exists during context)
    """
    if "db" not in g:
        g.db = sqlite3.connect("finance.db")
        g.db.row_factory = sqlite3.Row

    return g.db


def get_iexdb() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect("iexcloud.db")
        g.db.row_factory = sqlite3.Row

    return g.db


def query_db(query: str, args: tuple = ()) -> list:
    """Request query handler for sqlite3

    :param query: SQL query
    :param args: SQL string arguments, defaults to empty `tuple`
    :return: Query response as sqlite `Row` object
    """
    cur = get_db().execute(query, args)
    # Create a list with dicts for each row from que query
    rowValues = [dict(row) for row in cur.fetchall()]
    cur.close()
    return rowValues


def mod_db(query: str, args: tuple = ()):
    """Modification query handler for sqlite3

    :param query: SQL query
    :param args: SQL string arguments, defaults to empty `tuple`
    """
    db = get_db()
    db.execute(query, args)
    db.commit()
