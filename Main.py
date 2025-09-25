# Main.py
# Run with: streamlit run Main.py

import streamlit as st
import os
import sqlite3
from PIL import Image
import database

# --- Initialize Database Tables ---
database.init_all_tables()

# --- Page Config ---
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Session State Initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "redirect_to_welcome" not in st.session_state:
    st.session_state.redirect_to_welcome = False

# --- Show Banner ---
banner_path = os.path.join("assets", "banner.png")
if os.path.exists(banner_path):
    banner = Image.open(banner_path)
    st.image(banner, use_column_width=True)
else:
    st.warning("Banner image not found.")

# --- Database Helper for Login ---
def check_user(username, password):
    conn = sqlite3.connect("studybuddy.db")
    cur = conn.cursor()

    # Ensure users table exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()

    # Check if user exists
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()
    conn.close()
    return user

# --- Login Function ---
def login():
    st.title("🔐 Login to AI Study Buddy")
    st.markdown("Please enter your credentials to continue.")

    username = st.text_input("👤 Username", key="login_username")
    password = st.text_input("🔒 Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        if check_user(username.strip(), password):
            st.session_state.logged_in = True
            st.session_state.username = username.strip()
            st.session_state.redirect_to_welcome = True
            st.success("✅ Login successful")
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")

    st.markdown("👉 New here? Please contact admin to create an account.")

# --- Welcome Page (after login) ---
def show_main():
    st.title("📚 Welcome to AI Study Buddy")
    st.markdown("""
        Use the sidebar to explore tools like:
        - ✨ Summarizer  
        - 📝 Flashcards  
        - 📅 Exam Planner  
        - 📊 Study Tracker  
        - 💬 Chatbot Tutor  
        - 🧩 Other study tools  

        Navigate using the sidebar on the left.
    """)

# --- Access Control ---
if not st.session_state.logged_in:
    # Hide sidebar while not logged in
    st.markdown("""
        <style>
        [data-testid="stSidebar"] { display: none; }
        </style>
    """, unsafe_allow_html=True)
    login()
else:
    if st.session_state.redirect_to_welcome:
        st.session_state.redirect_to_welcome = False
        show_main()
    else:
        show_main()
