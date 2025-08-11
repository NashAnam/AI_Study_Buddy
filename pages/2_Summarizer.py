import streamlit as st
from stud_modules import summarizer
from stud_modules.auth import is_logged_in
from io import StringIO
from database import save_summary, get_user_summaries

st.set_page_config(page_title="Summarizer", page_icon="📝")

# ---------------------- AUTH CHECK ----------------------
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please login to access this page.")
    st.stop()
        
# Hide sidebar nav
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

def app():
    st.title("📝 Text & File Summarizer")
    custom_sidebar()

    if not is_logged_in():
        st.warning("🔒 Please log in to access the summarizer.")
        st.stop()

    username = st.session_state.get("username", "")

    st.write("Enter some text below or upload a `.txt`/`.pdf` file to get a summary.")

    uploaded_file = st.file_uploader("📄 Upload a file", type=["txt", "pdf"])
    input_text = ""

    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            input_text = stringio.read()
        elif uploaded_file.type == "application/pdf":
            input_text = summarizer.extract_text_from_pdf(uploaded_file)
        else:
            st.error("Unsupported file type.")
            return
    else:
        input_text = st.text_area("✍️ Or paste your text here", height=250)

    if st.button("🧠 Summarize"):
        if not input_text.strip():
            st.error("⚠️ Please provide some text.")
            return

        with st.spinner("Generating summary..."):
            summary = summarizer.generate_summary(input_text)

        st.success("✅ Summary generated:")
        st.markdown(f"""
            <div style='border:1px solid #ccc; padding:15px; border-radius:10px; background-color:#f9f9f9'>
                {summary}
            </div>""", unsafe_allow_html=True)

        st.download_button("⬇️ Download Summary", summary, file_name="summary.txt")

        # Save to database
        save_summary(username, input_text, summary)

    # Optional: Show past summaries
    with st.expander("📜 View Previous Summaries"):
        summaries = get_user_summaries(username)
        if summaries:
            for i, (original, summary, timestamp) in enumerate(summaries[::-1], 1):
                st.markdown(f"**📝 Summary {i} (🕒 {timestamp})**")
                st.markdown(f"<div style='border:1px solid #eee; padding:10px; border-radius:5px'>{summary}</div>", unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.info("No summaries saved yet.")

if __name__ == "__main__":
    app()
