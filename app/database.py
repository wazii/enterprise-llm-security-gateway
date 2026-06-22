import sqlite3
import os
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "gateway.db")
IS_POSTGRES = DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://")

def init_db():
    try:
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
    except Exception as e:
        print(f"[DB ERROR] Initialization failed: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if not IS_POSTGRES:
    init_db()

def save_log(log_level: str, event_type: str, message: str, user_id: str = "system"):
    """
    Database me unique details ke sath security logs store karne ka function.
    Supports graceful failover to avoid breaking the gateway app.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = None
    
    try:
        if not IS_POSTGRES:
            conn = sqlite3.connect("gateway.db", check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO audit_logs (timestamp, log_level, event_type, message, user_id) VALUES (?, ?, ?, ?, ?)",
                (timestamp, log_level, event_type, message, user_id)
            )
            conn.commit()
        else:
            import psycopg2
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO audit_logs (timestamp, log_level, event_type, message, user_id) VALUES (%s, %s, %s, %s, %s)",
                (timestamp, log_level, event_type, message, user_id)
            )
            conn.commit()
    except Exception as e:
        print(f"[DB ERROR] Failed to save log: {e}")
    finally:
        if conn:
            conn.close()

def get_logs(event_type: str = None, limit: int = 100):
    """
    Audit and Security Reports ke liye database se logs nikalne ka function.
    Returns clean dictionaries instead of raw tuples.
    """
    param = "%s" if IS_POSTGRES else "?"
    conn = None
    structured_logs = []
    
    try:
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
            
        raw_logs = cursor.fetchall()
        
        
        for row in raw_logs:
            structured_logs.append({
                "id": row[0],
                "timestamp": str(row[1]),
                "log_level": row[2],
                "event_type": row[3],
                "message": row[4],
                "user_id": row[5]
            })
            
    except Exception as e:
        print(f"[DB ERROR] Failed to fetch logs: {e}")
    finally:
        if conn:
            conn.close()
            
    return structured_logs