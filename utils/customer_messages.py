"""
utils/customer_messages.py - Customer-Company Messaging
SmartCar AI-Dealer - رسائل العملاء
"""
import sqlite3
from datetime import datetime
from config import Config


class CustomerMessages:
    """Internal messaging between customers and company"""

    @staticmethod
    def _ensure_table():
        conn = sqlite3.connect(Config.DB_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER NOT NULL,
                sender_name TEXT,
                receiver_id INTEGER,
                subject TEXT,
                body TEXT NOT NULL,
                is_read INTEGER DEFAULT 0,
                reply_to INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit(); conn.close()

    @staticmethod
    def send(sender_id: int, sender_name: str, body: str, subject: str = None, receiver_id: int = None, reply_to: int = None):
        CustomerMessages._ensure_table()
        conn = sqlite3.connect(Config.DB_PATH)
        conn.execute("INSERT INTO messages (sender_id, sender_name, receiver_id, subject, body, reply_to) VALUES (?,?,?,?,?,?)",
                     (sender_id, sender_name, receiver_id, subject, body, reply_to))
        conn.commit(); conn.close()

    @staticmethod
    def get_inbox(user_id: int, is_admin: bool = False) -> list:
        CustomerMessages._ensure_table()
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        if is_admin:
            rows = conn.execute("SELECT * FROM messages ORDER BY created_at DESC LIMIT 50").fetchall()
        else:
            rows = conn.execute("SELECT * FROM messages WHERE sender_id=? OR receiver_id=? ORDER BY created_at DESC LIMIT 50",
                               (user_id, user_id)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def mark_read(message_id: int):
        conn = sqlite3.connect(Config.DB_PATH)
        conn.execute("UPDATE messages SET is_read=1 WHERE id=?", (message_id,))
        conn.commit(); conn.close()

    @staticmethod
    def get_unread_count(user_id: int, is_admin: bool = False) -> int:
        CustomerMessages._ensure_table()
        conn = sqlite3.connect(Config.DB_PATH)
        if is_admin:
            row = conn.execute("SELECT COUNT(*) FROM messages WHERE is_read=0").fetchone()
        else:
            row = conn.execute("SELECT COUNT(*) FROM messages WHERE (receiver_id=? OR (receiver_id IS NULL AND sender_id!=?)) AND is_read=0",
                               (user_id, user_id)).fetchone()
        conn.close()
        return row[0] if row else 0

    @staticmethod
    def render_messaging_ui():
        """Render messaging UI in Streamlit"""
        import streamlit as st
        from utils.i18n import t
        
        user = st.session_state.get('user', {})
        is_admin = user.get('role') == 'admin'
        
        st.markdown(f"### 💬 {t('messages.title', 'Messages')}")
        
        # Compose
        with st.expander(f"✍️ {t('messages.compose', 'New Message')}", expanded=False):
            with st.form("msg_form"):
                subject = st.text_input(t('messages.subject', 'Subject'), key="msg_subj")
                body = st.text_area(t('messages.body', 'Message'), key="msg_body")
                if st.form_submit_button(f"📨 {t('messages.send', 'Send')}", use_container_width=True, type="primary"):
                    if body:
                        CustomerMessages.send(user['id'], user.get('full_name', user.get('username', '')), body, subject)
                        st.success(f"✅ {t('messages.sent', 'Message sent!')}")
                        st.rerun()
        
        # Inbox
        messages = CustomerMessages.get_inbox(user['id'], is_admin)
        for msg in messages:
            read_style = '' if msg['is_read'] else 'border-left: 3px solid #D4AF37;'
            date = msg['created_at'][:16] if msg['created_at'] else ''
            st.markdown(f"""
            <div style="background: #16213e; padding: 10px; border-radius: 8px; margin: 5px 0; {read_style}">
                <b style="color: #D4AF37;">{msg['subject'] or 'No Subject'}</b>
                <span style="color: #a0a0c0; float: right; font-size: 0.8em;">{date}</span><br>
                <span style="color: #a0a0c0; font-size: 0.85em;">👤 {msg['sender_name'] or 'Unknown'}</span><br>
                <span style="color: white;">{msg['body'][:200]}</span>
            </div>
            """, unsafe_allow_html=True)
            if not msg['is_read']:
                CustomerMessages.mark_read(msg['id'])
        
        if not messages:
            st.info(t('messages.empty', 'No messages yet'))
