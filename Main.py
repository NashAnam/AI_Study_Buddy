# Main.py
# Run with: streamlit run Main.py

import streamlit as st
import os
from PIL import Image
import database
import utils  # password hashing/verification

# --- Database Initialization (Ensures tables are set up once) ---
# Note: database.init_all_tables() is sufficient and is run when 'import database' runs.
# Keep this line if you prefer it here, but it's redundant if in database.py
# database.init_all_tables() 

# --- Page Config ---
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="centered",
    # initial_sidebar_state="collapsed" - Removed, we control visibility with CSS below
)

# --- Session State Initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
# State for which page is currently viewed, starts at Welcome
if "current_page" not in st.session_state:
    st.session_state.current_page = "Welcome" 

# --- Show Banner ---
banner_path = os.path.join("assets", "banner.png")
if os.path.exists(banner_path):
    # Check if the image path is correct, assuming an 'assets' folder
    # If the image is uploaded as a single file, you might need to adjust the path.
    # We will assume the path is correct for now.
    try:
        banner = Image.open(banner_path)
        st.image(banner, use_column_width=True)
    except FileNotFoundError:
        st.warning("Banner image not found in 'assets/banner.png'.")
else:
    st.warning("Banner image path not found.")

# --- Database Helper for Login ---
def get_user(username):
    """Fetch user from database for login."""
    # database.get_user returns (username, password_hash) or None
    return database.get_user(username.strip()) 

# --- Placeholder Functions for Study Buddy Tools ---
def show_summarizer():
    st.title("✨ Summarizer")
    st.info(f"Welcome, {st.session_state.username}. Start summarizing your notes!")

def show_flashcards():
    st.title("📝 Flashcards")
    st.info(f"Welcome, {st.session_state.username}. Create or review flashcards!")
    
# --- Welcome Page (after login) ---
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

# --- Login Function (FINAL FIX) ---
def login():
    st.title("🔐 Login to AI Study Buddy")
    st.markdown("Please enter your credentials to continue.")

    username = st.text_input("👤 Username", key="login_username")
    password = st.text_input("🔒 Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        user = get_user(username)
        # Check if user was found (user is not None)
        if user:
            # user is a tuple: (username, password_hash)
            stored_hash = user[1]  
            
            # --- CRITICAL: Call verification function ---
            if utils.verify_password(password, stored_hash):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.current_page = "Welcome" # Set initial page
                st.success("✅ Login successful")
                # NO st.experimental_rerun() here. Let Streamlit redraw the app.
            else:
                st.error("❌ Invalid username or password.")
        else:
            # This is hit if database.get_user returns None
            st.error("❌ Invalid username or password.")

# --- Main App Navigation ---
def main_app():
    # 1. Sidebar Navigation
    st.sidebar.title("🧭 Navigation")
    
    # Define pages and their functions
    pages = {
        "Welcome": show_welcome,
        "✨ Summarizer": show_summarizer,
        "📝 Flashcards": show_flashcards,
        # Add other pages here
    }
    
    # Create a radio button for navigation
    selected_page = st.sidebar.radio(
        "Select a tool",
        list(pages.keys()),
        # Use session state to manage selection
        index=list(pages.keys()).index(st.session_state.current_page) 
            if st.session_state.current_page in pages else 0
    )
    st.session_state.current_page = selected_page
    
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


# --- Access Control (FIXED) ---
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
    # After login, the main app takes over
    main_app()