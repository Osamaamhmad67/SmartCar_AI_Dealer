"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         SmartCar AI-Dealer                                   ║
║                    نظام تقييم وبيع السيارات بالذكاء الاصطناعي                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  المطور: Osama Ahmed                                                         ║
║  الإصدار: 2.0                                                                ║
║  تاريخ الإنشاء: 2024                                                         ║
║  آخر تحديث: يناير 2026                                                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                              فهرس الملف                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  📦 الاستيرادات ................................. السطر ~25                  ║
║  🎨 مكونات HTML/CSS ............................ السطر ~40-1610              ║
║     ├─ get_clock_html()                                                      ║
║     ├─ get_home_subheader_html()                                             ║
║     ├─ get_predict_subheader_html()                                          ║
║     ├─ get_invoices_subheader_html()                                         ║
║     ├─ get_profile_stats_html()                                              ║
║     ├─ get_admin_stats_html()                                                ║
║     ├─ get_results_page_html()                                               ║
║     ├─ get_analysis_results_html()                                           ║
║     ├─ get_section_header_html()                                             ║
║     ├─ get_admin_dashboard_html()                                            ║
║     └─ get_profile_subheader_html()                                          ║
║  ⚙️ إعدادات Streamlit .......................... السطر ~1630                 ║
║  🎨 الأنماط المخصصة (CSS) ...................... السطر ~1640                 ║
║  🔧 تهيئة النظام ............................... السطر ~1920                 ║
║     ├─ init_system()                                                         ║
║     ├─ init_session_state()                                                  ║
║     ├─ navigate_to()                                                         ║
║     └─ logout()                                                              ║
║  📄 صفحات التطبيق .............................. السطر ~1985-6955            ║
║     ├─ login_page() .............. تسجيل الدخول                              ║
║     ├─ register_page() ........... إنشاء حساب                                ║
║     ├─ forgot_password_page() .... نسيان كلمة المرور                         ║
║     ├─ home_page() ............... الصفحة الرئيسية + لوحة الأدمن            ║
║     ├─ predict_page() ............ تقييم السيارة                             ║
║     ├─ results_page() ............ عرض النتائج                               ║
║     ├─ invoices_page() ........... الفواتير السابقة + OCR                    ║
║     ├─ profile_page() ............ الملف الشخصي                              ║
║     ├─ change_password_page() .... تغيير كلمة المرور                         ║
║     ├─ admin_page() .............. لوحة تحكم المشرف                          ║
║     ├─ verify_identity_page() .... التحقق من الهوية                          ║
║     └─ checkout_page() ........... الدفع والتعاقد                            ║
║  💬 الحوارات (Dialogs) ......................... السطر ~5695                 ║
║     ├─ show_features_dialog()                                                ║
║     ├─ show_about_dialog()                                                   ║
║     └─ show_help_dialog()                                                    ║
║  📱 الشريط الجانبي ............................. السطر ~5850                 ║
║  🚀 الدالة الرئيسية main() .................... السطر ~6960                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                            الميزات الرئيسية                                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ✅ تقييم أسعار السيارات بالذكاء الاصطناعي                                   ║
║  ✅ مسح المستندات OCR (البطاقة الشخصية + رخصة القيادة)                       ║
║  ✅ نظام دفع متعدد (نقدي + تقسيط)                                            ║
║  ✅ إنشاء فواتير وعقود PDF                                                   ║
║  ✅ دعم متعدد اللغات (العربية + الألمانية + الإنجليزية)                       ║
║  ✅ لوحة تحكم للمشرف مع إحصائيات شاملة                                       ║
║  ✅ نظام مصادقة كامل مع GDPR                                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""


import streamlit as st
import sys
import os
import base64
import json
from pathlib import Path
from datetime import datetime, timedelta
import time
import streamlit.components.v1 as components
from io import BytesIO

# === i18n ===
from utils.i18n import t, init_language, set_language, get_current_lang, apply_language_css, SUPPORTED_LANGUAGES, get_language_display_name, is_rtl, clear_translations_cache, rtl_tabs

# === Components ===
from components.html_components import *
from components.css_styles import load_custom_css
from components.dialogs import show_features_dialog, show_about_dialog, show_help_dialog
from components.sidebar import render_sidebar

