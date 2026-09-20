# Chat tab: memory chat + ask questions about the uploaded PDF (Member 4)
import streamlit as st
from google.genai import types
from utils import MODEL, build_config


def show(client, level, language):
    if "chat" not in st.session_state:
        st.session_state.chat = client.chats.create(
            model=MODEL, config=build_config(level, language)
        )
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
            if use_pdf:
                pdf_part = types.Part.from_bytes(
                    data=st.session_state["pdf_bytes"], mime_type="application/pdf"
                )
                reply = client.models.generate_content(
                    model=MODEL,
                    contents=[pdf_part, prompt],
                    config=build_config(level, language),
                ).text
            else:
                reply = st.session_state.chat.send_message(prompt).text
        except Exception as e:
            reply = f"Error: {e}"
        st.session_state.msgs.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)

    if st.button("🗑️ Clear chat"):
        del st.session_state["chat"]
        st.session_state.msgs = []
        st.rerun()
