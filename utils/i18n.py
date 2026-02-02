"""
utils/i18n.py - نظام التوطين البسيط
SmartCar AI-Dealer
"""

import json
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
from typing import Optional

LOCALES_DIR = Path(__file__).parent.parent / "locales"

SUPPORTED_LANGUAGES = {
    'de': {'name': 'Deutsch', 'dir': 'ltr', 'flag': '🇩🇪'},
    'ar': {'name': 'العربية', 'dir': 'rtl', 'flag': '🇸🇦'},
    'en': {'name': 'English', 'dir': 'ltr', 'flag': '🇬🇧'}
}

DEFAULT_LANGUAGE = 'de'
_translations_cache = {}


def load_translations(lang: str, force_reload: bool = False) -> dict:
    global _translations_cache
    # إعادة تحميل الترجمات دائماً لضمان ظهور التحديثات
    force_reload = True
    if lang in _translations_cache and not force_reload:
        return _translations_cache[lang]
    
    file_path = LOCALES_DIR / f"{lang}.json"
    if not file_path.exists():
        file_path = LOCALES_DIR / f"{DEFAULT_LANGUAGE}.json"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)
            _translations_cache[lang] = translations
            return translations
    except:
        return {}


def clear_translations_cache():
    """Clear the translations cache to force reload"""
    global _translations_cache
    _translations_cache = {}


def get_current_lang() -> str:
    """الحصول على اللغة الحالية من session_state"""
    lang = st.session_state.get('language', DEFAULT_LANGUAGE)
    if lang in SUPPORTED_LANGUAGES:
        return lang
    return DEFAULT_LANGUAGE


def set_language(lang: str):
    """تعيين اللغة في session_state"""
    if lang in SUPPORTED_LANGUAGES:
        st.session_state['language'] = lang


def get_direction() -> str:
    return SUPPORTED_LANGUAGES.get(get_current_lang(), {}).get('dir', 'ltr')


def is_rtl() -> bool:
    return get_direction() == 'rtl'


def t(key: str, default: Optional[str] = None, **kwargs) -> str:
    """ترجمة نص بناءً على مفتاح"""
    lang = get_current_lang()
    translations = load_translations(lang)
    
    keys = key.split('.')
    value = translations
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k)
        else:
            value = None
            break
    
    if value is None:
        return default if default else key
    
    if kwargs and isinstance(value, str):
        try:
            return value.format(**kwargs)
        except:
            return value
    return value


def get_language_display_name(code: str) -> str:
    info = SUPPORTED_LANGUAGES.get(code, {})
    return f"{info.get('flag', '')} {info.get('name', code)}"


def init_language():
    """تهيئة اللغة - فقط إذا لم تكن موجودة"""
    if 'language' not in st.session_state:
        st.session_state['language'] = DEFAULT_LANGUAGE


def rtl_tabs(tab_labels: list):
    """
    إنشاء تبويبات مع دعم RTL
    للغة العربية، يتم عكس ترتيب التبويبات في العرض
    Returns: tuple of tab objects in ORIGINAL order (not reversed)
    """
    if is_rtl():
        # Reverse the labels for display (CSS row-reverse doesn't work reliably)
        reversed_labels = list(reversed(tab_labels))
        tabs = st.tabs(reversed_labels)
        # Return tabs in reversed order so they match original label order
        return tuple(reversed(tabs))
    else:
        return st.tabs(tab_labels)


def rtl_checkbox(label: str, key: str = None, value: bool = False, help: str = None):
    """
    Checkbox مخصص مع دعم RTL
    يضع المربع على اليمين والنص على اليسار في وضع RTL
    """
    if is_rtl():
        # Create a container with checkbox first, then check value
        checkbox_result = st.checkbox(label, key=key, value=value, help=help)
        return checkbox_result
    else:
        # LTR: normal checkbox
        return st.checkbox(label, key=key, value=value, help=help)

