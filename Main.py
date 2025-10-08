# Main.py
# Run with: streamlit run Main.py

import streamlit as st
import os
from PIL import Image
import database
import utils

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

# --- Sidebar Functions ---
def hide_default_sidebar():
    """Hide the default Streamlit sidebar navigation"""
    st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

def custom_sidebar():
    """Create custom sidebar with navigation links"""
    hide_default_sidebar()
    
    st.sidebar.title("📚 AI Study Buddy")
    st.sidebar.markdown("---")
    
    # User info
    if "username" in st.session_state and st.session_state.username:
        st.sidebar.markdown(f"**👤 {st.session_state.username}**")
        st.sidebar.markdown("---")
    
    # Navigation links
    st.sidebar.page_link("pages/1_Welcome.py", label="🏠 Welcome")
    st.sidebar.page_link("pages/2_Summarizer.py", label="📝 Summarizer")
    st.sidebar.page_link("pages/3_ExamPlanner.py", label="📅 Exam Planner")
    st.sidebar.page_link("pages/4_StudyTracker.py", label="📊 Study Tracker")
    st.sidebar.page_link("pages/5_Flashcard.py", label="🧠 Flashcards")
    st.sidebar.page_link("pages/6_Report.py", label="📈 Report")
    st.sidebar.page_link("pages/7_FAQ.py", label="❓ FAQ")
    st.sidebar.page_link("pages/8_About.py", label="ℹ️ About")
    st.sidebar.page_link("pages/9_Feedback.py", label="💬 Feedback")
    
    st.sidebar.markdown("---")
    
    # Logout button
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.success("👋 You have been logged out.")
        st.switch_page("Main.py")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("💡 **Tips:**")
    st.sidebar.markdown("- Use the navigation above")
    st.sidebar.markdown("- Your data is auto-saved")
    st.sidebar.markdown("- Happy studying! 🎓")

def check_authentication():
    """Check if user is logged in, redirect to main if not"""
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("⚠️ Please login first to access this page.")
        st.stop()

# --- Show Banner ---
def show_banner():
    banner_path = os.path.join("assets", "banner.png")
    if os.path.exists(banner_path):
        try:
            banner = Image.open(banner_path)
            st.image(banner, use_container_width=True)
        except Exception as e:
            st.info("📚 AI Study Buddy - Your Learning Companion")
    else:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 20px;'>
            <h1>📚 AI Study Buddy</h1>
            <p>Your Personal Learning Companion</p>
        </div>
        """, unsafe_allow_html=True)

# --- Login Function ---
def login():
    st.title("🔐 Login to AI Study Buddy")
    st.markdown("Please enter your credentials to continue.")
    
    with st.expander("ℹ️ Default Login Credentials"):
        st.info("Default username: **admin**\nDefault password: **admin123**")

    username = st.text_input("👤 Username", key="login_username")
    password = st.text_input("🔑 Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        if not username.strip():
            st.error("⚠️ Please enter a username.")
            return
        
        if not password:
            st.error("⚠️ Please enter a password.")
            return
        
        user = database.get_user(username.strip())
        if user:
            stored_username, stored_hash = user
            
            if utils.verify_password(password, stored_hash):
                st.session_state.logged_in = True
                st.session_state.username = username.strip()
                st.success("🎉 Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Invalid password.")
        else:
            st.error("❌ User not found.")

# --- Registration Function ---
def show_register():
    st.title("📝 Register New User")
    st.markdown("Create a new account to access AI Study Buddy.")
    
    new_username = st.text_input("👤 New Username", key="reg_username")
    new_password = st.text_input("🔑 New Password", type="password", key="reg_password")
    confirm_password = st.text_input("🔑 Confirm Password", type="password", key="reg_confirm")
    
    if st.button("Register", key="register_button"):
        if not new_username.strip():
            st.error("⚠️ Please enter a username.")
            return
        
        if len(new_password) < 6:
            st.error("⚠️ Password must be at least 6 characters long.")
            return
            
        if new_password != confirm_password:
            st.error("⚠️ Passwords do not match.")
            return
        
        hashed_password = utils.hash_password(new_password)
        if database.add_user(new_username.strip(), hashed_password):
            st.success("✅ Registration successful! You can now log in.")
        else:
            st.error("❌ Username already exists. Please choose a different username.")

# --- Pre-login Options ---
def pre_login_navigation():
    st.sidebar.title("🚀 Get Started")
    
    auth_option = st.sidebar.radio(
        "Choose an option:",
        ["🔐 Login", "📝 Register"]
    )
    
    if auth_option == "🔐 Login":
        login()
    else:
        show_register()

# --- Main Application Logic ---
def main():
    show_banner()
    
    try:
        database.init_all_tables()
    except Exception as e:
        st.error(f"Database initialization failed: {e}")
        st.stop()
    
    if not st.session_state.logged_in:
        pre_login_navigation()
    else:
        # Redirect to Welcome page after login
        st.switch_page("pages/1_Welcome.py")

if __name__ == "__main__":
    main()