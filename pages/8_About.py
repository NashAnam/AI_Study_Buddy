import streamlit as st

# Hide default sidebar navigation
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

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

custom_sidebar()

st.set_page_config(page_title="ℹ️ About")

st.title("ℹ️ About AI Study Buddy")

st.markdown(
    """
    **AI Study Buddy** is a smart, interactive, AI-powered platform designed to help students by:

    - 📄 **Summarizing large texts** quickly and effectively  
    - 📅 **Planning and tracking study sessions** with ease  
    - 🔁 **Generating flashcards** for efficient revision  
    - 📊 **Viewing detailed reports and feedback** to monitor progress  

    ---

    ### 👩‍💻 Developed by  
    **Nashrah Anam Fathima**  
    Department of AI & Data Science — JNTU Hyderabad  

    © 2025 All rights reserved.
    """
)
