"""
utils/document_archive.py - Document Archive System
SmartCar AI-Dealer - أرشيف المستندات
"""
import sqlite3, os, base64
from datetime import datetime
from config import Config


class DocumentArchive:
    """Upload and archive car documents (TÜV, registration, insurance)"""

    DOC_TYPES = ['TÜV', 'Fahrzeugschein', 'Fahrzeugbrief', 'Versicherung', 'Gutachten', 'Kaufvertrag', 'Sonstige']

    @staticmethod
    def _ensure_table():
        conn = sqlite3.connect(Config.DB_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id INTEGER,
                doc_type TEXT NOT NULL,
                filename TEXT NOT NULL,
                file_data BLOB,
                file_size INTEGER,
                uploaded_by INTEGER,
                notes TEXT,
                expiry_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit(); conn.close()

    @staticmethod
    def upload(transaction_id: int, doc_type: str, filename: str, file_data: bytes,
               uploaded_by: int = None, notes: str = None, expiry_date: str = None):
        DocumentArchive._ensure_table()
        conn = sqlite3.connect(Config.DB_PATH)
        conn.execute("""
            INSERT INTO documents (transaction_id, doc_type, filename, file_data, file_size, uploaded_by, notes, expiry_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (transaction_id, doc_type, filename, file_data, len(file_data), uploaded_by, notes, expiry_date))
        conn.commit(); conn.close()

    @staticmethod
    def get_documents(transaction_id: int) -> list:
        DocumentArchive._ensure_table()
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT id, transaction_id, doc_type, filename, file_size, notes, expiry_date, created_at FROM documents WHERE transaction_id=? ORDER BY created_at DESC",
                           (transaction_id,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def download(doc_id: int) -> tuple:
        conn = sqlite3.connect(Config.DB_PATH)
        row = conn.execute("SELECT filename, file_data FROM documents WHERE id=?", (doc_id,)).fetchone()
        conn.close()
        return (row[0], row[1]) if row else (None, None)

    @staticmethod
    def delete(doc_id: int):
        conn = sqlite3.connect(Config.DB_PATH)
        conn.execute("DELETE FROM documents WHERE id=?", (doc_id,))
        conn.commit(); conn.close()

    @staticmethod
    def get_expiring_docs(days: int = 30) -> list:
        DocumentArchive._ensure_table()
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT d.*, t.brand, t.model FROM documents d
            LEFT JOIN transactions t ON d.transaction_id = t.id
            WHERE d.expiry_date IS NOT NULL AND d.expiry_date <= date('now', ?)
            ORDER BY d.expiry_date ASC
        """, (f'+{days} days',)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def render_archive_ui(transaction_id: int):
        import streamlit as st
        from utils.i18n import t
        
        st.markdown(f"#### 📑 {t('docs.title', 'Document Archive')}")
        
        user = st.session_state.get('user', {})
        
        with st.expander(f"📤 {t('docs.upload', 'Upload Document')}", expanded=False):
            with st.form(f"doc_form_{transaction_id}"):
                dc1, dc2 = st.columns(2)
                with dc1:
                    doc_type = st.selectbox(t('docs.type', 'Type'), DocumentArchive.DOC_TYPES, key=f"dtype_{transaction_id}")
                with dc2:
                    expiry = st.date_input(t('docs.expiry', 'Expiry (optional)'), value=None, key=f"dexp_{transaction_id}")
                
                uploaded = st.file_uploader(t('docs.file', 'File'), type=['pdf', 'jpg', 'png', 'docx'], key=f"dfile_{transaction_id}")
                notes = st.text_input(t('docs.notes', 'Notes'), key=f"dnote_{transaction_id}")
                
                if st.form_submit_button(f"📤 {t('docs.upload', 'Upload')}", use_container_width=True):
                    if uploaded:
                        DocumentArchive.upload(transaction_id, doc_type, uploaded.name, uploaded.read(),
                            user.get('id'), notes, str(expiry) if expiry else None)
                        st.success("✅ Uploaded!")
                        st.rerun()
        
        docs = DocumentArchive.get_documents(transaction_id)
        type_icons = {'TÜV': '🔍', 'Versicherung': '🛡️', 'Kaufvertrag': '📋', 'Fahrzeugschein': '📄', 'Fahrzeugbrief': '📃'}
        
        for d in docs:
            icon = type_icons.get(d['doc_type'], '📄')
            size_kb = (d['file_size'] or 0) / 1024
            st.markdown(f"""
            <div style="background: #16213e; padding: 8px 12px; border-radius: 8px; margin: 4px 0; border-left: 3px solid #D4AF37;">
                <b style="color: #D4AF37;">{icon} {d['doc_type']}</b> — {d['filename']}
                <span style="color: #a0a0c0; font-size: 0.8em;">({size_kb:.0f} KB) {d['expiry_date'] or ''}</span>
            </div>
            """, unsafe_allow_html=True)
