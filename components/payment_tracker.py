"""
components/payment_tracker.py - Payment Tracking Dashboard
SmartCar AI-Dealer - تتبع المدفوعات
"""
import streamlit as st
import sqlite3
from config import Config
from utils.i18n import t


def render_payment_tracker():
    """Track all payments and installments"""
    st.markdown(f"""
    <div style="text-align: center; padding: 15px 0;">
        <h2 style="color: #D4AF37;">💳 {t('payments.title', 'Payment Tracker')}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    conn = sqlite3.connect(Config.DATABASE_PATH)
    
    try:
        # Overview metrics
        total_due = conn.execute("SELECT COALESCE(SUM(estimated_price),0) FROM transactions WHERE estimated_price > 0").fetchone()[0]
        total_paid = conn.execute("SELECT COALESCE(SUM(amount_paid),0) FROM transactions WHERE amount_paid > 0").fetchone()[0]
        outstanding = total_due - total_paid
        
        m1, m2, m3 = st.columns(3)
        m1.markdown(f"""
        <div style="background: #16213e; padding: 15px; border-radius: 12px; text-align: center; border-top: 3px solid #3498db;">
            <div style="color: #a0a0c0;">💰 {t('payments.total_due', 'Total Due')}</div>
            <div style="color: #3498db; font-size: 1.5em; font-weight: bold;">€{total_due:,.0f}</div>
        </div>""", unsafe_allow_html=True)
        m2.markdown(f"""
        <div style="background: #16213e; padding: 15px; border-radius: 12px; text-align: center; border-top: 3px solid #27ae60;">
            <div style="color: #a0a0c0;">✅ {t('payments.paid', 'Paid')}</div>
            <div style="color: #27ae60; font-size: 1.5em; font-weight: bold;">€{total_paid:,.0f}</div>
        </div>""", unsafe_allow_html=True)
        m3.markdown(f"""
        <div style="background: #16213e; padding: 15px; border-radius: 12px; text-align: center; border-top: 3px solid #e74c3c;">
            <div style="color: #a0a0c0;">⏳ {t('payments.outstanding', 'Outstanding')}</div>
            <div style="color: #e74c3c; font-size: 1.5em; font-weight: bold;">€{outstanding:,.0f}</div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Overdue list
        st.markdown(f"### ⚠️ {t('payments.overdue', 'Pending Payments')}")
        overdue = conn.execute("""
            SELECT t.id, t.brand, t.model, t.estimated_price, 
                   COALESCE(t.amount_paid, 0) as paid,
                   u.full_name, t.created_at
            FROM transactions t
            LEFT JOIN users u ON t.user_id = u.id
            WHERE t.estimated_price > COALESCE(t.amount_paid, 0)
            ORDER BY (t.estimated_price - COALESCE(t.amount_paid, 0)) DESC
            LIMIT 20
        """).fetchall()
        
        for o in overdue:
            remaining = (o[3] or 0) - (o[4] or 0)
            pct = (o[4] / max(o[3], 1)) * 100 if o[3] else 0
            color = '#27ae60' if pct >= 80 else '#f39c12' if pct >= 40 else '#e74c3c'
            st.markdown(f"""
            <div style="background: #16213e; padding: 10px; border-radius: 10px; margin: 5px 0;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: white;">🏎️ {o[1]} {o[2]} — 👤 {o[5] or 'N/A'}</span>
                    <span style="color: {color};">€{remaining:,.0f} remaining</span>
                </div>
                <div style="background: #1a1a2e; border-radius: 6px; height: 6px; margin-top: 6px;">
                    <div style="background: {color}; width: {pct:.0f}%; height: 6px; border-radius: 6px;"></div>
                </div>
                <span style="color: #a0a0c0; font-size: 0.75em;">€{o[4]:,.0f} / €{o[3]:,.0f} ({pct:.0f}%)</span>
            </div>
            """, unsafe_allow_html=True)
        
        if not overdue:
            st.success(t('payments.all_paid', 'All payments up to date! ✅'))
    except Exception as e:
        st.info(f"Payment tracking: {e}")
    conn.close()
