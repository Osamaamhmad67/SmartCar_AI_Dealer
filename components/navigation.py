"""
components/navigation.py - دوال التنقل المشتركة
SmartCar AI-Dealer
تم فصلها لتجنب الاستيرادات الدائرية
"""

import streamlit as st


def navigate_to(page_name: str):
    """التنقل إلى صفحة معينة مع الحفاظ على اللغة والتمرير للأعلى"""
    # حفظ اللغة الحالية قبل التنقل
    current_lang = st.session_state.get('language', 'de')
    st.session_state.page = page_name
    st.session_state.language = current_lang  # إعادة تعيين اللغة
    st.session_state['scroll_to_top'] = True  # flag للتمرير للأعلى
    st.rerun()


def logout():
    """تسجيل الخروج"""
    from utils.i18n import clear_language_on_logout
    clear_language_on_logout()  # مسح اللغة من localStorage
    st.session_state.clear()
    st.session_state.page = 'login'
    st.rerun()
