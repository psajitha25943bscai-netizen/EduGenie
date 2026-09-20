# 🧞 EduGenie Pro (Tough Version)

AI learning assistant with login, database, PDF analysis and progress tracking.
Built with Google Gemini, Streamlit and SQLite.

## Features
- **Login / Register** (passwords stored as salted hashes in SQLite)
- **Learn**: explain, study plan, notes
- **PDF Summary**: upload a PDF, get summary / key points / exam questions
- **Quiz**: difficulty levels, scoring, scores saved per user
- **Chat**: tutor with memory + ask questions about the uploaded PDF
- **Progress**: dashboard with average, best score, trend chart and history

## Project Structure
```
3_Tough/
├── app.py            main app, login, tabs
├── utils.py          Gemini settings
├── db.py             SQLite database + login
├── learn.py          Learn tab
├── pdf_summary.py    PDF Summary tab
├── quiz.py           Quiz tab
├── chat.py           Chat tab
├── progress.py       Progress dashboard
├── requirements.txt
└── README.md
```

## Team Members & Roles
| Member | Role | Files |
|---|---|---|
| Member 1 | Team Lead, login + database, integration | app.py, utils.py, db.py |
| Member 2 | Learn + PDF Summary | learn.py, pdf_summary.py |
| Member 3 | Quiz with difficulty + saving scores | quiz.py |
| Member 4 | Chat + PDF Q&A | chat.py |
| Member 5 | Progress dashboard, documentation, testing, demo video | progress.py, README.md |

## How to Run
1. Get a free API key from https://aistudio.google.com
2. `pip install -r requirements.txt`
3. Set `GEMINI_API_KEY` (or paste the key in the sidebar)
4. `streamlit run app.py`

## Screenshots
Add screenshots of every tab here.
