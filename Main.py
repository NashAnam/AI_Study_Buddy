# main.py
# Run with: python -m streamlit run main.py

import streamlit as st
import json
import os
from PIL import Image

# Import database and initialize tables
import database
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



# --- Login Function ---
def login():
    st.title("🔐 Login to AI Study Buddy")
    st.markdown("Please enter your credentials to continue.")

    username = st.text_input("👤 Username", key="login_username")
    password = st.text_input("🔒 Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        try:
            # Use absolute path relative to main.py
            json_path = os.path.join(os.path.dirname(__file__), "users.json")
            with open(json_path, "r") as f:
                users = json.load(f)

            if username.strip() in users and password == users[username.strip()]["password"]:
                st.session_state.logged_in = True
                st.session_state.username = username.strip()
                st.session_state.redirect_to_welcome = True
                st.success("✅ Login successful")
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")
        except FileNotFoundError:
            st.error("⚠️ 'users.json' file not found.")
        except Exception as e:
            st.error(f"⚠️ Error reading users: {e}")

# --- Main UI ---
def show_main():
    st.title("📚 Welcome to AI Study Buddy")
    st.markdown("Use the sidebar to explore tools like **Summarizer**, **Flashcards**, **Exam Planner**, and more.")

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
        st.switch_page("pages/1_Welcome.py")
    else:
        show_main()
