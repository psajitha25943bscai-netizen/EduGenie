# Database + login (Member 1 - Team Lead)
import sqlite3
import hashlib
import os
from datetime import datetime

DB_FILE = "edugenie.db"


def _conn():
    return sqlite3.connect(DB_FILE)


def init_db():
    with _conn() as c:
        c.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "username TEXT PRIMARY KEY, salt TEXT, pw_hash TEXT)"
        )
        c.execute(
            "CREATE TABLE IF NOT EXISTS scores ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, topic TEXT, "
            "difficulty TEXT, score INTEGER, total INTEGER, ts TEXT)"
        )


def _hash(password: str, salt: str) -> str:
    return hashlib.sha256((salt + password).encode()).hexdigest()


def register(username: str, password: str):
    username = username.strip()
    if not username or not password:
        return False, "Username and password rendum venum."
    with _conn() as c:
        if c.execute("SELECT 1 FROM users WHERE username=?", (username,)).fetchone():
            return False, "Andha username already irukku."
        salt = os.urandom(8).hex()
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, salt, _hash(password, salt)))
    return True, "Account create aagiduchu! Ippo login pannunga."


def login(username: str, password: str) -> bool:
    with _conn() as c:
        row = c.execute(
            "SELECT salt, pw_hash FROM users WHERE username=?", (username.strip(),)
        ).fetchone()
    return bool(row) and _hash(password, row[0]) == row[1]


def save_score(username, topic, difficulty, score, total):
    with _conn() as c:
        c.execute(
            "INSERT INTO scores (username, topic, difficulty, score, total, ts) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (username, topic, difficulty, score, total, datetime.now().strftime("%Y-%m-%d %H:%M")),
        )


def get_scores(username):
    with _conn() as c:
        return c.execute(
            "SELECT ts, topic, difficulty, score, total FROM scores "
            "WHERE username=? ORDER BY id",
            (username,),
        ).fetchall()
