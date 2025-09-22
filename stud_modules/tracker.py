# stud_modules/tracker.py
import pandas as pd
import os
from datetime import datetime

DATA_FILE = "data/study_log.csv"

# Initialize CSV
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Subject", "Hours", "Date", "Start", "End", "Duration (mins)"])
    df.to_csv(DATA_FILE, index=False)

def log_study(subject, hours=None, date=None, start=None, end=None, duration=None):
    df = pd.read_csv(DATA_FILE)
    new_row = {
        "Subject": subject,
        "Hours": round(duration / 60, 2) if duration else hours,
        "Date": date if date else datetime.now().date(),
        "Start": start.strftime("%H:%M") if hasattr(start, 'strftime') else start,
        "End": end.strftime("%H:%M") if hasattr(end, 'strftime') else end,
        "Duration (mins)": round(duration, 2) if duration else ""
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

def get_study_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Subject", "Hours", "Date", "Start", "End", "Duration (mins)"])

def delete_logs(indices):
    df = pd.read_csv(DATA_FILE)
    df.drop(indices, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv(DATA_FILE, index=False)
