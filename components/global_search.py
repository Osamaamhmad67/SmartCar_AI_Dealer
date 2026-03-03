"""
components/global_search.py - Universal Search
SmartCar AI-Dealer - بحث شامل
"""
import streamlit as st
import sqlite3
from config import Config
from utils.i18n import t


def render_global_search():
    """Render universal search across all data"""
    query = st.text_input(f"🔍 {t('search.placeholder', 'Search cars, customers, transactions...')}", key="global_search")
    
    if not query or len(query) < 2:
        return
    
    conn = sqlite3.connect(Config.DB_PATH)
    conn.row_factory = sqlite3.Row
    q = f"%{query}%"
    
    results_found = False
    
    # Search transactions
    try:
        cars = conn.execute("""
            SELECT id, brand, model, manufacture_year, estimated_price, color 
            FROM transactions WHERE brand LIKE ? OR model LIKE ? OR color LIKE ? OR car_type LIKE ?
            LIMIT 10
        """, (q, q, q, q)).fetchall()
        
        if cars:
            results_found = True
            st.markdown(f"### 🚗 {t('search.cars', 'Cars')} ({len(cars)})")
            for c in cars:
                st.markdown(f"""
                <div style="background: #16213e; padding: 8px 12px; border-radius: 8px; margin: 3px 0; border-left: 3px solid #D4AF37;">
                    🏎️ <b style="color: white;">{c['brand']} {c['model']}</b> ({c['manufacture_year']}) 
                    <span style="color: #4CAF50;">€{(c['estimated_price'] or 0):,.0f}</span>
                    <span style="color: #a0a0c0;">🎨 {c['color'] or ''}</span>
                </div>""", unsafe_allow_html=True)
    except: pass
    
    # Search users
    try:
        users = conn.execute("""
            SELECT id, username, full_name, email, phone, role
            FROM users WHERE username LIKE ? OR full_name LIKE ? OR email LIKE ? OR phone LIKE ?
            LIMIT 10
        """, (q, q, q, q)).fetchall()
        
        if users:
            results_found = True
            st.markdown(f"### 👥 {t('search.users', 'Users')} ({len(users)})")
            for u in users:
                st.markdown(f"""
                <div style="background: #16213e; padding: 8px 12px; border-radius: 8px; margin: 3px 0; border-left: 3px solid #3498db;">
                    👤 <b style="color: white;">{u['full_name'] or u['username']}</b>
                    <span style="color: #a0a0c0;">📧 {u['email'] or ''} 📞 {u['phone'] or ''}</span>
                    <span style="color: #9b59b6;">{u['role']}</span>
                </div>""", unsafe_allow_html=True)
    except: pass
    
    # Search employees
    try:
        emps = conn.execute("""
            SELECT id, first_name, last_name, position, phone
            FROM employees WHERE first_name LIKE ? OR last_name LIKE ? OR position LIKE ?
            LIMIT 10
        """, (q, q, q)).fetchall()
        
        if emps:
            results_found = True
            st.markdown(f"### 👔 {t('search.employees', 'Employees')} ({len(emps)})")
            for e in emps:
                st.markdown(f"""
                <div style="background: #16213e; padding: 8px 12px; border-radius: 8px; margin: 3px 0; border-left: 3px solid #27ae60;">
                    👔 <b style="color: white;">{e['first_name']} {e['last_name'] or ''}</b>
                    <span style="color: #a0a0c0;">{e['position'] or ''} 📞 {e['phone'] or ''}</span>
                </div>""", unsafe_allow_html=True)
    except: pass
    
    conn.close()
    
    if not results_found:
        st.info(f"🔍 {t('search.no_results', 'No results found for')} \"{query}\"")
