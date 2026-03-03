"""
components/live_dashboard.py - Live Auto-Refreshing Dashboard
SmartCar AI-Dealer - لوحة مباشرة
"""
import streamlit as st
import sqlite3
from datetime import datetime
from config import Config
from utils.i18n import t


def render_live_dashboard():
    """Render live auto-refreshing dashboard"""
    st.markdown(f"""
    <div style="text-align: center; padding: 15px 0;">
        <h2 style="color: #D4AF37;">🖥️ {t('live.title', 'Live Dashboard')}</h2>
        <p style="color: #a0a0c0;">{t('live.subtitle', 'Real-time system overview')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-refresh toggle
    auto_refresh = st.checkbox(f"🔄 {t('live.auto_refresh', 'Auto-refresh (10s)')}", value=False, key="live_auto")
    if auto_refresh:
        import time
        st.empty()
        time.sleep(0)  # Placeholder - actual refresh via st.rerun below
    
    conn = sqlite3.connect(Config.DATABASE_PATH)
    
    # Row 1: Key metrics
    m1, m2, m3, m4 = st.columns(4)
    
    try:
        total_trans = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
        today_trans = conn.execute("SELECT COUNT(*) FROM transactions WHERE created_at >= date('now')").fetchone()[0]
        total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        revenue = conn.execute("SELECT COALESCE(SUM(estimated_price),0) FROM transactions").fetchone()[0]
    except:
        total_trans = today_trans = total_users = 0; revenue = 0
    
    m1.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #D4AF3733;">
        <div style="font-size: 2.5em; color: #D4AF37;">{total_trans}</div>
        <div style="color: #a0a0c0;">📊 {t('live.total', 'Total')}</div>
    </div>""", unsafe_allow_html=True)
    
    m2.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #27ae6033;">
        <div style="font-size: 2.5em; color: #27ae60;">{today_trans}</div>
        <div style="color: #a0a0c0;">📅 {t('live.today', 'Today')}</div>
    </div>""", unsafe_allow_html=True)
    
    m3.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #3498db33;">
        <div style="font-size: 2.5em; color: #3498db;">{total_users}</div>
        <div style="color: #a0a0c0;">👥 {t('live.users', 'Users')}</div>
    </div>""", unsafe_allow_html=True)
    
    m4.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #9b59b633;">
        <div style="font-size: 2.5em; color: #9b59b6;">€{revenue:,.0f}</div>
        <div style="color: #a0a0c0;">💰 {t('live.revenue', 'Revenue')}</div>
    </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Row 2: Recent activity
    st.markdown(f"### 🔔 {t('live.recent', 'Recent Activity')}")
    
    try:
        recent = conn.execute("""
            SELECT brand, model, estimated_price, created_at FROM transactions 
            ORDER BY created_at DESC LIMIT 5
        """).fetchall()
        
        for r in recent:
            price = r[2] or 0
            date = (r[3] or '')[:16]
            st.markdown(f"""
            <div style="background: #16213e; padding: 8px 12px; border-radius: 8px; margin: 4px 0; border-left: 3px solid #D4AF37; display: flex; justify-content: space-between;">
                <span style="color: white;">🏎️ {r[0]} {r[1]}</span>
                <span style="color: #4CAF50; font-weight: bold;">€{price:,.0f}</span>
                <span style="color: #a0a0c0; font-size: 0.8em;">🕐 {date}</span>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.info("No recent activity")
    
    conn.close()
    
    # Status bar
    st.markdown(f"""
    <div style="text-align: center; padding: 10px; color: #a0a0c0; font-size: 0.8em;">
        🟢 System Online | Last update: {datetime.now().strftime('%H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-refresh mechanism
    if auto_refresh:
        import time
        time.sleep(10)
        st.rerun()
