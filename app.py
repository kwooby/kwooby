import psycopg2
from psycopg2.extras import RealDictCursor
import os
import uuid
import calendar
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect, flash, url_for
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import cloudinary
import cloudinary.uploader

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = os.environ.get("SECRET_KEY")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file (filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db_connection():
    return psycopg2.connect(
        os.environ["DATABASE_URL"],
        cursor_factory=RealDictCursor
    )


def create_table():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS runs (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    activity TEXT NOT NULL,
                    miles REAL NOT NULL,
                    run_date DATE NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS photos (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    photo_filename TEXT NOT NULL
                )
            """)

        connection.commit()


@app.route("/")
def index():
    return render_template('portfolio/index.html')

@app.route("/mile-tracker/register_user", methods=["GET", "POST"])
def register_user():
    if request.method == "GET":
        return render_template("mile-tracker/register-user.html")
        
    if request.method == "POST":
        username = request.form["username"].strip().lower()
        password = request.form["password"]
        confirm_password = request.form["confirm-password"]

        # Validation

        if len(username) < 3:
            flash("Username must be at least 3 characters.")
            return redirect(url_for("register_user"))

        if len(password) < 5:
            flash("Password must be at least 5 characters.")
            return redirect(url_for("register_user"))

        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for("register_user"))

        password_hash = generate_password_hash(password)

        try:
            with get_db_connection() as connection:
                with connection.cursor() as cursor:

                    cursor.execute("""
                        INSERT INTO users (username, password_hash)
                        VALUES (%s, %s)
                    """, (username, password_hash))

                connection.commit()

        except psycopg2.IntegrityError:
            flash("Username already exists")
            return redirect(url_for("register_user"))

        return redirect(url_for("login"))

@app.route("/mile-tracker/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("mile-tracker/login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = get_user(username)

        if user and check_password_hash(user["password_hash"], password):
            session["authenticated"] = True
            session["user_id"] = user["id"]
            return redirect(url_for('dashboard'))
        else:
            return render_template("mile-tracker/login.html", error="Invalid username or password")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/mile-tracker/settings/change-username", methods=["POST"])
def change_username():
    if not session.get("authenticated") or "user_id" not in session:
        return redirect(url_for('login'))

    user_id = session["user_id"]

    new_username = request.form["change-username"].strip().lower()
    password = request.form["current-password"]

    if not new_username:
        flash("Username cannot be empty.")
        return redirect(url_for('settings'))

    if not password:
        flash("Password cannot be empty.")
        return redirect(url_for('settings'))

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM users
                WHERE id = %s
            """, (user_id,))

            user = cursor.fetchone()

            if user["username"] == new_username:
                flash("That's already your username!")
                return redirect(url_for('settings'))

            if not check_password_hash(user["password_hash"], password):
                flash("Incorrect password.")
                return redirect(url_for("settings"))

            cursor.execute("""
                UPDATE users
                SET username = %s
                WHERE id = %s
            """, (new_username, user_id))

        connection.commit()

    flash("Username updated successfully.")
    return redirect(url_for("settings"))

@app.route("/mile-tracker/settings/delete-account", methods=["POST"])
def delete_account():
    if not session.get("authenticated") or "user_id" not in session:
        return redirect(url_for('login'))

    user_id = session["user_id"]

    password = request.form["delete-current-password"]

    if not password:
        flash("Password cannot be empty")
        return redirect(url_for('settings'))

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM users
                WHERE id = %s
            """, (user_id,))

            user = cursor.fetchone()

            if not user:
                flash("User not found.")
                session.clear()
                return redirect(url_for('login'))

            if not check_password_hash(user["password_hash"], password):
                flash("Incorrect password.")
                return redirect(url_for('settings'))
            
            cursor.execute("""
                DELETE FROM users
                WHERE id = %s
            """, (user_id,))

        connection.commit()
        session.clear()

    flash("Your account has been deleted.")
    return redirect(url_for('index'))

@app.route("/delete-run/<int:run_id>", methods=["POST"])
def delete_run(run_id):
    if not session.get("authenticated") or "user_id" not in session:
        return redirect(url_for('login'))

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM runs
                WHERE id = %s AND user_id = %s
            """, (run_id, session["user_id"]))

        connection.commit()

    flash("Run deleted.")

    return redirect("/mile-tracker/dashboard")

