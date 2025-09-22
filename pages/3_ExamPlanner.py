# pages/3_ExamPlanner.py

import streamlit as st
import pandas as pd
from datetime import datetime
from database import add_exam, get_user_exams

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(page_title="Study Tracker", page_icon="📊", layout="wide")

# --- Hide default sidebar navigation ---
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------- AUTH CHECK ----------------------
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please login to access this page.")
    st.stop()

# --- Sidebar ---
def custom_sidebar():
    st.sidebar.title("📚 AI Study Buddy")
    st.sidebar.page_link("pages/1_Welcome.py", label="🏠 Welcome")
    st.sidebar.page_link("pages/2_Summarizer.py", label="📝 Summarizer")
    st.sidebar.page_link("pages/3_ExamPlanner.py", label="📅 Exam Planner")
    st.sidebar.page_link("pages/4_StudyTracker.py", label="📊 Study Tracker")
    st.sidebar.page_link("pages/5_Flashcard.py", label="🧠 Flashcards")
    st.sidebar.page_link("pages/6_Report.py", label="📈 Report")
    st.sidebar.page_link("pages/7_FAQ.py", label="❓ FAQ")
    st.sidebar.page_link("pages/8_About.py", label="ℹ️ About")
    st.sidebar.page_link("pages/9_Feedback.py", label="💬 Feedback")
    st.sidebar.page_link("pages/Login.py", label="🔒 Logout")

# --- App Logic ---
def app():
    # Check login
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("⚠️ Please login to access this page.")
        st.stop()

    custom_sidebar()

    st.title("🗓️ Smart Exam Planner")
    st.markdown("Add your upcoming exams and get personalized revision schedules.")

    username = st.session_state.username

    # --- Form to Add Exam ---
    with st.form("exam_form"):
        subject = st.text_input("📚 Subject")
        date = st.date_input("📅 Exam Date")
        difficulty = st.slider("🔥 Difficulty (1 = easy, 5 = hard)", 1, 5, 3)
        notes = st.text_area("📝 Notes", "") # Added notes field
        submit = st.form_submit_button("Add Exam")

        if submit and subject:
            add_exam(username, subject, date.isoformat(), notes, difficulty)
            st.success(f"✅ Added exam: {subject} on {date}")
            st.rerun()

    # --- Show Upcoming Exams ---
    rows = get_user_exams(username)
    if rows:
        # Corrected column names to match the database query
        df = pd.DataFrame(rows, columns=["ID", "Subject", "Date", "Notes", "Difficulty"])
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        today = datetime.now().date()
        df["Days Left"] = df["Date"].apply(lambda d: (d - today).days)
        df = df[df["Days Left"] >= 0].sort_values("Days Left")

        st.subheader("📋 Your Upcoming Exams")
        st.dataframe(df)

        st.subheader("📆 Auto Revision Planner")
        for _, row in df.iterrows():
            subject = row["Subject"]
            days_left = row["Days Left"]
            # FIXED: Converted difficulty from string to integer
            difficulty = int(row["Difficulty"])
            exam_date = row["Date"]

            st.markdown(f"### 📘 {subject} ({exam_date})")
            if days_left == 0:
                st.warning("🛑 Exam is today! Use this day for review and rest.")
            elif days_left > 0:
                suggested_sessions = min(days_left, difficulty * 2)
                st.markdown(f"- ⏳ **{days_left} days left**")
                st.markdown(f"- 📌 **Suggested Plan:** {suggested_sessions} sessions of focused study.")
            else:
                st.info("✅ Exam completed.")
    else:
        st.info("No upcoming exams added yet.")

# --- Run App ---
if __name__ == "__main__":
    app()