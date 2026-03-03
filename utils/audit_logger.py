"""
utils/audit_logger.py - Audit Log System
SmartCar AI-Dealer
"""
import sqlite3, json
from datetime import datetime
from config import Config


class AuditLogger:
    """تسجيل جميع العمليات المهمة"""

    @staticmethod
    def log(action, user_id=None, username=None, entity_type=None, entity_id=None, details=None):
        try:
            import streamlit as st
            if not user_id and st.session_state.get('user'):
                user_id = st.session_state.user.get('id')
                username = username or st.session_state.user.get('username', '')
        except Exception:
            pass
        details_json = json.dumps(details, ensure_ascii=False) if details else None
        try:
            conn = sqlite3.connect(Config.DB_PATH)
            conn.execute(
                "INSERT INTO audit_log (user_id,username,action,entity_type,entity_id,details,created_at) VALUES (?,?,?,?,?,?,?)",
                (user_id, username, action, entity_type, str(entity_id) if entity_id else None, details_json, datetime.now().isoformat()))
            conn.commit()
            conn.close()
        except Exception as e:
            if Config.logger: Config.logger.error(f"Audit: {e}")

    @staticmethod
    def get_logs(limit=100, action_filter=None, user_filter=None):
        try:
            conn = sqlite3.connect(Config.DB_PATH)
            q, p = "SELECT * FROM audit_log WHERE 1=1", []
            if action_filter: q += " AND action=?"; p.append(action_filter)
            if user_filter: q += " AND username LIKE ?"; p.append(f"%{user_filter}%")
            q += " ORDER BY created_at DESC LIMIT ?"; p.append(limit)
            c = conn.cursor(); c.execute(q, p)
            cols = [d[0] for d in c.description]
            rows = [dict(zip(cols, r)) for r in c.fetchall()]
            conn.close(); return rows
        except Exception: return []

    @staticmethod
    def get_stats():
        try:
            conn = sqlite3.connect(Config.DB_PATH); c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM audit_log"); total = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM audit_log WHERE created_at >= date('now','-1 day')"); today = c.fetchone()[0]
            c.execute("SELECT action,COUNT(*) as cnt FROM audit_log GROUP BY action ORDER BY cnt DESC LIMIT 5"); top = c.fetchall()
            conn.close(); return {'total': total, 'today': today, 'top_actions': top}
        except Exception: return {'total': 0, 'today': 0, 'top_actions': []}
