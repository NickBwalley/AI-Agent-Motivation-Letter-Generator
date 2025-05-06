import streamlit as st
from agents import input_validator, web_scraper, document_parser, synthesizer, letter_generator, output_formatter, download_generator
import os
import time

# Optional: from agents import chroma_storage
## Langsmith Tracking (Optional)
langsmith_key = os.getenv("LANGSMITH_API_KEY")
if langsmith_key:
    os.environ["LANGSMITH_API_KEY"] = langsmith_key
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "AI Motivation Letter Generator"

st.set_page_config(page_title="AI Motivation Letter Generator", layout="centered")

st.title("✉️ AI-Agent Motivation Letter Generator")
st.markdown(" Hello friend... 👋🏾 I will help you generate a high-quality, personalized motivation letter with ease based on the job description / website URL you give and additionally your CV if you have one.")

# Sidebar: Only API key
with st.sidebar:
    st.header("🔐 API Key")
    api_key = st.text_input("OpenAI / Claude / Gemini API Key", type="password")

# Main content: Inputs
description = st.text_area(
    "Brief Description of the Role you are applying for",
    placeholder="""To generate a high-quality motivation letter, please provide:
1. A detailed description of the role you're applying for,
2. The company website URL or job posting URL (optional),
3. Any specific requirements or qualifications you would like to include in the letter,
4. Why you're interested in this position (optional),

""",
    height=200
)

cv_file = st.file_uploader("Upload your CV or Résumé (.pdf or .docx) (optional)", type=["pdf", "docx"]) 

# Initialize session state
if "letter" not in st.session_state:
    st.session_state.letter = None
if "formatted" not in st.session_state:
    st.session_state.formatted = None
if "processing_time" not in st.session_state:
    st.session_state.processing_time = None

# Generate button
generate_btn = st.button("🚀 Generate Motivation Letter")

if generate_btn:
    if not description.strip():
        st.warning("⚠️ Please provide a description of the role and company information before generating.")
        st.stop()

    start_time = time.time()

    with st.spinner("🔍 Validating input..."):
        # Extract URL from description if present
        url = ""
        if "http" in description.lower():
            # Simple URL extraction - you might want to use a more robust method
            words = description.split()
            for word in words:
                if word.startswith(("http://", "https://")):
                    url = word
                    break

        valid_input, error, user_data = input_validator.validate(api_key, "", description, url, cv_file)
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

    # Calculate processing time
    processing_time = time.time() - start_time
    st.session_state.processing_time = processing_time

    # Store in session_state
    st.session_state.letter = letter
    st.session_state.formatted = formatted

# Display output if available
if st.session_state.letter:
    st.header("📝 Generated Motivation Letter")
    st.markdown(st.session_state.formatted, unsafe_allow_html=True)
    
    # Display processing time
    if st.session_state.processing_time:
        st.info(f"⏱️ Processing time: {st.session_state.processing_time:.2f} seconds")

    with st.spinner("⬇️ Preparing downloads..."):
        download_generator.generate_buttons(st.session_state.letter)

# Footer
st.markdown("---")  # Add a horizontal line
st.markdown(
    '<div style="text-align: center; color: gray;">Powered by NickBiiyAI ❤️ May 4, 2025 😊</div>',
    unsafe_allow_html=True
)
