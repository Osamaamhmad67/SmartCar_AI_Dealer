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
from PIL import Image
from io import BytesIO
from utils.invoice_generator import InvoiceGenerator
from utils.payment_processor import PaymentProcessor
from utils.ocr_scanner import DocumentScanner
from utils.i18n import t, init_language, set_language, get_current_lang, apply_language_css, SUPPORTED_LANGUAGES, get_language_display_name, is_rtl, clear_translations_cache, rtl_tabs

def get_clock_html():
    """Returns the proprietary HTML/CSS/JS for the ultra-premium 3D crystalline analog clock component"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body { 
                background: transparent; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
                height: 100vh; 
                overflow: hidden;
                perspective: 1200px;
            }
            
            .clock-wrapper {
                position: relative;
                transform-style: preserve-3d;
                animation: float 8s ease-in-out infinite;
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0) rotateX(8deg) rotateY(-3deg); }
                25% { transform: translateY(-6px) rotateX(5deg) rotateY(3deg); }
                50% { transform: translateY(-10px) rotateX(-5deg) rotateY(-3deg); }
                75% { transform: translateY(-4px) rotateX(3deg) rotateY(5deg); }
            }
            
            /* Outer rotating ring */
            .outer-ring {
                position: absolute;
                width: 200px;
                height: 200px;
                border-radius: 50%;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                border: 2px dashed rgba(241, 196, 15, 0.3);
                animation: rotateRing 60s linear infinite;
            }
            
            @keyframes rotateRing {
                from { transform: translate(-50%, -50%) rotate(0deg); }
                to { transform: translate(-50%, -50%) rotate(360deg); }
            }
            
            /* Pulsing glow effect */
            .glow-pulse {
                position: absolute;
                width: 180px;
                height: 180px;
                border-radius: 50%;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: radial-gradient(circle, rgba(241, 196, 15, 0.15) 0%, transparent 70%);
                animation: pulse 3s ease-in-out infinite;
                pointer-events: none;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 0.5; transform: translate(-50%, -50%) scale(1); }
                50% { opacity: 1; transform: translate(-50%, -50%) scale(1.1); }
            }
            
            .clock {
                width: 170px;
                height: 170px;
                border-radius: 50%;
                position: relative;
                background: 
                    radial-gradient(ellipse at 30% 20%, rgba(255, 255, 255, 0.15) 0%, transparent 50%),
                    radial-gradient(ellipse at 70% 80%, rgba(0, 0, 0, 0.3) 0%, transparent 50%),
                    linear-gradient(145deg, 
                        rgba(30, 30, 50, 0.95) 0%,
                        rgba(15, 15, 30, 0.98) 50%,
                        rgba(5, 5, 15, 1) 100%);
                backdrop-filter: blur(15px);
                -webkit-backdrop-filter: blur(15px);
                border: 3px solid transparent;
                background-clip: padding-box;
                box-shadow: 
                    0 0 80px rgba(241, 196, 15, 0.25),
                    0 0 40px rgba(241, 196, 15, 0.15),
                    inset 0 0 50px rgba(241, 196, 15, 0.08),
                    0 25px 50px rgba(0, 0, 0, 0.5),
                    inset 0 -8px 25px rgba(0, 0, 0, 0.4),
                    inset 0 8px 25px rgba(255, 255, 255, 0.05);
                transform-style: preserve-3d;
            }
            
            /* Golden border with gradient */
            .clock::before {
                content: '';
                position: absolute;
                top: -3px; left: -3px; right: -3px; bottom: -3px;
                border-radius: 50%;
                background: linear-gradient(135deg, 
                    #f1c40f 0%, 
                    #d4a00a 25%, 
                    #8b6914 50%,
                    #d4a00a 75%,
                    #f1c40f 100%);
                z-index: -1;
                animation: borderShine 4s linear infinite;
            }
            
            @keyframes borderShine {
                0% { filter: hue-rotate(0deg) brightness(1); }
                50% { filter: hue-rotate(10deg) brightness(1.2); }
                100% { filter: hue-rotate(0deg) brightness(1); }
            }
            
            /* Glass reflection */
            .clock::after {
                content: '';
                position: absolute;
                top: 8%;
                left: 12%;
                width: 76%;
                height: 35%;
                background: linear-gradient(180deg, 
                    rgba(255, 255, 255, 0.25) 0%,
                    rgba(255, 255, 255, 0.08) 40%,
                    transparent 100%);
                border-radius: 50% 50% 45% 45% / 100% 100% 40% 40%;
                pointer-events: none;
            }
            
            /* Inner decorative ring */
            .inner-ring {
                position: absolute;
                top: 12px; left: 12px; right: 12px; bottom: 12px;
                border-radius: 50%;
                border: 1px solid rgba(241, 196, 15, 0.25);
                box-shadow: 
                    inset 0 0 20px rgba(241, 196, 15, 0.08),
                    0 0 10px rgba(241, 196, 15, 0.05);
            }
            
            .hand {
                position: absolute;
                bottom: 50%;
                left: 50%;
                transform-origin: 50% 100%;
                z-index: 5;
            }
            
            .hour-hand { 
                width: 7px; 
                height: 26%; 
                background: linear-gradient(180deg, #f1c40f 0%, #c49b00 60%, #8b6914 100%);
                margin-left: -3.5px; 
                z-index: 6;
                border-radius: 4px 4px 2px 2px;
                box-shadow: 
                    0 0 12px rgba(241, 196, 15, 0.6),
                    0 3px 6px rgba(0, 0, 0, 0.4);
            }
            
            .hour-hand::after {
                content: '';
                position: absolute;
                top: 0; left: 1px;
                width: 2px; height: 60%;
                background: linear-gradient(180deg, rgba(255,255,255,0.5), transparent);
                border-radius: 2px;
            }
            
            .min-hand { 
                width: 5px; 
                height: 36%; 
                background: linear-gradient(180deg, #ffffff 0%, #e0e0e0 50%, #b0b0b0 100%);
                margin-left: -2.5px; 
                z-index: 7;
                border-radius: 3px 3px 1.5px 1.5px;
                box-shadow: 
                    0 0 10px rgba(255, 255, 255, 0.4),
                    0 3px 6px rgba(0, 0, 0, 0.3);
            }
            
            .min-hand::after {
                content: '';
                position: absolute;
                top: 0; left: 1px;
                width: 1.5px; height: 50%;
                background: linear-gradient(180deg, rgba(255,255,255,0.6), transparent);
                border-radius: 1px;
            }
            
            .sec-hand { 
                width: 2px; 
                height: 42%; 
                background: linear-gradient(180deg, #ff6b6b 0%, #ee5a24 50%, #c0392b 100%);
                margin-left: -1px; 
                z-index: 8;
                border-radius: 1px;
                box-shadow: 0 0 15px rgba(238, 90, 36, 0.7);
            }
            
            /* Second hand tail */
            .sec-tail {
                position: absolute;
                bottom: 50%;
                left: 50%;
                width: 2px;
                height: 12%;
                background: linear-gradient(0deg, #c0392b, #ee5a24);
                margin-left: -1px;
                margin-bottom: -12%;
                transform-origin: 50% 0%;
                z-index: 8;
                border-radius: 1px;
            }
            
            .clock-center {
                width: 18px; 
                height: 18px;
                background: radial-gradient(circle at 35% 35%, #ffdd57 0%, #f1c40f 40%, #c49b00 70%, #8b6914 100%);
                border-radius: 50%;
                position: absolute;
                top: 50%; 
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 10;
                box-shadow: 
                    0 0 20px rgba(241, 196, 15, 0.7),
                    0 0 40px rgba(241, 196, 15, 0.3),
                    inset 0 -3px 6px rgba(0, 0, 0, 0.4),
                    inset 0 3px 6px rgba(255, 255, 255, 0.4);
            }
            
            .clock-center::before {
                content: '';
                position: absolute;
                top: 3px; left: 4px;
                width: 5px; height: 5px;
                background: rgba(255, 255, 255, 0.8);
                border-radius: 50%;
                filter: blur(1px);
            }
            
            .clock-center::after {
                content: '';
                position: absolute;
                top: 50%; left: 50%;
                transform: translate(-50%, -50%);
                width: 6px; height: 6px;
                background: radial-gradient(circle, #0E1117, #0a0a15);
                border-radius: 50%;
                box-shadow: inset 0 1px 2px rgba(255,255,255,0.2);
            }
            
            .clock-date {
                font-family: 'Orbitron', 'Segoe UI', sans-serif;
                font-size: 9px;
                font-weight: 700;
                color: rgba(241, 196, 15, 0.95);
                text-align: center;
                position: absolute;
                width: 100%;
                bottom: 32px;
                z-index: 4;
                text-shadow: 
                    0 0 15px rgba(241, 196, 15, 0.6),
                    0 0 30px rgba(241, 196, 15, 0.3);
                letter-spacing: 2px;
                text-transform: uppercase;
            }
            
            .clock-number {
                position: absolute;
                width: 100%; 
                height: 100%;
                text-align: center;
                font-family: 'Orbitron', 'Segoe UI', sans-serif;
                font-size: 12px;
                font-weight: 900;
            }
            
            .clock-number span {
                display: inline-block;
                color: rgba(241, 196, 15, 0.95);
                text-shadow: 
                    0 0 15px rgba(241, 196, 15, 0.6),
                    0 0 8px rgba(241, 196, 15, 0.4),
                    0 2px 4px rgba(0, 0, 0, 0.5);
            }
            
            /* Diamond hour markers */
            .hour-marker {
                position: absolute;
                width: 4px;
                height: 12px;
                background: linear-gradient(180deg, 
                    rgba(241, 196, 15, 1) 0%, 
                    rgba(200, 160, 10, 0.8) 50%,
                    rgba(241, 196, 15, 0.5) 100%);
                left: 50%;
                margin-left: -2px;
                top: 8px;
                transform-origin: 50% 77px;
                border-radius: 2px;
                box-shadow: 0 0 8px rgba(241, 196, 15, 0.5);
            }
            
            .minute-marker {
                position: absolute;
                width: 2px;
                height: 6px;
                background: rgba(241, 196, 15, 0.4);
                left: 50%;
                margin-left: -1px;
                top: 10px;
                transform-origin: 50% 75px;
                border-radius: 1px;
            }
            
            /* Luxury brand text */
            .brand-text {
                position: absolute;
                width: 100%;
                top: 38%;
                text-align: center;
                font-family: 'Orbitron', sans-serif;
                font-size: 7px;
                font-weight: 400;
                color: rgba(241, 196, 15, 0.5);
                letter-spacing: 3px;
                text-transform: uppercase;
            }
        </style>
    </head>
    <body>
        <div class="clock-wrapper">
            <div class="outer-ring"></div>
            <div class="glow-pulse"></div>
            <div class="clock">
                <div class="inner-ring"></div>
                
                <!-- Hour markers (at 12, 3, 6, 9) -->
                <div class="hour-marker" style="transform: rotate(0deg);"></div>
                <div class="hour-marker" style="transform: rotate(90deg);"></div>
                <div class="hour-marker" style="transform: rotate(180deg);"></div>
                <div class="hour-marker" style="transform: rotate(270deg);"></div>
                
                <!-- Minute markers -->
                <div class="minute-marker" style="transform: rotate(30deg);"></div>
                <div class="minute-marker" style="transform: rotate(60deg);"></div>
                <div class="minute-marker" style="transform: rotate(120deg);"></div>
                <div class="minute-marker" style="transform: rotate(150deg);"></div>
                <div class="minute-marker" style="transform: rotate(210deg);"></div>
                <div class="minute-marker" style="transform: rotate(240deg);"></div>
                <div class="minute-marker" style="transform: rotate(300deg);"></div>
                <div class="minute-marker" style="transform: rotate(330deg);"></div>
                
                <!-- Numbers -->
                <div class="clock-number" style="transform: rotate(0deg);"><span style="transform: rotate(0deg);">12</span></div>
                <div class="clock-number" style="transform: rotate(30deg);"><span style="transform: rotate(-30deg);">1</span></div>
                <div class="clock-number" style="transform: rotate(60deg);"><span style="transform: rotate(-60deg);">2</span></div>
                <div class="clock-number" style="transform: rotate(90deg);"><span style="transform: rotate(-90deg);">3</span></div>
                <div class="clock-number" style="transform: rotate(120deg);"><span style="transform: rotate(-120deg);">4</span></div>
                <div class="clock-number" style="transform: rotate(150deg);"><span style="transform: rotate(-150deg);">5</span></div>
                <div class="clock-number" style="transform: rotate(180deg);"><span style="transform: rotate(-180deg);">6</span></div>
                <div class="clock-number" style="transform: rotate(210deg);"><span style="transform: rotate(-210deg);">7</span></div>
                <div class="clock-number" style="transform: rotate(240deg);"><span style="transform: rotate(-240deg);">8</span></div>
                <div class="clock-number" style="transform: rotate(270deg);"><span style="transform: rotate(-270deg);">9</span></div>
                <div class="clock-number" style="transform: rotate(300deg);"><span style="transform: rotate(-300deg);">10</span></div>
                <div class="clock-number" style="transform: rotate(330deg);"><span style="transform: rotate(-330deg);">11</span></div>
                
                <div class="brand-text">SMARTCAR</div>
                
                <div class="hand hour-hand" id="hour"></div>
                <div class="hand min-hand" id="min"></div>
                <div class="hand sec-hand" id="sec"></div>
                <div class="sec-tail" id="sec-tail"></div>
                <div class="clock-center"></div>
                <div class="clock-date" id="date"></div>
            </div>
        </div>
        <script>
            function updateClock() {
                const now = new Date();
                const s = now.getSeconds();
                const ms = now.getMilliseconds();
                const m = now.getMinutes();
                const h = now.getHours();
                
                // Smooth second hand movement
                const sD = ((s + ms/1000) / 60) * 360;
                const mD = (m / 60) * 360 + (s / 60) * 6;
                const hD = (h % 12 / 12) * 360 + (m / 60) * 30;
                
                document.getElementById('sec').style.transform = "rotate(" + sD + "deg)";
                document.getElementById('sec-tail').style.transform = "rotate(" + sD + "deg)";
                document.getElementById('min').style.transform = "rotate(" + mD + "deg)";
                document.getElementById('hour').style.transform = "rotate(" + hD + "deg)";
                
                const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
                const day = now.getDate().toString().padStart(2, '0');
                document.getElementById('date').innerText = day + ' ' + months[now.getMonth()];
                
                requestAnimationFrame(updateClock);
            }
            updateClock();
        </script>
    </body>
    </html>
    """


def render_universal_header(page_title: str, subtitle: str = ""):
    """
    Renders the universal header with clock and logo for all pages.
    
    Args:
        page_title: The title to display on the left side of the header
        subtitle: Optional subtitle to display below the title
    """
    # Load logo
    header_logo_path = r"C:\Users\Osama\Desktop\SmartCar_AI_Dealer\logs\osamaslogo.png"
    header_logo_img = ""
    if os.path.exists(header_logo_path):
        with open(header_logo_path, "rb") as image_file:
            header_logo_img = base64.b64encode(image_file.read()).decode()
    
    # Determine language direction
    lang_code = st.session_state.get('language', 'de')
    direction = 'rtl' if lang_code == 'ar' else 'ltr'
    text_align = 'right' if direction == 'rtl' else 'left'
    text_align_opposite = 'left' if direction == 'rtl' else 'right'
    flex_direction = 'row-reverse' if direction == 'rtl' else 'row'
    
    # Build subtitle HTML if provided
    subtitle_html = f'<p>{subtitle}</p>' if subtitle else ''
    
    # Premium Header with Clock embedded inside
    combined_header_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                background: transparent; 
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            
            .universal-header {{
                background: linear-gradient(145deg, #0a0a15 0%, #0E1117 50%, #0f0f1a 100%);
                border-radius: 20px;
                padding: 25px 40px;
                border: 2px solid rgba(241, 196, 15, 0.3);
                box-shadow: 
                    0 10px 40px rgba(0, 0, 0, 0.5),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
                display: flex;
                flex-direction: {flex_direction};
                align-items: center;
                justify-content: space-between;
                gap: 30px;
                min-height: 260px;
                direction: {direction};
            }}
            
            .header-left {{
                flex: 1;
                text-align: {text_align};
            }}
            .header-left h2 {{
                color: #f1c40f;
                font-size: 1.5rem;
                margin: 0 0 10px 0;
                font-weight: 700;
                text-shadow: 0 0 20px rgba(241, 196, 15, 0.4);
            }}
            .header-left p {{
                color: rgba(255, 255, 255, 0.85);
                font-size: 1rem;
                margin: 0;
            }}
            
            .header-center {{
                flex: 1.5;
                display: flex;
                justify-content: center;
                align-items: center;
                position: relative;
            }}
            
            .header-right {{
                flex: 1;
                text-align: {text_align_opposite};
            }}
            .header-right img {{
                height: 238px;
                filter: drop-shadow(0 0 15px rgba(241, 196, 15, 0.3));
                transition: transform 0.3s ease;
            }}
            .header-right img:hover {{
                transform: scale(1.05);
            }}
            
            /* Clock Styles */
            .clock-wrapper {{
                position: relative;
                transform-style: preserve-3d;
                animation: float 8s ease-in-out infinite;
            }}
            
            @keyframes float {{
                0%, 100% {{ transform: translateY(0) rotateX(8deg) rotateY(-3deg); }}
                25% {{ transform: translateY(-4px) rotateX(5deg) rotateY(3deg); }}
                50% {{ transform: translateY(-8px) rotateX(-5deg) rotateY(-3deg); }}
                75% {{ transform: translateY(-3px) rotateX(3deg) rotateY(5deg); }}
            }}
            
            .outer-ring {{
                position: absolute;
                width: 200px;
                height: 200px;
                border-radius: 50%;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                border: 2px dashed rgba(241, 196, 15, 0.3);
                animation: rotateRing 60s linear infinite;
            }}
            
            @keyframes rotateRing {{
                from {{ transform: translate(-50%, -50%) rotate(0deg); }}
                to {{ transform: translate(-50%, -50%) rotate(360deg); }}
            }}
            
            .glow-pulse {{
                position: absolute;
                width: 190px;
                height: 190px;
                border-radius: 50%;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: radial-gradient(circle, rgba(241, 196, 15, 0.15) 0%, transparent 70%);
                animation: pulse 3s ease-in-out infinite;
                pointer-events: none;
            }}
            
            @keyframes pulse {{
                0%, 100% {{ opacity: 0.5; transform: translate(-50%, -50%) scale(1); }}
                50% {{ opacity: 1; transform: translate(-50%, -50%) scale(1.1); }}
            }}
            
            .clock {{
                width: 163px;
                height: 163px;
                border-radius: 50%;
                position: relative;
                background: 
                    radial-gradient(ellipse at 30% 20%, rgba(255, 255, 255, 0.15) 0%, transparent 50%),
                    radial-gradient(ellipse at 70% 80%, rgba(0, 0, 0, 0.3) 0%, transparent 50%),
                    linear-gradient(145deg, rgba(30, 30, 50, 0.95) 0%, rgba(15, 15, 30, 0.98) 50%, rgba(5, 5, 15, 1) 100%);
                backdrop-filter: blur(15px);
                border: 3px solid transparent;
                background-clip: padding-box;
                box-shadow: 
                    0 0 60px rgba(241, 196, 15, 0.25),
                    0 0 30px rgba(241, 196, 15, 0.15),
                    inset 0 0 40px rgba(241, 196, 15, 0.08),
                    0 20px 40px rgba(0, 0, 0, 0.5);
                transform-style: preserve-3d;
            }}
            
            .clock::before {{
                content: '';
                position: absolute;
                top: -3px; left: -3px; right: -3px; bottom: -3px;
                border-radius: 50%;
                background: linear-gradient(135deg, #f1c40f 0%, #d4a00a 25%, #8b6914 50%, #d4a00a 75%, #f1c40f 100%);
                z-index: -1;
                animation: borderShine 4s linear infinite;
            }}
            
            @keyframes borderShine {{
                0% {{ filter: hue-rotate(0deg) brightness(1); }}
                50% {{ filter: hue-rotate(10deg) brightness(1.2); }}
                100% {{ filter: hue-rotate(0deg) brightness(1); }}
            }}
            
            .clock::after {{
                content: '';
                position: absolute;
                top: 8%; left: 12%;
                width: 76%; height: 35%;
                background: linear-gradient(180deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.08) 40%, transparent 100%);
                border-radius: 50% 50% 45% 45% / 100% 100% 40% 40%;
                pointer-events: none;
            }}
            
            .inner-ring {{
                position: absolute;
                top: 10px; left: 10px; right: 10px; bottom: 10px;
                border-radius: 50%;
                border: 1px solid rgba(241, 196, 15, 0.25);
                box-shadow: inset 0 0 15px rgba(241, 196, 15, 0.08);
            }}
            
            .hand {{
                position: absolute;
                bottom: 50%;
                left: 50%;
                transform-origin: 50% 100%;
                z-index: 5;
            }}
            
            .hour-hand {{ 
                width: 8px; height: 26%; 
                background: linear-gradient(180deg, #2c2c2c 0%, #1a1a1a 40%, #0a0a0a 70%, #000000 100%);
                margin-left: -4px; z-index: 6;
                border-radius: 4px 4px 2px 2px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.8), 0 2px 4px rgba(0, 0, 0, 0.5);
            }}
            
            .min-hand {{ 
                width: 6px; height: 35%; 
                background: linear-gradient(180deg, #ffffff 0%, #f0f0f0 30%, #e0e0e0 60%, #c0c0c0 100%);
                margin-left: -3px; z-index: 7;
                border-radius: 3px 3px 1.5px 1.5px;
                box-shadow: 0 0 12px rgba(255, 255, 255, 0.6), 0 0 20px rgba(255, 255, 255, 0.3);
            }}
            
            .sec-hand {{ 
                width: 3px; height: 42%; 
                background: linear-gradient(180deg, #ff6b6b 0%, #ff5252 30%, #ee5a24 60%, #c0392b 100%);
                margin-left: -1.5px; z-index: 8;
                border-radius: 2px;
                box-shadow: 0 0 18px rgba(238, 90, 36, 0.9), 0 0 30px rgba(255, 82, 82, 0.5);
            }}
            
            .clock-center {{
                width: 18px; height: 18px;
                background: radial-gradient(circle at 35% 35%, #ffdd57 0%, #f1c40f 40%, #c49b00 70%, #8b6914 100%);
                border-radius: 50%;
                position: absolute;
                top: 50%; left: 50%;
                transform: translate(-50%, -50%);
                z-index: 10;
                box-shadow: 0 0 20px rgba(241, 196, 15, 0.9), 0 0 35px rgba(241, 196, 15, 0.5);
            }}
            
            .clock-number {{
                position: absolute;
                width: 100%; height: 100%;
                text-align: center;
                font-family: 'Orbitron', sans-serif;
                font-size: 13px;
                font-weight: 900;
            }}
            
            .clock-number span {{
                display: inline-block;
                color: #000000;
                text-shadow: 0 0 8px rgba(0, 0, 0, 0.3);
            }}
            
            .hour-marker {{
                position: absolute;
                width: 4px; height: 12px;
                background: linear-gradient(180deg, rgba(241, 196, 15, 1) 0%, rgba(200, 160, 10, 0.5) 100%);
                left: 50%; margin-left: -2px; top: 8px;
                transform-origin: 50% 73px;
                border-radius: 2px;
                box-shadow: 0 0 8px rgba(241, 196, 15, 0.6);
            }}
            
            .clock-date {{
                font-family: 'Orbitron', sans-serif;
                font-size: 10px;
                font-weight: 700;
                color: #00d4ff;
                text-align: center;
                position: absolute;
                width: 100%;
                bottom: 30px;
                z-index: 4;
                text-shadow: 0 0 12px rgba(0, 212, 255, 0.7);
                letter-spacing: 1px;
            }}
        </style>
    </head>
    <body>
        <div class="universal-header">
            <div class="header-left">
                <h2>{page_title}</h2>
                {subtitle_html}
            </div>
            <div class="header-center">
                <div class="clock-wrapper">
                    <div class="outer-ring"></div>
                    <div class="glow-pulse"></div>
                    <div class="clock">
                        <div class="inner-ring"></div>
                        <div class="hour-marker" style="transform: rotate(0deg);"></div>
                        <div class="hour-marker" style="transform: rotate(90deg);"></div>
                        <div class="hour-marker" style="transform: rotate(180deg);"></div>
                        <div class="hour-marker" style="transform: rotate(270deg);"></div>
                        <div class="clock-number" style="transform: rotate(0deg);"><span style="transform: rotate(0deg);">12</span></div>
                        <div class="clock-number" style="transform: rotate(30deg);"><span style="transform: rotate(-30deg);">1</span></div>
                        <div class="clock-number" style="transform: rotate(60deg);"><span style="transform: rotate(-60deg);">2</span></div>
                        <div class="clock-number" style="transform: rotate(90deg);"><span style="transform: rotate(-90deg);">3</span></div>
                        <div class="clock-number" style="transform: rotate(120deg);"><span style="transform: rotate(-120deg);">4</span></div>
                        <div class="clock-number" style="transform: rotate(150deg);"><span style="transform: rotate(-150deg);">5</span></div>
                        <div class="clock-number" style="transform: rotate(180deg);"><span style="transform: rotate(-180deg);">6</span></div>
                        <div class="clock-number" style="transform: rotate(210deg);"><span style="transform: rotate(-210deg);">7</span></div>
                        <div class="clock-number" style="transform: rotate(240deg);"><span style="transform: rotate(-240deg);">8</span></div>
                        <div class="clock-number" style="transform: rotate(270deg);"><span style="transform: rotate(-270deg);">9</span></div>
                        <div class="clock-number" style="transform: rotate(300deg);"><span style="transform: rotate(-300deg);">10</span></div>
                        <div class="clock-number" style="transform: rotate(330deg);"><span style="transform: rotate(-330deg);">11</span></div>
                        <div class="hand hour-hand" id="hour"></div>
                        <div class="hand min-hand" id="min"></div>
                        <div class="hand sec-hand" id="sec"></div>
                        <div class="clock-center"></div>
                        <div class="clock-date" id="date"></div>
                    </div>
                </div>
            </div>
            <div class="header-right">
                <img src="data:image/png;base64,{header_logo_img}" alt="SmartCar Logo">
            </div>
        </div>
        <script>
            function updateClock() {{
                const now = new Date();
                const s = now.getSeconds();
                const ms = now.getMilliseconds();
                const m = now.getMinutes();
                const h = now.getHours();
                
                const sD = ((s + ms/1000) / 60) * 360;
                const mD = (m / 60) * 360 + (s / 60) * 6;
                const hD = (h % 12 / 12) * 360 + (m / 60) * 30;
                
                document.getElementById('sec').style.transform = "rotate(" + sD + "deg)";
                document.getElementById('min').style.transform = "rotate(" + mD + "deg)";
                document.getElementById('hour').style.transform = "rotate(" + hD + "deg)";
                
                const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
                const day = now.getDate().toString().padStart(2, '0');
                document.getElementById('date').innerText = day + ' ' + months[now.getMonth()];
                
                requestAnimationFrame(updateClock);
            }}
            updateClock();
        </script>
    </body>
    </html>
    """
    components.html(combined_header_html, height=280)


def get_home_subheader_html(logo_b64):
    """Returns the unified Home Subheader HTML with background and clock"""
    from utils.i18n import t
    
    lang_code = st.session_state.get('language', 'de')
    direction = 'rtl' if lang_code == 'ar' else 'ltr'
    text_align = 'right' if direction == 'rtl' else 'left'

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; padding: 0; background: transparent; font-family: sans-serif; }}
            .container {{
                background: rgba(0, 0, 0, 0.6); /* Black rectangle with 60% density */
                border-radius: 15px;
                padding: 10px 20px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                color: white;
                direction: {direction}; /* Dynamic layout */
            }}
            .text-section {{
                text-align: {text_align};
                flex: 1;
            }}
            .text-section h2 {{ font-size: 1.2rem; margin: 0; font-weight: bold; color: #fff; }}
            .text-section p {{ font-size: 0.9rem; margin: 5px 0 0 0; opacity: 0.8; color: #ddd; }}
            
            .logo-section {{
                flex: 1;
                text-align: center;
            }}
            .logo-section img {{ width: 120px; }}
            
            .clock-section {{
                flex: 1;
                display: flex;
                justify-content: flex-end; /* Align clock to end */
            }}
            
            /* Clock Styles */
            .clock {{
                width: 150px; height: 150px;
                border: 4px solid #f1c40f;
                border-radius: 50%;
                position: relative;
                background: #000;
                box-shadow: 0 0 20px rgba(241, 196, 15, 0.2);
            }}
            .hand {{ position: absolute; bottom: 50%; left: 50%; transform-origin: 50% 100%; border-radius: 5px; z-index: 5; }}
            .hour-hand {{ width: 6px; height: 25%; background: #f1c40f; margin-left: -3px; z-index: 6; }}
            .min-hand {{ width: 4px; height: 35%; background: #fff; margin-left: -2px; z-index: 7; }}
            .sec-hand {{ width: 2px; height: 45%; background: #e74c3c; margin-left: -1px; z-index: 8; }}
            .clock-center {{ width: 12px; height: 12px; background: #f1c40f; border-radius: 50%; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 10; }}
            .clock-date {{ font-family: sans-serif; font-size: 14px; color: #fff; text-align: center; position: absolute; width: 100%; bottom: 25px; z-index: 4; }}
            .clock-number {{ position: absolute; width: 100%; height: 100%; text-align: center; color: #f1c40f; font-size: 16px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="text-section">
                <h2>{t('home.info_title')}</h2>
                <p>{t('home.info_subtitle')}</p>
            </div>
            
            <div class="logo-section">
                <img src="data:image/png;base64,{logo_b64}">
            </div>
            
            <div class="clock-section">
                <div class="clock">
                    <div class="clock-number" style="transform: rotate(0deg);"><span style="display: inline-block; transform: rotate(0deg);">12</span></div>
                    <div class="clock-number" style="transform: rotate(30deg);"><span style="display: inline-block; transform: rotate(-30deg);">1</span></div>
                    <div class="clock-number" style="transform: rotate(60deg);"><span style="display: inline-block; transform: rotate(-60deg);">2</span></div>
                    <div class="clock-number" style="transform: rotate(90deg);"><span style="display: inline-block; transform: rotate(-90deg);">3</span></div>
                    <div class="clock-number" style="transform: rotate(120deg);"><span style="display: inline-block; transform: rotate(-120deg);">4</span></div>
                    <div class="clock-number" style="transform: rotate(150deg);"><span style="display: inline-block; transform: rotate(-150deg);">5</span></div>
                    <div class="clock-number" style="transform: rotate(180deg);"><span style="display: inline-block; transform: rotate(-180deg);">6</span></div>
                    <div class="clock-number" style="transform: rotate(210deg);"><span style="display: inline-block; transform: rotate(-210deg);">7</span></div>
                    <div class="clock-number" style="transform: rotate(240deg);"><span style="display: inline-block; transform: rotate(-240deg);">8</span></div>
                    <div class="clock-number" style="transform: rotate(270deg);"><span style="display: inline-block; transform: rotate(-270deg);">9</span></div>
                    <div class="clock-number" style="transform: rotate(300deg);"><span style="display: inline-block; transform: rotate(-300deg);">10</span></div>
                    <div class="clock-number" style="transform: rotate(330deg);"><span style="display: inline-block; transform: rotate(-330deg);">11</span></div>
                    
                    <div class="hand hour-hand" id="hour"></div>
                    <div class="hand min-hand" id="min"></div>
                    <div class="hand sec-hand" id="sec"></div>
                    <div class="clock-center"></div>
                    <div class="clock-date" id="date"></div>
                </div>
            </div>
        </div>
        <script>
            function updateClock() {{
                const now = new Date();
                const s = now.getSeconds();
                const m = now.getMinutes();
                const h = now.getHours();
                
                const sD = (s / 60) * 360;
                const mD = (m / 60) * 360 + (s / 60) * 6;
                const hD = (h % 12 / 12) * 360 + (m / 60) * 30;
                
                document.getElementById('sec').style.transform = "rotate(" + sD + "deg)";
                document.getElementById('min').style.transform = "rotate(" + mD + "deg)";
                document.getElementById('hour').style.transform = "rotate(" + hD + "deg)";
                
                document.getElementById('date').innerText = now.toLocaleDateString('en-GB', {{day:'numeric',month:'short',year:'numeric'}});
                
                requestAnimationFrame(updateClock);
            }}
            updateClock();
        </script>
    </body>
    </html>
    """




def get_predict_subheader_html(logo_b64):
    """Returns the unified Predict Subheader HTML with Title Bar, background, and clock"""

    from utils.i18n import t
    
    lang_code = st.session_state.get('language', 'de')
    direction = 'rtl' if lang_code == 'ar' else 'ltr'
    text_align = 'right' if direction == 'rtl' else 'left'

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; padding: 0; background: transparent; font-family: sans-serif; }}
            .main-wrapper {{
                display: flex;
                flex-direction: column;
                gap: 0;
            }}
            .title-bar {{
                background: black;
                color: white;
                text-align: center;
                padding: 10px;
                font-size: 1.5rem;
                font-weight: bold;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
            }}
            .container {{
                background: rgba(0, 0, 0, 0.6); /* Black rectangle with 60% density */
                border-bottom-left-radius: 15px;
                border-bottom-right-radius: 15px;
                padding: 10px 20px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                color: white;
                direction: {direction}; /* Dynamic layout */
                margin-top: -2px; /* Remove gap */
            }}
            .text-section {{
                text-align: {text_align};
                flex: 1;
            }}
            .text-section h2 {{ font-size: 1.1rem; margin: 0; font-weight: bold; color: #fff; }}
            .text-section p {{ font-size: 0.9rem; margin: 5px 0 0 0; opacity: 0.8; color: #ddd; }}
            
            .logo-section {{
                flex: 1;
                text-align: center;
            }}
            .logo-section img {{ width: 120px; }}
            
            .clock-section {{
                flex: 1;
                display: flex;
                justify-content: flex-end; /* Align clock to end */
            }}
            
            /* Clock Styles */
            .clock {{
                width: 150px; height: 150px;
                border: 4px solid #f1c40f;
                border-radius: 50%;
                position: relative;
                background: #000;
                box-shadow: 0 0 20px rgba(241, 196, 15, 0.2);
            }}
            .hand {{ position: absolute; bottom: 50%; left: 50%; transform-origin: 50% 100%; border-radius: 5px; z-index: 5; }}
            .hour-hand {{ width: 6px; height: 25%; background: #f1c40f; margin-left: -3px; z-index: 6; }}
            .min-hand {{ width: 4px; height: 35%; background: #fff; margin-left: -2px; z-index: 7; }}
            .sec-hand {{ width: 2px; height: 45%; background: #e74c3c; margin-left: -1px; z-index: 8; }}
            .clock-center {{ width: 12px; height: 12px; background: #f1c40f; border-radius: 50%; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 10; }}
            .clock-date {{ font-family: sans-serif; font-size: 14px; color: #fff; text-align: center; position: absolute; width: 100%; bottom: 25px; z-index: 4; }}
            .clock-number {{ position: absolute; width: 100%; height: 100%; text-align: center; color: #f1c40f; font-size: 16px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="main-wrapper">
            <div class="title-bar">
                🏎️ {t('predict.title')}
            </div>
            <div class="container">
                <div class="text-section">
                    <h2>{t('predict.info_title')}</h2>
                    <p>{t('predict.info_subtitle')}</p>
                </div>
                
                <div class="logo-section">
                    <img src="data:image/png;base64,{logo_b64}">
                </div>
                
                <div class="clock-section">
                    <div class="clock">
                        <div class="clock-number" style="transform: rotate(0deg);"><span style="display: inline-block; transform: rotate(0deg);">12</span></div>
                        <div class="clock-number" style="transform: rotate(30deg);"><span style="display: inline-block; transform: rotate(-30deg);">1</span></div>
                        <div class="clock-number" style="transform: rotate(60deg);"><span style="display: inline-block; transform: rotate(-60deg);">2</span></div>
                        <div class="clock-number" style="transform: rotate(90deg);"><span style="display: inline-block; transform: rotate(-90deg);">3</span></div>
                        <div class="clock-number" style="transform: rotate(120deg);"><span style="display: inline-block; transform: rotate(-120deg);">4</span></div>
                        <div class="clock-number" style="transform: rotate(150deg);"><span style="display: inline-block; transform: rotate(-150deg);">5</span></div>
                        <div class="clock-number" style="transform: rotate(180deg);"><span style="display: inline-block; transform: rotate(-180deg);">6</span></div>
                        <div class="clock-number" style="transform: rotate(210deg);"><span style="display: inline-block; transform: rotate(-210deg);">7</span></div>
                        <div class="clock-number" style="transform: rotate(240deg);"><span style="display: inline-block; transform: rotate(-240deg);">8</span></div>
                        <div class="clock-number" style="transform: rotate(270deg);"><span style="display: inline-block; transform: rotate(-270deg);">9</span></div>
                        <div class="clock-number" style="transform: rotate(300deg);"><span style="display: inline-block; transform: rotate(-300deg);">10</span></div>
                        <div class="clock-number" style="transform: rotate(330deg);"><span style="display: inline-block; transform: rotate(-330deg);">11</span></div>
                        
                        <div class="hand hour-hand" id="hour"></div>
                        <div class="hand min-hand" id="min"></div>
                        <div class="hand sec-hand" id="sec"></div>
                        <div class="clock-center"></div>
                        <div class="clock-date" id="date"></div>
                    </div>
                </div>
            </div>
        </div>
        <script>
            function updateClock() {{
                const now = new Date();
                const s = now.getSeconds();
                const m = now.getMinutes();
                const h = now.getHours();
                
                const sD = (s / 60) * 360;
                const mD = (m / 60) * 360 + (s / 60) * 6;
                const hD = (h % 12 / 12) * 360 + (m / 60) * 30;
                
                document.getElementById('sec').style.transform = "rotate(" + sD + "deg)";
                document.getElementById('min').style.transform = "rotate(" + mD + "deg)";
                document.getElementById('hour').style.transform = "rotate(" + hD + "deg)";
                
                document.getElementById('date').innerText = now.toLocaleDateString('en-GB', {{day:'numeric',month:'short',year:'numeric'}});
                
                requestAnimationFrame(updateClock);
            }}
            updateClock();
        </script>
    </body>
    </html>
    """



def get_invoices_subheader_html(logo_b64):
    """Returns the unified Invoices Subheader HTML with Title Bar, background, and clock"""
    from utils.i18n import t
    
    lang_code = st.session_state.get('language', 'de')
    direction = 'rtl' if lang_code == 'ar' else 'ltr'
    text_align = 'right' if direction == 'rtl' else 'left'
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; padding: 0; background: transparent; font-family: sans-serif; }}
            .main-wrapper {{
                display: flex;
                flex-direction: column;
                gap: 0;
            }}
            .title-bar {{
                background: black;
                color: white;
                text-align: center;
                padding: 10px;
                font-size: 1.5rem;
                font-weight: bold;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
            }}
            .container {{
                background: rgba(0, 0, 0, 0.6); /* Black rectangle with 60% density */
                border-bottom-left-radius: 15px;
                border-bottom-right-radius: 15px;
                padding: 10px 20px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                color: white;
                direction: {direction}; /* Dynamic layout */
                margin-top: -2px; /* Remove gap */
            }}
            .text-section {{
                text-align: {text_align};
                flex: 1;
            }}
            .text-section h2 {{ font-size: 1.1rem; margin: 0; font-weight: bold; color: #fff; }}
            .text-section p {{ font-size: 0.9rem; margin: 5px 0 0 0; opacity: 0.8; color: #ddd; }}
            
            .logo-section {{
                flex: 1;
                text-align: center;
            }}
            .logo-section img {{ width: 120px; }}
            
            .clock-section {{
                flex: 1;
                display: flex;
                justify-content: flex-end; /* Align clock to end */
            }}
            
            /* Clock Styles */
            .clock {{
                width: 150px; height: 150px;
                border: 4px solid #f1c40f;
                border-radius: 50%;
                position: relative;
                background: #000;
                box-shadow: 0 0 20px rgba(241, 196, 15, 0.2);
            }}
            .hand {{ position: absolute; bottom: 50%; left: 50%; transform-origin: 50% 100%; border-radius: 5px; z-index: 5; }}
            .hour-hand {{ width: 6px; height: 25%; background: #f1c40f; margin-left: -3px; z-index: 6; }}
            .min-hand {{ width: 4px; height: 35%; background: #fff; margin-left: -2px; z-index: 7; }}
            .sec-hand {{ width: 2px; height: 45%; background: #e74c3c; margin-left: -1px; z-index: 8; }}
            .clock-center {{ width: 12px; height: 12px; background: #f1c40f; border-radius: 50%; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 10; }}
            .clock-date {{ font-family: sans-serif; font-size: 14px; color: #fff; text-align: center; position: absolute; width: 100%; bottom: 25px; z-index: 4; }}
            .clock-number {{ position: absolute; width: 100%; height: 100%; text-align: center; color: #f1c40f; font-size: 16px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="main-wrapper">
            <div class="title-bar">
                📄 {t('invoices.title')}
            </div>
            <div class="container">
                <div class="text-section">
                    <h2>{t('invoices.title')}</h2>
                    <p>{t('invoices.header_subtitle')}</p>
                </div>
                
                <div class="logo-section">
                    <img src="data:image/png;base64,{logo_b64}">
                </div>
                
                <div class="clock-section">
                    <div class="clock">
                        <div class="clock-number" style="transform: rotate(0deg);"><span style="display: inline-block; transform: rotate(0deg);">12</span></div>
                        <div class="clock-number" style="transform: rotate(30deg);"><span style="display: inline-block; transform: rotate(-30deg);">1</span></div>
                        <div class="clock-number" style="transform: rotate(60deg);"><span style="display: inline-block; transform: rotate(-60deg);">2</span></div>
                        <div class="clock-number" style="transform: rotate(90deg);"><span style="display: inline-block; transform: rotate(-90deg);">3</span></div>
                        <div class="clock-number" style="transform: rotate(120deg);"><span style="display: inline-block; transform: rotate(-120deg);">4</span></div>
                        <div class="clock-number" style="transform: rotate(150deg);"><span style="display: inline-block; transform: rotate(-150deg);">5</span></div>
                        <div class="clock-number" style="transform: rotate(180deg);"><span style="display: inline-block; transform: rotate(-180deg);">6</span></div>
                        <div class="clock-number" style="transform: rotate(210deg);"><span style="display: inline-block; transform: rotate(-210deg);">7</span></div>
                        <div class="clock-number" style="transform: rotate(240deg);"><span style="display: inline-block; transform: rotate(-240deg);">8</span></div>
                        <div class="clock-number" style="transform: rotate(270deg);"><span style="display: inline-block; transform: rotate(-270deg);">9</span></div>
                        <div class="clock-number" style="transform: rotate(300deg);"><span style="display: inline-block; transform: rotate(-300deg);">10</span></div>
                        <div class="clock-number" style="transform: rotate(330deg);"><span style="display: inline-block; transform: rotate(-330deg);">11</span></div>
                        
                        <div class="hand hour-hand" id="hour"></div>
                        <div class="hand min-hand" id="min"></div>
                        <div class="hand sec-hand" id="sec"></div>
                        <div class="clock-center"></div>
                        <div class="clock-date" id="date"></div>
                    </div>
                </div>
            </div>
        </div>
        <script>
            function updateClock() {{
                const now = new Date();
                const s = now.getSeconds();
                const m = now.getMinutes();
                const h = now.getHours();
                
                const sD = (s / 60) * 360;
                const mD = (m / 60) * 360 + (s / 60) * 6;
                const hD = (h % 12 / 12) * 360 + (m / 60) * 30;
                
                document.getElementById('sec').style.transform = "rotate(" + sD + "deg)";
                document.getElementById('min').style.transform = "rotate(" + mD + "deg)";
                document.getElementById('hour').style.transform = "rotate(" + hD + "deg)";
                
                document.getElementById('date').innerText = now.toLocaleDateString('en-GB', {{day:'numeric',month:'short',year:'numeric'}});
                
                requestAnimationFrame(updateClock);
            }}
            updateClock();
        </script>
    </body>
    </html>
    """




def get_profile_stats_html(count, total_value, avg_price):
    """Returns the unified Profile Statistics HTML"""
    lang_code = st.session_state.get('language', 'de')
    direction = 'rtl' if lang_code == 'ar' else 'ltr'
    
    return f"""
    <!DOCTYPE html>
    <html dir="{direction}" lang="{lang_code}">
    <head>
        <style>
            body {{ margin: 0; padding: 0; background: transparent; font-family: sans-serif; }}
            .main-wrapper {{
                display: flex;
                flex-direction: column;
                gap: 0;
            }}
            .title-bar {{
                background: black;
                color: white;
                text-align: center;
                padding: 10px;
                font-size: 1.2rem;
                font-weight: bold;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
            }}
            .container {{
                background: rgba(0, 0, 0, 0.6);
                border-bottom-left-radius: 15px;
                border-bottom-right-radius: 15px;
                padding: 20px;
                display: flex;
                align-items: center;
                justify-content: space-around;
                color: white;
                direction: {direction};
                margin-top: -2px;
            }}
            .stat-item {{
                text-align: center;
                flex: 1;
                border-left: 1px solid rgba(255,255,255,0.2);
            }}
            .stat-item:last-child {{
                border-left: none;
            }}
            .stat-value {{
                font-size: 1.8rem;
                font-weight: bold;
                color: #f1c40f;
                margin-bottom: 5px;
            }}
            .stat-label {{
                font-size: 1rem;
                color: #ddd;
            }}
        </style>
    </head>
    <body>
        <div class="main-wrapper">
            <div class="title-bar">
                📊 {t('profile.recent_estimates')}
            </div>
            <div class="container">
                <div class="stat-item">
                    <div class="stat-value">{count}</div>
                    <div class="stat-label">{t('admin.total_transactions')}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${total_value:,.0f}</div>
                    <div class="stat-label">{t('admin.total_value')}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${avg_price:,.0f}</div>
                    <div class="stat-label">{t('admin.average_value')}</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

def get_admin_stats_html(total_users, total_transactions, total_invoices, total_value):
    """
    Returns the unified Admin Statistics HTML
    """
    lang_code = st.session_state.get('language', 'de')
    direction = 'rtl' if lang_code == 'ar' else 'ltr'

    html_content = f"""
    <!DOCTYPE html>
    <html dir="{direction}" lang="{lang_code}">
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
            
            :root {{
                --primary-color: #000000;
                --text-color: #333333;
                --bg-glass: rgba(255, 255, 255, 0.9);
                --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            
            body {{
                font-family: 'Cairo', sans-serif;
                margin: 0;
                padding: 0;
                background-color: transparent;
            }}
            
            .main-wrapper {{
                width: 100%;
                max-width: 1200px;
                margin: 0 auto;
                background: var(--bg-glass);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                overflow: hidden;
                box-shadow: var(--shadow);
                border: 1px solid rgba(255,255,255,0.5);
            }}
            
            /* Black Title Bar */
            .title-bar {{
                background-color: var(--primary-color);
                color: white;
                padding: 15px 25px;
                font-size: 1.2rem;
                font-weight: 700;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            
            .content-box {{
                padding: 25px;
            }}
            
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                text-align: center;
            }}
            
            .stat-item {{
                padding: 15px;
                transition: transform 0.2s;
            }}
            
            .stat-item:hover {{
                transform: translateY(-2px);
            }}
            
            .stat-icon {{
                font-size: 2rem;
                margin-bottom: 10px;
                display: block;
            }}
            
            .stat-label {{
                font-size: 0.9rem;
                color: #666;
                margin-bottom: 5px;
                font-weight: 600;
            }}
            
            .stat-value {{
                font-size: 1.8rem;
                font-weight: 700;
                color: var(--primary-color);
            }}
            
            /* Responsive */
            @media (max-width: 768px) {{
                .stats-grid {{
                    grid-template-columns: repeat(2, 1fr);
                }}
            }}
        </style>
    </head>
    <body>
        <div class="main-wrapper">
             <div class="title-bar">
                📊 {t('admin.statistics')}
            </div>
            
            <div class="content-box">
                <div class="stats-grid">
                    <div class="stat-item">
                        <span class="stat-icon">👥</span>
                        <div class="stat-label">{t('admin.total_users')}</div>
                        <div class="stat-value">{total_users}</div>
                    </div>
                    
                    <div class="stat-item">
                        <span class="stat-icon">💼</span>
                        <div class="stat-label">{t('admin.total_transactions')}</div>
                        <div class="stat-value">{total_transactions}</div>
                    </div>
                    
                    <div class="stat-item">
                        <span class="stat-icon">📄</span>
                        <div class="stat-label">{t('admin.total_invoices')}</div>
                        <div class="stat-value">{total_invoices}</div>
                    </div>
                     
                    <div class="stat-item">
                        <span class="stat-icon">💰</span>
                        <div class="stat-label">{t('admin.total_value')}</div>
                        <div class="stat-value">${total_value:,.0f}</div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html_content, height=220)

def get_results_page_html(estimated_price, price_range, confidence, confidence_pct, car_data, comp):
    """
    Returns the unified Results Page HTML with Black Title Bar and Glass Effect
    """
    
    lang_code = st.session_state.get('language', 'de')
    direction = 'rtl' if lang_code == 'ar' else 'ltr'
    text_align = 'right' if direction == 'rtl' else 'left'

    html_content = f"""
    <!DOCTYPE html>
    <html dir="{direction}" lang="{lang_code}">
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
            
            :root {{
                --primary-color: #000000;
                --text-color: #333333;
                --bg-glass: rgba(255, 255, 255, 0.9);
                --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                --success-color: #28a745;
            }}
            
            body {{
                font-family: 'Cairo', sans-serif;
                margin: 0;
                padding: 0;
                background-color: transparent;
            }}
            
            .main-wrapper {{
                width: 100%;
                max-width: 1200px;
                margin: 0 auto;
                background: var(--bg-glass);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                overflow: hidden;
                box-shadow: var(--shadow);
                border: 1px solid rgba(255,255,255,0.5);
                margin-bottom: 20px;
            }}
            
            /* Black Title Bar */
            .title-bar {{
                background-color: var(--primary-color);
                color: white;
                padding: 15px 25px;
                font-size: 1.2rem;
                font-weight: 700;
                display: flex;
                align-items: center;
                gap: 10px;
                justify-content: space-between;
            }}
            
            .content-box {{
                padding: 30px;
                text-align: center;
            }}
            
            .price-display {{
                margin-bottom: 30px;
            }}
            
            .price-value {{
                font-size: 3.5rem;
                font-weight: 700;
                color: var(--primary-color);
                margin: 10px 0;
            }}
            
            .price-label {{
                font-size: 1.1rem;
                color: #666;
            }}
            
            .range-badge {{
                background: rgba(0,0,0,0.05);
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.9rem;
                color: #555;
                font-weight: 600;
            }}
            
            .details-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                text-align: {text_align};
                border-top: 1px solid #eee;
                padding-top: 20px;
            }}
            
            .section-title {{
                font-size: 1.1rem;
                font-weight: 700;
                margin-bottom: 15px;
                color: var(--primary-color);
                border-bottom: 2px solid #eee;
                padding-bottom: 5px;
                display: inline-block;
            }}
            
            .detail-row {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 10px;
                font-size: 0.95rem;
            }}
            
            .detail-label {{ color: #777; }}
            .detail-val {{ font-weight: 600; color: #333; }}
            
            /* Responsive */
            @media (max-width: 768px) {{
                .details-grid {{ grid-template-columns: 1fr; gap: 20px; }}
            }}
        </style>
    </head>
    <body>
        <div class="main-wrapper">
             <div class="title-bar">
                <span>💰 {t('results.title')}</span>
                <span style="font-size:0.9rem; opacity:0.9">{t('results.confidence')}: {confidence} ({confidence_pct}%)</span>
            </div>
            
            <div class="content-box">
                <div class="price-display">
                    <div class="price-label">{t('results.estimated_price')}</div>
                    <div class="price-value">${estimated_price:,.0f}</div>
                    <span class="range-badge">{t('results.range', 'Range')}: ${price_range.get('min', 0):,.0f} - ${price_range.get('max', 0):,.0f}</span>
                <div style="font-size: 0.85rem; color: #666; margin-top: 8px; font-weight: normal;">
                    <span style="color: #d9534f;">▼ {t('results.min_sell', 'Min (Sell)')}</span> &nbsp;&nbsp;|&nbsp;&nbsp; 
                    <span style="color: #5cb85c;">▲ {t('results.max_negotiate', 'Max (Negotiate)')}</span>
                </div>
                
                <div class="details-grid">
                    <div>
                        <div class="section-title">🏎️ {t('predict.step2_title')}</div>
                        <div class="detail-row"><span class="detail-label">{t('predict.car_type')}:</span> <span class="detail-val">{car_data.get('car_type', '-')}</span></div>
                        <div class="detail-row"><span class="detail-label">{t('predict.model')}:</span> <span class="detail-val">{car_data.get('brand', '-')} {car_data.get('model', '')}</span></div>
                        <div class="detail-row"><span class="detail-label">{t('predict.year')}:</span> <span class="detail-val">{car_data.get('manufacture_year', '-')}</span></div>
                        <div class="detail-row"><span class="detail-label">{t('predict.mileage')}:</span> <span class="detail-val">{car_data.get('mileage', 0):,} km</span></div>
                        <div class="detail-row"><span class="detail-label">{t('predict.fuel_type')}:</span> <span class="detail-val">{car_data.get('fuel_type', 'Petrol')}</span></div>
                        <div class="detail-row"><span class="detail-label">{t('results.owners', 'Owners')}:</span> <span class="detail-val">{car_data.get('previous_owners', 1)}</span></div>
                        
                        <div class="section-title" style="margin-top: 15px;">🛠️ {t('results.engine_maintenance', 'Engine & Maintenance')}</div>
                        <div class="detail-row"><span class="detail-label">{t('results.engine', 'Engine')}:</span> <span class="detail-val">{car_data.get('analysis', {}).get('engine_cylinders', '-')} cyl / {car_data.get('analysis', {}).get('engine_displacement_cc', '-')} cc</span></div>
                        <div class="detail-row"><span class="detail-label">{t('results.power', 'Power')}:</span> <span class="detail-val">{car_data.get('analysis', {}).get('engine_horsepower', '-')} hp</span></div>
                        <div class="detail-row"><span class="detail-label">{t('results.maintenance', 'Maintenance')}:</span> <span class="detail-val">{'Yes' if car_data.get('maintenance_history') else 'No'}</span></div>
                        <div class="detail-row"><span class="detail-label">{t('results.tuv', 'TÜV')}:</span> <span class="detail-val">{car_data.get('tuv_months', 0)} {t('results.months_left', 'months left')}</span></div>
                    </div>
                    
                    <div>
                        <div class="section-title">📊 {t('results.price_analysis', 'Price Analysis')}</div>
                        <div class="detail-row"><span class="detail-label">{t('checkout.base_price')}:</span> <span class="detail-val">${comp['base_price']:,}</span></div>
                        <div class="detail-row"><span class="detail-label">{t('results.condition_factor', 'Condition Factor')}:</span> <span class="detail-val">x{comp['condition']['factor']:.2f} ({comp['condition']['contribution']:+})</span></div>
                        <div class="detail-row"><span class="detail-label">{t('results.mileage_factor', 'Mileage Factor')}:</span> <span class="detail-val">x{comp['mileage']['factor']:.2f} ({comp['mileage']['contribution']:+})</span></div>
                        <div class="detail-row"><span class="detail-label">{t('results.age_factor', 'Age Factor')}:</span> <span class="detail-val">x{comp['age']['factor']:.2f} ({comp['age']['contribution']:+})</span></div>
                        
                        <div class="detail-row" style="margin-top:5px; border-top:1px dashed #eee; padding-top:5px"><span class="detail-label">{t('predict.brand')}:</span> <span class="detail-val">x{comp['brand_factor']:.2f}</span></div>
                        <div class="detail-row"><span class="detail-label">{t('predict.fuel_type')}:</span> <span class="detail-val">x{comp.get('fuel_factor', 1.0):.2f}</span></div>
                        <div class="detail-row"><span class="detail-label">{t('results.owners', 'Owners')}:</span> <span class="detail-val">x{comp.get('owners_factor', 1.0):.2f}</span></div>
                        <div class="detail-row"><span class="detail-label">{t('results.tuv_factor', 'TÜV Factor')}:</span> <span class="detail-val">x{comp.get('tuv_factor', 1.0):.2f}</span></div>
                        <div class="detail-row"><span class="detail-label">{t('results.maintenance_factor', 'Maintenance Factor')}:</span> <span class="detail-val">x{comp.get('maintenance_factor', 1.0):.2f}</span></div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html_content, height=500, scrolling=True)


def get_analysis_results_html(analysis):
    """
    Returns the unified Analysis Results HTML with Black Title Bar and Glass Effect
    """
    # Extract values with defaults
    # Mapping English conditions dynamically
    lang_code = st.session_state.get('language', 'de')
    cond_map = {
        'Excellent': t('predict.cond_excellent', 'Excellent'),
        'Good': t('predict.cond_good', 'Good'),
        'Fair': t('predict.cond_fair', 'Fair'),
        'Poor': t('predict.cond_poor', 'Poor')
    }
    raw_cond = analysis.get('exterior_condition', analysis.get('condition', 'Good'))
    condition = cond_map.get(raw_cond, raw_cond)
    
    unknown_text = t('common.unknown', 'Unknown')
    car_type = analysis.get('estimated_type', unknown_text)
    color = analysis.get('color', unknown_text)
    doors = str(analysis.get('doors', t('common.unspecified', 'N/A')))
    fuel = analysis.get('fuel_type', unknown_text)
    
    # Engine Specs
    cylinders = str(analysis.get('engine_cylinders', unknown_text))
    displacement = str(analysis.get('engine_displacement_cc', unknown_text))
    hp = str(analysis.get('engine_horsepower', unknown_text))
    
    confidence = analysis.get('confidence', 0)
    conf_str = f"{confidence * 100:.0f}%" if isinstance(confidence, (int, float)) else str(confidence)

    lang_code = st.session_state.get('language', 'de')
    direction = 'rtl' if lang_code == 'ar' else 'ltr'

    html_content = f"""
    <!DOCTYPE html>
    <html dir="{direction}" lang="{lang_code}">
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
            
            :root {{
                --primary-color: #000000;
                --text-color: #333333;
                --bg-glass: rgba(255, 255, 255, 0.9);
                --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            
            body {{
                font-family: 'Cairo', sans-serif;
                margin: 0;
                padding: 0;
                background-color: transparent;
            }}
            
            .main-wrapper {{
                width: 100%;
                max-width: 1200px;
                margin: 0 auto;
                background: var(--bg-glass);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                overflow: hidden;
                box-shadow: var(--shadow);
                border: 1px solid rgba(255,255,255,0.5);
            }}
            
            /* Black Title Bar */
            .title-bar {{
                background-color: var(--primary-color);
                color: white;
                padding: 15px 25px;
                font-size: 1.2rem;
                font-weight: 700;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            
            .content-box {{
                padding: 20px;
            }}
            
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr); /* 3 أعمدة رئيسية */
                gap: 20px;
                text-align: center;
            }}
            
            .stat-item {{
                padding: 10px;
                background: rgba(255,255,255,0.5);
                border-radius: 10px;
                border: 1px solid #eee;
            }}
            
            .stat-label {{
                font-size: 0.8rem;
                color: #666;
                margin-bottom: 5px;
            }}
            
            .stat-value {{
                font-size: 1.1rem;
                font-weight: 700;
                color: var(--primary-color);
            }}
            
            .grid-row {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 10px;
                margin-bottom: 15px;
            }}

        </style>
    </head>
    <body>
        <div class="main-wrapper">
             <div class="title-bar">
                🔍 {t('analysis.title', 'Analysis Results')}
            </div>
            
            <div class="content-box">
                <!-- Row 1: Basic Info -->
                <div class="grid-row">
                    <div class="stat-item">
                        <div class="stat-label">{t('predict.car_type')}</div>
                        <div class="stat-value">{car_type}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">{t('predict.condition', 'Condition')}</div>
                        <div class="stat-value">{condition}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">{t('results.confidence')}</div>
                        <div class="stat-value">{conf_str}</div>
                    </div>
                </div>

                <!-- Row 2: Specs -->
                <div class="grid-row">
                    <div class="stat-item">
                        <div class="stat-label">{t('predict.color')}</div>
                        <div class="stat-value">{color}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">{t('predict.doors', 'Doors')}</div>
                        <div class="stat-value">{doors}</div>
                    </div>
                     <div class="stat-item">
                        <div class="stat-label">{t('predict.fuel_type')}</div>
                        <div class="stat-value">{fuel}</div>
                    </div>
                </div>
                
                <!-- Row 3: Engine Specs -->
                <div class="grid-row">
                    <div class="stat-item">
                        <div class="stat-label">{t('predict.engine_size', 'Engine Size')}</div>
                        <div class="stat-value">{displacement} cc</div>
                    </div>
                     <div class="stat-item">
                        <div class="stat-label">{t('predict.horsepower', 'Horsepower')}</div>
                        <div class="stat-value">{hp} hp</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">{t('predict.cylinders', 'Cylinders')}</div>
                        <div class="stat-value">{cylinders}</div>
                    </div>
                </div>

                <!-- Row 4: Drivetrain & Features (New) -->
                <div class="grid-row">
                    <div class="stat-item">
                        <div class="stat-label">{t('predict.transmission', 'Transmission')}</div>
                        <div class="stat-value">{analysis.get('transmission', 'غير معروف')}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">{t('predict.drivetrain', 'Drivetrain')}</div>
                        <div class="stat-value">{analysis.get('drivetrain', 'غير معروف')}</div>
                    </div>
                     <div class="stat-item">
                        <div class="stat-label">{t('predict.trim', 'Trim')}</div>
                        <div class="stat-value">{analysis.get('estimated_trim', 'غير معروف')}</div>
                    </div>
                </div>
                
                <!-- Row 5: Interior & Features -->
                 <div class="grid-row" style="grid-template-columns: 1fr 2fr;">
                    <div class="stat-item">
                        <div class="stat-label">{t('predict.interior', 'Interior')}</div>
                        <div class="stat-value">{analysis.get('interior_type', '-')} - {analysis.get('interior_color', '-')}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">{t('predict.features', 'Key Features')}</div>
                        <div class="stat-value" style="font-size: 0.9rem;">{', '.join(analysis.get('features', ['لا يوجد']))}</div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html_content, height=400)


def get_section_header_html(title):
    """
    Returns a unified Section Header HTML (Black Title Bar only)
    """
    lang_code = st.session_state.get('language', 'de')
    direction = 'rtl' if lang_code == 'ar' else 'ltr'

    html_content = f"""
    <!DOCTYPE html>
    <html dir="{direction}" lang="{lang_code}">
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
            
            :root {{
                --primary-color: #000000;
            }}
            
            body {{
                font-family: 'Cairo', sans-serif;
                margin: 0;
                padding: 0;
                background-color: transparent;
            }}
            
            .title-bar {{
                background-color: var(--primary-color);
                color: white;
                padding: 10px 20px;
                font-size: 1.1rem;
                font-weight: 700;
                border-radius: 10px;
                display: flex;
                align-items: center;
                gap: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
        </style>
    </head>
    <body>
        <div class="title-bar">
            {title}
        </div>
    </body>
    </html>
    """
    components.html(html_content, height=60)


def get_admin_dashboard_html(stats):
    """
    Returns the unified Admin Dashboard Overview HTML
    (Combines General Stats and Time-based Activity)
    """
    
    # Extract values safely
    total_users = stats.get('total_users', 0)
    total_txns = stats.get('total_transactions', 0)
    total_invoices = stats.get('total_invoices', 0)
    total_value = stats.get('total_estimated_value', 0)
    
    today = stats.get('today_transactions', 0)
    week = stats.get('week_transactions', 0)
    month = stats.get('month_transactions', 0)
    year = stats.get('year_transactions', 0)
    
    lang_code = st.session_state.get('language', 'de')
    direction = 'rtl' if lang_code == 'ar' else 'ltr'
    html_lang = lang_code

    html_content = f"""
    <!DOCTYPE html>
    <html dir="{direction}" lang="{html_lang}">
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
            
            :root {{
                --primary-dark: #0E1117;
                --secondary-dark: #161B22;
                --accent-gold: #D4AF37;
                --accent-amber: #ffb800;
                --text-light: #ffffff;
                --text-muted: #a0a0c0;
                --glass-bg: rgba(26, 26, 46, 0.95);
                --card-gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                --card-gradient-2: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                --card-gradient-3: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                --card-gradient-4: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            }}
            
            body {{
                font-family: 'Cairo', sans-serif;
                margin: 0;
                padding: 0;
                background-color: transparent;
            }}
            
            .main-wrapper {{
                width: 100%;
                background: var(--glass-bg);
                backdrop-filter: blur(15px);
                border-radius: 20px;
                overflow: hidden;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                border: 1px solid rgba(255,255,255,0.1);
                margin-bottom: 20px;
            }}
            
            /* Golden Title Bar */
            .title-bar {{
                background: linear-gradient(135deg, #0E1117 0%, #161B22 100%);
                color: var(--accent-gold);
                padding: 15px 25px;
                font-size: 1.2rem;
                font-weight: 700;
                display: flex;
                align-items: center;
                gap: 12px;
                border-bottom: 2px solid var(--accent-gold);
            }}
            
            .title-bar .icon {{
                font-size: 1.5rem;
            }}
            
            .content-box {{
                padding: 25px;
                background: linear-gradient(180deg, rgba(26,26,46,0.9) 0%, rgba(15,52,96,0.7) 100%);
            }}
            
            /* Grid Layouts */
            .stats-row {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                margin-bottom: 25px;
            }}
            
            /* 3D Crystal Glass Cards */
            .stat-card {{
                padding: 25px 20px;
                border-radius: 20px;
                text-align: center;
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                position: relative;
                overflow: hidden;
                transform-style: preserve-3d;
                perspective: 1000px;
                border: 1px solid rgba(255, 255, 255, 0.25);
                backdrop-filter: blur(20px);
                box-shadow: 
                    0 8px 32px rgba(0, 0, 0, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.4),
                    inset 0 -1px 0 rgba(0, 0, 0, 0.1);
            }}
            
            /* Crystal top shine */
            .stat-card::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 50%;
                background: linear-gradient(180deg, 
                    rgba(255, 255, 255, 0.35) 0%, 
                    rgba(255, 255, 255, 0.15) 40%,
                    transparent 100%);
                border-radius: 20px 20px 50% 50%;
                z-index: 1;
                pointer-events: none;
            }}
            
            /* Crystal bottom reflection */
            .stat-card::after {{
                content: '';
                position: absolute;
                bottom: 0;
                left: 10%;
                right: 10%;
                height: 30%;
                background: linear-gradient(0deg, 
                    rgba(255, 255, 255, 0.08) 0%, 
                    transparent 100%);
                border-radius: 0 0 15px 15px;
                z-index: 1;
                pointer-events: none;
            }}
            
            .stat-card:hover {{
                transform: translateY(-10px) rotateX(5deg) rotateY(-3deg);
                box-shadow: 
                    0 25px 50px rgba(0, 0, 0, 0.4),
                    0 15px 30px rgba(0, 0, 0, 0.3),
                    inset 0 2px 0 rgba(255, 255, 255, 0.5),
                    inset 0 -2px 0 rgba(0, 0, 0, 0.15);
                border-color: rgba(255, 255, 255, 0.4);
            }}
            
            /* Crystal gradient backgrounds */
            .stat-card.gradient-1 {{ 
                background: linear-gradient(145deg, 
                    rgba(102, 126, 234, 0.85) 0%, 
                    rgba(118, 75, 162, 0.85) 50%,
                    rgba(102, 126, 234, 0.7) 100%); 
            }}
            .stat-card.gradient-2 {{ 
                background: linear-gradient(145deg, 
                    rgba(240, 147, 251, 0.85) 0%, 
                    rgba(245, 87, 108, 0.85) 50%,
                    rgba(240, 147, 251, 0.7) 100%); 
            }}
            .stat-card.gradient-3 {{ 
                background: linear-gradient(145deg, 
                    rgba(79, 172, 254, 0.85) 0%, 
                    rgba(0, 242, 254, 0.85) 50%,
                    rgba(79, 172, 254, 0.7) 100%); 
            }}
            .stat-card.gradient-4 {{ 
                background: linear-gradient(145deg, 
                    rgba(67, 233, 123, 0.85) 0%, 
                    rgba(56, 249, 215, 0.85) 50%,
                    rgba(67, 233, 123, 0.7) 100%); 
            }}
            
            .stat-icon {{
                font-size: 2.8rem;
                margin-bottom: 12px;
                display: block;
                position: relative;
                z-index: 2;
                filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.4));
                animation: float-icon 4s ease-in-out infinite;
            }}
            
            @keyframes float-icon {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-5px); }}
            }}
            
            .stat-label {{
                font-size: 0.95rem;
                color: rgba(255, 255, 255, 0.95);
                margin-bottom: 10px;
                font-weight: 600;
                position: relative;
                z-index: 2;
                text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
                letter-spacing: 0.5px;
            }}
            
            .stat-value {{
                font-size: 2.2rem;
                font-weight: 800;
                color: var(--text-light);
                position: relative;
                z-index: 2;
                text-shadow: 
                    0 2px 4px rgba(0, 0, 0, 0.4),
                    0 4px 15px rgba(0, 0, 0, 0.2);
                letter-spacing: 1px;
            }}
            
            .section-divider {{
                height: 2px;
                background: linear-gradient(90deg, transparent, var(--accent-gold), transparent);
                margin: 15px 0 25px 0;
            }}
            
            .section-header {{
                font-size: 1.1rem;
                font-weight: 700;
                margin-bottom: 20px;
                color: var(--accent-gold);
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            
            .section-header .icon {{
                font-size: 1.3rem;
            }}
            
            /* Time-based stats styling */
            .time-stat {{
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 18px;
                background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
                border-radius: 14px;
                border: 1px solid rgba(255,255,255,0.1);
                backdrop-filter: blur(5px);
                transition: transform 0.2s, border-color 0.2s;
            }}
            
            .time-stat:hover {{
                transform: translateY(-3px);
                border-color: var(--accent-gold);
            }}
            
            .time-label {{
                font-size: 0.85rem;
                color: var(--text-muted);
                margin-bottom: 5px;
            }}
            
            .time-value {{
                font-size: 1.8rem;
                font-weight: 700;
            }}
            
            /* Golden accent colors for time values */
            .time-stat:nth-child(1) .time-value {{ color: #4facfe; }}
            .time-stat:nth-child(2) .time-value {{ color: #43e97b; }}
            .time-stat:nth-child(3) .time-value {{ color: #f093fb; }}
            .time-stat:nth-child(4) .time-value {{ color: var(--accent-gold); }}

        </style>
    </head>
    <body>
        <div class="main-wrapper">
             <div class="title-bar">
                <span class="icon">📊</span> {t('admin.dashboard_title')}
            </div>
            
            <div class="content-box">
                <!-- Top Row: Main KPIs with Gradient Cards -->
                <div class="stats-row">
                    <div class="stat-card gradient-1">
                        <span class="stat-icon">👥</span>
                        <div class="stat-label">{t('admin.total_users')}</div>
                        <div class="stat-value">{total_users}</div>
                    </div>
                    <div class="stat-card gradient-2">
                        <span class="stat-icon">💼</span>
                        <div class="stat-label">{t('admin.total_transactions')}</div>
                        <div class="stat-value">{total_txns}</div>
                    </div>
                    <div class="stat-card gradient-3">
                        <span class="stat-icon">📄</span>
                        <div class="stat-label">{t('admin.total_invoices')}</div>
                        <div class="stat-value">{total_invoices}</div>
                    </div>
                    <div class="stat-card gradient-4">
                        <span class="stat-icon">💰</span>
                        <div class="stat-label">{t('admin.total_value')}</div>
                        <div class="stat-value" style="font-size: 1.5rem;">€{total_value:,.0f}</div>
                    </div>
                </div>
                
                <div class="section-divider"></div>
                
                <div class="section-header">
                    <span class="icon">📅</span> {t('admin.activity_title')}
                </div>
                
                <!-- Bottom Row: Time-based Activity -->
                <div class="stats-row">
                    <div class="time-stat">
                        <div class="time-label">{t('admin.today')}</div>
                        <div class="time-value">{today}</div>
                    </div>
                    <div class="time-stat">
                        <div class="time-label">{t('admin.this_week')}</div>
                        <div class="time-value">{week}</div>
                    </div>
                    <div class="time-stat">
                        <div class="time-label">{t('admin.this_month')}</div>
                        <div class="time-value">{month}</div>
                    </div>
                    <div class="time-stat">
                        <div class="time-label">{t('admin.this_year')}</div>
                        <div class="time-value">{year}</div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html_content, height=600)


def get_profile_subheader_html(logo_b64):
    """Returns the unified Profile Subheader HTML with Title Bar, background, and clock"""
    from utils.i18n import t
    
    lang_code = st.session_state.get('language', 'de')
    direction = 'rtl' if lang_code == 'ar' else 'ltr'
    text_align = 'right' if direction == 'rtl' else 'left'

    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; padding: 0; background: transparent; font-family: sans-serif; }}
            .main-wrapper {{
                display: flex;
                flex-direction: column;
                gap: 0;
            }}
            .title-bar {{
                background: black;
                color: white;
                text-align: center;
                padding: 10px;
                font-size: 1.5rem;
                font-weight: bold;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
            }}
            .container {{
                background: rgba(0, 0, 0, 0.6); /* Black rectangle with 60% density */
                border-bottom-left-radius: 15px;
                border-bottom-right-radius: 15px;
                padding: 10px 20px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                color: white;
                direction: {direction}; /* Dynamic layout */
                margin-top: -2px; /* Remove gap */
            }}
            .text-section {{
                text-align: {text_align};
                flex: 1;
            }}
            .text-section h2 {{ font-size: 1.1rem; margin: 0; font-weight: bold; color: #fff; }}
            .text-section p {{ font-size: 0.9rem; margin: 5px 0 0 0; opacity: 0.8; color: #ddd; }}
            
            .logo-section {{
                flex: 1;
                text-align: center;
            }}
            .logo-section img {{ width: 120px; }}
            
            .clock-section {{
                flex: 1;
                display: flex;
                justify-content: flex-end; /* Align clock to end */
            }}
            
            /* Clock Styles */
            .clock {{
                width: 150px; height: 150px;
                border: 4px solid #f1c40f;
                border-radius: 50%;
                position: relative;
                background: #000;
                box-shadow: 0 0 20px rgba(241, 196, 15, 0.2);
            }}
            .hand {{ position: absolute; bottom: 50%; left: 50%; transform-origin: 50% 100%; border-radius: 5px; z-index: 5; }}
            .hour-hand {{ width: 6px; height: 25%; background: #f1c40f; margin-left: -3px; z-index: 6; }}
            .min-hand {{ width: 4px; height: 35%; background: #fff; margin-left: -2px; z-index: 7; }}
            .sec-hand {{ width: 2px; height: 45%; background: #e74c3c; margin-left: -1px; z-index: 8; }}
            .clock-center {{ width: 12px; height: 12px; background: #f1c40f; border-radius: 50%; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 10; }}
            .clock-date {{ font-family: sans-serif; font-size: 14px; color: #fff; text-align: center; position: absolute; width: 100%; bottom: 25px; z-index: 4; }}
            .clock-number {{ position: absolute; width: 100%; height: 100%; text-align: center; color: #f1c40f; font-size: 16px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="main-wrapper">
            <div class="title-bar">
                👤 {t('profile.header_title')}
            </div>
            <div class="container">
                <div class="text-section">
                    <h2>{t('profile.header_title')}</h2>
                    <p>{t('profile.header_subtitle')}</p>
                </div>
                
                <div class="logo-section">
                    <img src="data:image/png;base64,{logo_b64}">
                </div>
                
                <div class="clock-section">
                    <div class="clock">
                        <div class="clock-number" style="transform: rotate(0deg);"><span style="display: inline-block; transform: rotate(0deg);">12</span></div>
                        <div class="clock-number" style="transform: rotate(30deg);"><span style="display: inline-block; transform: rotate(-30deg);">1</span></div>
                        <div class="clock-number" style="transform: rotate(60deg);"><span style="display: inline-block; transform: rotate(-60deg);">2</span></div>
                        <div class="clock-number" style="transform: rotate(90deg);"><span style="display: inline-block; transform: rotate(-90deg);">3</span></div>
                        <div class="clock-number" style="transform: rotate(120deg);"><span style="display: inline-block; transform: rotate(-120deg);">4</span></div>
                        <div class="clock-number" style="transform: rotate(150deg);"><span style="display: inline-block; transform: rotate(-150deg);">5</span></div>
                        <div class="clock-number" style="transform: rotate(180deg);"><span style="display: inline-block; transform: rotate(-180deg);">6</span></div>
                        <div class="clock-number" style="transform: rotate(210deg);"><span style="display: inline-block; transform: rotate(-210deg);">7</span></div>
                        <div class="clock-number" style="transform: rotate(240deg);"><span style="display: inline-block; transform: rotate(-240deg);">8</span></div>
                        <div class="clock-number" style="transform: rotate(270deg);"><span style="display: inline-block; transform: rotate(-270deg);">9</span></div>
                        <div class="clock-number" style="transform: rotate(300deg);"><span style="display: inline-block; transform: rotate(-300deg);">10</span></div>
                        <div class="clock-number" style="transform: rotate(330deg);"><span style="display: inline-block; transform: rotate(-330deg);">11</span></div>
                        
                        <div class="hand hour-hand" id="hour"></div>
                        <div class="hand min-hand" id="min"></div>
                        <div class="hand sec-hand" id="sec"></div>
                        <div class="clock-center"></div>
                        <div class="clock-date" id="date"></div>
                    </div>
                </div>
            </div>
        </div>
        <script>
            function updateClock() {{
                const now = new Date();
                const s = now.getSeconds();
                const m = now.getMinutes();
                const h = now.getHours();
                
                const sD = (s / 60) * 360;
                const mD = (m / 60) * 360 + (s / 60) * 6;
                const hD = (h % 12 / 12) * 360 + (m / 60) * 30;
                
                document.getElementById('sec').style.transform = "rotate(" + sD + "deg)";
                document.getElementById('min').style.transform = "rotate(" + mD + "deg)";
                document.getElementById('hour').style.transform = "rotate(" + hD + "deg)";
                
                document.getElementById('date').innerText = now.toLocaleDateString('en-GB', {{day:'numeric',month:'short',year:'numeric'}});
                
                requestAnimationFrame(updateClock);
            }}
            updateClock();
        </script>
    </body>
    </html>
    """

# إضافة المسار الرئيسي
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


# ======================
# تهيئة النظام
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
# ======================

def home_page():
    """الصفحة الرئيسية"""
    user = st.session_state.user
    
    username = user.get('full_name') or user.get('username')
    
    # Render universal header
    render_universal_header(t('app.welcome') + f", {username}!", "🏠 " + t('nav.home'))
    
    # === لوحة التحكم المدمجة (للأدمن فقط) ===
    if user.get('role') == 'admin':
        # Custom styled admin header
        admin_dashboard_title = t('admin.dashboard')
        st.markdown(f"""
        <style>
            .admin-header {{
                background: linear-gradient(135deg, #0E1117 0%, #161B22 100%);
                padding: 15px 25px;
                border-radius: 15px;
                margin: 20px 0;
                border: 2px solid #D4AF37;
            }}
            .admin-header h3 {{
                color: #D4AF37;
                margin: 0;
                font-size: 1.3rem;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            /* Style the selectbox */
            div[data-testid="stSelectbox"] > div > div {{
                background: linear-gradient(135deg, #0E1117 0%, #161B22 100%) !important;
                border: 2px solid #D4AF37 !important;
                border-radius: 12px !important;
                color: #D4AF37 !important;
                min-height: 48px !important;
                font-size: 1rem !important;
                padding: 6px 10px !important;
            }}
            div[data-testid="stSelectbox"] > div > div > div {{
                font-size: 1rem !important;
                font-weight: 600 !important;
                color: #ffffff !important;
            }}
            div[data-testid="stSelectbox"] [data-baseweb="select"] > div {{
                min-width: 100% !important;
            }}
            div[data-testid="stSelectbox"] label {{
                color: #D4AF37 !important;
                font-weight: 600 !important;
                font-size: 1.1rem !important;
            }}
            /* Dropdown menu items */
            div[data-baseweb="popover"] {{
                background: linear-gradient(135deg, #0E1117 0%, #161B22 100%) !important;
                border: 2px solid #D4AF37 !important;
                border-radius: 12px !important;
            }}
            div[data-baseweb="popover"] ul {{
                background: transparent !important;
            }}
            div[data-baseweb="popover"] ul li {{
                font-size: 1.05rem !important;
                padding: 14px 20px !important;
                color: #ffffff !important;
                background: transparent !important;
                font-weight: 500 !important;
            }}
            div[data-baseweb="popover"] ul li:hover {{
                background: rgba(240, 180, 41, 0.3) !important;
                color: #D4AF37 !important;
            }}
            div[data-baseweb="popover"] ul li[aria-selected="true"] {{
                background: rgba(240, 180, 41, 0.2) !important;
                color: #D4AF37 !important;
            }}
        </style>
        """, unsafe_allow_html=True)
        
        # القائمة المنسدلة بتنسيق محسن (عرض 50%)
        menu_col, _ = st.columns([0.5, 0.5])
        with menu_col:
            admin_menu = st.selectbox(
                f"📂 {t('admin.select_section')}",
                [t('admin.statistics'), t('admin.users'), t('admin.employees'), t('admin.payroll'), t('admin.transactions'), t('admin.financial_settings'), t('admin.profit_reports'), t('admin.attendance')],
                label_visibility="collapsed"
            )
        
        db = DatabaseManager()
        
        if admin_menu == t('admin.statistics'):
            stats = db.get_statistics()
            get_admin_dashboard_html(stats)
        
        elif admin_menu == t('admin.users'):
            # Enhanced CSS for User Management
            st.markdown("""
            <style>
                /* User Card Enhanced Styling */
                div[data-testid="stExpander"] {
                    background: linear-gradient(135deg, rgba(26, 26, 46, 0.98) 0%, rgba(15, 52, 96, 0.95) 100%) !important;
                    border: 2px solid #D4AF37 !important;
                    border-radius: 15px !important;
                    margin-bottom: 15px !important;
                    box-shadow: 0 4px 20px rgba(240, 180, 41, 0.2) !important;
                }
                /* Expander Header */
                div[data-testid="stExpander"] > div:first-child {
                    background: linear-gradient(90deg, rgba(240, 180, 41, 0.25) 0%, rgba(240, 180, 41, 0.05) 100%) !important;
                    border-radius: 13px 13px 0 0 !important;
                    padding: 12px 15px !important;
                }
                /* Force white text on ALL expander header elements */
                div[data-testid="stExpander"] > div:first-child,
                div[data-testid="stExpander"] > div:first-child *,
                div[data-testid="stExpander"] > div:first-child span,
                div[data-testid="stExpander"] > div:first-child p,
                div[data-testid="stExpander"] > details > summary,
                div[data-testid="stExpander"] > details > summary *,
                div[data-testid="stExpander"] summary,
                div[data-testid="stExpander"] summary *,
                .st-emotion-cache-p5msec,
                .st-emotion-cache-sh2krr,
                [data-testid="stExpander"] p,
                [data-testid="stExpander"] span {
                    color: #ffffff !important;
                    font-weight: 600 !important;
                }
                div[data-testid="stExpander"] [data-testid="stExpanderToggleIcon"] {
                    color: #D4AF37 !important;
                }
                div[data-testid="stExpander"] summary {
                    color: #ffffff !important;
                    font-weight: 700 !important;
                    font-size: 1.15rem !important;
                    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5) !important;
                }
                div[data-testid="stExpander"] > div:first-child p {
                    color: #ffffff !important;
                    font-weight: 700 !important;
                    font-size: 1.15rem !important;
                }
                /* User Info Text */
                div[data-testid="stExpander"] .stMarkdown p {
                    color: #ffffff !important;
                    font-size: 1rem !important;
                    line-height: 1.9 !important;
                }
                div[data-testid="stExpander"] .stMarkdown strong {
                    color: #4facfe !important;
                    font-weight: 700 !important;
                }
                /* Selectbox in User Management */
                div[data-testid="stExpander"] div[data-testid="stSelectbox"] > div > div {
                    background: linear-gradient(135deg, #0E1117 0%, #161B22 100%) !important;
                    border: 2px solid #4facfe !important;
                    color: #ffffff !important;
                }
                /* Buttons Styling */
                div[data-testid="stExpander"] button[kind="primary"] {
                    background: linear-gradient(135deg, #D4AF37 0%, #d4a017 100%) !important;
                    color: #0E1117 !important;
                    font-weight: 700 !important;
                    border: none !important;
                }
                div[data-testid="stExpander"] button[kind="secondary"] {
                    background: linear-gradient(135deg, #2a2a4e 0%, #0E1117 100%) !important;
                    border: 2px solid rgba(255, 255, 255, 0.4) !important;
                    color: #ffffff !important;
                }
                div[data-testid="stExpander"] button[kind="secondary"]:hover {
                    border-color: #D4AF37 !important;
                    background: linear-gradient(135deg, #3a3a5e 0%, #2a2a4e 100%) !important;
                }
            </style>
            """, unsafe_allow_html=True)
            
            st.subheader(f"👥 {t('admin.users')}")
            
            users = db.get_all_users()
            
            if users:
                for admin_user in users:
                    user_label = f"👤 {admin_user.get('username', 'مستخدم')} - {admin_user.get('email', '')}"
                    with st.expander(user_label, expanded=False):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**{t('admin.username')}:** {admin_user.get('username')}")
                            st.write(f"**{t('admin.email')}:** {admin_user.get('email')}")
                            st.write(f"**{t('admin.role')}:** {admin_user.get('role', 'user')}")
                        
                        with col2:
                            st.write(f"**{t('admin.registration_date')}:** {str(admin_user.get('created_at', ''))[:10]}")
                            st.write(f"**{t('admin.last_login')}:** {str(admin_user.get('last_login', ''))[:19]}")
                            status = f"{t('admin.active')} ✅" if admin_user.get('is_active') else f"{t('admin.inactive')} ❌"
                            st.write(f"**{t('admin.status')}:** {status}")
                        
                        st.markdown("---")
                        
                        # Show success message if role was just saved
                        if st.session_state.get(f"role_saved_{admin_user.get('id')}"):
                            st.success(f"✅ {t('messages.success')} - {t('admin.save_role')}")
                            st.session_state[f"role_saved_{admin_user.get('id')}"] = False
                        
                        # Professional 2x2 Button Grid Layout
                        st.markdown("""
                        <style>
                            .user-actions-grid { margin-top: 15px; }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        # Row 1: Role Selection + Save Button
                        row1_col1, row1_col2 = st.columns([3, 2])
                        with row1_col1:
                            new_role = st.selectbox(
                                t('admin.role'),
                                ["user", "admin"],
                                index=0 if admin_user.get('role') == 'user' else 1,
                                key=f"role_{admin_user.get('id')}",
                                label_visibility="collapsed"
                            )
                        with row1_col2:
                            if st.button(f"💾 {t('admin.save_role')}", key=f"save_role_{admin_user.get('id')}", type="primary", use_container_width=True):
                                db.update_user(admin_user.get('id'), role=new_role)
                                st.session_state[f"role_saved_{admin_user.get('id')}"] = True
                                st.rerun()
                        
                        # Row 2: Enable/Disable + Delete (evenly spaced)
                        st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
                        row2_col1, row2_col2 = st.columns(2)
                        
                        with row2_col1:
                            if admin_user.get('is_active'):
                                if st.button(f"🚫 {t('admin.disable_account')}", key=f"disable_{admin_user.get('id')}", type="secondary", use_container_width=True):
                                    db.update_user(admin_user.get('id'), is_active=0)
                                    st.rerun()
                            else:
                                if st.button(f"✅ {t('admin.enable_account')}", key=f"enable_{admin_user.get('id')}", type="primary", use_container_width=True):
                                    db.update_user(admin_user.get('id'), is_active=1)
                                    st.rerun()
                        
                        # تغيير كلمة المرور
                        st.markdown("---")
                        with st.expander(f"🔐 {t('admin.change_password')}"):
                            new_password = st.text_input(
                                t('admin.new_password'),
                                type="password",
                                key=f"new_pass_{admin_user.get('id')}"
                            )
                            confirm_password = st.text_input(
                                t('admin.confirm_password'),
                                type="password",
                                key=f"confirm_pass_{admin_user.get('id')}"
                            )
                            if st.button(f"💾 {t('admin.save_password')}", key=f"save_pass_{admin_user.get('id')}"):
                                if new_password and confirm_password:
                                    if new_password == confirm_password:
                                        from auth import AuthManager
                                        auth = AuthManager()
                                        hashed = auth.hash_password(new_password)
                                        db.update_user(admin_user.get('id'), password_hash=hashed)
                                        st.success(f"✅ {t('messages.success')}")
                                    else:
                                        st.error(f"❌ {t('admin.passwords_not_match')}")
                                else:
                                    st.error(f"❌ {t('admin.enter_password')}")
            else:
                st.info(t('admin.no_users'))
                
        elif admin_menu == t('admin.financial_settings'):
            st.subheader(f"💰 {t('admin.interest_rates')}")
            
            current_rates = db.get_setting('interest_rates', {
                '3_months': 0.0,
                '12_months': 0.12,
                '24_months': 0.18,
                'default': 0.10
            })
            
            st.info(t('admin.financial_info_msg'))
            
            with st.form("interest_rates_form"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    rate_3 = st.number_input(t('admin.interest_3_months'), 
                                           min_value=0.0, max_value=1.0, step=0.01, 
                                           value=float(current_rates.get('3_months', 0.0)),
                                           format="%.2f")
                    st.caption(f"{t('admin.percentage')}: {rate_3*100:.1f}%")

                with col2:
                    rate_12 = st.number_input(t('admin.interest_12_months'), 
                                            min_value=0.0, max_value=1.0, step=0.01,
                                            value=float(current_rates.get('12_months', 0.12)),
                                            format="%.2f")
                    st.caption(f"{t('admin.percentage')}: {rate_12*100:.1f}%")

                with col3:
                    rate_24 = st.number_input(t('admin.interest_24_months'), 
                                            min_value=0.0, max_value=1.0, step=0.01,
                                            value=float(current_rates.get('24_months', 0.18)),
                                            format="%.2f")
                    st.caption(f"{t('admin.percentage')}: {rate_24*100:.1f}%")
                    
                submitted = st.form_submit_button(f"💾 {t('admin.save_financial_settings')}")
                
                if submitted:
                    new_settings = {
                        '3_months': rate_3,
                        '12_months': rate_12,
                        '24_months': rate_24,
                        'default': 0.10
                    }
                    db.set_setting('interest_rates', new_settings)
                    st.success(f"✅ {t('messages.success')}")
            
            # === قسم نسبة ربح الشركة ===
            st.markdown("---")
            st.subheader(f"💰 {t('admin.company_profit_margin')}")
            st.info(t('admin.profit_margin_info'))
            
            # جلب القيمة الحالية
            current_margin = db.get_setting('company_profit_margin', 0.20)
            
            # حقل الإدخال مع التحقق
            new_margin = st.number_input(
                t('admin.profit_percentage'),
                min_value=0.15,
                max_value=0.30,
                value=float(current_margin),
                step=0.01,
                format="%.2f",
                key="profit_margin_input"
            )
            st.caption(f"{t('admin.current_percentage')}: {new_margin*100:.1f}%")
            
            # عرض تحذير إذا كانت القيمة خارج النطاق
            if new_margin < 0.15 or new_margin > 0.30:
                st.error(t('admin.profit_margin_error'))
            
            # زر الحفظ مع تأكيد كلمة المرور
            if abs(new_margin - float(current_margin)) > 0.001:
                st.warning(t('admin.password_required_to_save'))
                confirm_password = st.text_input(
                    t('admin.enter_password'), 
                    type="password", 
                    key="profit_margin_password"
                )
                
                if st.button(f"💾 {t('admin.save_profit_margin')}", type="primary", key="save_profit_btn"):
                    if not confirm_password:
                        st.error(t('admin.password_required'))
                    elif 0.15 <= new_margin <= 0.30:
                        # التحقق من كلمة المرور
                        from auth import AuthManager
                        auth = AuthManager()
                        user = auth.get_current_user()
                        user_data = db.get_user_by_username(user['username'])
                        
                        if user_data and auth.check_password(confirm_password, user_data['password_hash']):
                            db.set_setting('company_profit_margin', new_margin)
                            st.success(f"✅ {t('admin.profit_margin_saved')}")
                            st.rerun()
                        else:
                            st.error(t('admin.wrong_password'))
                    else:
                        st.error(t('admin.profit_margin_error'))

        # === قسم تقارير الأرباح ===
        elif admin_menu == t('admin.profit_reports'):
            st.subheader(f"📊 {t('admin.profit_reports')}")
            
            # اختيار السنة
            available_years = db.get_available_years()
            from datetime import datetime
            current_year = datetime.now().year
            
            selected_year = st.selectbox(
                t('admin.select_year'),
                available_years,
                index=0 if current_year in available_years else 0
            )
            
            # جلب البيانات
            yearly_data = db.get_yearly_profit(selected_year)
            monthly_data = db.get_monthly_profits(selected_year)
            quarterly_data = db.get_quarterly_profits(selected_year)
            
            # عرض نسبة الربح المستخدمة
            st.info(f"📌 {t('admin.profit_margin_used')}: **{yearly_data['profit_margin']*100:.1f}%**")
            
            # === الملخص السنوي ===
            st.markdown("---")
            st.markdown(f"### 📅 {t('admin.yearly_profits')} - {selected_year}")
            
            yr_col1, yr_col2, yr_col3 = st.columns(3)
            with yr_col1:
                st.metric(t('admin.sales_count'), f"{yearly_data['sales_count']}")
            with yr_col2:
                st.metric(t('admin.total_sales'), f"€{yearly_data['total_sales']:,.2f}")
            with yr_col3:
                st.metric(t('admin.total_profit'), f"€{yearly_data['profit']:,.2f}")
            
            # === الأرباح ربع السنوية ===
            st.markdown("---")
            st.markdown(f"### 📊 {t('admin.quarterly_profits')}")
            
            q_col1, q_col2, q_col3, q_col4 = st.columns(4)
            quarter_names = [t('admin.quarter_1'), t('admin.quarter_2'), t('admin.quarter_3'), t('admin.quarter_4')]
            
            for idx, (col, q_data) in enumerate(zip([q_col1, q_col2, q_col3, q_col4], quarterly_data)):
                with col:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                                padding: 15px; border-radius: 10px; text-align: center; margin: 5px;">
                        <h4 style="color: #D4AF37; margin: 0;">{quarter_names[idx]}</h4>
                        <p style="font-size: 1.8rem; color: #4CAF50; margin: 10px 0;">€{q_data['profit']:,.0f}</p>
                        <p style="color: #888; font-size: 0.8rem;">{t('admin.sales_count')}: {q_data['sales_count']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # === الأرباح الشهرية ===
            st.markdown("---")
            st.markdown(f"### 📈 {t('admin.monthly_profits')}")
            
            # رسم بياني للأرباح الشهرية
            import pandas as pd
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            df = pd.DataFrame({
                'Month': month_names,
                t('admin.total_profit'): [m['profit'] for m in monthly_data],
                t('admin.total_sales'): [m['total_sales'] for m in monthly_data]
            })
            
            st.bar_chart(df.set_index('Month')[[t('admin.total_profit')]])
            
            # جدول الأرباح الشهرية
            with st.expander(f"📋 {t('admin.monthly_profits')} - {t('buttons.details')}"):
                table_data = []
                for m in monthly_data:
                    table_data.append({
                        'Month': month_names[m['month']-1],
                        t('admin.sales_count'): m['sales_count'],
                        t('admin.total_sales'): f"€{m['total_sales']:,.2f}",
                        t('admin.total_profit'): f"€{m['profit']:,.2f}"
                    })
                st.dataframe(pd.DataFrame(table_data), use_container_width=True)

        # ===== قسم إدارة الحضور (Attendance Management) =====
        elif admin_menu == t('admin.attendance'):
            import pandas as pd
            st.subheader(f"⏰ {t('admin.attendance')}")
            
            # التبويبات
            att_tab1, att_tab2, att_tab3, att_tab4 = st.tabs([
                f"📲 {t('admin.check_in')}/{t('admin.check_out')}",
                f"📷 {t('admin.qr_scan')}",
                f"📋 {t('admin.attendance_log')}",
                f"📊 {t('admin.monthly_report')}"
            ])
            
            # === تبويب تسجيل الحضور ===
            with att_tab1:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #0E1117 0%, #1a1a2e 100%); 
                            padding: 20px; border-radius: 15px; border: 2px solid #D4AF37; margin-bottom: 20px;">
                    <h4 style="color: #D4AF37; margin: 0;">📲 {t('admin.check_in')} / {t('admin.check_out')}</h4>
                    <p style="color: #a0a0c0; margin: 5px 0 0 0;">{t('buttons.select')} {t('admin.employees')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # اختيار الموظف
                employees = db.get_all_employees()
                active_employees = [e for e in employees if e.get('is_active')]
                
                if active_employees:
                    emp_options = {f"{e['first_name']} {e.get('last_name', '')} (ID: {e['id']})": e for e in active_employees}
                    selected_emp_name = st.selectbox(f"👤 {t('buttons.select')} {t('admin.employees')}", list(emp_options.keys()))
                    selected_emp = emp_options[selected_emp_name]
                    
                    # عرض حالة الموظف اليوم
                    today_record = db.get_attendance_today(selected_emp['id'])
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if today_record:
                            status_color = "#27ae60" if today_record.get('status') == 'complete' else "#f39c12"
                            status_text = t('admin.complete') if today_record.get('status') == 'complete' else t('admin.incomplete')
                            st.markdown(f"""
                            <div style="background: #1a1a2e; padding: 15px; border-radius: 10px; border-left: 4px solid {status_color};">
                                <h5 style="color: {status_color}; margin: 0;">{t('admin.attendance_status')}</h5>
                                <p style="color: white;">🕒 {t('admin.check_in')}: {today_record.get('check_in', 'N/A')[:16] if today_record.get('check_in') else '-'}</p>
                                <p style="color: white;">🕕 {t('admin.check_out')}: {today_record.get('check_out', 'N/A')[:16] if today_record.get('check_out') else '-'}</p>
                                <p style="color: #D4AF37;">⏱️ {t('admin.worked_hours')}: {today_record.get('net_worked_hours', 0):.2f}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.info(t('admin.no_check_in_found'))
                    
                    with col2:
                        # أزرار الحضور/الانصراف
                        st.markdown(f"### {t('buttons.actions')}")
                        
                        btn_col1, btn_col2 = st.columns(2)
                        
                        with btn_col1:
                            if st.button(f"✅ {t('admin.check_in')}", type="primary", use_container_width=True):
                                result = db.record_check_in(selected_emp['id'])
                                if result['success']:
                                    st.success(f"✅ {t('admin.check_in_recorded')} - {result['time']}")
                                    st.rerun()
                                else:
                                    st.warning(f"⚠️ {t('admin.already_checked_in')}")
                        
                        with btn_col2:
                            if st.button(f"🚪 {t('admin.check_out')}", type="secondary", use_container_width=True):
                                result = db.record_check_out(selected_emp['id'])
                                if result['success']:
                                    adj = result.get('adjustment', {})
                                    msg = f"✅ {t('admin.check_out_recorded')}\n"
                                    msg += f"⏱️ {t('admin.worked_hours')}: {result['net_worked_hours']:.2f}\n"
                                    if adj.get('type') == 'overtime':
                                        msg += f"💰 {t('admin.overtime')}: +{adj['hours']:.1f}h (+€{adj['amount']:.2f})"
                                    elif adj.get('type') == 'deduction':
                                        msg += f"⚠️ {t('admin.deduction')}: -{adj['hours']:.1f}h (-€{adj['amount']:.2f})"
                                    st.success(msg)
                                    st.rerun()
                                else:
                                    st.error(f"❌ {t('admin.no_check_in_found')}")
                        
                        # زر توليد QR
                        if st.button(f"🔲 {t('admin.generate_qr')}", use_container_width=True):
                            qr_token = selected_emp.get('qr_token')
                            if not qr_token:
                                qr_token = db.generate_employee_qr_token(selected_emp['id'])
                            
                            # إنشاء صورة QR Code
                            import qrcode
                            from io import BytesIO
                            
                            qr = qrcode.QRCode(version=1, box_size=10, border=4)
                            qr.add_data(qr_token)
                            qr.make(fit=True)
                            qr_img = qr.make_image(fill_color="black", back_color="white")
                            
                            # تحويل لصيغة يمكن عرضها
                            buffer = BytesIO()
                            qr_img.save(buffer, format="PNG")
                            buffer.seek(0)
                            
                            # عرض الصورة
                            st.image(buffer, caption=f"{t('admin.qr_code')}: {qr_token}", width=250)
                            st.code(qr_token, language=None)
                else:
                    st.warning(t('admin.no_data'))
            
            # === تبويب سجل الحضور ===
            with att_tab2:
                st.markdown(f"### 📋 {t('admin.attendance_log')}")
                
                # فلاتر
                filter_col1, filter_col2, filter_col3 = st.columns(3)
                
                with filter_col1:
                    if active_employees:
                        all_text = t('buttons.all') if t('buttons.all') else "All"
                        emp_filter_options = [all_text] + [f"{e['first_name']} {e.get('last_name', '')}" for e in active_employees]
                        selected_emp_filter = st.selectbox(t('admin.employees'), emp_filter_options)
                
                with filter_col2:
                    from datetime import datetime
                    current_year = datetime.now().year
                    selected_year = st.selectbox(t('admin.select_year'), range(current_year, current_year-3, -1))
                
                with filter_col3:
                    month_names = [t(f'months.{i}') if t(f'months.{i}') else str(i) for i in range(1, 13)]
                    current_month = datetime.now().month
                    selected_month = st.selectbox(t('admin.select_month') if t('admin.select_month') else "Month", range(1, 13), index=current_month-1, 
                                                 format_func=lambda x: month_names[x-1])
                
                # جلب البيانات
                all_records = []
                if active_employees:
                    if selected_emp_filter == all_text:
                        for emp in active_employees:
                            records = db.get_monthly_attendance(emp['id'], selected_year, selected_month)
                            for r in records:
                                r['employee_name'] = f"{emp['first_name']} {emp.get('last_name', '')}"
                            all_records.extend(records)
                    else:
                        emp_idx = emp_filter_options.index(selected_emp_filter) - 1
                        emp = active_employees[emp_idx]
                        all_records = db.get_monthly_attendance(emp['id'], selected_year, selected_month)
                        for r in all_records:
                            r['employee_name'] = f"{emp['first_name']} {emp.get('last_name', '')}"
                
                if all_records:
                    # تحويل للجدول
                    table_data = []
                    for r in all_records:
                        status_emoji = "✅" if r.get('status') == 'complete' else "⚠️"
                        table_data.append({
                            t('admin.employees'): r.get('employee_name', 'N/A'),
                            t('fields.date'): r.get('date', 'N/A'),
                            t('admin.check_in'): r.get('check_in', 'N/A')[:16] if r.get('check_in') else '-',
                            t('admin.check_out'): r.get('check_out', 'N/A')[:16] if r.get('check_out') else '-',
                            t('admin.worked_hours'): f"{r.get('net_worked_hours', 0):.2f}",
                            t('admin.attendance_status'): f"{status_emoji} {t('admin.complete') if r.get('status') == 'complete' else t('admin.incomplete')}"
                        })
                    st.dataframe(pd.DataFrame(table_data), use_container_width=True)
                else:
                    st.info(t('admin.no_data'))
            
            # === تبويب التقارير الشهرية ===
            with att_tab3:
                st.markdown(f"### 📊 {t('admin.monthly_report')}")
                
                report_col1, report_col2 = st.columns(2)
                
                with report_col1:
                    from datetime import datetime
                    current_year = datetime.now().year
                    report_year = st.selectbox(t('admin.select_year'), range(current_year, current_year-3, -1), key="report_year")
                
                with report_col2:
                    month_names = [t(f'months.{i}') if t(f'months.{i}') else str(i) for i in range(1, 13)]
                    current_month = datetime.now().month
                    report_month = st.selectbox(t('admin.select_month') if t('admin.select_month') else "Month", range(1, 13), index=current_month-1,
                                               format_func=lambda x: month_names[x-1], key="report_month")
                
                if active_employees:
                    # ملخص لكل موظف
                    summary_data = []
                    for emp in active_employees:
                        adjustments = db.get_monthly_adjustments(emp['id'], report_year, report_month)
                        attendance = db.get_monthly_attendance(emp['id'], report_year, report_month)
                        total_days = len(attendance)
                        complete_days = len([a for a in attendance if a.get('status') == 'complete'])
                        
                        summary_data.append({
                            t('admin.employees'): f"{emp['first_name']} {emp.get('last_name', '')}",
                            t('fields.working_days') if t('fields.working_days') else "Work Days": total_days,
                            t('admin.complete'): complete_days,
                            t('admin.overtime'): f"{adjustments['overtime_hours']:.1f}h",
                            f"{t('admin.overtime')} €": f"€{adjustments['overtime_amount']:.2f}",
                            t('admin.deduction'): f"{adjustments['deduction_hours']:.1f}h",
                            f"{t('admin.deduction')} €": f"€{adjustments['deduction_amount']:.2f}",
                            "Net €": f"€{adjustments['net_adjustment']:.2f}"
                        })
                    
                    st.dataframe(pd.DataFrame(summary_data), use_container_width=True)
                    
                    # ملخص إجمالي
                    total_overtime = sum(db.get_monthly_adjustments(e['id'], report_year, report_month)['overtime_amount'] for e in active_employees)
                    total_deductions = sum(db.get_monthly_adjustments(e['id'], report_year, report_month)['deduction_amount'] for e in active_employees)
                    
                    summary_col1, summary_col2, summary_col3 = st.columns(3)
                    with summary_col1:
                        st.metric(f"💰 {t('admin.overtime')}", f"€{total_overtime:.2f}")
                    with summary_col2:
                        st.metric(f"📉 {t('admin.deduction')}", f"€{total_deductions:.2f}")
                    with summary_col3:
                        st.metric(f"📊 Net", f"€{total_overtime - total_deductions:.2f}")
            
            # === تبويب مسح QR Code ===
            with att_tab4:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #0E1117 0%, #1a1a2e 100%); 
                            padding: 20px; border-radius: 15px; border: 2px solid #27ae60; margin-bottom: 20px;">
                    <h4 style="color: #27ae60; margin: 0;">📷 {t('admin.qr_scan')}</h4>
                    <p style="color: #a0a0c0; margin: 5px 0 0 0;">{t('admin.qr_scan_desc') if t('admin.qr_scan_desc') else 'Scan employee QR code for quick check-in/out'}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # اختيار طريقة الإدخال - عنوان مرئي
                st.markdown(f"""
                <p style="color: #D4AF37; font-size: 1.1rem; font-weight: bold; margin-bottom: 10px;">
                    📋 {t('admin.select_method') if t('admin.select_method') else 'Select Method'}
                </p>
                """, unsafe_allow_html=True)
                
                input_method = st.radio(
                    "",  # العنوان فارغ لأننا أضفناه أعلاه
                    [f"📷 {t('admin.camera') if t('admin.camera') else 'Camera'}", 
                     f"📁 {t('admin.upload_image') if t('admin.upload_image') else 'Upload Image'}",
                     f"⌨️ {t('admin.manual_code') if t('admin.manual_code') else 'Manual Code'}"],
                    horizontal=True,
                    label_visibility="collapsed"
                )
                
                qr_code_value = None
                
                if "Camera" in input_method or "الكاميرا" in input_method:
                    # استخدام كاميرا المتصفح - تصغير الحجم
                    cam_col1, cam_col2, cam_col3 = st.columns([3, 2, 3])  # 25% في الوسط
                    with cam_col2:
                        captured_image = st.camera_input(t('admin.capture_qr') if t('admin.capture_qr') else "📸 QR")
                    
                    if captured_image:
                        try:
                            from PIL import Image
                            import cv2
                            import numpy as np
                            from pyzbar.pyzbar import decode
                            
                            # تحويل الصورة
                            img = Image.open(captured_image)
                            img_array = np.array(img)
                            
                            # البحث عن QR في الصورة
                            decoded_objects = decode(img_array)
                            
                            if decoded_objects:
                                qr_code_value = decoded_objects[0].data.decode('utf-8')
                                st.success(f"✅ {t('admin.qr_detected') if t('admin.qr_detected') else 'QR Detected'}: {qr_code_value}")
                            else:
                                st.warning(t('admin.no_qr_found') if t('admin.no_qr_found') else "⚠️ No QR code found in image")
                        except ImportError:
                            st.error("❌ Please install: pip install opencv-python pyzbar")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                
                elif "Upload" in input_method or "رفع" in input_method:
                    # رفع صورة QR
                    uploaded_file = st.file_uploader(
                        t('admin.upload_qr_image') if t('admin.upload_qr_image') else "Upload QR Code Image",
                        type=['png', 'jpg', 'jpeg']
                    )
                    
                    if uploaded_file:
                        try:
                            from PIL import Image
                            import cv2
                            import numpy as np
                            from pyzbar.pyzbar import decode
                            
                            img = Image.open(uploaded_file)
                            img_array = np.array(img)
                            
                            decoded_objects = decode(img_array)
                            
                            if decoded_objects:
                                qr_code_value = decoded_objects[0].data.decode('utf-8')
                                st.success(f"✅ {t('admin.qr_detected') if t('admin.qr_detected') else 'QR Detected'}: {qr_code_value}")
                            else:
                                st.warning(t('admin.no_qr_found') if t('admin.no_qr_found') else "⚠️ No QR code found in image")
                        except ImportError:
                            st.error("❌ Please install: pip install opencv-python pyzbar")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                
                else:
                    # إدخال الكود يدوياً
                    qr_code_value = st.text_input(
                        t('admin.enter_qr_code') if t('admin.enter_qr_code') else "Enter QR Code",
                        placeholder="e.g. 0FD0E0E221015BE8"
                    )
                
                # معالجة الكود
                if qr_code_value:
                    emp = db.get_employee_by_qr_token(qr_code_value.strip().upper())
                    
                    if emp:
                        st.markdown(f"""
                        <div style="background: #1a1a2e; padding: 20px; border-radius: 10px; border-left: 4px solid #D4AF37; margin: 20px 0;">
                            <h4 style="color: #D4AF37; margin: 0;">👤 {emp['first_name']} {emp.get('last_name', '')}</h4>
                            <p style="color: white;">{t('admin.employees')} ID: {emp['id']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # عرض حالة اليوم
                        today_record = db.get_attendance_today(emp['id'])
                        
                        qr_col1, qr_col2 = st.columns(2)
                        
                        with qr_col1:
                            if st.button(f"✅ {t('admin.check_in')}", type="primary", use_container_width=True, key="qr_checkin"):
                                result = db.record_check_in(emp['id'])
                                if result['success']:
                                    st.success(f"✅ {t('admin.check_in_recorded')} - {result['time']}")
                                    st.balloons()
                                else:
                                    st.warning(f"⚠️ {t('admin.already_checked_in')}")
                        
                        with qr_col2:
                            if st.button(f"🚪 {t('admin.check_out')}", type="secondary", use_container_width=True, key="qr_checkout"):
                                result = db.record_check_out(emp['id'])
                                if result['success']:
                                    adj = result.get('adjustment', {})
                                    msg = f"✅ {t('admin.check_out_recorded')}\n"
                                    msg += f"⏱️ {t('admin.worked_hours')}: {result['net_worked_hours']:.2f}h"
                                    if adj.get('type') == 'overtime':
                                        msg += f"\n💰 +€{adj['amount']:.2f}"
                                    elif adj.get('type') == 'deduction':
                                        msg += f"\n⚠️ -€{adj['amount']:.2f}"
                                    st.success(msg)
                                else:
                                    st.error(f"❌ {t('admin.no_check_in_found')}")
                        
                        # عرض الحالة الحالية
                        if today_record:
                            status_color = "#27ae60" if today_record.get('status') == 'complete' else "#f39c12"
                            st.markdown(f"""
                            <div style="background: #1a1a2e; padding: 15px; border-radius: 10px; border-left: 4px solid {status_color}; margin-top: 20px;">
                                <p style="color: white;">🕒 {t('admin.check_in')}: {today_record.get('check_in', '-')[:16] if today_record.get('check_in') else '-'}</p>
                                <p style="color: white;">🕕 {t('admin.check_out')}: {today_record.get('check_out', '-')[:16] if today_record.get('check_out') else '-'}</p>
                                <p style="color: #D4AF37;">⏱️ {t('admin.worked_hours')}: {today_record.get('net_worked_hours', 0):.2f}h</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.error(t('admin.invalid_qr') if t('admin.invalid_qr') else "❌ Invalid QR Code - Employee not found")

        elif admin_menu == t('admin.employees'):
            st.subheader(f"👔 {t('admin.employees')}")
            
            # === قسم إدارة فريق العمل (الأدمنز) ===
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0E1117 0%, #161B22 100%); 
                        padding: 15px 25px; border-radius: 15px; margin: 20px 0; border: 2px solid #D4AF37;">
                <h4 style="color: #D4AF37; margin: 0;">👑 {t('admin.team_management_title')}</h4>
                <p style="color: #a0a0c0; font-size: 0.9rem; margin: 5px 0 0 0;">{t('admin.team_management_desc')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # جلب جميع الآدمنز من جدول الموظفين (بناءً على job_title)
            all_employees = db.get_all_employees()
            admin_titles = ['Admin', 'Administrator', 'مدير النظام', 'Systemadministrator', 'آدمن', 'مدير']
            all_admins = [e for e in all_employees if e.get('job_title') in admin_titles]
            
            if all_admins:
                admin_options = {f"👤 {e.get('first_name', '')} {e.get('last_name', '')} ({e.get('email')})": e for e in all_admins}
                
                # Radio buttons لاختيار الأدمن (أفقي)
                st.subheader(f"👥 {t('admin.select_team_member')}:")
                selected_admin_key = st.radio(
                    label="",
                    options=list(admin_options.keys()),
                    key="admin_staff_radio",
                    label_visibility="collapsed",
                    horizontal=True
                )
                
                selected_admin = admin_options.get(selected_admin_key)
                
                if selected_admin:
                    admin_tab1, admin_tab2 = rtl_tabs([f"📋 {t('admin.personal_data_tab')}", f"💼 {t('admin.job_data_tab')}"])
                    
                    with admin_tab1:
                        st.markdown("""
                        <style>
                            .data-header-white { color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-size: 1.5em !important; font-weight: bold !important; }
                        </style>
                        """, unsafe_allow_html=True)
                        st.markdown(f"""
                        <div style='margin: 10px 0;'>
                            <span class='data-header-white'>
                                📋 {t('admin.data_of')}: {selected_admin.get('first_name', '')} {selected_admin.get('last_name', '')}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.form(f"edit_admin_personal_{selected_admin['id']}"):
                            # الصف الأول: الاسم الكامل + البريد الإلكتروني
                            p_row1_col1, p_row1_col2 = st.columns(2)
                            with p_row1_col1:
                                admin_fullname = st.text_input(t('admin.full_name'), value=f"{selected_admin.get('first_name', '')} {selected_admin.get('last_name', '')}".strip(), key=f"ap_name_{selected_admin['id']}")
                            with p_row1_col2:
                                admin_email = st.text_input(t('admin.email'), value=selected_admin.get('email', ''), key=f"ap_email_{selected_admin['id']}")
                            
                            # الصف الثاني: الجنسية + تاريخ الميلاد
                            p_row2_col1, p_row2_col2 = st.columns(2)
                            with p_row2_col1:
                                admin_nationality = st.text_input(t('profile.nationality'), value=selected_admin.get('nationality', ''), key=f"ap_nat_{selected_admin['id']}")
                            with p_row2_col2:
                                admin_dob = st.text_input(t('admin.date_of_birth'), value=selected_admin.get('date_of_birth', ''), key=f"ap_dob_{selected_admin['id']}")
                            
                            # الصف الثالث: رقم الهوية + رقم الرخصة
                            p_row3_col1, p_row3_col2 = st.columns(2)
                            with p_row3_col1:
                                admin_id_number = st.text_input(t('admin.id_number'), value=selected_admin.get('id_number', ''), key=f"ap_id_{selected_admin['id']}")
                            with p_row3_col2:
                                admin_license = st.text_input(t('admin.license_number'), value=selected_admin.get('license_number', ''), key=f"ap_lic_{selected_admin['id']}")
                            
                            # الصف الرابع: الهاتف + العنوان
                            p_row4_col1, p_row4_col2 = st.columns(2)
                            with p_row4_col1:
                                admin_phone = st.text_input(t('admin.phone'), value=selected_admin.get('phone', ''), key=f"ap_phone_{selected_admin['id']}")
                            with p_row4_col2:
                                admin_address = st.text_input(t('admin.address'), value=selected_admin.get('address', ''), key=f"ap_addr_{selected_admin['id']}")
                            
                            if st.form_submit_button(f"💾 {t('admin.save_personal_data')}", type="primary"):
                                # تحديث بيانات الموظف
                                name_parts = admin_fullname.split(' ', 1)
                                first_name = name_parts[0] if name_parts else ''
                                last_name = name_parts[1] if len(name_parts) > 1 else ''
                                db.update_employee(selected_admin['id'],
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=admin_email,
                                    phone=admin_phone,
                                    address=admin_address
                                )
                                st.success(f"✅ {t('admin.personal_data_saved')}")
                                st.rerun()
                    
                    with admin_tab2:
                        st.markdown(f"""
                        <div style='margin: 10px 0;'>
                            <span class='data-header-white'>
                                💼 {t('admin.job_data_of')}: {selected_admin.get('first_name', '')} {selected_admin.get('last_name', '')}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # selected_admin هو نفسه سجل الموظف
                        emp_data = selected_admin
                        
                        # اختيار الدور (آدمن / موظف عادي) خارج الفورم للحفظ المباشر
                        role_options = [t('admin.admin_role'), t('admin.employee_role')]
                        current_role = emp_data.get('job_title', 'Admin')
                        # تحديد الفهرس الحالي
                        if current_role in ['Admin', 'Administrator', 'آدمن', 'مدير', 'Systemadministrator']:
                            default_index = 0
                        else:
                            default_index = 1
                        
                        selected_role = st.selectbox(
                            t('admin.job_title'),
                            options=role_options,
                            index=default_index,
                            key=f"role_select_{selected_admin['id']}"
                        )
                        
                        # تحويل الاختيار للقيمة المحفوظة
                        job_title_value = 'Admin' if selected_role == role_options[0] else t('admin.employee_role')
                        
                        # حفظ تلقائي إذا تغير الدور
                        if job_title_value != current_role:
                            if emp_data.get('id'):
                                db.update_employee(emp_data['id'], job_title=job_title_value)
                            else:
                                # إنشاء سجل موظف جديد
                                db.create_employee(
                                    first_name=selected_admin.get('full_name', '').split()[0] if selected_admin.get('full_name') else selected_admin.get('username'),
                                    last_name=' '.join(selected_admin.get('full_name', '').split()[1:]) if selected_admin.get('full_name') else '',
                                    phone=selected_admin.get('phone', ''),
                                    email=selected_admin.get('email', ''),
                                    user_id=selected_admin['id'],
                                    job_title=job_title_value
                                )
                            st.success(f"✅ {t('admin.role_updated')}")
                            st.rerun()
                        
                        with st.form(f"edit_admin_job_{selected_admin['id']}"):
                            j_col1, j_col2, j_col3, j_col4 = st.columns(4)
                            
                            with j_col1:
                                job_salary = st.number_input(f"{t('admin.monthly_salary')} (€)", value=float(emp_data.get('monthly_salary', 0)), key=f"aj_sal_{selected_admin['id']}")
                            
                            with j_col2:
                                job_annual_leave = st.number_input(t('admin.annual_leave'), value=int(emp_data.get('annual_leave', 0)), key=f"aj_annual_{selected_admin['id']}")
                            
                            with j_col3:
                                job_hire_date = st.text_input(t('admin.hire_date'), value=emp_data.get('hire_date', ''), key=f"aj_hire_{selected_admin['id']}")
                            
                            with j_col4:
                                job_special_leave = st.number_input(t('admin.special_leave'), value=int(emp_data.get('special_leave', 0)), key=f"aj_special_{selected_admin['id']}")
                            
                            job_notes = st.text_area(t('admin.notes'), value=emp_data.get('notes', ''), key=f"aj_notes_{selected_admin['id']}")
                            
                            if st.form_submit_button(f"💾 {t('admin.save_job_data')}", type="primary"):
                                # حفظ أو تحديث بيانات الموظف
                                if emp_data.get('id'):
                                    db.update_employee(emp_data['id'],
                                        job_title=job_title_value,
                                        monthly_salary=job_salary,
                                        hire_date=job_hire_date,
                                        annual_leave=job_annual_leave,
                                        special_leave=job_special_leave,
                                        notes=job_notes
                                    )
                                else:
                                    # إنشاء سجل موظف جديد مرتبط بالمستخدم
                                    db.create_employee(
                                        first_name=selected_admin.get('full_name', '').split()[0] if selected_admin.get('full_name') else selected_admin.get('username'),
                                        last_name=' '.join(selected_admin.get('full_name', '').split()[1:]) if selected_admin.get('full_name') else '',
                                        phone=selected_admin.get('phone', ''),
                                        email=selected_admin.get('email', ''),
                                        monthly_salary=job_salary,
                                        annual_leave=job_annual_leave,
                                        special_leave=job_special_leave,
                                        user_id=selected_admin['id'],
                                        job_title=job_title,
                                        hire_date=job_hire_date,
                                        notes=job_notes
                                    )
                                st.success(f"✅ {t('admin.job_data_saved')}")
                                st.rerun()
                        
                        # === قسم إدارة الإجازات المرضية للآدمن ===
                        st.markdown("---")
                        st.markdown(f"""
                        <div style='margin: 10px 0;'>
                            <span class='data-header-white'>🏥 {t('admin.sick_leave_records')}</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # نسبة التأمين الصحي
                        health_rate = db.get_setting('health_insurance_rate', 70)
                        st.markdown(f"<p style='color: #888;'>ℹ️ {t('admin.special_leave_info')} {health_rate}%</p>", unsafe_allow_html=True)
                        
                        # حساب مجموع الإجازات المرضية
                        admin_total_sick = db.get_total_sick_leave_days(user_id=selected_admin['id'])
                        st.markdown(f"<h2 style='color: #FFD700;'>{t('admin.total_sick_days')}: {admin_total_sick} 📊</h2>", unsafe_allow_html=True)
                        
                        # نموذج إضافة إجازة مرضية جديدة
                        with st.expander(f"➕ {t('admin.add_sick_leave')}", expanded=False):
                            from datetime import date
                            admin_sick_col1, admin_sick_col2, admin_sick_col3 = st.columns(3)
                            with admin_sick_col1:
                                admin_sick_start = st.date_input(
                                    t('admin.start_date'), 
                                    value=date.today(),
                                    key=f"admin_sick_start_{selected_admin['id']}"
                                )
                            with admin_sick_col2:
                                admin_sick_end = st.date_input(
                                    t('admin.end_date'), 
                                    value=date.today(),
                                    key=f"admin_sick_end_{selected_admin['id']}"
                                )
                            
                            # حساب عدد الأيام تلقائياً
                            if admin_sick_end >= admin_sick_start:
                                admin_auto_days = (admin_sick_end - admin_sick_start).days + 1
                            else:
                                admin_auto_days = 1
                            
                            with admin_sick_col3:
                                st.markdown(f"<br>", unsafe_allow_html=True)
                                st.info(f"📊 {t('admin.days_count')}: **{admin_auto_days}**")
                            
                            admin_sick_reason = st.text_input(
                                t('admin.reason'), 
                                key=f"admin_sick_reason_{selected_admin['id']}"
                            )
                            
                            if st.button(f"💾 {t('admin.add_sick_leave')}", key=f"add_admin_sick_{selected_admin['id']}", type="primary"):
                                db.add_sick_leave_record(
                                    user_id=selected_admin['id'],
                                    employee_id=emp_data.get('id'),
                                    start_date=str(admin_sick_start),
                                    end_date=str(admin_sick_end),
                                    days_count=admin_auto_days,
                                    reason=admin_sick_reason
                                )
                                st.success(f"✅ {t('messages.success')}")
                                st.rerun()
                        
                        # عرض سجلات الإجازات المرضية
                        admin_sick_records = db.get_sick_leave_records(user_id=selected_admin['id'])
                        if admin_sick_records:
                            for rec in admin_sick_records:
                                with st.container():
                                    rec_col1, rec_col2 = st.columns([5, 1])
                                    with rec_col1:
                                        st.markdown(f"""
                                        <p style='color: #FFFFFF; margin: 0;'>
                                        <b>📅 {t('admin.start_date')}:</b> {rec.get('start_date')} → <b>{t('admin.end_date')}:</b> {rec.get('end_date')}<br>
                                        <b>🔢 {t('admin.days_count')}:</b> {rec.get('days_count')}
                                        </p>
                                        """, unsafe_allow_html=True)
                                        if rec.get('reason'):
                                            st.markdown(f"<p style='color: #888; font-size: 0.9em;'>📝 {rec.get('reason')}</p>", unsafe_allow_html=True)
                                    with rec_col2:
                                        if st.button("🗑️", key=f"del_admin_sick_{rec.get('id')}", help=t('admin.delete_record')):
                                            db.delete_sick_leave_record(rec.get('id'))
                                            st.rerun()
                                    st.markdown("---")
                        else:
                            st.markdown(f"<div style='background: rgba(30,60,114,0.8); padding: 10px; border-radius: 5px; border-left: 4px solid #64B4FF;'><span style='color: #FFFFFF;'>ℹ️ {t('admin.no_sick_records')}</span></div>", unsafe_allow_html=True)
            else:
                st.info(f"👑 {t('admin.team_management_title')}")
            
            st.markdown("---")
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0E1117 0%, #161B22 100%); 
                        padding: 15px 25px; border-radius: 15px; margin: 20px 0; border: 2px solid #4a9eff;">
                <h4 style="color: #4a9eff; margin: 0;">👔 {t('admin.regular_employees')}</h4>
                <p style="color: #a0a0c0; font-size: 0.9rem; margin: 5px 0 0 0;">{t('admin.team_management_desc')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # نموذج إضافة موظف جديد
            with st.expander(f"➕ {t('admin.add_employee')}", expanded=False):
                with st.form("add_employee_form_home"):
                    st.markdown(f"**{t('profile.personal_info')}**")
                    # المعلومات الشخصية في 4 أعمدة
                    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
                    with p_col1:
                        emp_first_name = st.text_input(f"{t('admin.first_name')} *", key="new_emp_first_h")
                    with p_col2:
                        emp_last_name = st.text_input(t('admin.last_name'), key="new_emp_last_h")
                    with p_col3:
                        emp_phone = st.text_input(t('admin.phone'), key="new_emp_phone_h")
                    with p_col4:
                        emp_email = st.text_input(t('admin.email'), key="new_emp_email_h")
                    
                    emp_address = st.text_input(t('admin.address'), key="new_emp_address_h")
                    
                    st.markdown("---")
                    st.markdown(f"**{t('admin.financial_settings')}**")
                    # الإعدادات المالية في 6 أعمدة
                    f_col1, f_col2, f_col3, f_col4, f_col5, f_col6 = st.columns(6)
                    with f_col1:
                        emp_salary = st.number_input(f"{t('admin.monthly_salary')} (€)", min_value=0.0, key="new_emp_salary_h")
                    with f_col2:
                        emp_annual = st.number_input(t('admin.annual_leave'), min_value=0, key="new_emp_annual_h")
                    with f_col3:
                        emp_sick = st.number_input(t('admin.sick_leave'), min_value=0, key="new_emp_sick_h")
                    with f_col4:
                        emp_unpaid = st.number_input(t('admin.unpaid_leave'), min_value=0, key="new_emp_unpaid_h")
                    with f_col5:
                        emp_feiertags = st.number_input(f"{t('admin.feiertags_geld')} (€)", min_value=0.0, key="new_emp_feiertags_h")
                    with f_col6:
                        emp_urlaub = st.number_input(f"{t('admin.urlaubsgeld')} (€)", min_value=0.0, key="new_emp_urlaub_h")
                    
                    emp_notes = st.text_area(t('admin.notes'), key="new_emp_notes_h")
                    
                    st.markdown("---")
                    # اختيار نوع الموظف (آدمن أو موظف عادي)
                    emp_type = st.selectbox(
                        f"👔 {t('admin.employee_type')}",
                        options=[t('admin.regular_employee'), t('admin.admin_employee')],
                        key="new_emp_type_h"
                    )
                    
                    submitted = st.form_submit_button(f"💾 {t('admin.save_employee')}", type="primary")
                    
                    if submitted:
                        if emp_first_name:
                            # تحديد إذا كان الموظف آدمن
                            is_admin = emp_type == t('admin.admin_employee')
                            
                            # تحديد المسمى الوظيفي بناءً على النوع
                            job_title_value = 'Admin' if is_admin else t('admin.employee_role')
                            
                            # إنشاء سجل الموظف
                            new_emp_id = db.create_employee(
                                first_name=emp_first_name,
                                last_name=emp_last_name,
                                phone=emp_phone,
                                email=emp_email,
                                address=emp_address,
                                monthly_salary=emp_salary,
                                annual_leave=emp_annual,
                                sick_leave=emp_sick,
                                unpaid_leave=emp_unpaid,
                                feiertags_geld=emp_feiertags,
                                urlaubsgeld=emp_urlaub,
                                notes=emp_notes,
                                job_title=job_title_value
                            )
                            
                            # إذا كان آدمن، ننشئ حساب مستخدم له
                            if is_admin and emp_email:
                                import secrets
                                import string
                                # إنشاء كلمة مرور عشوائية مؤقتة
                                temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))
                                
                                # إنشاء اسم مستخدم من الإيميل
                                username = emp_email.split('@')[0]
                                
                                # التحقق من عدم وجود المستخدم
                                existing_user = db.get_user_by_username(username)
                                if not existing_user:
                                    db.create_user(
                                        username=username,
                                        password=temp_password,
                                        full_name=f"{emp_first_name} {emp_last_name}".strip(),
                                        email=emp_email,
                                        role='admin'
                                    )
                                    st.success(f"✅ {t('messages.success')}: {emp_first_name} {emp_last_name}")
                                    st.info(f"🔑 {t('admin.temp_password')}: **{temp_password}**")
                                else:
                                    st.success(f"✅ {t('messages.success')}: {emp_first_name} {emp_last_name}")
                                    st.warning(f"⚠️ {t('admin.user_exists')}: {username}")
                            else:
                                st.success(f"✅ {t('messages.success')}: {emp_first_name} {emp_last_name}")
                            
                            st.rerun()
                        else:
                            st.error(f"❌ {t('messages.required_field')}")
            
            st.markdown("---")
            
            # عرض الموظفين العاديين فقط (استبعاد الآدمنز)
            all_employees = db.get_all_employees()
            # جلب قائمة emails للآدمنز للفلترة
            admin_emails = [u.get('email') for u in db.get_all_users() if u.get('role') == 'admin']
            # فلترة الموظفين لاستبعاد الذين لديهم job_title=Admin أو email مطابق لآدمن
            employees = [e for e in all_employees 
                        if e.get('email') not in admin_emails 
                        and e.get('job_title') not in ['Admin', 'Administrator', 'مدير النظام', 'Systemadministrator']]
            
            if employees:
                # إنشاء قائمة بأسماء الموظفين للاختيار
                emp_options = {}
                for emp in employees:
                    status_icon = "✅" if emp.get('is_active') else "❌"
                    full_name = f"{emp.get('first_name', '')} {emp.get('last_name', '')}".strip()
                    emp_options[f"👤 {full_name} {status_icon}"] = emp
                
                # Radio buttons لاختيار الموظف (أكثر وضوحاً)
                st.markdown(f"**{t('admin.select_employee')}:**")
                selected_emp_name = st.radio(
                    label="",
                    options=list(emp_options.keys()),
                    key="select_employee_radio_home",
                    label_visibility="collapsed",
                    horizontal=True
                )
                
                if selected_emp_name and selected_emp_name in emp_options:
                    emp = emp_options[selected_emp_name]
                    full_name = f"{emp.get('first_name', '')} {emp.get('last_name', '')}".strip()
                    
                    # حساب مجموع الإجازات المرضية من السجلات
                    total_sick_days = db.get_total_sick_leave_days(employee_id=emp.get('id'))
                    
                    # تبويبات البيانات الشخصية والوظيفية (مثل الآدمنز)
                    emp_tab1, emp_tab2 = rtl_tabs([f"📋 {t('admin.personal_data_tab')}", f"💼 {t('admin.job_data_tab')}"])
                    
                    with emp_tab1:
                        # Header للبيانات الشخصية
                        st.markdown("""
                        <style>
                            .emp-data-header-white { color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-size: 1.5em !important; font-weight: bold !important; }
                        </style>
                        """, unsafe_allow_html=True)
                        st.markdown(f"""
                        <div style='margin: 10px 0;'>
                            <span class='emp-data-header-white'>
                                📋 {t('admin.data_of')}: {full_name}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.form(f"edit_emp_personal_{emp.get('id')}"):
                            # الصف الأول: الاسم الأول + البريد الإلكتروني
                            p_row1_col1, p_row1_col2 = st.columns(2)
                            with p_row1_col1:
                                edit_first_name = st.text_input(f"{t('admin.first_name')} *", value=emp.get('first_name', ''), key=f"ep_first_{emp.get('id')}")
                            with p_row1_col2:
                                edit_email = st.text_input(t('admin.email'), value=emp.get('email') or '', key=f"ep_email_{emp.get('id')}")
                            
                            # الصف الثاني: الاسم الأخير + العنوان
                            p_row2_col1, p_row2_col2 = st.columns(2)
                            with p_row2_col1:
                                edit_last_name = st.text_input(t('admin.last_name'), value=emp.get('last_name') or '', key=f"ep_last_{emp.get('id')}")
                            with p_row2_col2:
                                edit_address = st.text_input(t('admin.address'), value=emp.get('address') or '', key=f"ep_addr_{emp.get('id')}")
                            
                            # الصف الثالث: رقم الهاتف
                            edit_phone = st.text_input(t('admin.phone'), value=emp.get('phone') or '', key=f"ep_phone_{emp.get('id')}")
                            
                            if st.form_submit_button(f"💾 {t('admin.save_personal_data')}", type="primary"):
                                if edit_first_name:
                                    db.update_employee(
                                        emp.get('id'),
                                        first_name=edit_first_name,
                                        last_name=edit_last_name,
                                        phone=edit_phone,
                                        email=edit_email,
                                        address=edit_address
                                    )
                                    st.success(f"✅ {t('admin.personal_data_saved')}")
                                    st.rerun()
                                else:
                                    st.error(f"❌ {t('admin.first_name_required')}")
                    
                    with emp_tab2:
                        # Header للبيانات الوظيفية
                        st.markdown(f"""
                        <div style='margin: 10px 0;'>
                            <span class='emp-data-header-white'>
                                💼 {t('admin.job_data_of')}: {full_name}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # اختيار الدور (آدمن / موظف عادي) خارج الفورم للحفظ المباشر
                        role_options = [t('admin.admin_role'), t('admin.employee_role')]
                        current_job_title = emp.get('job_title', '')
                        # تحديد الفهرس الحالي
                        if current_job_title in ['Admin', 'Administrator', 'آدمن', 'مدير', 'Systemadministrator', 'مدير النظام']:
                            default_role_index = 0
                        else:
                            default_role_index = 1
                        
                        selected_role = st.selectbox(
                            t('admin.job_title'),
                            options=role_options,
                            index=default_role_index,
                            key=f"emp_role_select_{emp.get('id')}"
                        )
                        
                        # تحويل الاختيار للقيمة المحفوظة
                        new_job_title = 'Admin' if selected_role == role_options[0] else t('admin.employee_role')
                        
                        # حفظ تلقائي إذا تغير الدور
                        if new_job_title != current_job_title and current_job_title:
                            db.update_employee(emp.get('id'), job_title=new_job_title)
                            st.success(f"✅ {t('admin.role_updated')}")
                            st.rerun()
                        
                        with st.form(f"edit_emp_job_{emp.get('id')}"):
                            j_col1, j_col2, j_col3, j_col4 = st.columns(4)
                            
                            with j_col1:
                                edit_salary = st.number_input(f"{t('admin.monthly_salary')} (€)", value=float(emp.get('monthly_salary', 0)), key=f"ej_sal_{emp.get('id')}")
                            
                            with j_col2:
                                edit_annual = st.number_input(t('admin.annual_leave'), value=int(emp.get('annual_leave') or 0), min_value=0, key=f"ej_ann_{emp.get('id')}")
                            
                            with j_col3:
                                edit_hire_date = st.text_input(t('admin.hire_date'), value=emp.get('hire_date', ''), key=f"ej_hire_{emp.get('id')}")
                            
                            with j_col4:
                                edit_unpaid = st.number_input(t('admin.unpaid_leave'), value=int(emp.get('unpaid_leave') or 0), min_value=0, key=f"ej_unpaid_{emp.get('id')}")
                            
                            edit_notes = st.text_area(f"📝 {t('admin.notes')}", value=emp.get('notes') or '', key=f"ej_notes_{emp.get('id')}")
                            
                            if st.form_submit_button(f"💾 {t('admin.save_job_data')}", type="primary"):
                                db.update_employee(
                                    emp.get('id'),
                                    monthly_salary=edit_salary,
                                    hire_date=edit_hire_date,
                                    annual_leave=edit_annual,
                                    unpaid_leave=edit_unpaid,
                                    notes=edit_notes,
                                    job_title=new_job_title
                                )
                                st.success(f"✅ {t('admin.job_data_saved')}")
                                st.rerun()
                        
                        # === قسم سجلات الإجازات المرضية ===
                        st.markdown("---")
                        st.markdown(f"""
                        <div style='margin: 10px 0;'>
                            <span class='emp-data-header-white'>🏥 {t('admin.sick_leave_records')}</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # عرض مجموع الإجازات المرضية
                        st.markdown(f"<h2 style='color: #FFD700;'>{t('admin.total_sick_days')}: {total_sick_days} 📊</h2>", unsafe_allow_html=True)
                        
                        # معلومات الخصم القانوني مع نسبة التأمين الصحي
                        health_rate = db.get_setting('health_insurance_rate', 70)
                        col_info_rate1, col_info_rate2 = st.columns([3, 1])
                        with col_info_rate1:
                            st.caption(f"ℹ️ {t('admin.special_leave_info')} {health_rate}%")
                        with col_info_rate2:
                            new_rate = st.number_input(
                                t('admin.health_insurance_rate'),
                                min_value=0, max_value=100, value=int(health_rate),
                                key=f"health_rate_{emp.get('id')}",
                                label_visibility="collapsed"
                            )
                            if new_rate != health_rate:
                                db.set_setting('health_insurance_rate', new_rate)
                                st.rerun()
                        
                        # نموذج إضافة إجازة مرضية جديدة
                        with st.expander(f"➕ {t('admin.add_sick_leave')}", expanded=False):
                            from datetime import date, timedelta
                            sick_col1, sick_col2, sick_col3 = st.columns(3)
                            with sick_col1:
                                sick_start = st.date_input(
                                    t('admin.start_date'), 
                                    value=date.today(),
                                    key=f"sick_start_{emp.get('id')}"
                                )
                            with sick_col2:
                                sick_end = st.date_input(
                                    t('admin.end_date'), 
                                    value=date.today(),
                                    key=f"sick_end_{emp.get('id')}"
                                )
                            
                            # حساب عدد الأيام تلقائياً
                            if sick_end >= sick_start:
                                auto_days = (sick_end - sick_start).days + 1
                            else:
                                auto_days = 1
                            
                            with sick_col3:
                                st.markdown(f"<br>", unsafe_allow_html=True)
                                st.info(f"📊 {t('admin.days_count')}: **{auto_days}**")
                            
                            sick_reason = st.text_input(
                                t('admin.reason'), 
                                key=f"sick_reason_{emp.get('id')}"
                            )
                            
                            if st.button(f"💾 {t('admin.add_sick_leave')}", key=f"add_sick_{emp.get('id')}", type="primary"):
                                db.add_sick_leave_record(
                                    employee_id=emp.get('id'),
                                    start_date=str(sick_start),
                                    end_date=str(sick_end),
                                    days_count=auto_days,
                                    reason=sick_reason
                                )
                                st.success(f"✅ {t('messages.success')}")
                                st.rerun()
                        
                        # عرض سجلات الإجازات المرضية
                        sick_records = db.get_sick_leave_records(employee_id=emp.get('id'))
                        if sick_records:
                            for rec in sick_records:
                                with st.container():
                                    rec_col1, rec_col2 = st.columns([5, 1])
                                    with rec_col1:
                                        st.markdown(f"""
                                        <p style='color: #FFFFFF; margin: 0;'>
                                        <b>📅 {t('admin.start_date')}:</b> {rec.get('start_date')} → <b>{t('admin.end_date')}:</b> {rec.get('end_date')}<br>
                                        <b>🔢 {t('admin.days_count')}:</b> {rec.get('days_count')}
                                        </p>
                                        """, unsafe_allow_html=True)
                                        if rec.get('reason'):
                                            st.markdown(f"<p style='color: #888; font-size: 0.9em;'>📝 {rec.get('reason')}</p>", unsafe_allow_html=True)
                                    with rec_col2:
                                        if st.button("🗑️", key=f"del_sick_{rec.get('id')}", help=t('admin.delete_record')):
                                            db.delete_sick_leave_record(rec.get('id'))
                                            st.rerun()
                                    st.markdown("---")
                        else:
                            st.markdown(f"<div style='background: rgba(30,60,114,0.8); padding: 10px; border-radius: 5px; border-left: 4px solid #64B4FF;'><span style='color: #FFFFFF;'>ℹ️ {t('admin.no_sick_records')}</span></div>", unsafe_allow_html=True)
                    
                    # أزرار التحكم للموظف
                    st.markdown("---")
                    btn_col1, btn_col2 = st.columns(2)
                    
                    with btn_col1:
                        if emp.get('is_active'):
                            if st.button(f"🚫 {t('admin.disable_account')}", key=f"emp_disable_h_{emp.get('id')}", use_container_width=True):
                                db.update_employee(emp.get('id'), is_active=0)
                                st.rerun()
                        else:
                            if st.button(f"✅ {t('admin.enable_account')}", key=f"emp_enable_h_{emp.get('id')}", use_container_width=True):
                                db.update_employee(emp.get('id'), is_active=1)
                                st.rerun()
                    
                    with btn_col2:
                        # حذف الموظف مع تأكيد - زرين
                        if st.session_state.get(f"confirm_del_h_{emp.get('id')}", False):
                            # عرض زر التأكيد النهائي
                            if st.button(f"⚠️ {t('admin.delete_permanent')}", key=f"emp_delete_h_{emp.get('id')}", type="primary", use_container_width=True):
                                db.delete_employee(emp.get('id'))
                                st.session_state[f"confirm_del_h_{emp.get('id')}"] = False
                                st.rerun()
                            if st.button(f"❌ {t('buttons.cancel')}", key=f"cancel_del_h_{emp.get('id')}", use_container_width=True):
                                st.session_state[f"confirm_del_h_{emp.get('id')}"] = False
                                st.rerun()
                        else:
                            # زر طلب الحذف
                            if st.button(f"🗑️ {t('admin.confirm_delete')}", key=f"ask_del_h_{emp.get('id')}", type="secondary", use_container_width=True):
                                st.session_state[f"confirm_del_h_{emp.get('id')}"] = True
                                st.rerun()  # إعادة تحميل فورية لعرض أزرار التأكيد
            else:
                st.info(t('admin.no_employees'))

        elif admin_menu == t('admin.payroll'):
            st.subheader(f"💰 {t('admin.payroll')}")
            
            import calendar
            from utils import InvoiceGenerator, NotificationManager
            from utils.i18n import get_current_lang
            
            # جلب اللغة الحالية للتطبيق
            lang = get_current_lang()
            
            # تنبيه نهاية الشهر
            today = datetime.now()
            days_in_month = calendar.monthrange(today.year, today.month)[1]
            if today.day >= days_in_month - 2:
                st.warning(f"⚠️ {t('admin.payroll_reminder')}")
            
            # اختيار الشهر والسنة
            col_month, col_year, col_gen = st.columns([2, 2, 3])
            
            month_names = {
                'en': ['January', 'February', 'March', 'April', 'May', 'June', 
                       'July', 'August', 'September', 'October', 'November', 'December'],
                'de': ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',
                       'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'],
                'ar': ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو',
                       'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
            }
            lang = st.session_state.get('language', 'de')
            current_months = month_names.get(lang, month_names['en'])
            
            with col_month:
                selected_month_idx = st.selectbox(
                    f"📅 {t('admin.select_month')}",
                    range(1, 13),
                    index=today.month - 1,
                    format_func=lambda x: current_months[x-1],
                    key="payroll_month"
                )
            
            with col_year:
                available_years = list(range(2024, today.year + 2))
                selected_year = st.selectbox(
                    f"📅 {t('admin.select_year')}",
                    available_years,
                    index=available_years.index(today.year),
                    key="payroll_year"
                )
            
            # جلب الموظفين النشطين
            employees = db.get_active_employees_for_payroll()
            
            if not employees:
                st.info(f"ℹ️ {t('admin.no_employees_payroll')}")
            else:
                # حساب إجمالي الرواتب
                total_gross = sum(float(emp.get('monthly_salary', 0) or 0) for emp in employees)
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                            padding: 15px 20px; border-radius: 12px; margin: 15px 0;
                            border: 2px solid #D4AF37;">
                    <h4 style="color: #D4AF37; margin: 0;">
                        💵 {t('admin.total_payroll')}: <span style="color: #4CAF50;">{total_gross:,.2f} EUR</span>
                        | 👥 {len(employees)} {t('admin.employees')}
                    </h4>
                </div>
                """, unsafe_allow_html=True)
                
                with col_gen:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button(f"📄 {t('admin.generate_all_invoices')}", key="gen_all_salaries", type="primary", use_container_width=True):
                        gen = InvoiceGenerator()
                        generated_count = 0
                        
                        progress_bar = st.progress(0)
                        for idx, emp in enumerate(employees):
                            try:
                                # التحقق من عدم وجود فاتورة مسبقة
                                if not db.salary_invoice_exists(emp['id'], selected_year, selected_month_idx):
                                    pdf_path = gen.generate_salary_invoice(
                                        emp, selected_month_idx, selected_year,
                                        has_children=True, church_tax=False, tax_class=1, lang='de'
                                    )
                                    
                                    # حفظ في قاعدة البيانات
                                    calc = getattr(gen, '_last_salary_calculation', {})
                                    db.create_salary_invoice(
                                        employee_id=emp['id'],
                                        month=selected_month_idx,
                                        year=selected_year,
                                        gross_salary=calc.get('gross_salary', 0),
                                        net_salary=calc.get('net_salary', 0),
                                        feiertags_geld=calc.get('holiday_bonus', 0),
                                        urlaubsgeld=calc.get('vacation_bonus', 0),
                                        tax_amount=calc.get('total_taxes', 0),
                                        insurance_amount=calc.get('total_sozialversicherung', 0),
                                        deductions=calc.get('other_deductions', 0),
                                        pdf_path=pdf_path
                                    )
                                    generated_count += 1
                            except Exception as e:
                                st.error(f"❌ {emp.get('first_name')} {emp.get('last_name')}: {e}")
                            
                            progress_bar.progress((idx + 1) / len(employees))
                        
                        if generated_count > 0:
                            st.success(f"✅ {t('admin.salary_generated')} ({generated_count})")
                        st.rerun()
                
                st.markdown("---")
                
                # جلب الفواتير الموجودة لهذا الشهر
                existing_invoices = db.get_salary_invoices_by_month(selected_year, selected_month_idx)
                invoice_map = {inv['employee_id']: inv for inv in existing_invoices}
                
                # عرض قائمة الموظفين
                for emp in employees:
                    emp_id = emp.get('id')
                    full_name = f"{emp.get('first_name', '')} {emp.get('last_name', '')}".strip()
                    salary = float(emp.get('monthly_salary', 0) or 0)
                    job = emp.get('job_title', 'N/A')
                    
                    invoice = invoice_map.get(emp_id)
                    status_icon = "✅" if invoice else "⏳"
                    status_text = t('admin.generated') if invoice else t('admin.pending')
                    
                    with st.expander(f"{status_icon} {full_name} | {job} | {salary:,.2f} EUR | {status_text}", expanded=False):
                        col1, col2, col3 = st.columns([3, 2, 2])
                        
                        with col1:
                            st.markdown(f"""
                            <div style="color: #E0E0E0;">
                                <p><b>{t('admin.gross_salary')}:</b> {salary:,.2f} EUR</p>
                                <p><b>{t('admin.feiertags_geld')}:</b> {float(emp.get('feiertags_geld', 0) or 0):,.2f} EUR</p>
                                <p><b>{t('admin.urlaubsgeld')}:</b> {float(emp.get('urlaubsgeld', 0) or 0):,.2f} EUR</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            if invoice:
                                net = float(invoice.get('net_salary', 0) or 0)
                                st.markdown(f"""
                                <div style="background: rgba(76, 175, 80, 0.2); padding: 10px; border-radius: 8px; border-left: 4px solid #4CAF50;">
                                    <b style="color: #4CAF50;">{t('admin.net_salary')}</b><br>
                                    <span style="color: #FFFFFF; font-size: 1.3em;">{net:,.2f} EUR</span>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                # حساب صافي تقديري - بالضرائب الألمانية
                                if selected_month_idx == 12:
                                    gross_total = salary + float(emp.get('feiertags_geld', 0) or 0) + float(emp.get('urlaubsgeld', 0) or 0)
                                else:
                                    gross_total = salary
                                # الاقتطاعات الألمانية التقريبية (~40% من الراتب)
                                est_deductions = salary * 0.40  # ضرائب + تأمينات
                                est_net = gross_total - est_deductions
                                st.markdown(f"""
                                <div style="background: rgba(255, 193, 7, 0.2); padding: 10px; border-radius: 8px; border-left: 4px solid #FFC107;">
                                    <b style="color: #FFC107;">{t('admin.net_salary')} (Est.)</b><br>
                                    <span style="color: #FFFFFF; font-size: 1.3em;">~{est_net:,.2f} EUR</span>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        with col3:
                            if invoice and invoice.get('pdf_path'):
                                # زر التحميل
                                pdf_path = invoice.get('pdf_path')
                                if os.path.exists(pdf_path):
                                    with open(pdf_path, "rb") as f:
                                        st.download_button(
                                            f"⬇️ {t('admin.download_salary_slip')}",
                                            f,
                                            file_name=os.path.basename(pdf_path),
                                            key=f"dl_salary_{emp_id}_{selected_month_idx}_{selected_year}",
                                            use_container_width=True
                                        )
                                
                                # زر إرسال البريد
                                if emp.get('email'):
                                    if st.button(f"📧 {t('admin.send_by_email')}", key=f"email_salary_{emp_id}", use_container_width=True):
                                        try:
                                            notifier = NotificationManager()
                                            subject = f"{t('admin.salary_slip')} - {current_months[selected_month_idx-1]} {selected_year}"
                                            body = f"<p>Dear {full_name},</p><p>Please find attached your salary slip for {current_months[selected_month_idx-1]} {selected_year}.</p>"
                                            if notifier.send_email(emp['email'], subject, body, is_html=True):
                                                st.success(f"✅ {t('admin.email_sent')}")
                                            else:
                                                st.error("❌ Email failed")
                                        except Exception as e:
                                            st.error(f"❌ {e}")
                            else:
                                # زر إصدار فردي
                                if st.button(f"📄 {t('admin.generate_salary_invoice')}", key=f"gen_salary_{emp_id}", use_container_width=True, type="primary"):
                                    try:
                                        gen = InvoiceGenerator()
                                        pdf_path = gen.generate_salary_invoice(
                                            emp, selected_month_idx, selected_year,
                                            has_children=True, church_tax=False, tax_class=1, lang='de'
                                        )
                                        calc = getattr(gen, '_last_salary_calculation', {})
                                        db.create_salary_invoice(
                                            employee_id=emp_id,
                                            month=selected_month_idx,
                                            year=selected_year,
                                            gross_salary=calc.get('gross_salary', 0),
                                            net_salary=calc.get('net_salary', 0),
                                            feiertags_geld=calc.get('holiday_bonus', 0),
                                            urlaubsgeld=calc.get('vacation_bonus', 0),
                                            tax_amount=calc.get('total_taxes', 0),
                                            insurance_amount=calc.get('total_sozialversicherung', 0),
                                            pdf_path=pdf_path
                                        )
                                        st.success(f"✅ {t('admin.salary_generated')}")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ {e}")

        elif admin_menu == t('admin.transactions'):
            st.subheader(f"💼 {t('admin.contracts_header')}")
            
            tab1, tab2 = rtl_tabs([f"💰 {t('admin.tab_contracts')}", f"🏎️ {t('admin.tab_estimates')}"])
            
            with tab1:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #0E1117 0%, #161B22 100%); 
                            padding: 12px 20px; border-radius: 10px; margin: 10px 0; 
                            border: 1px solid #4a9eff;'>
                    <span style='color: #FFFFFF; font-size: 1rem;'>ℹ️ {t('admin.contracts_desc')}</span>
                </div>
                """, unsafe_allow_html=True)
                contracts = db.get_all_contracts_with_users()
                
                if contracts:
                    for c in contracts:
                        with st.expander(f"{t('admin.contract')} #{c['id']} - {c['full_name']} ({c['created_at'][:10]})"):
                            # بيانات العميل الكاملة
                            st.markdown(f"""
                            <div style='background: rgba(74,158,255,0.1); padding: 12px; border-radius: 8px; margin: 10px 0; border-right: 4px solid #4a9eff;'>
                                <b style='color: #4a9eff;'>👤 {t('admin.client')}:</b><br>
                                <span style='color: #FFFFFF; font-size: 1.1em;'>{c.get('full_name', '-')}</span><br>
                                <span style='color: #a0a0c0;'>📧 {c.get('email', '-')} | 📱 {c.get('phone', '-')}</span><br>
                                <span style='color: #a0a0c0;'>🪪 {t('profile.id_number')}: {c.get('id_number', '-')} | 🌍 {c.get('nationality', '-')}</span><br>
                                <span style='color: #a0a0c0;'>🏎️ {t('profile.license_number')}: {c.get('license_number', '-')}</span>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            col1, col2 = st.columns([1, 1])
                            with col1:
                                st.write(f"**{t('admin.plan')}:** {c.get('plan_type', 'Full')}")
                            with col2:
                                st.write(f"**{t('admin.total_price')}:** {c['total_amount']:,.2f} €")
                            
                            try:
                                car_info = json.loads(c.get('car_details', '{}'))
                            except:
                                car_info = {'brand': 'Vehicle', 'model': 'Unknown'}
                            
                            # عرض بيانات السيارة
                            if car_info and (car_info.get('brand') or car_info.get('model')):
                                # دالة مساعدة لتجنب عرض None
                                def safe_get(d, key, default='-'):
                                    val = d.get(key)
                                    return val if val not in [None, '', 'None'] else default
                                
                                st.markdown(f"""
                                <div style='background: rgba(240,180,41,0.1); padding: 12px; border-radius: 8px; margin: 10px 0; border-right: 4px solid #D4AF37;'>
                                    <b style='color: #D4AF37;'>🏎️ {t('checkout.car_summary')}:</b><br>
                                    <span style='color: #FFFFFF; font-weight: bold;'>{safe_get(car_info, 'brand')} {safe_get(car_info, 'model', '')} - {safe_get(car_info, 'manufacture_year', safe_get(car_info, 'year', '-'))}</span><br>
                                    <span style='color: #a0a0c0; font-size: 0.9rem;'>
                                        📏 {t('predict.mileage')}: {car_info.get('mileage', 0) or 0:,} km | 
                                        ⛽ {t('predict.fuel_type')}: {safe_get(car_info, 'fuel_type')} | 
                                        🎨 {t('predict.color')}: {safe_get(car_info, 'color')}<br>
                                        📋 {t('predict.condition')}: {safe_get(car_info, 'condition')}
                                    </span>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                # محاولة استخراج من الحقول المباشرة
                                direct_brand = c.get('brand', '')
                                direct_model = c.get('model', '')
                                direct_year = c.get('manufacture_year', '')
                                direct_mileage = c.get('mileage', '-')
                                direct_fuel = c.get('fuel_type', '-')
                                direct_color = c.get('color', '-')
                                direct_condition = c.get('condition', '-')
                                # دالة مساعدة لتجنب عرض None
                                def safe_val(v, default='-'):
                                    return v if v not in [None, '', 'None'] else default
                                
                                if direct_brand or direct_model:
                                    st.markdown(f"""
                                    <div style='background: rgba(240,180,41,0.1); padding: 12px; border-radius: 8px; margin: 10px 0; border-right: 4px solid #D4AF37;'>
                                        <b style='color: #D4AF37;'>🏎️ {t('checkout.car_summary')}:</b><br>
                                        <span style='color: #FFFFFF; font-weight: bold;'>{safe_val(direct_brand)} {safe_val(direct_model, '')} - {safe_val(direct_year)}</span><br>
                                        <span style='color: #a0a0c0; font-size: 0.9rem;'>
                                            📏 {t('predict.mileage')}: {direct_mileage if direct_mileage not in [None, '', '-'] else 0:,} km | 
                                            ⛽ {t('predict.fuel_type')}: {safe_val(direct_fuel)} | 
                                            🎨 {t('predict.color')}: {safe_val(direct_color)}<br>
                                            📋 {t('predict.condition')}: {safe_val(direct_condition)}
                                        </span>
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            adm_col1, adm_col2, adm_col3 = st.columns(3)
                            
                            with adm_col1:
                                if st.button(f"🖨️ {t('admin.print_contract')}", key=f"adm_contract_h_{c['id']}", use_container_width=True, type="primary"):
                                    st.session_state.selected_transaction = c
                                    # تجميع بيانات السيارة من JSON أو من الحقول المباشرة
                                    if car_info and car_info.get('brand'):
                                        final_car_data = car_info
                                    else:
                                        final_car_data = {
                                            'brand': c.get('brand', ''),
                                            'model': c.get('model', ''),
                                            'manufacture_year': c.get('manufacture_year', ''),
                                            'mileage': c.get('mileage', 0),
                                            'fuel_type': c.get('fuel_type', ''),
                                            'condition': c.get('condition', ''),
                                            'color': c.get('color', '')
                                        }
                                    st.session_state.car_data = final_car_data
                                    st.session_state.car_details = final_car_data  # مهم لصفحة الدفع
                                    st.session_state.estimated_price = c.get('total_amount', 0)
                                    st.session_state.last_price = c.get('total_amount', 0)  # مهم أيضاً
                                    st.session_state.last_transaction_id = c['id']
                                    st.session_state.current_contract_id = c['id']
                                    # ربط العقد بالعميل الصحيح
                                    st.session_state['admin_selected_customer_id'] = c.get('user_id')
                                    # تخزين بيانات العميل الكاملة للطباعة
                                    st.session_state['checkout_customer_data'] = {
                                        'id': c.get('user_id'),
                                        'full_name': c.get('full_name', ''),
                                        'email': c.get('email', ''),
                                        'phone': c.get('phone', ''),
                                        'id_number': c.get('id_number', ''),
                                        'nationality': c.get('nationality', ''),
                                        'birth_date': c.get('birth_date', ''),
                                        'license_number': c.get('license_number', ''),
                                        'license_type': c.get('license_type', ''),
                                        'license_expiry': c.get('license_expiry', ''),
                                        'username': c.get('username', '')
                                    }
                                    st.session_state.page = 'checkout'
                                    st.rerun()
                            
                            with adm_col2:
                                if st.button(f"📄 {t('admin.print_invoices')}", key=f"adm_invoices_h_{c['id']}", use_container_width=True):
                                    st.session_state.selected_transaction = c
                                    # تجميع بيانات السيارة من JSON أو من الحقول المباشرة
                                    if car_info and car_info.get('brand'):
                                        final_car_data = car_info
                                    else:
                                        final_car_data = {
                                            'brand': c.get('brand', ''),
                                            'model': c.get('model', ''),
                                            'manufacture_year': c.get('manufacture_year', ''),
                                            'mileage': c.get('mileage', 0),
                                            'fuel_type': c.get('fuel_type', ''),
                                            'condition': c.get('condition', ''),
                                            'color': c.get('color', '')
                                        }
                                    st.session_state.car_data = final_car_data
                                    st.session_state.car_details = final_car_data  # مهم لصفحة الدفع
                                    st.session_state.estimated_price = c.get('total_amount', 0)
                                    st.session_state.last_price = c.get('total_amount', 0)  # مهم أيضاً
                                    st.session_state.last_transaction_id = c['id']
                                    st.session_state.current_contract_id = c['id']
                                    # ربط العقد بالعميل الصحيح
                                    st.session_state['admin_selected_customer_id'] = c.get('user_id')
                                    # تخزين بيانات العميل الكاملة للطباعة
                                    st.session_state['checkout_customer_data'] = {
                                        'id': c.get('user_id'),
                                        'full_name': c.get('full_name', ''),
                                        'email': c.get('email', ''),
                                        'phone': c.get('phone', ''),
                                        'id_number': c.get('id_number', ''),
                                        'nationality': c.get('nationality', ''),
                                        'birth_date': c.get('birth_date', ''),
                                        'license_number': c.get('license_number', ''),
                                        'license_type': c.get('license_type', ''),
                                        'license_expiry': c.get('license_expiry', ''),
                                        'username': c.get('username', '')
                                    }
                                    st.session_state.page = 'checkout'
                                    st.rerun()
                            
                            with adm_col3:
                                # زر حذف المعاملة
                                if st.session_state.get(f"confirm_del_tx_{c['id']}", False):
                                    if st.button(f"⚠️ {t('admin.delete_permanent')}", key=f"del_tx_confirm_{c['id']}", use_container_width=True, type="primary"):
                                        db.delete_transaction(c['id'])
                                        st.session_state[f"confirm_del_tx_{c['id']}"] = False
                                        st.success(f"✅ {t('messages.success')}")
                                        st.rerun()
                                    if st.button(f"❌ {t('buttons.cancel')}", key=f"cancel_del_tx_{c['id']}", use_container_width=True):
                                        st.session_state[f"confirm_del_tx_{c['id']}"] = False
                                        st.rerun()
                                else:
                                    if st.button(f"🗑️ {t('buttons.delete')}", key=f"del_tx_{c['id']}", use_container_width=True):
                                        st.session_state[f"confirm_del_tx_{c['id']}"] = True
                                        st.rerun()
                else:
                    st.info(t('admin.no_contracts_yet_user'))
            
            with tab2:
                st.caption(t('admin.estimates_history_caption'))
                available_years = db.get_available_years()
                selected_year = st.selectbox(f"📅 {t('admin.select_year')}", available_years, key="year_select_h")
                
                transactions = db.get_transactions_by_year(selected_year)
                
                if transactions:
                    st.write(f"{t('admin.transaction_count')}: {len(transactions)}")
                    for trans in transactions:
                        with st.expander(f"#{trans.get('id')} - {trans.get('brand')} {trans.get('model')} - €{trans.get('estimated_price', 0):,.2f}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**{t('admin.username')}:** {trans.get('username')}")
                                st.write(f"**{t('admin.car_type')}:** {trans.get('car_type')}")
                                st.write(f"**{t('admin.brand')}:** {trans.get('brand')}")
                            
                            with col2:
                                st.write(f"**{t('admin.model')}:** {trans.get('model')} {trans.get('manufacture_year')}")
                                st.write(f"**{t('admin.mileage')}:** {trans.get('mileage')} km")
                                st.write(f"**{t('admin.estimated_price')}:** €{trans.get('estimated_price', 0):,.2f}")
                            
                            st.markdown("---")
                            
                            adm_act1, adm_act2 = st.columns(2)
                            
                            with adm_act1:
                                if st.button(f"❌ {t('admin.delete')}", key=f"adm_del_tr_h_{trans['id']}"):
                                    if db.delete_transaction(trans['id']):
                                        st.success(t('messages.success'))
                                        st.rerun()
                            
                            with adm_act2:
                                if st.button(f"💳 {t('predict.step3_title')}", key=f"adm_checkout_h_{trans['id']}"):
                                    st.session_state.selected_transaction = trans
                                    st.session_state.car_data = {
                                        'brand': trans.get('brand'),
                                        'model': trans.get('model'),
                                        'manufacture_year': trans.get('manufacture_year'),
                                        'mileage': trans.get('mileage'),
                                        'car_type': trans.get('car_type'),
                                        'estimated_price': trans.get('estimated_price')
                                    }
                                    st.session_state.estimated_price = trans.get('estimated_price', 0)
                                    st.session_state.page = 'checkout'
                                    st.rerun()
                else:
                    st.info(t('admin.no_transactions_year'))
    
    else:
        # === المستخدم العادي (غير الأدمن) ===
        st.markdown("""
        <style>
            .user-welcome-card {
                background: linear-gradient(135deg, #0E1117 0%, #1a1f2e 100%);
                padding: 25px;
                border-radius: 15px;
                margin: 20px 0;
                border: 2px solid #4facfe;
            }
            .user-action-btn {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                padding: 15px 25px;
                border-radius: 12px;
                text-align: center;
                margin: 10px;
                display: inline-block;
                transition: transform 0.3s ease;
            }
            .user-action-btn:hover {
                transform: scale(1.05);
            }
        </style>
        """, unsafe_allow_html=True)
        
        # رسالة ترحيبية
        st.markdown(f"""
        <div class="user-welcome-card">
            <h3 style="color: #4facfe; margin: 0;">👋 {t('home.user_welcome_title', 'Welcome to SmartCar AI-Dealer!')}</h3>
            <p style="color: #a0a0c0; margin-top: 10px;">{t('home.user_welcome_desc', 'Start evaluating your car and get the best price estimate.')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # (الأزرار موجودة في القائمة الجانبية - تمت إزالة التكرار)
        
        st.markdown("---")
        
        # آخر المعاملات
        st.subheader(f"📋 {t('home.recent_transactions', 'Recent Transactions')}")
        
        db = DatabaseManager()
        user_transactions = db.get_user_transactions(user['id'], limit=5)
        
        if user_transactions:
            for trans in user_transactions:
                with st.expander(f"🏎️ {trans.get('brand', '')} {trans.get('model', '')} - €{trans.get('estimated_price', 0):,.2f}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**{t('admin.car_type')}:** {trans.get('car_type', '-')}")
                        st.write(f"**{t('admin.year')}:** {trans.get('manufacture_year', '-')}")
                    with col2:
                        st.write(f"**{t('admin.mileage')}:** {trans.get('mileage', 0):,} km")
                        st.write(f"**{t('admin.condition')}:** {trans.get('condition', '-')}")
        else:
            st.info(t('home.no_transactions_yet', 'You have no transactions yet. Start by evaluating your car!'))


# ======================
# مكونات واجهة المستخدم
# ======================

def render_progress_bar(current_step):
    """عرض شريط التقدم"""
    steps = {
        1: t('predict.step1_title'),
        2: t('predict.step2_title'),
        3: t('predict.step3_title')
    }
    
    st.markdown("""
    <style>
    .progress-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
        position: fixed;
        top: 80px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 99999;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 10px 40px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        border-radius: 50px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        width: auto;
        min-width: 600px;
        max-width: 90%;
    }
    .progress-container::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 40px;
        right: 40px;
        width: auto;
        height: 4px;
        background: #e0e0e0;
        z-index: 0;
        transform: translateY(-50%);
    }
    .step {
        position: relative;
        z-index: 1;
        background: white;
        width: 35px;
        height: 35px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid #e0e0e0;
        font-weight: bold;
        color: #7f8c8d;
        font-size: 14px;
        transition: all 0.3s ease;
    }
    .step.active {
        background: #4facfe;
        color: white;
        border-color: #4facfe;
        transform: scale(1.1);
        box-shadow: 0 0 10px rgba(79, 172, 254, 0.4);
    }
    .step.completed {
        background: #38ef7d;
        color: white;
        border-color: #38ef7d;
    }
    .step-label {
        position: absolute;
        top: 45px;
        left: 50%;
        transform: translateX(-50%);
        white-space: nowrap;
        font-size: 12px;
        color: #555;
        font-weight: 500;
        background: rgba(255,255,255,0.9);
        padding: 2px 8px;
        border-radius: 10px;
    }
    .step.active .step-label {
        color: #4facfe;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # بناء HTML للشريط
    html_content = '<div class="progress-container">'
    for step_num, label in steps.items():
        if step_num < current_step:
            cls = "step completed"
            icon = "✓"
        elif step_num == current_step:
            cls = "step active"
            icon = str(step_num)
        else:
            cls = "step"
            icon = str(step_num)
            
        html_content += f'<div class="{cls}">{icon}<div class="step-label">{label}</div></div>'
    
    html_content += '</div>'
    
    st.markdown(html_content, unsafe_allow_html=True)


# ======================
# صفحة تقدير السعر
# ======================

def predict_page():
    """صفحة تقدير السعر"""
    render_progress_bar(1)
    
    # تحميل بيانات العميل من قاعدة البيانات
    if st.session_state.get('user'):
        db = DatabaseManager()
        fresh_user = db.get_user_by_id(st.session_state.user['id'])
        if fresh_user:
            st.session_state.user = fresh_user
    
    st.session_state.user = fresh_user

    # Render universal header
    render_universal_header(t('nav.predict'), "🏎️ " + t('predict.ai_evaluation'))
    
    st.markdown("---")
    
    # الخطوة 1: رفع الصورة
    st.subheader(f"📸 {t('predict.step1_title')}")
    
    # اختيار طريقة الحصول على الصورة
    image_tab1, image_tab2 = rtl_tabs([f"📁 {t('predict.upload_image')}", f"📷 {t('predict.capture_image')}"])
    
    images_to_analyze = {}
    main_image_bytes = None
    
    with image_tab1:
        st.markdown(f"### 📸 {t('predict.upload_images')}")
        st.info(f"💡 {t('predict.upload_hint')}")
        
        col_up1, col_up2, col_up3 = st.columns(3)
        
        with col_up1:
            st.markdown(f"**1. {t('predict.front_image')}**")
            front_img = st.file_uploader(t('predict.front_image'), type=['jpg', 'jpeg', 'png', 'webp'], key="up_front")
        
        with col_up2:
            st.markdown(f"**2. {t('predict.side_image')}**")
            side_img = st.file_uploader(t('predict.side_image'), type=['jpg', 'jpeg', 'png', 'webp'], key="up_side")
            
        with col_up3:
            st.markdown(f"**3. {t('predict.interior_image')}**")
            interior_img = st.file_uploader(t('predict.interior_image'), type=['jpg', 'jpeg', 'png', 'webp'], key="up_interior")

        # تجميع الصور
        
        if front_img:
            images_to_analyze['front'] = front_img.getvalue()
            main_image_bytes = front_img.getvalue()
            
        if side_img:
            images_to_analyze['side'] = side_img.getvalue()
            
        if interior_img:
            images_to_analyze['interior'] = interior_img.getvalue()

    with image_tab2:
        # تلميح مهم للمستخدم
        st.warning(f"📸 {t('predict.camera_tip', 'Get close to the car and make sure the brand LOGO is clearly visible for accurate identification!')}")
        
        # الكاميرا (دائماً الصورة الأمامية متاحة)
        st.markdown(f"##### 1. {t('predict.front_image')}")
        
        # تصغير الكاميرا إلى 50% مع معالجة الصورة (قص الحواف)
        cam_col1, cam_col2, cam_col3 = st.columns([1, 2, 1])
        with cam_col2:
            camera_front = st.camera_input(t('predict.take_front_photo'), key="cam_front")
            if camera_front:
                # معالجة الصورة لقص الزوائد الجانبية (15% من كل جانب)
                try:
                    img = Image.open(camera_front)
                    width, height = img.size
                    
                    # إضافة slider للتكبير (Zoom)
                    zoom_level = st.slider(
                        f"🔍 {t('predict.zoom_level', 'Zoom Level')}",
                        min_value=1.0,
                        max_value=3.0,
                        value=1.0,
                        step=0.1,
                        key="front_zoom",
                        help=t('predict.zoom_help', 'Zoom in to capture the brand logo more clearly')
                    )
                    
                    # حساب منطقة القص بناءً على مستوى التكبير
                    if zoom_level > 1.0:
                        # حساب حجم المنطقة المقصوصة (كلما زاد الزوم، صغرت المنطقة)
                        crop_ratio = 1.0 / zoom_level
                        new_width = width * crop_ratio
                        new_height = height * crop_ratio
                        
                        # حساب إحداثيات القص من المركز
                        left = (width - new_width) / 2
                        top = (height - new_height) / 2
                        right = left + new_width
                        bottom = top + new_height
                    else:
                        # الزوم الافتراضي: قص 15% من الجوانب فقط
                        left = width * 0.15
                        top = 0
                        right = width * 0.85
                        bottom = height
                    
                    img_cropped = img.crop((left, top, right, bottom))
                    
                    # عرض الصورة المقصوصة للمستخدم
                    st.image(img_cropped, caption=f"📷 {t('predict.zoomed_preview', 'Zoomed Preview')} ({zoom_level}x)", use_container_width=True)
                    
                    # تحويل الصورة المقصوصة إلى bytes
                    buf = BytesIO()
                    img_cropped.save(buf, format="JPEG")
                    main_image_bytes = buf.getvalue()
                    images_to_analyze['front'] = main_image_bytes
                    
                    st.success(f"✅ {t('predict.image_processed_success')}")
                except Exception as e:
                    st.error(f"❌ {t('predict.image_process_error')}: {e}")
                    # في حالة الخطأ، نستخدم الصورة الأصلية
                    images_to_analyze['front'] = camera_front.getvalue()
                    main_image_bytes = camera_front.getvalue()


        
        # خيار التقاط صور إضافية
        if st.checkbox(f"📸 {t('predict.enable_multi_cam')}", key="enable_multi_cam"):
            col_cam_side, col_cam_int = st.columns(2)
            
            with col_cam_side:
                st.markdown(f"##### {t('predict.side_image_header')}")
                camera_side = st.camera_input(t('predict.take_side_photo'), key="cam_side")
                if camera_side:
                    images_to_analyze['side'] = camera_side.getvalue()
            
            with col_cam_int:
                st.markdown(f"##### {t('predict.interior_image_header')}")
                camera_interior = st.camera_input(t('predict.take_interior_photo'), key="cam_interior")
                if camera_interior:
                    images_to_analyze['interior'] = camera_interior.getvalue()

    if main_image_bytes:
        # حفظ الصورة الرئيسية للعرض
        st.session_state.uploaded_image = main_image_bytes
        
        # عرض الصور المرفوعة
        st.markdown("---")
        st.markdown(f"### 🖼️ {t('admin.selected_images')}")
        
        num_images = len(images_to_analyze)
        if num_images == 1:
            # إذا كانت صورة واحدة، نعرضها بحجم أصغر (50% تقريباً) وفي المنتصف
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                for label, img_data in images_to_analyze.items():
                    localized_label = t(f'predict.label_{label}') if t(f'predict.label_{label}') else label
                    st.image(img_data, caption=t('predict.image_caption', label=localized_label), use_container_width=True)
        else:
            # عرض متعدد (أعمدة متساوية)
            disp_cols = st.columns(num_images)
            for idx, (label, img_data) in enumerate(images_to_analyze.items()):
                with disp_cols[idx]:
                    localized_label = t(f'predict.label_{label}') if t(f'predict.label_{label}') else label
                    st.image(img_data, caption=t('predict.image_caption', label=localized_label), use_container_width=True)
        
        # التحقق الأولي (توفير التكلفة)
        st.markdown("---")
        col_check, col_analyze = st.columns([1, 1])
        
        with col_check:
            st.warning(f"🔄 {t('admin.verifying_image')}")
            # التحقق السريع (أقل تكلفة)
            analyzer = GroqCarAnalyzer()
            validation = analyzer.quick_validate_image(main_image_bytes)
            
            if validation['is_valid']:
                st.success(f"✅ **{t('admin.valid_image')}**")
                valid_car = True
            else:
                st.error(f"❌ **{t('admin.alert')}:** {validation['message']}")
                st.warning(t('admin.upload_clear_image'))
                valid_car = False
        
        with col_analyze:
            if valid_car:
                if st.button(f"🤖 {t('admin.ai_full_analysis')}", type="primary"):
                    with st.spinner(t('admin.analyzing_images')):
                        try:
                            # استخدام التحليل المتعدد
                            analysis_result = analyzer.analyze_car_from_multiple_angles(images_to_analyze)
                            
                            st.session_state.analysis_result = analysis_result
                            st.session_state.car_details['analysis'] = analysis_result
                            
                            if analysis_result.get('success'):
                                st.success(f"✅ {t('messages.success')}")
                                st.rerun()
                            else:
                                st.warning(f"⚠️ {analysis_result.get('error', t('messages.error'))}")
                        except Exception as e:
                            st.error(f"❌ {t('messages.error')}: {str(e)}")
            else:
                st.button(f"🤖 {t('predict.analyzing')}", disabled=True, help=t('predict.upload_hint'))
    
    # عرض نتائج التحليل
    if st.session_state.get('analysis_result') and st.session_state.analysis_result.get('success'):
        st.markdown("---")
        analysis = st.session_state.analysis_result
        
        # استدعاء المكون الجديد بدلاً من الكود القديم
        get_analysis_results_html(analysis)
        
        # Legacy expander restored by user request
        with st.expander(f"📊 {t('predict.analysis_details')}", expanded=True):
            st.write(f"**{t('predict.expected_brand')}:** {analysis.get('estimated_brand', t('messages.unknown'))}")
            st.write(f"**{t('predict.expected_model')}:** {analysis.get('estimated_model', t('messages.unknown'))}")
            st.write(f"**{t('predict.color')}:** {analysis.get('color', t('messages.unknown'))}")
            
            # Use dynamic condition map
            cond_map = {
                'Excellent': t('predict.cond_excellent'), 
                'Good': t('predict.cond_good'), 
                'Fair': t('predict.cond_fair'), 
                'Poor': t('predict.cond_poor')
            }
            raw_cond = analysis.get('exterior_condition', analysis.get('condition', 'Good'))
            condition = cond_map.get(raw_cond, raw_cond)
            
            st.write(f"**حالة الهيكل الخارجي:** {condition}")
            
            damages = analysis.get('visible_damage', [])
            if damages and damages != ['لا يوجد'] and damages != ['None']:
                st.write(f"**الأضرار المرئية:** {', '.join(damages)}")
            else:
                st.write("**الأضرار المرئية:** لا توجد أضرار ظاهرة")
            
            if analysis.get('notes'):
                st.write(f"**ملاحظات:** {analysis.get('notes')}")

    
    # الخطوة 2: معلومات إضافية
    if st.session_state.uploaded_image:
        st.markdown("<br>", unsafe_allow_html=True)
        get_section_header_html(f"📊 {t('admin.step2_car_info')}")
        
        st.info(f"💡 {t('predict.upload_hint')}")
        
        # استخراج القيم من التحليل
        analysis = st.session_state.get('analysis_result') or {}
        has_analysis = analysis.get('success', False) if analysis else False
        
        # تحديد نوع السيارة من التحليل
        car_type_options = [t('admin.car_type_sedan'), t('admin.car_type_suv'), t('admin.car_type_coupe'), t('admin.car_type_hybrid'), t('admin.car_type_electric'), t('admin.car_type_pickup')]
        default_type_index = 0
        if analysis.get('estimated_type'):
            estimated_type = analysis.get('estimated_type', '')
            for i, opt in enumerate(car_type_options):
                if opt in estimated_type or estimated_type in opt:
                    default_type_index = i
                    break
        
        # استخراج القيم الافتراضية
        default_year = 2020
        year_range = analysis.get('estimated_year_range', '')
        if year_range and year_range != 'غير معروف':
            try:
                import re
                years = re.findall(r'20\d{2}', str(year_range))
                if years:
                    default_year = int(years[-1])
            except:
                pass

        default_brand = analysis.get('estimated_brand', '') if analysis.get('estimated_brand') != 'غير معروف' else ""
        default_model = analysis.get('estimated_model', '') if analysis.get('estimated_model') != 'غير معروف' else ""

        # تخطيط 4 أعمدة للمدخلات (الصف الأول: البيانات الأساسية)
        c1, c2, c3, c4 = st.columns(4)
        
        # تخطيط 4 أعمدة للمدخلات (الصف الثاني: المواصفات)
        c5, c6, c7, c8 = st.columns(4)

        # تخطيط 4 أعمدة للمدخلات (الصف الثالث: التوف والصيانة)
        c9, c10, c11, c12 = st.columns(4)
        
        # تخطيط 4 أعمدة للمدخلات (الصف الرابع: اللون والمقاعد)
        c13, c14, c15, c16 = st.columns(4)

        if has_analysis:
            # الصف الأول
            with c1:
                car_type = st.text_input(t('predict.car_type'), value=car_type_options[default_type_index], disabled=True, key="live_type")
            with c2:
                brand = st.text_input(t('predict.brand'), value=default_brand, disabled=True, key="live_brand")
            with c3:
                model = st.text_input(t('predict.model'), value=default_model, disabled=True, key="live_model")
            with c4:
                manufacture_year = st.number_input(t('predict.year'), min_value=1990, max_value=datetime.now().year + 1, value=default_year, disabled=True, key="live_year")
            
            # منطق قفل نوع الوقود
            fuel_options = [t('admin.fuel_gasoline'), t('admin.fuel_diesel'), t('admin.fuel_hybrid'), t('admin.fuel_electric')]
            analyzed_fuel = analysis.get('fuel_type', '')
            fuel_idx = 0
            fuel_disabled = False
            if analyzed_fuel in fuel_options:
                fuel_idx = fuel_options.index(analyzed_fuel)
                fuel_disabled = True
            
            # منطق الحالة
            # منطق الحالة
            cond_map_form = {
                'Excellent': t('admin.condition_excellent'), 'Good': t('admin.condition_good'), 'Fair': t('admin.condition_fair'), 'Poor': t('admin.condition_poor')
            }
            raw_cond_form = analysis.get('exterior_condition', analysis.get('condition', ''))
            default_condition = cond_map_form.get(raw_cond_form, t('admin.condition_good'))
            
            condition_options = [t('admin.condition_excellent'), t('admin.condition_very_good'), t('admin.condition_good'), t('admin.condition_fair'), t('admin.condition_poor')]
            cond_idx = 2
            if default_condition in condition_options:
                cond_idx = condition_options.index(default_condition)

            # الصف الثاني
            with c5:
                fuel_type = st.selectbox(t('admin.fuel_type'), fuel_options, index=fuel_idx, disabled=fuel_disabled, key="live_fuel")
            with c6:
                condition = st.selectbox(t('admin.car_condition_label'), condition_options, index=cond_idx, help=t('admin.car_condition_label'), key="live_condition")
            with c7:
                mileage = st.number_input(t('admin.mileage_km'), min_value=0, max_value=1000000, value=0, step=1000, help=t('admin.mileage_km'), key="live_mileage")
            with c8:
                previous_owners = st.number_input(t('admin.previous_owners'), min_value=1, max_value=10, value=1, step=1, help=t('admin.previous_owners'), key="live_owners")
            
            # الصف الثالث (التوف والصيانة)
            with c9:
                tuv_start = st.date_input(t('admin.tuv_start'), value=datetime.now(), format="DD/MM/YYYY", key="live_tuv_start")
            with c10:
                default_end = datetime.now() + timedelta(days=365)
                tuv_end = st.date_input(t('admin.tuv_end'), value=default_end, format="DD/MM/YYYY", key="live_tuv_end")
            with c11:
                # حساب المدة المتبقية
                tuv_remaining_days = (tuv_end - datetime.now().date()).days
                tuv_months = int(tuv_remaining_days / 30)
                
                tuv_display = f"{tuv_months} {t('admin.month')}"
                if tuv_months < 0: tuv_display = t('admin.expired')
                
                st.metric(t('admin.tuv_remaining'), tuv_display)
                
            with c12:
                maintenance_opt = st.selectbox(t('admin.maintenance'), [t('admin.maintenance_yes'), t('admin.maintenance_no')], index=0, key="live_maintenance")
                has_maintenance = (maintenance_opt == t('admin.maintenance_yes'))
            
            # الصف الرابع (اللون والمقاعد)
            default_color = analysis.get('color', '').lower().strip()
            color_options = [t('admin.color_white'), t('admin.color_black'), t('admin.color_gray'), t('admin.color_silver'), t('admin.color_red'), t('admin.color_blue'), t('admin.color_green'), t('admin.color_brown'), t('admin.color_gold'), t('admin.color_other')]
            
            # خريطة الألوان الإنجليزية للفهرس
            color_mapping = {
                'white': 0, 'weiß': 0, 'weiss': 0, 'أبيض': 0,
                'black': 1, 'schwarz': 1, 'أسود': 1,
                'gray': 2, 'grey': 2, 'grau': 2, 'رمادي': 2,
                'silver': 3, 'silber': 3, 'فضي': 3,
                'red': 4, 'rot': 4, 'أحمر': 4,
                'blue': 5, 'blau': 5, 'أزرق': 5,
                'green': 6, 'grün': 6, 'gruen': 6, 'أخضر': 6,
                'brown': 7, 'braun': 7, 'بني': 7,
                'gold': 8, 'golden': 8, 'ذهبي': 8,
            }
            
            color_idx = 0
            if default_color:
                # البحث في الخريطة أولاً
                for color_key, idx in color_mapping.items():
                    if color_key in default_color:
                        color_idx = idx
                        break
            
            with c13:
                color = st.selectbox(t('admin.car_color'), color_options, index=color_idx, key="live_color")
            with c14:
                seats = st.number_input(t('admin.seats_count'), min_value=2, max_value=9, value=5, key="live_seats")
            with c15:
                st.write("")  # فارغ
            with c16:
                st.write("")  # فارغ

        else:
            # وضع يدوي
            with c1:
                car_type = st.selectbox(f"{t('admin.car_type_required')} *", car_type_options, index=0, key="live_type_man")
            with c2:
                brand = st.text_input(f"{t('admin.brand_required')} *", value="", key="live_brand_man")
            with c3:
                model = st.text_input(t('admin.model_optional'), value="", key="live_model_man")
            with c4:
                manufacture_year = st.number_input(f"{t('admin.manufacture_year')} *", min_value=1990, max_value=datetime.now().year + 1, value=2020, key="live_year_man")
            
            with c5:
                fuel_type = st.selectbox(f"{t('admin.fuel_type')} *", [t('admin.fuel_gasoline'), t('admin.fuel_diesel'), t('admin.fuel_hybrid'), t('admin.fuel_electric')], index=0, key="live_fuel_man")
            with c6:
                condition = st.selectbox(f"{t('admin.car_condition')} *", [t('admin.condition_excellent'), t('admin.condition_very_good'), t('admin.condition_good'), t('admin.condition_fair'), t('admin.condition_poor')], index=2, key="live_condition_man")
            with c7:
                mileage = st.number_input(f"{t('admin.mileage_km')} *", min_value=0, max_value=1000000, value=50000, step=1000, key="live_mileage_man")
            with c8:
                previous_owners = st.number_input(t('admin.previous_owners'), min_value=1, max_value=10, value=1, step=1, key="live_owners_man")
            
            # الصف الثالث (التوف والصيانة) - يدوي
            with c9:
                tuv_start = st.date_input(t('admin.tuv_start'), value=datetime.now(), format="DD/MM/YYYY", key="live_tuv_start_man")
            with c10:
                default_end = datetime.now() + timedelta(days=365)
                tuv_end = st.date_input(t('admin.tuv_end'), value=default_end, format="DD/MM/YYYY", key="live_tuv_end_man")
            with c11:
                tuv_remaining_days = (tuv_end - datetime.now().date()).days
                tuv_months = int(tuv_remaining_days / 30)
                
                tuv_display = f"{tuv_months} {t('admin.month')}"
                if tuv_months < 0: 
                    tuv_display = f"{t('admin.expired')} ❌"
                
                st.metric(t('admin.tuv_remaining'), tuv_display)
                
                # عرض التأثير بشكل منفصل لضمان ظهوره
                if tuv_months > 12:
                    st.caption(f"**:green[{t('admin.price_increase_tuv')} 📈]**")
                elif tuv_months < 3:
                    st.caption(f"**:red[{t('admin.price_decrease_tuv')} 📉]**")
                else:
                    st.caption(f"**:grey[{t('admin.price_neutral_tuv')} 😐]**")
            with c12:
                maintenance_opt = st.selectbox(t('admin.maintenance'), [t('admin.maintenance_yes'), t('admin.maintenance_no')], index=0, key="live_maintenance_man")
                has_maintenance = (maintenance_opt == t('admin.maintenance_yes'))
            
            # الصف الرابع (اللون والمقاعد) - يدوي
            color_options = [t('admin.color_white'), t('admin.color_black'), t('admin.color_gray'), t('admin.color_silver'), t('admin.color_red'), t('admin.color_blue'), t('admin.color_green'), t('admin.color_brown'), t('admin.color_gold'), t('admin.color_other')]
            with c13:
                color = st.selectbox(t('admin.car_color'), color_options, index=0, key="live_color_man")
            with c14:
                seats = st.number_input(t('admin.seats_count'), min_value=2, max_value=9, value=5, key="live_seats_man")
            with c15:
                st.write("")  # فارغ
            with c16:
                st.write("")  # فارغ

        # معاينة السعر المباشرة
        st.markdown("<br>", unsafe_allow_html=True)
        get_section_header_html(f"👁️ {t('admin.live_price_preview')}")
        
        if brand: # حساب فقط عند وجود البيانات الأساسية
            try:
                # تهيئة الكائن
                predictor = PricePredictor()
                
                # نستخدم القيم المباشرة من السيشن لضمان التحديث اللحظي
                current_condition = st.session_state.get("live_condition", condition)
                current_mileage = st.session_state.get("live_mileage", mileage)
                current_owners = st.session_state.get("live_owners", previous_owners)
                # حساب ال TUV من الودجت مباشرة
                # ملاحظة: التاريخ لا يمكن الوصول له بسهولة من ال session state بنفس طريقة النص، لذا نستخدم القيم المحسوبة
                
                # تحويل الحالة النصية إلى رقمية
                condition_map = {
                    'ممتازة': 1.0, 'جيدة جداً': 0.9, 'جيدة': 0.8,
                    'مقبولة': 0.6, 'سيئة': 0.4, 'سيئة جداً': 0.2
                }
                c_score = condition_map.get(current_condition, 0.8)

                # تجهيز البيانات كـ Dictionary كما يتوقعها PricePredictor
                live_data = {
                    'car_type': car_type,
                    'brand': brand,
                    'condition_score': c_score,
                    'mileage': current_mileage,
                    'manufacture_year': manufacture_year,
                    'fuel_type': fuel_type,
                    'owners': current_owners,
                    'maintenance': has_maintenance,
                    'tuv_months': tuv_months
                }
                
                # توقع السعر
                with st.spinner(t('admin.updating_price')):
                     live_price = predictor.predict_price(live_data)

                
                # عرض السعر في بطاقة ملونة
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #000000 0%, #333333 100%);
                    padding: 20px;
                    border-radius: 15px;
                    color: white;
                    text-align: center;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                    margin-top: 10px;
                    border: 1px solid rgba(255,255,255,0.2);">
                    <small style="opacity: 0.8">السعر التقديري الحالي</small>
                    <h1 style="color: white; margin: 10px 0; font-size: 2.5em;">${live_price:,.0f}</h1>
                    <div style="font-size: 0.9em; opacity: 0.7; margin-top: 5px;">
                        {car_type} | {manufacture_year} | {condition}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"{t('admin.calculating')} ({e})")
        else:
            st.info(t('admin.enter_car_data'))

        st.markdown("---")
        if st.button(f"✅ {t('admin.approve_result')}", type="primary", use_container_width=True):
             if not brand:
                 st.error(f"⚠️ {t('admin.enter_brand')}")
             else:
                 # حفظ البيانات
                 st.session_state.car_details.update({
                     'car_type': car_type,
                     'brand': brand,
                     'model': model,
                     'manufacture_year': manufacture_year,
                     'mileage': mileage,
                     'fuel_type': fuel_type,
                     'color': color,
                     'seats': seats,
                     'previous_owners': previous_owners,
                     'tuv_months': tuv_months,
                     'maintenance_history': has_maintenance,
                     'condition': condition
                 })
                 navigate_to('results')


# ======================
# صفحة النتائج
# ======================

def results_page():
    """صفحة عرض النتائج"""
    render_progress_bar(3)
    
    # Render universal header
    render_universal_header(t('results.title'), "📊 " + t('results.evaluation_results'))
    
    # التحقق من وجود البيانات
    if not st.session_state.uploaded_image or not st.session_state.car_details:
        st.error(f"⚠️ {t('messages.error')}")
        if st.button(f"← {t('buttons.back')}"):
            navigate_to('predict')
        return
    
    car_data = st.session_state.car_details
    analysis = car_data.get('analysis', {})
    
    # تقدير السعر
    # تقدير السعر
    with st.spinner(t('messages.loading')):
        predictor = PricePredictor()
        
        # تحويل الحالة النصية إلى رقمية
        condition_map = {
            'ممتازة': 1.0, 'جيدة جداً': 0.9, 'جيدة': 0.8,
            'مقبولة': 0.6, 'سيئة': 0.4, 'سيئة جداً': 0.2
        }
        c_str = car_data.get('condition', 'جيدة')
        c_score = condition_map.get(c_str, 0.8)
        
        predict_data = {
            'car_type': car_data.get('car_type', 'سيدان'),
            'brand': car_data.get('brand', 'أخرى'),
            'condition_score': c_score,
            'mileage': car_data.get('mileage', 50000),
            'manufacture_year': car_data.get('manufacture_year', 2020),
            'fuel_type': car_data.get('fuel_type', 'بنزين'),
            'owners': car_data.get('previous_owners', 1),
            'tuv_months': car_data.get('tuv_months', 0),
            'maintenance': car_data.get('maintenance_history', False)
        }
        
        estimated_price = predictor.predict_price(predict_data)
        min_p, max_p = predictor.get_price_range(estimated_price)
        price_range = {'min': min_p, 'max': max_p}
        
        st.session_state.prediction_data = {'estimated_price': estimated_price, 'price_range': price_range}
    
    # عرض النتيجة الرئيسية باستخدام التصميم الجديد
    # استخلاص الثقة من تحليل الذكاء الاصطناعي
    confidence_str = analysis.get('confidence_score', '90%').replace('%', '')
    try:
        confidence_pct = int(confidence_str)
    except:
        confidence_pct = 90
        
    confidence = 'عالية' if confidence_pct > 80 else 'متوسطة'
    
    # مكونات السعر (سنستخدم قيم افتراضية ومحسوبة للعرض)
    comp = {
        'base_price': estimated_price * 0.5, # قيمة افتراضية للعرض
        'condition': {'factor': 1.0, 'contribution': 0}, 
        'mileage': {'factor': 1.0, 'contribution': 0}, 
        'age': {'factor': 1.0, 'contribution': 0},
        'brand_factor': 1.0, # Note: using brand_factor (flat key) as expected by line 887
        'fuel_factor': 1.0,
        'owners_factor': 1.0,
        'tuv_factor': 1.0,
        'maintenance_factor': 1.0
    }
    
    # استدعاء الواجهة الموحدة
    get_results_page_html(
        estimated_price, 
        price_range, 
        confidence, 
        confidence_pct, 
        car_data, 
        comp
    )
    
    st.markdown("---")
    
    st.markdown("---")
    
    # أزرار الإجراءات
    st.subheader(f"📄 {t('admin.action_options')}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # التحقق إذا كان الأدمن - عرض خيار اختيار العميل
        if st.session_state.user.get('role') == 'admin':
            if not st.session_state.get('admin_save_mode'):
                if st.button("💾 حفظ التقدير", use_container_width=True):
                    st.session_state['admin_save_mode'] = True
                    st.rerun()
            
            if st.session_state.get('admin_save_mode'):
                st.markdown("""
                <div style="background: linear-gradient(135deg, #0E1117 0%, #161B22 100%); 
                            padding: 15px; border-radius: 10px; border: 2px solid #D4AF37; margin: 10px 0;">
                    <h4 style="color: #D4AF37; margin: 0;">👤 اختر العميل الحقيقي</h4>
                    <p style="color: #a0a0c0; font-size: 0.9rem; margin: 5px 0 0 0;">سيتم ربط هذا التقدير بالعميل المختار</p>
                </div>
                """, unsafe_allow_html=True)
                
                db = DatabaseManager()
                all_users = db.get_all_users()
                # استبعاد الأدمن من القائمة
                customers = [u for u in all_users if u.get('role') != 'admin']
                
                if customers:
                    customer_options = {f"{u.get('full_name') or u.get('username')} ({u.get('email')})": u for u in customers}
                    
                    selected_customer_key = st.selectbox(
                        t('admin.customer'),
                        options=list(customer_options.keys()),
                        key="admin_customer_select"
                    )
                    
                    selected_customer = customer_options.get(selected_customer_key)
                    
                    save_col1, save_col2 = st.columns(2)
                    with save_col1:
                        if st.button(f"✅ {t('admin.save_for_customer')}", use_container_width=True, type="primary"):
                            try:
                                car_image = st.session_state.get('uploaded_image')
                                transaction_id = db.create_transaction(
                                    user_id=selected_customer['id'],  # ID العميل وليس الأدمن
                                    car_data=car_data,
                                    estimated_price=estimated_price,
                                    condition_analysis=analysis,
                                    car_image_bytes=car_image
                                )
                                
                                st.session_state.last_transaction_id = transaction_id
                                st.session_state['admin_save_mode'] = False
                                st.success(f"✅ {t('admin.estimate_saved_for_customer')}: {selected_customer.get('full_name') or selected_customer.get('username')}")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ {t('admin.save_error')}: {e}")
                    
                    with save_col2:
                        if st.button(f"❌ {t('admin.cancel')}", use_container_width=True):
                            st.session_state['admin_save_mode'] = False
                            st.rerun()
                else:
                    st.warning(f"⚠️ {t('admin.no_customers')}")
                    if st.button(f"❌ {t('admin.cancel')}", use_container_width=True):
                        st.session_state['admin_save_mode'] = False
                        st.rerun()
        else:
            # المستخدم العادي - حفظ مباشر
            if st.button(f"💾 {t('admin.save_estimate')}", use_container_width=True):
                try:
                    db = DatabaseManager()
                    car_image = st.session_state.get('uploaded_image')
                    transaction_id = db.create_transaction(
                        user_id=st.session_state.user['id'],
                        car_data=car_data,
                        estimated_price=estimated_price,
                        condition_analysis=analysis,
                        car_image_bytes=car_image
                    )
                    
                    st.session_state.last_transaction_id = transaction_id
                    st.success(f"✅ {t('admin.estimate_saved')}")
                except Exception as e:
                    st.error(f"❌ {t('admin.save_error')}: {e}")
    
    with col2:
        if st.button(f"💳 {t('admin.go_to_payment')}", use_container_width=True, type="primary"):
            # حفظ السعر للخطوة القادمة
            st.session_state.last_price = estimated_price
            
            # التحقق من توثيق الهوية قبل الانتقال للدفع
            user = st.session_state.user
            is_verified = bool(user.get('id_number') and user.get('nationality') and user.get('license_number'))
            
            if is_verified:
                navigate_to('checkout')
            else:
                st.warning(f"⚠️ {t('admin.verify_id_first')}")
                navigate_to('verify_identity')
    
    with col3:
        if st.button(f"📧 {t('invoices.send_email')}", use_container_width=True):
            try:
                # إنشاء الفاتورة أولاً إذا لم تكن موجودة
                if not st.session_state.get('invoice_path'):
                    generator = InvoiceGenerator()
                    transaction_data = {
                        'id': st.session_state.get('last_transaction_id', datetime.now().strftime('%Y%m%d%H%M%S')),
                        'estimated_price': prediction_result['estimated_price'],
                        **car_data
                    }
                    invoice_path = generator.generate_car_invoice(
                        transaction_data,
                        st.session_state.user
                    )
                    st.session_state.invoice_path = invoice_path
                
                # إرسال البريد
                notifier = NotificationManager()
                
                if not notifier.email_configured:
                    st.warning(f"⚠️ {t('admin.email_incomplete')}")
                else:
                    result = notifier.send_invoice_email(
                        recipient_email=st.session_state.user['email'],
                        invoice_path=st.session_state.invoice_path,
                        user_data=st.session_state.user,
                        transaction_data={
                            'estimated_price': prediction_result['estimated_price'],
                            **car_data
                        }
                    )
                    
                    if result['success']:
                        st.success(f"✅ {t('messages.success')}")
                    else:
                        st.error(f"❌ {result['message']}")
            except Exception as e:
                st.error(f"❌ {t('messages.error')}: {e}")
    
    st.markdown("---")
    
    # أزرار التنقل
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"🏎️ {t('results.new_evaluation')}", use_container_width=True):
            # مسح البيانات السابقة
            st.session_state.uploaded_image = None
            st.session_state.car_details = {}
            st.session_state.analysis_result = None
            st.session_state.prediction_data = None
            navigate_to('predict')
    
    with col2:
        if st.button(f"✏️ {t('buttons.edit')}", use_container_width=True, help=t('buttons.back')):
            navigate_to('predict')
            
    with col3:
        if st.button(f"🏠 {t('nav.home')}", type="secondary", use_container_width=True):
            navigate_to('home')


# ======================
# صفحة الفواتير
# ======================

def invoices_page():
    """صفحة الفواتير السابقة"""
    # Render universal header
    render_universal_header(t('nav.invoices'), "📄 " + t('invoices.previous'))
    
    # تحديث بيانات المستخدم
    if st.session_state.get('user'):
        db = DatabaseManager()
        fresh_user = db.get_user_by_id(st.session_state.user['id'])
        if fresh_user:
            st.session_state.user = fresh_user
    
    try:
        db = DatabaseManager()
        
        # === قسم مسح المستندات (للأدمن فقط) ===
        if st.session_state.user.get('role') == 'admin':
            st.markdown("---")
            ocr_title = t('ocr.title')
            st.markdown(f"""
            <style>
                .ocr-header {{
                    background: linear-gradient(135deg, #0E1117 0%, #161B22 100%);
                    padding: 15px 25px;
                    border-radius: 15px;
                    margin: 20px 0;
                    border: 2px solid #D4AF37;
                }}
                .ocr-header h3 {{
                    color: #D4AF37;
                    margin: 0;
                    font-size: 1.2rem;
                }}
            </style>
            <div class="ocr-header">
            <h3>📋 {ocr_title}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # اختيار المستخدم للتعديل
            users = db.get_all_users()
            user_options = {f"{u.get('full_name') or u.get('username')} ({u.get('email')})": u for u in users}
            
            selected_user_key = st.selectbox(
                f"👤 {t('ocr.select_customer')}",
                options=list(user_options.keys()),
                key="ocr_user_select"
            )
            
            selected_user = user_options.get(selected_user_key)
            
            if selected_user:
                ocr_tab1, ocr_tab2, ocr_tab3 = rtl_tabs([f"🪪 {t('ocr.id_card_tab')}", f"🏎️ {t('ocr.driver_license_tab')}", f"📋 {t('ocr.previous_transactions_tab')}"])
                
                with ocr_tab1:
                    st.write(f"**📄 {t('ocr.front_side')}**")
                    id_front_col1, id_front_col2 = st.columns(2)
                    with id_front_col1:
                        id_front_file = st.file_uploader(t('ocr.upload_image'), type=['jpg', 'jpeg', 'png'], key="inv_id_front")
                    with id_front_col2:
                        id_front_cam = st.camera_input(f"📷 {t('ocr.capture_image')}", key="inv_id_front_cam")
                    
                    id_front_bytes = id_front_file.getvalue() if id_front_file else (id_front_cam.getvalue() if id_front_cam else None)
                    
                    st.write(f"**📄 {t('ocr.back_side')}**")
                    id_back_col1, id_back_col2 = st.columns(2)
                    with id_back_col1:
                        id_back_file = st.file_uploader(t('ocr.upload_image'), type=['jpg', 'jpeg', 'png'], key="inv_id_back")
                    with id_back_col2:
                        id_back_cam = st.camera_input(f"📷 {t('ocr.capture_image')}", key="inv_id_back_cam")
                    
                    id_back_bytes = id_back_file.getvalue() if id_back_file else (id_back_cam.getvalue() if id_back_cam else None)
                    
                    if id_front_bytes and id_back_bytes:
                        if st.button(f"🔍 {t('ocr.scan_id_card')}", key="inv_scan_id"):
                            with st.spinner(t('ocr.scanning')):
                                from utils.ocr_scanner import DocumentScanner
                                scanner = DocumentScanner()
                                front_result = scanner.scan_id_card(id_front_bytes)
                                back_result = scanner.scan_id_card(id_back_bytes)
                                
                                combined = {}
                                unclear = t('ocr.unclear')
                                for key in ['full_name', 'id_number', 'nationality', 'date_of_birth', 'gender', 'expiry_date', 'address']:
                                    front_val = front_result.get(key, unclear)
                                    back_val = back_result.get(key, unclear)
                                    combined[key] = front_val if front_val != unclear else back_val
                                
                                # حفظ البيانات في قاعدة البيانات للمستخدم المحدد
                                db.update_user(selected_user['id'], **{k: v for k, v in combined.items() if v != unclear})
                                st.success(f"✅ {t('ocr.id_updated')} {selected_user.get('full_name') or selected_user.get('username')}!")
                                st.rerun()
                
                with ocr_tab2:
                    st.write(f"**📄 {t('ocr.front_side')}**")
                    lic_front_col1, lic_front_col2 = st.columns(2)
                    with lic_front_col1:
                        lic_front_file = st.file_uploader(t('ocr.upload_image'), type=['jpg', 'jpeg', 'png'], key="inv_lic_front")
                    with lic_front_col2:
                        lic_front_cam = st.camera_input(f"📷 {t('ocr.capture_image')}", key="inv_lic_front_cam")
                    
                    lic_front_bytes = lic_front_file.getvalue() if lic_front_file else (lic_front_cam.getvalue() if lic_front_cam else None)
                    
                    st.write(f"**📄 {t('ocr.back_side')}**")
                    lic_back_col1, lic_back_col2 = st.columns(2)
                    with lic_back_col1:
                        lic_back_file = st.file_uploader(t('ocr.upload_image'), type=['jpg', 'jpeg', 'png'], key="inv_lic_back")
                    with lic_back_col2:
                        lic_back_cam = st.camera_input(f"📷 {t('ocr.capture_image')}", key="inv_lic_back_cam")
                    
                    lic_back_bytes = lic_back_file.getvalue() if lic_back_file else (lic_back_cam.getvalue() if lic_back_cam else None)
                    
                    if lic_front_bytes and lic_back_bytes:
                        if st.button(f"🔍 {t('ocr.scan_license')}", key="inv_scan_lic"):
                            with st.spinner(t('ocr.scanning')):
                                from utils.ocr_scanner import DocumentScanner
                                scanner = DocumentScanner()
                                front_result = scanner.scan_driver_license(lic_front_bytes)
                                back_result = scanner.scan_driver_license(lic_back_bytes)
                                
                                combined = {}
                                unclear = t('ocr.unclear')
                                for key in ['license_number', 'license_type', 'license_class', 'expiry_date', 'blood_type']:
                                    front_val = front_result.get(key, unclear)
                                    back_val = back_result.get(key, unclear)
                                    combined[key] = front_val if front_val != unclear else back_val
                                
                                # حفظ البيانات في قاعدة البيانات للمستخدم المحدد
                                db.update_user(selected_user['id'], 
                                    license_number=combined.get('license_number') if combined.get('license_number') != unclear else None,
                                    license_type=combined.get('license_type') if combined.get('license_type') != unclear else None,
                                    license_class=combined.get('license_class') if combined.get('license_class') != unclear else None,
                                    license_expiry=combined.get('expiry_date') if combined.get('expiry_date') != unclear else None,
                                    blood_type=combined.get('blood_type') if combined.get('blood_type') != unclear else None
                                )
                                st.success(f"✅ {t('ocr.license_updated')} {selected_user.get('full_name') or selected_user.get('username')}!")
                                st.rerun()
                
                with ocr_tab3:
                    # عرض معاملات المستخدم المحدد
                    user_trans = db.get_user_transactions(selected_user['id'])
                    
                    if user_trans:
                        st.info(f"📊 {t('ocr.transactions_count')}: {len(user_trans)}")
                        
                        for ut in user_trans:
                            with st.expander(f"🏎️ {ut.get('brand', '')} {ut.get('model', '')} - €{ut.get('estimated_price', 0):,.0f}"):
                                # وضع التعديل
                                edit_key = f"edit_trans_{ut['id']}"
                                
                                if st.session_state.get(edit_key):
                                    # نموذج التعديل
                                    with st.form(f"edit_form_{ut['id']}"):
                                        e_col1, e_col2 = st.columns(2)
                                        
                                        with e_col1:
                                            new_brand = st.text_input(t('ocr.brand'), value=ut.get('brand', ''), key=f"e_brand_{ut['id']}")
                                            new_model = st.text_input(t('ocr.model'), value=ut.get('model', ''), key=f"e_model_{ut['id']}")
                                            new_year = st.number_input(t('ocr.year'), value=int(ut.get('manufacture_year', 2020)), key=f"e_year_{ut['id']}")
                                            new_car_type = st.text_input(t('ocr.car_type'), value=ut.get('car_type', ''), key=f"e_type_{ut['id']}")
                                        
                                        with e_col2:
                                            new_mileage = st.number_input(f"{t('ocr.mileage')} (km)", value=int(ut.get('mileage', 0)), key=f"e_miles_{ut['id']}")
                                            new_price = st.number_input(f"{t('ocr.estimated_price')} (€)", value=float(ut.get('estimated_price', 0)), key=f"e_price_{ut['id']}")
                                            new_fuel = st.text_input(t('ocr.fuel_type'), value=ut.get('fuel_type', ''), key=f"e_fuel_{ut['id']}")
                                            new_condition = st.text_input(t('ocr.condition'), value=ut.get('condition', ''), key=f"e_cond_{ut['id']}")
                                            new_color = st.text_input(t('predict.color'), value=ut.get('color', ''), key=f"e_color_{ut['id']}")
                                        
                                        submit_col1, submit_col2 = st.columns(2)
                                        with submit_col1:
                                            if st.form_submit_button(f"💾 {t('ocr.save_changes')}", type="primary"):
                                                db.update_transaction(ut['id'], 
                                                    brand=new_brand,
                                                    model=new_model,
                                                    manufacture_year=new_year,
                                                    car_type=new_car_type,
                                                    mileage=new_mileage,
                                                    estimated_price=new_price,
                                                    fuel_type=new_fuel,
                                                    condition=new_condition,
                                                    color=new_color
                                                )
                                                st.session_state[edit_key] = False
                                                st.success(f"✅ {t('ocr.saved')}")
                                                st.rerun()
                                        with submit_col2:
                                            if st.form_submit_button(f"❌ {t('ocr.cancel')}"):
                                                st.session_state[edit_key] = False
                                                st.rerun()
                                else:
                                    # عرض البيانات
                                    d_col1, d_col2 = st.columns(2)
                                    with d_col1:
                                        st.write(f"**{t('ocr.brand')}:** {ut.get('brand', '-')}")
                                        st.write(f"**{t('ocr.model')}:** {ut.get('model', '-')}")
                                        st.write(f"**{t('ocr.year')}:** {ut.get('manufacture_year', '-')}")
                                        st.write(f"**{t('ocr.car_type')}:** {ut.get('car_type', '-')}")
                                    with d_col2:
                                        st.write(f"**{t('ocr.mileage')}:** {ut.get('mileage', 0):,} km")
                                        st.write(f"**{t('ocr.estimated_price')}:** €{ut.get('estimated_price', 0):,.0f}")
                                        st.write(f"**{t('ocr.fuel_type')}:** {ut.get('fuel_type', '-')}")
                                        st.write(f"**{t('ocr.condition')}:** {ut.get('condition', '-')}")
                                        st.write(f"**{t('predict.color')}:** {ut.get('color', '-')}")
                                        st.write(f"**{t('ocr.date')}:** {str(ut.get('created_at', ''))[:10]}")
                                    
                                    st.markdown("---")
                                    
                                    btn1, btn2, btn3 = st.columns(3)
                                    with btn1:
                                        if st.button(f"✏️ {t('ocr.edit')}", key=f"btn_edit_{ut['id']}"):
                                            st.session_state[edit_key] = True
                                            st.rerun()
                                    with btn2:
                                        if st.button(f"🗑️ {t('ocr.delete')}", key=f"btn_del_{ut['id']}"):
                                            db.delete_transaction(ut['id'])
                                            st.success(f"✅ {t('ocr.deleted')}")
                                            st.rerun()
                                    with btn3:
                                        if st.button(f"🖨️ {t('ocr.print')}", key=f"btn_print_{ut['id']}"):
                                            st.session_state.selected_transaction = ut
                                            st.session_state.car_data = {
                                                'brand': ut.get('brand'),
                                                'model': ut.get('model'),
                                                'manufacture_year': ut.get('manufacture_year'),
                                                'mileage': ut.get('mileage'),
                                                'car_type': ut.get('car_type'),
                                                'estimated_price': ut.get('estimated_price')
                                            }
                                            st.session_state.estimated_price = ut.get('estimated_price', 0)
                                            st.session_state.last_transaction_id = ut['id']
                                            st.session_state.page = 'checkout'
                                            st.rerun()
                    else:
                        st.info(t('admin.no_customer_transactions'))
        
        else:
            # === المستخدم العادي - عرض معاملاته السابقة ===
            user = st.session_state.user
            user_transactions = db.get_user_transactions(user['id'])
            
            if user_transactions:
                st.markdown(f"### 📋 {t('invoices.your_transactions', 'Your Previous Transactions')}")
                st.info(f"📊 {t('invoices.total_transactions', 'Total transactions')}: {len(user_transactions)}")
                
                for trans in user_transactions:
                    with st.expander(f"🏎️ {trans.get('brand', '')} {trans.get('model', '')} - €{trans.get('estimated_price', 0):,.2f} ({str(trans.get('created_at', ''))[:10]})"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**{t('admin.car_type')}:** {trans.get('car_type', '-')}")
                            st.write(f"**{t('admin.brand')}:** {trans.get('brand', '-')}")
                            st.write(f"**{t('admin.model')}:** {trans.get('model', '-')}")
                            st.write(f"**{t('admin.year')}:** {trans.get('manufacture_year', '-')}")
                        with col2:
                            st.write(f"**{t('admin.mileage')}:** {trans.get('mileage', 0):,} km")
                            st.write(f"**{t('admin.fuel_type')}:** {trans.get('fuel_type', '-')}")
                            st.write(f"**{t('admin.condition')}:** {trans.get('condition', '-')}")
                            st.write(f"**{t('predict.color')}:** {trans.get('color', '-')}")
                        
                        st.markdown("---")
                        st.markdown(f"### 💰 {t('admin.estimated_price')}: €{trans.get('estimated_price', 0):,.2f}")
                        
                        # زر للانتقال إلى الدفع/الطباعة
                        if st.button(f"🖨️ {t('buttons.print_invoice', 'Print Invoice')}", key=f"user_print_{trans['id']}"):
                            st.session_state.selected_transaction = trans
                            st.session_state.car_data = {
                                'brand': trans.get('brand'),
                                'model': trans.get('model'),
                                'manufacture_year': trans.get('manufacture_year'),
                                'mileage': trans.get('mileage'),
                                'car_type': trans.get('car_type'),
                                'estimated_price': trans.get('estimated_price')
                            }
                            st.session_state.estimated_price = trans.get('estimated_price', 0)
                            st.session_state.last_transaction_id = trans['id']
                            st.session_state.page = 'checkout'
                            st.rerun()
            else:
                st.info(t('invoices.no_transactions_yet', 'You have no previous transactions. Start by evaluating your car!'))
                
                if st.button(f"🏎️ {t('nav.predict')}", type="primary"):
                    navigate_to('predict')
                
    except Exception as e:
        st.error(f"❌ {t('messages.error')}: {e}")


# ======================
# صفحة الملف الشخصي
# ======================

def profile_page():
    """صفحة الملف الشخصي"""
    # Render universal header
    render_universal_header(t('nav.profile'), "👤 " + t('profile.personal_info'))
    
    user = st.session_state.user
    
    # تحديث البيانات من قاعدة البيانات
    db = DatabaseManager()
    fresh_user = db.get_user_by_id(user['id'])
    if fresh_user:
        st.session_state.user = fresh_user
        user = fresh_user
    
    # الحصول على بيانات المستندات المحفوظة في الجلسة (من OCR)
    id_data = st.session_state.get('id_card_data', {})
    lic_data = st.session_state.get('license_data', {})
    
    # دمج البيانات: الأولوية لقاعدة البيانات، ثم OCR
    default_name = user.get('full_name') or id_data.get('full_name', '')
    default_id_number = user.get('id_number') or id_data.get('id_number', '')
    default_nationality = user.get('nationality') or id_data.get('nationality', '')
    default_dob = user.get('date_of_birth') or user.get('birth_date') or id_data.get('date_of_birth', '')
    default_license = user.get('license_number') or lic_data.get('license_number', '')
    default_license_type = user.get('license_type') or lic_data.get('license_type', '')
    default_license_expiry = user.get('license_expiry') or lic_data.get('expiry_date', '')
    
    # الحقول الإضافية - الأولوية لقاعدة البيانات
    default_gender = user.get('gender') or id_data.get('gender', '')
    if default_gender == 'غير واضح':
        default_gender = ''
    default_id_expiry = user.get('expiry_date') or id_data.get('expiry_date', '')
    if default_id_expiry == 'غير واضح':
        default_id_expiry = ''
    default_address = user.get('address') or id_data.get('address', '')
    if default_address == 'غير واضح':
        default_address = ''
    default_license_class = user.get('license_class') or lic_data.get('license_class', '')
    if default_license_class == 'غير واضح':
        default_license_class = ''
    default_blood_type = user.get('blood_type') or lic_data.get('blood_type', '')
    if default_blood_type == 'غير واضح':
        default_blood_type = ''
    
    st.subheader(f"📝 {t('profile.personal_info')}")
    
    # === أزرار التحكم الرئيسية ===
    # الأدمن لا يحتاج وضع التعديل الآلي لأنه متاح في صفحة الفواتير
    is_admin_user = user.get('role') == 'admin'
    
    if is_admin_user:
        # الأدمن: 3 أزرار فقط (بدون التعديل الآلي)
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        
        with btn_col1:
            show_data = st.button(f"👁️ {t('profile.show_data')}", key="show_profile_data_btn", type="primary" if not st.session_state.get('show_profile_data') else "secondary")
            if show_data:
                st.session_state['show_profile_data'] = True
                st.session_state['edit_mode'] = None
                st.rerun()
        
        with btn_col2:
            if st.button(f"✏️ {t('profile.edit_manual')}", key="edit_manual"):
                st.session_state['show_profile_data'] = True
                st.session_state['edit_mode'] = 'manual'
                st.rerun()
        
        with btn_col3:
            if st.button(f"📋 {t('admin.go_to_invoices')}", key="go_to_invoices"):
                navigate_to('invoices')
        
        st.info(f"💡 {t('admin.admin_scan_hint')}")
    else:
        # المستخدم العادي: 4 أزرار
        btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
        
        with btn_col1:
            show_data = st.button(f"👁️ {t('profile.show_data')}", key="show_profile_data_btn", type="primary" if not st.session_state.get('show_profile_data') else "secondary")
            if show_data:
                st.session_state['show_profile_data'] = True
                st.session_state['edit_mode'] = None
                st.rerun()
        
        with btn_col2:
            if st.button(f"✏️ {t('profile.edit_manual')}", key="edit_manual"):
                st.session_state['show_profile_data'] = True
                st.session_state['edit_mode'] = 'manual'
                st.rerun()
        
        with btn_col3:
            if st.button(f"📷 {t('profile.edit_auto')}", key="edit_auto"):
                st.session_state['show_profile_data'] = True
                st.session_state['edit_mode'] = 'auto'
                st.rerun()
        
        with btn_col4:
            if st.button(f"⏭️ {t('profile.skip_data')}", key="skip_data"):
                # الانتقال مباشرة إلى صفحة الدفع والتعاقد بدون إدخال بيانات البطاقات
                st.toast(f"💡 {t('profile.skip_hint')}", icon="ℹ️")
                navigate_to('checkout')
    
    st.markdown("---")
    
    # === عرض البيانات (إذا تم الضغط على إظهار البيانات) ===
    if st.session_state.get('show_profile_data'):
        
        # === وضع التعديل الآلي بالتصوير ===
        if st.session_state.get('edit_mode') == 'auto':
            st.info(f"📷 **{t('profile.auto_edit_mode')}**")
            
            auto_tab1, auto_tab2 = rtl_tabs([f"🪪 {t('profile.id_card_full')}", f"🏎️ {t('profile.driver_license_full')}"])
            
            with auto_tab1:
                # الوجه الأمامي والخلفي جنباً إلى جنب
                front_col, back_col = st.columns(2)
                
                with front_col:
                    st.write(f"**📄 {t('profile.front_face')}:**")
                    id_front_file = st.file_uploader(t('profile.upload_image'), type=['jpg', 'jpeg', 'png'], key="auto_id_front")
                    id_front_cam = st.camera_input(f"📷 {t('profile.capture_image')}", key="auto_id_front_cam")
                
                with back_col:
                    st.write(f"**📄 {t('profile.back_face')}:**")
                    id_back_file = st.file_uploader(t('profile.upload_image'), type=['jpg', 'jpeg', 'png'], key="auto_id_back")
                    id_back_cam = st.camera_input(f"📷 {t('profile.capture_image')}", key="auto_id_back_cam")
                
                id_front_bytes = id_front_file.getvalue() if id_front_file else (id_front_cam.getvalue() if id_front_cam else None)
                id_back_bytes = id_back_file.getvalue() if id_back_file else (id_back_cam.getvalue() if id_back_cam else None)
                
                if id_front_bytes and id_back_bytes:
                    if st.button(f"🔍 {t('profile.scan_id_btn')}", key="scan_id_auto"):
                        with st.spinner(t('messages.loading')):
                            from utils.ocr_scanner import DocumentScanner
                            scanner = DocumentScanner()
                            front_result = scanner.scan_id_card(id_front_bytes)
                            back_result = scanner.scan_id_card(id_back_bytes)
                            
                            combined = {}
                            for key in ['full_name', 'id_number', 'nationality', 'date_of_birth', 'gender', 'expiry_date', 'address']:
                                front_val = front_result.get(key, 'غير واضح')
                                back_val = back_result.get(key, 'غير واضح')
                                combined[key] = front_val if front_val != 'غير واضح' else back_val
                            
                            # حفظ البيانات في قاعدة البيانات
                            db.update_user(user['id'], **{k: v for k, v in combined.items() if v != 'غير واضح'})
                            st.session_state.id_card_data = combined
                            st.success(f"✅ {t('admin.id_data_saved')}")
                            st.rerun()
            
            with auto_tab2:
                # الوجه الأمامي والخلفي جنباً إلى جنب
                lic_front_col, lic_back_col = st.columns(2)
                
                with lic_front_col:
                    st.write(f"**📄 {t('profile.front_face')}:**")
                    lic_front_file = st.file_uploader(t('profile.upload_image'), type=['jpg', 'jpeg', 'png'], key="auto_lic_front")
                    lic_front_cam = st.camera_input(f"📷 {t('profile.capture_image')}", key="auto_lic_front_cam")
                
                with lic_back_col:
                    st.write(f"**📄 {t('profile.back_face')}:**")
                    lic_back_file = st.file_uploader(t('profile.upload_image'), type=['jpg', 'jpeg', 'png'], key="auto_lic_back")
                    lic_back_cam = st.camera_input(f"📷 {t('profile.capture_image')}", key="auto_lic_back_cam")
                
                lic_front_bytes = lic_front_file.getvalue() if lic_front_file else (lic_front_cam.getvalue() if lic_front_cam else None)
                lic_back_bytes = lic_back_file.getvalue() if lic_back_file else (lic_back_cam.getvalue() if lic_back_cam else None)
                
                if lic_front_bytes and lic_back_bytes:
                    if st.button(f"🔍 {t('profile.scan_lic_btn')}", key="scan_lic_auto"):
                        with st.spinner(t('messages.loading')):
                            from utils.ocr_scanner import DocumentScanner
                            scanner = DocumentScanner()
                            front_result = scanner.scan_driver_license(lic_front_bytes)
                            back_result = scanner.scan_driver_license(lic_back_bytes)
                            
                            combined = {}
                            for key in ['license_number', 'license_type', 'license_class', 'expiry_date', 'blood_type']:
                                front_val = front_result.get(key, 'غير واضح')
                                back_val = back_result.get(key, 'غير واضح')
                                combined[key] = front_val if front_val != 'غير واضح' else back_val
                            
                            # حفظ البيانات في قاعدة البيانات
                            db.update_user(user['id'], 
                                license_number=combined.get('license_number') if combined.get('license_number') != 'غير واضح' else None,
                                license_type=combined.get('license_type') if combined.get('license_type') != 'غير واضح' else None,
                                license_class=combined.get('license_class') if combined.get('license_class') != 'غير واضح' else None,
                                license_expiry=combined.get('expiry_date') if combined.get('expiry_date') != 'غير واضح' else None,
                                blood_type=combined.get('blood_type') if combined.get('blood_type') != 'غير واضح' else None
                            )
                            st.session_state.license_data = combined
                            st.success(f"✅ {t('messages.success')}")
                            st.rerun()
            
            # زر العودة لوضع العرض
            if st.button(f"⬅️ {t('profile.back_to_view')}", key="back_to_view"):
                st.session_state['edit_mode'] = None
                st.rerun()
        
        # === وضع التعديل اليدوي أو العرض العادي ===
        else:
            # عرض البيانات الحالية في جدول أنيق
            if st.session_state.get('edit_mode') != 'manual':
                st.markdown(f"### 📋 {t('profile.current_data_header')}")
                
                # بناء العنوان الكامل
                address_parts = [user.get('street_name', ''), user.get('building_number', ''), user.get('postal_code', ''), user.get('city', '')]
                constructed_address = ' - '.join([p for p in address_parts if p])
                full_address = constructed_address if constructed_address else (user.get('address') or '-')
                
                # Dynamic Styles using f-strings
                data_html = f"""
<style>
    body {{ font-family: "Source Sans Pro", sans-serif; }}
    .profile-table {{ width: 100%; border-collapse: collapse; background: linear-gradient(135deg, #0E1117 0%, #161B22 100%); border-radius: 12px; overflow: hidden; }}
    .profile-table th {{ background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 12px; text-align: {('right' if st.session_state.language == 'ar' else 'left')}; }}
    .profile-table td {{ padding: 10px 15px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #ffffff; text-align: {('right' if st.session_state.language == 'ar' else 'left')}; }}
    .profile-table tr:hover {{ background: rgba(79, 172, 254, 0.1); }}
    .section-header {{ background: rgba(241, 196, 15, 0.15) !important; }}
    .section-header td {{ color: #f1c40f; font-weight: bold; }}
</style>
<table class="profile-table">
    <tr class="section-header"><td colspan="2">🪪 {t('profile.personal_data_header')}</td></tr>
    <tr><td>{t('profile.full_name')}</td><td>{user.get('full_name') or '-'}</td></tr>
    <tr><td>{t('profile.id_number')}</td><td>{user.get('id_number') or '-'}</td></tr>
    <tr><td>{t('profile.nationality')}</td><td>{user.get('nationality') or '-'}</td></tr>
    <tr><td>{t('profile.dob')}</td><td>{user.get('date_of_birth') or user.get('birth_date') or '-'}</td></tr>
    <tr><td>{t('profile.gender')}</td><td>{user.get('gender') or '-'}</td></tr>
    <tr><td>{t('profile.phone')}</td><td>{user.get('phone') or '-'}</td></tr>
    <tr><td>{t('profile.email')}</td><td>{user.get('email') or '-'}</td></tr>
    
    <tr class="section-header"><td colspan="2">🏠 {t('profile.address_header')}</td></tr>
    <tr><td>{t('profile.address')}</td><td>{full_address}</td></tr>
    
    <tr class="section-header"><td colspan="2">🏎️ {t('profile.license_header')}</td></tr>
    <tr><td>{t('profile.lic_no')}</td><td>{user.get('license_number') or '-'}</td></tr>
    <tr><td>{t('profile.lic_type')}</td><td>{user.get('license_type') or '-'}</td></tr>
    <tr><td>{t('profile.lic_class')}</td><td>{user.get('license_class') or '-'}</td></tr>
    <tr><td>{t('profile.lic_expiry')}</td><td>{user.get('license_expiry') or '-'}</td></tr>
    <tr><td>{t('profile.blood_type')}</td><td>{user.get('blood_type') or '-'}</td></tr>
</table>
"""
                components.html(data_html, height=750, scrolling=True)
                
                # زر إخفاء البيانات
                if st.button(f"🙈 {t('profile.hide_data')}", key="hide_data"):
                    st.session_state['show_profile_data'] = False
                    st.rerun()
            
            # === نموذج التعديل اليدوي ===
            if st.session_state.get('edit_mode') == 'manual':
                st.info(f"✏️ **{t('profile.manual_edit_mode')}**")
                
                with st.form("profile_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        full_name = st.text_input(t('profile.full_name'), value=default_name)
                        email = st.text_input(t('profile.email'), value=user.get('email', ''), disabled=True)
                        phone = st.text_input(t('profile.phone'), value=user.get('phone', ''))
                    
                    with col2:
                        username = st.text_input(t('login.username'), value=user.get('username', ''), disabled=True)
                        id_number = st.text_input(t('profile.id_number'), value=default_id_number)
                        nationality = st.text_input(t('profile.nationality'), value=default_nationality)
                    
                    st.markdown("---")
                    
                    # بيانات البطاقة الشخصية
                    st.write(f"**🪪 {t('profile.id_card_full')}:**")
                    id_col1, id_col2 = st.columns(2)
                    
                    with id_col1:
                        date_of_birth = st.text_input(t('profile.dob'), value=default_dob)
                        # تحديد index للجنس من قاعدة البيانات أو OCR
                        gender_index = 0
                        if default_gender == 'ذكر' or default_gender == 'Male':
                            gender_index = 1
                        elif default_gender == 'أنثى' or default_gender == 'Female':
                            gender_index = 2
                        gender = st.selectbox(t('profile.gender'), ["", t('profile.male'), t('profile.female')], index=gender_index)
                    
                    with id_col2:
                         id_expiry = st.text_input(t('profile.id_expiry'), value=default_id_expiry)
                    
                    st.markdown("---")
                    
                    # حقول العنوان المنفصلة
                    st.write(f"**🏠 {t('profile.address_header')}:**")
                    addr_col1, addr_col2 = st.columns(2)
                    
                    with addr_col1:
                        street_name = st.text_input(t('profile.street'), value=user.get('street_name') or '')
                        building_number = st.text_input(t('profile.building_no'), value=user.get('building_number') or '')
                    
                    with addr_col2:
                        postal_code = st.text_input(t('profile.postal_code'), value=user.get('postal_code') or '')
                        city = st.text_input(t('profile.city'), value=user.get('city') or '')
                    
                    st.markdown("---")
                    
                    # بيانات رخصة القيادة
                    st.write(f"**🏎️ {t('profile.driver_license_full')}:**")
                    lic_col1, lic_col2 = st.columns(2)
                    
                    with lic_col1:
                        license_number = st.text_input(t('profile.lic_no'), value=default_license)
                        license_type = st.text_input(t('profile.lic_type'), value=default_license_type)
                    
                    with lic_col2:
                        license_class = st.text_input(t('profile.lic_class'), value=default_license_class)
                        license_expiry = st.text_input(t('profile.lic_expiry'), value=default_license_expiry)
                    
                    blood_type = st.text_input(t('profile.blood_type'), value=default_blood_type)
                    
                    st.markdown("---")
                    
                    submitted = st.form_submit_button(f"💾 {t('profile.save')}", use_container_width=True, type="primary")
                    
                    if submitted:
                        try:
                            db = DatabaseManager()
                            db.update_user(
                                user['id'],
                                full_name=full_name,
                                phone=phone,
                                id_number=id_number if id_number else None,
                                nationality=nationality if nationality else None,
                                date_of_birth=date_of_birth if date_of_birth else None,
                                gender=gender if gender else None,
                                expiry_date=id_expiry if id_expiry else None,
                                # حقول العنوان المنفصلة
                                street_name=street_name if street_name else None,
                                building_number=building_number if building_number else None,
                                postal_code=postal_code if postal_code else None,
                                city=city if city else None,
                                # حقول الرخصة
                                license_number=license_number if license_number else None,
                                license_type=license_type if license_type else None,
                                license_class=license_class if license_class else None,
                                license_expiry=license_expiry if license_expiry else None,
                                blood_type=blood_type if blood_type else None
                            )
                            
                            # تحديث الجلسة
                            st.session_state.user.update({
                                'full_name': full_name,
                                'phone': phone,
                                'id_number': id_number,
                                'nationality': nationality,
                                'date_of_birth': date_of_birth,
                                'gender': gender,
                                'expiry_date': id_expiry,
                                'street_name': street_name,
                                'building_number': building_number,
                                'postal_code': postal_code,
                                'city': city,
                                'license_number': license_number,
                                'license_type': license_type,
                                'license_class': license_class,
                                'license_expiry': license_expiry,
                                'blood_type': blood_type
                            })
                            
                            st.success(f"✅ {t('messages.saved')}")
                            st.session_state['edit_mode'] = None
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ {t('messages.error')}: {e}")
                
                # زر إلغاء التعديل
                if st.button(f"❌ {t('profile.cancel_edit')}", key="cancel_edit_manual"):
                    st.session_state['edit_mode'] = None
                    st.rerun()
    
    # === عرض معلومات الأمان دائماً إذا كانت البيانات معروضة ===
    if st.session_state.get('show_profile_data'):
        st.markdown("---")
    
    # معلومات الأمان
    st.subheader(f"🔒 {t('profile.security', 'Security')}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        created_at = user.get('created_at', t('messages.unknown', 'Unknown'))
        st.write(f"**{t('profile.created_at', 'Registration Date')}:** {str(created_at)[:10] if created_at else t('messages.unknown', 'Unknown')}")
        
        last_login = user.get('last_login', t('messages.unknown', 'Unknown'))
        st.write(f"**{t('profile.last_login', 'Last Login')}:** {str(last_login)[:19] if last_login else t('messages.unknown', 'Unknown')}")
    
    with col2:
        if st.button(f"🔄 {t('profile.change_password')}", use_container_width=True):
            navigate_to('change_password')
    
    st.markdown("---")
    
    # إحصائيات
    try:
        db = DatabaseManager()
        transactions = db.get_user_transactions(user['id'], limit=1000)
        
        count = len(transactions) if transactions else 0
        total_value = sum(trans.get('estimated_price', 0) for trans in transactions) if transactions else 0
        avg_price = total_value / count if count > 0 else 0
        
        # Render Unified Statistics Component
        components.html(get_profile_stats_html(count, total_value, avg_price), height=180)
        
    except Exception as e:
        print(f"Stats Error: {e}")
    
    st.markdown("---")
    
    # قسم مسح المستندات
    st.subheader(f"📋 {t('profile.document_scan', 'Document Scanning (OCR)')}")
    st.info(t('profile.document_scan_hint', 'Upload or capture an image of your ID card or driver\'s license to auto-extract data'))
    
    from utils import DocumentScanner
    
    # الأدمن لا يحتاج تبويب العقود والتقديرات (لأن معاملاته محفوظة باسم العملاء)
    if user.get('role') == 'admin':
        doc_tab1, doc_tab2 = rtl_tabs([f"🪪 {t('profile.id_card', 'ID Card')}", f"🏎️ {t('profile.driver_license', 'Driver License')}"])
        contracts_tab = None
        est_tab = None
    else:
        doc_tab1, doc_tab2, contracts_tab, est_tab = rtl_tabs([f"🪪 {t('profile.id_card', 'ID Card')}", f"🏎️ {t('profile.driver_license', 'Driver License')}", f"📜 {t('profile.contracts', 'Contracts & Invoices')}", f"🏎️ {t('profile.recent_estimates', 'Recent Estimates')}"])
    
    if est_tab:
        st.subheader(f"📋 {t('profile.recent_estimates', 'Recent Price Estimates')}")
        user_trans = db.get_user_transactions(user['id'], limit=10)
        
        if user_trans:
            for tr in user_trans:
                with st.expander(f"{tr.get('brand')} {tr.get('model')} ({tr.get('manufacture_year')}) - {tr.get('estimated_price', 0):,.2f} €"):
                    e_col1, e_col2 = st.columns([1, 2])
                    
                    with e_col1:
                        img_path = tr.get('image_path')
                        if img_path and Path(img_path).exists():
                            st.image(img_path, width=150)
                        else:
                            st.info(t('profile.no_image'))
                            
                    with e_col2:
                         st.write(f"**{t('profile.model')}:** {tr.get('brand')} {tr.get('model')} {tr.get('manufacture_year')}")
                         st.write(f"**{t('profile.mileage')}:** {tr.get('mileage')} km")
                         st.write(f"**{t('profile.car_condition')}:** {tr.get('condition_score')}/10 ({tr.get('confidence', 'Low')})")
                         st.write(f"**{t('profile.estimated_price')}:** {tr.get('estimated_price', 0):,.2f} €")
                         
                         st.markdown("---")
                         act_c1, act_c2 = st.columns(2)
                         
                         # === Delete Action ===
                         with act_c1:
                             if st.button(f"❌ {t('profile.delete_estimate')}", key=f"del_tr_{tr['id']}"):
                                 if db.delete_transaction(tr['id']):
                                     st.success(t('profile.delete_success'))
                                     st.rerun()
                                 else:
                                     st.error(t('messages.error'))
                         
                         # === Edit Action ===
                         with act_c2:
                             # Toggle Edit Mode using Session State
                             edit_key = f"edit_mode_{tr['id']}"
                             if st.button(f"✏️ {t('profile.edit_estimate_data')}", key=f"btn_ed_{tr['id']}"):
                                 st.session_state[edit_key] = not st.session_state.get(edit_key, False)
                    
                    # === Edit Form ===
                    if st.session_state.get(f"edit_mode_{tr['id']}", False):
                        st.markdown(f"#### 📝 {t('profile.edit_estimate_title')}")
                        with st.form(key=f"form_ed_{tr['id']}"):
                            n_brand = st.text_input(t('results.brand'), value=tr.get('brand', ''))
                            n_model = st.text_input(t('results.model'), value=tr.get('model', ''))
                            n_year = st.number_input(t('results.year'), value=tr.get('manufacture_year', 2020))
                            n_km = st.number_input(t('profile.mileage'), value=tr.get('mileage', 0))
                            n_price = st.number_input(f"{t('profile.estimated_price')} (€)", value=tr.get('estimated_price', 0.0))
                            
                            if st.form_submit_button(f"💾 {t('profile.save_changes')}"):
                                updates = {
                                    'brand': n_brand, 'model': n_model, 
                                    'manufacture_year': n_year, 'mileage': n_km,
                                    'estimated_price': n_price
                                }
                                if db.update_transaction(tr['id'], updates):
                                    st.success(t('profile.update_success'))
                                    st.session_state[f"edit_mode_{tr['id']}"] = False
                                    st.rerun()
                                else:
                                    st.error(t('messages.error'))

        else:
            st.info(t('invoices.no_invoices'))

    with doc_tab1:
        st.write(f"**📄 {t('profile.front_side', 'Front Side')}:**")
        id_front_col1, id_front_col2 = st.columns(2)
        
        with id_front_col1:
            id_front_file = st.file_uploader(t('profile.upload_front', 'Upload Front Side'), type=['jpg', 'jpeg', 'png'], key="id_front_upload")
        with id_front_col2:
            id_front_cam = st.camera_input(f"📷 {t('predict.capture_image')}", key="id_front_cam")
        
        id_front_bytes = id_front_file.getvalue() if id_front_file else (id_front_cam.getvalue() if id_front_cam else None)
        
        st.write(f"**📄 {t('profile.back_side', 'Back Side')}:**")
        id_back_col1, id_back_col2 = st.columns(2)
        
        with id_back_col1:
            id_back_file = st.file_uploader(t('profile.upload_back', 'Upload Back Side'), type=['jpg', 'jpeg', 'png'], key="id_back_upload")
        with id_back_col2:
            id_back_cam = st.camera_input(f"📷 {t('predict.capture_image')}", key="id_back_cam")
        
        id_back_bytes = id_back_file.getvalue() if id_back_file else (id_back_cam.getvalue() if id_back_cam else None)
        
        # عرض الصور
        if id_front_bytes or id_back_bytes:
            img_col1, img_col2 = st.columns(2)
            if id_front_bytes:
                with img_col1:
                    st.image(id_front_bytes, caption=t('profile.front_side'), width=200)
            if id_back_bytes:
                with img_col2:
                    st.image(id_back_bytes, caption=t('profile.back_side'), width=200)
        
        if id_front_bytes and id_back_bytes:
            if st.button(f"🔍 {t('profile.scan_id')}", key="scan_id"):
                with st.spinner(t('messages.loading')):
                    scanner = DocumentScanner()
                    
                    # مسح الوجه الأمامي
                    front_result = scanner.scan_id_card(id_front_bytes)
                    # مسح الوجه الخلفي
                    back_result = scanner.scan_id_card(id_back_bytes)
                    
                    # دمج النتائج
                    combined = {}
                    for key in ['full_name', 'id_number', 'nationality', 'date_of_birth', 'gender', 'expiry_date', 'issue_date', 'address', 'place_of_birth']:
                        front_val = front_result.get(key, 'غير واضح')
                        back_val = back_result.get(key, 'غير واضح')
                        combined[key] = front_val if front_val != 'غير واضح' else back_val
                    
                    st.success(f"✅ {t('messages.success')}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**الاسم:** {combined.get('full_name', 'غير واضح')}")
                        st.write(f"**رقم الهوية:** {combined.get('id_number', 'غير واضح')}")
                        st.write(f"**الجنسية:** {combined.get('nationality', 'غير واضح')}")
                        st.write(f"**العنوان:** {combined.get('address', 'غير واضح')}")
                    with col2:
                        st.write(f"**تاريخ الميلاد:** {combined.get('date_of_birth', 'غير واضح')}")
                        st.write(f"**تاريخ الإصدار:** {combined.get('issue_date', 'غير واضح')}")
                        st.write(f"**تاريخ الانتهاء:** {combined.get('expiry_date', 'غير واضح')}")
                        st.write(f"**الجنس:** {combined.get('gender', 'غير واضح')}")
                    
                    st.session_state.id_card_data = combined
                    
                    if st.button(f"💾 {t('profile.save_data')}", key="save_id"):
                        try:
                            db = DatabaseManager()
                            db.update_user(user['id'], **{k: v for k, v in combined.items() if v != 'غير واضح'})
                            st.success(f"✅ {t('messages.saved')}")
                        except Exception as e:
                            st.error(f"❌ {t('messages.error')}: {e}")
        elif id_front_bytes or id_back_bytes:
            st.warning(f"⚠️ {t('profile.document_scan_hint')}")
    
    with doc_tab2:
        st.write(f"**📄 {t('profile.front_side')}:**")
        lic_front_col1, lic_front_col2 = st.columns(2)
        
        with lic_front_col1:
            lic_front_file = st.file_uploader(t('profile.upload_front'), type=['jpg', 'jpeg', 'png'], key="lic_front_upload")
        with lic_front_col2:
            lic_front_cam = st.camera_input(f"📷 {t('predict.capture_image')}", key="lic_front_cam")
        
        lic_front_bytes = lic_front_file.getvalue() if lic_front_file else (lic_front_cam.getvalue() if lic_front_cam else None)
        
        st.write(f"**📄 {t('profile.back_side')}:**")
        lic_back_col1, lic_back_col2 = st.columns(2)
        
        with lic_back_col1:
            lic_back_file = st.file_uploader(t('profile.upload_back'), type=['jpg', 'jpeg', 'png'], key="lic_back_upload")
        with lic_back_col2:
            lic_back_cam = st.camera_input(f"📷 {t('predict.capture_image')}", key="lic_back_cam")
        
        lic_back_bytes = lic_back_file.getvalue() if lic_back_file else (lic_back_cam.getvalue() if lic_back_cam else None)
        
        # عرض الصور
        if lic_front_bytes or lic_back_bytes:
            img_col1, img_col2 = st.columns(2)
            if lic_front_bytes:
                with img_col1:
                    st.image(lic_front_bytes, caption=t('profile.front_side'), width=200)
            if lic_back_bytes:
                with img_col2:
                    st.image(lic_back_bytes, caption=t('profile.back_side'), width=200)
        
        if lic_front_bytes and lic_back_bytes:
            if st.button(f"🔍 {t('profile.scan_license')}", key="scan_lic"):
                with st.spinner(t('messages.loading')):
                    scanner = DocumentScanner()
                    
                    # مسح الوجه الأمامي
                    front_result = scanner.scan_driver_license(lic_front_bytes)
                    # مسح الوجه الخلفي
                    back_result = scanner.scan_driver_license(lic_back_bytes)
                    
                    # دمج النتائج
                    combined = {}
                    for key in ['full_name', 'license_number', 'license_type', 'license_class', 'expiry_date', 'issue_date', 'blood_type', 'nationality', 'restrictions', 'issuing_authority']:
                        front_val = front_result.get(key, 'غير واضح')
                        back_val = back_result.get(key, 'غير واضح')
                        combined[key] = front_val if front_val != 'غير واضح' else back_val
                    
                    st.success(f"✅ {t('messages.success')}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**الاسم:** {combined.get('full_name', 'غير واضح')}")
                        st.write(f"**رقم الرخصة:** {combined.get('license_number', 'غير واضح')}")
                        st.write(f"**نوع الرخصة:** {combined.get('license_type', 'غير واضح')}")
                        st.write(f"**فئة الرخصة:** {combined.get('license_class', 'غير واضح')}")
                    with col2:
                        st.write(f"**تاريخ الإصدار:** {combined.get('issue_date', 'غير واضح')}")
                        st.write(f"**تاريخ الانتهاء:** {combined.get('expiry_date', 'غير واضح')}")
                        st.write(f"**فصيلة الدم:** {combined.get('blood_type', 'غير واضح')}")
                        st.write(f"**{t('profile.lic_class')}:** {combined.get('restrictions', t('admin.no_restrictions'))}")
                    
                    st.session_state.license_data = combined
                    
                    if st.button(f"💾 {t('profile.save_data')}", key="save_lic"):
                        try:
                            db = DatabaseManager()
                            db.update_user(user['id'], 
                                license_number=combined.get('license_number') if combined.get('license_number') != 'غير واضح' else None,
                                license_type=combined.get('license_type') if combined.get('license_type') != 'غير واضح' else None,
                                license_expiry=combined.get('expiry_date') if combined.get('expiry_date') != 'غير واضح' else None
                            )
                            st.success(f"✅ {t('messages.saved')}")
                        except Exception as e:
                            st.error(f"❌ {t('messages.error')}: {e}")
        elif lic_front_bytes or lic_back_bytes:
            st.warning(f"⚠️ {t('profile.document_scan_hint')}")
            
    if contracts_tab:
        with contracts_tab:
            st.subheader(f"📜 {t('profile.contracts')}")
        
            try:
                db = DatabaseManager()
                contracts = db.get_user_contracts(user['id'])
            
                if not contracts:
                    st.info(f"💡 {t('contracts.no_active')}")
                else:
                    for contract in contracts:
                        try:
                            car_info = json.loads(contract.get('car_details', '{}'))
                        except:
                            car_info = {'brand': t('contracts.default_brand'), 'model': t('contracts.unknown_car')}
                            
                        total = contract.get('total_amount', 0)
                        paid = contract.get('paid_amount', 0)
                        remaining = total - paid
                        progress = (paid / total) if total > 0 else 0
                        
                        with st.expander(f"📌 {t('contracts.contract')} #{contract['id']} - {car_info.get('brand')} {car_info.get('model')} ({str(contract.get('created_at'))[:10]})"):
                            
                            # عرض تفاصيل السيارة داخل العقد
                            st.markdown(f"**🏎️ {t('contracts.car_summary')}:**")
                            cd_col1, cd_col2, cd_col3, cd_col4 = st.columns(4)
                            with cd_col1:
                                st.write(f"**{t('predict.brand')}:** {car_info.get('brand', '-')}")
                            with cd_col2:
                                st.write(f"**{t('predict.model')}:** {car_info.get('model', '-')}")
                            with cd_col3:
                                st.write(f"**{t('predict.year')}:** {car_info.get('manufacture_year', '-')}")
                            with cd_col4:
                                st.write(f"**{t('predict.mileage')}:** {car_info.get('mileage', 0)} km")
                            
                            st.markdown("---")

                            # 1. أجراءات العقد (حفظ - طباعة عقد - طباعة فواتير)
                            col_c1, col_c2, col_c3, col_c4 = st.columns([1, 1, 1, 2])
                            
                            # زر الحفظ (Save)
                            with col_c1:
                                if st.button(f"💾 {t('buttons.save')}", key=f"save_k_{contract['id']}"):
                                    gen = InvoiceGenerator()
                                    c_path = gen.generate_contract(contract['id'], contract, user, st.session_state.get('language', 'de'))
                                    st.session_state[f'contract_pdf_{contract["id"]}'] = c_path
                                
                                if f'contract_pdf_{contract["id"]}' in st.session_state:
                                    with open(st.session_state[f'contract_pdf_{contract["id"]}'], "rb") as f:
                                        st.download_button(f"⬇️", f, file_name=f"Contract_{contract['id']}.pdf", mime="application/pdf", key=f"dl_save_{contract['id']}")

                            # زر طباعة العقد (Print Contract) - الانتقال إلى صفحة Checkout
                            with col_c2:
                                if st.button(f"📄 {t('contracts.print_contract')}", key=f"print_k_{contract['id']}"):
                                    st.session_state.selected_transaction = contract
                                    st.session_state.car_data = car_info
                                    st.session_state.estimated_price = total
                                    st.session_state.last_transaction_id = contract['id']
                                    st.session_state.current_contract_id = contract['id']
                                    st.session_state.page = 'checkout'
                                    st.rerun()
                            
                            # زر طباعة الفواتير (Print Invoices)
                            with col_c3:
                                if st.button(f"🧾 {t('contracts.print_invoices')}", key=f"print_invoices_{contract['id']}"):
                                    st.session_state.selected_transaction = contract
                                    st.session_state.car_data = car_info
                                    st.session_state.estimated_price = total
                                    st.session_state.last_transaction_id = contract['id']
                                    st.session_state.current_contract_id = contract['id']
                                    st.session_state.page = 'checkout'
                                    st.rerun()
                            
                            with col_c4:
                                st.write(f"💰 **{t('contracts.total_value')}:** {total:,.2f} €")
                                due_day = contract.get('payment_due_day', 1)
                                grace = contract.get('grace_period', 3)
                                st.caption(f"📅 {t('contracts.due_day')}: {due_day} | ⏳ {t('contracts.grace_period')}: {grace}")
                             
                            st.progress(progress)
                            st.caption(f"✅ {t('contracts.paid')}: {paid:,.2f} € ({progress*100:.1f}%) | ⏳ {t('contracts.remaining')}: {remaining:,.2f} €")
                            
                            if contract.get('reschedule_reason'):
                                new_date = contract.get('next_payment_date', 'غير محدد')
                                st.warning(f"⚠️ **{t('contracts.reschedule_warning')}** **{new_date}**.")
                                st.info(f"📋 **{t('contracts.reason')}:** {contract.get('reschedule_reason')}")
                                st.markdown("---")
                            
                            st.subheader(f"🧾 {t('contracts.history')}")
                            payments = db.get_contract_payments(contract['id'])
                            if payments:
                                for pay in payments:
                                    status_color = "red"
                                    if pay['status'] == 'verified': status_color = "green"
                                    elif pay['status'] == 'pending': status_color = "orange"
                                    
                                    p_col1, p_col2 = st.columns([3, 1])
                                    with p_col1:
                                        st.markdown(f"🔹 **{pay['payment_date']}**: {pay['amount']:,.2f} € - <span style='color:{status_color}'>{pay['status']}</span>", unsafe_allow_html=True)
                                    with p_col2:
                                        if pay['status'] == 'verified':
                                            if st.button(f"🖨️ {t('contracts.reprint')}", key=f"reprint_{pay['id']}"):
                                                gen = InvoiceGenerator()
                                                re_path = gen.generate_receipt(f"INV-{pay['id']}", {'amount': pay['amount'], 'method': pay['payment_method'], 'date': pay['payment_date'], 'ref': pay['transaction_ref']}, {'total_amount': total, 'total_paid': paid, 'remaining_balance': remaining}, user)
                                                st.session_state[f'inv_re_{pay["id"]}'] = re_path
                                            
                                            if f'inv_re_{pay["id"]}' in st.session_state:
                                                with open(st.session_state[f'inv_re_{pay["id"]}'], "rb") as f:
                                                    st.download_button("⬇️", f, file_name=f"Inv_{pay['id']}.pdf", key=f"dl_re_{pay['id']}")
                                        else:
                                            st.caption(t('contracts.pending_review'))
                            else:
                                st.info(t('contracts.no_payments'))

                            st.markdown("---")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if remaining <= 1.0:
                                    st.success(f"🎉 {t('contracts.settled')}")
                                    if st.button(f"📥 {t('contracts.issue_settlement')} #{contract['id']}"):
                                        generator = InvoiceGenerator()
                                        path = generator.generate_settlement(contract['id'], {'total_paid': paid}, user)
                                        st.session_state[f'settlement_{contract["id"]}'] = path
                                        st.success(t('messages.success'))
                                    
                                    if f'settlement_{contract["id"]}' in st.session_state:
                                        with open(st.session_state[f'settlement_{contract["id"]}'], "rb") as f:
                                            st.download_button(t('contracts.download_settlement'), f, file_name=f"Settlement_{contract['id']}.pdf", key=f"dl_{contract['id']}")
                                else:
                                    st.warning(f"⚠️ {t('contracts.payment_pending')}")
                            
                            with col2:
                                if remaining > 1.0:
                                    if st.button(f"💳 {t('contracts.pay_new')}", key=f"pay_{contract['id']}"):
                                        st.session_state.current_contract_id = contract['id']
                                        st.session_state.last_price = remaining
                                        st.session_state.car_details = car_info
                                        navigate_to('checkout')
            except Exception as e:
                st.error(f"{t('admin.contract_load_error')}: {e}")


# ======================
# صفحة تغيير كلمة المرور
# ======================

def change_password_page():
    """صفحة تغيير كلمة المرور"""
    st.markdown(f"""
    <div class="main-header">
        <h1>🔐 {t('admin.change_password_title')}</h1>
    </div>
    <div class="sub-header">
        <p>{t('admin.change_password_hint')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("change_password_form"):
            current_password = st.text_input(t('admin.current_password'), type="password")
            new_password = st.text_input(t('admin.new_password_label'), type="password")
            confirm_password = st.text_input(t('admin.confirm_new_password'), type="password")
            
            submitted = st.form_submit_button(t('profile.change_password'), use_container_width=True)
            
            if submitted:
                if not current_password or not new_password or not confirm_password:
                    st.error("⚠️ يرجى ملء جميع الحقول")
                elif new_password != confirm_password:
                    st.error("⚠️ كلمتا المرور الجديدتان غير متطابقتين")
                else:
                    auth = AuthManager()
                    success, message = auth.change_password(
                        st.session_state.user['id'],
                        current_password,
                        new_password
                    )
                    
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")
        
        st.markdown("---")
        
        if st.button(f"← {t('admin.back_to_profile')}", use_container_width=True):
            navigate_to('profile')


# ======================
# لوحة تحكم المشرف
# ======================

def admin_page():
    """صفحة لوحة تحكم المشرف"""
    # التحقق من الصلاحيات
    if st.session_state.user.get('role') != 'admin':
        st.error(f"⛔ {t('messages.error')}")
        navigate_to('home')
        return
    
    # Render universal header
    render_universal_header(t('admin.title'), "👑 " + t('admin.dashboard'))
    
    # القائمة الجانبية
    admin_menu = st.selectbox(
        t('admin.title'),
        [t('admin.statistics'), t('admin.users'), t('admin.employees'), t('admin.transactions'), t('admin.financial_settings')]
    )
    
    db = DatabaseManager()
    
    if admin_menu == t('admin.statistics'):
        stats = db.get_statistics()
        
        # تنسيق احترافي للإحصائيات
        # تنسيق احترافي للإحصائيات (Unified Dashboard)
        get_admin_dashboard_html(stats)
    
    elif admin_menu == t('admin.users'):
        st.subheader(f"👥 {t('admin.users')}")
        
        users = db.get_all_users()
        
        if users:
            for user in users:
                with st.expander(f"👤 {user.get('username', 'مستخدم')} - {user.get('email', '')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**{t('admin.username')}:** {user.get('username')}")
                        st.write(f"**{t('admin.email')}:** {user.get('email')}")
                        st.write(f"**{t('admin.role')}:** {user.get('role', 'user')}")
                    
                    with col2:
                        st.write(f"**{t('admin.registration_date')}:** {str(user.get('created_at', ''))[:10]}")
                        st.write(f"**{t('admin.last_login')}:** {str(user.get('last_login', ''))[:19]}")
                        status = f"{t('admin.active')} ✅" if user.get('is_active') else f"{t('admin.inactive')} ❌"
                        st.write(f"**{t('admin.status')}:** {status}")
                    
                    st.markdown("---")
                    
                    # أزرار التعديل والحذف
                    btn_col1, btn_col2, btn_col3 = st.columns(3)
                    
                    with btn_col1:
                        # تعديل الدور
                        new_role = st.selectbox(
                            t('admin.role'),
                            ["user", "admin"],
                            index=0 if user.get('role') == 'user' else 1,
                            key=f"role_{user.get('id')}"
                        )
                        if st.button(f"💾 {t('admin.save_role')}", key=f"save_role_{user.get('id')}"):
                            db.update_user(user.get('id'), role=new_role)
                            st.success(f"✅ {t('messages.success')}")
                            st.rerun()
                    
                    with btn_col2:
                        # تفعيل/تعطيل
                        if user.get('is_active'):
                            if st.button(f"🚫 {t('admin.disable_account')}", key=f"disable_{user.get('id')}", type="secondary"):
                                db.update_user(user.get('id'), is_active=0)
                                st.warning(t('messages.success'))
                                st.rerun()
                        else:
                            if st.button(f"✅ {t('admin.enable_account')}", key=f"enable_{user.get('id')}", type="primary"):
                                db.update_user(user.get('id'), is_active=1)
                                st.success(t('messages.success'))
                                st.rerun()
                    
                    # تغيير كلمة المرور
                    st.markdown("---")
                    with st.expander(f"🔐 {t('admin.change_password')}"):
                        new_password = st.text_input(
                            t('admin.new_password'),
                            type="password",
                            key=f"new_pass_{user.get('id')}"
                        )
                        confirm_password = st.text_input(
                            t('admin.confirm_password'),
                            type="password",
                            key=f"confirm_pass_{user.get('id')}"
                        )
                        if st.button(f"💾 {t('admin.save_password')}", key=f"save_pass_{user.get('id')}"):
                            if new_password and confirm_password:
                                if new_password == confirm_password:
                                    from auth import AuthManager
                                    auth = AuthManager()
                                    hashed = auth.hash_password(new_password)
                                    db.update_user(user.get('id'), password_hash=hashed)
                                    st.success(f"✅ {t('messages.success')}")
                                else:
                                    st.error(f"❌ {t('admin.passwords_not_match')}")
                            else:
                                st.error(f"❌ {t('admin.enter_password')}")
        else:
            st.info(t('admin.no_users'))
    
    

            
    elif admin_menu == t('admin.financial_settings'):
        st.subheader(f"💰 {t('admin.interest_rates')}")
        
        # جلب الإعدادات الحالية
        db = DatabaseManager()
        current_rates = db.get_setting('interest_rates', {
            '3_months': 0.0,
            '12_months': 0.12,
            '24_months': 0.18,
            'default': 0.10
        })
        
        st.info(t('admin.financial_info_msg'))
        
        with st.form("interest_rates_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                rate_3 = st.number_input(t('admin.interest_3_months'), 
                                       min_value=0.0, max_value=1.0, step=0.01, 
                                       value=float(current_rates.get('3_months', 0.0)),
                                       format="%.2f")
                st.caption(f"{t('admin.percentage')}: {rate_3*100:.1f}%")

            with col2:
                rate_12 = st.number_input(t('admin.interest_12_months'), 
                                        min_value=0.0, max_value=1.0, step=0.01,
                                        value=float(current_rates.get('12_months', 0.12)),
                                        format="%.2f")
                st.caption(f"{t('admin.percentage')}: {rate_12*100:.1f}%")

            with col3:
                rate_24 = st.number_input(t('admin.interest_24_months'), 
                                        min_value=0.0, max_value=1.0, step=0.01,
                                        value=float(current_rates.get('24_months', 0.18)),
                                        format="%.2f")
                st.caption(f"{t('admin.percentage')}: {rate_24*100:.1f}%")
                
            submitted = st.form_submit_button(f"💾 {t('admin.save_financial_settings')}")
            
            if submitted:
                new_settings = {
                    '3_months': rate_3,
                    '12_months': rate_12,
                    '24_months': rate_24,
                    'default': 0.10 # ثابت حالياً أو يمكن إضافته
                }
                db.set_setting('interest_rates', new_settings)
                st.success(f"✅ {t('messages.success')}")

    elif admin_menu == t('admin.employees'):
        st.subheader(f"👔 {t('admin.employees')}")
        
        # عرض الموظفين
        employees = db.get_all_employees()
        
        if employees:
            # إنشاء قائمة بأسماء الموظفين للاختيار
            emp_options = {}
            for emp in employees:
                status_icon = "✅" if emp.get('is_active') else "❌"
                full_name = f"{emp.get('first_name', '')} {emp.get('last_name', '')}".strip()
                emp_options[f"{full_name} {status_icon}"] = emp
            
            # Selectbox لاختيار الموظف
            selected_emp_name = st.selectbox(
                f"👤 {t('admin.select_employee')}",
                options=[""] + list(emp_options.keys()),
                key="select_employee_dropdown"
            )
            
            if selected_emp_name and selected_emp_name in emp_options:
                emp = emp_options[selected_emp_name]
                full_name = f"{emp.get('first_name', '')} {emp.get('last_name', '')}".strip()
                
                # جدول البيانات الشخصية والمالية
                employee_table = f"""
                <style>
                    .emp-table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin: 10px 0;
                        font-size: 14px;
                        background: linear-gradient(135deg, #0E1117 0%, #161B22 100%);
                        border-radius: 10px;
                        overflow: hidden;
                    }}
                    .emp-table th {{
                        background: linear-gradient(135deg, #161B22 0%, #0E1117 100%);
                        color: #f1c40f;
                        padding: 12px 15px;
                        text-align: right;
                        font-weight: 600;
                        border-bottom: 2px solid #f1c40f;
                    }}
                    .emp-table td {{
                        padding: 10px 15px;
                        border-bottom: 1px solid #2a2a4a;
                        color: #ffffff;
                    }}
                    .emp-table tr:hover {{
                        background: rgba(241, 196, 15, 0.1);
                    }}
                    .emp-table .label {{
                        color: #a0a0c0;
                        font-weight: 500;
                        width: 40%;
                    }}
                    .emp-table .value {{
                        color: #ffffff;
                        font-weight: 600;
                    }}
                    .section-title {{
                        color: #f1c40f;
                        font-size: 16px;
                        font-weight: 600;
                        margin: 15px 0 10px 0;
                        padding-bottom: 5px;
                        border-bottom: 2px solid #f1c40f;
                    }}
                </style>
                
                <div class="section-title">📋 {t('admin.emp_personal_data')}</div>
                <table class="emp-table">
                    <tr><td class="label">{t('admin.emp_full_name')}</td><td class="value">{full_name}</td></tr>
                    <tr><td class="label">{t('admin.phone')}</td><td class="value">{emp.get('phone', '-')}</td></tr>
                    <tr><td class="label">{t('admin.email')}</td><td class="value">{emp.get('email', '-')}</td></tr>
                    <tr><td class="label">{t('admin.address')}</td><td class="value">{emp.get('address', '-')}</td></tr>
                    <tr><td class="label">{t('admin.hire_date')}</td><td class="value">{emp.get('hire_date', '-') or '-'}</td></tr>
                </table>
                
                <div class="section-title">💰 {t('admin.emp_financial_data')}</div>
                <table class="emp-table">
                    <tr><td class="label">{t('admin.monthly_salary')}</td><td class="value">€{emp.get('monthly_salary', 0):,.2f}</td></tr>
                    <tr><td class="label">{t('admin.feiertags_geld')}</td><td class="value">€{emp.get('feiertags_geld', 0):,.2f}</td></tr>
                    <tr><td class="label">{t('admin.urlaubsgeld')}</td><td class="value">€{emp.get('urlaubsgeld', 0):,.2f}</td></tr>
                </table>
                
                <div class="section-title">🏖️ {t('admin.emp_leaves')}</div>
                <table class="emp-table">
                    <tr><td class="label">{t('admin.annual_leave')}</td><td class="value">{emp.get('annual_leave', 0)}</td></tr>
                    <tr><td class="label">{t('admin.sick_leave')}</td><td class="value">{emp.get('sick_leave', 0)}</td></tr>
                    <tr><td class="label">{t('admin.unpaid_leave')}</td><td class="value">{emp.get('unpaid_leave', 0)}</td></tr>
                </table>
                
                <div class="section-title">📝 {t('admin.notes')}</div>
                <table class="emp-table">
                    <tr><td class="label">{t('admin.notes')}</td><td class="value">{emp.get('notes') or '-'}</td></tr>
                </table>
                """
                
                st.markdown(employee_table, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # أزرار التحكم
                btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
                
                with btn_col1:
                    if emp.get('is_active'):
                        if st.button(f"🚫 {t('admin.disable_account')}", key=f"emp_disable_{emp.get('id')}"):
                            db.update_employee(emp.get('id'), is_active=0)
                            st.rerun()
                    else:
                        if st.button(f"✅ {t('admin.enable_account')}", key=f"emp_enable_{emp.get('id')}"):
                            db.update_employee(emp.get('id'), is_active=1)
                            st.rerun()
                
                with btn_col2:
                    if st.button(f"✏️ {t('admin.edit_employee')}", key=f"emp_edit_{emp.get('id')}", type="primary"):
                        st.session_state[f"edit_emp_{emp.get('id')}"] = True
                
                with btn_col3:
                    # حذف الموظف مع تأكيد - زرين
                    if st.session_state.get(f"confirm_del_{emp.get('id')}", False):
                        # عرض زر التأكيد النهائي
                        if st.button(f"⚠️ {t('admin.delete_permanent')}", key=f"emp_delete_{emp.get('id')}", type="primary"):
                            db.delete_employee(emp.get('id'))
                            st.session_state[f"confirm_del_{emp.get('id')}"] = False
                            st.rerun()
                        if st.button(f"❌ {t('buttons.cancel')}", key=f"cancel_del_{emp.get('id')}"):
                            st.session_state[f"confirm_del_{emp.get('id')}"] = False
                            st.rerun()
                    else:
                        # زر طلب الحذف
                        if st.button(f"🗑️ {t('admin.confirm_delete')}", key=f"ask_del_{emp.get('id')}", type="secondary"):
                            st.session_state[f"confirm_del_{emp.get('id')}"] = True
                
                with btn_col4:
                    if st.session_state.get(f"edit_emp_{emp.get('id')}"):
                        if st.button(f"❌ {t('admin.cancel_edit')}", key=f"emp_cancel_edit_{emp.get('id')}"):
                            st.session_state[f"edit_emp_{emp.get('id')}"] = False
                            st.rerun()
                
                # نموذج تعديل البيانات
                if st.session_state.get(f"edit_emp_{emp.get('id')}"):
                    st.markdown("---")
                    st.subheader(f"✏️ {t('admin.edit_employee')}")
                    
                    with st.form(key=f"edit_emp_form_{emp.get('id')}"):
                        # البيانات الشخصية
                        st.markdown(f"**📋 {t('admin.emp_personal_data')}:**")
                        edit_col1, edit_col2 = st.columns(2)
                        
                        with edit_col1:
                            edit_first_name = st.text_input(f"{t('admin.first_name')} *", value=emp.get('first_name', ''), key=f"ef_first_{emp.get('id')}")
                            edit_last_name = st.text_input(t('admin.last_name'), value=emp.get('last_name') or '', key=f"ef_last_{emp.get('id')}")
                            edit_phone = st.text_input(t('admin.phone'), value=emp.get('phone') or '', key=f"ef_phone_{emp.get('id')}")
                        
                        with edit_col2:
                            edit_email = st.text_input(t('admin.email'), value=emp.get('email') or '', key=f"ef_email_{emp.get('id')}")
                            edit_address = st.text_input(t('admin.address'), value=emp.get('address') or '', key=f"ef_addr_{emp.get('id')}")
                        
                        st.markdown("---")
                        
                        # البيانات المالية
                        st.markdown(f"**💰 {t('admin.emp_financial_data')}:**")
                        fin_col1, fin_col2, fin_col3 = st.columns(3)
                        
                        with fin_col1:
                            edit_salary = st.number_input(f"{t('admin.monthly_salary')} (€)", value=float(emp.get('monthly_salary') or 0), min_value=0.0, key=f"ef_sal_{emp.get('id')}")
                        with fin_col2:
                            edit_feiertags = st.number_input(f"{t('admin.feiertags_geld')} (€)", value=float(emp.get('feiertags_geld') or 0), min_value=0.0, key=f"ef_fei_{emp.get('id')}")
                        with fin_col3:
                            edit_urlaub = st.number_input(f"{t('admin.urlaubsgeld')} (€)", value=float(emp.get('urlaubsgeld') or 0), min_value=0.0, key=f"ef_url_{emp.get('id')}")
                        
                        st.markdown("---")
                        
                        # الإجازات
                        st.markdown(f"**🏖️ {t('admin.emp_leaves')}:**")
                        leave_col1, leave_col2, leave_col3 = st.columns(3)
                        
                        with leave_col1:
                            edit_annual = st.number_input(t('admin.annual_leave'), value=int(emp.get('annual_leave') or 0), min_value=0, key=f"ef_ann_{emp.get('id')}")
                        with leave_col2:
                            edit_sick = st.number_input(t('admin.sick_leave'), value=int(emp.get('sick_leave') or 0), min_value=0, key=f"ef_sick_{emp.get('id')}")
                        with leave_col3:
                            edit_unpaid = st.number_input(t('admin.unpaid_leave'), value=int(emp.get('unpaid_leave') or 0), min_value=0, key=f"ef_unp_{emp.get('id')}")
                        
                        st.markdown("---")
                        
                        # الملاحظات
                        edit_notes = st.text_area(f"📝 {t('admin.notes')}", value=emp.get('notes') or '', key=f"ef_notes_{emp.get('id')}")
                        
                        # زر الحفظ
                        if st.form_submit_button(f"💾 {t('admin.save_changes')}", type="primary", use_container_width=True):
                            if edit_first_name:
                                db.update_employee(
                                    emp.get('id'),
                                    first_name=edit_first_name,
                                    last_name=edit_last_name,
                                    phone=edit_phone,
                                    email=edit_email,
                                    address=edit_address,
                                    monthly_salary=edit_salary,
                                    feiertags_geld=edit_feiertags,
                                    urlaubsgeld=edit_urlaub,
                                    annual_leave=edit_annual,
                                    sick_leave=edit_sick,
                                    unpaid_leave=edit_unpaid,
                                    notes=edit_notes
                                )
                                st.session_state[f"edit_emp_{emp.get('id')}"] = False
                                st.success(f"✅ {t('admin.edits_saved')}")
                                st.rerun()
                            else:
                                st.error(f"❌ {t('admin.first_name_required')}")
        else:
            st.info(t('admin.no_employees'))
    
    elif admin_menu == t('admin.transactions'):
        st.subheader(f"💼 {t('admin.contracts_header')}")
        
        # Tabs for easier navigation
        tab1, tab2 = rtl_tabs([f"💰 {t('admin.tab_contracts')}", f"🏎️ {t('admin.tab_estimates')}"])
        
        with tab1:
            st.info(t('admin.contracts_desc'))
            contracts = db.get_all_contracts_with_users()
            
            if contracts:
                for c in contracts:
                    with st.expander(f"{t('admin.contract')} #{c['id']} - {c['full_name']} ({c['created_at'][:10]})"):
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            st.write(f"**{t('admin.client')}:** {c['full_name']}")
                            st.write(f"**{t('admin.plan')}:** {c.get('plan_type', 'Full')}")
                        with col2:
                            st.write(f"**{t('admin.total_price')}:** {c['total_amount']:,.2f} €")
                             
                        # --- إدارة الجدولة (Scheduling) ---
                        with st.expander(f"📅 {t('admin.schedule_management')}"):
                            sch_c1, sch_c2 = st.columns(2)
                            with sch_c1:
                                new_due_day = st.selectbox(t('admin.due_day'), [1, 15], index=0 if c.get('payment_due_day', 1) == 1 else 1, key=f"dead_{c['id']}")
                                new_grace = st.slider(t('admin.grace_period'), 1, 3, c.get('grace_period', 3), key=f"grc_{c['id']}")
                                if st.button(t('admin.update_settings'), key=f"upd_set_{c['id']}"):
                                    db.update_contract_schedule(c['id'], due_day=new_due_day, grace=new_grace)
                                    st.success(t('messages.success'))
                                    st.rerun()
                            
                            with sch_c2:
                                st.caption(t('admin.defer_title'))
                                resch_date = st.date_input(t('admin.new_date'), key=f"res_d_{c['id']}")
                                resch_reason = st.text_input(t('admin.defer_reason'), placeholder="e.g. holiday", key=f"res_r_{c['id']}")
                                if st.button(t('admin.confirm_defer'), key=f"conf_res_{c['id']}"):
                                    if resch_reason:
                                        db.update_contract_schedule(c['id'], next_date=str(resch_date), reason=resch_reason)
                                        st.success(t('messages.success'))
                                    else:
                                        st.error(t('messages.error'))
                        
                        # === أزرار الطباعة - الانتقال إلى صفحة Checkout ===
                        adm_col1, adm_col2 = st.columns(2)
                        
                        # استخراج بيانات السيارة من العقد
                        try:
                            car_info = json.loads(c.get('car_details', '{}'))
                        except:
                            car_info = {'brand': 'Vehicle', 'model': 'Unknown'}
                        
                        with adm_col1:
                            # زر طباعة العقد - الانتقال إلى Checkout
                            if st.button(f"🖨️ {t('admin.print_contract')}", key=f"adm_contract_{c['id']}", use_container_width=True, type="primary"):
                                st.session_state.selected_transaction = c
                                st.session_state.car_data = car_info
                                st.session_state.estimated_price = c.get('total_amount', 0)
                                st.session_state.last_transaction_id = c['id']
                                st.session_state.current_contract_id = c['id']
                                st.session_state.page = 'checkout'
                                st.rerun()
                        
                        with adm_col2:
                            # زر طباعة الفواتير - الانتقال إلى Checkout
                            if st.button(f"📄 {t('admin.print_invoices')}", key=f"adm_invoices_{c['id']}", use_container_width=True):
                                st.session_state.selected_transaction = c
                                st.session_state.car_data = car_info
                                st.session_state.estimated_price = c.get('total_amount', 0)
                                st.session_state.last_transaction_id = c['id']
                                st.session_state.current_contract_id = c['id']
                                st.session_state.page = 'checkout'
                                st.rerun()

                        st.markdown("---")

                        st.write(f"**{t('admin.transaction_history')}:**")
                        payments = db.get_contract_payments(c['id'])
                        if payments:
                            for pay in payments:
                                pc1, pc2 = st.columns([3, 1])
                                with pc1:
                                    st.write(f"- {t('admin.payment')} {pay['payment_date']}: {pay['amount']:,.2f} € ({pay['status']})")
                                with pc2:
                                    if pay['status'] == 'verified':
                                        if st.button(f"🖨️ {t('admin.invoice')}", key=f"adm_pr_inv_{pay['id']}"):
                                             gen = InvoiceGenerator()
                                             # Need summary for invoice
                                             summary = db.get_contract_summary(c['id'])
                                             re_path = gen.generate_receipt(f"INV-{pay['id']}", {'amount': pay['amount'], 'method': pay['payment_method'], 'date': pay['payment_date'], 'ref': pay['transaction_ref']}, summary, c)
                                             st.session_state[f'adm_inv_{pay['id']}'] = re_path
                                        if f'adm_inv_{pay['id']}' in st.session_state:
                                             with open(st.session_state[f'adm_inv_{pay["id"]}'], "rb") as f:
                                                 st.download_button("⬇️", f, file_name=f"Inv_{pay['id']}.pdf", key=f"adm_dl_inv_{pay['id']}")
                        else:
                            st.caption(t('admin.no_payments'))
                        
                        st.markdown("---")
                        
                        # === قسم تعديل بيانات الأقساط ===
                        with st.expander(f"💳 {t('admin.edit_installment_data')}"):
                            st.info(t('admin.edit_installment_desc'))
                            
                            inst_col1, inst_col2 = st.columns(2)
                            
                            with inst_col1:
                                # طريقة الدفع
                                current_method = c.get('payment_method', 'installment')
                                payment_method = st.selectbox(
                                    t('admin.payment_method'),
                                    ["cash", "installment"],
                                    index=0 if current_method == 'cash' else 1,
                                    format_func=lambda x: f"{t('checkout.cash')} / Cash" if x == "cash" else f"{t('checkout.installments')} / Installment",
                                    key=f"pay_method_{c['id']}"
                                )
                                
                                # السعر الإجمالي
                                total_price = st.number_input(
                                    f"{t('admin.total_price')} (€)",
                                    value=float(c.get('total_amount', c.get('total_price', c.get('estimated_price', 0)))),
                                    min_value=0.0,
                                    key=f"total_price_{c['id']}"
                                )
                            
                            with inst_col2:
                                # الدفعة المقدمة
                                down_payment = st.number_input(
                                    f"{t('admin.down_payment')} (€)",
                                    value=float(c.get('down_payment', 0)),
                                    min_value=0.0,
                                    key=f"down_pay_{c['id']}"
                                )
                                
                                # حساب المتبقي
                                remaining = total_price - down_payment
                                st.metric(t('admin.remaining_amount'), f"€{remaining:,.2f}")
                            
                            # إذا كان تقسيط، إظهار حقول الأقساط
                            if payment_method == "installment":
                                st.markdown(f"**📊 {t('admin.installment_details')}:**")
                                inst_col3, inst_col4 = st.columns(2)
                                
                                with inst_col3:
                                    installment_count = st.number_input(
                                        t('admin.installment_count'),
                                        value=int(c.get('installment_count', 12)),
                                        min_value=1,
                                        max_value=60,
                                        key=f"inst_count_{c['id']}"
                                    )
                                
                                with inst_col4:
                                    # حساب القسط الشهري تلقائياً
                                    monthly_calc = remaining / installment_count if installment_count > 0 else 0
                                    monthly_installment = st.number_input(
                                        f"{t('admin.monthly_installment')} (€)",
                                        value=float(c.get('monthly_installment', monthly_calc)),
                                        min_value=0.0,
                                        key=f"monthly_{c['id']}"
                                    )
                                
                                # عرض ملخص الأقساط
                                st.info(f"📋 **{t('admin.summary')}:** {installment_count} x {monthly_installment:,.2f}€ = {installment_count * monthly_installment:,.2f}€")
                            else:
                                installment_count = 0
                                monthly_installment = 0.0
                            
                            # زر حفظ التعديلات
                            if st.button(f"💾 {t('admin.save_installment_data')}", key=f"save_inst_{c['id']}", type="primary"):
                                try:
                                    db.update_contract(c['id'], 
                                        payment_method=payment_method,
                                        total_amount=total_price,
                                        down_payment=down_payment,
                                        installment_count=installment_count,
                                        monthly_installment=monthly_installment,
                                        remaining_amount=remaining
                                    )
                                    st.success(f"✅ {t('messages.success')}!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ خطأ: {e}")
            else:
                 st.info(t('admin.no_contracts_yet'))
        
        with tab2:
            st.caption(t('admin.estimates_history_caption'))
            # فلتر السنة
            available_years = db.get_available_years()
            selected_year = st.selectbox(f"📅 {t('admin.select_year')}", available_years)
        
        # زر الجرد السنوي
        if st.button(f"📊 {t('admin.annual_report')}", type="primary"):
            st.session_state['show_annual_report'] = True
            st.rerun()
            
        if st.session_state.get('show_annual_report'):
            st.markdown("---")
            st.subheader(f"📑 {t('admin.annual_report_title', year=selected_year)}")
            
            # جلب إحصائيات السنة المحددة
            # جلب إحصائيات السنة المحددة
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT COUNT(*), COALESCE(SUM(estimated_price), 0), COALESCE(AVG(estimated_price), 0)
                    FROM transactions 
                    WHERE strftime('%Y', created_at) = ?
                ''', (selected_year,))
                year_count, year_total, year_avg = cursor.fetchone()
            
            # عرض بطاقات الملخص للسنة
            ac1, ac2, ac3 = st.columns(3)
            with ac1:
                st.metric(t('admin.transaction_count'), year_count)
            with ac2:
                st.metric(t('admin.report_total_value'), f"€{year_total:,.2f}")
            with ac3:
                st.metric(t('admin.average_value'), f"€{year_avg:,.2f}")
            
            conn.close()
            
            if st.button(f"❌ {t('admin.close_report')}"):
                st.session_state['show_annual_report'] = False
                st.rerun()
            st.markdown("---")
        
        # عرض المعاملات حسب السنة المختارة
        transactions = db.get_transactions_by_year(selected_year)
        
        if transactions:
            st.write(f"{t('admin.transaction_count')}: {len(transactions)}")
            for trans in transactions:
                with st.expander(
                    f"#{trans.get('id')} - {trans.get('brand')} {trans.get('model')} - "
                    f"€{trans.get('estimated_price', 0):,.2f}"
                ):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**{t('admin.username')}:** {trans.get('username')}")
                        st.write(f"**{t('admin.car_type')}:** {trans.get('car_type')}")
                        st.write(f"**{t('admin.brand')}:** {trans.get('brand')}")
                        img_path = trans.get('image_path')
                        if img_path and img_path != 'stored_in_session' and os.path.exists(img_path):
                            st.image(img_path, width=150)
                    
                    with col2:
                        st.write(f"**{t('admin.model')}:** {trans.get('model')} {trans.get('manufacture_year')}")
                        st.write(f"**{t('admin.mileage')}:** {trans.get('mileage')} km")
                        st.write(f"**{t('admin.estimated_price')}:** €{trans.get('estimated_price', 0):,.2f}")
                        st.write(f"**{t('admin.creation_date')}:** {str(trans.get('created_at', ''))[:19]}")

                    st.markdown("---")
                    
                    # Admin Actions
                    adm_act1, adm_act2, adm_act3, adm_act4 = st.columns(4)
                    
                    # === Admin Delete ===
                    with adm_act1:
                         if st.button(f"❌ {t('admin.delete')}", key=f"adm_del_tr_{trans['id']}"):
                             if db.delete_transaction(trans['id']):
                                 st.success(t('messages.success'))
                                 st.rerun()
                             else:
                                 st.error(t('messages.error'))

                    # === Admin Edit ===
                    with adm_act2:
                         adm_edit_key = f"adm_edit_mode_{trans['id']}"
                         if st.button(f"✏️ {t('admin.edit_transaction')}", key=f"adm_btn_ed_{trans['id']}"):
                             st.session_state[adm_edit_key] = not st.session_state.get(adm_edit_key, False)
                             st.rerun()
                    
                    # === Continue to Verify Identity (مثل تدفق العميل) ===
                    with adm_act3:
                        if st.button(f"🆔 {t('predict.step2_title')}", key=f"adm_verify_{trans['id']}", help=t('admin.continue_verification')):
                            # تخزين بيانات المعاملة في الجلسة
                            st.session_state.selected_transaction = trans
                            st.session_state.car_data = {
                                'brand': trans.get('brand'),
                                'model': trans.get('model'),
                                'manufacture_year': trans.get('manufacture_year'),
                                'mileage': trans.get('mileage'),
                                'car_type': trans.get('car_type'),
                                'estimated_price': trans.get('estimated_price')
                            }
                            st.session_state.estimated_price = trans.get('estimated_price', 0)
                            st.session_state.page = 'verify_identity'
                            st.rerun()
                    
                    # === Continue to Checkout (مثل تدفق العميل) ===
                    with adm_act4:
                        if st.button(f"💳 {t('predict.step3_title')}", key=f"adm_checkout_{trans['id']}", help=t('admin.continue_payment')):
                            # تخزين بيانات المعاملة في الجلسة
                            st.session_state.selected_transaction = trans
                            st.session_state.car_data = {
                                'brand': trans.get('brand'),
                                'model': trans.get('model'),
                                'manufacture_year': trans.get('manufacture_year'),
                                'mileage': trans.get('mileage'),
                                'car_type': trans.get('car_type'),
                                'estimated_price': trans.get('estimated_price')
                            }
                            st.session_state.estimated_price = trans.get('estimated_price', 0)
                            st.session_state.page = 'checkout'
                            st.rerun()
                    
                    # نموذج التعديل الإداري
                    if st.session_state.get(f"adm_edit_mode_{trans['id']}", False):
                        st.markdown("---")
                        st.subheader(f"✏️ {t('admin.edit_transaction')}")
                        
                        # عرض جميع بيانات المعاملة الحالية في جدول
                        st.markdown("**📋 البيانات الحالية:**")
                        current_data = f"""
                        <table style="width:100%; background:#0E1117; border-radius:8px; color:#fff;">
                            <tr><td style="padding:8px; color:#a0a0c0;">ID</td><td style="padding:8px;">{trans.get('id')}</td></tr>
                            <tr><td style="padding:8px; color:#a0a0c0;">{t('admin.username')}</td><td style="padding:8px;">{trans.get('username') or '-'}</td></tr>
                            <tr><td style="padding:8px; color:#a0a0c0;">{t('admin.car_type')}</td><td style="padding:8px;">{trans.get('car_type') or '-'}</td></tr>
                            <tr><td style="padding:8px; color:#a0a0c0;">{t('admin.brand')}</td><td style="padding:8px;">{trans.get('brand') or '-'}</td></tr>
                            <tr><td style="padding:8px; color:#a0a0c0;">{t('admin.model')}</td><td style="padding:8px;">{trans.get('model') or '-'}</td></tr>
                            <tr><td style="padding:8px; color:#a0a0c0;">{t('admin.year')}</td><td style="padding:8px;">{trans.get('manufacture_year') or '-'}</td></tr>
                            <tr><td style="padding:8px; color:#a0a0c0;">{t('admin.mileage')}</td><td style="padding:8px;">{trans.get('mileage') or 0} km</td></tr>
                            <tr><td style="padding:8px; color:#a0a0c0;">{t('admin.estimated_price')}</td><td style="padding:8px;">€{trans.get('estimated_price') or 0:,.2f}</td></tr>
                            <tr><td style="padding:8px; color:#a0a0c0;">{t('admin.creation_date')}</td><td style="padding:8px;">{str(trans.get('created_at') or '-')[:19]}</td></tr>
                        </table>
                        """
                        st.markdown(current_data, unsafe_allow_html=True)
                        
                        st.markdown("---")
                        st.markdown("**✏️ تعديل البيانات:**")
                        
                        with st.form(key=f"adm_form_ed_{trans['id']}"):
                            # الصف الأول: نوع السيارة والشركة والموديل
                            row1_col1, row1_col2, row1_col3 = st.columns(3)
                            
                            with row1_col1:
                                a_car_type = st.text_input(t('admin.car_type'), value=trans.get('car_type') or '', key=f"tr_type_{trans['id']}")
                            with row1_col2:
                                a_brand = st.text_input(t('admin.brand'), value=trans.get('brand') or '', key=f"tr_brand_{trans['id']}")
                            with row1_col3:
                                a_model = st.text_input(t('admin.model'), value=trans.get('model') or '', key=f"tr_model_{trans['id']}")
                            
                            # الصف الثاني: السنة والممشى والسعر
                            row2_col1, row2_col2, row2_col3 = st.columns(3)
                            
                            with row2_col1:
                                a_year = st.number_input(t('admin.year'), value=int(trans.get('manufacture_year') or 2020), min_value=1900, max_value=2030, key=f"tr_year_{trans['id']}")
                            with row2_col2:
                                a_km = st.number_input(f"{t('admin.mileage')} (km)", value=int(trans.get('mileage') or 0), min_value=0, key=f"tr_km_{trans['id']}")
                            with row2_col3:
                                a_price = st.number_input(f"{t('admin.estimated_price')} (€)", value=float(trans.get('estimated_price') or 0.0), min_value=0.0, key=f"tr_price_{trans['id']}")
                            
                            st.markdown("---")
                            
                            col_save, col_cancel = st.columns(2)
                            
                            with col_save:
                                if st.form_submit_button(f"💾 {t('admin.save_edits')}", type="primary", use_container_width=True):
                                    updates = {
                                        'car_type': a_car_type,
                                        'brand': a_brand, 
                                        'model': a_model, 
                                        'manufacture_year': a_year, 
                                        'mileage': a_km,
                                        'estimated_price': a_price
                                    }
                                    if db.update_transaction(trans['id'], updates):
                                        st.session_state[f"adm_edit_mode_{trans['id']}"] = False
                                        st.rerun()
                                    else:
                                        st.error(f"❌ {t('messages.error')}")
                            
                            with col_cancel:
                                if st.form_submit_button(f"❌ {t('admin.cancel')}", use_container_width=True):
                                    st.session_state[f"adm_edit_mode_{trans['id']}"] = False
                                    st.rerun()
        else:
            st.info(t('admin.no_transactions'))
    
    elif admin_menu == t('admin.statistics'):
        st.subheader(f"📈 {t('admin.detailed_statistics')}")
        
        stats = db.get_statistics()

        # استدعاء المكون الجديد بدلاً من الكود القديم
        get_admin_stats_html(
            stats.get('total_users', 0),
            stats.get('total_transactions', 0),
            stats.get('total_invoices', 0),
            stats.get('total_estimated_value', 0)
        )
        
        st.markdown("---")
        
        # الرسوم البيانية التفاعلية
        import plotly.express as px
        import plotly.graph_objects as go
        import pandas as pd
        
        try:
            # 1. تحليل المعاملات حسب الوقت (خط زمني)
            # نحتاج لجلب البيانات مجمعة حسب التاريخ
            
            # جلب المعاملات مع التاريخ والسعر باستخدام مدير قاعدة البيانات
            with db.get_connection() as conn:
                df_trans = pd.read_sql_query("SELECT created_at, estimated_price, brand, car_type FROM transactions", conn)
            
            if not df_trans.empty:
                df_trans['created_at'] = pd.to_datetime(df_trans['created_at'])
                df_trans['date'] = df_trans['created_at'].dt.date
                
                # تجميع حسب اليوم
                daily_stats = df_trans.groupby('date').agg({
                    'estimated_price': 'sum',
                    'created_at': 'count'
                }).reset_index()
                daily_stats.columns = ['التاريخ', 'إجمالي القيمة', 'عدد المعاملات']
                
                st.subheader(f"📅 {t('admin.growth_analysis')}")
                
                chart_col1, chart_col2 = st.columns(2)
                
                with chart_col1:
                    fig_line = px.line(daily_stats, x='التاريخ', y='عدد المعاملات', 
                                     title='📈 عدد المعاملات اليومية', markers=True)
                    st.plotly_chart(fig_line, use_container_width=True)
                
                with chart_col2:
                    fig_bar_val = px.bar(daily_stats, x='التاريخ', y='إجمالي القيمة',
                                       title='💰 حجم التعاملات اليومية ($)', color='إجمالي القيمة')
                    st.plotly_chart(fig_bar_val, use_container_width=True)
                
                st.markdown("---")
                
                # 2. توزيع العلامات التجارية والأنواع
                st.subheader(f"🏎️ {t('admin.market_preferences')}")
                
                pie_col1, pie_col2 = st.columns(2)
                
                with pie_col1:
                    # العلامات التجارية الأكثر شعبية
                    brand_counts = df_trans['brand'].value_counts().reset_index()
                    brand_counts.columns = ['العلامة التجارية', 'العدد']
                    fig_pie = px.pie(brand_counts, values='العدد', names='العلامة التجارية', 
                                   title='توزيع العلامات التجارية', hole=0.4)
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                with pie_col2:
                    # أنواع السيارات
                    type_counts = df_trans['car_type'].value_counts().reset_index()
                    type_counts.columns = ['نوع السيارة', 'العدد']
                    fig_bar_h = px.bar(type_counts, x='العدد', y='نوع السيارة', orientation='h',
                                     title='أنواع السيارات الأكثر طلباً', color='العدد')
                    st.plotly_chart(fig_bar_h, use_container_width=True)
                
            else:
                st.info(t('admin.no_chart_data'))
                
        except Exception as e:
            st.error(f"{t('messages.error')}: {e}")
            
    elif admin_menu == t('admin.financial_settings'):
        st.subheader(f"⚙️ {t('admin.system_settings')}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"💾 {t('admin.create_backup')}", use_container_width=True):
                try:
                    backup_path = db.backup_database()
                    st.success(f"✅ تم إنشاء النسخة الاحتياطية: {backup_path}")
                except Exception as e:
                    st.error(f"❌ خطأ: {e}")
            
            st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
            
            # زر تنظيف الصور
            from utils.cleanup import ImageCleanupManager
            if st.button(f"🧹 {t('admin.clean_images')}", help="Delete unused images", use_container_width=True):
                with st.spinner("Cleaning images..."):
                    try:
                        cleaner = ImageCleanupManager()
                        report = cleaner.cleanup_orphaned_images(retention_hours=24)
                        
                        if report['errors']:
                            st.warning(f"Finished with errors: {report['errors']}")
                        
                        st.success(f"""
                        ✅ {t('admin.clean_success')}!
                        - Deleted Files: {report['deleted_files']}
                        - Freed Space: {report['freed_space_mb']:.2f} MB
                        """)
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        
        with col2:
            if st.button(f"🧹 {t('admin.clean_cache')}", use_container_width=True):
                try:
                    cache = CacheManager()
                    count = cache.clear()
                    st.success(f"✅ {t('admin.clean_success')} ({count})")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        st.markdown("---")
        st.markdown(f"### ⛽ {t('admin.fuel_price_settings')}")
        st.caption(t('admin.fuel_settings_hint'))
        
        current_factors = Config.FUEL_FACTORS
        
        with st.form("fuel_settings_form"):
            f_col1, f_col2, f_col3, f_col4 = st.columns(4)
            
            with f_col1:
                f_electric = st.number_input(t('admin.fuel_label_electric'), min_value=0.5, max_value=2.0, value=current_factors.get(t('admin.fuel_electric'), 1.25), step=0.05, format="%.2f")
            with f_col2:
                f_hybrid = st.number_input(t('admin.fuel_label_hybrid'), min_value=0.5, max_value=2.0, value=current_factors.get(t('admin.fuel_hybrid'), 1.15), step=0.05, format="%.2f")
            with f_col3:
                f_diesel = st.number_input(t('admin.fuel_label_diesel'), min_value=0.5, max_value=2.0, value=current_factors.get(t('admin.fuel_diesel'), 1.05), step=0.05, format="%.2f")
            with f_col4:
                f_gasoline = st.number_input(t('admin.fuel_label_gasoline'), min_value=0.5, max_value=2.0, value=current_factors.get(t('admin.fuel_gasoline'), 1.00), step=0.05, format="%.2f")
            
            if st.form_submit_button(f"💾 {t('admin.save_fuel_settings')}", type="primary"):
                try:
                    import json
                    
                    new_factors = {
                        t('admin.fuel_electric'): f_electric,
                        t('admin.fuel_hybrid'): f_hybrid,
                        t('admin.fuel_diesel'): f_diesel,
                        t('admin.fuel_gasoline'): f_gasoline,
                        t('common.unspecified'): 1.0
                    }
                    
                    # 1. التحديث في الذاكرة الحالية
                    Config.FUEL_FACTORS.update(new_factors)
                    
                    # 2. الحفظ في الملف
                    config_path = Config.DATA_DIR / "config.json"
                    
                    # قراءة الملف الحالي إن وجد للحفاظ على إعدادات أخرى
                    current_config_data = {}
                    if config_path.exists():
                        try:
                            with open(config_path, 'r', encoding='utf-8') as f:
                                current_config_data = json.load(f)
                        except:
                            pass
                    
                    current_config_data['fuel_factors'] = new_factors
                    
                    with open(config_path, 'w', encoding='utf-8') as f:
                        json.dump(current_config_data, f, ensure_ascii=False, indent=4)
                        
                    st.success(f"✅ {t('admin.fuel_settings_saved')}")
                    time.sleep(1)
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ {t('admin.save_error')}: {e}")




# ======================
# دالة عرض الميزات
# ======================

@st.dialog(t('nav.features'), width="large")
def show_features_dialog():
    """عرض ميزات التطبيق"""
    st.session_state['show_features'] = False
    
    st.markdown(f"""
## ✨ {t('features.title')}

---

### 🤖 {t('features.ai_recognition_title')}
{t('features.ai_recognition_desc')}

---

### 💰 {t('features.ai_pricing_title')}
{t('features.ai_pricing_desc')}

---

### 🔒 {t('features.data_protection_title')}
{t('features.data_protection_desc')}

---

### 🧾 {t('features.invoices_title')}
{t('features.invoices_desc')}

---

### 🌍 {t('features.multilingual_title')}
{t('features.multilingual_desc')}

---

### 📊 {t('features.dashboard_title')}
{t('features.dashboard_desc')}

---

### 👥 {t('features.employee_title')}
{t('features.employee_desc')}

---

### 📱 {t('features.easy_use_title')}
{t('features.easy_use_desc')}
    """)
    
    if st.button(t('buttons.close'), use_container_width=True, type="primary"):
        st.rerun()



# ======================
# دالة عن التطبيق
# ======================

@st.dialog(t('nav.about'), width="large")
def show_about_dialog():
    """عرض معلومات عن التطبيق"""
    st.session_state['show_about'] = False
    
    st.markdown(f"""
## ℹ️ {t('about.title')}

---

# 🏎️ SmartCar AI-Dealer
### {t('about.version')}

---

{t('about.description')}

---

## {t('about.main_features')}

- 🤖 {t('about.feature1')}
- 💰 {t('about.feature2')}
- 🔒 {t('about.feature3')}
- 🧾 {t('about.feature4')}
- 🌍 {t('about.feature5')}

---

## {t('about.developer')}
**{t('about.developer_name')}**

---

© 2024 SmartCar AI-Dealer. {t('about.rights')}
    """)
    
    if st.button(t('buttons.close'), use_container_width=True, type="primary"):
        st.rerun()


# ======================
# دالة عرض المساعدة
# ======================

@st.dialog(t('nav.help'), width="large")
def show_help_dialog():
    """عرض دليل سير العمل"""
    st.session_state['show_help'] = False
    
    st.markdown(f"""
## 📖 {t('help.title')}

### 🏎️ {t('help.workflow_title')}

---

#### 📸 {t('help.step1_title')}
{t('help.step1_desc')}

---

#### 📝 {t('help.step2_title')}
{t('help.step2_desc')}

---

#### 💰 {t('help.step3_title')}
{t('help.step3_desc')}

---

#### 💳 {t('help.step4_title')}
{t('help.step4_desc')}

---

#### 📄 {t('help.step5_title')}
{t('help.step5_desc')}

---

### 💡 {t('help.tips_title')}
    """)
    
    # عرض النصائح بتنسيق مخصص - نص أبيض واضح
    tips_html = f"""
    <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 15px;">
        <div style="background: linear-gradient(135deg, #1e5631 0%, #2d7a46 100%); padding: 12px 16px; border-radius: 8px; border-right: 4px solid #28a745;">
            <span style="color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-weight: 500;">✅ {t('help.tip1')}</span>
        </div>
        <div style="background: linear-gradient(135deg, #1e5631 0%, #2d7a46 100%); padding: 12px 16px; border-radius: 8px; border-right: 4px solid #28a745;">
            <span style="color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-weight: 500;">✅ {t('help.tip2')}</span>
        </div>
        <div style="background: linear-gradient(135deg, #1e5631 0%, #2d7a46 100%); padding: 12px 16px; border-radius: 8px; border-right: 4px solid #28a745;">
            <span style="color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-weight: 500;">✅ {t('help.tip3')}</span>
        </div>
    </div>
    """
    st.markdown(tips_html, unsafe_allow_html=True)
    
    if st.button(t('buttons.close'), use_container_width=True, type="primary"):
        st.rerun()


# ======================
# الشريط الجانبي
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


# ======================
# صفحة التحقق من الهوية (جديدة)
# ======================

def verify_identity_page():
    """Identity verification page"""
    st.markdown(f"""
    <div class="main-header">
        <h1>🔐 {t('identity.title', 'Identity Verification')}</h1>
    </div>
    <div class="sub-header">
        <p>{t('identity.hint', 'Please scan your ID card and driver license to continue')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # التحقق مما إذا كان المستخدم قد وثق حسابه بالفعل
    user = st.session_state.user
    db = DatabaseManager()
    
    # نتحقق من وجود البيانات في السيشن أو قاعدة البيانات
    is_id_verified = bool(user.get('id_number') and user.get('nationality'))
    is_license_verified = bool(user.get('license_number'))
    
    # إذا كان كلاهما موثق، نظهر رسالة ونزر للمتابعة
    if is_id_verified and is_license_verified:
        st.success(f"✅ {t('identity.verified', 'Identity verified successfully!')}")
        if st.button(f"{t('identity.proceed_checkout', 'Proceed to Payment')} 💳", type="primary", use_container_width=True):
            navigate_to('checkout')
        return

    from utils import DocumentScanner
    
    tab1, tab2 = rtl_tabs([f"🪪 {t('profile.id_card', 'ID Card')}", f"🏎️ {t('profile.driver_license', 'Driver License')}"])
    
    # === تبويب البطاقة الشخصية ===
    with tab1:
        if is_id_verified:
            st.success(f"✅ {t('identity.id_verified', 'ID Verified')} ({t('profile.id_number')}: {user.get('id_number')})")
        else:
            st.info(t('identity.step1_hint', 'Step 1: Please scan front and back of your ID'))
            
            method = st.radio(t('identity.input_method', 'Input Method'), [t('predict.upload_image'), t('predict.capture_image')], horizontal=True, key="id_method")
            
            id_front_val = None
            id_back_val = None
            
            col1, col2 = st.columns(2)
            
            if method == t('admin.upload_image'):
                with col1:
                    id_front = st.file_uploader(t('admin.id_front'), type=['jpg', 'png', 'jpeg'], key="v_id_f")
                    if id_front: id_front_val = id_front.getvalue()
                with col2:
                    id_back = st.file_uploader(t('admin.id_back'), type=['jpg', 'png', 'jpeg'], key="v_id_b")
                    if id_back: id_back_val = id_back.getvalue()
            else:
                with col1:
                    id_front_cam = st.camera_input(t('admin.capture_front'), key="cam_id_f")
                    if id_front_cam: id_front_val = id_front_cam.getvalue()
                with col2:
                    id_back_cam = st.camera_input(t('admin.capture_back'), key="cam_id_b")
                    if id_back_cam: id_back_val = id_back_cam.getvalue()

            if id_front_val and id_back_val:
                if st.button(f"{t('admin.scan_verify_id')} 🔍", key="btn_verify_id"):
                    with st.spinner(t('admin.analyzing_id')):
                        scanner = DocumentScanner()
                        front_res = scanner.scan_id_card(id_front_val)
                        back_res = scanner.scan_id_card(id_back_val)
                        
                        # دمج البيانات
                        combined = {k: v for k, v in front_res.items() if v != 'غير واضح'}
                        for k, v in back_res.items():
                            if v != 'غير واضح' and k not in combined:
                                combined[k] = v
                        
                        # حفظ البيانات في الجلسة لعرضها
                        st.session_state.scanned_id_data = combined
                
                # عرض البيانات المستخرجة إذا وجدت
                if st.session_state.get('scanned_id_data'):
                    combined = st.session_state.scanned_id_data
                    
                    st.markdown("""
                    <style>
                    .id-card {
                        background: linear-gradient(135deg, #0E1117 0%, #161B22 100%);
                        border-radius: 16px;
                        padding: 24px;
                        margin: 20px 0;
                        border: 2px solid #f1c40f;
                        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                    }
                    .id-card h3 { color: #f1c40f; margin-bottom: 20px; text-align: center; }
                    .id-field { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
                    .id-label { color: #888; font-size: 0.9rem; }
                    .id-value { color: #fff; font-weight: bold; }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="id-card">
                        <h3>🪪 بيانات الهوية المستخرجة</h3>
                        <div class="id-field"><span class="id-label">الاسم الكامل:</span><span class="id-value">{combined.get('full_name', 'غير واضح')}</span></div>
                        <div class="id-field"><span class="id-label">رقم الهوية:</span><span class="id-value">{combined.get('id_number', 'غير واضح')}</span></div>
                        <div class="id-field"><span class="id-label">الجنسية:</span><span class="id-value">{combined.get('nationality', 'غير واضح')}</span></div>
                        <div class="id-field"><span class="id-label">تاريخ الميلاد:</span><span class="id-value">{combined.get('birth_date', 'غير واضح')}</span></div>
                        <div class="id-field"><span class="id-label">تاريخ الانتهاء:</span><span class="id-value">{combined.get('expiry_date', 'غير واضح')}</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if combined.get('id_number') and combined.get('id_number') != 'غير واضح':
                        col_confirm, col_retry = st.columns(2)
                        with col_confirm:
                            if st.button(f"✅ {t('admin.confirm_save_data')}", key="confirm_id", type="primary", use_container_width=True):
                                try:
                                    db.update_user(user['id'], **combined)
                                    st.session_state.user.update(combined)
                                    del st.session_state.scanned_id_data
                                    st.success(f"✅ {t('admin.id_verified_success')}")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"{t('admin.save_data_error')}: {e}")
                        with col_retry:
                            if st.button(f"🔄 {t('admin.rescan')}", key="retry_id", use_container_width=True):
                                del st.session_state.scanned_id_data
                                st.rerun()
                    else:
                        st.warning("⚠️ لم يتم التعرف على بعض البيانات بوضوح. يمكنك القبول أو إعادة المحاولة.")
                        col_force, col_retry2 = st.columns(2)
                        with col_force:
                            if st.button(f"✅ قبول البيانات المتاحة", key="force_accept_id", type="primary", use_container_width=True):
                                try:
                                    save_data = {k: v for k, v in combined.items() if k != 'error'}
                                    # ضمان وجود قيم أساسية حتى لو غير واضحة
                                    if not save_data.get('id_number') or save_data.get('id_number') == 'غير واضح':
                                        save_data['id_number'] = 'PENDING'
                                    if not save_data.get('nationality') or save_data.get('nationality') == 'غير واضح':
                                        save_data['nationality'] = 'PENDING'
                                    db.update_user(user['id'], **save_data)
                                    st.session_state.user.update(save_data)
                                    del st.session_state.scanned_id_data
                                    st.success("✅ تم حفظ البيانات المتاحة!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"خطأ: {e}")
                        with col_retry2:
                            if st.button(f"🔄 إعادة المحاولة", key="retry_id_fail", use_container_width=True):
                                if 'scanned_id_data' in st.session_state:
                                    del st.session_state.scanned_id_data
                                st.rerun()


    # === تبويب رخصة القيادة ===
    with tab2:
        if is_license_verified:
            st.success(f"✅ تم التحقق من الرخصة (رقم: {user.get('license_number')})")
        else:
            st.info(t('admin.step2_license_hint'))
            
            method_lic = st.radio(t('identity.input_method', 'Input Method'), [t('predict.upload_image'), t('predict.capture_image')], horizontal=True, key="lic_method")
            
            lic_front_val = None
            lic_back_val = None
            
            col1, col2 = st.columns(2)
            
            if method_lic == t('admin.upload_image'):
                with col1:
                    lic_front = st.file_uploader(t('admin.license_front'), type=['jpg', 'png', 'jpeg'], key="v_lic_f")
                    if lic_front: lic_front_val = lic_front.getvalue()
                with col2:
                    lic_back = st.file_uploader(t('admin.license_back'), type=['jpg', 'png', 'jpeg'], key="v_lic_b")
                    if lic_back: lic_back_val = lic_back.getvalue()
            else:
                with col1:
                    lic_front_cam = st.camera_input(t('admin.capture_front'), key="cam_lic_f")
                    if lic_front_cam: lic_front_val = lic_front_cam.getvalue()
                with col2:
                    lic_back_cam = st.camera_input(t('admin.capture_back'), key="cam_lic_b")
                    if lic_back_cam: lic_back_val = lic_back_cam.getvalue()

            if lic_front_val and lic_back_val:
                if st.button(f"{t('admin.scan_verify_license')} 🔍", key="btn_verify_lic"):
                    with st.spinner(t('admin.analyzing_license')):
                        scanner = DocumentScanner()
                        front_res = scanner.scan_driver_license(lic_front_val)
                        back_res = scanner.scan_driver_license(lic_back_val)
                        
                        # دمج البيانات
                        combined = {k: v for k, v in front_res.items() if v != 'غير واضح'}
                        for k, v in back_res.items():
                            if v != 'غير واضح' and k not in combined:
                                combined[k] = v
                        
                        # حفظ البيانات في الجلسة لعرضها
                        st.session_state.scanned_license_data = combined
                
                # عرض البيانات المستخرجة إذا وجدت
                if st.session_state.get('scanned_license_data'):
                    combined = st.session_state.scanned_license_data
                    
                    st.markdown("""
                    <style>
                    .license-card {
                        background: linear-gradient(135deg, #161B22 0%, #161B22 100%);
                        border-radius: 16px;
                        padding: 24px;
                        margin: 20px 0;
                        border: 2px solid #00d9ff;
                        box-shadow: 0 10px 30px rgba(0,217,255,0.2);
                    }
                    .license-card h3 { color: #00d9ff; margin-bottom: 20px; text-align: center; }
                    .lic-field { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
                    .lic-label { color: #888; font-size: 0.9rem; }
                    .lic-value { color: #fff; font-weight: bold; }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="license-card">
                        <h3>🏎️ بيانات رخصة القيادة المستخرجة</h3>
                        <div class="lic-field"><span class="lic-label">الاسم الكامل:</span><span class="lic-value">{combined.get('full_name', 'غير واضح')}</span></div>
                        <div class="lic-field"><span class="lic-label">رقم الرخصة:</span><span class="lic-value">{combined.get('license_number', 'غير واضح')}</span></div>
                        <div class="lic-field"><span class="lic-label">نوع الرخصة:</span><span class="lic-value">{combined.get('license_type', 'غير واضح')}</span></div>
                        <div class="lic-field"><span class="lic-label">تاريخ الإصدار:</span><span class="lic-value">{combined.get('issue_date', 'غير واضح')}</span></div>
                        <div class="lic-field"><span class="lic-label">تاريخ الانتهاء:</span><span class="lic-value">{combined.get('expiry_date', 'غير واضح')}</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if combined.get('license_number') and combined.get('license_number') != 'غير واضح':
                        update_data = {
                            'license_number': combined.get('license_number'),
                            'license_type': combined.get('license_type'),
                            'license_expiry': combined.get('expiry_date')
                        }
                        update_data = {k: v for k, v in update_data.items() if v}
                        
                        col_confirm, col_retry = st.columns(2)
                        with col_confirm:
                            if st.button(f"✅ {t('admin.confirm_save_data')}", key="confirm_lic", type="primary", use_container_width=True):
                                try:
                                    db.update_user(user['id'], **update_data)
                                    st.session_state.user.update(update_data)
                                    del st.session_state.scanned_license_data
                                    st.success(f"✅ {t('admin.license_verified_success')}")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"{t('admin.save_data_error')}: {e}")
                        with col_retry:
                            if st.button(f"🔄 {t('admin.rescan')}", key="retry_lic", use_container_width=True):
                                del st.session_state.scanned_license_data
                                st.rerun()
                    else:
                        st.warning("⚠️ لم يتم التعرف على بعض البيانات بوضوح. يمكنك القبول أو إعادة المحاولة.")
                        col_force, col_retry2 = st.columns(2)
                        with col_force:
                            if st.button(f"✅ قبول البيانات المتاحة", key="force_accept_lic", type="primary", use_container_width=True):
                                try:
                                    save_data = {
                                        'license_number': combined.get('license_number', 'PENDING'),
                                        'license_type': combined.get('license_type', 'PENDING'),
                                        'license_expiry': combined.get('expiry_date', 'PENDING')
                                    }
                                    db.update_user(user['id'], **save_data)
                                    st.session_state.user.update(save_data)
                                    del st.session_state.scanned_license_data
                                    st.success("✅ تم حفظ البيانات المتاحة!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"خطأ: {e}")
                        with col_retry2:
                            if st.button(f"🔄 إعادة المحاولة", key="retry_lic_fail", use_container_width=True):
                                if 'scanned_license_data' in st.session_state:
                                    del st.session_state.scanned_license_data
                                st.rerun()
                             
    st.markdown("---")
    
    # تحقق حي من حالة التوثيق (يشمل البيانات المحفوظة حديثاً)
    current_user = st.session_state.user
    id_done = bool(current_user.get('id_number') and current_user.get('nationality'))
    lic_done = bool(current_user.get('license_number'))
    
    if id_done and lic_done:
        st.success("✅ تم التحقق من الهوية والرخصة بنجاح!")
        if st.button(f"➡️ {t('admin.continue_to_payment', 'متابعة إلى الدفع')} 💳", type="primary", use_container_width=True, key="btn_continue_verified"):
            navigate_to('checkout')
    else:
        # إظهار حالة كل خطوة
        col_status1, col_status2 = st.columns(2)
        with col_status1:
            if id_done:
                st.success("✅ الهوية: تم التحقق")
            else:
                st.warning("⏳ الهوية: لم يتم التحقق")
        with col_status2:
            if lic_done:
                st.success("✅ الرخصة: تم التحقق")
            else:
                st.warning("⏳ الرخصة: لم يتم التحقق")
        
        st.caption(f"💡 {t('admin.edit_later_hint', 'يمكنك تعديل بياناتك لاحقاً من ملفك الشخصي')}")
        if st.button(f"➡️ متابعة", type="primary", use_container_width=True, key="btn_continue_anyway"):
            navigate_to('checkout')


# ======================
# صفحة الدفع (Checkout)
# ======================

def checkout_page():
    # Render universal header
    render_universal_header(t('checkout.title'), "💳 " + t('checkout.payment'))
    
    # --- Custom CSS for Checkout ---
    st.markdown("""
    <style>
    .checkout-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }
    .checkout-header {
        font-family: 'Outfit', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .price-tag {
        font-size: 1.2rem;
        font-weight: bold;
        color: #4CAF50;
    }
    /* منع التفاف النص داخل الأزرار */
    div[data-testid="stButton"] button p {
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        font-size: 16px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    .plan-detail-box {
        background: rgba(0, 0, 0, 0.2);
        padding: 15px;
        border-radius: 8px;
        border-right: 4px solid #4facfe;
    }
    
    /* === CHECKOUT PAGE: Force WHITE Text Colors for Dark Theme === */
    /* Target all form element labels with maximum specificity */
    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] label span,
    div[data-testid="stRadio"] label p,
    div[data-testid="stRadio"] div label,
    div[data-testid="stCheckbox"] label,
    div[data-testid="stCheckbox"] label span,
    div[data-testid="stSelectbox"] label,
    div[data-testid="stSelectbox"] label span {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    
    /* Force radio button options text to white */
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label p {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    
    /* Selectbox dropdown text - keep readable on dropdown */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] span {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

    get_section_header_html(f"💳 {t('checkout.title')}")
    
    # ==========================
    # State: Payment Success
    # ==========================
    if st.session_state.get('payment_success'):
        # عرض شاشة النجاح فقط
        st.balloons()
        
        st.markdown(f"""
        <div style="text-align: center; padding: 50px;">
            <h1 style="color: #4CAF50; font-size: 3rem;">🎉</h1>
            <h2 style="color: #4CAF50;">{t('checkout.success')}</h2>
            <p>{t('messages.success')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            # استخدام مولد فواتير الأقساط للحصول على نفس النتيجة في جميع الصفحات
            contract_id = st.session_state.get('current_contract_id') or st.session_state.get('last_transaction_id')
            if contract_id:
                try:
                    from utils import InstallmentInvoiceGenerator
                    inv_gen = InstallmentInvoiceGenerator()
                    all_inv_path = inv_gen.generate_all_invoices(contract_id)
                    if os.path.exists(all_inv_path):
                        with open(all_inv_path, "rb") as pdf_file:
                            st.download_button(
                                f"🧾 {t('checkout.download_invoice')}", 
                                pdf_file.read(), 
                                file_name=f"Invoices_{contract_id}.pdf", 
                                mime="application/pdf",
                                use_container_width=True
                            )
                    else:
                        st.info(f"⏳ {t('messages.loading')}...")
                except Exception as e:
                    st.warning(f"📄 {t('admin.no_invoices')}: {e}")
            else:
                st.info(f"📄 {t('admin.no_invoices')}")
        with col2:
             if 'last_contract_path' in st.session_state:
                contract_path = st.session_state.last_contract_path
                if os.path.exists(contract_path):
                    with open(contract_path, "rb") as pdf_file:
                        st.download_button(
                            f"📄 {t('checkout.download_contract')}", 
                            pdf_file, 
                            file_name=f"Contract_{st.session_state.get('current_contract_id', 'new')}.pdf", 
                            mime="application/pdf",
                            use_container_width=True,
                            type="primary"
                        )
                else:
                    st.info(f"⏳ {t('messages.loading')}...")
             else:
                st.info(f"📄 {t('admin.no_contract_available')}")
        with col3:
            if st.button(f"📂 {t('nav.profile')}", use_container_width=True):
                # مسح حالة الدفع للبدء من جديد مستقبلاً
                st.session_state.payment_success = False
                navigate_to('profile')
        
        if st.button(f"{t('nav.home')}", use_container_width=True):
            st.session_state.payment_success = False
            navigate_to('predict')
            
        return # توقف هنا ولا تعرض باقي الصفحة

    car_data = st.session_state.get('car_details') or st.session_state.get('car_data', {})
    estimated_price = st.session_state.get('last_price') or st.session_state.get('estimated_price', 0)
    
    # التحقق من وجود بيانات صالحة - منع الصفحات الفارغة
    if not car_data or not car_data.get('brand'):
        st.warning(f"⚠️ {t('messages.error')}: {t('admin.no_car_data')}")
        st.info(t('admin.select_transaction_hint'))
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"📋 {t('nav.invoices')}", use_container_width=True):
                navigate_to('invoices')
        with col2:
            if st.button(f"🏎️ {t('nav.predict')}", use_container_width=True, type="primary"):
                navigate_to('predict')
        return
    
    if not estimated_price or estimated_price <= 0:
        st.warning(f"⚠️ {t('messages.error')}: {t('admin.invalid_price')}")
        if st.button(f"🏎️ {t('nav.predict')}", type="primary"):
            navigate_to('predict')
        return
    
    # تفاصيل السيارة (ملخص)
    # تفاصيل السيارة (ملخص)
    # تفاصيل السيارة (ملخص) - Styled Card
    st.markdown(f"""
    <div class="checkout-card">
        <h3 style="margin-top:0;">🏎️ {t('checkout.car_summary')}</h3>
        <p style="font-size: 1.1rem;">
            {car_data.get('brand')} {car_data.get('model')} - {car_data.get('manufacture_year')}
        </p>
        <div class="price-tag">{t('profile.estimated_price')}: {estimated_price:,.2f} €</div>
    </div>
    """, unsafe_allow_html=True)
    
    # === حقول إدخال VIN ورقم اللوحة ===
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0E1117 0%, #1a2636 100%); 
                padding: 15px; border-radius: 10px; border: 2px solid #4facfe; margin: 10px 0;">
        <h4 style="color: #4facfe; margin: 0;">🔢 {t('checkout.vehicle_ids', 'Vehicle Identification')}</h4>
        <p style="color: #a0a0c0; font-size: 0.9rem; margin: 5px 0 0 0;">{t('checkout.vehicle_ids_hint', 'Enter vehicle identification details (optional)')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    vin_col, plate_col = st.columns(2)
    with vin_col:
        vehicle_vin = st.text_input(
            f"🔖 {t('checkout.vin_label', 'VIN (Vehicle Identification Number)')}",
            value=car_data.get('vin', car_data.get('vehicle_vin', '')),
            placeholder="WVWZZZ3CZWE123456",
            key="checkout_vin_input"
        )
    with plate_col:
        vehicle_plate = st.text_input(
            f"🏎️ {t('checkout.plate_label', 'Plate Number')}",
            value=car_data.get('plate', car_data.get('vehicle_plate', '')),
            placeholder="B-AB 1234",
            key="checkout_plate_input"
        )
    
    # تحديث car_data مع VIN ورقم اللوحة
    car_data['vehicle_vin'] = vehicle_vin
    car_data['vehicle_plate'] = vehicle_plate
    car_data['vin'] = vehicle_vin
    car_data['plate'] = vehicle_plate
    
    # === اختيار العميل للأدمن ===
    if st.session_state.user.get('role') == 'admin':
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0E1117 0%, #161B22 100%); 
                    padding: 15px; border-radius: 10px; border: 2px solid #D4AF37; margin: 10px 0;">
            <h4 style="color: #D4AF37; margin: 0;">👤 تحديد العميل</h4>
            <p style="color: #a0a0c0; font-size: 0.9rem; margin: 5px 0 0 0;">سيتم ربط العقد بالعميل المختار (أنت مُدخل البيانات فقط)</p>
        </div>
        """, unsafe_allow_html=True)
        
        admin_db = DatabaseManager()
        all_users = admin_db.get_all_users()
        customers = [u for u in all_users if u.get('role') != 'admin']
        
        if customers:
            customer_options = {f"{u.get('full_name') or u.get('username')} ({u.get('email')})": u['id'] for u in customers}
            
            selected_customer_key = st.selectbox(
                t('admin.customer_owner'),
                options=list(customer_options.keys()),
                key="checkout_customer_select"
            )
            
            st.session_state['admin_selected_customer_id'] = customer_options.get(selected_customer_key)
            st.markdown(f"""<div style='background: linear-gradient(135deg, #0E1117 0%, #1a2e1a 100%); padding: 12px 16px; border-radius: 8px; border-right: 4px solid #28a745; margin: 10px 0;'>
                <span style='color: #38ef7d !important; font-size: 0.95rem; font-weight: 500;'>✅ {t('admin.link_contract_info')}</span>
            </div>""", unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ {t('admin.no_customers')}")
            st.session_state['admin_selected_customer_id'] = None

    
    # === جلب تفضيلات الدفع المحفوظة ===
    db = DatabaseManager()
    
    # تحديد مصدر تفضيلات الدفع
    # إذا كنا نأتي من صفحة العقود، نستخدم بيانات العقد المحفوظة
    if st.session_state.get('selected_transaction'):
        tx = st.session_state.selected_transaction
        saved_prefs = {
            'plan_type': 'installments' if tx.get('installment_count', 0) > 0 else 'full',
            'installment_months': tx.get('installment_count', 0),
            'down_payment': tx.get('down_payment', 0),
            'payment_due_day': tx.get('payment_due_day', 1),
            'grace_period': tx.get('grace_period', 3),
            'has_payments': db.has_contract_payments(tx['id']) if tx.get('id') else False,
            'contract_id': tx.get('id')
        }
    elif st.session_state.get('admin_selected_customer_id'):
        # إذا كان الأدمن يختار عميل، نجلب تفضيلات العميل
        saved_prefs = db.get_user_payment_preferences(st.session_state['admin_selected_customer_id'])
    else:
        # الحالة الافتراضية: تفضيلات المستخدم الحالي
        saved_prefs = db.get_user_payment_preferences(st.session_state.user['id'])
    
    # التحقق من وجود عقد نشط مع دفعات سابقة
    current_contract_id = st.session_state.get('current_contract_id')
    has_previous_payments = False
    if current_contract_id:
        has_previous_payments = db.has_contract_payments(current_contract_id)
    elif saved_prefs:
        has_previous_payments = saved_prefs.get('has_payments', False)
    
    # هل المستخدم مشرف؟
    is_admin = st.session_state.user.get('role') == 'admin'
    
    # قفل طريقة الدفع إذا كان هناك دفعات سابقة (للمستخدم العادي فقط)
    payment_method_locked = has_previous_payments and not is_admin
    
    # إزالة التقسيم إلى أعمدة لإعطاء المحتوى العرض الكامل
    # CSS لإصلاح لون نصوص الـ Radio buttons
    st.markdown("""
    <style>
        /* إصلاح لون نصوص Radio buttons في صفحة الدفع */
        div[data-testid="stRadio"] label p,
        div[data-testid="stRadio"] label span {
            color: #FFFFFF !important;
        }
        div[data-testid="stRadio"] > label > div > p {
            color: #FFFFFF !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.subheader(f"1. {t('checkout.payment_method_label')}")
        
        # تحديد القيمة الافتراضية لنوع الدفع
        default_plan_index = 0
        if saved_prefs and saved_prefs.get('plan_type') == 'installments':
            default_plan_index = 1
        
        if payment_method_locked:
            # عرض رسالة تنبيه بأن الطريقة مقفلة
            st.warning(f"⚠️ {t('admin.payment_locked')}")
            
            # عرض ملخص الأقساط
            contract_id_for_summary = saved_prefs.get('contract_id') if saved_prefs else current_contract_id
            if contract_id_for_summary:
                summary = db.get_contract_installment_summary(contract_id_for_summary)
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #0E1117 0%, #161B22 100%); 
                            border-radius: 10px; padding: 15px; margin: 10px 0;
                            border-left: 4px solid #4facfe;">
                    <h4 style="color: #4facfe; margin-top: 0;">📊 ملخص الأقساط</h4>
                    <table style="width: 100%; color: #fff;">
                        <tr>
                            <td style="padding: 5px 0;">📌 عدد الأقساط الكلي:</td>
                            <td style="font-weight: bold; text-align: left;">{summary['total_installments']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px 0; color: #4CAF50;">✅ الأقساط المدفوعة:</td>
                            <td style="font-weight: bold; color: #4CAF50; text-align: left;">{summary['paid_installments']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px 0; color: #ff6b6b;">⏳ الأقساط المتبقية:</td>
                            <td style="font-weight: bold; color: #ff6b6b; text-align: left;">{summary['remaining_installments']}</td>
                        </tr>
                        <tr style="border-top: 1px solid rgba(255,255,255,0.2);">
                            <td style="padding: 8px 0;">💰 المبلغ المدفوع:</td>
                            <td style="font-weight: bold; color: #4CAF50; text-align: left;">{summary['paid_amount']:,.2f} €</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px 0;">💸 المبلغ المتبقي:</td>
                            <td style="font-weight: bold; color: #ff6b6b; text-align: left;">{summary['remaining_amount']:,.2f} €</td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
            
            # عرض الخيار المحدد بدون إمكانية التغيير
            if saved_prefs and saved_prefs.get('plan_type') == 'installments':
                plan_type = t('checkout.choose_installment_plan')
            else:
                plan_type = t('checkout.full_amount')
            st.info(f"📋 {t('checkout.payment_method_label')}: **{plan_type}**")
        else:
            plan_type = st.radio(t('checkout.payment_method_label'), 
                                [t('checkout.full_amount'), t('checkout.choose_installment_plan')],
                                index=default_plan_index)
        
        processor = PaymentProcessor()
        
        # متغيرات لحفظ تفاصيل الخطة المختارة
        selected_plan_type = 'full'
        selected_months = 0
        selected_interest = 0.0
        selected_monthly = 0.0
        final_contract_amount = estimated_price
        
        if t('checkout.choose_installment_plan') in plan_type or "Installments" in plan_type:
            # خيارات التقسيط المحددة
            st.markdown(f"<p style='color: #FFFFFF; font-weight: bold; margin: 10px 0;'>{t('checkout.choose_installment_plan')}:</p>", unsafe_allow_html=True)
            
            # تحديد القيمة الافتراضية للخطة من التفضيلات المحفوظة
            default_plan_choice_index = 0  # افتراضي: 3 أشهر
            if saved_prefs:
                default_plan_choice_index = saved_prefs.get('plan_choice_index', 0)
            
            # نستخدم columns لعرضها بشكل أجمل كـ "checkboxes" (radio في الحقيقة)
            plan_choice = st.radio(
                t('checkout.duration'),
                [
                    t('checkout.months_3_free'),
                    t('checkout.year_1'),
                    t('checkout.years_2')
                ],
                index=default_plan_choice_index,
                label_visibility="collapsed"
            )
            
            # تحويل الاختيار إلى عدد أشهر
            if "3" in plan_choice:
                months = 3
            elif "12" in plan_choice:
                months = 12
            else:
                months = 24
                
            # === حقل الدفعة المقدمة (Down Payment) ===
            st.markdown("---")
            st.markdown(f"<div style='background: linear-gradient(135deg, #0E1117 0%, #2d2a1a 100%); padding: 10px 15px; border-radius: 8px; border-right: 4px solid #D4AF37; margin: 10px 0;'><span style='color: #D4AF37; font-weight: bold; font-size: 1rem;'>💵 {t('checkout.down_payment_label')}:</span></div>", unsafe_allow_html=True)
            
            # تحديد القيمة الافتراضية للدفعة المقدمة
            default_down_payment = 0.0
            if saved_prefs:
                saved_dp = saved_prefs.get('down_payment', 0)
                # التأكد من أن الدفعة المحفوظة لا تتجاوز 90% من السعر الحالي
                default_down_payment = min(float(saved_dp), float(estimated_price * 0.9))
            
            down_payment = st.number_input(
                t('checkout.down_payment_input'),
                min_value=0.0,
                max_value=float(estimated_price * 0.9),  # الحد الأقصى 90% من السعر
                value=default_down_payment,
                step=500.0,
                key="down_payment_input"
            )
            
            # حساب خطة التقسيط مع الدفعة المقدمة
            plan_details = processor.calculate_installment_plan(estimated_price, months, down_payment)
            
            selected_plan_type = 'installments'
            selected_months = months
            selected_interest = plan_details['interest_rate']
            selected_monthly = plan_details['monthly_installment']
            final_contract_amount = plan_details['grand_total']
            
            # عرض تفاصيل الخطة
            st.markdown(f"""
            <div class="checkout-card">
                <div class="plan-detail-box">
                    <h4 style="margin-top:0; color:#4facfe;">📊 {t('checkout.plan_details_title')}</h4>
                    <ul style="list-style: none; padding-right: 0;">
                        <li>💰 {t('checkout.base_price')}: <b>{estimated_price:,.2f} €</b></li>
                        <li>💵 {t('checkout.down_payment')}: <b style="color:#4CAF50">{down_payment:,.2f} €</b></li>
                        <li>📊 {t('checkout.remaining_amount')}: <b>{plan_details['remaining_after_down']:,.2f} €</b></li>
                        <li>📈 {t('checkout.interest_rate')}: <b style="color:#ff6b6b">{plan_details['interest_rate']*100:.2f}%</b></li>
                        <li>📉 {t('checkout.total_payable')}: <b>{plan_details['total_payable']:,.2f} €</b></li>
                        <hr style="border-color: rgba(255,255,255,0.1);">
                        <li><h3 style="margin:5px 0;">🗓️ {t('checkout.monthly_installment')}: <span style="color:#4CAF50">{plan_details['monthly_installment']:,.2f} €</span> × {months} {t('checkout.month')}</h3></li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # حفظ تفاصيل الخطة في session للاستخدام لاحقاً
            st.session_state.installment_plan = plan_details
            
            # المبلغ المطلوب دفعه الآن (دفعة مقدمة + أول قسط)
            if down_payment > 0:
                amount_to_pay = down_payment
                payment_label = t('checkout.down_payment')
            else:
                amount_to_pay = plan_details['monthly_installment']
                payment_label = t('checkout.first_payment')
        else:
            # تصميم الدفع الكامل بنفس نمط الأقساط
            st.markdown(f"""
            <div class="checkout-card">
                <div class="plan-detail-box" style="border-right-color: #4CAF50;">
                    <h4 style="margin-top:0; color:#4CAF50;">💎 {t('checkout.full_payment_details')}</h4>
                    <ul style="list-style: none; padding-right: 0;">
                        <li>💰 {t('checkout.base_price')}: <b>{estimated_price:,.2f} €</b></li>
                        <li>📉 {t('checkout.interest_rate')}: <b style="color:#4CAF50">0.00% (Cash)</b></li>
                        <hr style="border-color: rgba(255,255,255,0.1);">
                        <li><h3 style="margin:5px 0;">💶 {t('checkout.total_required')}: <span style="color:#4CAF50">{estimated_price:,.2f} €</span></h3></li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            selected_plan_type = 'full'
            amount_to_pay = estimated_price
            final_contract_amount = estimated_price
            payment_label = t('checkout.full_amount')
            
        st.markdown("---")
        
        # Wrapping Payment Section in 50% width
        pay_col, _ = st.columns([1, 1])
        with pay_col:
            st.markdown(f"""<div class="checkout-header">2. {t('checkout.payment_header')} 💳</div>""", unsafe_allow_html=True)
            
            pay_method = st.selectbox(t('checkout.payment_method_label'), [t('checkout.bank_transfer'), t('checkout.credit_card'), t('checkout.cash_branch')])
            
            if pay_method != t('checkout.cash_branch'):
                
                # --- ميزة 1: عرض QR كود للدفع (للعميل) ---
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #0E1117 0%, #1a2636 100%); padding: 12px 16px; border-radius: 8px; margin: 10px 0; border-right: 4px solid #4a9eff;'>
                    <span style='color: #4facfe; font-size: 0.95rem;'>ℹ️ {t('checkout.scan_qr_hint')}</span>
                </div>
                """, unsafe_allow_html=True)
                # عرض checkbox مع Label في columns
                qr_col1, qr_col2 = st.columns([0.05, 0.95])
                with qr_col1:
                    show_qr = st.checkbox("‎", key="show_qr_code_checkbox", label_visibility="collapsed")
                with qr_col2:
                    st.markdown(f"""<div style='background: linear-gradient(135deg, #0E1117 0%, #1a3636 100%); padding: 8px 15px; border-radius: 8px; border-right: 4px solid #17a2b8; display: inline-block;'>
                        <span style='color: #17a2b8; font-weight: bold; font-size: 1rem;'>{t('checkout.show_qr_btn')}</span>
                    </div>""", unsafe_allow_html=True)
                if show_qr:
                    # بيانات الشركة
                    company_name = Config.APP_NAME
                    company_iban = "DE01234567890123123"
                    company_bic = "SMART12345"
                    
                    # رقم الفاتورة

                    invoice_number = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    
                    # سبب التحويل / Verwendungszweck
                    car_info = f"{car_data.get('brand', 'Unknown')} {car_data.get('model', 'Unknown')}"
                    verwendungszweck = f"{t('checkout.purchase_car')} {car_info} - {t('checkout.invoice_no')} {invoice_number}"
                    
                    # صيغة EPC QR كود للتحويل البنكي (معيار SEPA)
                    qr_data = f"""BCD
002
1
SCT
{company_bic}
{company_name}
{company_iban}
EUR{amount_to_pay:.2f}

{verwendungszweck}
{invoice_number}"""
                    
                    # توليد QR
                    import qrcode
                    from io import BytesIO
                    qr = qrcode.QRCode(box_size=8, border=4)
                    qr.add_data(qr_data)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="#0E1117", back_color="white")
                    
                    buf = BytesIO()
                    img.save(buf, format="PNG")
                    
                    # عرض QR مع المعلومات
                    st.image(buf.getvalue(), caption=f"{t('checkout.scan_to_pay')}: {amount_to_pay:,.2f} €", width=300)
                    
                    # عرض تفاصيل التحويل بشكل احترافي
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #0E1117 0%, #161B22 100%); 
                                border-radius: 12px; padding: 20px; margin: 15px 0;
                                border: 1px solid #4facfe;">
                        <h4 style="color: #4facfe; margin-top: 0;">📋 {t('checkout.bank_info_title')}</h4>
                        <table style="width: 100%; color: #fff;">
                            <tr><td style="color: #888; padding: 5px 0;">{t('checkout.company_name')}:</td>
                                <td style="font-weight: bold;">{company_name}</td></tr>
                            <tr><td style="color: #888; padding: 5px 0;">IBAN:</td>
                                <td style="font-weight: bold; font-family: monospace;">{company_iban}</td></tr>
                            <tr><td style="color: #888; padding: 5px 0;">BIC:</td>
                                <td style="font-weight: bold; font-family: monospace;">{company_bic}</td></tr>
                            <tr><td style="color: #888; padding: 5px 0;">{t('checkout.amount')}:</td>
                                <td style="font-weight: bold; color: #4CAF50;">{amount_to_pay:,.2f} €</td></tr>
                            <tr><td style="color: #888; padding: 5px 0;">{t('checkout.invoice_no')}:</td>
                                <td style="font-weight: bold;">{invoice_number}</td></tr>
                            <tr><td style="color: #888; padding: 5px 0;">Verwendungszweck:</td>
                                <td style="font-weight: bold; font-size: 0.9rem;">{verwendungszweck}</td></tr>
                        </table>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.info(f"ℹ️ {t('checkout.hide_qr_hint')}")


                st.write("---")
                st.markdown(f"<div style='background: linear-gradient(135deg, #0E1117 0%, #1a2e1a 100%); padding: 10px 15px; border-radius: 8px; border-right: 4px solid #28a745; margin: 10px 0;'><span style='color: #38ef7d; font-weight: bold; font-size: 1rem;'>📎 {t('checkout.upload_proof_label')}:</span></div>", unsafe_allow_html=True)
                
                # --- ميزة 2: خيار الكاميرا أو رفع ملف ---
                upload_method = st.radio(t('checkout.upload_method_label'), [t('checkout.upload_file_option'), t('checkout.camera_option')], horizontal=True)
                
                uploaded_file = None
                if upload_method == t('checkout.camera_option'):
                    # الكاميرا تأخذ عرض العمود بالكامل (وهو أصلاً 50% من الشاشة)
                    uploaded_file = st.camera_input(t('checkout.capture_receipt'))
                else:
                    uploaded_file = st.file_uploader(f"{t('checkout.upload_receipt_for')} {payment_label}", type=['png', 'jpg', 'jpeg', 'pdf'])
                
                # --- NEW: خيارات جدولة الأقساط (مرونة الدفع) ---
                if t('checkout.choose_installment_plan') in plan_type or "Installments" in plan_type:
                    st.write("---")
                    st.markdown(f"<p style='color: #FFFFFF; font-weight: bold; margin: 10px 0;'>{t('checkout.payment_preferences')}:</p>", unsafe_allow_html=True)
                    
                    # تحديد القيم الافتراضية من التفضيلات المحفوظة
                    default_due_day_index = 0  # افتراضي: يوم 1
                    default_grace = 3
                    if saved_prefs:
                        saved_due_day = saved_prefs.get('payment_due_day', 1)
                        default_due_day_index = 0 if saved_due_day == 1 else 1
                        default_grace = saved_prefs.get('grace_period', 3)
                    
                    sch_col1, sch_col2 = st.columns(2)
                    with sch_col1:
                        pref_due_day = st.radio(f"{t('checkout.due_day')}:", [1, 15], horizontal=True, index=default_due_day_index)
                    with sch_col2:
                         pref_grace = st.slider(f"{t('checkout.grace_period')}:", 1, 3, default_grace)
                else:
                     pref_due_day = 1
                     pref_grace = 3
                
                # --- أزرار الإجراءات بتصميم احترافي ---
                st.markdown("""
                <style>
                .action-btn-container {
                    display: flex; gap: 10px; margin: 15px 0;
                }
                /* Fix secondary button text visibility - force dark text on light backgrounds */
                [data-testid="stButton"] button:not([data-testid="baseButton-primary"]) {
                    color: #0E1117 !important;
                    -webkit-text-fill-color: #0E1117 !important;
                }
                [data-testid="stButton"] button:not([data-testid="baseButton-primary"]) p,
                [data-testid="stButton"] button:not([data-testid="baseButton-primary"]) span,
                [data-testid="stButton"] button:not([data-testid="baseButton-primary"]) p {
                    color: #FFFFFF !important;
                    -webkit-text-fill-color: #FFFFFF !important;
                }
                /* Give secondary buttons golden border on dark background */
                [data-testid="stButton"] button:not([data-testid="baseButton-primary"]) {
                    border: 2px solid #D4A84B !important;
                    background-color: #1a1a2e !important;
                }
                [data-testid="stButton"] button:not([data-testid="baseButton-primary"]):hover {
                    background-color: #2a2a4e !important;
                    border-color: #f1c40f !important;
                }
                </style>
                """, unsafe_allow_html=True)
                
                col_save, col_contract, col_invoice = st.columns(3)
                
                with col_save:
                    if st.button(f"💾 {t('buttons.save')}", key="chk_pref_save", use_container_width=True, type="primary"):
                        try:
                            # تحديث بيانات التحليل لتشمل خطة التقسيط
                            current_analysis = car_data.get('analysis', {})
                            if 'installment_plan' in st.session_state:
                                current_analysis['payment_plan'] = st.session_state.installment_plan
                            
                            db = DatabaseManager()
                            # حفظ المعاملة كمسودة أو تحديثها
                            if 'last_transaction_id' not in st.session_state:
                                 tr_id = db.create_transaction(st.session_state.user['id'], car_data, estimated_price, current_analysis)
                                 st.session_state.last_transaction_id = tr_id
                                 st.success(f"✅ {t('messages.saved')}")
                            else:
                                # تحديث البيانات الحالية
                                db.update_transaction(st.session_state.last_transaction_id, {
                                    'estimated_price': estimated_price,
                                    'condition_analysis': json.dumps(current_analysis, ensure_ascii=False)
                                })
                                st.success(f"✅ {t('messages.saved')} (Updated)")
                        except Exception as e:
                            st.error(f"❌ {e}")

                with col_contract:
                    if st.button(f"📄 {t('admin.contract')}", key="chk_pref_contract", use_container_width=True):
                         try:
                             # تحديد قيم الأقساط من البيانات المحفوظة أو المحددة
                             if saved_prefs and payment_method_locked:
                                 contract_installment_count = saved_prefs.get('months', 0)
                                 contract_down_payment = saved_prefs.get('down_payment', 0)
                             else:
                                 contract_installment_count = selected_months if 'selected_months' in dir() and selected_months > 0 else 0
                                 contract_down_payment = down_payment if 'down_payment' in dir() else 0
                             
                             # تحديد طريقة الدفع
                             if contract_installment_count > 0:
                                 contract_payment_method = f"Installment ({contract_installment_count} months) / تقسيط"
                                 contract_monthly = (estimated_price - contract_down_payment) / contract_installment_count if contract_installment_count > 0 else 0
                             else:
                                 contract_payment_method = "Cash / كاش"
                                 contract_monthly = 0
                             
                             dummy_contract = {
                                 'id': 'DRAFT',
                                 'created_at': datetime.now(),
                                 'total_amount': estimated_price,
                                 'total_price': estimated_price,
                                 'paid_amount': 0,
                                 'status': 'Draft / مسودة',
                                 'payment_method': contract_payment_method,
                                 # بيانات السيارة مباشرة
                                 **(car_data if isinstance(car_data, dict) else {}),
                                 # البيانات المالية
                                 'down_payment': contract_down_payment,
                                 'remaining_amount': estimated_price - contract_down_payment,
                                 'monthly_installment': contract_monthly,
                                 'installment_count': contract_installment_count,
                                 'interest_rate': selected_interest if 'selected_interest' in dir() else 0,
                                 'car_details': json.dumps(car_data if isinstance(car_data, dict) else {})
                             }
                             gen = InvoiceGenerator()
                             # استخدام بيانات المستخدم الحالية
                             c_path = gen.generate_contract('DRAFT', dummy_contract, st.session_state.user, st.session_state.get('language', 'de'))
                             st.session_state['chk_draft_contract'] = c_path
                         except Exception as e:
                             st.error(f"❌ {e}")
                    
                    if 'chk_draft_contract' in st.session_state:
                         with open(st.session_state['chk_draft_contract'], "rb") as f:
                             st.download_button(f"⬇️ {t('buttons.download')}", f, file_name="Draft_Contract.pdf", key="dl_chk_contract", use_container_width=True)

                with col_invoice:
                    if st.button(f"🧾 {t('admin.invoice')}", key="chk_pref_invoice", use_container_width=True):
                         try:
                             # استخدام مولد فواتير الأقساط
                             from utils import InstallmentInvoiceGenerator
                             inv_gen = InstallmentInvoiceGenerator()
                             
                             # تحديد عدد الأقساط من البيانات المحفوظة أو المحددة حالياً
                             if saved_prefs and payment_method_locked:
                                 # إذا كانت الطريقة مقفلة، استخدم بيانات العقد المحفوظ
                                 invoice_installment_count = saved_prefs.get('months', 1)
                                 invoice_monthly_amount = saved_prefs.get('down_payment', 0) if invoice_installment_count <= 1 else estimated_price / invoice_installment_count
                             else:
                                 # وإلا استخدم الاختيار الحالي
                                 invoice_installment_count = selected_months if 'selected_months' in dir() and selected_months > 0 else 1
                                 invoice_monthly_amount = selected_monthly if 'selected_monthly' in dir() else estimated_price
                             
                             # بناء بيانات العقد للفواتير
                             contract_for_invoice = {
                                 'id': st.session_state.get('current_contract_id') or st.session_state.get('last_transaction_id', 'DRAFT'),
                                 'estimated_price': estimated_price,
                                 'total_price': final_contract_amount if 'final_contract_amount' in dir() else estimated_price,
                                 'down_payment': down_payment if 'down_payment' in dir() else 0,
                                 'installment_count': invoice_installment_count,
                                 'monthly_installment': invoice_monthly_amount,
                                 'created_at': datetime.now().strftime('%Y-%m-%d'),
                                 'full_name': st.session_state.user.get('full_name', 'N/A'),
                                 'id_number': st.session_state.user.get('id_number', ''),
                                 'phone': st.session_state.user.get('phone', ''),
                                 'street_name': st.session_state.user.get('street_name', ''),
                                 'building_number': st.session_state.user.get('building_number', ''),
                                 'postal_code': st.session_state.user.get('postal_code', ''),
                                 'city': st.session_state.user.get('city', ''),
                                 **car_data
                             }
                             
                             # توليد فواتير الأقساط
                             i_path = inv_gen._generate_summary_pdf(
                                 contract_for_invoice.get('id', 'DRAFT'), 
                                 contract_for_invoice
                             )
                             st.session_state['chk_draft_invoice'] = i_path
                             
                             # عدد الأقساط - الحد الأدنى 1 فاتورة حتى للدفع الكامل
                             num_invoices = max(1, contract_for_invoice.get('installment_count', 1))
                             if num_invoices == 1:
                                 st.success(f"✅ تم إنشاء فاتورة واحدة")
                             else:
                                 st.success(f"✅ تم إنشاء {num_invoices} فاتورة للأقساط")
                         except Exception as e:
                             st.error(f"❌ {e}")

                    if 'chk_draft_invoice' in st.session_state:
                         with open(st.session_state['chk_draft_invoice'], "rb") as f:
                             st.download_button(f"⬇️ {t('buttons.download')}", f, file_name="All_Invoices.pdf", key="dl_chk_invoice", use_container_width=True)

                # --- زر التأكيد (يظهر للكل) ---
                st.write("---")
                
                # التحقق من الجاهزية
                is_ready = False
                if pay_method == t('checkout.cash_branch'):
                    st.info(f"⚠️ {t('checkout.cash_hint')}")
                    is_ready = True
                elif uploaded_file is not None:
                     st.image(uploaded_file, caption=t('checkout.receipt_preview'), width=200)
                     is_ready = True
                
                if is_ready:
                    if st.button(f"✅ {t('checkout.create_contract_btn')}", type="primary"):
                        
                        spinner_text = t('checkout.creating_contract')
                        if pay_method != t('checkout.cash_branch'):
                            spinner_text = t('checkout.verifying_receipt')
                            
                        with st.spinner(spinner_text):
                            
                            # 1. إنشاء العقد
                            db = DatabaseManager()
                            
                            # التحقق من العميل المحدد إذا كان المستخدم أدمن
                            if st.session_state.user.get('role') == 'admin' and st.session_state.get('admin_selected_customer_id'):
                                user_id = st.session_state['admin_selected_customer_id']
                            else:
                                user_id = st.session_state.user['id']
                            
                            try:
                                new_contract_id = db.create_contract(
                                    user_id, 
                                    car_data, 
                                    final_contract_amount, 
                                    plan_type=selected_plan_type,
                                    installments_count=selected_months,
                                    interest_rate=selected_interest,
                                    monthly_amount=selected_monthly,
                                    payment_due_day=pref_due_day,
                                    grace_period=pref_grace
                                )
                                st.session_state.current_contract_id = new_contract_id
                                contract_id = new_contract_id
                                
                                # === توليد عقد PDF ===
                                gen = InvoiceGenerator()
                                
                                # تجميع بيانات العقد الكاملة
                                contract_pdf_data = {
                                    **car_data,  # بيانات السيارة من التنبؤ
                                    'total_price': final_contract_amount,
                                    'down_payment': down_payment if 'Installments' in plan_type else 0,
                                    'remaining_amount': final_contract_amount - (down_payment if 'Installments' in plan_type else 0),
                                    'monthly_installment': selected_monthly,
                                    'installment_count': selected_months,
                                    'interest_rate': selected_interest,
                                }
                                
                                # بيانات العميل - الأولوية لـ checkout_customer_data إذا كانت موجودة
                                if st.session_state.get('checkout_customer_data'):
                                    user_full_data = st.session_state['checkout_customer_data']
                                elif st.session_state.user.get('role') == 'admin' and st.session_state.get('admin_selected_customer_id'):
                                    customer_id = st.session_state['admin_selected_customer_id']
                                    user_full_data = db.get_user_by_id(customer_id)
                                    if not user_full_data:
                                        user_full_data = st.session_state.user
                                else:
                                    user_full_data = st.session_state.user
                                
                                # توليد PDF
                                contract_pdf_path = gen.generate_contract(contract_id, contract_pdf_data, user_full_data, st.session_state.get('language', 'de'))
                                st.session_state.last_contract_path = contract_pdf_path
                                
                            except Exception as e:
                                st.error(f"{t('admin.contract_save_error')}: {e}")
                                st.stop()

                            # 2. معالجة الدفع (إذا لم يكن نقداً)
                            payment_status = 'pending'
                            verified = False
                            
                            # نتحقق من وجود الملف المرفوع قبل محاولة القراءة
                            if uploaded_file is not None:
                                file_bytes = uploaded_file.getvalue()
                                claim = { 'amount': amount_to_pay, 'date': datetime.now().strftime('%Y-%m-%d') }
                                
                                try:
                                    # OCR Verify
                                    result = processor.verify_payment_claim(file_bytes, claim)
                                except Exception as e:
                                    st.error(f"{t('messages.error')}: {e}")
                                    st.stop()
                                
                                if result['verified']:
                                    st.balloons()
                                    st.success(result['message'])
                                    
                                    # Save to DB
                                    # Mock path for proof
                                    proof_path = f"receipt_{contract_id}_{int(time.time())}.jpg"
                                    
                                    pay_id = db.add_payment(contract_id, amount_to_pay, pay_method, proof_path, result.get('ai_data', {}).get('ref_number', 'REF'))
                                    db.verify_payment(pay_id) # Auto verify
                                    
                                    # Generate Invoice
                                    gen = InvoiceGenerator()
                                    summary = db.get_contract_summary(contract_id)
                                    # Fix: Pass user directly to generate_receipt
                                    pdf_path = gen.generate_receipt(f"INV-{pay_id}", {'amount': amount_to_pay, 'method': pay_method, 'date': datetime.now().strftime('%Y-%m-%d'), 'ref': result.get('ai_data', {}).get('ref_number')}, summary, st.session_state.user)
                                    
                                    st.session_state.last_invoice_path = pdf_path
                                    st.session_state.payment_success = True
                                    st.session_state.completed_payment_id = pay_id
                                    
                                else:
                                    st.error(f"❌ فشل التحقق الآلي: {result.get('reason', 'Unknown reason')}")
                                    
                                    # Even if failed, save as pending? Plan said "Mismatch = Manual Review"
                                    if 'manual_review' in result.get('status', ''):
                                        db = DatabaseManager() # Re-init just in case
                                        pay_id = db.add_payment(contract_id, amount_to_pay, pay_method, "path/pending", "PENDING")
                                        st.warning(f"⚠️ {t('admin.payment_pending_review')}")
                                        st.info(t('admin.notify_on_approval'))
                                        # لا نضع payment_success هنا لأننا ننتظر الموافقة
                                        
                            else:
                                # معالجة الدفع النقدي (Cash)
                                st.success(t('checkout.contract_created_success'))
                                st.info(t('checkout.cash_hint'))
                                
                                # تسجيل دفعة "معلقة"
                                try:
                                    db.add_payment(contract_id, amount_to_pay, "Cash", "pending_cash", "BRANCH-VISIT")
                                except: pass
                                
                                st.session_state.payment_success = True
                                
                            # تمت إزالة except اليتيم من هنا
                                
                # Trigger rerun to show success screen immediately
                if st.session_state.get('payment_success'):
                    st.rerun()


# ======================
# الدالة الرئيسية
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
        
        page_handlers = {
            'home': home_page,
            'predict': predict_page,
            'results': results_page,
            'verify_identity': verify_identity_page,
            'checkout': checkout_page,
            'invoices': invoices_page,
            'profile': profile_page,
            'change_password': change_password_page,
            'admin': admin_page
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
