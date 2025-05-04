import streamlit as st
from docx import Document
import tempfile

def generate_buttons(letter: str):
    st.subheader("📄 Download Your Motivation Letter")

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
