"""
components/html_components.py - مكونات HTML/CSS الاحترافية
SmartCar AI-Dealer
تم استخراجها من app.py لتحسين الأداء
"""

import os
import base64
import streamlit as st
import streamlit.components.v1 as components
from utils.i18n import t, get_current_lang, is_rtl


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
