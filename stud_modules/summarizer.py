from transformers import pipeline
import fitz  # PyMuPDF

# Load the summarization model once
summarizer_model = pipeline("summarization")

def generate_summary(text, max_length=150, min_length=50):
    """Generate a summary for the given text using chunked processing for long texts."""
    max_input_length = 1024  # BART’s token limit

    # Tokenize to check input size
    tokens = summarizer_model.tokenizer(text, return_tensors="pt", truncation=False)
    token_count = tokens['input_ids'].shape[1]

    if token_count <= max_input_length:
        # Direct summarization
        summary = summarizer_model(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
            truncation=True
        )
        return summary[0]['summary_text']

    else:
        # Split into chunks
        words = text.split()
        num_chunks = (token_count // max_input_length) + 1
        chunk_size = len(words) // num_chunks
        chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

        summaries = []
        for chunk in chunks:
            # Safeguard against zero-length values
            local_max = max(50, max_length // num_chunks)
            local_min = max(20, min_length // num_chunks)

            summary = summarizer_model(
                chunk,
                max_new_tokens=local_max,  # better than max_length
                min_length=local_min,
                do_sample=False,
                truncation=True
            )
            summaries.append(summary[0]['summary_text'])

        combined_summary = ' '.join(summaries)

        # If still too long, re-summarize
        if len(combined_summary.split()) > max_length:
            final_summary = summarizer_model(
                combined_summary,
                max_new_tokens=max_length,
                min_length=min_length,
                do_sample=False,
                truncation=True
            )
            return final_summary[0]['summary_text']

        return combined_summary



def extract_text_from_pdf(uploaded_file):
    """Extract full text from an uploaded PDF file."""
    pdf_reader = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    full_text = ""
    for page in pdf_reader:
        full_text += page.get_text()
    return full_text
