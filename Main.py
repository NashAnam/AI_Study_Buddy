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
def show_banner():
    banner_path = os.path.join("assets", "banner.png")
    if os.path.exists(banner_path):
        try:
            banner = Image.open(banner_path)
            st.image(banner, use_container_width=True)
        except Exception as e:
            st.info("📚 AI Study Buddy - Your Learning Companion")
    else:
        # Show a nice header instead of warning
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 20px;'>
            <h1>📚 AI Study Buddy</h1>
            <p>Your Personal Learning Companion</p>
        </div>
        """, unsafe_allow_html=True)

# --- Placeholder Functions for Study Buddy Tools ---
def show_summarizer():
    st.title("✨ Summarizer")
    st.info(f"Welcome, {st.session_state.username}. Start summarizing your notes!")
    
    # Add a simple text area for demonstration
    text_input = st.text_area("Enter text to summarize:", height=200)
    if st.button("Generate Summary"):
        if text_input.strip():
            # Simple mock summary (you can integrate actual AI here)
            summary = f"Summary: {text_input[:100]}..." if len(text_input) > 100 else f"Summary: {text_input}"
            st.success("Summary generated!")
            st.write(summary)
            # Save to database
            database.save_summary(st.session_state.username, text_input, summary)
        else:
            st.warning("Please enter some text to summarize.")

def show_flashcards():
    st.title("🃏 Flashcards")
    st.info(f"Welcome, {st.session_state.username}. Create or review flashcards!")
    
    # Create new flashcard
    st.subheader("Create New Flashcard")
    question = st.text_input("Question:")
    answer = st.text_area("Answer:")
    
    if st.button("Add Flashcard"):
        if question.strip() and answer.strip():
            database.save_flashcard(st.session_state.username, question, answer)
            st.success("Flashcard added successfully!")
        else:
            st.warning("Please enter both question and answer.")
    
    # Show existing flashcards
    st.subheader("Your Flashcards")
    flashcards = database.get_flashcards(st.session_state.username)
    if flashcards:
        for i, (card_id, q, a, created_ts) in enumerate(flashcards):
            with st.expander(f"Card {i+1}: {q[:50]}..."):
                st.write(f"**Question:** {q}")
                st.write(f"**Answer:** {a}")
                st.write(f"**Created:** {created_ts}")
    else:
        st.info("No flashcards yet. Create your first one above!")
    
def show_welcome():
    st.title("📚 Welcome to AI Study Buddy")
    st.markdown(f"""
        Hello, **{st.session_state.username}**! 👋
        
        Welcome to your personalized learning companion. Here's what you can do:
        
        - **✨ Summarizer**: Quickly summarize your study materials
        - **🃏 Flashcards**: Create and review flashcards for better retention
        - **📊 Study Tracker**: Track your study sessions (coming soon)
        - **📝 Exam Planner**: Plan and manage your upcoming exams (coming soon)
        
        Use the sidebar on the left to navigate between tools and start your learning journey!
        
        ### Getting Started
        1. Click on **Summarizer** to start summarizing your notes
        2. Use **Flashcards** to create study cards
        3. Explore other features as they become available
        
        Happy studying! 🎓
    """)

# --- Login Function ---
def login():
    st.title("🔐 Login to AI Study Buddy")
    st.markdown("Please enter your credentials to continue.")
    
    # Add info about default credentials
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
        
        # Debug information
        st.info("🔍 Checking credentials...")
        
        user = database.get_user(username.strip())
        if user:
            stored_username, stored_hash = user
            st.success(f"✅ User found: {stored_username}")
            
            # Verify password
            if utils.verify_password(password, stored_hash):
                st.session_state.logged_in = True
                st.session_state.username = username.strip()
                st.session_state.current_page = "Welcome" 
                st.success("🎉 Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Invalid password.")
                # Debug hash comparison
                with st.expander("🔧 Debug Info"):
                    st.write(f"Input password hash: {utils.hash_password(password)}")
                    st.write(f"Stored hash: {stored_hash}")
        else:
            st.error("❌ User not found.")
            
            # Show available users for debugging
            with st.expander("🔧 Debug: Available Users"):
                try:
                    import sqlite3
                    conn = sqlite3.connect(database.DB_FILE)
                    cur = conn.cursor()
                    cur.execute("SELECT username FROM users")
                    users = cur.fetchall()
                    conn.close()
                    st.write("Available users:", [u[0] for u in users])
                except Exception as e:
                    st.write(f"Error checking users: {e}")

# --- Registration Function (Optional) ---
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
        
        # Hash password and save user
        hashed_password = utils.hash_password(new_password)
        if database.add_user(new_username.strip(), hashed_password):
            st.success("✅ Registration successful! You can now log in.")
        else:
            st.error("❌ Username already exists. Please choose a different username.")

# --- Main App Navigation ---
def main_app():
    # 1. Sidebar Navigation
    st.sidebar.title("🧭 Navigation")
    
    pages = {
        "Welcome": show_welcome,
        "✨ Summarizer": show_summarizer,
        "🃏 Flashcards": show_flashcards,
        # Add other pages here
    }
    
    selected_page = st.sidebar.radio(
        "Select a tool",
        list(pages.keys()),
        index=list(pages.keys()).index(st.session_state.current_page) 
            if st.session_state.current_page in pages else 0
    )
    st.session_state.current_page = selected_page
    
    # Logout button
    if st.sidebar.button("🚪 Logout", key="logout_button"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.current_page = "Welcome"
        st.success("👋 You have been logged out.")
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**👤 Logged in as:** {st.session_state.username}")
    st.sidebar.markdown("---")
    st.sidebar.markdown("💡 **Tips:**")
    st.sidebar.markdown("- Use the tools above to enhance your learning")
    st.sidebar.markdown("- Your data is automatically saved")
    st.sidebar.markdown("- Logout when you're done")
    
    # 2. Page Content Rendering
    pages[st.session_state.current_page]()

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
    # Show banner
    show_banner()
    
    # Initialize database on first run
    try:
        database.init_all_tables()
    except Exception as e:
        st.error(f"Database initialization failed: {e}")
        st.stop()
    
    # Access Control
    if not st.session_state.logged_in:
        # Hide main sidebar content when not logged in
        st.markdown("""
            <style>
            .main-sidebar {display: none;}
            </style>
        """, unsafe_allow_html=True)
        
        pre_login_navigation()
    else:
        main_app()

if __name__ == "__main__":
    main()