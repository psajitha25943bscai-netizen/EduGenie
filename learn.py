# Learn tab (Member 2)
import streamlit as st
from utils import MODEL, build_config

PROMPTS = {
    "Explain a topic": "Explain this topic clearly with an example and a short summary: {t}",
    "7-day study plan": "Create a 7-day study plan to learn: {t}. Give daily goals and practice tasks.",
    "Revision notes": "Write concise revision notes with key points for: {t}",
}


def show(client, level, language):
    config = build_config(level, language)
    mode = st.selectbox("What do you want?", list(PROMPTS.keys()))
    topic = st.text_input("Topic", placeholder="e.g. Photosynthesis, Python loops")

    if st.button("Generate ✨", key="learn_btn"):
        if not topic.strip():
            st.warning("Topic ah enter pannunga.")
        else:
            try:
                with st.spinner("EduGenie yosikkudhu..."):
                    r = client.models.generate_content(
                        model=MODEL,
                        contents=PROMPTS[mode].format(t=topic),
                        config=config,
                    )
                    st.session_state["learn_out"] = r.text
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.get("learn_out"):
        st.markdown(st.session_state["learn_out"])
        st.download_button(
            "⬇️ Download notes",
            st.session_state["learn_out"],
            file_name="edugenie_notes.md",
        )
