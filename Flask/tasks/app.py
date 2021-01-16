from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def tasks():
    if "tasks" not in session:
        session["tasks"] = []
    return render_template("tasks.html", taskList=session["tasks"])


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    elif request.method == "POST":
        tasks = request.form.getlist("task")
        for task in tasks:
            session["tasks"].append(task)
        return redirect("/")


@app.route("/updatelist", methods=["POST"])
def update_list():
    removedItem = request.form.get("item", type=str)
    session["tasks"].remove(removedItem)
    return redirect("/")
