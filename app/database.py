import sqlite3
import os
from datetime import datetime


DATABASE_URL = os.getenv("DATABASE_URL", "gateway.db")
IS_POSTGRES = DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://")

def init_db():
    if not IS_POSTGRES:
        conn = sqlite3.connect("gateway.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            log_level TEXT,
            event_type TEXT,
            message TEXT,
            user_id TEXT
        )
        """)
        conn.commit()
        conn.close()
    else:
        
        import psycopg2
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            log_level TEXT,
            event_type TEXT,
            message TEXT,
            user_id TEXT
        )
        """)
        conn.commit()
        conn.close()


if not IS_POSTGRES:
    init_db()

def save_log(log_level: str, event_type: str, message: str, user_id: str = "system"):
    """
    Database me unique details ke sath security logs store karne ka function.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not IS_POSTGRES:
        conn = sqlite3.connect("gateway.db", check_same_thread=False)
        cursor = conn.cursor()
    
        cursor.execute(
            "INSERT INTO audit_logs (timestamp, log_level, event_type, message, user_id) VALUES (?, ?, ?, ?, ?)",
            (timestamp, log_level, event_type, message, user_id)
        )
        conn.commit()
        conn.close()
    else:
        import psycopg2
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO audit_logs (timestamp, log_level, event_type, message, user_id) VALUES (%s, %s, %s, %s, %s)",
            (timestamp, log_level, event_type, message, user_id)
        )
        conn.commit()
        conn.close()

def get_logs(event_type: str = None, limit: int = 100):
    """
    Audit and Security Reports ke liye database se logs nikalne ka function.
    """

    param = "%s" if IS_POSTGRES else "?"
    
    if not IS_POSTGRES:
        conn = sqlite3.connect("gateway.db", check_same_thread=False)
    else:
        import psycopg2
        conn = psycopg2.connect(DATABASE_URL)
        
    cursor = conn.cursor()
    
    if event_type:
        query = f"SELECT id, timestamp, log_level, event_type, message, user_id FROM audit_logs WHERE event_type = {param} ORDER BY timestamp DESC LIMIT {param}"
        cursor.execute(query, (event_type, limit))
    else:
        query = f"SELECT id, timestamp, log_level, event_type, message, user_id FROM audit_logs ORDER BY timestamp DESC LIMIT {param}"
        cursor.execute(query, (limit,))
        
    logs = cursor.fetchall()
    conn.close()
    return logs