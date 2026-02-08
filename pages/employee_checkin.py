"""
صفحة تسجيل الحضور الذاتي للموظفين
Employee Self-Service Attendance Page
Mitarbeiter-Selbstbedienung Anwesenheitsseite
"""
import streamlit as st
from db_manager import DatabaseManager
from datetime import datetime
import json
import os

# إعداد الصفحة
st.set_page_config(
    page_title="📱 Employee Check-In",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# إخفاء الـ sidebar
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    .stApp {background: linear-gradient(135deg, #0E1117 0%, #1a1a2e 100%);}
    .success-box {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin: 20px 0;
    }
    .error-box {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin: 20px 0;
    }
    .info-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #0E1117 100%);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #D4AF37;
        text-align: center;
        margin: 20px 0;
    }
    /* تصغير حجم الكاميرا إلى 25% */
    [data-testid="stCameraInput"] {
        max-width: 25% !important;
        margin: 0 auto !important;
    }
    [data-testid="stCameraInput"] video,
    [data-testid="stCameraInput"] img {
        max-width: 100% !important;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# تحميل اللغة
def load_language(lang_code):
    try:
        with open(f'locales/{lang_code}.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

# اختيار اللغة
lang = st.selectbox("🌐 Language", ["DE", "EN", "AR"], index=0, key="lang_select")
translations = load_language(lang.lower())

def t(key):
    keys = key.split('.')
    value = translations
    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return key
    return value if isinstance(value, str) else key

# العنوان
st.markdown(f"""
<div style="text-align: center; padding: 20px;">
    <h1 style="color: #D4AF37; font-size: 2.5rem;">📱 {t('admin.attendance')}</h1>
    <p style="color: #a0a0c0; font-size: 1.2rem;">{t('admin.qr_scan_desc') if t('admin.qr_scan_desc') != 'admin.qr_scan_desc' else 'Scan your QR code to check in/out'}</p>
</div>
""", unsafe_allow_html=True)

# قاعدة البيانات
db = DatabaseManager()

# اختيار طريقة الإدخال
st.markdown("---")
input_method = st.radio(
    t('admin.select_method') if t('admin.select_method') != 'admin.select_method' else "Select Method",
    [f"📷 {t('admin.camera') if t('admin.camera') != 'admin.camera' else 'Camera'}", 
     f"⌨️ {t('admin.manual_code') if t('admin.manual_code') != 'admin.manual_code' else 'Enter Code'}"],
    horizontal=True
)

qr_code_value = None

if "Camera" in input_method or "Kamera" in input_method or "الكاميرا" in input_method:
    # الكاميرا - تصغير الحجم باستخدام الأعمدة
    col1, col2, col3 = st.columns([3, 2, 3])  # 25% في الوسط
    with col2:
        captured_image = st.camera_input(
            t('admin.capture_qr') if t('admin.capture_qr') != 'admin.capture_qr' else "📸 QR"
        )
    
    if captured_image:
        try:
            from PIL import Image
            import numpy as np
            from pyzbar.pyzbar import decode
            
            img = Image.open(captured_image)
            img_array = np.array(img)
            decoded_objects = decode(img_array)
            
            if decoded_objects:
                qr_code_value = decoded_objects[0].data.decode('utf-8')
            else:
                st.warning("⚠️ " + (t('admin.no_qr_found') if t('admin.no_qr_found') != 'admin.no_qr_found' else "No QR code found"))
        except ImportError:
            st.error("❌ QR scanning libraries not installed")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
else:
    # إدخال يدوي
    qr_code_value = st.text_input(
        t('admin.enter_qr_code') if t('admin.enter_qr_code') != 'admin.enter_qr_code' else "Enter your QR Code",
        placeholder="e.g. 0FD0E0E221015BE8"
    )
    if qr_code_value:
        qr_code_value = qr_code_value.strip().upper()

# معالجة الكود تلقائياً
if qr_code_value:
    emp = db.get_employee_by_qr_token(qr_code_value.strip().upper())
    
    if emp:
        # عرض معلومات الموظف
        st.markdown(f"""
        <div class="info-box">
            <h2 style="color: #D4AF37; margin: 0;">👤 {emp['first_name']} {emp.get('last_name', '')}</h2>
            <p style="color: white; font-size: 1.1rem;">{emp.get('job_title', '')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # التحقق من حالة اليوم
        today_record = db.get_attendance_today(emp['id'])
        
        # تحديد العملية تلقائياً
        if today_record:
            if today_record.get('check_out'):
                # سجل حضور وانصراف بالفعل اليوم
                st.markdown(f"""
                <div class="info-box">
                    <h3 style="color: #27ae60;">✅ {t('admin.complete') if t('admin.complete') != 'admin.complete' else 'Completed for today'}</h3>
                    <p style="color: white;">🕒 {t('admin.check_in')}: {today_record['check_in'][:16]}</p>
                    <p style="color: white;">🕕 {t('admin.check_out')}: {today_record['check_out'][:16]}</p>
                    <p style="color: #D4AF37; font-size: 1.3rem;">⏱️ {today_record['net_worked_hours']:.2f}h</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # سجل حضور ولكن لم يسجل انصراف - يجب تسجيل الانصراف
                st.markdown(f"""
                <div style="background: #f39c12; padding: 20px; border-radius: 15px; text-align: center; margin: 20px 0;">
                    <h3 style="color: white; margin: 0;">🕒 {t('admin.check_in')}: {today_record['check_in'][11:16]}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🚪 {t('admin.check_out') if t('admin.check_out') != 'admin.check_out' else 'CHECK OUT'}", 
                            type="primary", use_container_width=True, key="auto_checkout"):
                    result = db.record_check_out(emp['id'])
                    if result['success']:
                        adj = result.get('adjustment', {})
                        st.markdown(f"""
                        <div class="success-box">
                            <h2 style="color: white; margin: 0;">✅ {t('admin.check_out_recorded') if t('admin.check_out_recorded') != 'admin.check_out_recorded' else 'Check-out recorded!'}</h2>
                            <p style="color: white; font-size: 1.5rem; margin: 15px 0;">⏱️ {result['net_worked_hours']:.2f}h</p>
                            {'<p style="color: white;">💰 +€' + f"{adj['amount']:.2f}</p>" if adj.get('type') == 'overtime' else ''}
                            {'<p style="color: white;">⚠️ -€' + f"{adj['amount']:.2f}</p>" if adj.get('type') == 'deduction' else ''}
                        </div>
                        """, unsafe_allow_html=True)
                        st.balloons()
        else:
            # لم يسجل حضور اليوم - يجب تسجيل الحضور
            current_time = datetime.now().strftime("%H:%M")
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <p style="color: #a0a0c0; font-size: 1.2rem;">🕐 {current_time}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"✅ {t('admin.check_in') if t('admin.check_in') != 'admin.check_in' else 'CHECK IN'}", 
                        type="primary", use_container_width=True, key="auto_checkin"):
                result = db.record_check_in(emp['id'])
                if result['success']:
                    st.markdown(f"""
                    <div class="success-box">
                        <h2 style="color: white; margin: 0;">✅ {t('admin.check_in_recorded') if t('admin.check_in_recorded') != 'admin.check_in_recorded' else 'Check-in recorded!'}</h2>
                        <p style="color: white; font-size: 2rem; margin: 15px 0;">🕐 {result['time']}</p>
                        <p style="color: white;">👋 {t('messages.success') if t('messages.success') != 'messages.success' else 'Have a great day!'}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.warning(f"⚠️ {t('admin.already_checked_in') if t('admin.already_checked_in') != 'admin.already_checked_in' else 'Already checked in'}")
    else:
        st.markdown(f"""
        <div class="error-box">
            <h3 style="color: white; margin: 0;">❌ {t('admin.invalid_qr') if t('admin.invalid_qr') != 'admin.invalid_qr' else 'Invalid QR Code'}</h3>
            <p style="color: white;">Please check your code and try again</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <p style="color: #666;">SmartCar AI Dealer - Employee Attendance System</p>
</div>
""", unsafe_allow_html=True)
