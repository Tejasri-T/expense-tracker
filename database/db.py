"""Database layer for Spendly — SQLite implementation."""

import sqlite3
from datetime import date
from pathlib import Path
from werkzeug.security import generate_password_hash


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "expense_tracker.db"

CATEGORIES = (
    "Food",
    "Transport",
    "Bills",
    "Health",
    "Entertainment",
    "Shopping",
    "Other",
)


def get_db():
    """Return a SQLite connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create tables if they don't exist. Safe to call multiple times."""
    conn = get_db()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        conn.commit()
    finally:
        conn.close()


def seed_db():
    """Insert demo user and 8 sample expenses if database is empty."""
    conn = get_db()
    try:
        # Check if users table already has data
        user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if user_count > 0:
            return  # Already seeded

        # Insert demo user
        password_hash = generate_password_hash("demo123")
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", password_hash)
        )
        user_id = cursor.lastrowid

        # Build 8 sample expenses spread across current month (days 1-28 for validity)
        today = date.today()
        days = (2, 5, 8, 11, 14, 17, 21, 25)
        sample_expenses = [
            (user_id, 4500.0, "Bills", today.replace(day=days[0]).strftime("%Y-%m-%d"),
             "Electricity and water bill"),
            (user_id, 3200.0, "Food", today.replace(day=days[1]).strftime("%Y-%m-%d"),
             "Groceries and dining out"),
            (user_id, 2050.0, "Health", today.replace(day=days[2]).strftime("%Y-%m-%d"),
             "Pharmacy and checkup"),
            (user_id, 1800.0, "Transport", today.replace(day=days[3]).strftime("%Y-%m-%d"),
             "Metro and fuel"),
            (user_id, 1200.0, "Entertainment", today.replace(day=days[4]).strftime("%Y-%m-%d"),
             "Movie and streaming"),
            (user_id, 2800.0, "Shopping", today.replace(day=days[5]).strftime("%Y-%m-%d"),
             "Clothing and accessories"),
            (user_id, 950.0, "Other", today.replace(day=days[6]).strftime("%Y-%m-%d"),
             "Miscellaneous expenses"),
            (user_id, 1500.0, "Food", today.replace(day=days[7]).strftime("%Y-%m-%d"),
             "Weekend lunch and snacks"),
        ]

        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            sample_expenses
        )
        conn.commit()
    finally:
        conn.close()