@app.route("/log-details", methods=["POST"])
def log_details():
    if not session.get("authenticated") or "user_id" not in session:
        return redirect(url_for('login'))

    user_id = session["user_id"]
    
    activity = request.form["activity"]

    try:
        miles = float(request.form["miles"])
    except ValueError:
        flash("Please enter a number")
        return redirect("/mile-tracker/dashboard")
    
    run_date = request.form["run_date"]

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO runs (user_id, activity, miles, run_date)
                VALUES (%s, %s, %s, %s)
            """, (user_id, activity, miles, run_date))

        connection.commit()

    flash("Miles logged successfully!")
    return redirect('/mile-tracker/dashboard')

@app.route("/log-photos", methods=["POST"])
def log_photos():
    if not session.get("authenticated") or "user_id" not in session:
        return redirect(url_for('login'))
        
    photo = request.files["log_photos"]

    if photo.filename == "":
        flash("Please select a photo")
        return redirect('/mile-tracker/dashboard')

    if not allowed_file(photo.filename):
        flash("Invalid file type")
        return redirect('/mile-tracker/dashboard')

    filename = secure_filename(photo.filename)
    unique_filename = str(uuid.uuid4()) + "_" + filename

    user_id = session["user_id"]
    
    result = cloudinary.uploader.upload(
        photo,
        public_id=unique_filename,
        folder="mile-tracker"
    )

    photo_url = result["secure_url"]

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO photos (user_id, photo_filename)
                VALUES (%s, %s)
            """, (user_id, photo_url))

        connection.commit()

    flash('Photo logged successfully!')

    return redirect('/mile-tracker/dashboard')

@app.route("/delete-photo/<int:photo_id>", methods=["POST"])
def delete_photo(photo_id):
    if not session.get("authenticated") or "user_id" not in session:
        return redirect(url_for('login'))

    user_id = session["user_id"]

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT photo_filename
                FROM photos
                WHERE id = %s and user_id = %s
            """, (photo_id, user_id))

            photo = cursor.fetchone()

            if photo is None:
                flash("Photo not found.")
                return redirect(url_for('dashboard'))

            photo_url = photo["photo_filename"]

            upload_path = photo_url.split("/upload/")[1]
            public_id = upload_path.split("/", 1)[1]
            public_id = public_id.rsplit(".", 1)[0]

            cloudinary.uploader.destroy(public_id)

            cursor.execute("""
                DELETE FROM photos
                WHERE id = %s AND user_id = %s
            """, (photo_id, user_id))

            connection.commit()

    flash("Photo deleted.")
    return redirect(url_for('dashboard'))

def get_runs(user_id, activity=None, page=1, history=False, year=None):
    
    runs_per_page = 6
    offset = (page - 1) * runs_per_page

    where_clauses = ["user_id = %s"]
    params = [user_id]

    if activity:
        where_clauses.append("activity = %s")
        params.append(activity)

    if year:
        where_clauses.append("EXTRACT(YEAR FROM run_date) = %s")        
        params.append(int(year))

    where_sql = " AND ".join(where_clauses)

    sql = f"""
        SELECT * FROM runs
        WHERE {where_sql}
        ORDER BY run_date DESC
    """

    if not history:
        sql += " LIMIT %s OFFSET %s"
        params.extend([runs_per_page + 1, offset])

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, tuple(params))
            runs = cursor.fetchall()

    if history:
        return runs

    has_next_runs = len(runs) > runs_per_page

    if has_next_runs:
        runs=runs[:runs_per_page]

    return runs, has_next_runs

def get_photos(user_id, page=1):
    
    photos_per_page = 6
    offset = (page - 1) * photos_per_page
        
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM photos
                WHERE user_id = %s
                ORDER BY id DESC
                LIMIT %s OFFSET %s
            """, (user_id, photos_per_page + 1, offset))

            photos = cursor.fetchall()

    has_next_photo = len(photos) > photos_per_page

    if has_next_photo:
        photos = photos[:photos_per_page]
        
    return photos, has_next_photo

