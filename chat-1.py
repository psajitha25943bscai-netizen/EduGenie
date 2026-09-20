# Chat tab: memory chat + ask questions about the uploaded PDF (Member 4)
# The conversation history is kept in st.session_state and sent to Gemini on every message.
import streamlit as st
from google.genai import types
from utils import MODEL, build_config


def to_contents(msgs):
    return [
        types.Content(
            role="user" if m["role"] == "user" else "model",
            parts=[types.Part(text=m["content"])],
        )
        for m in msgs
    ]


def show(client, level, language):
    if "msgs" not in st.session_state:
        st.session_state.msgs = []

    use_pdf = False
    if st.session_state.get("pdf_bytes"):
        use_pdf = st.checkbox(f"📄 Ask about my PDF ({st.session_state.get('pdf_name', 'PDF')})")

    for m in st.session_state.msgs:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Unga doubt ah kelunga..."):
        st.session_state.msgs.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        try:
            contents = to_contents(st.session_state.msgs)
            if use_pdf:
                pdf_part = types.Part.from_bytes(
                    data=st.session_state["pdf_bytes"], mime_type="application/pdf"
                )
                contents[-1].parts = [pdf_part] + list(contents[-1].parts)
            reply = client.models.generate_content(
                model=MODEL,
                contents=contents,
                config=build_config(level, language),
            ).text
        except Exception as e:
            st.session_state.msgs.pop()
            st.error(f"Error: {e}")
        else:
            st.session_state.msgs.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.markdown(reply)

    if st.button("🗑️ Clear chat"):
        st.session_state.msgs = []
        st.rerun()
