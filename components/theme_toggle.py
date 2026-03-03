"""
components/theme_toggle.py - Dark/Light Theme Toggle
SmartCar AI-Dealer - تبديل الثيم
"""
import streamlit as st
from utils.i18n import t


def render_theme_toggle():
    """Render theme toggle in sidebar"""
    with st.sidebar:
        current = st.session_state.get('theme', 'dark')
        label = "☀️ Light Mode" if current == 'dark' else "🌙 Dark Mode"
        
        if st.button(label, use_container_width=True, key="theme_btn"):
            st.session_state['theme'] = 'light' if current == 'dark' else 'dark'
            st.rerun()


def apply_theme():
    """Apply current theme CSS"""
    theme = st.session_state.get('theme', 'dark')
    
    if theme == 'light':
        st.markdown("""
        <style>
            .stApp { background-color: #f5f5f5 !important; }
            .stSidebar { background-color: #ffffff !important; }
            .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #1a1a2e !important; }
            .stMetricValue { color: #1a1a2e !important; }
            div[data-testid="stExpander"] { background: #ffffff; border: 1px solid #e0e0e0; border-radius: 10px; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            .stApp { background: linear-gradient(180deg, #0a0a14 0%, #1a1a2e 100%) !important; }
            .stSidebar { background-color: #16213e !important; }
            div[data-testid="stExpander"] { background: #16213e; border: 1px solid #D4AF3733; border-radius: 10px; }
        </style>
        """, unsafe_allow_html=True)
