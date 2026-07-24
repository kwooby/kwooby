import sqlite3
import os 
import uuid
import calendar
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = os.environ.get("SECRET_KEY")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file (filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db_connection():
    print("DATABASE:", os.path.abspath("miles.db"))
    
    connection = sqlite3.connect("miles.db")
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_table():
    connection = get_db_connection()

    # If table structure is changed, delete miles.db and restart
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            activity TEXT NOT NULL,
            miles REAL NOT NULL,
            run_date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            photo_filename TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        password_hash = generate_password_hash(password)

        try:
            with get_db_connection() as connection:
                connection.execute("""
                    INSERT INTO users (username, password_hash)
                    VALUES (?, ?)
                """,(username, password_hash))

            flash("Account created! Please log in.")
            return redirect("/")
        except sqlite3.IntegrityError:
            flash("Username already exists")
            return redirect("/register")

    return render_template("register.html")

@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    user = get_user(username)

    print("LOGIN ATTEMPT: ", username)
    print("FOUND USER: ", user)

    if user and check_password_hash(user["password_hash"], password):
        session["authenticated"] = True
        session["user_id"] = user["id"]
        return redirect("/home")
    else:
        return render_template("index.html", error="Invalid username or password")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/home")
def home():
    if not session.get("authenticated") or "user_id" not in session:
        return redirect("/")
    
    return render_template("home.html")

@app.route("/delete-run/<int:run_id>", methods=["POST"])
def delete_run(run_id):
    if not session.get("authenticated") or "user_id" not in session:
        return redirect("/")
    
    with get_db_connection() as connection:
        connection.execute("""
            DELETE FROM runs
            WHERE id = ? AND user_id = ?
        """, (run_id, session["user_id"]))

    flash("Run deleted.")

    return redirect("/mile-tracker")

@app.route("/log-details", methods=["POST"])
def log_details():
    if not session.get("authenticated") or "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]
    
    activity = request.form["activity"]

    try:
        miles = float(request.form["miles"])
    except ValueError:
        flash("Please enter a number")
        return redirect("/mile-tracker")
    
    run_date = request.form["run_date"]

    with get_db_connection() as connection:
        connection.execute("""
            INSERT INTO runs (user_id, activity, miles, run_date)
            VALUES (?, ?, ?, ?)
        """, (user_id, activity, miles, run_date))

    flash("Miles logged successfully!")
    return redirect('/mile-tracker')

@app.route("/log-photos", methods=["POST"])
def log_photos():
    if not session.get("authenticated") or "user_id" not in session:
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

    user_id = session["user_id"]
    
    photo.save(f"static/images/{unique_filename}")

    with get_db_connection() as connection:
        connection.execute("""
            INSERT INTO photos (user_id, photo_filename)
            VALUES (?, ?)
        """, (user_id, unique_filename,))

    flash('Photo logged successfully!')

    return redirect('/mile-tracker')

def get_runs(user_id, activity=None, page=1, history=False, year=None):
    
    runs_per_page = 5
    offset = (page - 1) * runs_per_page

    where_clauses = ["user_id = ?"]
    params = [user_id]

    if activity:
        where_clauses.append("activity = ?")
        params.append(activity)

    if year:
        where_clauses.append("strftime('%Y', run_date) = ?")
        params.append(str(year))

    where_sql = " AND ".join(where_clauses)

    sql = f"""
        SELECT* FROM runs
        WHERE {where_sql}
        ORDER BY run_date DESC
    """

    if not history:
        sql += " LIMIT ? OFFSET ?"
        params.extend([runs_per_page, offset])

    with get_db_connection() as connection:
        runs = connection.execute(sql, tuple(params)).fetchall()

    if history:
        return runs

    return runs, len(runs) == runs_per_page

def get_photos(user_id, page=1):
    
    photos_per_page = 9
    offset = (page - 1) * photos_per_page

    with get_db_connection() as connection:
        
        photos = connection.execute("""
            SELECT * FROM photos
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ? OFFSET ?
        """, (user_id, photos_per_page, offset)).fetchall()

    return photos

def get_total_miles(user_id):
    
    with get_db_connection() as connection:
        total_miles = connection.execute("""
            SELECT SUM(miles) 
            FROM runs
            WHERE user_id = ?
        """, (user_id,)).fetchone()[0]

        return round(total_miles or 0, 1)
    
def get_available_years(user_id):
    """Return a list of years (as strings) in which the user has runs, ordered desc."""
    with get_db_connection() as connection:
        years = connection.execute("""
            SELECT DISTINCT STRFTIME('%Y', run_date) as year
            FROM runs
            WHERE user_id = ?
            ORDER BY year DESC
        """, (user_id,)).fetchall()

    # fetchall returns list of sqlite3.Row; extract year strings
    return [row[0] for row in years if row[0] is not None]

def get_monthly_miles(user_id, year=None, activity=None):
    query_params = [user_id]

    where_clauses = ["user_id = ?"]

    if year:
        where_clauses.append("STRFTIME('%Y', run_date) = ?")
        query_params.append(str(year))

    if activity:
        where_clauses.append("activity = ?")
        query_params.append(activity)

    where_sql = " AND ".join(where_clauses)

    # Group by month number and order by month number so months are in calendar order
    sql = f"""
        SELECT STRFTIME('%m', run_date) as month_num,
                SUM(miles) as total_miles
        FROM runs
        WHERE {where_sql}
        GROUP BY month_num
        ORDER BY month_num
    """

    with get_db_connection() as connection:
        rows = connection.execute(sql, tuple(query_params)).fetchall()

    result = []
    for row in rows:
        month_num = int(row[0])
        month_name = calendar.month_name[month_num]
        total_miles = round(row[1] or 0, 1)
        result.append((month_num, month_name, total_miles))

    return result

def get_username(user_id):
    with get_db_connection() as connection:
        user = connection.execute(
            "SELECT username FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

    return user["username"] if user else None

def get_user(username):
    with get_db_connection() as connection:
        user = connection.execute("""
            SELECT * FROM users
            WHERE username = ?
        """, (username,)).fetchone()

    return user

@app.route("/runs-history")
def runs_history():
    if not session.get("authenticated") or "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]

    display_user = get_username(user_id)

    activity = request.args.get("activity")
    selected_year = request.args.get("year") or None

    if selected_year == "":
        selected_year = None

    years = get_available_years(user_id)
    total_miles = get_total_miles(user_id)

    runs = get_runs(
        user_id,
        activity,
        history=True,
        year=selected_year
        )

    return render_template(
        "runs-history.html",
        runs=runs,
        user=display_user,
        total_miles=total_miles,
        selected_year=selected_year,
        years=years,
        )

@app.route("/mile-tracker")
def mile_tracker():
    if not session.get("authenticated") or "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]

    display_user = get_username(user_id)

    # Activity filter (keeps existing behavior for runs listing)
    activity = request.args.get("activity")

    # Pagination params
    photo_page = request.args.get("photo_page", 1, type=int)
    run_page = request.args.get("run_page", 1, type=int)

    # Year filter (for monthly aggregation). Empty string -> None
    selected_year = request.args.get("year")

    if selected_year == "":
        selected_year = None

    photos = get_photos(user_id, photo_page)
    runs, has_next_runs = get_runs(
        user_id,
        activity,
        run_page,
        year=selected_year
    )

    total_miles = get_total_miles(user_id)

    # Get list of years that have runs for this user so UI can present options
    years = get_available_years(user_id)

    # Compute monthly aggregation restricted to the selected year (if provided)
    monthly_miles = get_monthly_miles(user_id, year=selected_year)

    return render_template(
        "mile-tracker.html",
        runs=runs,
        photos=photos,
        user=display_user,
        photo_page=photo_page,
        run_page=run_page,
        has_next_runs=has_next_runs,
        total_miles=total_miles,
        monthly_miles=monthly_miles,
        selected_year=selected_year,
        years=years
    )

if __name__ == "__main__":
    create_table()
    app.run(debug=True)