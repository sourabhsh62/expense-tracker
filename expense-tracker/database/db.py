import sqlite3
import os

# ------------------------------------------------------------------ #
# Database Configuration
# ------------------------------------------------------------------ #

# Database file path - stored in the database directory
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expense_tracker.db")


# ------------------------------------------------------------------ #
# Database Connection
# ------------------------------------------------------------------ #

def get_db():
    """
    Return a SQLite connection with row_factory and foreign keys enabled.

    Returns:
        sqlite3.Connection: Database connection with Row factory enabled
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
    conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key support
    return conn


# ------------------------------------------------------------------ #
# Database Initialization
# ------------------------------------------------------------------ #

def init_db():
    """
    Create all tables using CREATE TABLE IF NOT EXISTS.

    Creates:
        - users table: Stores user account information
        - expenses table: Stores expense records linked to users
    """
    conn = get_db()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


# ------------------------------------------------------------------ #
# Database Seeding
# ------------------------------------------------------------------ #

def seed_db():
    """
    Insert sample data for development.

    Uses INSERT OR IGNORE to avoid duplicates on re-runs.
    """
    conn = get_db()
    cursor = conn.cursor()

    # Sample users
    sample_users = [
        ("alice", "alice@example.com", "hashed_password_alice"),
        ("bob", "bob@example.com", "hashed_password_bob"),
        ("charlie", "charlie@example.com", "hashed_password_charlie"),
    ]

    for username, email, password_hash in sample_users:
        cursor.execute("""
            INSERT OR IGNORE INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        """, (username, email, password_hash))

    # Sample expenses (will link to user_id 1, 2, 3)
    sample_expenses = [
        (1, 50.00, "Food", "Grocery shopping", "2026-04-01"),
        (1, 120.00, "Utilities", "Electric bill", "2026-04-05"),
        (1, 15.99, "Food", "Coffee and snacks", "2026-04-08"),
        (2, 200.00, "Transport", "Car maintenance", "2026-04-02"),
        (2, 45.00, "Entertainment", "Movie tickets", "2026-04-10"),
        (2, 80.00, "Food", "Dinner out", "2026-04-11"),
        (3, 35.50, "Food", "Lunch meetings", "2026-04-03"),
        (3, 150.00, "Shopping", "New shoes", "2026-04-07"),
        (3, 25.00, "Transport", "Bus pass", "2026-04-09"),
        (3, 60.00, "Utilities", "Internet bill", "2026-04-12"),
    ]

    for user_id, amount, category, description, date in sample_expenses:
        cursor.execute("""
            INSERT OR IGNORE INTO expenses (user_id, amount, category, description, date)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, amount, category, description, date))

    conn.commit()
    conn.close()


# ------------------------------------------------------------------ #
# Helper function to initialize and seed in one call
# ------------------------------------------------------------------ #

def setup_database():
    """
    Initialize and seed the database in one call.
    Convenience function for application startup.
    """
    init_db()
    seed_db()
