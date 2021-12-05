import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
#from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology;



# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///menu.db")

# Make sure API key is set
#if not os.environ.get("API_KEY"):
    #raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show foods"""

    food = db.execute("SELECT id, food FROM menu");
    rows = food;

    for i in range(len(food)):
        rating = db.execute("SELECT AVG(rating) FROM ratings WHERE food_id = ?", str(food[i]['id']))
        number_of_ratings = len(db.execute("SELECT DISTINCT user_id FROM ratings WHERE food_id = ?", str(food[i]['id'])))
        print(number_of_ratings)
        my_rating = db.execute("SELECT rating FROM ratings WHERE user_id = ? and food_id = ?", session["user_id"], str(food[i]['id']))
        rows[i]['rating'] = rating[0]['AVG(rating)']
        rows[i]['number_of_ratings'] = number_of_ratings
        rows[i]['my_rating'] = my_rating[0]['rating']


    return render_template("index.html", rows=rows)

@app.route("/rate", methods=["GET", "POST"])
@login_required
def rate():
    """Rate foods"""
    if request.method == "POST":

        food = request.form.get("food")
        food_id = db.execute("SELECT id FROM menu WHERE food = ?", food)[0]['id']
        print(food_id)
        rating = request.form.get("rating")

        # should override if the user has already ranked this food
        if len(db.execute("SELECT * FROM ratings WHERE user_id = ? AND food_id = ?", session["user_id"], food_id)) > 0:
            db.execute("""
                UPDATE ratings
                SET rating = ?, ts = CURRENT_TIMESTAMP WHERE
                user_id = ? AND food_id = ?
                """,
                rating, session["user_id"], food_id);
        else:
            db.execute("""
                INSERT INTO ratings
                (user_id, food_id, rating, ts)
                VALUES
                (?, ?, ?, CURRENT_TIMESTAMP);
                """,
                session["user_id"], food_id, rating);

        return redirect("/", code=302)
    else:
        food = db.execute("SELECT id, food FROM menu");
        return render_template("rate.html", rows=food)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password.", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")




@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure passwords match
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("confirmation password must match", 400)

        # Ensure username does not exist

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) > 0:
            return apology("username already taken", 400)

        # Register user
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))

        # Remember which user has logged in
        #session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
