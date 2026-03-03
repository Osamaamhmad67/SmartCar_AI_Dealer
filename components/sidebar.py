"""
components/sidebar.py - الشريط الجانبي
SmartCar AI-Dealer
"""

import streamlit as st
from utils.i18n import t, get_language_display_name, get_current_lang, set_language, SUPPORTED_LANGUAGES
from components.navigation import navigate_to, logout
from components.dialogs import show_help_dialog, show_features_dialog, show_about_dialog


# ======================

def render_sidebar():
    """عرض الشريط الجانبي"""
    with st.sidebar:
        user = st.session_state.user
        
        st.markdown(f"### 👤 {user.get('full_name') or user.get('username')}")
        st.caption(user.get('email', ''))
        
        st.markdown("---")
        
        # Language Selector
        lang_options = list(SUPPORTED_LANGUAGES.keys())
        lang_labels = [get_language_display_name(code) for code in lang_options]
        
        current_lang = get_current_lang()
        current_idx = lang_options.index(current_lang) if current_lang in lang_options else 0
        
        selected = st.selectbox(
            "🌐 Language / اللغة",
            lang_labels,
            index=current_idx,
            key="sidebar_lang_select"
        )
        
        new_idx = lang_labels.index(selected)
        new_lang = lang_options[new_idx]
        if new_lang != current_lang:
            set_language(new_lang)
            st.rerun()
        
        st.markdown("---")
        
        # قائمة التنقل - مترجمة
        # Admin button
        if user.get('role') == 'admin':
            if st.button(f"👑 {t('nav.admin')}", use_container_width=True, 
                        type="primary" if st.session_state.page == "home" else "secondary"):
                navigate_to("home")
        
        # Predict button
        if st.button(f"🏎️ {t('nav.predict')}", use_container_width=True, 
                    type="primary" if st.session_state.page == "predict" else "secondary"):
            navigate_to("predict")
        
        # Help button with workflow dialog
        if st.button(f"❓ {t('nav.help')}", use_container_width=True):
            st.session_state['show_help'] = True
            st.session_state['scroll_to_top'] = True
            st.rerun()
        
        # Features button with features dialog
        if st.button(f"✨ {t('nav.features')}", use_container_width=True):
            st.session_state['show_features'] = True
            st.session_state['scroll_to_top'] = True
            st.rerun()
        
        # About button with about dialog
        if st.button(f"ℹ️ {t('nav.about')}", use_container_width=True):
            st.session_state['show_about'] = True
            st.session_state['scroll_to_top'] = True
            st.rerun()
        
        # Profile button
        if st.button(f"👤 {t('nav.profile')}", use_container_width=True, 
                    type="primary" if st.session_state.page == "profile" else "secondary"):
            navigate_to("profile")
        
        # Invoices button
        if st.button(f"📄 {t('nav.invoices')}", use_container_width=True, 
                    type="primary" if st.session_state.page == "invoices" else "secondary"):
            navigate_to("invoices")
        
        # Inventory button
        if st.button(f"🚗 {t('nav.inventory', 'Inventory')}", use_container_width=True, 
                    type="primary" if st.session_state.page == "inventory" else "secondary"):
            navigate_to("inventory")
        
        # Showcase button
        if st.button(f"🌐 {t('nav.showcase', 'Showcase')}", use_container_width=True, 
                    type="primary" if st.session_state.page == "showcase" else "secondary"):
            navigate_to("showcase")
        
        st.markdown("---")
        
        if st.button(f"🚪 {t('app.logout')}", use_container_width=True):
            logout()
        
        st.markdown("---")
        st.caption("© 2024 SmartCar AI-Dealer")
        
        # Help Dialog
        if st.session_state.get('show_help', False):
            show_help_dialog()
        
        # Features Dialog
        if st.session_state.get('show_features', False):
            show_features_dialog()
        
        # About Dialog
        if st.session_state.get('show_about', False):
            show_about_dialog()


