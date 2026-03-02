"""
pages_app/auth_pages.py - صفحات المصادقة
SmartCar AI-Dealer
"""

import streamlit as st
from utils.i18n import t, get_current_lang, set_language, get_language_display_name, SUPPORTED_LANGUAGES, apply_language_css
from auth import AuthManager
from utils.notifier import NotificationManager
from components.html_components import render_universal_header
from components.navigation import navigate_to


# ======================

def login_page():
    """صفحة تسجيل الدخول"""
    
    # إخفاء القائمة الجانبية في صفحة تسجيل الدخول
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none !important;}
        [data-testid="stSidebarNav"] {display: none !important;}
        section[data-testid="stSidebar"] {display: none !important;}
        .css-1d391kg {display: none !important;}
        button[kind="header"] {display: none !important;}
    </style>
    """, unsafe_allow_html=True)

    # Render the universal header with welcome message
    render_universal_header("Welcome to SmartCar!", "✨ AI-Powered Dealer Solution")

    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Language Selector
        sub_col1, sub_col2 = st.columns([1, 1.5])
        with sub_col1:
            from utils.i18n import get_current_lang, set_language
            
            lang_options = list(SUPPORTED_LANGUAGES.keys())
            lang_labels = [get_language_display_name(code) for code in lang_options]
            
            # اللغة الحالية من URL أو session
            current_lang = get_current_lang()
            current_idx = lang_options.index(current_lang) if current_lang in lang_options else 0
            
            # عرض القائمة
            selected = st.selectbox(
                "🌐 Language / اللغة",
                lang_labels,
                index=current_idx,
                key="login_lang_select"
            )
            
            # تحديث اللغة
            new_idx = lang_labels.index(selected)
            new_lang = lang_options[new_idx]
            if new_lang != current_lang:
                set_language(new_lang)
                st.rerun()
        
        with sub_col2:
            st.subheader(f"🔐 {t('login.title')}")
        
        # Apply RTL/LTR CSS
        apply_language_css()
        
        with st.form("login_form"):
            username = st.text_input(t('login.username'), key="login_username")
            password = st.text_input(t('login.password'), type="password", key="login_password")
            
            # Checkbox for "Save" - CSS handles RTL layout
            remember = st.checkbox(t('buttons.save'), key="remember_me")
            
            # GDPR Consent Section
            st.markdown("---")
            with st.expander(f"📋 {t('gdpr_login.title')}", expanded=False):
                st.markdown(t('gdpr_login.full_text'))
            
            # GDPR checkbox - checked by default (Enter key submits with consent)
            gdpr_consent = st.checkbox(f"✅ {t('gdpr_login.consent_checkbox')}", key="gdpr_consent_login", value=True)
            
            submitted = st.form_submit_button(t('login.submit'), use_container_width=True)
            
            if submitted:
                if not username or not password:
                    st.error(f"⚠️ {t('messages.required_field')}")
                elif not gdpr_consent:
                    st.error(f"⚠️ {t('gdpr_login.consent_required')}")
                else:
                    auth = AuthManager()
                    success, message, user_data = auth.login_user(username, password)
                    
                    if success:
                        # حفظ اللغة الحالية قبل الانتقال
                        current_lang = st.session_state.get('language', 'de')
                        st.session_state.user = user_data
                        st.session_state.page = 'home'
                        st.session_state['language'] = current_lang
                        st.session_state['gdpr_accepted'] = True  # حفظ موافقة GDPR
                        
                        # إنشاء ملف JSON للعميل
                        try:
                            import json
                            import os
                            from datetime import datetime
                            
                            customers_dir = os.path.join(os.path.dirname(__file__), 'customers')
                            os.makedirs(customers_dir, exist_ok=True)
                            
                            # اسم الملف = اسم المستخدم
                            customer_filename = f"{user_data.get('username', 'unknown')}.json"
                            customer_filepath = os.path.join(customers_dir, customer_filename)
                            
                            # بيانات العميل الأساسية
                            customer_data = {
                                "language": current_lang,
                                "full_name": user_data.get('full_name', ''),
                                "email": user_data.get('email', ''),
                                "last_login": datetime.now().isoformat(),
                                # سيتم إضافة المزيد لاحقاً
                            }
                            
                            # حفظ الملف
                            with open(customer_filepath, 'w', encoding='utf-8') as f:
                                json.dump(customer_data, f, ensure_ascii=False, indent=4)
                        except Exception as e:
                            pass  # لا نوقف تسجيل الدخول بسبب خطأ في الملف
                        
                        st.success(f"✅ {t('messages.success')}")
                        st.rerun()
                    else:
                        st.error(f"❌ {t('login.error_invalid')}")
        
        st.markdown("---")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button(f"📝 {t('login.create_account')}", use_container_width=True, key="btn_register"):
                lang = st.session_state.get('language', 'de')
                st.session_state.page = 'register'
                st.session_state['language'] = lang
                st.rerun()
        with col_b:
            if st.button(f"🔓 {t('profile.change_password')}", use_container_width=True, key="btn_forgot"):
                lang = st.session_state.get('language', 'de')
                st.session_state.page = 'forgot_password'
                st.session_state['language'] = lang
                st.rerun()


# ======================
# صفحة التسجيل
# ======================

def register_page():
    """صفحة إنشاء حساب جديد"""
    st.markdown(f"""
    <div class="main-header">
        <h1>📝 {t('register.title')}</h1>
    </div>
    <div class="sub-header">
        <p>{t('app.subtitle')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("register_form"):
            username = st.text_input(f"{t('register.username')} *")
            email = st.text_input(f"{t('register.email')} *")
            full_name = st.text_input(t('register.full_name'))
            phone = st.text_input(t('profile.phone'))
            
            password = st.text_input(f"{t('register.password')} *", type="password")
            confirm_password = st.text_input(f"{t('register.confirm_password')} *", type="password")
            
            agree = st.checkbox(t('register.agree_terms', "I agree to the Terms of Service and Privacy Policy"))
            
            submitted = st.form_submit_button(t('register.submit'), use_container_width=True)
            
            if submitted:
                if not username or not email or not password:
                    st.error(f"⚠️ {t('messages.required_field')}")
                elif password != confirm_password:
                    st.error(f"⚠️ {t('register.error_password_match', 'Passwords do not match')}")
                elif not agree:
                    st.error(f"⚠️ {t('register.error_agree', 'Please agree to terms')}")
                else:
                    auth = AuthManager()
                    success, message, user_id = auth.register_user(
                        username=username,
                        email=email,
                        password=password,
                        full_name=full_name,
                        phone=phone
                    )
                    
                    if success:
                        st.success(f"✅ {message}")
                        st.info(t('admin.can_login_now'))
                        
                        # إرسال بريد ترحيبي
                        try:
                            notifier = NotificationManager()
                            notifier.send_welcome_email(email, username)
                        except:
                            pass
                    else:
                        st.error(f"❌ {message}")
        
        st.markdown("---")
        
        if st.button(f"← {t('admin.back_to_login')}", use_container_width=True):
            navigate_to('login')


# ======================
# صفحة نسيان كلمة المرور
# ======================

def forgot_password_page():
    """صفحة نسيان كلمة المرور"""
    st.markdown(f"""
    <div class="main-header">
        <h1>🔓 {t('admin.password_reset_title')}</h1>
    </div>
    <div class="sub-header">
        <p>{t('admin.password_reset_hint')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.info(t('admin.enter_email_reset'))
        
        with st.form("forgot_form"):
            email = st.text_input(t('register.email'))
            submitted = st.form_submit_button(t('admin.send_reset_link'), use_container_width=True)
            
            if submitted:
                if not email:
                    st.error(f"⚠️ {t('admin.enter_email')}")
                else:
                    auth = AuthManager()
                    success, message, token = auth.generate_reset_token(email)
                    st.success(f"✅ {t('admin.email_reset_sent')}")
        
        st.markdown("---")
        
        if st.button(f"← {t('admin.back_to_login')}", use_container_width=True):
            navigate_to('login')


# ======================
# الصفحة الرئيسية
