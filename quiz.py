# Quiz tab with difficulty + saving scores (Member 3)
import json
import streamlit as st
import db
from utils import MODEL, build_config


def make_quiz(client, level, language, topic, n, difficulty):
    r = client.models.generate_content(
        model=MODEL,
        contents=(
            f"Create {n} {difficulty}-difficulty multiple-choice questions on: {topic}. "
            "Return a JSON list. Each item must have keys: "
            "question, options (list of 4 strings), answer_index (0-3), explanation."
        ),
        config=build_config(level, language, json_output=True),
    )
    return json.loads(r.text)


def show(client, level, language):
    topic = st.text_input("Quiz topic", key="q_topic")
    difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"], value="Medium")
    n = st.slider("Number of questions", 3, 10, 5)

    if st.button("Create quiz 🎯"):
        if not topic.strip():
            st.warning("Topic ah enter pannunga.")
        else:
            try:
                with st.spinner("Quiz ready aagudhu..."):
                    st.session_state["quiz"] = make_quiz(client, level, language, topic, n, difficulty)
                    st.session_state["quiz_meta"] = {"topic": topic.strip(), "difficulty": difficulty}
                for k in list(st.session_state.keys()):
                    if k.startswith("ans_"):
                        del st.session_state[k]
            except Exception as e:
                st.error(f"Quiz create panna mudiyala, marubadiyum try pannunga. ({e})")

    quiz = st.session_state.get("quiz")
    if quiz:
        answers = []
        for i, q in enumerate(quiz):
            a = st.radio(f"{i + 1}. {q['question']}", q["options"], index=None, key=f"ans_{i}")
            answers.append(a)

        if st.button("Submit answers ✅"):
            score = 0
            for i, q in enumerate(quiz):
                correct = q["options"][q["answer_index"]]
                if answers[i] == correct:
                    score += 1
                    st.success(f"Q{i + 1}: Correct ✅")
                else:
                    st.error(f"Q{i + 1}: Correct answer: {correct}. {q['explanation']}")
            st.subheader(f"Your score: {score}/{len(quiz)}")
            meta = st.session_state.get("quiz_meta", {"topic": "General", "difficulty": "Medium"})
            db.save_score(st.session_state["user"], meta["topic"], meta["difficulty"], score, len(quiz))
            st.caption("Score save aagiduchu. Progress tab la paarunga.")
