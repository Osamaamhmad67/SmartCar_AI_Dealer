"""
utils/delivery_checklist.py - Car Delivery Checklist
SmartCar AI-Dealer - قائمة فحص التسليم
"""
import sqlite3
from datetime import datetime
from config import Config


class DeliveryChecklist:
    """Pre-delivery inspection checklist"""

    DEFAULT_ITEMS = [
        ('exterior', '🚗 Exterior Inspection', 'Check body, paint, windows, lights'),
        ('interior', '🪑 Interior Check', 'Seats, dashboard, AC, electronics'),
        ('engine', '🔧 Engine Check', 'Oil, coolant, belts, battery'),
        ('tires', '🛞 Tires & Brakes', 'Tire condition, brake pads, fluids'),
        ('documents', '📄 Documents Ready', 'Registration, insurance, manual, keys'),
        ('clean', '✨ Vehicle Cleaned', 'Interior/exterior cleaning done'),
        ('fuel', '⛽ Fuel Level', 'Minimum half tank'),
        ('test_drive', '🏁 Test Drive', 'Final test drive completed'),
        ('photos', '📸 Final Photos', 'Delivery photos taken'),
        ('handover', '🤝 Customer Briefing', 'Features explained to customer'),
    ]

    @staticmethod
    def _ensure_table():
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS delivery_checklist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id INTEGER NOT NULL,
                item_key TEXT NOT NULL,
                checked INTEGER DEFAULT 0,
                checked_by TEXT,
                checked_at TIMESTAMP,
                notes TEXT
            )
        """)
        conn.commit(); conn.close()

    @staticmethod
    def init_checklist(transaction_id: int):
        DeliveryChecklist._ensure_table()
        conn = sqlite3.connect(Config.DATABASE_PATH)
        existing = conn.execute("SELECT COUNT(*) FROM delivery_checklist WHERE transaction_id=?", (transaction_id,)).fetchone()[0]
        if existing == 0:
            for key, label, desc in DeliveryChecklist.DEFAULT_ITEMS:
                conn.execute("INSERT INTO delivery_checklist (transaction_id, item_key) VALUES (?,?)", (transaction_id, key))
            conn.commit()
        conn.close()

    @staticmethod
    def toggle_item(transaction_id: int, item_key: str, checked_by: str = None):
        conn = sqlite3.connect(Config.DATABASE_PATH)
        current = conn.execute("SELECT checked FROM delivery_checklist WHERE transaction_id=? AND item_key=?", 
                              (transaction_id, item_key)).fetchone()
        new_val = 0 if current and current[0] else 1
        conn.execute("UPDATE delivery_checklist SET checked=?, checked_by=?, checked_at=? WHERE transaction_id=? AND item_key=?",
                     (new_val, checked_by, datetime.now().isoformat() if new_val else None, transaction_id, item_key))
        conn.commit(); conn.close()

    @staticmethod
    def get_status(transaction_id: int) -> dict:
        DeliveryChecklist._ensure_table()
        DeliveryChecklist.init_checklist(transaction_id)
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        items = conn.execute("SELECT * FROM delivery_checklist WHERE transaction_id=?", (transaction_id,)).fetchall()
        conn.close()
        
        total = len(items)
        checked = sum(1 for i in items if i['checked'])
        return {
            'items': [dict(i) for i in items],
            'total': total,
            'checked': checked,
            'progress': (checked / max(total, 1)) * 100
        }

    @staticmethod
    def render_checklist_ui(transaction_id: int):
        import streamlit as st
        from utils.i18n import t
        
        status = DeliveryChecklist.get_status(transaction_id)
        user = st.session_state.get('user', {})
        
        st.markdown(f"#### ✅ {t('checklist.title', 'Delivery Checklist')} ({status['checked']}/{status['total']})")
        
        # Progress bar
        pct = status['progress']
        color = '#27ae60' if pct >= 80 else '#f39c12' if pct >= 50 else '#e74c3c'
        st.markdown(f"""
        <div style="background: #1a1a2e; border-radius: 10px; height: 10px; margin: 10px 0;">
            <div style="background: {color}; width: {pct:.0f}%; height: 10px; border-radius: 10px;"></div>
        </div>""", unsafe_allow_html=True)
        
        # Items
        item_map = {key: (label, desc) for key, label, desc in DeliveryChecklist.DEFAULT_ITEMS}
        for item in status['items']:
            key = item['item_key']
            label, desc = item_map.get(key, (key, ''))
            if st.checkbox(f"{label}", value=bool(item['checked']), key=f"cl_{transaction_id}_{key}"):
                if not item['checked']:
                    DeliveryChecklist.toggle_item(transaction_id, key, user.get('username', ''))
            elif item['checked']:
                DeliveryChecklist.toggle_item(transaction_id, key)
