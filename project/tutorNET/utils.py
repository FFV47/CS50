from functools import wraps

from flask import redirect, render_template, session
from flask.helpers import url_for


def apology(message: str, code: int = 400):
    """Render message as an apology to user."""

    def escape(msg: str) -> str:
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
            msg = msg.replace(old, new)
        return msg

    return render_template("apology.html", top=escape(message), bottom=code)


def login_required(f):
    """
    Decorate routes to require login.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return decorated_function
