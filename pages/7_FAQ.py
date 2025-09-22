import streamlit as st

st.set_page_config(page_title="❓ FAQ - AI Study Buddy", layout="centered")

# Hide default sidebar nav (optional)
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

st.title("❓ Frequently Asked Questions")

st.markdown(
    """
    Welcome to the FAQ page! Here are answers to some common questions about AI Study Buddy.
    """
)

# Use expanders for each FAQ — cleaner UI and easy scanning
faqs = {
    "What is AI Study Buddy?": (
        "AI Study Buddy is your personal AI-powered learning assistant that helps you "
        "summarize notes, plan study schedules, generate flashcards, and more."
    ),
    "Is my data stored securely?": (
        "Currently, your data is stored locally on your device. No cloud storage or external "
        "APIs are used without your permission, ensuring your privacy."
    ),
    "Can I use this offline?": (
        "Yes! AI Study Buddy runs entirely on your local machine after setup, so no internet "
        "connection is required to use the core features."
    ),
    "How does the local database work?": (
        "The app uses a local SQLite database file named 'studybuddy.db' to store all your "
        "study logs, exams, and feedback. This file is located in the same directory as the app."
    ),
    "Can I customize features?": (
        "Absolutely! You can add your own questions, customize flashcards, and expand modules "
        "to tailor the app to your learning style."
    ),
    "How do I get support if I encounter issues?": (
        "Feel free to use the Feedback page to report bugs or request features. "
        "We're committed to continuous improvement."
    )
}

for question, answer in faqs.items():
    with st.expander(f"❓ {question}"):
        st.write(answer)

st.markdown("---")
st.markdown("💡 **Tip:** Explore other pages to maximize your study efficiency with AI Study Buddy!")