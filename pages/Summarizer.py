import streamlit as st
import database
import utils
from components.navbar import render_navbar

# --- Page Setup ---
st.set_page_config(page_title="AI Summarizer", page_icon="📄", layout="wide", initial_sidebar_state="collapsed")

# Auth guard
if "username" not in st.session_state or not st.session_state.username:
    st.warning("🔒 Please log in to access this page.")
    if st.button("Go to Login"):
        st.switch_page("app.py")
    st.stop()

username = st.session_state.username

# Session state init
if "summarizer_text" not in st.session_state:
    st.session_state.summarizer_text = ""
if "summary_result" not in st.session_state:
    st.session_state.summary_result = None
if "summary_error" not in st.session_state:
    st.session_state.summary_error = None


def delete_summary_action(sid):
    if database.delete_summary(sid):
        st.toast("🗑️ Summary deleted")
    else:
        st.error("Failed to delete summary.")


def delete_all_summaries_action():
    if database.delete_all_summaries(st.session_state.username):
        st.toast("✅ All summaries cleared")
    else:
        st.error("Failed to clear history.")


def run_summarization(input_text, title, length_pct):
    """Run the AI summarization and save result. Called inline (not as callback)."""
    if not input_text or len(input_text.strip()) < 20:
        st.error("⚠️ Please provide at least 20 characters of text.")
        return

    with st.spinner("🤖 AI is reading and summarizing… this may take a few seconds."):
        # Map the percentage to token lengths: 10% → max=80, 100% → max=250
        max_length = max(60, int(80 + (length_pct / 100) * 170))
        min_length = max(20, int(max_length * 0.3))

        summary = utils.generate_ai_summary(input_text, max_length=max_length, min_length=min_length)
        keywords = utils.extract_keywords(input_text)
        display_summary = f"{summary}\n\n**Key Topics:** {', '.join(keywords)}" if keywords else summary

        if database.add_summary(username, input_text, display_summary, title=title):
            st.toast("✅ Summary saved!", icon="📄")
            st.rerun()
        else:
            st.error("Could not save summary to history.")


# --- Main Page ---
database.init_all_tables()
utils.load_css()
render_navbar(active_page="Summarizer")

summaries = database.get_summaries(username)

# --- Page Header ---
st.markdown("""
<div style="margin-bottom:1.5rem;">
<h2 style="margin:0; font-size:1.8rem; font-weight:700; color:#1e293b;">📄 AI Summarizer</h2>
<p style="color:#64748b; margin:0.25rem 0 0 0;">Paste text or upload a file to generate an AI-powered summary instantly</p>
</div>
""", unsafe_allow_html=True)

# --- Main Content Grid ---
col_input, col_sidebar = st.columns([2, 1])