# === Pages ===
from pages_app.auth_pages import login_page, register_page, forgot_password_page
from pages_app.home_page import home_page
from pages_app.predict_pages import predict_page, results_page, render_progress_bar
from pages_app.invoices_page import invoices_page
from pages_app.profile_pages import profile_page, change_password_page
from pages_app.admin_page import admin_page
from pages_app.checkout_pages import verify_identity_page, checkout_page
from pages_app.inventory_page import inventory_page
from components.chatbot_component import render_chatbot
from pages_app.showcase_page import showcase_page
from pages_app.appointments_page import appointments_page
from pages_app.branches_page import branches_page
from components.notifications_bell import render_notification_bell
from components.reviews_component import render_reviews

sys.path.append(str(Path(__file__).parent))

# استيراد المكونات
from config import Config
from auth import AuthManager
from db_manager import DatabaseManager
from utils.predictor import PricePredictor
from groq_client import CarAIClient as GroqCarAnalyzer
from utils.validation import validate_car_image, ImageValidator
# from utils.pdf_generator import InvoiceGenerator
from utils.notifier import NotificationManager
from utils.cache_manager import CacheManager


# ======================
# إعدادات الصفحة
# ======================

st.set_page_config(
    page_title="SmartCar AI-Dealer",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# التمرير للأعلى فقط عند تغيير الصفحة أو عند الطلب صريحاً
from streamlit_scroll_to_top import scroll_to_here

# تتبع الصفحة الحالية للتمرير عند التغيير فقط
if 'last_page_for_scroll' not in st.session_state:
    st.session_state.last_page_for_scroll = None

current_page = st.session_state.get('page', 'home')
should_scroll = st.session_state.get('scroll_to_top', False)

# التمرير فقط عند تغيير الصفحة أو عند الطلب صريحاً
if current_page != st.session_state.last_page_for_scroll or should_scroll:
    st.session_state.last_page_for_scroll = current_page
    st.session_state['scroll_to_top'] = False
    scroll_to_here()


# ======================
# الأنماط المخصصة
# ======================


# ======================

def init_system():
    """تهيئة جميع مكونات النظام"""
    # إنشاء المجلدات
    Config.create_directories()
    
    # التحقق من الإعدادات
    Config.validate_config()
    
    if Config.logger:
        Config.logger.info("[OK] System initialized successfully")


def init_session_state():
    """تهيئة حالة الجلسة"""
    defaults = {
        'page': 'login',
        'user': None,
        'prediction_data': None,
        'car_details': {},
        'uploaded_image': None,
        'analysis_result': None,
        'last_transaction_id': None,
        'logo_base64': "",
        'language': 'de'  # اللغة الافتراضية
    }
    
    # تحميل اللوغو مرة واحدة
    if not st.session_state.get('logo_base64'):
        logo_path = r"C:\Users\Osama\Desktop\SmartCar_AI_Dealer\logs\logo.png"
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                st.session_state.logo_base64 = base64.b64encode(f.read()).decode()
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ======================
# دوال التنقل
# ======================

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


# ======================
# صفحة تسجيل الدخول
# ======================

def main():
    """الدالة الرئيسية"""
    # تهيئة النظام
    init_system()
    init_session_state()
    
    # تهيئة اللغة
    init_language()
    
    # تحميل CSS الأساسي أولاً
    load_custom_css()
    
    # ثم تطبيق CSS اللغة (RTL/LTR) لتتفوق على CSS الأساسي
    apply_language_css()
    
    # التمرير للأعلى عند التنقل
    if st.session_state.get('scroll_to_top', False):
        st.session_state['scroll_to_top'] = False
        from streamlit_scroll_to_top import scroll_to_here
        scroll_to_here()
    
    # التوجيه
    if st.session_state.user:
        # المستخدم مسجل الدخول
        render_sidebar()
        render_chatbot()
        render_notification_bell()
        
        page_handlers = {
            'home': home_page,
            'predict': predict_page,
            'results': results_page,
            'verify_identity': verify_identity_page,
            'checkout': checkout_page,
            'invoices': invoices_page,
            'profile': profile_page,
            'change_password': change_password_page,
            'admin': admin_page,
            'inventory': inventory_page,
            'showcase': showcase_page,
            'appointments': appointments_page,
            'branches': branches_page
        }
        
        current_page = st.session_state.page
        
        if current_page in page_handlers:
            page_handlers[current_page]()

        else:
            navigate_to('home')
    else:
        # المستخدم غير مسجل
        page_handlers = {
            'login': login_page,
            'register': register_page,
            'forgot_password': forgot_password_page
        }
        
        current_page = st.session_state.page
        
        if current_page in page_handlers:
            page_handlers[current_page]()
        else:
            navigate_to('login')


# ======================
# نقطة البداية
# ======================

if __name__ == "__main__":
    main()