def apply_language_css():
    """تطبيق CSS للغة الحالية"""
    if is_rtl():
        st.markdown("""<style>
        /* Import Arabic Font */
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700&display=swap');
        
        /* ═══════════════════════════════════════════════════════════════════════
           RTL MASTER STYLES - Arabic Language Support
           ═══════════════════════════════════════════════════════════════════════ */
        
        /* === الاتجاه العام === */
        html, body, .stApp, .main, .block-container,
        [data-testid="stAppViewContainer"],
        [data-testid="stMainBlockContainer"] { 
            direction: rtl !important; 
            text-align: right !important;
            font-family: 'Cairo', 'Noto Sans Arabic', 'Segoe UI', 'Tahoma', sans-serif !important;
            -webkit-font-smoothing: antialiased !important;
            -moz-osx-font-smoothing: grayscale !important;
        }
        
        /* Sidebar direction only */
        [data-testid="stSidebar"],
        [data-testid="stSidebarContent"] {
            direction: rtl !important;
            text-align: right !important;
        }
        
        /* Hide any remaining white decorations */
        [data-testid="stDecoration"] {
            display: none !important;
        }
        
        /* Hide Material Icon ligature text (keyboard_double_arrow etc) */
        [data-testid="stSidebarCollapseButton"] span,
        [data-testid="collapsedControl"] span,
        button[kind="headerNoPadding"] span,
        [data-testid="stSidebar"] button span[class*="Icon"],
        span[class*="material-icons"] {
            font-size: 0 !important;
            overflow: hidden !important;
        }
        
        /* Make sure SVG icons still show */
        [data-testid="stSidebarCollapseButton"] svg,
        [data-testid="collapsedControl"] svg,
        button[kind="headerNoPadding"] svg {
            font-size: 1.5rem !important;
            width: 24px !important;
            height: 24px !important;
        }
        
        /* Arabic text clarity - font and color */
        * {
            font-family: 'Cairo', 'Noto Sans Arabic', 'Segoe UI', 'Tahoma', sans-serif !important;
        }
        
        /* PREMIUM TEXT - Smoky White on Soft Black */
        .stApp .main *:not([style*="color"]):not(a):not(svg):not(path) {
            color: #E0E0E0 !important;
            -webkit-text-fill-color: #E0E0E0 !important;
        }
        
        /* Headlines - Pure White */
        h1, h2, h3, .main-header, [data-testid="stHeader"] {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           PREMIUM WIDGET STYLING - Glassmorphism Design
           ═══════════════════════════════════════════════════════════════════════ */
        
        /* 1. Premium Input Fields with Glass Effect */
        .stTextInput input, 
        .stSelectbox div[data-baseweb="select"], 
        .stNumberInput input,
        .stTextArea textarea {
            color: #E0E0E0 !important;
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(212, 175, 55, 0.3) !important;
            backdrop-filter: blur(10px);
        }
        
        /* 2. Premium Dropdowns with Soft Black */
        div[data-baseweb="popover"], 
        div[data-baseweb="menu"], 
        ul[role="listbox"] {
            background-color: #161B22 !important;
            color: white !important;
        }
        
        div[data-baseweb="select"] span,
        div[data-baseweb="select"] div {
            color: white !important;
        }
        
        /* 3. تحسين قراءة العناوين (Labels) فوق الحقول */
        .stTextInput label, 
        .stSelectbox label, 
        .stNumberInput label,
        .stTextArea label,
        .stRadio label,
        .stCheckbox label {
            color: #D4AF37 !important;
            -webkit-text-fill-color: #D4AF37 !important;
            font-weight: bold !important;
        }
        
        /* 4. تحسين الأزرار الثانوية (Secondary Buttons) */
        button[kind="secondary"],
        [data-testid="stButton"] button:not([data-testid="baseButton-primary"]) {
            background-color: transparent !important;
            border: 2px solid #D4AF37 !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        
        button[kind="secondary"]:hover,
        [data-testid="stButton"] button:not([data-testid="baseButton-primary"]):hover {
            background-color: rgba(240, 180, 41, 0.1) !important;
            border-color: #ffffff !important;
        }
        
        /* 5. الأزرار الرئيسية (Primary Buttons) - نص أبيض */
        [data-testid="stButton"] button[data-testid="baseButton-primary"],
        button[kind="primary"] {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        
        /* 6. Radio Buttons - نص أبيض على الخلفية الداكنة - ALL SELECTORS */
        .stRadio,
        .stRadio *,
        .stRadio label,
        .stRadio label *,
        .stRadio div,
        .stRadio span,
        .stRadio p,
        .stRadio > div,
        .stRadio > div > div,
        .stRadio > div > div > label,
        .stRadio > div > div > label *,
        [data-testid="stRadio"],
        [data-testid="stRadio"] *,
        [data-testid="stRadio"] div,
        [data-testid="stRadio"] label,
        [data-testid="stRadio"] span,
        [data-testid="stRadio"] p,
        [data-baseweb="radio"],
        [data-baseweb="radio"] + div,
        [data-baseweb="radio"] ~ div,
        [data-baseweb="radio"] ~ span,
        div[role="radiogroup"],
        div[role="radiogroup"] *,
        div[role="radiogroup"] label,
        div[role="radiogroup"] span,
        div[role="radiogroup"] p,
        div[role="radiogroup"] div {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        
        /* 7. Checkbox - نص أبيض */
        .stCheckbox label,
        .stCheckbox label span,
        [data-testid="stCheckbox"] label,
        [data-testid="stCheckbox"] label span {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           تصحيحات ألوان محددة - SPECIFIC COLOR FIXES ONLY
           لا نغير الألوان بشكل عام، فقط المناطق المشكلة
           ═══════════════════════════════════════════════════════════════════════ */
        
        /* File uploader dropzone - ensure dark text on white background */
        [data-testid="stFileUploaderDropzone"] span,
        [data-testid="stFileUploaderDropzone"] small,
        [data-testid="stFileUploaderDropzone"] p {
            color: #333333 !important;
            -webkit-text-fill-color: #333333 !important;
        }
        
        /* Camera input tabs - ensure readable text */
        .stCameraInput button[role="tab"],
        [data-testid="stCameraInput"] button[role="tab"] {
            color: #333333 !important;
            -webkit-text-fill-color: #333333 !important;
        }
        
        /* Browse files button - gold styling */
        [data-testid="stFileUploaderDropzone"] button,
        .stFileUploader button,
        [data-testid="stFileUploader"] button {
            background: linear-gradient(135deg, #D4A84B 0%, #C9952C 100%) !important;
            color: #0E1117 !important;
            -webkit-text-fill-color: #0E1117 !important;
            border: 2px solid #B8860B !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 8px 20px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 8px rgba(212, 168, 75, 0.3) !important;
        }
        
        [data-testid="stFileUploaderDropzone"] button:hover,
        .stFileUploader button:hover {
            background: linear-gradient(135deg, #E5B95C 0%, #D4A84B 100%) !important;
            box-shadow: 0 4px 12px rgba(212, 168, 75, 0.5) !important;
            transform: translateY(-1px) !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           UNIFIED DARK THEME - نظام ألوان موحّد
           All general text = WHITE on dark backgrounds
           Styled elements preserve their explicit colors via inherit
           ═══════════════════════════════════════════════════════════════════════ */
        
        /* General text color - WHITE for dark theme */
        .stMarkdown,
        [data-testid="stMarkdownContainer"] {
            color: #FFFFFF !important;
        }
        
        /* BUT: Elements with inline style should inherit from their parent */
        .stMarkdown div[style],
        .stMarkdown div[style] *,
        [data-testid="stMarkdownContainer"] div[style],
        [data-testid="stMarkdownContainer"] div[style] * {
            color: inherit !important;
            -webkit-text-fill-color: inherit !important;
        }
        
        /* Streamlit Alert Components (st.success, st.info, st.warning, st.error) 
           These have light backgrounds, need dark text */
        [data-testid="stAlert"],
        .stAlert,
        [data-testid="stAlertContainer"],
        div[data-baseweb="notification"] {
            direction: rtl !important;
        }
        
        [data-testid="stAlert"] p,
        [data-testid="stAlert"] span,
        .stAlert p,
        .stAlert span,
        div[data-baseweb="notification"] div {
            color: #0E1117 !important;
            -webkit-text-fill-color: #0E1117 !important;
        }
        
        /* Camera input and all input labels */
        .stCameraInput *,
        [data-testid="stCameraInput"] *,
        .stTextInput label,
        .stSelectbox label,
        .stMultiselect label {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        
        /* === الشريط الجانبي === */
        .stSidebar, [data-testid="stSidebar"], 
        [data-testid="stSidebarContent"],
        section[data-testid="stSidebar"] { 
            direction: rtl !important; 
            text-align: right !important; 
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           الأعمدة - COLUMNS (Critical for RTL)
           ═══════════════════════════════════════════════════════════════════════ */
        .stHorizontalBlock,
        .row-widget.stHorizontalBlock,
        [data-testid="stHorizontalBlock"],
        [data-testid="stColumns"],
        div[data-testid="stHorizontalBlock"],
        div.stHorizontalBlock { 
            flex-direction: row-reverse !important; 
            direction: rtl !important;
        }
        
        [data-testid="column"],
        [data-testid="stColumn"],
        div[data-testid="column"] { 
            direction: rtl !important; 
            text-align: right !important; 
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           التبويبات - TABS (CRITICAL RTL FIX)
           ═══════════════════════════════════════════════════════════════════════ */
        .stTabs,
        [data-testid="stTabs"] {
            direction: rtl !important;
        }
        
        /* Tab list container - RTL direction only (rtl_tabs handles label order) */
        .stTabs [data-baseweb="tab-list"],
        [data-testid="stTabs"] [data-baseweb="tab-list"],
        [role="tablist"],
        div[data-baseweb="tab-list"],
        .stTabs > div > div:first-child,
        [data-testid="stTabs"] > div > div:first-child { 
            direction: rtl !important;
        }
        
        /* Individual tabs */
        .stTabs [data-baseweb="tab"],
        [data-testid="stTabs"] button,
        [role="tab"],
        button[data-baseweb="tab"] { 
            direction: rtl !important;
        }
        
        /* Tabs in camera/file section (white background) - DARK text */
        .stCameraInput [data-baseweb="tab"],
        .stCameraInput button[data-baseweb="tab"],
        [data-testid="stCameraInput"] button,
        [data-testid="stCameraInput"] [role="tab"] {
            color: #333333 !important;
            -webkit-text-fill-color: #333333 !important;
            background-color: #f0f0f0 !important;
        }
        
        /* Selected tab styling */
        .stCameraInput button[aria-selected="true"],
        [data-testid="stCameraInput"] button[aria-selected="true"] {
            color: #0E1117 !important;
            -webkit-text-fill-color: #0E1117 !important;
            background: linear-gradient(135deg, #D4A84B 0%, #C9952C 100%) !important;
            border-bottom: 3px solid #B8860B !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           القوائم المنسدلة - SELECTBOX
           ═══════════════════════════════════════════════════════════════════════ */
        .stSelectbox, .stMultiselect,
        [data-testid="stSelectbox"],
        [data-testid="stMultiselect"] { 
            direction: rtl !important; 
        }
        
        .stSelectbox > div,
        .stMultiselect > div,
        [data-testid="stSelectbox"] > div { 
            direction: rtl !important; 
        }
        
        /* Selectbox inner container - flip arrow position */
        [data-baseweb="select"],
        .stSelectbox [data-baseweb="select"] { 
            direction: rtl !important; 
        }
        
        /* Control container - reverse order to put arrow on right */
        [data-baseweb="select"] > div,
        [data-baseweb="select"] > div:first-child,
        .stSelectbox [data-baseweb="select"] > div { 
            flex-direction: row-reverse !important; 
            direction: rtl !important;
        }
        
        /* The actual select control */
        [data-baseweb="select"] [class*="control"],
        [data-baseweb="select"] [class*="ControlContainer"] {
            flex-direction: row-reverse !important;
        }
        
        /* Value container */
        [data-baseweb="select"] [class*="valueContainer"],
        [data-baseweb="select"] [class*="Value"] {
            direction: rtl !important;
            text-align: right !important;
        }
        
        /* Selectbox text direction - simple RTL fix */
        [data-baseweb="select"] input,
        [data-baseweb="select"] [class*="value"],
        .stSelectbox [data-baseweb="select"] span {
            direction: rtl !important;
            text-align: right !important;
        }
        
        /* Dropdown menu */
        [data-baseweb="popover"],
        [data-baseweb="menu"],
        [data-baseweb="list"],
        ul[role="listbox"] { 
            direction: rtl !important; 
            text-align: right !important; 
        }
        
        /* Dropdown options */
        [data-baseweb="menu"] li,
        [role="listbox"] li,
        [role="option"] {
            direction: rtl !important;
            text-align: right !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           حقول الإدخال - INPUT FIELDS
           ═══════════════════════════════════════════════════════════════════════ */
        .stTextInput input, 
        .stTextArea textarea,
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea { 
            direction: rtl !important; 
            text-align: right !important; 
        }
        
        .stNumberInput input,
        [data-testid="stNumberInput"] input { 
            direction: ltr !important; 
            text-align: left !important; 
        }
        
        /* Labels */
        .stTextInput label, 
        .stSelectbox label, 
        .stNumberInput label, 
        .stTextArea label,
        .stDateInput label,
        .stCheckbox label,
        [data-testid="stWidgetLabel"] {
            direction: rtl !important;
            text-align: right !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           حقل كلمة المرور - PASSWORD EYE ICON RTL
           ═══════════════════════════════════════════════════════════════════════ */
        /* Password field wrapper */
        .stTextInput > div > div,
        [data-testid="stTextInput"] > div > div {
            direction: rtl !important;
        }
        
        /* Password input container with button - BaseWeb */
        .stTextInput [data-baseweb="input"],
        .stTextInput [data-baseweb="base-input"],
        [data-testid="stTextInput"] [data-baseweb="input"],
        [data-testid="stTextInput"] [data-baseweb="base-input"] {
            flex-direction: row-reverse !important;
            display: flex !important;
        }
        
        
        /* ═══════════════════════════════════════════════════════════════════════
           النماذج والأزرار - FORMS & BUTTONS
           ═══════════════════════════════════════════════════════════════════════ */
        .stForm, [data-testid="stForm"] { 
            direction: rtl !important; 
        }
        
        .stButton button,
        [data-testid="stButton"] button { 
            direction: rtl !important; 
        }
        
        /* Ensure button text is visible */
        .stButton button p,
        .stButton button span,
        [data-testid="stButton"] button p,
        [data-testid="stButton"] button span {
            color: inherit !important;
            -webkit-text-fill-color: inherit !important;
            visibility: visible !important;
            opacity: 1 !important;
        }
        
        /* Primary (dark) button text color */
        .stButton button[kind="primary"],
        .stButton button[data-testid="baseButton-primary"],
        [data-testid="stButton"] button[data-testid="baseButton-primary"] {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        
        .stButton button[kind="primary"] p,
        .stButton button[kind="primary"] span,
        .stButton button[data-testid="baseButton-primary"] p,
        .stButton button[data-testid="baseButton-primary"] span,
        [data-testid="stButton"] button[data-testid="baseButton-primary"] p,
        [data-testid="stButton"] button[data-testid="baseButton-primary"] span {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            text-shadow: 0 0 0 #ffffff !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           العناصر الموسعة - EXPANDER
           ═══════════════════════════════════════════════════════════════════════ */
        /* Expander container */
        [data-testid="stExpander"] {
            text-align: right !important;
        }
        
        /* Expander header */
        .streamlit-expanderHeader,
        [data-testid="stExpander"] summary,
        details summary { 
            text-align: right !important;
        }
        
        /* Hide Material Icon text (keyboard_arrow_right) that appears */
        [data-testid="stExpander"] summary span[data-testid*="Icon"],
        [data-testid="stExpander"] summary .material-icons,
        [data-testid="stExpander"] summary [class*="icon"],
        [data-testid="stExpander"] summary svg + span,
        details summary span[data-testid*="Icon"] {
            font-size: 0 !important;
            color: transparent !important;
            width: 0 !important;
            overflow: hidden !important;
        }
        
        /* Keep the SVG arrow visible */
        [data-testid="stExpander"] summary svg,
        details summary svg {
            font-size: 1rem !important;
            width: auto !important;
        }
        
        /* Expander content - RTL for inner content */
        [data-testid="stExpander"] > div:not(:first-child),
        details > *:not(summary) {
            direction: rtl !important;
            text-align: right !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           الجداول والعناوين - TABLES & HEADERS
           ═══════════════════════════════════════════════════════════════════════ */
        .stDataFrame,
        [data-testid="stDataFrame"] { 
            direction: rtl !important; 
        }
        
        h1, h2, h3, h4, h5, h6,
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { 
            direction: rtl !important; 
            text-align: right !important; 
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           الرسائل والتنبيهات - ALERTS
           ═══════════════════════════════════════════════════════════════════════ */
        .stAlert, 
        [data-testid="stAlert"],
        .stInfo, .stWarning, .stError, .stSuccess { 
            direction: rtl !important; 
            text-align: right !important; 
        }
        
        /* Alert text colors - ensure visibility on light backgrounds */
        .stAlert p,
        .stAlert span,
        [data-testid="stAlert"] p,
        [data-testid="stAlert"] span,
        .stInfo p, .stWarning p, .stError p, .stSuccess p,
        [data-testid="stNotification"] p,
        [data-testid="stNotification"] span {
            color: #333333 !important;
            -webkit-text-fill-color: #333333 !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           النصوص والفقرات - TEXT & PARAGRAPHS
           ═══════════════════════════════════════════════════════════════════════ */
        .stMarkdown, 
        .stMarkdown p,
        .stCaption,
        [data-testid="stMarkdownContainer"],
        [data-testid="stCaptionContainer"] { 
            direction: rtl !important; 
            text-align: right !important; 
        }
        
        /* File uploader RTL only - colors handled by theme */
        .stFileUploader,
        [data-testid="stFileUploader"] {
            direction: rtl !important;
            text-align: right !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           Radio و Checkbox - CRITICAL RTL FIX
           ═══════════════════════════════════════════════════════════════════════ */
        /* Checkbox container - align right */
        .stCheckbox,
        [data-testid="stCheckbox"] {
            direction: rtl !important;
            text-align: right !important;
            display: flex !important;
            justify-content: flex-end !important;
        }
        
        /* ALL checkbox labels - checkbox on left, text on right */
        .stCheckbox label,
        [data-testid="stCheckbox"] label,
        [data-baseweb="checkbox"],
        .stApp .stCheckbox label,
        .stApp [data-testid="stCheckbox"] label,
        div[data-testid="stCheckbox"] > label {
            display: inline-flex !important;
            flex-direction: row !important;
            align-items: center !important;
            gap: 6px !important;
            width: auto !important;
        }
        
        /* Text inside checkbox - RTL direction and improved clarity */
        .stCheckbox label span,
        .stCheckbox label p,
        .stCheckbox label div,
        [data-testid="stCheckbox"] label span,
        [data-testid="stCheckbox"] label p {
            direction: rtl !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            color: #000000 !important;
            text-shadow: none !important;
        }
        
        /* Radio button labels - make text visible */
        .stRadio label,
        .stRadio label span,
        .stRadio label p,
        .stRadio [role="radio"] span,
        .stRadio > div > label,
        .stRadio > div > div label,
        [data-testid="stRadio"] label,
        [data-testid="stRadio"] label span,
        [data-testid="stRadio"] label p,
        [data-testid="stRadio"] > div label,
        [data-testid="stRadio"] > div > div label {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            font-size: 0.95rem !important;
            font-weight: 500 !important;
            text-shadow: none !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           حقل كلمة المرور - PASSWORD FIELD
           ═══════════════════════════════════════════════════════════════════════ */
        /* Move password toggle icon to left side */
        .stTextInput [data-testid="stTextInputRootElement"] {
            direction: rtl !important;
        }
        .stTextInput [data-testid="stTextInputRootElement"] > div {
            flex-direction: row-reverse !important;
        }
        
        /* Password toggle button position */
        [data-testid="stTextInput"] button,
        .stTextInput button {
            order: -1 !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           إصلاحات إضافية - ADDITIONAL FIXES
           ═══════════════════════════════════════════════════════════════════════ */
        /* Expander icon position */
        [data-testid="stExpander"] > details > summary > span:first-child {
            order: 1 !important;
        }
        
        [data-testid="stExpander"] > details > summary {
            justify-content: flex-end !important;
        }
        
        /* Selectbox value container */
        [data-baseweb="select"] [data-testid="stSelectboxVirtualDropdown"],
        .stSelectbox [class*="valueContainer"] {
            direction: rtl !important;
            text-align: right !important;
        }
        
        /* Fix icon ordering in select */
        [data-baseweb="select"] svg {
            order: -1 !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           الأزرار الاحترافية - PROFESSIONAL BUTTONS
           ═══════════════════════════════════════════════════════════════════════ */
        /* Primary buttons - Gold styling */
        .stButton > button,
        button[kind="primary"],
        [data-testid="stFormSubmitButton"] button,
        .stFormSubmitButton button {
            background: linear-gradient(135deg, #D4A84B 0%, #C9952C 100%) !important;
            color: #0E1117 !important;
            -webkit-text-fill-color: #0E1117 !important;
            border: 2px solid #B8860B !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            padding: 10px 24px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(212, 168, 75, 0.3) !important;
        }
        
        .stButton > button:hover,
        button[kind="primary"]:hover,
        [data-testid="stFormSubmitButton"] button:hover {
            background: linear-gradient(135deg, #E5B95C 0%, #D4A84B 100%) !important;
            box-shadow: 0 6px 20px rgba(212, 168, 75, 0.5) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Secondary buttons */
        .stButton > button[kind="secondary"],
        button[kind="secondary"] {
            background: transparent !important;
            color: #D4A84B !important;
            -webkit-text-fill-color: #D4A84B !important;
            border: 2px solid #D4A84B !important;
        }
        
        .stButton > button[kind="secondary"]:hover {
            background: rgba(212, 168, 75, 0.1) !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           ضمان رؤية النصوص - ENSURE TEXT VISIBILITY
           ═══════════════════════════════════════════════════════════════════════ */
        /* All button text must be dark on light backgrounds */
        .stButton > button *,
        button span,
        button p {
            color: inherit !important;
            -webkit-text-fill-color: inherit !important;
        }
        
        /* Camera input Take Photo button */
        .stCameraInput button,
        [data-testid="stCameraInput"] button:not([role="tab"]) {
            background: linear-gradient(135deg, #D4A84B 0%, #C9952C 100%) !important;
            color: #0E1117 !important;
            -webkit-text-fill-color: #0E1117 !important;
            border: 2px solid #B8860B !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }
        
        </style>""", unsafe_allow_html=True)
    else:
        st.markdown("""<style>
        /* ═══════════════════════════════════════════════════════════════════════
           LTR MASTER STYLES - German/English Language Support
           Colors handled by config.toml
           ═══════════════════════════════════════════════════════════════════════ */
        
        /* === Direction only === */
        html, body, .stApp, .main, .block-container,
        [data-testid="stAppViewContainer"],
        [data-testid="stMainBlockContainer"] { 
            direction: ltr !important; 
            text-align: left !important;
        }
        
        /* Sidebar direction only */
        [data-testid="stSidebar"],
        [data-testid="stSidebarContent"],
        .stSidebar { 
            direction: ltr !important; 
            text-align: left !important; 
        }
        
        /* Hide white decorations */
        [data-testid="stDecoration"] {
            display: none !important;
        }
        
        /* Hide Material Icon ligature text (keyboard_double_arrow etc) */
        [data-testid="stSidebarCollapseButton"] span,
        [data-testid="collapsedControl"] span,
        button[kind="headerNoPadding"] span,
        span[class*="material-icons"] {
            font-size: 0 !important;
            overflow: hidden !important;
        }
        
        /* Horizontal blocks */
        .row-widget.stHorizontalBlock,
        [data-testid="stHorizontalBlock"] { 
            flex-direction: row !important; 
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] { 
            flex-direction: row !important; 
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           PREMIUM WIDGET STYLING - Same as RTL (German/English)
           ═══════════════════════════════════════════════════════════════════════ */
        
        /* PREMIUM TEXT - Smoky White */
        .stApp .main *:not([style*="color"]):not(a):not(svg):not(path) {
            color: #E0E0E0 !important;
            -webkit-text-fill-color: #E0E0E0 !important;
        }
        
        /* Headlines - Pure White */
        h1, h2, h3, .main-header {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }
        
        /* 1. Premium Input Fields with Glass Effect */
        .stTextInput input, 
        .stSelectbox div[data-baseweb="select"], 
        .stNumberInput input,
        .stTextArea textarea {
            color: #E0E0E0 !important;
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(212, 175, 55, 0.3) !important;
            backdrop-filter: blur(10px);
        }
        
        /* 2. Premium Dropdowns with Soft Black */
        div[data-baseweb="popover"], 
        div[data-baseweb="menu"], 
        ul[role="listbox"] {
            background-color: #161B22 !important;
            color: #E0E0E0 !important;
        }
        
        div[data-baseweb="select"] span,
        div[data-baseweb="select"] div {
            color: #E0E0E0 !important;
        }
        
        /* Labels - Metallic Gold */
        .stTextInput label, 
        .stSelectbox label, 
        .stNumberInput label,
        .stTextArea label,
        .stRadio label,
        .stCheckbox label {
            color: #D4AF37 !important;
            -webkit-text-fill-color: #D4AF37 !important;
            font-weight: bold !important;
        }
        
        /* Secondary buttons */
        button[kind="secondary"],
        [data-testid="stButton"] button:not([data-testid="baseButton-primary"]) {
            background-color: transparent !important;
            border: 2px solid #D4AF37 !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        
        /* Primary buttons */
        [data-testid="stButton"] button[data-testid="baseButton-primary"],
        button[kind="primary"] {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        
        /* Radio button options text - WHITE */
        .stRadio label,
        .stRadio label span,
        .stRadio label p,
        .stRadio label div,
        .stRadio > div > label,
        [data-testid="stRadio"] label span,
        [data-testid="stRadio"] label p,
        [data-baseweb="radio"] + div,
        div[role="radiogroup"] label,
        div[role="radiogroup"] span {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        
        /* Checkbox text - WHITE */
        .stCheckbox label span,
        [data-testid="stCheckbox"] label span {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        
        /* General text color - WHITE for dark theme */
        .stMarkdown,
        [data-testid="stMarkdownContainer"] {
            color: #FFFFFF !important;
        }
        
        /* Styled elements keep their colors */
        .stMarkdown div[style],
        .stMarkdown div[style] *,
        [data-testid="stMarkdownContainer"] div[style],
        [data-testid="stMarkdownContainer"] div[style] * {
            color: inherit !important;
            -webkit-text-fill-color: inherit !important;
        }
        
        /* Streamlit Alerts - dark text on light background */
        [data-testid="stAlert"] p,
        [data-testid="stAlert"] span,
        .stAlert p,
        .stAlert span {
            color: #0E1117 !important;
            -webkit-text-fill-color: #0E1117 !important;
        }
        
        /* File uploader dropzone */
        [data-testid="stFileUploaderDropzone"] span,
        [data-testid="stFileUploaderDropzone"] small,
        [data-testid="stFileUploaderDropzone"] p {
            color: #333333 !important;
            -webkit-text-fill-color: #333333 !important;
        }
        
        /* Browse files button - gold styling */
        [data-testid="stFileUploaderDropzone"] button,
        .stFileUploader button {
            background: linear-gradient(135deg, #D4A84B 0%, #C9952C 100%) !important;
            color: #0E1117 !important;
            -webkit-text-fill-color: #0E1117 !important;
            border: 2px solid #B8860B !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }
        
        </style>""", unsafe_allow_html=True)


def clear_language_on_logout():
    """مسح اللغة عند الخروج - لا نفعل شيء"""
    pass
