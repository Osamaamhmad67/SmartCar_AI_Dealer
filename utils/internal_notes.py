"""
utils/internal_notes.py - Internal Notes System
SmartCar AI-Dealer - ملاحظات داخلية للموظفين
"""
import sqlite3
from datetime import datetime
from config import Config


class InternalNotes:
    """Internal notes visible only to employees"""

    @staticmethod
    def _ensure_table():
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS internal_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_type TEXT NOT NULL,
                entity_id INTEGER NOT NULL,
                user_id INTEGER,
                username TEXT,
                note TEXT NOT NULL,
                priority TEXT DEFAULT 'normal',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit(); conn.close()

    @staticmethod
    def add_note(entity_type: str, entity_id: int, note: str, user_id: int = None, username: str = None, priority: str = 'normal'):
        InternalNotes._ensure_table()
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.execute("INSERT INTO internal_notes (entity_type, entity_id, user_id, username, note, priority) VALUES (?,?,?,?,?,?)",
                     (entity_type, entity_id, user_id, username, note, priority))
        conn.commit(); conn.close()

    @staticmethod
    def get_notes(entity_type: str, entity_id: int) -> list:
        InternalNotes._ensure_table()
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM internal_notes WHERE entity_type=? AND entity_id=? ORDER BY created_at DESC",
                           (entity_type, entity_id)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def delete_note(note_id: int):
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.execute("DELETE FROM internal_notes WHERE id=?", (note_id,))
        conn.commit(); conn.close()

    @staticmethod
    def render_notes_section(entity_type: str, entity_id: int):
        """Render notes UI section in Streamlit"""
        import streamlit as st
        from utils.i18n import t
        
        st.markdown(f"#### 📝 {t('notes.internal', 'Internal Notes')}")
        
        user = st.session_state.get('user', {})
        
        # Add note form
        with st.form(f"note_form_{entity_type}_{entity_id}"):
            nc1, nc2 = st.columns([3, 1])
            with nc1:
                new_note = st.text_input(t('notes.add', 'Add note'), key=f"note_txt_{entity_type}_{entity_id}")
            with nc2:
                priority = st.selectbox("Priority", ['normal', 'high', 'urgent'], key=f"note_pri_{entity_type}_{entity_id}")
            
            if st.form_submit_button(f"➕ {t('notes.save', 'Save')}", use_container_width=True):
                if new_note:
                    InternalNotes.add_note(entity_type, entity_id, new_note,
                        user.get('id'), user.get('username', ''), priority)
                    st.rerun()
        
        # Show notes
        notes = InternalNotes.get_notes(entity_type, entity_id)
        priority_colors = {'normal': '#3498db', 'high': '#f39c12', 'urgent': '#e74c3c'}
        
        for n in notes:
            color = priority_colors.get(n['priority'], '#3498db')
            date = n['created_at'][:16] if n['created_at'] else ''
            st.markdown(f"""
            <div style="background: #16213e; padding: 8px 12px; border-radius: 8px; margin: 4px 0; border-left: 3px solid {color};">
                <span style="color: white;">{n['note']}</span>
                <span style="color: #a0a0c0; font-size: 0.75em; float: right;">👤 {n['username'] or '-'} | {date}</span>
            </div>
            """, unsafe_allow_html=True)
