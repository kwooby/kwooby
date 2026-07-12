from flask import Flask, render_template
import sqlite3
from datetime import date

mile_tracker = Flask(__name__)

def get_db_connection():
    connection = sqlite3.connect("miles.db")
    connection.row_factory = sqlite3.Row
    return connection

def create_table():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY,
            activity TEXT NOT NULL,
            miles REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS cats (
            id INTEGER PRIMARY KEY,
            image_filename TEXT
        )
    """)

    connection.commit()
    connection.close()

@mile_tracker.route("/log-details", methods=["POST"])
def log_details():
    # run data here
    today = str(date.today())

    return "Miles logged"

@mile_tracker.route("/log-photos", methods=["POST"])
def log_photos():
    # save photo here
    return "Photo stored in the archive"

@mile_tracker.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    create_table()
    mile_tracker.run(debug=True)