"""
utils/tags_system.py - Car Tagging System
SmartCar AI-Dealer - نظام الوسوم
"""
import sqlite3
from config import Config


class TagsSystem:
    """Tag cars with custom labels for organization"""

    @staticmethod
    def _ensure_table():
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS car_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id INTEGER NOT NULL,
                tag TEXT NOT NULL,
                color TEXT DEFAULT '#D4AF37',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit(); conn.close()

    PRESET_TAGS = [
        ('⭐ Premium', '#D4AF37'),
        ('🔥 Hot Deal', '#e74c3c'),
        ('🆕 New Arrival', '#27ae60'),
        ('📉 Price Drop', '#3498db'),
        ('🏆 Best Seller', '#9b59b6'),
        ('⚡ Quick Sale', '#f39c12'),
        ('🔧 Needs Service', '#e67e22'),
        ('📸 Photo Ready', '#1abc9c'),
    ]

    @staticmethod
    def add_tag(transaction_id: int, tag: str, color: str = '#D4AF37'):
        TagsSystem._ensure_table()
        conn = sqlite3.connect(Config.DATABASE_PATH)
        # Avoid duplicates
        existing = conn.execute("SELECT id FROM car_tags WHERE transaction_id=? AND tag=?", (transaction_id, tag)).fetchone()
        if not existing:
            conn.execute("INSERT INTO car_tags (transaction_id, tag, color) VALUES (?,?,?)", (transaction_id, tag, color))
            conn.commit()
        conn.close()

    @staticmethod
    def remove_tag(transaction_id: int, tag: str):
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.execute("DELETE FROM car_tags WHERE transaction_id=? AND tag=?", (transaction_id, tag))
        conn.commit(); conn.close()

    @staticmethod
    def get_tags(transaction_id: int) -> list:
        TagsSystem._ensure_table()
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM car_tags WHERE transaction_id=?", (transaction_id,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_cars_by_tag(tag: str) -> list:
        TagsSystem._ensure_table()
        conn = sqlite3.connect(Config.DATABASE_PATH)
        rows = conn.execute("SELECT transaction_id FROM car_tags WHERE tag=?", (tag,)).fetchall()
        conn.close()
        return [r[0] for r in rows]

    @staticmethod
    def render_tags_html(tags: list) -> str:
        html = ""
        for t in tags:
            color = t.get('color', '#D4AF37')
            html += f'<span style="background:{color}22; color:{color}; padding:2px 8px; border-radius:12px; font-size:0.8em; margin:2px;">{t["tag"]}</span> '
        return html
