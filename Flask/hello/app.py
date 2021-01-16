import random

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
@app.route("/<name>")
def index(name=None):
    number = random.randint(0, 1)
    return render_template("index.html", number=number, name=name)


@app.route("/hello")
def hello():
    fname = request.args.get("fname", type=str)
    lname = request.args.get("lname", type=str)
    if not fname or not lname:
        return render_template("failure.html")
    return render_template("hello.html", fname=fname, lname=lname)
