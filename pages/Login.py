import streamlit as st
import json
import os

# Hide sidebar nav
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar (can skip if you want it only on Welcome page)
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

# Ensure session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

def login():
    st.title("🔐 Login to AI Study Buddy")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        # Load user credentials from users.json
        try:
            with open("users.json", "r") as f:
                users = json.load(f)
              # ✅ moved here after loading
        except Exception as e:
            st.error(f"⚠️ Failed to load user data: {e}")
            return

        if username.strip() in users and users[username.strip()]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username.strip()
            st.success("✅ Login successful")
            st.switch_page("pages/1_Welcome.py")
            return


        st.error("❌ Invalid credentials. Please try again.")


# Show login or redirect
if not st.session_state.logged_in:
    login()
else:
    st.switch_page("pages/1_Welcome.py")
