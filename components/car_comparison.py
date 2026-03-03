"""
components/car_comparison.py - Side-by-Side Car Comparison
SmartCar AI-Dealer - مقارنة السيارات
"""
import streamlit as st
import sqlite3
from config import Config
from utils.i18n import t


def render_car_comparison():
    """Render side-by-side car comparison tool"""
    st.markdown(f"""
    <div style="text-align: center; padding: 15px 0;">
        <h2 style="color: #D4AF37;">📊 {t('compare.title', 'Car Comparison')}</h2>
        <p style="color: #a0a0c0;">{t('compare.subtitle', 'Compare two vehicles side by side')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cars = conn.execute("SELECT id, brand, model, manufacture_year, estimated_price FROM transactions WHERE estimated_price > 0 ORDER BY created_at DESC LIMIT 50").fetchall()
    conn.close()
    
    car_options = {f"{c['brand']} {c['model']} ({c['manufacture_year']}) - €{c['estimated_price']:,.0f}": c['id'] for c in cars}
    
    col1, col2 = st.columns(2)
    
    with col1:
        car1_label = st.selectbox(f"🚗 {t('compare.car1', 'Car 1')}", list(car_options.keys()), key="cmp_car1")
    with col2:
        car2_label = st.selectbox(f"🚗 {t('compare.car2', 'Car 2')}", list(car_options.keys()), key="cmp_car2", index=min(1, len(car_options)-1))
    
    if car1_label and car2_label and st.button(f"📊 {t('compare.compare', 'Compare')}", type="primary", use_container_width=True):
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        c1 = dict(conn.execute("SELECT * FROM transactions WHERE id=?", (car_options[car1_label],)).fetchone())
        c2 = dict(conn.execute("SELECT * FROM transactions WHERE id=?", (car_options[car2_label],)).fetchone())
        conn.close()
        
        specs = [
            ('🏷️', 'Brand', 'brand'),
            ('🚗', 'Model', 'model'),
            ('📅', 'Year', 'manufacture_year'),
            ('💰', 'Price (€)', 'estimated_price'),
            ('🛣️', 'Mileage (km)', 'mileage'),
            ('⛽', 'Fuel', 'fuel_type'),
            ('⚙️', 'Transmission', 'transmission'),
            ('🐎', 'Horsepower', 'horsepower'),
            ('🏭', 'Engine CC', 'engine_cc'),
            ('🎨', 'Color', 'color'),
            ('📋', 'Condition', 'condition'),
            ('🌿', 'Emissions', 'emissions_class'),
            ('🛡️', 'Warranty', 'warranty'),
            ('💥', 'Accidents', 'accident_history'),
        ]
        
        st.markdown("---")
        
        for icon, label, key in specs:
            v1 = c1.get(key, '-') or '-'
            v2 = c2.get(key, '-') or '-'
            
            # Highlight winner for numeric fields
            highlight1 = highlight2 = ''
            if key == 'estimated_price' and str(v1).replace('.','').isdigit() and str(v2).replace('.','').isdigit():
                if float(v1) < float(v2): highlight1 = 'color: #27ae60; font-weight: bold;'
                elif float(v2) < float(v1): highlight2 = 'color: #27ae60; font-weight: bold;'
            
            if key == 'estimated_price':
                v1 = f"€{float(v1):,.0f}" if str(v1).replace('.','').isdigit() else v1
                v2 = f"€{float(v2):,.0f}" if str(v2).replace('.','').isdigit() else v2
            elif key == 'mileage':
                v1 = f"{float(v1):,.0f}" if str(v1).replace('.','').isdigit() else v1
                v2 = f"{float(v2):,.0f}" if str(v2).replace('.','').isdigit() else v2
            
            st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 6px 0; border-bottom: 1px solid #1a1a2e;">
                <div style="flex: 1; text-align: center; {highlight1}">{v1}</div>
                <div style="flex: 0.6; text-align: center; background: #16213e; padding: 4px; border-radius: 8px; color: #D4AF37; font-size: 0.85em;">{icon} {label}</div>
                <div style="flex: 1; text-align: center; {highlight2}">{v2}</div>
            </div>
            """, unsafe_allow_html=True)
