"""
components/employee_stats.py - Personal Employee Dashboard
SmartCar AI-Dealer - لوحة الموظف الشخصية
"""
import streamlit as st
import sqlite3
from config import Config
from utils.i18n import t


def render_employee_stats(employee_id: int = None):
    """Render personal performance dashboard for employee"""
    if not employee_id:
        user = st.session_state.get('user', {})
        employee_id = user.get('employee_id') or user.get('id')
    
    st.markdown(f"""
    <div style="text-align: center; padding: 15px 0;">
        <h2 style="color: #D4AF37;">📊 {t('emp_stats.title', 'My Performance')}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    conn = sqlite3.connect(Config.DATABASE_PATH)
    
    # Personal stats
    total = conn.execute("SELECT COUNT(*) FROM transactions WHERE employee_id=?", (employee_id,)).fetchone()[0]
    revenue = conn.execute("SELECT COALESCE(SUM(estimated_price),0) FROM transactions WHERE employee_id=?", (employee_id,)).fetchone()[0]
    avg = conn.execute("SELECT COALESCE(AVG(estimated_price),0) FROM transactions WHERE employee_id=?", (employee_id,)).fetchone()[0]
    this_month = conn.execute("SELECT COUNT(*) FROM transactions WHERE employee_id=? AND created_at >= date('now','start of month')", (employee_id,)).fetchone()[0]
    
    c1, c2, c3, c4 = st.columns(4)
    
    metrics = [
        (c1, '🛒', t('emp_stats.total', 'Total Sales'), total, '#D4AF37'),
        (c2, '💰', t('emp_stats.revenue', 'Revenue'), f"€{revenue:,.0f}", '#4CAF50'),
        (c3, '📊', t('emp_stats.average', 'Avg Price'), f"€{avg:,.0f}", '#3498db'),
        (c4, '📅', t('emp_stats.this_month', 'This Month'), this_month, '#9b59b6'),
    ]
    
    for col, icon, label, value, color in metrics:
        with col:
            st.markdown(f"""
            <div style="background: #16213e; padding: 15px; border-radius: 12px; text-align: center; border-top: 3px solid {color};">
                <div style="font-size: 1.5em;">{icon}</div>
                <div style="color: {color}; font-size: 1.4em; font-weight: bold;">{value}</div>
                <div style="color: #a0a0c0; font-size: 0.8em;">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent sales
    st.markdown(f"### 🕐 {t('emp_stats.recent', 'Recent Sales')}")
    recent = conn.execute("""
        SELECT brand, model, estimated_price, created_at FROM transactions 
        WHERE employee_id=? ORDER BY created_at DESC LIMIT 10
    """, (employee_id,)).fetchall()
    
    for r in recent:
        st.markdown(f"""
        <div style="background: #16213e; padding: 8px 12px; border-radius: 8px; margin: 4px 0; display: flex; justify-content: space-between;">
            <span style="color: white;">🏎️ {r[0]} {r[1]}</span>
            <span style="color: #4CAF50;">€{(r[2] or 0):,.0f}</span>
            <span style="color: #a0a0c0; font-size: 0.8em;">{(r[3] or '')[:10]}</span>
        </div>
        """, unsafe_allow_html=True)
    
    if not recent:
        st.info(t('emp_stats.no_sales', 'No sales yet'))
    
    conn.close()
