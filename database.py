import sqlite3
import hashlib
import secrets
from datetime import datetime

DB_PATH = "chat_history.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL DEFAULT 'student',
            api_key_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            sender TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Admin API keys table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_hash TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL,
            label TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )
    """)

    conn.commit()
    conn.close()


def save_message(session_id: str, sender: str, content: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (session_id, sender, content)
        VALUES (?, ?, ?)
    """, (session_id, sender, content))
    conn.commit()
    conn.close()


def get_chat_history(session_id: str) -> list:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sender, content FROM messages
        WHERE session_id = ?
        ORDER BY timestamp ASC
        LIMIT 50
    """, (session_id,))

    messages = []
    for row in cursor.fetchall():
        messages.append({
            "role": row["sender"],
            "content": row["content"]
        })

    conn.close()
    return messages


def create_session(session_id: str, role: str):
    """Naya session database mein register karo."""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO sessions (session_id, role)
            VALUES (?, ?)
        """, (session_id, role))
        conn.commit()
    finally:
        conn.close()


def get_session_role(session_id: str) -> str | None:
    """Session ka registered role wapas lo."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role FROM sessions WHERE session_id = ?", (session_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row["role"] if row else None


def hash_key(raw_key: str) -> str:
    return hashlib.sha256(raw_key.encode()).hexdigest()


def verify_api_key(raw_key: str) -> str | None:
    """
    API key verify karo.
    Valid hone par role return karo, warna None.
    """
    key_hash = hash_key(raw_key)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT role FROM api_keys
        WHERE key_hash = ? AND is_active = 1
    """, (key_hash,))
    row = cursor.fetchone()
    conn.close()
    return row["role"] if row else None


def create_api_key(role: str, label: str = "") -> str:
    """Naya API key generate karo (sirf setup ke liye)."""
    raw_key = secrets.token_urlsafe(32)
    key_hash = hash_key(raw_key)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO api_keys (key_hash, role, label)
        VALUES (?, ?, ?)
    """, (key_hash, role, label))
    conn.commit()
    conn.close()
    return raw_key
