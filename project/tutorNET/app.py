import os
from tempfile import mkdtemp

from flask import Flask, flash, redirect, render_template, request, session
from flask.helpers import url_for
from flask_session import Session
from werkzeug.exceptions import HTTPException, InternalServerError, default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from database.base_orm import db_session, init_db
from database.tables import Schedule, Subject, Teacher
from utils import apology, login_required

# Configure application
app = Flask(__name__)


init_db()
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
# Limit file uploads to 5 MB
app.config["MAX_CONTENT_LENGTH"] = 3 * 1024 * 1024
# Extensions allowed for profile photos
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
UPLOAD_FOLDER = "./static/profile"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/find-teacher", methods=["GET", "POST"])
def find_teacher():
    if request.method == "POST":
        subject = request.form.get("subject")
        weekday = request.form.get("weekday")

        if subject and weekday:
            teachers = (
                Teacher.query.join(Subject)
                .join(Schedule)
                .filter(Subject.subject == subject, Schedule.weekday == weekday)
                .all()
            )
        elif subject and not weekday:
            teachers = (
                Teacher.query.join(Subject).filter(Subject.subject == subject).all()
            )
        elif weekday and not subject:
            teachers = (
                Teacher.query.join(Subject)
                .join(Schedule)
                .filter(Schedule.weekday == weekday)
                .all()
            )
        else:
            teachers = Teacher.query.all()

        return render_template("find-teacher.html", teachers=teachers)

    teachers = Teacher.query.all()
    return render_template("find-teacher.html", teachers=teachers)


@app.route("/profile")
@login_required
def profile():
    teacher = Teacher.query.filter(Teacher.id == session["user_id"]).first()
    return render_template("profile.html", teacher=teacher, subjects=teacher.subjects)


@app.route("/update-profile", methods=["GET", "POST"])
@login_required
def update_profile():
    if request.method == "POST":
        name = request.form.get("name")
        biography = request.form.get("biography")
        photo = request.files.get("profile-photo")
        phone = request.form.get("phone")

        # If the user doesnt provide any information
        if not name and not biography and not photo and not phone:
            return apology("all fields empty", "You must fill at least one field")

        # IF the input name is already taken
        if Teacher.query.filter(Teacher.name == name).all():
            return apology("This name is already taken", "")

        # Get user from database to update profile data
        user = Teacher.query.filter(Teacher.id == session["user_id"]).one()

        # Update user profile based on filled forms
        if name:
            user.name = name
        if biography:
            user.bio = biography
        if phone:
            user.phone = phone
        if photo.filename:
            # get file extension
            photo_ext = os.path.splitext(photo.filename)[1]
            # return error if extension not allowed
            if photo_ext not in ALLOWED_EXTENSIONS:
                return apology("File type not allowed")

            # If everything goes right, save photo with user_id as filename
            file_path = os.path.join(
                app.config["UPLOAD_FOLDER"], str(session["user_id"]) + photo_ext
            )
            photo.save(file_path)
            # split file_path to store a path that Jinja can use
            db_photo = file_path.split("/")
            user.photo = url_for("static", filename=f"profile/{db_photo[-1]}")

        # Commit modifications to database
        db_session.commit()

        # User dont have any registered subject, so redirect him to add one
        if not user.subjects:
            flash(
                "You don't have any registered subjects. Without at least one subject your profile will now be shown"
            )
            return redirect(url_for("subject_handler"))

        # If they do, redirect to profile
        return redirect(url_for("profile"))

    return render_template("update-profile.html")


@app.route("/subject-handler")
@login_required
def subject_handler():
    teacher = Teacher.query.filter(Teacher.id == session["user_id"]).first()
    return render_template("subject-handler.html", subjects=teacher.subjects)


