import streamlit as st
from fpdf import FPDF
from docx import Document
import textwrap
import tempfile

# Helper to wrap long lines to avoid FPDFException
def safe_wrap(text, width=100):
    return '\n'.join(textwrap.wrap(text, width=width, break_long_words=True, replace_whitespace=False))

def generate_buttons(letter: str):
    st.subheader("📄 Download Your Motivation Letter")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📥 Download as PDF"):
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            # Set margins and font
            pdf.set_left_margin(15)
            pdf.set_right_margin(15)
            pdf.set_font("Arial", size=12)

            # Safely wrap and write letter text
            for line in letter.split('\n'):
                current_line = safe_wrap(line)
                pdf.multi_cell(180, 10, current_line)

            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                pdf.output(tmp_file.name)
                st.download_button(
                    label="📥 Click to Download PDF",
                    data=open(tmp_file.name, "rb").read(),
                    file_name="motivation_letter.pdf",
                    mime="application/pdf"
                )

    with col2:
        if st.button("📝 Download as DOCX"):
            doc = Document()
            for line in letter.split('\n'):
                doc.add_paragraph(line)

            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
                doc.save(tmp_file.name)
                st.download_button(
                    label="📝 Click to Download DOCX",
                    data=open(tmp_file.name, "rb").read(),
                    file_name="motivation_letter.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
