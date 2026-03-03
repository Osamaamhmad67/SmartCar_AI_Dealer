"""
components/notifications_bell.py - In-App Push Notifications
SmartCar AI-Dealer - إشعارات داخل التطبيق
"""
import streamlit as st
import sqlite3
from datetime import datetime
from config import Config
from utils.i18n import t


def _ensure_notifications_table():
    conn = sqlite3.connect(Config.DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            message TEXT,
            type TEXT DEFAULT 'info',
            read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def push_notification(user_id: int, title: str, message: str, notif_type: str = 'info'):
    """Create a new notification for a user"""
    _ensure_notifications_table()
    conn = sqlite3.connect(Config.DB_PATH)
    conn.execute("INSERT INTO notifications (user_id, title, message, type) VALUES (?, ?, ?, ?)",
                 (user_id, title, message, notif_type))
    conn.commit()
    conn.close()


def render_notification_bell():
    """Render notification bell in sidebar"""
    _ensure_notifications_table()
    user = st.session_state.get('user', {})
    if not user:
        return
    
    user_id = user.get('id')
    conn = sqlite3.connect(Config.DB_PATH)
    conn.row_factory = sqlite3.Row
    
    unread = conn.execute("SELECT COUNT(*) as cnt FROM notifications WHERE user_id=? AND read=0", (user_id,)).fetchone()['cnt']
    notifications = conn.execute("SELECT * FROM notifications WHERE user_id=? ORDER BY created_at DESC LIMIT 10", (user_id,)).fetchall()
    conn.close()
    
    with st.sidebar:
        badge = f" ({unread})" if unread > 0 else ""
        if st.button(f"🔔{badge} {t('notifications.title', 'Notifications')}", use_container_width=True,
                    type="primary" if unread > 0 else "secondary"):
            st.session_state['show_notifications'] = not st.session_state.get('show_notifications', False)
            # Mark all as read
            if unread > 0:
                conn2 = sqlite3.connect(Config.DB_PATH)
                conn2.execute("UPDATE notifications SET read=1 WHERE user_id=? AND read=0", (user_id,))
                conn2.commit(); conn2.close()
            st.rerun()
    
    if st.session_state.get('show_notifications', False):
        st.markdown(f"### 🔔 {t('notifications.title', 'Notifications')}")
        
        type_icons = {'info': 'ℹ️', 'success': '✅', 'warning': '⚠️', 'error': '❌', 'payment': '💰'}
        type_colors = {'info': '#3498db', 'success': '#27ae60', 'warning': '#f39c12', 'error': '#e74c3c', 'payment': '#9b59b6'}
        
        for n in notifications:
            icon = type_icons.get(n['type'], 'ℹ️')
            color = type_colors.get(n['type'], '#3498db')
            read_style = 'opacity: 0.6;' if n['read'] else ''
            date = n['created_at'][:16] if n['created_at'] else ''
            
            st.markdown(f"""
            <div style="background: #16213e; padding: 10px; border-radius: 8px; margin: 5px 0; border-left: 3px solid {color}; {read_style}">
                <b style="color: {color};">{icon} {n['title']}</b>
                <span style="color: #a0a0c0; font-size: 0.75em; float: right;">{date}</span><br>
                <span style="color: #a0a0c0; font-size: 0.85em;">{n['message'] or ''}</span>
            </div>
            """, unsafe_allow_html=True)
        
        if not notifications:
            st.info(t('notifications.empty', 'No notifications'))
