"""
pages_app/branches_page.py - Branch Map Page
SmartCar AI-Dealer - خريطة الفروع
"""
import streamlit as st
from utils.i18n import t


def branches_page():
    """Interactive branch locations page"""
    st.markdown(f"""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #D4AF37;">🗺️ {t('branches.title', 'Our Locations')}</h1>
        <p style="color: #a0a0c0;">{t('branches.subtitle', 'Visit us at our showrooms')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Branch data
    branches = [
        {
            'name': 'SmartCar Hauptsitz Berlin',
            'address': 'Kurfürstendamm 100, 10711 Berlin',
            'phone': '+49 30 123 456 78',
            'hours': 'Mo-Sa 09:00-18:00',
            'lat': 52.5037, 'lon': 13.3156,
            'color': '#D4AF37'
        },
        {
            'name': 'SmartCar München',
            'address': 'Leopoldstraße 50, 80802 München',
            'phone': '+49 89 234 567 89',
            'hours': 'Mo-Sa 09:00-18:00',
            'lat': 48.1618, 'lon': 11.5860,
            'color': '#3498db'
        },
        {
            'name': 'SmartCar Hamburg',
            'address': 'Jungfernstieg 30, 20354 Hamburg',
            'phone': '+49 40 345 678 90',
            'hours': 'Mo-Fr 09:00-17:00',
            'lat': 53.5527, 'lon': 9.9930,
            'color': '#27ae60'
        },
        {
            'name': 'SmartCar Frankfurt',
            'address': 'Zeil 80, 60313 Frankfurt',
            'phone': '+49 69 456 789 01',
            'hours': 'Mo-Sa 10:00-19:00',
            'lat': 50.1141, 'lon': 8.6826,
            'color': '#e74c3c'
        }
    ]
    
    # Map
    import pandas as pd
    df_map = pd.DataFrame(branches)
    st.map(df_map, latitude='lat', longitude='lon', zoom=5)
    
    st.markdown("---")
    
    # Branch cards
    for i in range(0, len(branches), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j >= len(branches): break
            b = branches[i + j]
            with col:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a1a2e, #16213e);
                            border-radius: 15px; padding: 20px; margin-bottom: 15px;
                            border-left: 4px solid {b['color']};">
                    <h3 style="color: {b['color']};">📍 {b['name']}</h3>
                    <p style="color: #a0a0c0; line-height: 1.8;">
                        🏠 {b['address']}<br>
                        📞 {b['phone']}<br>
                        🕐 {b['hours']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
