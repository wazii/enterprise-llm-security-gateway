import sqlite3

conn = sqlite3.connect(
    "gateway.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event TEXT
)
""")

conn.commit()


def save_log(event: str):
    cursor.execute(
        "INSERT INTO audit_logs (event) VALUES (?)",
        (event,)
    )
    conn.commit()