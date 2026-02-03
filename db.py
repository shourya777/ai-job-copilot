import sqlite3
from datetime import datetime

DB_PATH = "runs.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        # Create table if it doesn't exist (fresh installs)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            company TEXT,
            role_title TEXT,
            cv_text TEXT NOT NULL,
            jd_text TEXT NOT NULL
        )
        """)
        conn.commit()

        # Migration: add ai_summary column if missing (existing installs)
        cur = conn.execute("PRAGMA table_info(runs)")
        cols = [row[1] for row in cur.fetchall()]
        if "ai_summary" not in cols:
            conn.execute("ALTER TABLE runs ADD COLUMN ai_summary TEXT")
            conn.commit()

def save_run(company: str, role_title: str, cv_text: str, jd_text: str):
    created_at = datetime.utcnow().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO runs (created_at, company, role_title, cv_text, jd_text)
            VALUES (?, ?, ?, ?, ?)
        """, (created_at, company, role_title, cv_text, jd_text))
        conn.commit()

def save_run_with_ai(company: str, role_title: str, cv_text: str, jd_text: str, ai_summary: str):
    created_at = datetime.utcnow().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO runs (created_at, company, role_title, cv_text, jd_text, ai_summary)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (created_at, company, role_title, cv_text, jd_text, ai_summary))
        conn.commit()

def get_recent_runs(limit: int = 10):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("""
            SELECT run_id, created_at, company, role_title
            FROM runs
            ORDER BY run_id DESC
            LIMIT ?
        """, (limit,))
        return cur.fetchall()

def get_ai_summary(run_id: int) -> str:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT ai_summary FROM runs WHERE run_id = ?", (run_id,))
        row = cur.fetchone()
        return row[0] if row and row[0] else ""
