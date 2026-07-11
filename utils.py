import bcrypt
import logging
import os
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Resolve the CSS file path relative to this file's location,
# so it works regardless of the current working directory.
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_css_path():
    """Return absolute path to custom.css."""
    return os.path.join(_BASE_DIR, "static", "custom.css")

def load_css():
    """Inject custom CSS into the Streamlit page."""
    css_file = get_css_path()
    if os.path.exists(css_file):
        with open(css_file, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        logger.warning(f"CSS file not found at: {css_file}")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    try:
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    except Exception as e:
        logger.error(f"Error hashing password: {e}")
        raise

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its bcrypt hash."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception as e:
        logger.error(f"Error verifying password: {e}")
        return False

# --- AI & File Helpers (Lazy Loaded) ---

@st.cache_resource
def load_summarizer():
    try:
        from transformers import pipeline
        # Small, efficient model suitable for this app
        return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    except Exception as e:
        logger.error(f"Error loading summarizer: {e}")
        return None

def extract_text_from_file(uploaded_file):
    text = ""
    try:
        if uploaded_file.name.endswith('.pdf'):
            import fitz  # PyMuPDF
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            for page in doc:
                text += page.get_text()
        elif uploaded_file.name.endswith('.docx'):
            import docx
            doc = docx.Document(uploaded_file)
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif uploaded_file.name.endswith('.txt'):
            text = uploaded_file.read().decode('utf-8')
    except ImportError:
        logger.error("Required library (PyMuPDF or python-docx) not installed.")
        st.error("Missing dependencies for file parsing. Please run: pip install pymupdf python-docx")
    except Exception as e:
        logger.error(f"File Parsing Error: {e}")
    return text

def generate_ai_summary(text, max_length=150, min_length=40):
    """Generate a summary using the cached HuggingFace pipeline."""
    if not text or len(text.strip()) == 0:
        return "No text provided."

    summarizer = load_summarizer()
    if not summarizer:
        return "AI Summarizer unavailable. Ensure 'transformers' and 'torch' are installed."

    # DistilBART has a ~1024 token limit — chunk at ~3000 chars to stay safe
    chunk_size = 3000
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    summaries = []
    try:
        for chunk in chunks:
            if len(chunk.strip()) < 30:
                continue
            res = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
            summaries.append(res[0]['summary_text'])

        if not summaries:
            return "Text was too short or empty to summarize."

        # If multiple chunks, do a final pass on the combined summaries
        if len(summaries) > 1:
            combined = " ".join(summaries)
            if len(combined) > chunk_size:
                final_res = summarizer(combined[:chunk_size], max_length=200, min_length=60, do_sample=False)
                return final_res[0]['summary_text']
            return combined

        return summaries[0]
    except Exception as e:
        logger.error(f"AI Summary Error: {e}")
        return "Error generating summary. The text might be too complex or malformed."

def extract_keywords(text):
    try:
        import yake
        kw_extractor = yake.KeywordExtractor(lan="en", n=1, dedupLim=0.9, top=5)
        keywords = kw_extractor.extract_keywords(text)
        return [kw[0] for kw in keywords]
    except ImportError:
        logger.warning("yake not installed. Skipping keyword extraction.")
        return []
    except Exception as e:
        logger.error(f"Keyword Extraction Error: {e}")
        return []
