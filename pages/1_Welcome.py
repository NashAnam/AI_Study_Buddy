import streamlit as st
import json
import os 

st.set_page_config(page_title="Welcome", page_icon="👋")

# Hide default sidebar
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

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


    if st.sidebar.button("🔒 Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("✅ Logged out successfully!")
        st.switch_page("pages/Login.py")

# Ensure session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- Main Content ---
def app():
    if not st.session_state.get("logged_in", False):
        st.warning("🔒 Please login to access this page.")
        st.switch_page("pages/Login.py")
        return

    custom_sidebar()

    st.title("👋 Welcome to AI Study Buddy!")

    st.markdown("""
        <style>
            .big-font { font-size:28px !important; font-weight:600; }
            .subtle-text { font-size:18px; color: #555; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f'<p class="big-font">Hello, {st.session_state.username.title()}!</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtle-text">You’re now logged in and ready to explore your personal AI-powered academic assistant.</p>', unsafe_allow_html=True)

    st.success("✅ Login successful. Explore the tools using the sidebar!")

    st.subheader("📌 What would you like to do today?")
    st.markdown("📄 Summarize Notes or Documents")
    st.markdown("🧠 Auto-generate Flashcards")
    st.markdown("🗓️ Plan Your Exam Preparation")
    st.markdown("📊 Track Your Study Progress")

    st.markdown("---")
    st.info("“The expert in anything was once a beginner.” – Helen Hayes")

if __name__ == "__main__":
    app()
