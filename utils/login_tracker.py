"""
utils/login_tracker.py - Login Session Tracker
SmartCar AI-Dealer - سجل تسجيل الدخول
"""
import sqlite3
from datetime import datetime
from config import Config


class LoginTracker:
    """Track user login sessions and devices"""

    @staticmethod
    def _ensure_table():
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS login_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT,
                action TEXT DEFAULT 'login',
                ip_address TEXT,
                user_agent TEXT,
                success INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit(); conn.close()

    @staticmethod
    def log_login(user_id: int, username: str, success: bool = True, ip: str = None, agent: str = None):
        LoginTracker._ensure_table()
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.execute("INSERT INTO login_sessions (user_id, username, action, success, ip_address, user_agent) VALUES (?,?,?,?,?,?)",
                     (user_id, username, 'login', 1 if success else 0, ip, agent))
        conn.commit(); conn.close()

    @staticmethod
    def log_logout(user_id: int, username: str):
        LoginTracker._ensure_table()
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.execute("INSERT INTO login_sessions (user_id, username, action) VALUES (?,?,?)",
                     (user_id, username, 'logout'))
        conn.commit(); conn.close()

    @staticmethod
    def get_session_history(user_id: int = None, limit: int = 50) -> list:
        LoginTracker._ensure_table()
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        
        if user_id:
            rows = conn.execute("SELECT * FROM login_sessions WHERE user_id=? ORDER BY created_at DESC LIMIT ?",
                               (user_id, limit)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM login_sessions ORDER BY created_at DESC LIMIT ?",
                               (limit,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_failed_attempts(hours: int = 24) -> list:
        LoginTracker._ensure_table()
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT username, COUNT(*) as attempts, MAX(created_at) as last_attempt
            FROM login_sessions 
            WHERE success=0 AND created_at >= datetime('now', ?)
            GROUP BY username ORDER BY attempts DESC
        """, (f'-{hours} hours',)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_active_today() -> int:
        LoginTracker._ensure_table()
        conn = sqlite3.connect(Config.DATABASE_PATH)
        row = conn.execute("SELECT COUNT(DISTINCT user_id) FROM login_sessions WHERE action='login' AND success=1 AND created_at >= date('now')").fetchone()
        conn.close()
        return row[0] if row else 0
