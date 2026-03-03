"""
utils/maintenance_log.py - Car Maintenance History
SmartCar AI-Dealer - سجل الصيانة
"""
import sqlite3
from config import Config


class MaintenanceLog:
    """Track car maintenance and service history"""

    @staticmethod
    def _ensure_table():
        conn = sqlite3.connect(Config.DB_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS maintenance_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id INTEGER NOT NULL,
                service_type TEXT NOT NULL,
                description TEXT,
                cost REAL DEFAULT 0,
                service_date TEXT,
                next_service_date TEXT,
                mechanic TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (transaction_id) REFERENCES transactions(id)
            )
        """)
        conn.commit(); conn.close()

    @staticmethod
    def add_entry(transaction_id: int, service_type: str, description: str = None,
                  cost: float = 0, service_date: str = None, next_service: str = None, mechanic: str = None):
        MaintenanceLog._ensure_table()
        conn = sqlite3.connect(Config.DB_PATH)
        conn.execute("""
            INSERT INTO maintenance_log (transaction_id, service_type, description, cost, service_date, next_service_date, mechanic)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (transaction_id, service_type, description, cost, service_date, next_service, mechanic))
        conn.commit(); conn.close()

    @staticmethod
    def get_history(transaction_id: int) -> list:
        MaintenanceLog._ensure_table()
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM maintenance_log WHERE transaction_id=? ORDER BY service_date DESC",
                           (transaction_id,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_total_cost(transaction_id: int) -> float:
        MaintenanceLog._ensure_table()
        conn = sqlite3.connect(Config.DB_PATH)
        row = conn.execute("SELECT COALESCE(SUM(cost),0) FROM maintenance_log WHERE transaction_id=?",
                          (transaction_id,)).fetchone()
        conn.close()
        return row[0] if row else 0

    SERVICE_TYPES = ['Ölwechsel', 'Bremsen', 'Reifen', 'Inspektion', 'TÜV/AU',
                     'Karosserie', 'Elektronik', 'Getriebe', 'Motor', 'Klimaanlage', 'Sonstiges']

    @staticmethod
    def render_maintenance_ui(transaction_id: int):
        """Render maintenance log UI"""
        import streamlit as st
        from utils.i18n import t
        
        st.markdown(f"#### 🔧 {t('maintenance.title', 'Maintenance Log')}")
        
        total_cost = MaintenanceLog.get_total_cost(transaction_id)
        st.metric(f"💰 {t('maintenance.total_cost', 'Total Maintenance Cost')}", f"€{total_cost:,.2f}")
        
        with st.expander(f"➕ {t('maintenance.add', 'Add Entry')}", expanded=False):
            with st.form(f"maint_form_{transaction_id}"):
                mc1, mc2 = st.columns(2)
                with mc1:
                    stype = st.selectbox(t('maintenance.type', 'Service Type'), MaintenanceLog.SERVICE_TYPES, key=f"mt_{transaction_id}")
                    cost = st.number_input(t('maintenance.cost', 'Cost (€)'), min_value=0.0, step=10.0, key=f"mc_{transaction_id}")
                with mc2:
                    sdate = st.date_input(t('maintenance.date', 'Date'), key=f"md_{transaction_id}")
                    mechanic = st.text_input(t('maintenance.mechanic', 'Mechanic'), key=f"mm_{transaction_id}")
                
                desc = st.text_input(t('maintenance.description', 'Description'), key=f"mdesc_{transaction_id}")
                
                if st.form_submit_button(f"✅ {t('maintenance.save', 'Save')}", use_container_width=True):
                    MaintenanceLog.add_entry(transaction_id, stype, desc, cost, str(sdate), mechanic=mechanic)
                    st.rerun()
        
        history = MaintenanceLog.get_history(transaction_id)
        for h in history:
            st.markdown(f"""
            <div style="background: #16213e; padding: 8px 12px; border-radius: 8px; margin: 4px 0; border-left: 3px solid #f39c12;">
                <b style="color: #D4AF37;">🔧 {h['service_type']}</b>
                <span style="float: right; color: #4CAF50;">€{h['cost']:,.2f}</span><br>
                <span style="color: #a0a0c0;">{h['description'] or ''} | 📅 {h['service_date'] or ''} | 👤 {h['mechanic'] or '-'}</span>
            </div>
            """, unsafe_allow_html=True)
