import streamlit as st
import database

# ---------------------- HIDE DEFAULT SIDEBAR ----------------------
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------- CUSTOM SIDEBAR ----------------------
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


# ---------------------- PAGE HEADER ----------------------
st.markdown("<h2 style='text-align:center; color:#4CAF50;'>🌟 Feedback</h2>", unsafe_allow_html=True)
st.write("We value your feedback! Please share your thoughts about **AI Study Buddy**.")

# ---------------------- FEEDBACK FORM ----------------------
with st.form("feedback_form"):
    rating = st.slider("Rate your overall experience (1 = Poor, 5 = Excellent)", 1, 5, 3)
    message = st.text_area("✍️ Your feedback")
    submitted = st.form_submit_button("Submit ✅")

    if submitted:
        if message.strip() == "":
            st.error("⚠️ Please enter some feedback before submitting.")
        else:
            database.save_feedback(st.session_state.username, message.strip(), rating)
            st.success("✅ Thank you! Your feedback has been submitted.")

# ---------------------- PREVIOUS FEEDBACK ----------------------
st.markdown("---")
st.subheader("📋 Previous Feedback")
feedback_data = database.get_feedback()

if feedback_data:
    for fb in feedback_data:
        st.markdown(f"""
        **👤 {fb[0]}**  
        ⭐ Rating: {fb[2]} / 5  
        💬 {fb[1]}  
        🕒 _{fb[3]}_
        """)
        st.markdown("---")
else:
    st.info("No feedback submitted yet.")

# ---------------------- FOOTER ----------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:grey;'>© 2025 AI Study Buddy </p>", unsafe_allow_html=True)

# ---------------------- ACCESS CONTROL ----------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please log in to access the Feedback page.")
    st.stop()

# Ensure username exists in session
if "username" not in st.session_state:
    st.error("⚠️ Username not found in session. Please log in again.")
    st.stop()