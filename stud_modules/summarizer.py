from transformers import pipeline
import fitz  # PyMuPDF

summarizer_model = pipeline("summarization")

def generate_summary(text, max_length=130, min_length=30):
    summary = summarizer_model(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

def extract_text_from_pdf(uploaded_file):
    pdf_reader = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    full_text = ""
    for page in pdf_reader:
        full_text += page.get_text()
    return full_text
