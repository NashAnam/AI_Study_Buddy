# database.py

import sqlite3
import os
from datetime import datetime
import utils  # Import utils for password hashing

# Database file path - ensure it's in the same directory as the script
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "final_clean_db.sqlite")

# ---------------------- Database Initialization ----------------------
def init_all_tables():
    """Initializes all necessary database tables if they don't exist."""
    try:
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

        # Add default admin user with properly hashed password
        # Check if admin user already exists
        cur.execute("SELECT COUNT(*) FROM users WHERE username = ?", ("admin",))
        if cur.fetchone()[0] == 0:
            admin_hash = utils.hash_password("admin123")
            cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                        ("admin", admin_hash)) 
            print("Default admin user created: username=admin, password=admin123")

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
        print(f"Database initialized successfully at: {DB_FILE}")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        if 'conn' in locals():
            conn.close()


# ---------------------- User Functions ----------------------
def add_user(username, password_hash):
    """Add new user. Returns True if successful, False if username exists."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"User already exists: {e}")
        return False
    except Exception as e:
        print(f"Error adding user: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def get_user(username):
    """Get username and password_hash for given username"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT username, password_hash FROM users WHERE username = ?", (username.strip(),))
        user = cur.fetchone()
        return user  # returns (username, password_hash) or None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()


# ---------------------- Summarizer Functions ----------------------
def save_summary(username, original_text, summary_text):
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("INSERT INTO summaries (username, original_text, summary_text) VALUES (?, ?, ?)",
                    (username, original_text, summary_text))
        conn.commit()
    except Exception as e:
        print(f"Error saving summary: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def get_user_summaries(username):
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT original_text, summary_text, created_ts FROM summaries WHERE username = ?", (username,))
        summaries = cur.fetchall()
        return summaries
    except Exception as e:
        print(f"Error getting summaries: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()


# ---------------------- Flashcard Functions ----------------------
def save_flashcard(username, question, answer):
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("INSERT INTO flashcards (username, question, answer) VALUES (?, ?, ?)",
                    (username, question, answer))
        conn.commit()
    except Exception as e:
        print(f"Error saving flashcard: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def get_flashcards(username):
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT id, question, answer, created_ts FROM flashcards WHERE username = ?", (username,))
        flashcards = cur.fetchall()
        return flashcards
    except Exception as e:
        print(f"Error getting flashcards: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

def delete_flashcards(username, flashcard_ids):
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        placeholders = ','.join('?' for _ in flashcard_ids)
        cur.execute(f"DELETE FROM flashcards WHERE username = ? AND id IN ({placeholders})", (username, *flashcard_ids))
        conn.commit()
    except Exception as e:
        print(f"Error deleting flashcards: {e}")
    finally:
        if 'conn' in locals():
            conn.close()


# ---------------------- Study Tracker Functions ----------------------
def add_study_log(username, subject, duration, started_at):
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("INSERT INTO study_logs (username, subject, duration_minutes, started_at) VALUES (?, ?, ?, ?)",
                    (username, subject, duration, started_at))
        conn.commit()
    except Exception as e:
        print(f"Error adding study log: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def get_study_logs(username):
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT id, subject, duration_minutes, started_at, created_ts FROM study_logs WHERE username = ? ORDER BY started_at DESC", (username,))
        logs = cur.fetchall()
        return logs
    except Exception as e:
        print(f"Error getting study logs: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

def delete_study_logs(username, log_ids):
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        placeholders = ','.join('?' for _ in log_ids)
        cur.execute(f"DELETE FROM study_logs WHERE username = ? AND id IN ({placeholders})", (username, *log_ids))
        conn.commit()
    except Exception as e:
        print(f"Error deleting study logs: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def get_subjects(username):
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT subject FROM study_logs WHERE username = ? ORDER BY subject ASC", (username,))
        subjects = [row[0] for row in cur.fetchall()]
        return subjects
    except Exception as e:
        print(f"Error getting subjects: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()


# ---------------------- Exam Planner Functions ----------------------
def add_exam(username, subject, exam_date, notes, difficulty):
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("INSERT INTO exams (username, subject, exam_date, notes, difficulty) VALUES (?, ?, ?, ?, ?)",
                    (username, subject, exam_date, notes, difficulty))
        conn.commit()
    except Exception as e:
        print(f"Error adding exam: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def get_user_exams(username):
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT id, subject, exam_date, notes, difficulty FROM exams WHERE username = ?", (username,))
        exams = cur.fetchall()
        return exams
    except Exception as e:
        print(f"Error getting exams: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

def delete_exam(username, exam_id):
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("DELETE FROM exams WHERE username = ? AND id = ?", (username, exam_id))
        conn.commit()
    except Exception as e:
        print(f"Error deleting exam: {e}")
    finally:
        if 'conn' in locals():
            conn.close()


# ---------------------- Report Functions ----------------------
def save_report(username, report_name, report_data):
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("INSERT INTO reports (username, report_name, report_data) VALUES (?, ?, ?)",
                    (username, report_name, report_data))
        conn.commit()
    except Exception as e:
        print(f"Error saving report: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def get_reports(username):
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT id, report_name, created_ts, report_data FROM reports WHERE username = ? ORDER BY created_ts DESC", (username,))
        reports = cur.fetchall()
        return reports
    except Exception as e:
        print(f"Error getting reports: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

def get_report_by_id(report_id):
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT report_data FROM reports WHERE id = ?", (report_id,))
        report_data = cur.fetchone()
        return report_data[0] if report_data else None
    except Exception as e:
        print(f"Error getting report by id: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()


# ---------------------- Feedback Functions ----------------------
def save_feedback(username, message, rating):
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("INSERT INTO feedback (username, message, rating) VALUES (?, ?, ?)",
                    (username, message, rating))
        conn.commit()
    except Exception as e:
        print(f"Error saving feedback: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def get_feedback():
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT username, message, rating, created_ts FROM feedback ORDER BY created_ts DESC")
        feedback_data = cur.fetchall()
        return feedback_data
    except Exception as e:
        print(f"Error getting feedback: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()


# ---------------------- Initialize Tables on Import ----------------------
if __name__ == "__main__":
    # Only initialize when run directly
    init_all_tables()
else:
    # Initialize when imported
    init_all_tables()