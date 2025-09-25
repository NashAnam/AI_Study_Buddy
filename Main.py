# Main.py
# Run with: streamlit run Main.py

import streamlit as st
import os
from PIL import Image
import database
import utils  # password hashing/verification

# --- Database Initialization (Called once on initial run) ---
# Note: This is already called at the end of database.py, but including it here for clarity.
# database.init_all_tables() 

# --- Page Config ---
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="centered",
    # Sidebar state will be managed by content
)

# --- Session State Initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Welcome" # Initialize a page state for navigation

# --- Show Banner ---
banner_path = os.path.join("assets", "banner.png")
if os.path.exists(banner_path):
    banner = Image.open(banner_path)
    st.image(banner, use_column_width=True)
else:
    st.warning("Banner image not found.")

# --- Database Helper for Login ---
def get_user(username):
    """Fetch user from database for login."""
    # Ensure database is initialized before fetching on first run
    return database.get_user(username.strip()) # returns (username, password_hash) or None

# --- Login Function ---
def login():
    st.title("🔐 Login to AI Study Buddy")
    st.markdown("Please enter your credentials to continue.")

    # Use callbacks for a cleaner state change, but direct check is also fine.
    # We will use the direct check as in the original code.
    username = st.text_input("👤 Username", key="login_username")
    password = st.text_input("🔒 Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        user = get_user(username)
        if user:
            stored_hash = user[1] # hashed password from DB
            if utils.verify_password(password, stored_hash):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.current_page = "Welcome" # Set initial page after login
                st.success("✅ Login successful")
                # No need for st.experimental_rerun(), Streamlit handles the refresh
                # and re-executes the script, hitting the 'else' block for main content.
            else:
                st.error("❌ Invalid username or password.")
        else:
            st.error("❌ User not found. Please contact admin to create an account.")

# --- Placeholder Functions for Study Buddy Tools ---
def show_summarizer():
    st.title("✨ Summarizer")
    st.info(f"Welcome, {st.session_state.username}. Start summarizing your notes!")

def show_flashcards():
    st.title("📝 Flashcards")
    st.info(f"Welcome, {st.session_state.username}. Create or review flashcards!")
    
# Add other tool functions (Exam Planner, Study Tracker, etc.) as placeholders
def show_welcome():
    st.title("📚 Welcome to AI Study Buddy")
    st.markdown(f"""
        Hello, **{st.session_state.username}**! 👋
        
        Use the sidebar on the left to navigate and explore tools like:
        - ✨ Summarizer  
        - 📝 Flashcards  
        - 📅 Exam Planner  
        - 📊 Study Tracker  
        - 💬 Chatbot Tutor  
        - 🧩 Other study tools  
    """)

# --- Main App Navigation (after login) ---
def main_app():
    # 1. Sidebar Navigation
    st.sidebar.title("🧭 Navigation")
    
    # Define pages
    pages = {
        "Welcome": show_welcome,
        "✨ Summarizer": show_summarizer,
        "📝 Flashcards": show_flashcards,
        # Add other pages here
        # "📅 Exam Planner": show_exam_planner,
        # "📊 Study Tracker": show_study_tracker,
    }
    
    # Create a radio button for navigation and update session state
    st.session_state.current_page = st.sidebar.radio(
        "Select a tool",
        list(pages.keys()),
        index=list(pages.keys()).index(st.session_state.current_page) if st.session_state.current_page in pages else 0
    )
    
    # Add a logout button to the sidebar
    if st.sidebar.button("Logout", key="logout_button"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.current_page = "Welcome"
        st.success("You have been logged out.")
        # Streamlit will re-execute the script, showing the login page.
    
    st.sidebar.markdown("---")
    st.sidebar.text(f"Logged in as: {st.session_state.username}")
    
    # 2. Page Content Rendering
    pages[st.session_state.current_page]()


# --- Access Control ---
if not st.session_state.logged_in:
    # Use the custom CSS to hide the sidebar when not logged in
    st.markdown("""
        <style>
        [data-testid="stSidebar"] { 
            display: none !important; 
        }
        </style>
    """, unsafe_allow_html=True)
    login()
else:
    # Sidebar is visible and main content is displayed
    # This structure correctly handles the entire application flow after login.
    main_app()