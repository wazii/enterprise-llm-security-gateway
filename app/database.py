import sqlite3
from datetime import datetime


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

def save_log(log_level: str, event_type: str, message: str, user_id: str = "system"):
    """
    Database me unique details ke sath security logs store karne ke liye function.
    event_type values: 'FAILED_LOGIN', 'API_VIOLATION', 'PROMPT_INJECTION', 'SYSTEM_ERROR', 'INFO'
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO audit_logs (timestamp, log_level, event_type, message, user_id) VALUES (?, ?, ?, ?, ?)",
        (timestamp, log_level, event_type, message, user_id)
    )
    conn.commit() 

def get_logs(event_type: str = None, limit: int = 100):
    """
    Audit and Security Reports ke liye database se logs nikalne ka function.
    """
    if event_type:
        cursor.execute("SELECT * FROM audit_logs WHERE event_type = ? ORDER BY timestamp DESC LIMIT ?", (event_type, limit))
    else:
        cursor.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
    
    return cursor.fetchall()