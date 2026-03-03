"""
components/finance_calculator.py - Interactive Finance Calculator
SmartCar AI-Dealer - حاسبة التمويل التفاعلية
"""
import streamlit as st
from utils.i18n import t


def render_finance_calculator(car_price: float = 0):
    """Render interactive finance calculator"""
    st.markdown(f"""
    <div style="text-align: center; padding: 15px 0;">
        <h2 style="color: #D4AF37;">🧮 {t('calculator.title', 'Finance Calculator')}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        price = st.number_input(
            f"💰 {t('calculator.price', 'Vehicle Price (€)')}", 
            min_value=0, value=int(car_price) if car_price else 25000, step=1000, key="calc_price")
        
        down_payment_pct = st.slider(
            f"📊 {t('calculator.down_payment', 'Down Payment (%)')}", 
            0, 50, 20, key="calc_down_pct")
        
        months = st.selectbox(
            f"📅 {t('calculator.months', 'Duration (months)')}", 
            [6, 12, 18, 24, 36, 48], index=3, key="calc_months")
    
    with col2:
        interest_rate = st.slider(
            f"📈 {t('calculator.interest', 'Interest Rate (%)')}", 
            0.0, 15.0, 3.9, 0.1, key="calc_interest")
        
        # Calculations
        down_payment = price * (down_payment_pct / 100)
        loan_amount = price - down_payment
        
        if interest_rate > 0:
            monthly_rate = interest_rate / 100 / 12
            monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
        else:
            monthly_payment = loan_amount / months if months > 0 else 0
        
        total_cost = down_payment + (monthly_payment * months)
        total_interest = total_cost - price
    
    st.markdown("---")
    
    # Results
    r1, r2, r3, r4 = st.columns(4)
    
    r1.markdown(f"""
    <div style="background: #16213e; padding: 15px; border-radius: 10px; text-align: center;">
        <div style="color: #a0a0c0; font-size: 0.85em;">{t('calculator.down_payment', 'Down Payment')}</div>
        <div style="color: #D4AF37; font-size: 1.4em; font-weight: bold;">€{down_payment:,.0f}</div>
    </div>""", unsafe_allow_html=True)
    
    r2.markdown(f"""
    <div style="background: #16213e; padding: 15px; border-radius: 10px; text-align: center;">
        <div style="color: #a0a0c0; font-size: 0.85em;">{t('calculator.monthly', 'Monthly Payment')}</div>
        <div style="color: #4CAF50; font-size: 1.4em; font-weight: bold;">€{monthly_payment:,.0f}</div>
    </div>""", unsafe_allow_html=True)
    
    r3.markdown(f"""
    <div style="background: #16213e; padding: 15px; border-radius: 10px; text-align: center;">
        <div style="color: #a0a0c0; font-size: 0.85em;">{t('calculator.total_interest', 'Total Interest')}</div>
        <div style="color: #f39c12; font-size: 1.4em; font-weight: bold;">€{total_interest:,.0f}</div>
    </div>""", unsafe_allow_html=True)
    
    r4.markdown(f"""
    <div style="background: #16213e; padding: 15px; border-radius: 10px; text-align: center;">
        <div style="color: #a0a0c0; font-size: 0.85em;">{t('calculator.total_cost', 'Total Cost')}</div>
        <div style="color: white; font-size: 1.4em; font-weight: bold;">€{total_cost:,.0f}</div>
    </div>""", unsafe_allow_html=True)
