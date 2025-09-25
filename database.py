import sqlite3
from datetime import datetime

DB_FILE = "studybuddy.db"

# ---------------------- Database Initialization ----------------------
def init_all_tables():
    """Initializes all necessary database tables if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # 1. Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    # Add default admin user if not exists (username: admin, password: admin123)
    cur.execute("INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)",
                ("admin", "8c6976e5b5410415bde908bd4dee15dfb16b1f77f64f63b8a46f8f7f0ee6c2ab"))  # SHA256 of "admin123"

    # 2. Summaries table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS summaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        original_text TEXT NOT NULL,
        summary_text TEXT NOT NULL,
        created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 3. Flashcards table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS flashcards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 4. Study logs table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS study_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        subject TEXT,
        duration_minutes INTEGER,
        started_at TIMESTAMP,
        created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 5. Exams table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS exams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        subject TEXT NOT NULL,
        exam_date TEXT NOT NULL,
        notes TEXT,
        difficulty TEXT,
        created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 6. Reports table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        report_name TEXT NOT NULL,
        report_data TEXT NOT NULL,
        created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 7. Feedback table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        message TEXT NOT NULL,
        rating INTEGER,
        created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# ---------------------- User Functions (fixed) ----------------------
def add_user(username, password_hash):
    """
    Add a new user to the database.
    Returns True if successful, False if username already exists.
    """
    init_all_tables()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_user(username):
    """
    Retrieve username and password_hash for login.
    Returns a tuple (username, password_hash) or None if user does not exist.
    """
    init_all_tables()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT username, password_hash FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()
    return user


# ---------------------- Other functions unchanged ----------------------
# (Summarizer, Flashcards, Study Tracker, Exams, Reports, Feedback)
# Keep all existing code for these features as in your previous database.py

# ---------------------- Initialize Tables on Import ----------------------
init_all_tables()
