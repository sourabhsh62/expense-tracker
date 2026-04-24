from flask import Flask, render_template
from database.db import init_db, seed_db, setup_database, create_user

# -------------------------------------------------- #
# App Initialization
# -------------------------------------------------- #
app = Flask(__name__)

# Initialize database
setup_database()


# -------------------------------------------------- #
# Routes
# -------------------------------------------------- #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# -------------------------------------------------- #
# Placeholder Routes (Future Features)
# -------------------------------------------------- #

@app.route("/logout")
def logout():
    return "Logout — coming soon"


@app.route("/profile")
def profile():
    return "Profile page — coming soon"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming soon"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return f"Edit expense {id} — coming soon"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return f"Delete expense {id} — coming soon"


# -------------------------------------------------- #
# Run App
# -------------------------------------------------- #
if __name__ == "__main__":
    app.run(debug=True, port=5001)