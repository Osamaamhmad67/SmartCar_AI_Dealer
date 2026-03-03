"""
utils/newsletter.py - Newsletter System
SmartCar AI-Dealer
"""
import sqlite3
from datetime import datetime
from config import Config
from utils.email_templates import EmailTemplates


class Newsletter:
    """Manage newsletter subscribers and campaigns"""

    @staticmethod
    def _ensure_table():
        conn = sqlite3.connect(Config.DB_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS newsletter (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                name TEXT,
                subscribed INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                sent_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit(); conn.close()

    @staticmethod
    def subscribe(email: str, name: str = None):
        Newsletter._ensure_table()
        conn = sqlite3.connect(Config.DB_PATH)
        try:
            conn.execute("INSERT OR REPLACE INTO newsletter (email, name, subscribed) VALUES (?, ?, 1)", (email, name))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def unsubscribe(email: str):
        conn = sqlite3.connect(Config.DB_PATH)
        conn.execute("UPDATE newsletter SET subscribed=0 WHERE email=?", (email,))
        conn.commit(); conn.close()

    @staticmethod
    def get_subscribers() -> list:
        Newsletter._ensure_table()
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM newsletter WHERE subscribed=1 ORDER BY created_at DESC").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def create_campaign(subject: str, body: str) -> int:
        Newsletter._ensure_table()
        conn = sqlite3.connect(Config.DB_PATH)
        cursor = conn.execute("INSERT INTO campaigns (subject, body) VALUES (?, ?)", (subject, body))
        campaign_id = cursor.lastrowid
        conn.commit(); conn.close()
        return campaign_id

    @staticmethod
    def get_campaigns() -> list:
        Newsletter._ensure_table()
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM campaigns ORDER BY created_at DESC LIMIT 20").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_stats() -> dict:
        Newsletter._ensure_table()
        conn = sqlite3.connect(Config.DB_PATH)
        total = conn.execute("SELECT COUNT(*) FROM newsletter WHERE subscribed=1").fetchone()[0]
        campaigns = conn.execute("SELECT COUNT(*) FROM campaigns").fetchone()[0]
        conn.close()
        return {'subscribers': total, 'campaigns': campaigns}
