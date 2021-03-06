import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
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

        # Get a food's average rating across all users
        rating = db.execute("SELECT AVG(rating) FROM ratings WHERE food_id = ?", str(food[i]['id']))

        # Get the number of ratings for this food
        number_of_ratings = len(db.execute("SELECT DISTINCT user_id FROM ratings WHERE food_id = ?", str(food[i]['id'])))

        # Get the users' rating for this food
        my_rating = db.execute("SELECT rating FROM ratings WHERE user_id = ? and food_id = ?", session["user_id"], str(food[i]['id']))

        # Put all this information into a list of dictionaries

        if rating[0]['AVG(rating)'] != None:
            rows[i]['rating'] = round(rating[0]['AVG(rating)'], 2)
        else:
            rows[i]['rating'] = 0

        rows[i]['number_of_ratings'] = number_of_ratings
        if len(my_rating) > 0 and my_rating[0]['rating'] != None:
            rows[i]['my_rating'] = my_rating[0]['rating']
        else:
            rows[i]['my_rating'] = 0

        if rows[i]["rating"] != 0:
            rows[i]["rating_int"] = int(rows[i]['rating'])
        else:
            rows[i]["rating_int"] = 0

    # Sort by ranking

    sorted_rows = sorted(rows, key = lambda i: i['rating'], reverse=True)


    return render_template("index.html", rows=sorted_rows)

@app.route("/food/<food>", methods=["GET", "POST"])
@login_required
def food(food):
    """Show a food"""
    ingred = db.execute("SELECT class FROM menu WHERE food = ?", food)[0]['class']
    allergens = db.execute("SELECT ingredients FROM menu WHERE food = ?", food)[0]['ingredients']

    return render_template("food.html", food=food, ingred=ingred, allergens=allergens)

@app.route("/rate", methods=["GET", "POST"])
@login_required
def rate():
    """Rate foods"""
    if request.method == "POST":

        food = request.form.get("food")
        food_id = db.execute("SELECT id FROM menu WHERE food = ?", food)[0]['id']
        rating = request.form.get("rating")

        # Should update previous rating if the user has already ranked this food
        if len(db.execute("SELECT * FROM ratings WHERE user_id = ? AND food_id = ?", session["user_id"], food_id)) > 0:
            db.execute("""
                UPDATE ratings
                SET rating = ?, ts = CURRENT_TIMESTAMP WHERE
                user_id = ? AND food_id = ?
                """,
                rating, session["user_id"], food_id);
        else:
        # Add a new rating if user has not ranked this food
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
