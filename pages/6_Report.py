import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from database import get_study_logs
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="📈 Study Report", layout="wide")

# --- HIDE DEFAULT SIDEBAR NAVIGATION ---
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# --- CUSTOM SIDEBAR ---
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

custom_sidebar()

# --- AUTH CHECK ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first to access this page.")
    st.stop()

# --- TITLE ---
st.title("📈 Study Performance Report")
st.markdown("A real-time summary of your study activity with key insights and trends.")
st.markdown("---")

username = st.session_state.username

# --- FETCH REAL STUDY DATA ---
logs = get_study_logs(username)

if not logs:
    st.info("No study data available yet. Start tracking sessions to see your report.")
    st.stop()

# --- PREPROCESSING ---
df = pd.DataFrame(logs, columns=["ID", "Subject", "Duration (mins)", "Started At", "Created At"])
df['Date'] = pd.to_datetime(df['Started At']).dt.date
df['Duration (mins)'] = pd.to_numeric(df['Duration (mins)'], errors='coerce')
df = df.dropna(subset=['Duration (mins)'])

# --- KPIs ---
total_sessions = len(df)
total_hours = df['Duration (mins)'].sum() / 60
avg_duration = df['Duration (mins)'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("📚 Total Sessions", total_sessions)
col2.metric("⏱️ Total Study Hours", f"{total_hours:.2f} hrs")
col3.metric("📏 Avg. Session Duration", f"{avg_duration:.1f} mins")

# --- DAILY SUMMARY TABLE ---
st.subheader("📅 Daily Summary")
daily_summary = df.groupby(['Date', 'Subject'])['Duration (mins)'].sum().reset_index()
daily_pivot = daily_summary.pivot(index="Date", columns="Subject", values="Duration (mins)").fillna(0)
st.dataframe(daily_pivot.style.format("{:.1f}"), use_container_width=True)

# --- VISUALIZATION ---
st.subheader("📊 Visual Insights")

line1, line2 = st.columns(2)

with line1:
    st.markdown("**Study Duration Over Time**")
    fig1, ax1 = plt.subplots()
    sns.lineplot(data=daily_summary, x="Date", y="Duration (mins)", hue="Subject", marker="o", ax=ax1)
    ax1.set_ylabel("Minutes")
    ax1.set_title("Daily Study Time by Subject")
    plt.xticks(rotation=30)
    st.pyplot(fig1)

with line2:
    st.markdown("**Time Spent by Subject**")
    subject_summary = df.groupby("Subject")["Duration (mins)"].sum().reset_index()
    fig2, ax2 = plt.subplots()
    sns.barplot(data=subject_summary, x="Subject", y="Duration (mins)", palette="Set2", ax=ax2)
    ax2.set_ylabel("Total Minutes")
    ax2.set_title("Total Study Time per Subject")
    st.pyplot(fig2)

# --- OPTIONAL EXPORT ---
st.markdown("📤 Export Your Data")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", data=csv, file_name='study_report.csv', mime='text/csv')

# --- FOOTER ---
st.markdown("---")
st.markdown("📘 *AI Study Buddy – Real-time Study Tracking Powered by Data*")