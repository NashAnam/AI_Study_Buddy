import bcrypt
import logging
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        # Using a small, efficient model suitable for real-time app
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

def generate_ai_summary(text, length_pct=0.3):
    if not text:
        return "No text provided."
    
    summarizer = load_summarizer()
    if not summarizer:
        return "AI Summarizer unavailable. Ensure 'transformers' and 'torch' are installed."
    
    # BART/DistilBART typically has a 1024 token limit (~4000 chars)
    # We'll split text into chunks of ~3000 chars to be safe
    chunk_size = 3000
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    
    summaries = []
    try:
        # Process each chunk
        for chunk in chunks:
            # We adjust max_length based on chunk size but keep it within model limits
            res = summarizer(chunk, max_length=150, min_length=40, do_sample=False)
            summaries.append(res[0]['summary_text'])
        
        # If multiple chunks, summarize the combined summaries for a final polish
        if len(summaries) > 1:
            combined = " ".join(summaries)
            # Final pass on the concatenated summaries if it's still long
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
