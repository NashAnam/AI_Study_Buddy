# main.py
import streamlit as st
from PIL import Image
import os

import database
from utils import hash_password, verify_password

# ------------------ Initialize Database ------------------
database.init_all_tables()

# ------------------ Session State ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "redirect_to_welcome" not in st.session_state:
    st.session_state.redirect_to_welcome = False

# ------------------ Banner ------------------
banner_path = os.path.join("assets", "banner.png")
if os.path.exists(banner_path):
    banner = Image.open(banner_path)
    st.image(banner, use_column_width=True)
else:
    st.warning("Banner image not found.")

# ------------------ Auth Functions ------------------
def register_user(username, password):
    password_hash = hash_password(password)
    success = database.add_user(username, password_hash)
    if success:
        st.success("✅ User registered successfully")
    else:
        st.error("❌ Username already exists")

def login_user(username, password):
    user = database.get_user(username)
    if user and verify_password(password, user[0]):
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.redirect_to_welcome = True
        st.success("✅ Login successful")
        st.rerun()
    else:
        st.error("❌ Invalid username or password")

# ------------------ Auth Page ------------------
def auth_page():
    st.title("🔐 AI Study Buddy Login / Registration")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            login_user(username, password)

    with tab2:
        new_user = st.text_input("New Username", key="reg_user")
        new_pass = st.text_input("New Password", type="password", key="reg_pass")
        if st.button("Register"):
            register_user(new_user, new_pass)

# ------------------ Main App Page ------------------
def main_app():
    st.title(f"📚 Welcome, {st.session_state.username}!")
    st.markdown("Use the sidebar to explore tools like **Summarizer**, **Flashcards**, **Exam Planner**, and more.")

    # Show sidebar
    st.sidebar.title("Menu")
    st.sidebar.write(f"Logged in as: {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.redirect_to_welcome = False
        st.rerun()

# ------------------ Access Control ------------------
if not st.session_state.logged_in:
    # Hide sidebar while not logged in
    st.markdown("""
        <style>
        [data-testid="stSidebar"] { display: none; }
        </style>
    """, unsafe_allow_html=True)
    auth_page()
else:
    if st.session_state.redirect_to_welcome:
        st.session_state.redirect_to_welcome = False
        st.switch_page("pages/1_Welcome.py")  # Redirect to your Welcome page
    else:
        main_app()
