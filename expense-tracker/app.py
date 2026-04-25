from flask import Flask, render_template, request, redirect, url_for, flash, session
from database.db import init_db, seed_db, setup_database, create_user, get_user_by_email, get_user_by_id
from werkzeug.security import check_password_hash

# -------------------------------------------------- #
# App Initialization
# -------------------------------------------------- #
app = Flask(__name__)
app.secret_key = "spendly-dev-secret-key-change-in-production"

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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not email or not password:
            flash("Please enter both email and password.")
            return render_template("login.html")

        user = get_user_by_email(email)

        if not user or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password.")
            return render_template("login.html")

        session["user_id"] = user["id"]
        flash(f"Welcome back, {user['username']}!")
        return redirect(url_for("profile"))

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
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("landing"))


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