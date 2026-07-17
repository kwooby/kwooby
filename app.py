import sqlite3
import os 
import uuid
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect, flash
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = os.environ.get("SECRET_KEY")
PASSWORD = os.environ.get("PASSWORD")


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file (filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db_connection():
    connection = sqlite3.connect("miles.db")
    connection.row_factory = sqlite3.Row
    return connection

def create_table():
    connection = get_db_connection()

    # If table structure is changed, delete miles.db and restart
    connection.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            activity TEXT NOT NULL,
            miles REAL NOT NULL,
            run_date TEXT NOT NULL
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            photo_filename TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    password = request.form["password"]

    if password == PASSWORD:
        session["authenticated"] = True
        return redirect("/home")
    
    return render_template("index.html", error="Wrong Password")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/home")
def home():
    if not session.get("authenticated"):
        return redirect("/")
    
    return render_template("home.html")

@app.route("/delete-run/<int:run_id>", methods=["POST"])
def delete_run(run_id):
    if not session.get("authenticated"):
        return redirect("/")
    
    if "user" not in session:
        return redirect("/set-user")
    
    with get_db_connection() as connection:
        connection.execute("""
            DELETE FROM runs
            WHERE id = ? AND user = ?
        """, (run_id, session["user"]))

    flash("Run deleted.")

    return redirect("/mile-tracker")

@app.route("/set-user", methods=["GET", "POST"])
def set_user():
    if not session.get("authenticated"):
        return redirect("/")
    
    if request.method == "POST":
        print("FORM DATA:", request.form)

        session["user"] = request.form["user"]

        print("SESSION: ", session)

        return redirect("/mile-tracker")

    return render_template("set-user.html")

@app.route("/log-details", methods=["POST"])
def log_details():
    if not session.get("authenticated"):
        return redirect("/")
    
    activity = request.form["activity"]

    try:
        miles = float(request.form["miles"])
    except ValueError:
        flash("Please enter a number")
        return redirect("/mile-tracker")
    
    run_date = request.form["run_date"]
    user = session["user"]

    with get_db_connection() as connection:
        connection.execute("""
            INSERT INTO runs (user, activity, miles, run_date)
            VALUES (?, ?, ?, ?)
        """, (user, activity, miles, run_date))

    flash("Miles logged successfully!")
    return redirect('/mile-tracker')

@app.route("/log-photos", methods=["POST"])
def log_photos():
    if not session.get("authenticated"):
        return redirect("/")
    
    photo = request.files["log_photos"]

    if photo.filename == "":
        flash("Please select a photo")
        return redirect('/mile-tracker')

    if not allowed_file(photo.filename):
        flash("Invalid file type")
        return redirect('/mile-tracker')

    filename = secure_filename(photo.filename)
    unique_filename = str(uuid.uuid4()) + "_" + filename

    photo.save(f"static/images/{unique_filename}")

    with get_db_connection() as connection:
        connection.execute("""
            INSERT INTO photos (photo_filename)
            VALUES (?)
        """, (unique_filename,))

    flash('Photo logged successfully!')

    return redirect('/mile-tracker')

def get_runs(user, activity=None, page=1, history=False):
    
    runs_per_page = 5
    offset = (page - 1) * runs_per_page

    with get_db_connection() as connection:
        
        if history and activity:
            runs = connection.execute("""
                SELECT * FROM runs
                WHERE user = ? AND activity = ?
                ORDER BY run_date DESC
            """, (user, activity)).fetchall()

        elif history:
            runs = connection.execute("""
                SELECT * FROM runs
                WHERE user = ?
                ORDER BY run_date DESC
            """, (user,)).fetchall()

        elif activity:
            runs = connection.execute("""
                SELECT * FROM runs
                WHERE user = ? AND activity = ?
                ORDER BY run_date DESC
                LIMIT ? OFFSET ?
            """, (user, activity, runs_per_page, offset)).fetchall()

        else:
            runs = connection.execute("""
                SELECT * FROM runs
                WHERE user = ?
                ORDER BY run_date DESC
                LIMIT ? OFFSET ?
            """, (user, runs_per_page, offset)).fetchall()

    if history:
        return runs

    return runs, len(runs) == runs_per_page

def get_photos(page=1):

    photos_per_page = 9
    offset = (page - 1) * photos_per_page

    with get_db_connection() as connection:
        photos = connection.execute("""
            SELECT * FROM photos
            ORDER BY id DESC
            LIMIT ? OFFSET ?
        """, (photos_per_page, offset)).fetchall()

    return photos

def get_total_miles(user):
    
    with get_db_connection() as connection:
        total_miles = connection.execute("""
            SELECT SUM(miles) 
            FROM runs
            WHERE user = ?
        """, (user,)).fetchone()[0]

        return total_miles or 0
    
@app.route("/runs-history")
def get_all_history():
    if not session.get("authenticated"):
        return redirect("/")
    
    if "user" not in session:
        return redirect("/set-user")
    
    user = session["user"]
    display_user = user

    total_miles = get_total_miles(user)

    runs = get_runs(user, history=True)

    return render_template(
        "runs-history.html",
        runs=runs,
        user=display_user,
        total_miles=total_miles
        )

@app.route("/mile-tracker")
def mile_tracker():
    if not session.get("authenticated"):
        return redirect("/")
    
    if "user" not in session:
        return redirect("/set-user")
        
    user = session["user"]
    display_user = user

    if user == "Katie":
        display_user="My Love"

    activity = request.args.get("activity")

    photo_page = request.args.get("photo_page", 1, type=int)
    run_page = request.args.get("run_page", 1, type=int)

    photos = get_photos(photo_page)
    runs, has_next_runs = get_runs(user, activity, run_page)

    total_miles = get_total_miles(user)

    return render_template(
        "mile-tracker.html",
        runs=runs,
        photos=photos,
        user=display_user,
        photo_page=photo_page,
        run_page=run_page,
        has_next_runs=has_next_runs,
        total_miles=total_miles
    )

if __name__ == "__main__":
    create_table()
    app.run(debug=True)