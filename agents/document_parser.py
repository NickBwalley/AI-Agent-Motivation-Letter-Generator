from PyPDF2 import PdfReader
from docx import Document
import io

def parse(file):
    if not file:
        return ""
    try:
        if file.name.endswith(".pdf"):
            pdf = PdfReader(file)
            return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        elif file.name.endswith(".docx"):
            doc = Document(file)
            return "\n".join(p.text for p in doc.paragraphs)
    except Exception as e:
        return f"[Error parsing CV: {e}]"
