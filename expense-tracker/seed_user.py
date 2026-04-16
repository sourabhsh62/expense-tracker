#!/usr/bin/env python3
"""
Seed script to generate and insert a realistic random Indian user into the database.
"""

import sqlite3
import os
import random
from datetime import datetime
from werkzeug.security import generate_password_hash

# ------------------------------------------------------------------ #
# Database Configuration
# ------------------------------------------------------------------ #

DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database", "expense_tracker.db")


def get_db():
    """Return a SQLite connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ------------------------------------------------------------------ #
# Indian Names Data
# ------------------------------------------------------------------ #

# First names from various Indian regions/languages
FIRST_NAMES = [
    # North Indian (Hindi/Punjabi)
    "Rahul", "Amit", "Rajesh", "Vikram", "Suresh", "Rakesh", "Manoj", "Pradeep",
    "Priya", "Neha", "Pooja", "Ritu", "Sunita", "Anjali", "Deepika", "Kavita",
    # South Indian (Tamil/Telugu/Kannada/Malayalam)
    "Arjun", "Karthik", "Venkat", "Krishna", "Ravi", "Srinivas", "Madhav", "Gopal",
    "Lakshmi", "Meera", "Kavya", "Divya", "Swathi", "Anitha", "Revathi", "Padma",
    # East Indian (Bengali/Odia)
    "Sourav", "Debashish", "Arijit", "Siddhartha", "Prosenjit", "Anirban",
    "Sneha", "Raima", "Koena", "Sreelekha", "Moumita", "Tathagata",
    # West Indian (Gujarati/Marathi)
    "Chirag", "Parth", "Rohan", "Siddharth", "Pranav", "Atharva",
    "Trupti", "Sayali", " Rutuja", "Priyanka", "Swara", "Tejaswi",
    # Pan-India modern names
    "Aryan", "Aditya", "Rohan", "Karan", "Akash", "Vivek", "Nitin", "Abhishek",
    "Shruti", "Pallavi", "Simran", "Jasmine", "Isha", "Diya", "Kiara"
]

# Common Indian surnames from various communities
LAST_NAMES = [
    # North Indian
    "Sharma", "Verma", "Gupta", "Agarwal", "Singh", "Kumar", "Yadav", "Chauhan",
    "Malhotra", "Kapoor", "Bhatia", "Sethi", "Khanna", "Bansal", "Garg",
    # South Indian
    "Iyer", "Iyengar", "Menon", "Nair", "Reddy", "Rao", "Pillai", "Das",
    "Hegde", "Kulkarni", "Deshmukh", "Patil", "Shetty", "Bhat", "Kamath",
    # East Indian
    "Banerjee", "Chatterjee", "Ganguly", "Mukherjee", "Roy", "Das", "Bose",
    "Sengupta", "Mahapatra", "Pattnaik", "Joshi",
    # West Indian
    "Patel", "Shah", "Mehta", "Desai", "Joshi", "Kulkarni", "Pawar", "Jadhav",
    "Thakur", "Kale", "Deshpande",
    # Pan-India
    "Jain", "Saxena", "Sinha", "Pandey", "Tiwari", "Mishra", "Dubey", "Tripathi"
]


def generate_indian_name():
    """Generate a realistic Indian name."""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    return f"{first_name} {last_name}"


def generate_email(name):
    """
    Generate an email from the name with random 2-3 digit suffix.
    Example: 'Rahul Sharma' -> 'rahul.sharma91@gmail.com'
    """
    parts = name.lower().split()
    if len(parts) >= 2:
        first = parts[0]
        last = parts[-1]  # Use last part as surname
        number = random.randint(10, 999)
        return f"{first}.{last}{number}@gmail.com"
    else:
        # Fallback if name parsing fails
        number = random.randint(10, 999)
        return f"{name.lower().replace(' ', '')}{number}@gmail.com"


def email_exists(email):
    """Check if email already exists in the database."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def generate_unique_email(name, max_attempts=100):
    """Generate a unique email that doesn't exist in the database."""
    for _ in range(max_attempts):
        email = generate_email(name)
        if not email_exists(email):
            return email
        # Try with different number if email exists
        continue
    raise Exception(f"Could not generate unique email after {max_attempts} attempts")


def seed_user():
    """Generate and insert a random Indian user into the database."""
    # Generate name
    name = generate_indian_name()

    # Generate unique email
    email = generate_unique_email(name)

    # Hash password
    password_hash = generate_password_hash("password123")

    # Get current datetime
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert into database
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username, email, password_hash, created_at)
        VALUES (?, ?, ?, ?)
    """, (name, email, password_hash, created_at))

    conn.commit()

    # Get the inserted user's ID
    user_id = cursor.lastrowid

    conn.close()

    # Print confirmation
    print("=" * 50)
    print("User seeded successfully!")
    print("=" * 50)
    print(f"id: {user_id}")
    print(f"name: {name}")
    print(f"email: {email}")
    print("=" * 50)


if __name__ == "__main__":
    seed_user()
