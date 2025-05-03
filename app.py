import streamlit as st
from agents import input_validator, web_scraper, document_parser, synthesizer, letter_generator, output_formatter, download_generator
# Optional: from agents import chroma_storage

st.set_page_config(page_title="AI Motivation Letter Generator", layout="centered")

st.title("✉️ AI-Powered Motivation Letter Generator")
st.markdown("Generate a high-quality, personalized motivation letter with ease.")

# Sidebar: Only API key
with st.sidebar:
    st.header("🔐 API Key")
    api_key = st.text_input("OpenAI API Key", type="password")

# Main content: Inputs
st.header("📋 Input Details")
title = st.text_input("Motivation Letter Title", placeholder="e.g., Application for Data Scientist at XYZ")
description = st.text_area("Job Description / Key Points", height=200)
url = st.text_input("Optional URL (e.g., job posting or company page)")
cv_file = st.file_uploader("Upload your CV or Résumé (.pdf or .docx)", type=["pdf", "docx"])

generate_btn = st.button("🚀 Generate Motivation Letter")

if generate_btn:
    with st.spinner("🔍 Validating input..."):
        valid_input, error, user_data = input_validator.validate(api_key, title, description, url, cv_file)
        if not valid_input:
            st.error(error)
            st.stop()

    with st.spinner("🌐 Scraping website..."):
        web_data = web_scraper.scrape(user_data["url"])

    with st.spinner("📄 Parsing CV..."):
        cv_text = document_parser.parse(user_data["cv_file"])

    with st.spinner("🧠 Synthesizing information..."):
        context = synthesizer.synthesize(user_data, web_data, cv_text)

    with st.spinner("✍️ Generating letter..."):
        letter, error = letter_generator.generate(context, api_key)
        if error:
            st.error(error)
            st.stop()

    with st.spinner("📄 Formatting output..."):
        formatted = output_formatter.format(letter)
        st.markdown(formatted, unsafe_allow_html=True)

    with st.spinner("⬇️ Preparing downloads..."):
        download_generator.generate_buttons(letter)

    # Optional save
    # if st.button("💾 Save to ChromaDB"):
    #     chroma_storage.save(context, letter)
