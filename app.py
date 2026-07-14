import sqlite3
import os
from flask import Flask, render_template, request, session, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

PASSWORD = os.environ.get("PASSWORD")

def get_db_connection():
    connection = sqlite3.connect("miles.db")
    connection.row_factory = sqlite3.Row
    return connection

def create_table():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity TEXT NOT NULL,
            miles REAL NOT NULL,
            run_date TEXT NOT NULL
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS cats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            photo_filename TEXT
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

@app.route("/home")
def home():
    if not session.get("authenticated"):
        return redirect("/")
    
    return render_template("home.html")

@app.route("/mile-tracker")
def mile_tracker():
    if not session.get("authenticated"):
        return redirect("/")
    
    return render_template("mile-tracker.html")

@app.route("/log-details", methods=["POST"])
def log_details():
    if not session.get("authenticated"):
        return redirect("/")
    
    activity = request.form["activity"]
    miles = float(request.form["miles"])
    run_date = request.form["run_date"]

    connection = get_db_connection()

    connection.execute("""
        INSERT INTO runs (activity, miles, run_date)
        VALUES (?, ?, ?)
    """, (activity, miles, run_date))

    connection.commit()
    connection.close()

    return "Miles logged"

@app.route("/log-photos", methods=["POST"])
def log_photos():
    if not session.get("authenticated"):
        return redirect("/")
    
    photo = request.files["log_photos"]

    filename = secure_filename(photo.filename)
    photo.save(f"static/images/{filename}")

    connection = get_db_connection()

    connection.execute("""
        INSERT INTO cats (photo_filename)
        VALUES (?)
    """, (filename,))

    connection.commit()
    connection.close()

    return "Photo stored in archive"

@app.route("/photos")
def display_photos():
    if not session.get("authenticated"):
        return redirect("/")
    
    connection = get_db_connection()

    photos = connection.execute("""
        SELECT * FROM cats
    """).fetchall()

    connection.close()

    return render_template("photos.html", photos=photos)

if __name__ == "__main__":
    create_table()
    app.run()