def get_total_miles(user_id):
    
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT SUM(miles) AS total_miles
                FROM runs
                WHERE user_id = %s
            """, (user_id,))

            row = cursor.fetchone()
            total_miles = row["total_miles"]

        return round(total_miles or 0, 1)
    
def get_available_years(user_id):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT EXTRACT(YEAR FROM run_date) AS year
                FROM runs
                WHERE user_id = %s
                ORDER BY year DESC
            """, (user_id,))

            years = cursor.fetchall()

    return [str(int(row["year"])) for row in years if row["year"] is not None]

def get_monthly_miles(user_id, year=None, activity=None):
    query_params = [user_id]

    where_clauses = ["user_id = %s"]

    if year:
        where_clauses.append("EXTRACT(YEAR FROM run_date) = %s")
        query_params.append(int(year))

    if activity:
        where_clauses.append("activity = %s")
        query_params.append(activity)

    where_sql = " AND ".join(where_clauses)

    sql = f"""
        SELECT
            EXTRACT(MONTH FROM run_date) AS month_num,
            SUM(miles) AS total_miles
        FROM runs
        WHERE {where_sql}
        GROUP BY month_num
        ORDER BY month_num
    """

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, tuple(query_params))
            rows = cursor.fetchall()

    result = []
    for row in rows:
        month_num = int(row["month_num"])
        month_name = calendar.month_name[month_num]
        total_miles = round(row["total_miles"] or 0, 1)
        result.append((month_num, month_name, total_miles))

    return result

def get_username(user_id):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT username FROM users WHERE id = %s",
                (user_id,)
            )

            user = cursor.fetchone()

    return user["username"] if user else None

def get_user(username):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM users
                WHERE username = %s
            """, (username,))

            user = cursor.fetchone()

    return user

@app.route("/runs-history")
def runs_history():
    if not session.get("authenticated") or "user_id" not in session:
        return redirect(url_for('login'))

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

    for run in runs:
        run["formatted_date"] = run["run_date"].strftime("%b %d, %Y")

    return render_template(
        "mile-tracker/runs-history.html",
        runs=runs,
        user=display_user,
        total_miles=total_miles,
        selected_year=selected_year,
        years=years,
        )

@app.route("/mile-tracker/dashboard")
def dashboard():
    
    if not session.get("authenticated") or "user_id" not in session:
        return redirect(url_for('login'))

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

    photos, has_next_photo = get_photos(
        user_id,
        photo_page,
        )
    
    runs, has_next_runs = get_runs(
        user_id,
        activity,
        run_page,
    )

    for run in runs:
        run["formatted_date"] = run["run_date"].strftime("%b %d")

    total_miles = get_total_miles(user_id)

    # Get list of years that have runs for this user so UI can present options
    years = get_available_years(user_id)

    # Compute monthly aggregation restricted to the selected year (if provided)
    monthly_miles = get_monthly_miles(user_id, year=selected_year)

    return render_template(
        "mile-tracker/dashboard.html",
        runs=runs,
        photos=photos,
        user=display_user,
        photo_page=photo_page,
        run_page=run_page,
        has_next_runs=has_next_runs,
        has_next_photo=has_next_photo,
        total_miles=total_miles,
        monthly_miles=monthly_miles,
        selected_year=selected_year,
        years=years
    )

@app.route("/mile-tracker/settings")
def settings():
    if not session.get("authenticated") or "user_id" not in session:
        return redirect(url_for('login'))

    user_id= session["user_id"]

    display_user=get_username(user_id)

    return render_template(
        "mile-tracker/settings.html",
        user=display_user,
    )

@app.route("/debug-users")
def debug_users():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT username FROM users")
            users = cursor.fetchall()

    return str([user["username"] for user in users])

create_table()

if __name__ == "__main__":
    app.run()