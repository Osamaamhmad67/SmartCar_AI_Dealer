"""
components/yearly_comparison.py - Year-over-Year Comparison
SmartCar AI-Dealer - مقارنة سنة بسنة
"""
import streamlit as st
import sqlite3
from config import Config
from utils.i18n import t


def render_yearly_comparison():
    """Render year-over-year comparison charts"""
    st.markdown(f"""
    <div style="text-align: center; padding: 15px 0;">
        <h2 style="color: #D4AF37;">📊 {t('yearly.title', 'Year-over-Year Comparison')}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    conn = sqlite3.connect(Config.DB_PATH)
    
    try:
        import pandas as pd
        import plotly.graph_objects as go
        
        df = pd.read_sql_query("SELECT * FROM transactions WHERE created_at IS NOT NULL AND estimated_price > 0", conn)
        if df.empty:
            st.info("No data"); conn.close(); return
        
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        df['year'] = df['created_at'].dt.year
        df['month'] = df['created_at'].dt.month
        
        years = sorted(df['year'].dropna().unique())
        
        if len(years) < 2:
            st.info(t('yearly.need_two_years', 'Need at least 2 years of data'))
            # Show current year stats anyway
            year_data = df[df['year'] == years[0]]
            st.metric(f"📊 {years[0]}", f"{len(year_data)} transactions | €{year_data['estimated_price'].sum():,.0f}")
            conn.close(); return
        
        # Monthly comparison chart
        fig = go.Figure()
        colors = ['#D4AF37', '#3498db', '#27ae60', '#e74c3c']
        month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        
        for i, year in enumerate(years[-4:]):  # Last 4 years max
            year_data = df[df['year'] == year]
            monthly = year_data.groupby('month').agg({'estimated_price': ['count', 'sum']}).reset_index()
            monthly.columns = ['month', 'count', 'revenue']
            
            fig.add_trace(go.Bar(
                x=month_names, 
                y=[monthly[monthly['month']==m]['count'].values[0] if m in monthly['month'].values else 0 for m in range(1,13)],
                name=str(int(year)),
                marker_color=colors[i % len(colors)]
            ))
        
        fig.update_layout(
            template='plotly_dark', barmode='group',
            title=t('yearly.monthly_comparison', '📊 Monthly Transactions by Year')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Year summary table
        st.markdown(f"### 📋 {t('yearly.summary', 'Summary')}")
        
        for year in reversed(years[-4:]):
            year_data = df[df['year'] == year]
            count = len(year_data)
            revenue = year_data['estimated_price'].sum()
            avg = year_data['estimated_price'].mean()
            
            st.markdown(f"""
            <div style="background: #16213e; padding: 12px; border-radius: 10px; margin: 5px 0; display: flex; justify-content: space-around;">
                <span style="color: #D4AF37; font-size: 1.2em; font-weight: bold;">📅 {int(year)}</span>
                <span style="color: white;">🛒 {count} sales</span>
                <span style="color: #4CAF50;">💰 €{revenue:,.0f}</span>
                <span style="color: #3498db;">📊 Avg €{avg:,.0f}</span>
            </div>
            """, unsafe_allow_html=True)
    
    except Exception as e:
        st.info(f"Comparison unavailable: {e}")
    conn.close()
