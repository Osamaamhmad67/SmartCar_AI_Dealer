"""
components/satisfaction_chart.py - Customer Satisfaction Analysis
SmartCar AI-Dealer - تحليل رضا العملاء
"""
import streamlit as st
import sqlite3
from config import Config
from utils.i18n import t


def render_satisfaction_analysis():
    """Render charts from customer reviews data"""
    st.markdown(f"""
    <div style="text-align: center; padding: 15px 0;">
        <h2 style="color: #D4AF37;">📊 {t('satisfaction.title', 'Customer Satisfaction Analysis')}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    conn = sqlite3.connect(Config.DB_PATH)
    
    try:
        import pandas as pd
        import plotly.express as px
        import plotly.graph_objects as go
        
        df = pd.read_sql_query("SELECT * FROM reviews ORDER BY created_at", conn)
        
        if df.empty:
            st.info(t('satisfaction.no_data', 'No reviews data yet'))
            conn.close()
            return
        
        c1, c2 = st.columns(2)
        
        with c1:
            # Rating distribution
            rating_counts = df['rating'].value_counts().sort_index()
            fig_dist = px.bar(
                x=rating_counts.index, y=rating_counts.values,
                labels={'x': '⭐ Rating', 'y': 'Count'},
                title=t('satisfaction.distribution', '⭐ Rating Distribution'),
                color=rating_counts.values,
                color_continuous_scale='YlOrRd'
            )
            fig_dist.update_layout(template='plotly_dark')
            st.plotly_chart(fig_dist, use_container_width=True)
        
        with c2:
            # Average rating over time
            df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
            df_monthly = df.set_index('created_at').resample('M')['rating'].mean().reset_index()
            
            if len(df_monthly) > 1:
                fig_trend = px.line(
                    df_monthly, x='created_at', y='rating',
                    title=t('satisfaction.trend', '📈 Rating Trend'),
                    markers=True
                )
                fig_trend.update_layout(template='plotly_dark')
                fig_trend.update_yaxes(range=[1, 5])
                st.plotly_chart(fig_trend, use_container_width=True)
            else:
                avg = df['rating'].mean()
                st.metric(t('satisfaction.average', 'Average Rating'), f"⭐ {avg:.1f}/5")
        
        # Satisfaction score
        avg_rating = df['rating'].mean()
        total_reviews = len(df)
        five_star_pct = (len(df[df['rating'] == 5]) / total_reviews * 100) if total_reviews > 0 else 0
        
        st.markdown("---")
        ss1, ss2, ss3 = st.columns(3)
        ss1.metric(f"⭐ {t('satisfaction.avg', 'Average')}", f"{avg_rating:.1f}/5")
        ss2.metric(f"📊 {t('satisfaction.total', 'Total Reviews')}", total_reviews)
        ss3.metric(f"🏆 {t('satisfaction.five_star', '5-Star %')}", f"{five_star_pct:.0f}%")
        
        # NPS-style gauge
        nps = (avg_rating - 1) / 4 * 100  # Convert 1-5 to 0-100
        color = '#27ae60' if nps >= 70 else '#f39c12' if nps >= 40 else '#e74c3c'
        st.markdown(f"""
        <div style="background: #16213e; padding: 20px; border-radius: 15px; text-align: center;">
            <h3 style="color: #D4AF37;">{t('satisfaction.score', 'Satisfaction Score')}</h3>
            <div style="font-size: 3em; color: {color}; font-weight: bold;">{nps:.0f}%</div>
            <div style="background: #1a1a2e; border-radius: 10px; height: 12px; margin: 10px 40px;">
                <div style="background: {color}; width: {nps:.0f}%; height: 12px; border-radius: 10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    except Exception as e:
        st.info(f"Reviews table not available: {e}")
    
    conn.close()
