import sqlite3

conn = sqlite3.connect(
    "gateway.db",
    check_same_thread=False
)

cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT,
    event_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


def save_log(event_type: str, event_message: str):

    cursor.execute(
        """
        INSERT INTO audit_logs
        (event_type, event_message)
        VALUES (?, ?)
        """,
        (event_type, event_message)
    )

    conn.commit()

def get_logs():

    cursor.execute(
        "SELECT * FROM audit_logs ORDER BY id DESC"
    )

    return cursor.fetchall()
def search_logs(keyword: str):

    cursor.execute(
        """
        SELECT *
        FROM audit_logs
        WHERE
            event_type LIKE ?
            OR event_message LIKE ?
        ORDER BY id DESC
        """,
        (f"%{keyword}%", f"%{keyword}%")
    )

    return cursor.fetchall()

def filter_logs(event_type: str):

    cursor.execute(
        """
        SELECT *
        FROM audit_logs
        WHERE event_type=?
        ORDER BY id DESC
        """,
        (event_type,)
    )

    return cursor.fetchall()

def get_all_logs():

    cursor.execute("""
        SELECT *
        FROM audit_logs
        ORDER BY id DESC
    """)

    return cursor.fetchall()

def get_total_events():
    cursor.execute(
        "SELECT COUNT(*) FROM audit_logs"
    )
    return cursor.fetchone()[0]


def get_event_count(event_type):
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM audit_logs
        WHERE event_type=?
        """,
        (event_type,)
    )

    return cursor.fetchone()[0]

def get_event_by_id(event_id: int):

    cursor.execute(
        """
        SELECT
            id,
            event_type,
            event_message,
            created_at,
            status,
            analyst_notes
        FROM audit_logs
        WHERE id = ?
        """,
        (event_id,)
    )

    return cursor.fetchone()






def update_investigation(event_id: int, status: str, analyst_notes: str):
    cursor.execute(
        """
        UPDATE audit_logs
        SET status = ?, analyst_notes = ?
        WHERE id = ?
        """,
        (status, analyst_notes, event_id)
    )

    conn.commit()


def add_investigation_columns():
    try:
        cursor.execute(
            "ALTER TABLE audit_logs ADD COLUMN status TEXT DEFAULT 'Open'"
        )
    except Exception:
        pass

    try:
        cursor.execute(
            "ALTER TABLE audit_logs ADD COLUMN analyst_notes TEXT DEFAULT ''"
        )
    except Exception:
        pass

    conn.commit()


add_investigation_columns()

