import sqlite3
import os
import utils
import logging
from datetime import datetime, timedelta, date

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "study_buddy.sqlite")

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_all_tables():
    try:
        conn = get_db_connection()
        with conn:
            # Users
            conn.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                username TEXT UNIQUE NOT NULL, 
                password_hash TEXT NOT NULL, 
                created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
            
            # Tasks - Ensure all columns exist (Migration)
            conn.execute("""CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                username TEXT NOT NULL, 
                title TEXT NOT NULL, 
                subject TEXT, 
                due_date TIMESTAMP, 
                time_str TEXT,
                priority TEXT DEFAULT 'Medium', 
                completed BOOLEAN DEFAULT 0,
                created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
            
            # Migration: Add columns if they don't exist
            try:
                conn.execute("ALTER TABLE tasks ADD COLUMN time_str TEXT")
            except: pass
            try:
                conn.execute("ALTER TABLE tasks ADD COLUMN completed BOOLEAN DEFAULT 0")
            except: pass
            try:
                conn.execute("ALTER TABLE tasks ADD COLUMN created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            except: pass

            # Summaries
            conn.execute("""CREATE TABLE IF NOT EXISTS summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                username TEXT NOT NULL, 
                title TEXT,
                original_text TEXT, 
                summary_text TEXT, 
                created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
            
            # Migration for summaries
            summary_cols = ["title", "original_text", "summary_text", "created_ts"]
            for col in summary_cols:
                try:
                    conn.execute(f"ALTER TABLE summaries ADD COLUMN {col} TEXT")
                except: pass
            
            # Study Logs
            conn.execute("""CREATE TABLE IF NOT EXISTS study_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                username TEXT NOT NULL, 
                subject TEXT, 
                duration_minutes INTEGER, 
                started_at TIMESTAMP, 
                created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")

            # Create Admin
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
            if cur.fetchone()[0] == 0:
                conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                             ("admin", utils.hash_password("admin123")))
        conn.close()
    except Exception as e:
        logger.error(f"Init Error: {e}")

# --- User Auth ---
def add_user(username, password_hash):
    try:
        conn = get_db_connection()
        with conn:
            conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.close()
        return True
    except: return False

def get_user(username):
    try:
        conn = get_db_connection()
        user = conn.execute("SELECT username, password_hash FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        return user
    except: return None

# --- Task Management ---
def add_task(username, title, subject, due_date, time_str, priority):
    try:
        # Convert date to string if it's an object
        if hasattr(due_date, 'isoformat'):
            due_date = due_date.isoformat()
            
        conn = get_db_connection()
        with conn:
            conn.execute(
                "INSERT INTO tasks (username, title, subject, due_date, time_str, priority, completed) VALUES (?, ?, ?, ?, ?, ?, 0)",
                (username, title, subject, due_date, time_str, priority)
            )
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Add Task Error: {e}")
        return False

def get_tasks(username):
    try:
        conn = get_db_connection()
        tasks = conn.execute("SELECT * FROM tasks WHERE username = ? ORDER BY due_date ASC", (username,)).fetchall()
        conn.close()
        return tasks
    except: return []

def get_todays_tasks(username):
    try:
        tasks = get_tasks(username)
        today_str = date.today().isoformat()
        # Filter for tasks due today or previously overdue & not completed? 
        # For dashboard "Today's Schedule", usually strictly today.
        filtered = []
        for t in tasks:
            # Handle due_date being potentially date object or string? 
            # Sqlite returns string usually.
            d_val = t['due_date']
            if not d_val: continue
            # If d_val is full timestamp string "2026-02-02 00:00:00" or date "2026-02-02"
            if str(d_val).startswith(today_str):
                filtered.append(t)
        return filtered
    except Exception as e:
        logger.error(f"Todays Tasks Error: {e}")
        return []

def update_task_status(task_id, completed):
    try:
        conn = get_db_connection()
        with conn:
            conn.execute("UPDATE tasks SET completed = ? WHERE id = ?", (1 if completed else 0, task_id))
        conn.close()
        return True
    except: return False

def delete_task(task_id):
    try:
        conn = get_db_connection()
        with conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.close()
        return True
    except: return False

# --- Summaries ---
def add_summary(username, original, summary, title=None):
    if not title:
        title = original[:40] + "..." if len(original) > 40 else original
    try:
        conn = get_db_connection()
        with conn:
             conn.execute("INSERT INTO summaries (username, title, original_text, summary_text) VALUES (?, ?, ?, ?)",
                          (username, title, original, summary))
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Add Summary Database Error: {e}")
        return False

def get_summaries(username):
    try:
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM summaries WHERE username = ? ORDER BY created_ts DESC", (username,)).fetchall()
        conn.close()
        return rows
    except: return []

def delete_summary(summary_id):
    try:
        conn = get_db_connection()
        with conn:
            conn.execute("DELETE FROM summaries WHERE id = ?", (summary_id,))
        conn.close()
        return True
    except: return False

def delete_all_summaries(username):
    try:
        conn = get_db_connection()
        with conn:
            conn.execute("DELETE FROM summaries WHERE username = ?", (username,))
        conn.close()
        return True
    except: return False

# --- Study Logs & Stats ---
def add_study_log(username, subject, duration_minutes):
    try:
        conn = get_db_connection()
        with conn:
            conn.execute("INSERT INTO study_logs (username, subject, duration_minutes, started_at) VALUES (?, ?, ?, ?)",
                         (username, subject, duration_minutes, datetime.now()))
        conn.close()
        return True
    except: return False

def get_user_stats(username):
    stats = {
        'streak': 0, 
        'total_hours': 0.0, 
        'hours_week': 0.0, 
        'topics_mastered': 0,
        'daily_goal_pct': 0
    }
    try:
        conn = get_db_connection()
        
        # Total Hours
        rows = conn.execute("SELECT sum(duration_minutes) FROM study_logs WHERE username = ?", (username,)).fetchone()
        if rows and rows[0]:
            stats['total_hours'] = round(rows[0] / 60.0, 1)

        # Weekly Hours
        # Calculate start of week (Monday)
        today = date.today()
        start_week = today - timedelta(days=today.weekday())
        rows = conn.execute("SELECT sum(duration_minutes) FROM study_logs WHERE username = ? AND date(started_at) >= ?", 
                            (username, start_week.isoformat())).fetchone()
        if rows and rows[0]:
            stats['hours_week'] = round(rows[0] / 60.0, 1)
            
        # Topics (Distinct Subjects)
        rows = conn.execute("SELECT count(DISTINCT subject) FROM study_logs WHERE username = ?", (username,)).fetchone()
        if rows:
            stats['topics_mastered'] = rows[0]

        # Streak Calculation
        rows = conn.execute("SELECT DISTINCT date(started_at) as dt FROM study_logs WHERE username = ? ORDER BY dt DESC", (username,)).fetchall()
        dates = [r['dt'] for r in rows if r['dt']]
        
        streak = 0
        if dates:
            # Check if updated today or yesterday to keep streak alive
            today_str = today.isoformat()
            yesterday_str = (today - timedelta(days=1)).isoformat()
            
            current_check = today
            if today_str not in dates and yesterday_str in dates:
                current_check = today - timedelta(days=1)
                
            # Iterate backwards
            # Simple logic: consecutive days
            # Actually, robust logic:
            if dates[0] == today_str or dates[0] == yesterday_str:
                streak = 1
                curr_date = date.fromisoformat(dates[0])
                for d_str in dates[1:]:
                    d = date.fromisoformat(d_str)
                    if (curr_date - d).days == 1:
                        streak += 1
                        curr_date = d
                    else:
                        break
        stats['streak'] = streak

        # Daily Goal %
        # Goal: 60 mins
        rows = conn.execute("SELECT sum(duration_minutes) FROM study_logs WHERE username = ? AND date(started_at) = ?", 
                            (username, today.isoformat())).fetchone()
        today_mins = rows[0] if rows and rows[0] else 0
        stats['daily_goal_pct'] = min(int((today_mins / 60) * 100), 100)

        conn.close()
    except Exception as e:
        logger.error(f"Stats Error: {e}")
        
    return stats

def get_tasks_this_week(username):
    try:
        conn = get_db_connection()
        today = date.today()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)
        
        rows = conn.execute("""
            SELECT count(*) FROM tasks 
            WHERE username = ? 
            AND date(due_date) >= ? 
            AND date(due_date) <= ?
        """, (username, start_week.isoformat(), end_week.isoformat())).fetchone()
        count = rows[0] if rows else 0
        conn.close()
        return count
    except Exception as e:
        logger.error(f"Weekly Tasks Error: {e}")
        return 0

def get_weekly_activity(username):
    # Returns last 7 days activity
    activity = []
    try:
        conn = get_db_connection()
        today = date.today()
        # Last 7 days including today
        for i in range(6, -1, -1):
            d = today - timedelta(days=i)
            rows = conn.execute("SELECT sum(duration_minutes) FROM study_logs WHERE username = ? AND date(started_at) = ?", 
                                (username, d.isoformat())).fetchone()
            mins = rows[0] if rows and rows[0] else 0
            day_label = d.strftime("%a") # Mon, Tue...
            activity.append({'day': day_label, 'hours': round(mins/60.0, 1)})
        conn.close()
    except: pass
    return activity
