"""
components/sales_heatmap.py - Sales Heatmap by Day/Hour
SmartCar AI-Dealer
"""
import streamlit as st
import sqlite3
from config import Config
from utils.i18n import t


def render_sales_heatmap():
    """Render sales heatmap chart"""
    st.markdown(f"### 📊 {t('heatmap.title', 'Sales Heatmap')}")
    
    conn = sqlite3.connect(Config.DB_PATH)
    
    try:
        import pandas as pd
        import plotly.express as px
        
        df = pd.read_sql_query("SELECT created_at FROM transactions WHERE created_at IS NOT NULL", conn)
        if df.empty:
            st.info("No data"); conn.close(); return
        
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        df = df.dropna(subset=['created_at'])
        df['day'] = df['created_at'].dt.day_name()
        df['hour'] = df['created_at'].dt.hour
        
        heatmap_data = df.groupby(['day', 'hour']).size().reset_index(name='count')
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data['day'] = pd.Categorical(heatmap_data['day'], categories=days_order, ordered=True)
        
        pivot = heatmap_data.pivot_table(index='day', columns='hour', values='count', fill_value=0)
        
        fig = px.imshow(pivot, labels=dict(x="Hour", y="Day", color="Sales"),
                       color_continuous_scale='YlOrRd', aspect='auto',
                       title=t('heatmap.title', '🔥 Sales Activity Heatmap'))
        fig.update_layout(template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.info(f"Heatmap unavailable: {e}")
    conn.close()