@app.route("/add-subject", methods=["POST"])
@login_required
def add_subject():
    subject = request.form.get("subject")
    weekdays = request.form.getlist("weekday")
    time_from = request.form.getlist("time-from")
    time_to = request.form.getlist("time-to")

    # Get user from DB to add subject to profile
    user = Teacher.query.filter(Teacher.id == session["user_id"]).first()

    # Create new subject based on user input
    new_subject = Subject(subject=subject)

    # Create new schedules based on user input and add to new_subject
    for i in range(len(weekdays)):
        new_subject.schedules.append(
            Schedule(weekday=weekdays[i], time_from=time_from[i], time_to=time_to[i])
        )

    # Add new_subject to subjects list on user
    # (schedules are added as well because SQLalchemy cascades on adding data)
    user.subjects.append(new_subject)
    db_session.commit()

    flash(f"You successfully added {subject} to your profile")
    return redirect(url_for("profile"))


@app.route("/remove-subject", methods=["POST"])
@login_required
def remove_subject():
    subject_name = request.form.get("subject")

    # Query for user and input subject
    teacher, subject = (
        db_session.query(Teacher, Subject)
        .filter(Teacher.id == session["user_id"], Subject.subject == subject_name)
        .one()
    )

    # Remove subject from the user list
    teacher.subjects.remove(subject)
    db_session.commit()

    flash(f"{subject_name} has been removed from your profile")

    return redirect(url_for("profile"))


@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        old_password = request.form.get("old-passwd")
        new_password = request.form.get("new-passwd")
        confirmation = request.form.get("confirmation")

        user = Teacher.query.filter(Teacher.id == session["user_id"]).first()

        # Form Validation
        if not old_password or not new_password or not confirmation:
            return apology("You must fill all fields", "")
        elif new_password != confirmation:
            return apology("Passwords doesn't match", "")
        elif old_password == new_password:
            return apology("new is same as old", "")
        elif not check_password_hash(user.pwhash, old_password):
            return apology("Wrong password", "")

        # update password hash
        user.pwhash = generate_password_hash(new_password)
        db_session.commit()

        flash("Password has been updated")

        return redirect(url_for("profile"))

    return render_template("change-password.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Form Validation
        if not username:
            return apology("You must provide a username", "")
        elif not password or not confirmation:
            return apology("You must provide a password", "")
        elif password != confirmation:
            return apology("Passwords doesn't match", "")
        elif username in (row.user for row in Teacher.query):
            return apology("This username is already taken", "")

        # Insert the new user into the DB
        new_user = Teacher(user=username, pwhash=generate_password_hash(password))
        db_session.add(new_user)
        db_session.commit()

        # Get the new user id and assign to the session
        session["user_id"] = new_user.id
        session["username"] = new_user.user

        flash(
            "Registration was successful. Please fill out the form for a complete profile."
        )

        return redirect(url_for("update_profile"))

    return render_template("register.html")


@app.route("/delete-account", methods=["GET", "POST"])
@login_required
def delete_account():
    if request.method == "POST":
        password = request.form.get("password")
        user = Teacher.query.filter(Teacher.id == session["user_id"]).first()

        # Form Validation
        if not password:
            return apology("You must type your password for deletion")
        if not check_password_hash(user.pwhash, password):
            return apology("Wrong password", "")

        # Delete user from database
        db_session.delete(user)
        db_session.commit()

        # Remove user_id from session
        session.clear()

        return redirect(url_for("index"))
    return render_template("delete-account.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # Form Validation
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return apology("must provide username", "")

        elif not password:
            return apology("must provide password", "")

        # Query database for username
        user = Teacher.query.filter(Teacher.user == username).first()

        # Ensure username exists and password is correct
        if not user or not check_password_hash(user.pwhash, password):
            return apology("invalid username or password", "")

        # Remember which user has logged in by storing on session object
        session["user_id"] = user.id
        session["username"] = user.user

        flash("You were successfully logged in!")

        # Redirect user to home page
        return redirect(url_for("profile"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect(url_for("index"))
