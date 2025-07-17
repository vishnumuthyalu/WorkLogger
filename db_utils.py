import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st
import os

# FORCE local SQLite regardless of secrets or env
DB_TYPE = "sqlite"
DB_URL = f"sqlite:///work_logs.db"  # relative file db in your app folder

# Create engine
engine = create_engine(DB_URL)

def init_db():
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS work_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_date TEXT UNIQUE,
            log_summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """))

def save_log_to_db(log_date, log_summary):
    with engine.begin() as conn:
        # Upsert behavior: replace existing log for the same date if any
        conn.execute(text("""
        INSERT INTO work_logs (log_date, log_summary)
        VALUES (:log_date, :log_summary)
        ON CONFLICT(log_date) DO UPDATE SET
          log_summary=excluded.log_summary,
          created_at=CURRENT_TIMESTAMP
        """), {"log_date": str(log_date), "log_summary": log_summary})

def get_all_logs():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM work_logs ORDER BY created_at DESC"))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df
