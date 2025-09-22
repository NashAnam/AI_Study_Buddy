import streamlit as st
import pandas as pd
from database import save_flashcard, get_flashcards, delete_flashcards

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(page_title="Flashcards", page_icon="🧠", layout="wide")

# ---------------------- HIDE SIDEBAR NAV ----------------------
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------- AUTH CHECK ----------------------
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please login to access this page.")
    st.stop()
    
# ---------------------- SIDEBAR LINKS ----------------------
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

# ---------------------- AUTH CHECK ----------------------
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please login to access this page.")
    st.stop()

# ---------------------- AUTOMATIC GENERATION LOGIC (NEW AND IMPROVED) ----------------------
def generate_flashcards_from_text(text):
    """
    Generates flashcards in a 'Term' and 'Definition' format using a more robust set of rules.
    """
    flashcard_list = []
    
    # Split text by sentences to process individually
    sentences = text.split('.')
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        # Rule 1: Look for "is a" or "are" to identify definitions
        if ' is a ' in sentence:
            parts = sentence.split(' is a ', 1)
            term = parts[0].strip()
            definition = "is a " + parts[1].split('.')[0].strip()
            flashcard_list.append((term, definition))
        elif ' are ' in sentence:
            parts = sentence.split(' are ', 1)
            term = parts[0].strip()
            definition = "are " + parts[1].split('.')[0].strip()
            flashcard_list.append((term, definition))
            
        # Rule 2: Look for colons (:) to identify term-definition pairs
        elif ':' in sentence:
            parts = sentence.split(':', 1)
            term = parts[0].strip()
            definition = parts[1].split('.')[0].strip()
            if term and definition:
                flashcard_list.append((term, definition))
        
        # Rule 3: Look for facts with a clear subject and predicate
        else:
            words = sentence.split()
            if len(words) > 3:
                term = ' '.join(words[:2]).strip()
                definition = ' '.join(words[2:]).strip()
                flashcard_list.append((term, definition))

    return flashcard_list

# ---------------------- TITLE ----------------------
st.title("🧠 Flashcards")
st.markdown("Instantly create and study flashcards from your notes.")
st.markdown("---")

username = st.session_state.username

# --- Get and store flashcards in session state for reliable updates ---
if 'flashcards_data' not in st.session_state:
    st.session_state.flashcards_data = get_flashcards(username)

df = pd.DataFrame(st.session_state.flashcards_data, columns=["ID", "Question", "Answer", "Created At"]) if st.session_state.flashcards_data else pd.DataFrame()

# ---------------------- SECTION 1: AUTOMATED CREATOR ----------------------
st.header("1️⃣ Automated Creator")
st.markdown("Paste your study material below to have flashcards automatically generated and saved.")
source_text = st.text_area(
    "Paste your study material here:",
    height=200,
    placeholder="e.g., 'The capital of France is Paris. Jupiter: The largest planet in our solar system.'"
)
if st.button("Generate & Save Flashcards", key="generate_button", use_container_width=True):
    if source_text.strip():
        generated_cards = generate_flashcards_from_text(source_text)
        if generated_cards:
            with st.spinner(f"Saving {len(generated_cards)} flashcards..."):
                for q, a in generated_cards:
                    save_flashcard(username, q, a)
            st.success(f"✅ Successfully generated and saved {len(generated_cards)} flashcards!")
            st.session_state.flashcards_data = get_flashcards(username)
            st.rerun()
        else:
            st.info("💡 Could not generate flashcards. Try providing more descriptive text.")
    else:
        st.warning("⚠️ Please enter some text to generate flashcards.")

st.markdown("---")

# ---------------------- SECTION 2: STUDY SESSION ----------------------
st.header("2️⃣ Study Session")
st.markdown("Flip through your flashcards to test your knowledge. This session is always up-to-date.")

if not df.empty:
    flashcards = list(zip(df["Question"], df["Answer"]))
    card_count = len(flashcards)
    
    if 'card_index' not in st.session_state or st.session_state.card_index >= card_count:
        st.session_state.card_index = 0
    if 'show_answer' not in st.session_state:
        st.session_state.show_answer = False
    
    term, definition = flashcards[st.session_state.card_index]

    col_nav1, col_main, col_nav2 = st.columns([1, 4, 1])

    with col_nav1:
        if st.button("⬅️ Previous", key="prev_button", use_container_width=True):
            st.session_state.card_index = (st.session_state.card_index - 1) % card_count
            st.session_state.show_answer = False
            st.rerun()
    
    with col_nav2:
        if st.button("Next ➡️", key="next_button", use_container_width=True):
            st.session_state.card_index = (st.session_state.card_index + 1) % card_count
            st.session_state.show_answer = False
            st.rerun()

    with col_main:
        st.info(f"**Card {st.session_state.card_index + 1} of {card_count}**")
        st.markdown(f"### **Term:** {term}")

        if not st.session_state.show_answer:
            if st.button("Flip to See Definition", key="flip_button", use_container_width=True):
                st.session_state.show_answer = True
                st.rerun()
        else:
            st.success(f"### **Definition:** {definition}")
            if st.button("Hide Definition", key="hide_button", use_container_width=True):
                st.session_state.show_answer = False
                st.rerun()
else:
    st.info("No flashcards saved yet. Use the creator above to get started!")

st.markdown("---")

# ---------------------- SECTION 3: MANAGE FLASHCARDS ----------------------
st.header("3️⃣ Manage My Flashcards")

if not df.empty:
    st.dataframe(df.set_index("ID")[["Question", "Answer", "Created At"]], use_container_width=True)

    st.markdown("To delete, enter the **IDs** of the flashcards you want to remove, separated by commas.")

    ids_to_delete_str = st.text_input(
        "Enter Flashcard IDs (e.g., 1, 5, 8):",
        placeholder="e.g., 1, 5, 8"
    )
    
    if st.button("🗑️ Delete Flashcards by ID", key="delete_by_id_button", use_container_width=True):
        if ids_to_delete_str:
            try:
                ids_to_delete = [int(id_str.strip()) for id_str in ids_to_delete_str.split(',')]
                
                existing_ids = set(df["ID"])
                valid_ids = [id for id in ids_to_delete if id in existing_ids]

                if valid_ids:
                    delete_flashcards(username, valid_ids)
                    st.session_state.flashcards_data = get_flashcards(username)
                    st.session_state.card_index = 0
                    st.success(f"✅ Successfully deleted {len(valid_ids)} flashcards. The study session has been updated.")
                    st.rerun()
                else:
                    st.warning("⚠️ No valid flashcard IDs were found to delete. Please check your input.")

            except ValueError:
                st.error("❌ Invalid input. Please enter numbers separated by commas (e.g., 1, 5, 8).")
        else:
            st.warning("⚠️ Please enter at least one flashcard ID to delete.")
else:
    st.info("No flashcards to manage.")

# ---------------------- FOOTER ----------------------
st.markdown("---")
st.markdown("📘 *AI Study Buddy - Smarter Study Tools*")