# --- Left Column: Input & History ---
with col_input:
    tab_text, tab_file = st.tabs(["📄 Text Input", "📤 File Upload"])

    with tab_text:
        st.session_state.summarizer_text = st.text_area(
            "Paste text",
            value=st.session_state.summarizer_text,
            height=200,
            placeholder="Paste your notes, articles, or any text here…",
            label_visibility="collapsed"
        )

        char_count = len(st.session_state.summarizer_text)
        c_info, c_btn = st.columns([1, 1])
        with c_info:
            color = "#16a34a" if char_count >= 20 else "#94a3b8"
            st.markdown(f"<div style='color:{color}; font-size:0.88rem; padding-top:10px;'>{char_count} characters {('✓' if char_count >= 20 else '(need 20+)')}</div>", unsafe_allow_html=True)
        with c_btn:
            # Read the length_pct from sidebar state (defaults to 30 if not set yet)
            length_pct = st.session_state.get("summary_length_slider", 30)
            if st.button("✨ Generate Summary", type="primary", use_container_width=True,
                         disabled=char_count < 20):
                run_summarization(
                    input_text=st.session_state.summarizer_text,
                    title="Text Summary",
                    length_pct=length_pct
                )

    with tab_file:
        uploaded = st.file_uploader(
            "Upload a file",
            type=["pdf", "docx", "txt"],
            label_visibility="collapsed"
        )
        if uploaded:
            st.success(f"📎 File **'{uploaded.name}'** ready to summarize!")
            length_pct = st.session_state.get("summary_length_slider", 30)
            if st.button("✨ Generate from File", type="primary", use_container_width=True):
                # Extract text HERE before any rerun — avoids stale file object bug
                with st.spinner("Reading file…"):
                    extracted = utils.extract_text_from_file(uploaded)
                if extracted and len(extracted.strip()) >= 20:
                    run_summarization(
                        input_text=extracted,
                        title=uploaded.name,
                        length_pct=length_pct
                    )
                else:
                    st.error("Could not extract text from the file, or it was too short.")
        st.info("ℹ️ Supports PDF, DOCX, and TXT files up to 10MB")

    # --- Recent Summaries ---
    st.markdown("<br>", unsafe_allow_html=True)
    c_hist, c_clear = st.columns([0.7, 0.3])
    with c_hist:
        st.markdown("<h3 style='margin:0;'>📚 Recent Summaries</h3>", unsafe_allow_html=True)
    with c_clear:
        if summaries:
            st.button("🗑️ Clear All", on_click=delete_all_summaries_action,
                      type="secondary", use_container_width=True)

    if not summaries:
        st.info("No summaries yet. Generate one above!")
    else:
        for s in summaries[:5]:
            ts = s['created_ts'] or ""
            # Format timestamp nicely if possible
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(str(ts).split(".")[0])
                ts = dt.strftime("%b %d, %Y at %I:%M %p")
            except Exception:
                pass

            st.markdown(f"""
<div class="summary-card animate-in fade-in">
<div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.75rem;">
<div>
<h3 style="margin:0; color:#166534; font-size:1rem;">✅ {s['title'] or 'Summary'}</h3>
<div style="font-size:0.78rem; color:#64748b; margin-top:2px;">🕒 {ts}</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

            st.code(s['summary_text'] or "", language="text")

            c_del, c_spacer = st.columns([0.18, 0.82])
            with c_del:
                st.button("🗑️", key=f"del_{s['id']}", help="Delete this summary",
                          use_container_width=True,
                          on_click=delete_summary_action, args=(s['id'],))
            st.markdown("<hr style='border:none; border-top:1px solid #e2e8f0; margin:0.75rem 0;'>", unsafe_allow_html=True)

# --- Right Column: Settings & Templates ---
with col_sidebar:
    with st.container(border=True):
        st.markdown("### ⚙️ Settings")
        # Store value in session state so the text input tab can read it
        st.session_state.summary_length_slider = st.slider(
            "Summary Length", 10, 100, 30,
            format="%d%%",
            help="Controls how long the generated summary will be"
        )
        st.select_slider(
            "Detail Level",
            options=["Brief", "Balanced", "Detailed"],
            value="Balanced",
            help="Affects the minimum detail captured in the summary"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("### 📝 Quick Templates")
        st.markdown("<p style='color:#64748b; font-size:0.85rem;'>Load a sample text to test the summarizer</p>", unsafe_allow_html=True)

        if st.button("🔬 Scientific Article", use_container_width=True):
            st.session_state.summarizer_text = (
                "Quantum computing represents a paradigm shift in computational theory and practice. "
                "Unlike classical computers that process bits as either 0 or 1, quantum computers leverage "
                "quantum mechanical phenomena such as superposition and entanglement to process qubits that "
                "can represent 0, 1, or both simultaneously. This enables quantum computers to solve certain "
                "classes of problems exponentially faster than their classical counterparts. Key applications "
                "include cryptography, drug discovery, financial modeling, and optimization problems. "
                "Companies like IBM, Google, and various startups are racing to achieve quantum advantage — "
                "the point at which quantum computers outperform classical ones on practical tasks."
            )
            st.rerun()

        if st.button("📜 Historical Text", use_container_width=True):
            st.session_state.summarizer_text = (
                "The Industrial Revolution, which began in Britain in the late 18th century, fundamentally "
                "transformed human society and the global economy. The shift from agrarian, handicraft economies "
                "to one dominated by industry and machine manufacturing changed the nature of work, urbanization, "
                "and social class structures. New technologies such as the steam engine, textile machinery, and "
                "iron production methods enabled mass manufacturing. This period saw the rise of factory systems, "
                "the growth of cities, expansion of the middle class, and significant environmental impacts. "
                "The revolution spread from Britain to Western Europe and North America throughout the 19th century."
            )
            st.rerun()

        if st.button("🧬 Biology Notes", use_container_width=True):
            st.session_state.summarizer_text = (
                "DNA, or deoxyribonucleic acid, is the hereditary material in humans and almost all other organisms. "
                "Nearly every cell in a person's body has the same DNA. Most DNA is located in the cell nucleus, "
                "with a small amount found in mitochondria. Information in DNA is stored as a code made up of four "
                "chemical bases: adenine (A), guanine (G), cytosine (C), and thymine (T). DNA bases pair up with each "
                "other — A with T and C with G — to form units called base pairs. Each base is also attached to a "
                "sugar molecule and a phosphate molecule. Together, a base, sugar, and phosphate form a nucleotide. "
                "The double helix structure of DNA was discovered by Watson and Crick in 1953."
            )
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    # Stats sidebar
    with st.container(border=True):
        st.markdown("### 📊 Your Stats")
        total = len(summaries)
        st.metric("Total Summaries", total)
        if total > 0:
            st.progress(min(total / 10, 1.0), text=f"{total}/10 summaries milestone")
