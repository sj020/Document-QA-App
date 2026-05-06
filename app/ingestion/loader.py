import os
import tempfile
from pypdf import PdfReader

def load_documents(uploaded_files):
    """Load Documents utility it would take the input files and extract the text from the files."""
    documents = []

    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            temp_path = tmp.name

        reader = PdfReader(temp_path)

        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                documents.append({
                    "text": text,
                    "source": uploaded_file.name,
                    "page": i + 1
                })

        os.remove(temp_path)

    return documents