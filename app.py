# Main file (Member 1 - Team Lead). Run: streamlit run app.py
import os
import streamlit as st
import db
from utils import get_client
import learn
import pdf_summary
import quiz
import chat
import progress

st.set_page_config(page_title="EduGenie Pro", page_icon="🧞", layout="wide")
db.init_db()

st.title("🧞 EduGenie Pro")
st.caption("Google Gemini Powered Learning Assistant")

# ---------------- Login / Register ----------------
if "user" not in st.session_state:
    st.session_state["user"] = None

if not st.session_state["user"]:
    t_login, t_reg = st.tabs(["Login", "Register"])
    with t_login:
        u = st.text_input("Username", key="login_user")
        p = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if db.login(u, p):
                st.session_state["user"] = u.strip()
                st.rerun()
            else:
                st.error("Username or password thappu.")
    with t_reg:
        ru = st.text_input("New username", key="reg_user")
        rp = st.text_input("New password", type="password", key="reg_pass")
        if st.button("Create account"):
            ok, msg = db.register(ru, rp)
            (st.success if ok else st.error)(msg)
    st.stop()

# ---------------- Sidebar ----------------
st.sidebar.write(f"👤 {st.session_state['user']}")
if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

api_key = st.sidebar.text_input(
    "Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", "")
)
level = st.sidebar.selectbox("Your level", ["Beginner", "Intermediate", "Advanced"])
language = st.sidebar.selectbox("Language", ["English", "Tamil", "Hindi"])

if not api_key:
    st.info("Sidebar la Gemini API key podunga.")
    st.stop()

client = get_client(api_key)

# ---------------- Tabs ----------------
tabs = st.tabs(["📖 Learn", "📄 PDF Summary", "📝 Quiz", "💬 Chat", "📊 Progress"])
with tabs[0]:
    learn.show(client, level, language)
with tabs[1]:
    pdf_summary.show(client, level, language)
with tabs[2]:
    quiz.show(client, level, language)
with tabs[3]:
    chat.show(client, level, language)
with tabs[4]:
    progress.show()
