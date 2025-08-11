import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="❓ FAQ", layout="wide")

# --- HIDE DEFAULT SIDEBAR NAVIGATION ---
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# --- CUSTOM SIDEBAR ---
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


# --- TITLE ---
st.title("❓ Frequently Asked Questions (FAQ)")
st.markdown("Find quick answers to common questions about the app.")
st.markdown("---")

# --- FAQ CONTENT ---
with st.expander("Is AI Study Buddy a free application?"):
    st.markdown("Yes, AI Study Buddy is an open-source and free application. You can use all its features without any cost.")

with st.expander("Can I use this app offline?"):
    st.markdown("""
    Yes and no. The **core features** like the **Study Tracker** and **Report** pages work entirely offline, as they use a local database.

    However, the **AI-powered features** like the **Summarizer** and **Flashcard** pages require an active internet connection to communicate with the large language model (LLM) and process your text.
    """)

with st.expander("How do I add a new subject to my study tracker?"):
    st.markdown("""
    You can add a new subject directly on the **Study Tracker** page. When you start a new session, you can simply type in the name of your new subject, and it will be saved automatically for future use.
    """)

with st.expander("How are the reports generated?"):
    st.markdown("""
    The reports are generated in real-time from the data you log on the **Study Tracker** page. They use libraries like `pandas`, `matplotlib`, and `seaborn` to visualize your study sessions and provide key insights.
    """)

with st.expander("Is my data secure?"):
    st.markdown("""
    Yes. All your data, including study logs and feedback, is stored locally in a file named `studybuddy.db` on your computer. It is not sent to any external server. Your login credentials are also stored locally in `users.json`.
    """)

with st.expander("How do I create flashcards from my notes?"):
    st.markdown("""
    Go to the **Flashcards** page, paste your text into the input box, and the application will use an AI model to generate flashcards based on the content. This requires an active internet connection.
    """)

# --- FOOTER ---
st.markdown("---")
st.markdown("📘 *AI Study Buddy – Making Learning Easier*")