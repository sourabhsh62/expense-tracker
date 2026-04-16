#!/usr/bin/env python3
"""Seed realistic dummy expenses for a specific user."""

import random
from datetime import datetime, timedelta
from database.db import get_db

# Arguments
USER_ID = 2
COUNT = 5
MONTHS = 3

# Categories with Indian descriptions and amount ranges (₹)
CATEGORIES = {
    "Food": {"min": 50, "max": 800, "weight": 25, "descriptions": [
        "Grocery shopping", "Lunch at mess", "Dinner at restaurant",
        "Street food", "Tea and snacks", "Biryani order", "South Indian tiffin",
        "Fast food meal", "Home delivery", "Weekend feast"
    ]},
    "Transport": {"min": 20, "max": 500, "weight": 15, "descriptions": [
        "Auto fare", "Metro card recharge", "Bus pass", "Ola/Uber ride",
        "Fuel refill", "Bike maintenance", "Train ticket", "Taxi fare"
    ]},
    "Bills": {"min": 200, "max": 3000, "weight": 12, "descriptions": [
        "Electricity bill", "Internet broadband", "Mobile recharge",
        "DTH subscription", "Water bill", "Cooking gas refill", "Rent contribution"
    ]},
    "Health": {"min": 100, "max": 2000, "weight": 5, "descriptions": [
        "Doctor consultation", "Medicines", "Gym membership", "Health checkup",
        "Physiotherapy", "Dental visit", "Eye test and glasses"
    ]},
    "Entertainment": {"min": 100, "max": 1500, "weight": 8, "descriptions": [
        "Movie tickets", "Netflix subscription", "Concert entry",
        "Gaming subscription", "Book purchase", "Streaming services"
    ]},
    "Shopping": {"min": 200, "max": 5000, "weight": 12, "descriptions": [
        "Clothing purchase", "Electronics gadget", "Home decor",
        "Kitchen utensils", "Personal care items", "Furniture item"
    ]},
    "Other": {"min": 50, "max": 1000, "weight": 8, "descriptions": [
        "Donation", "Gift purchase", "Stationery", "Miscellaneous expense",
        "Emergency expense", "Small repair"
    ]},
}


def generate_expenses(user_id, count, months):
    """Generate expenses spread across the past months."""
    expenses = []

    # Build weighted category list for proportional distribution
    category_weights = []
    for cat_name, cat_data in CATEGORIES.items():
        category_weights.extend([cat_name] * cat_data["weight"])

    now = datetime.now()

    for _ in range(count):
        # Pick a random date within the past months
        days_ago = random.randint(0, months * 30)
        expense_date = (now - timedelta(days=days_ago)).strftime("%Y-%m-%d")

        # Pick category based on weights
        category = random.choice(category_weights)
        cat_data = CATEGORIES[category]

        # Generate random amount in range
        amount = round(random.uniform(cat_data["min"], cat_data["max"]), 2)

        # Pick random description
        description = random.choice(cat_data["descriptions"])

        expenses.append((user_id, amount, category, description, expense_date))

    return expenses


def insert_expenses(expenses):
    """Insert all expenses in a single transaction."""
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("BEGIN TRANSACTION")

        for expense in expenses:
            cursor.execute("""
                INSERT INTO expenses (user_id, amount, category, description, date)
                VALUES (?, ?, ?, ?, ?)
            """, expense)

        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error inserting expenses: {e}")
        return False
    finally:
        conn.close()


def main():
    # Generate expenses
    expenses = generate_expenses(USER_ID, COUNT, MONTHS)

    # Insert in single transaction
    success = insert_expenses(expenses)

    if not success:
        print("Failed to insert expenses due to error. All changes rolled back.")
        return

    # Get date range from inserted expenses
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*), MIN(date), MAX(date)
        FROM expenses
        WHERE user_id = ?
    """, (USER_ID,))
    row = cursor.fetchone()
    total_count = row[0]
    min_date = row[1]
    max_date = row[2]

    # Get sample of 5 records
    cursor.execute("""
        SELECT id, amount, category, description, date
        FROM expenses
        WHERE user_id = ?
        ORDER BY RANDOM()
        LIMIT 5
    """, (USER_ID,))
    samples = cursor.fetchall()
    conn.close()

    # Print confirmation
    print(f"\n{'='*50}")
    print(f"Successfully inserted {len(expenses)} expenses for user {USER_ID}")
    print(f"Date range: {min_date} to {max_date}")
    print(f"{'='*50}")
    print("\nSample records:")
    print(f"{'ID':<6} {'Amount (Rs)':<12} {'Category':<15} {'Date':<12} {'Description'}")
    print("-" * 70)
    for s in samples:
        print(f"{s[0]:<6} {s[1]:<12.2f} {s[2]:<15} {s[4]:<12} {s[3]}")


if __name__ == "__main__":
    main()
