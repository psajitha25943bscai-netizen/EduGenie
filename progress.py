# Progress dashboard tab (Member 5)
import pandas as pd
import streamlit as st
import db


def show():
    rows = db.get_scores(st.session_state["user"])
    if not rows:
        st.info("Innum quiz ezhudhala. Quiz tab la oru quiz try pannunga.")
        return

    df = pd.DataFrame(rows, columns=["Date", "Topic", "Difficulty", "Score", "Total"])
    df["Percent"] = (df["Score"] / df["Total"] * 100).round(1)

    c1, c2, c3 = st.columns(3)
    c1.metric("Quizzes taken", len(df))
    c2.metric("Average %", f"{df['Percent'].mean():.1f}")
    c3.metric("Best %", f"{df['Percent'].max():.1f}")

    st.subheader("Score trend")
    st.line_chart(df["Percent"])

    st.subheader("History")
    st.dataframe(df, use_container_width=True)
