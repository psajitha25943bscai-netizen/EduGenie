# PDF Summary tab (Member 2)
# Saves the uploaded PDF in st.session_state["pdf_bytes"] so chat.py (Member 4) can use it too.
import streamlit as st
from google.genai import types
from utils import MODEL, build_config

TASKS = {
    "Short summary": "Summarize this document in simple points.",
    "Key points": "List the most important key points from this document.",
    "5 exam questions": "Create 5 exam questions with answers from this document.",
}


def show(client, level, language):
    f = st.file_uploader("Upload a PDF", type=["pdf"])
    if f is not None:
        st.session_state["pdf_bytes"] = f.getvalue()
        st.session_state["pdf_name"] = f.name
        st.success(f"Uploaded: {f.name}")

    task = st.selectbox("What do you want?", list(TASKS.keys()))

    if st.button("Analyze PDF 📄"):
        pdf_bytes = st.session_state.get("pdf_bytes")
        if not pdf_bytes:
            st.warning("Munnadi oru PDF upload pannunga.")
            return
        try:
            with st.spinner("PDF padikkudhu..."):
                pdf_part = types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")
                r = client.models.generate_content(
                    model=MODEL,
                    contents=[pdf_part, TASKS[task]],
                    config=build_config(level, language),
                )
                st.session_state["pdf_out"] = r.text
        except Exception as e:
            st.error(f"Error: {e}")

    if st.session_state.get("pdf_out"):
        st.markdown(st.session_state["pdf_out"])
        st.download_button("⬇️ Download", st.session_state["pdf_out"], file_name="pdf_notes.md")
