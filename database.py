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
                ("admin", "8c6976e5b5410415bde908bd4dee15dfb16b1f77f64f63b8a46f8f7f0ee6c2ab"))  # SHA256 hash of "admin123"

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


# ---------------------- User Functions ----------------------
def add_user(username, password_hash):
    """Add new user. Returns True if successful, False if username exists."""
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
    """Get password hash for given username"""
    init_all_tables()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()
    return user  # Returns tuple (password_hash,) or None


# ---------------------- Summarizer Functions ----------------------
def save_summary(username, original_text, summary_text):
    init_all_tables()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO summaries (username, original_text, summary_text) VALUES (?, ?, ?)",
                (username, original_text, summary_text))
    conn.commit()
    conn.close()

def get_user_summaries(username):
    init_all_tables()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT original_text, summary_text, created_ts FROM summaries WHERE username = ?", (username,))
    summaries = cur.fetchall()
    conn.close()
    return summaries


# ---------------------- Flashcard Functions ----------------------
def save_flashcard(username, question, answer):
    init_all_tables()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO flashcards (username, question, answer) VALUES (?, ?, ?)",
                (username, question, answer))
    conn.commit()
    conn.close()

def get_flashcards(username):
    init_all_tables()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, question, answer, created_ts FROM flashcards WHERE username = ?", (username,))
    flashcards = cur.fetchall()
    conn.close()
    return flashcards

def delete_flashcards(username, flashcard_ids):
    init_all_tables()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    placeholders = ','.join('?' for _ in flashcard_ids)
    cur.execute(f"DELETE FROM flashcards WHERE username = ? AND id IN ({placeholders})", (username, *flashcard_ids))
    conn.commit()
    conn.close()


# ---------------------- Study Tracker Functions ----------------------
def add_study_log(username, subject, duration, started_at):
    init_all_tables()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO study_logs (username, subject, duration_minutes, started_at) VALUES (?, ?, ?, ?)",
                (username, subject, duration, started_at))
    conn.commit()
    conn.close()

def get_study_logs(username):
    init_all_tables()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, subject, duration_minutes, started_at, created_ts FROM study_logs WHERE username = ? ORDER BY started_at DESC", (username,))
    logs = cur.fetchall()
    conn.close()
    return logs

def delete_study_logs(username, log_ids):
    init_all_tables()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    placeholders = ','.join('?' for _ in log_ids)
    cur.execute(f"DELETE FROM study_logs WHERE username = ? AND id IN ({placeholders})", (username, *log_ids))
    conn.commit()
    conn.close()

def get_subjects(username):
    init_all_tables()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT subject FROM study_logs WHERE username = ? ORDER BY subject ASC", (username,))
    subjects = [row[0] for row in cur.fetchall()]
    conn.close()
    return subjects


# ---------------------- Exam Planner Functions ----------------------
def add_exam(username, subject, exam_date, notes, difficulty):
    init_all_tables()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO exams (username, subject, exam_date, notes, difficulty) VALUES (?, ?, ?, ?, ?)",
                (username, subject, exam_date, notes, difficulty))
    conn.commit()
    conn.close()

def get_user_exams(username):
    init_all_tables()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, subject, exam_date, notes, difficulty FROM exams WHERE username = ?", (username,))
    exams = cur.fetchall()
    conn.close()
    return exams

def delete_exam(username, exam_id):
    init_all_tables()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("DELETE FROM exams WHERE username = ? AND id = ?", (username, exam_id))
    conn.commit()
    conn.close()


# ---------------------- Report Functions ----------------------
def save_report(username, report_name, report_data):
    init_all_tables()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO reports (username, report_name, report_data) VALUES (?, ?, ?)",
                (username, report_name, report_data))
    conn.commit()
    conn.close()

def get_reports(username):
    init_all_tables()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, report_name, created_ts, report_data FROM reports WHERE username = ? ORDER BY created_ts DESC", (username,))
    reports = cur.fetchall()
    conn.close()
    return reports

def get_report_by_id(report_id):
    init_all_tables()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT report_data FROM reports WHERE id = ?", (report_id,))
    report_data = cur.fetchone()
    conn.close()
    return report_data[0] if report_data else None


# ---------------------- Feedback Functions ----------------------
def save_feedback(username, message, rating):
    init_all_tables()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO feedback (username, message, rating) VALUES (?, ?, ?)",
                (username, message, rating))
    conn.commit()
    conn.close()

def get_feedback():
    init_all_tables()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT username, message, rating, created_ts FROM feedback ORDER BY created_ts DESC")
    feedback_data = cur.fetchall()
    conn.close()
    return feedback_data


# ---------------------- Initialize Tables on Import ----------------------
init_all_tables()
