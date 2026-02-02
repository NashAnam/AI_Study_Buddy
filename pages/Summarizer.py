import streamlit as st
import time
import database
import utils
from components.navbar import render_navbar

# --- Setup ---
st.set_page_config(page_title="AI Summarizer", page_icon="📄", layout="wide")

# Ensure login
if "username" not in st.session_state or not st.session_state.username:
    st.warning("Please log in.")
    st.stop()

username = st.session_state.username

if "summarizer_text" not in st.session_state:
    st.session_state.summarizer_text = ""
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

def load_css():
    with open("static/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def handle_summarize(source="text", uploaded_file=None):
    # Set a flag to trigger summarization in the main flow
    st.session_state.trigger_summarize = {
        "source": source,
        "file": uploaded_file
    }

def delete_summary_action(sid):
    if database.delete_summary(sid):
        st.toast("Summary deleted")
    else:
        st.error("Failed to delete summary")

def delete_all_summaries_action():
    if database.delete_all_summaries(st.session_state.username):
        st.toast("All summaries cleared")
    else:
        st.error("Failed to clear history")

def main():
    if "trigger_summarize" not in st.session_state:
        st.session_state.trigger_summarize = None

    # Handle the triggered summarization logic here
    if st.session_state.trigger_summarize:
        trigger = st.session_state.trigger_summarize
        st.session_state.trigger_summarize = None # Reset
        
        with st.spinner("🤖 AI is reading and summarizing... this may take a few seconds."):
            try:
                if trigger["source"] == "file" and trigger["file"]:
                    input_text = utils.extract_text_from_file(trigger["file"])
                    title = trigger["file"].name
                else:
                    input_text = st.session_state.summarizer_text
                    title = "Text Summary"

                if input_text and len(input_text) > 0:
                    summary = utils.generate_ai_summary(input_text)
                    keywords = utils.extract_keywords(input_text)
                    display_summary = f"{summary}\n\nKey Topics: {', '.join(keywords)}" if keywords else summary
                    
                    if database.add_summary(username, input_text, display_summary, title=title):
                        st.toast("✅ Summary ready!", icon="📄")
                        st.rerun()
                    else:
                        st.error("Could not save summary to history.")
                else:
                    st.error("Text too short for summarization.")
            except Exception as e:
                st.error(f"Summarization Error: {e}")

    database.init_all_tables()
    load_css()
    render_navbar(active_page="Summarizer")
    summaries = database.get_summaries(username)

    # --- Main Content Grid ---
    col_input, col_sidebar = st.columns([2, 1])

    # --- Left Column: Input & History ---
    with col_input:
        
        st.markdown("""
<div class="ui-card" style="margin-bottom:0.5rem;">
<h3 style="margin:0;">Input Content</h3>
</div>
""", unsafe_allow_html=True)
        
        tab_text, tab_file = st.tabs(["📄 Text Input", "📤 File Upload"])
        
        with tab_text:
            st.session_state.summarizer_text = st.text_area(
                "Paste text", 
                value=st.session_state.summarizer_text,
                height=180,
                placeholder="Paste your text here...",
                label_visibility="collapsed"
            )
            
            char_count = len(st.session_state.summarizer_text)
            is_busy = st.session_state.get("trigger_summarize") is not None
            c_info, c_btn = st.columns([1, 1])
            with c_info:
                st.markdown(f"<div style='color:#64748b; font-size:0.9rem; padding-top:10px;'>{char_count} characters</div>", unsafe_allow_html=True)
            with c_btn:
                btn_label = "Generate Summary" if not is_busy else "Processing..."
                st.button("✨ " + btn_label, type="primary", use_container_width=True, 
                          disabled=char_count < 1 or is_busy,
                          on_click=handle_summarize, kwargs={"source": "text"})

        with tab_file:
            uploaded = st.file_uploader("Upload a file", type=["pdf", "docx", "txt"], label_visibility="collapsed")
            if uploaded:
                st.success(f"File '{uploaded.name}' ready!")
                is_busy = st.session_state.get("trigger_summarize") is not None
                if st.button("Generate from File", type="primary", use_container_width=True, disabled=is_busy):
                    handle_summarize(source="file", uploaded_file=uploaded)
            st.info("Supports PDF, DOCX, TXT files up to 10MB")

        # --- Recent Summaries (Real Data) ---
        c_hist, c_clear = st.columns([0.7, 0.3])
        with c_hist:
            st.markdown("<h3>Recent Summaries</h3>", unsafe_allow_html=True)
        with c_clear:
            if summaries:
                st.button("Clear All", on_click=delete_all_summaries_action, type="secondary", use_container_width=True)
        
        if not summaries:
            st.info("No summaries generated yet. Try creating one!")
            
        for s in summaries[:5]: # Show top 5
            with st.container():
                st.markdown(f"""
<div class="summary-card animate-in fade-in" style="margin-top:1rem; margin-bottom:0.5rem;">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
<div>
<h3 style="margin:0; color:#166534; font-size:1rem;">✅ {s['title'] or 'Summary'}</h3>
<div style="font-size:0.8rem; color:#64748b;">{s['created_ts']}</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)
                
                # Using st.code for built-in copy functionality
                st.code(s['summary_text'], language="text")
                
                c_del, c_spacer = st.columns([0.2, 0.8])
                with c_del:
                    st.button("🗑️ Delete", key=f"del_{s['id']}", help="Delete summary", use_container_width=True, 
                              on_click=delete_summary_action, args=(s['id'],))
                st.markdown("<br>", unsafe_allow_html=True)

    # --- Right Column: Sidebar ---
    with col_sidebar:
        with st.container(border=True):
            st.markdown("### ⚙️ Settings")
            st.slider("Summary Length", 10, 100, 30, format="%d%%")
            st.select_slider("Detail Level", options=["Low", "Medium", "High"], value="Medium")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("### 📝 Templates")
            if st.button("🔬 Scientific Article", use_container_width=True):
                st.session_state.summarizer_text = "Quantum computing represents a paradigm shift..."
                st.rerun()
                
            if st.button("📜 Historical Text", use_container_width=True):
                st.session_state.summarizer_text = "The Industrial Revolution transformed society..."
                st.rerun()

if __name__ == "__main__":
    main()
