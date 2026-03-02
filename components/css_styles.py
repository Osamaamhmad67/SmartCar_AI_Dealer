"""
components/css_styles.py - أنماط CSS المخصصة
SmartCar AI-Dealer
"""

import streamlit as st
import os
import base64


def load_custom_css():
    """تحميل أنماط CSS مخصصة والعلامة المائية - نظام التصميم المحسّن"""
    # تحويل اللوغو إلى Base64 للعلامة المائية
    logo_path = r"C:\Users\Osama\Desktop\SmartCar_AI_Dealer\logs\logo.png"
    logo_base64 = ""
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()
            
    st.markdown("""
    <style>
        /* ═══════════════════════════════════════════════════════════════════════
           🎨 المرحلة الأولى: نظام التصميم الأساسي (Design System Foundation)
           ═══════════════════════════════════════════════════════════════════════ */
        
        /* استيراد الخطوط الاحترافية */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Cairo:wght@400;500;600;700&family=Orbitron:wght@400;700;900&display=swap');
        
        /* متغيرات CSS الشاملة */
        :root {
            /* الألوان الأساسية */
            --color-primary: #4299e1;
            --color-primary-light: #63b3ed;
            --color-primary-dark: #2b6cb0;
            
            /* ألوان التمييز (Accent) */
            --color-accent: #D4AF37;
            --color-accent-light: #fbd38d;
            --color-accent-dark: #c79e2c;
            --color-accent-glow: rgba(240, 180, 41, 0.4);
            
            /* ألوان الحالة */
            --color-success: #48bb78;
            --color-success-light: #68d391;
            --color-warning: #ed8936;
            --color-danger: #f56565;
            --color-danger-light: #F97583;
            
            /* ══════════════════════════════════════════════════════════════
               PREMIUM LUXURY DARK THEME - Professional Color Palette
               ══════════════════════════════════════════════════════════════ */
            
            /* Core Premium Colors */
            --color-soft-black: #0E1117;
            --color-dark-surface: #161B22;
            --color-dark-elevated: #21262D;
            
            /* Text Hierarchy */
            --color-text-primary: #FFFFFF;        /* Headlines only */
            --color-text-body: #E0E0E0;           /* Body text - Smoky White */
            --color-text-secondary: #B0B0B0;      /* Secondary text */
            --color-text-muted: #8B949E;          /* Muted/disabled */
            
            /* Metallic Gold Palette */
            --color-gold: #D4AF37;
            --color-gold-light: #F2D06B;
            --color-gold-dark: #B8942C;
            
            /* Premium Gradients */
            --gradient-primary: linear-gradient(135deg, #0E1117 0%, #161B22 100%);
            --gradient-dark: linear-gradient(145deg, #0E1117 0%, #161B22 100%);
            --gradient-gold: linear-gradient(45deg, #D4AF37, #F2D06B);
            --gradient-gold-shimmer: linear-gradient(90deg, transparent, rgba(212,175,55,0.4), transparent);
            --gradient-success: linear-gradient(135deg, #3FB950, #2EA043);
            --gradient-glass: linear-gradient(145deg, rgba(14, 17, 23, 0.95), rgba(22, 27, 34, 0.9));
            
            /* Glassmorphism */
            --glass-bg: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
            --glass-blur: blur(10px);
            
            /* Premium Shadows */
            --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.3);
            --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.4);
            --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
            --shadow-xl: 0 25px 50px rgba(0, 0, 0, 0.6);
            --shadow-glow-gold: 0 0 20px rgba(212, 175, 55, 0.3);
            --shadow-glow-gold-intense: 0 0 30px rgba(212, 175, 55, 0.5);
            --shadow-inset: inset 0 1px 0 rgba(255, 255, 255, 0.05);
            
            /* المسافات */
            --space-xs: 0.25rem;
            --space-sm: 0.5rem;
            --space-md: 1rem;
            --space-lg: 1.5rem;
            --space-xl: 2rem;
            --space-2xl: 3rem;
            
            /* نصف القطر للحواف */
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 20px;
            --radius-full: 9999px;
            
            /* الانتقالات */
            --transition-fast: 0.15s ease;
            --transition-normal: 0.3s ease;
            --transition-slow: 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            --transition-bounce: 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }
        
        /* الخطوط الأساسية - config.toml يتحكم بالألوان */
        html, body, .stApp {
            font-family: 'Inter', 'Cairo', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        }
        
        /* Hide decorations */
        [data-testid="stDecoration"] {
            display: none !important;
        }
        
        /* Selectbox - Global height fix to prevent text cutoff (especially Arabic) */
        [data-baseweb="select"],
        .stSelectbox [data-baseweb="select"],
        div[data-testid="stSelectbox"] [data-baseweb="select"] {
            min-height: 60px !important;
            height: auto !important;
        }
        
        [data-baseweb="select"] > div,
        .stSelectbox [data-baseweb="select"] > div,
        div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
            min-height: 56px !important;
            height: auto !important;
            padding-top: 16px !important;
            padding-bottom: 16px !important;
            line-height: 2 !important;
            display: flex !important;
            align-items: center !important;
        }
        
        [data-baseweb="select"] span,
        .stSelectbox span,
        div[data-testid="stSelectbox"] span {
            line-height: 2 !important;
            overflow: visible !important;
            display: block !important;
            padding-top: 5px !important;
            padding-bottom: 5px !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           🔥 NUCLEAR RADIO BUTTON FIX - Maximum specificity override
           ═══════════════════════════════════════════════════════════════════════ */
        .stRadio label,
        .stRadio label span,
        .stRadio label p,
        .stRadio label div,
        .stRadio div[role="radiogroup"] label,
        .stRadio div[role="radiogroup"] label *,
        .stRadio [data-baseweb="radio"] + div,
        .stRadio [data-baseweb="radio"] ~ div,
        [data-testid="stRadio"] label,
        [data-testid="stRadio"] label span,
        [data-testid="stRadio"] label p,
        [data-testid="stRadio"] div[role="radiogroup"] label,
        [data-testid="stRadio"] div[role="radiogroup"] label * {
            color: #E0E0E0 !important;
            -webkit-text-fill-color: #E0E0E0 !important;
            font-size: 0.95rem !important;
            font-weight: 500 !important;
        }
        
        /* Radio title label - Gold color */
        .stRadio > label:first-child,
        [data-testid="stRadio"] > label:first-child {
            color: #D4AF37 !important;
            -webkit-text-fill-color: #D4AF37 !important;
            font-weight: 600 !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           🖼️ PREMIUM BACKGROUND - Soft Black with subtle watermark
           ═══════════════════════════════════════════════════════════════════════ */
        
        .stApp {
            background-image: linear-gradient(rgba(14, 17, 23, 0.95), rgba(14, 17, 23, 0.95)), url("data:image/png;base64,[LOGO_B64]");
            background-repeat: no-repeat;
            background-position: center;
            background-size: 800px;
            background-attachment: fixed;
            color: #E0E0E0 !important;  /* Smoky white default text */
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           📦 PREMIUM COMPONENTS - Headers with Glassmorphism
           ═══════════════════════════════════════════════════════════════════════ */
        
        /* --- العناوين الرئيسية - Premium Header --- */
        .main-header {
            background: linear-gradient(145deg, #0E1117 0%, #161B22 100%);
            padding: 0.2rem;
            border-top-left-radius: var(--radius-md);
            border-top-right-radius: var(--radius-md);
            color: #FFFFFF;  /* Pure white for headlines */
            text-align: center;
            margin-bottom: 0px;
            position: relative;
            z-index: 10;
            border: 1px solid rgba(212, 175, 55, 0.2);
        }
        
        .main-header h1 {
            font-size: 1.8rem;
            margin: 0;
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        
        .sub-header {
            background: var(--gradient-dark);
            padding: var(--space-md) var(--space-xl);
            border-bottom-left-radius: var(--radius-md);
            border-bottom-right-radius: var(--radius-md);
            color: var(--color-text-primary);
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: var(--space-xl);
            min-height: 120px;
            position: relative;
            z-index: 10;
            backdrop-filter: blur(10px);
        }
        
        /* --- PREMIUM BUTTONS - Dark Charcoal with Metallic Gold --- */
        div.stButton > button {
            background: linear-gradient(145deg, #21262D 0%, #161B22 100%) !important;
            color: #E0E0E0 !important;
            font-weight: 600 !important;
            font-family: 'Cairo', 'Inter', sans-serif !important;
            border: 2px solid !important;
            border-image: linear-gradient(45deg, #D4AF37, #F2D06B) 1 !important;
            border-radius: var(--radius-md) !important;
            position: relative;
            z-index: 10;
            white-space: normal !important;
            word-wrap: break-word !important;
            text-overflow: clip !important;
            overflow: hidden !important;
            min-height: 50px !important;
            font-size: 0.9rem !important;
            padding: var(--space-md) var(--space-lg) !important;
            line-height: 1.3 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
        }
        
        /* Gold shimmer effect on buttons */
        div.stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(212,175,55,0.3), transparent);
            transition: left 0.6s ease;
        }
        
        /* Premium hover effect with golden glow */
        div.stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 0 25px rgba(212, 175, 55, 0.4), 0 8px 32px rgba(0, 0, 0, 0.5) !important;
            background: linear-gradient(145deg, #2D333B 0%, #21262D 100%) !important;
            color: #FFFFFF !important;
        }
        
        div.stButton > button:hover::before {
            left: 100%;
        }
        
        div.stButton > button:active {
            transform: translateY(-1px) !important;
        }
        
        /* Premium Submit Button - Full Gold Gradient */
        [data-testid="stFormSubmitButton"] button {
            background: linear-gradient(45deg, #D4AF37, #F2D06B) !important;
            color: #0E1117 !important;
            font-weight: 700 !important;
            border: 2px solid #B8942C !important;
            border-radius: var(--radius-md) !important;
            position: relative;
            z-index: 10;
            transition: all 0.3s ease !important;
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.3), 0 4px 12px rgba(0, 0, 0, 0.4) !important;
        }
        
        [data-testid="stFormSubmitButton"] button:hover {
            background: linear-gradient(45deg, #F2D06B, #D4AF37) !important;
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 0 35px rgba(212, 175, 55, 0.5), 0 8px 32px rgba(0, 0, 0, 0.5) !important;
        }
        
        /* --- تنسيق النماذج المحسّن --- */
        [data-testid="stForm"] {
            background: var(--gradient-glass) !important;
            border-radius: var(--radius-lg) !important;
            padding: var(--space-xl) !important;
            border: 2px solid rgba(240, 180, 41, 0.2) !important;
            position: relative;
            z-index: 10;
            backdrop-filter: blur(20px) !important;
            box-shadow: var(--shadow-lg), var(--shadow-inset) !important;
        }
        
        [data-testid="stForm"] label, 
        [data-testid="stForm"] p {
            color: var(--color-text-primary) !important;
            font-weight: 600 !important;
        }
        
        /* --- حقول الإدخال المحسّنة --- */
        .stTextInput > div > div > input,
        .stTextArea > div > textarea {
            background: rgba(26, 26, 46, 0.85) !important;
            border: 2px solid rgba(240, 180, 41, 0.25) !important;
            border-radius: var(--radius-md) !important;
            color: var(--color-text-primary) !important;
            padding: var(--space-md) !important;
            transition: all var(--transition-normal) !important;
            font-family: 'Inter', 'Cairo', sans-serif !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > textarea:focus {
            border-color: var(--color-accent) !important;
            box-shadow: 0 0 0 3px rgba(240, 180, 41, 0.15), var(--shadow-glow-gold) !important;
            outline: none !important;
        }
        
        .stTextInput > div > div > input::placeholder,
        .stTextArea > div > textarea::placeholder {
            color: var(--color-text-muted) !important;
        }
        
        /* --- Checkbox محسّن --- */
        [data-testid="stCheckbox"] label div div {
            margin-right: 7px !important;
            margin-left: 0px !important;
        }
        
        [data-testid="stCheckbox"] label span {
            color: var(--color-text-primary) !important;
        }
        
        /* --- بطاقات المعلومات 3D Premium --- */
        .info-card, .premium-card {
            background: var(--gradient-glass);
            padding: var(--space-lg);
            border-radius: var(--radius-lg);
            border: 2px solid rgba(240, 180, 41, 0.2);
            box-shadow: var(--shadow-lg), var(--shadow-inset);
            margin-bottom: var(--space-md);
            position: relative;
            z-index: 10;
            backdrop-filter: blur(20px);
            transition: all var(--transition-slow);
            transform-style: preserve-3d;
            perspective: 1000px;
        }
        
        /* تأثير اللمعان العلوي */
        .info-card::before, .premium-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 50%;
            background: linear-gradient(180deg, rgba(255,255,255,0.08), transparent);
            border-radius: var(--radius-lg) var(--radius-lg) 0 0;
            pointer-events: none;
        }
        
        /* صندوق النجاح */
        .success-box {
            background: var(--gradient-success);
            color: var(--color-text-primary);
            padding: var(--space-xl);
            border-radius: var(--radius-lg);
            text-align: center;
            font-size: 1.5rem;
            position: relative;
            z-index: 10;
            box-shadow: var(--shadow-lg);
            animation: successPulse 2s ease-in-out infinite;
        }
        
        @keyframes successPulse {
            0%, 100% { box-shadow: var(--shadow-lg); }
            50% { box-shadow: var(--shadow-lg), 0 0 20px rgba(72, 187, 120, 0.4); }
        }
        
        /* --- الجداول المحسّنة --- */
        .styled-table {
            border-collapse: collapse;
            width: 100%;
            position: relative;
            z-index: 10;
            background: var(--gradient-glass);
            border-radius: var(--radius-md);
            overflow: hidden;
        }
        
        .styled-table th {
            background: rgba(240, 180, 41, 0.2);
            color: var(--color-accent);
            font-weight: 600;
        }
        
        .styled-table th, .styled-table td {
            padding: var(--space-md);
            text-align: right;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .styled-table tr:hover {
            background: rgba(240, 180, 41, 0.1);
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           📂 تنسيق Expander المحسّن
           ═══════════════════════════════════════════════════════════════════════ */
        
        /* رأس الـ Expander */
        [data-testid="stExpander"] {
            background: var(--gradient-glass) !important;
            border: 2px solid rgba(240, 180, 41, 0.3) !important;
            border-radius: var(--radius-lg) !important;
            overflow: hidden;
            backdrop-filter: blur(15px) !important;
            box-shadow: var(--shadow-md) !important;
        }
        
        [data-testid="stExpander"] summary {
            background: rgba(26, 26, 46, 0.9) !important;
            color: var(--color-text-primary) !important;
            font-weight: 600 !important;
            padding: var(--space-md) var(--space-lg) !important;
            border-bottom: 1px solid rgba(240, 180, 41, 0.2) !important;
        }
        
        [data-testid="stExpander"] summary:hover {
            background: rgba(240, 180, 41, 0.15) !important;
        }
        
        /* محتوى الـ Expander */
        [data-testid="stExpander"] > div > div {
            background: rgba(26, 26, 46, 0.95) !important;
            padding: var(--space-lg) !important;
        }
        
        /* النصوص داخل الـ Expander */
        [data-testid="stExpander"] p,
        [data-testid="stExpander"] li,
        [data-testid="stExpander"] span,
        [data-testid="stExpander"] div {
            color: var(--color-text-primary) !important;
        }
        
        [data-testid="stExpander"] h1,
        [data-testid="stExpander"] h2,
        [data-testid="stExpander"] h3,
        [data-testid="stExpander"] h4,
        [data-testid="stExpander"] strong {
            color: var(--color-accent) !important;
            font-weight: 700 !important;
        }
        
        /* الروابط داخل الـ Expander */
        [data-testid="stExpander"] a {
            color: var(--color-accent-light) !important;
            text-decoration: underline !important;
        }
        
        [data-testid="stExpander"] a:hover {
            color: var(--color-accent) !important;
        }
        
        /* القوائ النقطية داخل الـ Expander */
        [data-testid="stExpander"] ul,
        [data-testid="stExpander"] ol {
            color: var(--color-text-primary) !important;
            padding-right: var(--space-lg) !important;
        }
        
        [data-testid="stExpander"] li {
            margin-bottom: var(--space-sm) !important;
            line-height: 1.7 !important;
        }
        
        [data-testid="stExpander"] li::marker {
            color: var(--color-accent) !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           🎛️ الشريط الجانبي المحسّن (Premium Sidebar)
           ═══════════════════════════════════════════════════════════════════════ */
        
        section[data-testid="stSidebar"] {
            background: var(--gradient-primary) !important;
        }
        
        section[data-testid="stSidebar"] > div {
            background: transparent !important;
        }
        
        /* أزرار التنقل في الشريط الجانبي */
        section[data-testid="stSidebar"] button {
            margin: var(--space-xs) 0 !important;
            transition: all var(--transition-normal) !important;
            border-radius: var(--radius-md) !important;
        }
        
        /* Sidebar Primary Buttons - Gold gradient with dark text */
        section[data-testid="stSidebar"] button[kind="primary"],
        section[data-testid="stSidebar"] .stButton > button {
            background: linear-gradient(45deg, #D4AF37, #F2D06B) !important;
            color: #0E1117 !important;
            -webkit-text-fill-color: #0E1117 !important;
            font-weight: 700 !important;
            border: 2px solid #B8942C !important;
            box-shadow: 0 0 15px rgba(212, 175, 55, 0.3) !important;
        }
        
        section[data-testid="stSidebar"] button[kind="primary"] p,
        section[data-testid="stSidebar"] button[kind="primary"] span,
        section[data-testid="stSidebar"] .stButton > button p,
        section[data-testid="stSidebar"] .stButton > button span {
            color: #0E1117 !important;
            -webkit-text-fill-color: #0E1117 !important;
        }
        
        /* Sidebar Secondary Buttons - Dark charcoal with gold border */
        section[data-testid="stSidebar"] button[kind="secondary"] {
            background: linear-gradient(145deg, #21262D, #161B22) !important;
            color: #E0E0E0 !important;
            -webkit-text-fill-color: #E0E0E0 !important;
            border: 2px solid #D4AF37 !important;
        }
        
        section[data-testid="stSidebar"] button[kind="secondary"] p,
        section[data-testid="stSidebar"] button[kind="secondary"] span {
            color: #E0E0E0 !important;
            -webkit-text-fill-color: #E0E0E0 !important;
        }
        
        section[data-testid="stSidebar"] button[kind="secondary"]:hover {
            background: linear-gradient(145deg, #2D333B, #21262D) !important;
            transform: translateX(-5px) !important;
            border-color: #F2D06B !important;
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.3) !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           📋 القوائم المنسدلة Premium (Selectbox/Dropdown)
           ═══════════════════════════════════════════════════════════════════════ */
        
        /* الحاوية الرئيسية للقائمة المنسدلة */
        div[data-baseweb="popover"],
        div[data-baseweb="menu"],
        div[data-baseweb="select"] div[role="listbox"],
        [data-baseweb="popover"] > div,
        [data-baseweb="select"] [data-baseweb="popover"] {
            background: linear-gradient(135deg, #0E1117 0%, #161B22 100%) !important;
            border: 2px solid var(--color-accent) !important;
            border-radius: var(--radius-md) !important;
            box-shadow: var(--shadow-lg), var(--shadow-glow-gold) !important;
        }
        
        /* خلفية القائمة الداخلية */
        div[data-baseweb="popover"] ul,
        div[data-baseweb="menu"] ul,
        [role="listbox"],
        [data-baseweb="menu"] {
            background: linear-gradient(135deg, #0E1117 0%, #161B22 100%) !important;
        }
        
        /* العناصر داخل القائمة */
        div[data-baseweb="popover"] ul li,
        div[data-baseweb="menu"] ul li,
        [data-baseweb="menu"] [role="option"],
        [data-baseweb="select"] [role="option"],
        [role="listbox"] [role="option"],
        [role="listbox"] li {
            font-size: 1rem !important;
            padding: var(--space-md) var(--space-lg) !important;
            color: #ffffff !important;
            background: transparent !important;
            font-weight: 500 !important;
            font-family: 'Inter', 'Cairo', sans-serif !important;
            transition: all var(--transition-fast) !important;
        }
        
        /* تأثير Hover */
        div[data-baseweb="popover"] ul li:hover,
        div[data-baseweb="menu"] ul li:hover,
        [data-baseweb="menu"] [role="option"]:hover,
        [data-baseweb="select"] [role="option"]:hover,
        [role="listbox"] [role="option"]:hover,
        [role="listbox"] li:hover {
            background: rgba(240, 180, 41, 0.25) !important;
            color: var(--color-accent) !important;
        }
        
        /* العنصر المحدد */
        div[data-baseweb="popover"] ul li[aria-selected="true"],
        div[data-baseweb="menu"] ul li[aria-selected="true"],
        [data-baseweb="menu"] [role="option"][aria-selected="true"],
        [data-baseweb="select"] [role="option"][aria-selected="true"],
        [role="listbox"] [role="option"][aria-selected="true"],
        [role="listbox"] li[aria-selected="true"] {
            background: rgba(240, 180, 41, 0.3) !important;
            color: var(--color-accent) !important;
            font-weight: 600 !important;
        }
        
        /* حقل الـ Select نفسه - الحاوية الخارجية */
        .stSelectbox > div > div,
        .stSelectbox > div > div > div,
        .stSelectbox [data-baseweb="select"] > div,
        .stSelectbox [data-baseweb="select"] > div > div,
        [data-baseweb="select"] [class*="control"],
        [data-baseweb="select"] [class*="Control"],
        [data-baseweb="select"] [class*="container"],
        [data-baseweb="select"] [class*="Container"] {
            background: rgba(26, 26, 46, 0.95) !important;
            background-color: rgba(26, 26, 46, 0.95) !important;
            border: 2px solid rgba(240, 180, 41, 0.3) !important;
            border-radius: var(--radius-md) !important;
        }
        
        .stSelectbox > div > div:hover,
        .stSelectbox [data-baseweb="select"] > div:hover {
            border-color: var(--color-accent) !important;
        }
        
        /* إجبار الخلفية الداكنة على كل العناصر الداخلية */
        .stSelectbox [data-baseweb="select"],
        .stSelectbox [data-baseweb="select"] * {
            background-color: transparent !important;
        }
        
        /* الحاوية الرئيسية للـ control */
        .stSelectbox [data-baseweb="select"] > div:first-child {
            background: rgba(26, 26, 46, 0.95) !important;
            background-color: rgba(26, 26, 46, 0.95) !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           🔧 إصلاح شامل لـ Selectbox - استهداف baseweb مباشرة
           ═══════════════════════════════════════════════════════════════════════ */
        
        /* الحاوية الداخلية للـ Select */
        [data-baseweb="select"] {
            color: #ffffff !important;
        }
        
        /* حقل الإدخال الفعلي */
        [data-baseweb="select"] input {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            caret-color: var(--color-accent) !important;
        }
        
        /* القيمة المعروضة - استهداف كل الاحتمالات */
        [data-baseweb="select"] [class*="css-"] {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        
        /* baseweb specific value containers */
        div[data-baseweb="select"] > div:first-child,
        div[data-baseweb="select"] > div:first-child > div,
        div[data-baseweb="select"] > div:first-child > div > div {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        
        /* Target the actual dropdown trigger button/input area */
        .stSelectbox [role="combobox"],
        .stSelectbox [aria-haspopup="listbox"] {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            overflow: visible !important;
            text-overflow: ellipsis !important;
            white-space: nowrap !important;
        }
        
        /* منع قطع النص في الـ Selectbox */
        .stSelectbox > div > div,
        .stSelectbox [data-baseweb="select"] > div {
            overflow: visible !important;
            min-height: 55px !important;
            line-height: 1.5 !important;
            padding-top: 8px !important;
            padding-bottom: 8px !important;
        }
        
        .stSelectbox [data-baseweb="select"] > div > div {
            overflow: visible !important;
            text-overflow: clip !important;
        }
        
        /* Target span elements that might contain the value */
        .stSelectbox span:not([class*="Icon"]):not([class*="icon"]),
        [data-baseweb="select"] span:not([class*="Icon"]):not([class*="icon"]) {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        
        /* Hide input background but show text */
        [data-baseweb="select"] input[aria-autocomplete] {
            background: transparent !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            opacity: 1 !important;
        }
        
        /* Placeholder */
        [data-baseweb="select"] [class*="placeholder"],
        .stSelectbox [class*="placeholder"] {
            color: rgba(255, 255, 255, 0.6) !important;
            -webkit-text-fill-color: rgba(255, 255, 255, 0.6) !important;
            opacity: 1 !important;
        }
        
        /* السهم */
        .stSelectbox svg,
        [data-baseweb="select"] svg {
            fill: var(--color-accent) !important;
        }
        
        /* Force all text elements inside to be white */
        .stSelectbox div[data-baseweb="select"] * {
            color: #ffffff !important;
        }
        
        /* Ensure the background stays transparent for inner elements */
        .stSelectbox [data-baseweb="select"] > div {
            background: transparent !important;
        }
        
        /* === إصلاح شامل لعرض النص في Selectbox === */
        /* النص المختار في الـ Selectbox */
        .stSelectbox [data-baseweb="select"] [class*="singleValue"],
        .stSelectbox [data-baseweb="select"] [class*="SingleValue"],
        .stSelectbox [data-baseweb="select"] [class*="value-container"] > div,
        .stSelectbox [data-baseweb="select"] > div > div > div:not([class*="indicator"]) {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            font-weight: 500 !important;
            font-size: 1rem !important;
        }
        
        /* إجبار ظهور النص */
        .stSelectbox [data-baseweb="select"] [aria-selected="true"],
        .stSelectbox [data-baseweb="select"] [data-id],
        .stSelectbox > div > div > div > div:first-child > div {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            visibility: visible !important;
            opacity: 1 !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           ⏰ تنسيق الساعة
           ═══════════════════════════════════════════════════════════════════════ */
        
        .clock {
            width: 150px;
            height: 150px;
            border: 4px solid var(--color-accent);
            border-radius: 50%;
            position: relative;
            background: #000;
            box-shadow: var(--shadow-glow-gold);
        }
        
        .clock-hands {
            width: 100%;
            height: 100%;
            position: absolute;
        }
        
        .hand {
            position: absolute;
            bottom: 50%;
            left: 50%;
            transform-origin: 50% 100%;
            border-radius: 5px;
            z-index: 5;
        }
        
        .hour-hand {
            width: 6px;
            height: 25%;
            background: var(--color-accent);
            margin-left: -3px;
            z-index: 6;
        }
        
        .min-hand {
            width: 4px;
            height: 35%;
            background: var(--color-text-primary);
            margin-left: -2px;
            z-index: 7;
        }
        
        .sec-hand {
            width: 2px;
            height: 45%;
            background: var(--color-danger);
            margin-left: -1px;
            z-index: 8;
        }
        
        .clock-center {
            width: 12px;
            height: 12px;
            background: var(--color-accent);
            border-radius: 50%;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 10;
            box-shadow: 0 0 10px var(--color-accent-glow);
        }
        
        .clock-date {
            font-size: 1.1rem;
            margin-top: 10px;
            color: var(--color-text-primary);
            text-align: center;
            font-weight: 600;
        }
        
        .clock-number {
            position: absolute;
            width: 100%;
            height: 100%;
            text-align: center;
            color: var(--color-accent);
            font-size: 1.1rem;
            font-weight: bold;
            padding-top: 3px;
            pointer-events: none;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           🎬 المرحلة الرابعة: التأثيرات الحركية (Micro-interactions)
           ═══════════════════════════════════════════════════════════════════════ */
        
        /* تأثير دخول الصفحة */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .stApp > div > div > div > section.main > div {
            animation: fadeInUp 0.4s ease-out;
        }
        
        /* تأثير Skeleton Loading */
        @keyframes skeletonLoading {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        
        .skeleton {
            background: linear-gradient(90deg, 
                rgba(255,255,255,0.1) 25%, 
                rgba(255,255,255,0.2) 50%, 
                rgba(255,255,255,0.1) 75%
            );
            background-size: 200% 100%;
            animation: skeletonLoading 1.5s infinite;
            border-radius: var(--radius-sm);
        }
        
        /* تأثير الطفو للأيقونات */
        @keyframes floatIcon {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }
        
        .float-icon {
            animation: floatIcon 3s ease-in-out infinite;
        }
        
        /* تأثير النبض */
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .pulse {
            animation: pulse 2s ease-in-out infinite;
        }
        
        /* Toast Notifications محسّنة */
        .stToast {
            background: var(--gradient-glass) !important;
            border: 2px solid var(--color-accent) !important;
            border-radius: var(--radius-md) !important;
            box-shadow: var(--shadow-lg), var(--shadow-glow-gold) !important;
            backdrop-filter: blur(20px) !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           🔐 المرحلة الثالثة: صفحة تسجيل الدخول (Login Page)
           ═══════════════════════════════════════════════════════════════════════ */
        
        /* تأثير Glow على نموذج تسجيل الدخول */
        [data-testid="stForm"] {
            animation: formGlow 3s ease-in-out infinite alternate;
        }
        
        @keyframes formGlow {
            0% { box-shadow: 0 0 20px rgba(240, 180, 41, 0.1); }
            100% { box-shadow: 0 0 40px rgba(240, 180, 41, 0.25); }
        }
        
        /* أيقونات داخل حقول الإدخال */
        .stTextInput label::before {
            margin-left: var(--space-sm);
            opacity: 0.8;
        }
        
        /* زر تسجيل الدخول الرئيسي */
        [data-testid="stFormSubmitButton"] button {
            background: linear-gradient(145deg, #D4AF37 0%, #c79e2c 50%, #D4AF37 100%) !important;
            background-size: 200% 200% !important;
            animation: gradientShift 3s ease infinite !important;
            color: var(--color-dark) !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            padding: var(--space-md) var(--space-xl) !important;
            text-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        [data-testid="stFormSubmitButton"] button:hover {
            transform: translateY(-3px) scale(1.02) !important;
            box-shadow: 0 10px 30px rgba(240, 180, 41, 0.4) !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           🏠 المرحلة الثالثة: الصفحة الرئيسية (Home Page)
           ═══════════════════════════════════════════════════════════════════════ */
        
        /* بطاقات الإحصائيات */
        .stats-card {
            background: var(--gradient-glass);
            border: 2px solid rgba(240, 180, 41, 0.2);
            border-radius: var(--radius-lg);
            padding: var(--space-xl);
            text-align: center;
            transition: all var(--transition-slow);
            position: relative;
            overflow: hidden;
        }
        
        .stats-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(240, 180, 41, 0.1) 0%, transparent 70%);
            opacity: 0;
            transition: opacity var(--transition-normal);
        }
        
        .stats-card:hover::before {
            opacity: 1;
        }
        
        .stats-card:hover {
            border-color: var(--color-accent);
            transform: translateY(-5px);
        }
        
        /* رقم الإحصائية الكبير */
        .stats-number {
            font-size: 3rem;
            font-weight: 700;
            color: var(--color-accent);
            font-family: 'Orbitron', 'Inter', sans-serif;
            text-shadow: 0 0 20px rgba(240, 180, 41, 0.3);
        }
        
        /* عنوان الإحصائية */
        .stats-label {
            color: var(--color-text-secondary);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: var(--space-sm);
        }
        
        /* أزرار Quick Actions */
        .quick-action-btn {
            background: var(--gradient-glass) !important;
            border: 2px solid rgba(240, 180, 41, 0.3) !important;
            border-radius: var(--radius-md) !important;
            padding: var(--space-lg) !important;
            display: flex;
            align-items: center;
            gap: var(--space-md);
            transition: all var(--transition-normal) !important;
        }
        
        .quick-action-btn:hover {
            background: rgba(240, 180, 41, 0.15) !important;
            border-color: var(--color-accent) !important;
            transform: translateX(-5px);
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           👑 المرحلة الثالثة: لوحة الإدارة (Admin Panel)
           ═══════════════════════════════════════════════════════════════════════ */
        
        /* جدول المستخدمين Premium */
        [data-testid="stDataFrame"],
        .stDataFrame {
            background: var(--gradient-glass) !important;
            border: 2px solid rgba(240, 180, 41, 0.2) !important;
            border-radius: var(--radius-lg) !important;
            overflow: hidden;
        }
        
        [data-testid="stDataFrame"] table,
        .stDataFrame table {
            background: transparent !important;
        }
        
        [data-testid="stDataFrame"] th,
        .stDataFrame th {
            background: rgba(240, 180, 41, 0.15) !important;
            color: var(--color-accent) !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            padding: var(--space-md) !important;
            border-bottom: 2px solid rgba(240, 180, 41, 0.3) !important;
        }
        
        [data-testid="stDataFrame"] td,
        .stDataFrame td {
            color: var(--color-text-primary) !important;
            padding: var(--space-md) !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        
        [data-testid="stDataFrame"] tr:hover,
        .stDataFrame tr:hover {
            background: rgba(240, 180, 41, 0.08) !important;
        }
        
        /* مؤشرات الحالة */
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: var(--radius-full);
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .status-active {
            background: rgba(72, 187, 120, 0.2);
            color: var(--color-success);
            border: 1px solid var(--color-success);
        }
        
        .status-inactive {
            background: rgba(245, 101, 101, 0.2);
            color: var(--color-danger);
            border: 1px solid var(--color-danger);
        }
        
        .status-pending {
            background: rgba(237, 137, 54, 0.2);
            color: var(--color-warning);
            border: 1px solid var(--color-warning);
        }
        
        /* Tabs في لوحة الإدارة */
        .stTabs [data-baseweb="tab-list"] {
            background: var(--gradient-glass) !important;
            border-radius: var(--radius-lg) var(--radius-lg) 0 0 !important;
            padding: var(--space-sm) !important;
            gap: var(--space-sm) !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent !important;
            color: var(--color-text-secondary) !important;
            border-radius: var(--radius-md) !important;
            padding: var(--space-md) var(--space-lg) !important;
            font-weight: 500 !important;
            transition: all var(--transition-normal) !important;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(240, 180, 41, 0.1) !important;
            color: var(--color-accent) !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: rgba(240, 180, 41, 0.2) !important;
            color: var(--color-accent) !important;
            font-weight: 700 !important;
        }
        
        .stTabs [data-baseweb="tab-panel"] {
            background: var(--gradient-glass) !important;
            border: 2px solid rgba(240, 180, 41, 0.2) !important;
            border-top: none !important;
            border-radius: 0 0 var(--radius-lg) var(--radius-lg) !important;
            padding: var(--space-xl) !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           👤 المرحلة الثالثة: صفحة الملف الشخصي (Profile Page)
           ═══════════════════════════════════════════════════════════════════════ */
        
        /* بطاقة المستخدم */
        .profile-card {
            background: var(--gradient-glass);
            border: 2px solid rgba(240, 180, 41, 0.2);
            border-radius: var(--radius-xl);
            padding: var(--space-xl);
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .profile-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 120px;
            background: var(--gradient-gold);
            opacity: 0.1;
        }
        
        /* صورة Avatar */
        .avatar-container {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            border: 4px solid var(--color-accent);
            margin: 0 auto var(--space-lg);
            overflow: hidden;
            box-shadow: 0 0 30px rgba(240, 180, 41, 0.3);
            position: relative;
            z-index: 1;
        }
        
        .avatar-container img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        /* اسم المستخدم */
        .profile-name {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--color-text-primary);
            margin-bottom: var(--space-xs);
        }
        
        .profile-role {
            color: var(--color-accent);
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* إحصائيات الملف الشخصي */
        .profile-stats {
            display: flex;
            justify-content: center;
            gap: var(--space-xl);
            margin-top: var(--space-xl);
            padding-top: var(--space-lg);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .profile-stat-item {
            text-align: center;
        }
        
        .profile-stat-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--color-accent);
        }
        
        .profile-stat-label {
            font-size: 0.75rem;
            color: var(--color-text-secondary);
            text-transform: uppercase;
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           📱 Media Queries للموبايل (أداء محسّن)
           ═══════════════════════════════════════════════════════════════════════ */
        
        /* تأثيرات 3D فقط للأجهزة التي تدعم الماوس */
        @media (hover: hover) and (pointer: fine) {
            .info-card:hover, .premium-card:hover {
                transform: translateY(-8px) rotateX(3deg) rotateY(-2deg);
                box-shadow: var(--shadow-xl), var(--shadow-glow-gold);
                border-color: var(--color-accent);
            }
            
            div.stButton > button:hover {
                transform: translateY(-3px);
            }
        }
        
        /* تعطيل التأثيرات الثقيلة على الموبايل */
        @media (max-width: 768px) {
            .info-card, .premium-card {
                backdrop-filter: blur(10px);
            }
            
            .info-card:hover, .premium-card:hover {
                transform: translateY(-4px);
            }
            
            div.stButton > button:hover {
                transform: translateY(-2px);
            }
            
            .stApp {
                background-size: 400px;
            }
        }
        
        /* شاشات صغيرة جداً */
        @media (max-width: 480px) {
            :root {
                --space-md: 0.75rem;
                --space-lg: 1rem;
                --space-xl: 1.5rem;
            }
            
            div.stButton > button {
                font-size: 0.8rem !important;
                min-height: 45px !important;
            }
        }
        
        /* ═══════════════════════════════════════════════════════════════════════
           🔧 إعدادات عامة
           ═══════════════════════════════════════════════════════════════════════ */
        
        /* إخفاء عناصر Streamlit الافتراضية */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* تأخير Accessibility - تباين عالي */
        @media (prefers-contrast: high) {
            :root {
                --color-accent: #ffcc00;
                --color-text-primary: #ffffff;
            }
            
            [data-testid="stForm"] {
                background: rgba(0, 0, 0, 0.9) !important;
            }
        }
        
        /* دعم الوضع الداكن للنظام */
        @media (prefers-color-scheme: dark) {
            .stApp {
                background-image: linear-gradient(rgba(20, 20, 30, 0.92), rgba(20, 20, 30, 0.92)), url("data:image/png;base64,[LOGO_B64]");
            }
        }
        
    </style>
    """.replace("[LOGO_B64]", logo_base64), unsafe_allow_html=True)
