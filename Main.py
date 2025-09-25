# Main.py
# Run with: streamlit run Main.py

import streamlit as st
import os
from PIL import Image
import database
import utils  # password hashing/verification

# --- Page Config ---
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="centered",
)

# --- Session State Initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "Welcome" 

# --- Show Banner ---
banner_path = os.path.join("assets", "banner.png")
if os.path.exists(banner_path):
    # Assuming 'assets/banner.png' exists in your directory
    try:
        banner = Image.open(banner_path)
        st.image(banner, use_container_width=True)
    except Exception:
        st.warning("Banner image found but could not be loaded. Check file integrity.")
else:
    st.warning("Banner image not found. Ensure 'assets/banner.png' exists.")

# --- Database Helper for Login ---
def get_user(username):
    """Fetch user from database for login."""
    return database.get_user(username.strip()) 

# --- Placeholder Functions for Study Buddy Tools ---
def show_summarizer():
    st.title("✨ Summarizer")
    st.info(f"Welcome, {st.session_state.username}. Start summarizing your notes!")

def show_flashcards():
    st.title("📝 Flashcards")
    st.info(f"Welcome, {st.session_state.username}. Create or review flashcards!")
    
def show_welcome():
    st.title("📚 Welcome to AI Study Buddy")
    st.markdown(f"""
        Hello, **{st.session_state.username}**! 👋
        
        Use the sidebar on the left to navigate and explore tools.
    """)

# --- Login Function (CLEANED) ---
def login():
    st.title("🔐 Login to AI Study Buddy")
    st.markdown("Please enter your credentials to continue.")

    username = st.text_input("👤 Username", key="login_username")
    password = st.text_input("🔒 Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        user = get_user(username)
        if user:
            stored_hash = user[1] 
            if utils.verify_password(password, stored_hash):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.current_page = "Welcome" 
                st.success("✅ Login successful")
                # No forced rerun needed!
            else:
                st.error("❌ Invalid username or password.")
        else:
            st.error("❌ Invalid username or password.")

# --- Main App Navigation ---
def main_app():
    # 1. Sidebar Navigation
    st.sidebar.title("🧭 Navigation")
    
    pages = {
        "Welcome": show_welcome,
        "✨ Summarizer": show_summarizer,
        "📝 Flashcards": show_flashcards,
        # Add other pages here
    }
    
    selected_page = st.sidebar.radio(
        "Select a tool",
        list(pages.keys()),
        index=list(pages.keys()).index(st.session_state.current_page) 
            if st.session_state.current_page in pages else 0
    )
    st.session_state.current_page = selected_page
    
    if st.sidebar.button("Logout", key="logout_button"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.current_page = "Welcome"
        st.success("You have been logged out.")
    
    st.sidebar.markdown("---")
    st.sidebar.text(f"Logged in as: {st.session_state.username}")
    
    # 2. Page Content Rendering
    pages[st.session_state.current_page]()


# --- Access Control ---
if not st.session_state.logged_in:
    # Hide sidebar while not logged in using CSS
    st.markdown("""
        <style>
        [data-testid="stSidebar"] { 
            display: none !important; 
        }
        </style>
    """, unsafe_allow_html=True)
    login()
else:
    main_app()