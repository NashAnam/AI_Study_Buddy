import streamlit as st
import pandas as pd
from datetime import datetime
from database import get_subjects, get_study_logs, add_study_log, delete_study_logs
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(page_title="Study Tracker", page_icon="📊", layout="wide")

# ---------------------- HIDE SIDEBAR NAV ----------------------
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------- SIDEBAR LINKS ----------------------
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
    custom_sidebar()

    # ---------------------- AUTH CHECK ----------------------
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.warning("🔒 Please login to access this page.")
        st.stop()

    # ---------------------- TITLE ----------------------
    st.title("📊 Study Tracker Dashboard")
    st.markdown("Track, visualize, and manage your study sessions effectively.")
    st.markdown("---")

    username = st.session_state.username

    # --- Layout: Main Controls & Recent Logs ---
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("📝 Log Study Session")
        
        new_subject = st.text_input("Enter a new subject name to add:", key="new_subject_input")
        if st.button("Add Subject"):
            if new_subject:
                add_study_log(username, new_subject, 0, datetime.now())
                st.success(f"Subject '{new_subject}' added!")
                st.rerun()

        all_subjects = get_subjects(username)
        
        # Use multiselect for selecting multiple subjects
        if all_subjects:
            selected_subjects = st.multiselect("Select Subject(s) for visualization:", all_subjects, key="multiselect_subjects")
        else:
            st.info("Start by adding your first subject above.")
            selected_subjects = []
            
        st.markdown("---")

        # Timer logic
        if 'start_time' not in st.session_state:
            st.session_state.start_time = None
            st.session_state.current_subject = None
        
        # Timer control for a single subject
        st.markdown("#### Timer for a single subject:")
        subject_for_timer = st.selectbox("Choose a subject to track now:", all_subjects, key="timer_subject_box")

        if st.button("▶️ Start Timer"):
            if subject_for_timer:
                st.session_state.start_time = datetime.now()
                st.session_state.current_subject = subject_for_timer
                st.success(f"Timer started for **{st.session_state.current_subject}** at {st.session_state.start_time.strftime('%H:%M:%S')}")
            else:
                st.warning("Please select a subject to start the timer.")

        if st.button("⏹ Stop and Log"):
            if st.session_state.start_time and st.session_state.current_subject:
                end_time = datetime.now()
                duration_minutes = (end_time - st.session_state.start_time).total_seconds() / 60
                
                add_study_log(username, st.session_state.current_subject, duration_minutes, st.session_state.start_time)
                
                st.success(f"Ended at {end_time.strftime('%H:%M:%S')} | Duration: {duration_minutes:.1f} minutes")
                st.session_state.start_time = None
                st.session_state.current_subject = None
                st.rerun()
            else:
                st.warning("Start the timer first.")
    
    with col2:
        st.subheader("📚 Recent Study Sessions")
        
        logs = get_study_logs(username)
        
        if logs:
            # Corrected column names to match the 5 columns from the database
            df_logs = pd.DataFrame(logs, columns=["ID", "Subject", "Duration (mins)", "Started At", "Created At"])
            st.dataframe(df_logs, use_container_width=True)
        else:
            st.info("No study sessions logged yet.")

        st.markdown("---")
        st.subheader("🗑️ Delete Logs by Index")
        indices_to_delete_str = st.text_input("Enter row IDs to delete (comma-separated):", key="delete_input")
        
        if st.button("Delete Selected Logs"):
            try:
                indices_to_delete = [int(i.strip()) for i in indices_to_delete_str.split(',') if i.strip().isdigit()]
                if indices_to_delete:
                    delete_study_logs(username, indices_to_delete)
                    st.success(f"Successfully deleted logs with IDs: {indices_to_delete}")
                    st.rerun()
                else:
                    st.warning("Please enter valid log IDs to delete.")
            except Exception as e:
                st.error(f"Error deleting logs: {e}")

    # ---------------------- VISUALIZATIONS SECTION ----------------------
    st.markdown("---")
    st.header("📊 Study Visualizations")

    if selected_subjects:
        logs = get_study_logs(username)
        # Corrected column names to match the 5 columns from the database
        df_logs = pd.DataFrame(logs, columns=["ID", "Subject", "Duration (mins)", "Started At", "Created At"])
        
        # Filter data for selected subjects
        filtered_logs = df_logs[df_logs['Subject'].isin(selected_subjects)]
        
        if not filtered_logs.empty:
            # Global stats for all selected subjects
            st.markdown(f"#### Overview of your selected subjects: {', '.join(selected_subjects)}")
            total_duration = filtered_logs['Duration (mins)'].sum()
            st.metric("Total Study Time (mins)", f"{total_duration:.2f}")

            # Create two columns for visualizations
            vis_col1, vis_col2 = st.columns([1, 1])

            with vis_col1:
                st.markdown(f"##### Total Study Time per Subject")
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.barplot(data=filtered_logs.groupby('Subject')['Duration (mins)'].sum().reset_index(),
                            x='Subject', y='Duration (mins)', palette='Paired', ax=ax)
                ax.set_title(f"Total Duration by Subject")
                ax.set_xlabel("Subject")
                ax.set_ylabel("Total Duration (minutes)")
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig)
            
            with vis_col2:
                st.markdown(f"##### Percentage of Study Time")
                fig, ax = plt.subplots(figsize=(8, 8))
                subject_summary = filtered_logs.groupby('Subject')['Duration (mins)'].sum()
                ax.pie(subject_summary, labels=subject_summary.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('tab20'))
                ax.axis('equal')
                ax.set_title("Time Distribution")
                st.pyplot(fig)
        else:
            st.info(f"No study sessions logged for any of the selected subjects.")

    else:
        st.info("Please select one or more subjects above to see visualizations.")

    # ---------------------- FOOTER ----------------------
    st.markdown("---")
    st.markdown("📘 *AI Study Buddy - Smarter Study Tracking*")

if __name__ == "__main__":
    app()