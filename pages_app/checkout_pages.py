"""
pages_app/checkout_pages.py - صفحات الدفع والتعاقد
SmartCar AI-Dealer
"""

import streamlit as st
import streamlit.components.v1 as components
import os
import base64
import json
import time
from io import BytesIO
from datetime import datetime
from utils.i18n import t, get_current_lang, is_rtl, rtl_tabs
from config import Config
from db_manager import DatabaseManager
from utils.payment_processor import PaymentProcessor
from utils.invoice_generator import InvoiceGenerator
from components.html_components import render_universal_header, get_section_header_html
from components.navigation import navigate_to


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
    # إذا كان الأدمن يعمل نيابة عن عميل، نستخدم بيانات العميل
    if st.session_state.user.get('role') == 'admin':
        # محاولة جلب بيانات العميل المحدد
        customer_data = st.session_state.get('checkout_customer_data') or st.session_state.get('selected_customer_for_invoice')
        if customer_data:
            user = customer_data
        elif st.session_state.get('admin_selected_customer_id'):
            db = DatabaseManager()
            user = db.get_user_by_id(st.session_state['admin_selected_customer_id']) or st.session_state.user
        else:
            user = st.session_state.user
    else:
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
            # خيار بين المسح الضوئي والإدخال اليدوي
            entry_mode = st.radio(
                "اختر طريقة الإدخال:",
                ["📸 مسح ضوئي (OCR)", "⌨️ إدخال يدوي"],
                horizontal=True,
                key="id_entry_mode"
            )
            
            if entry_mode == "⌨️ إدخال يدوي":
                # === نموذج الإدخال اليدوي ===
                st.markdown("### 📝 أدخل بيانات الهوية يدوياً")
                
                # جلب الاسم والإيميل من بيانات المستخدم المسجل
                default_name = user.get('full_name', '') or ''
                default_email = user.get('email', '') or ''
                
                manual_full_name = st.text_input("الاسم الكامل *", value=default_name, key="manual_id_name")
                manual_email = st.text_input("البريد الإلكتروني", value=default_email, key="manual_id_email")
                manual_id_number = st.text_input("رقم الهوية *", key="manual_id_num")
                
                col_n1, col_n2 = st.columns(2)
                with col_n1:
                    manual_nationality = st.text_input(
                        "الجنسية *",
                        key="manual_nationality"
                    )
                with col_n2:
                    manual_gender = st.selectbox("الجنس", ["ذكر", "أنثى"], key="manual_gender")
                
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    from datetime import date
                    manual_birth_date = st.date_input("تاريخ الميلاد", value=date(1990, 1, 1), key="manual_birth")
                with col_d2:
                    manual_expiry_date = st.date_input("تاريخ انتهاء الهوية", value=date(2030, 12, 31), key="manual_expiry")
                
                if st.button("✅ حفظ البيانات", type="primary", use_container_width=True, key="save_manual_id"):
                    if manual_full_name and manual_id_number:
                        try:
                            manual_data = {
                                'full_name': manual_full_name,
                                'email': manual_email,
                                'id_number': manual_id_number,
                                'nationality': manual_nationality,
                                'gender': manual_gender,
                                'birth_date': str(manual_birth_date),
                                'expiry_date': str(manual_expiry_date)
                            }
                            db.update_user(user['id'], **manual_data)
                            st.session_state.user.update(manual_data)
                            st.success("✅ تم حفظ بيانات الهوية بنجاح!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ خطأ في الحفظ: {e}")
                    else:
                        st.warning("⚠️ يرجى ملء الحقول المطلوبة (الاسم ورقم الهوية)")
            
            else:
                # === المسح الضوئي (الطريقة القديمة) ===
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
                                        if 'scanned_id_data' in st.session_state:
                                            del st.session_state.scanned_id_data
                                        st.success("✅ تم حفظ البيانات المتاحة")
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
            # خيار بين المسح الضوئي والإدخال اليدوي
            entry_mode_lic = st.radio(
                "اختر طريقة الإدخال:",
                ["📸 مسح ضوئي (OCR)", "⌨️ إدخال يدوي"],
                horizontal=True,
                key="lic_entry_mode"
            )
            
            if entry_mode_lic == "⌨️ إدخال يدوي":
                # === نموذج الإدخال اليدوي ===
                st.markdown("### 🚗 أدخل بيانات الرخصة يدوياً")
                
                manual_license_number = st.text_input("رقم الرخصة *", key="manual_lic_num")
                
                col_l1, col_l2 = st.columns(2)
                with col_l1:
                    from datetime import date
                    manual_license_issue = st.date_input("تاريخ الإصدار", value=date(2020, 1, 1), key="manual_lic_issue")
                with col_l2:
                    manual_license_expiry = st.date_input("تاريخ الانتهاء", value=date(2030, 12, 31), key="manual_lic_expiry")
                
                manual_license_type = st.selectbox(
                    "نوع الرخصة",
                    ["B (سيارات خاصة)", "C (شاحنات)", "D (حافلات)", "أخرى"],
                    key="manual_lic_type"
                )
                
                if st.button("✅ حفظ البيانات", type="primary", use_container_width=True, key="save_manual_lic"):
                    if manual_license_number:
                        try:
                            manual_lic_data = {
                                'license_number': manual_license_number,
                                'license_issue_date': str(manual_license_issue),
                                'license_expiry_date': str(manual_license_expiry),
                                'license_type': manual_license_type
                            }
                            db.update_user(user['id'], **manual_lic_data)
                            st.session_state.user.update(manual_lic_data)
                            st.success("✅ تم حفظ بيانات الرخصة بنجاح!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ خطأ في الحفظ: {e}")
                    else:
                        st.warning("⚠️ يرجى إدخال رقم الرخصة")
            
            else:
                # === المسح الضوئي (الطريقة القديمة) ===
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
            customer_options = {f"{u.get('full_name') or u.get('username')} ({u.get('email')})": u for u in customers}
            
            selected_customer_key = st.selectbox(
                t('admin.customer_owner'),
                options=list(customer_options.keys()),
                key="checkout_customer_select"
            )
            
            selected_cust = customer_options.get(selected_customer_key)
            st.session_state['admin_selected_customer_id'] = selected_cust['id'] if selected_cust else None
            st.session_state['checkout_customer_data'] = selected_cust  # حفظ بيانات العميل الكاملة
            st.markdown(f"""<div style='background: linear-gradient(135deg, #0E1117 0%, #1a2e1a 100%); padding: 12px 16px; border-radius: 8px; border-right: 4px solid #28a745; margin: 10px 0;'>
                <span style='color: #38ef7d !important; font-size: 0.95rem; font-weight: 500;'>✅ {t('admin.link_contract_info')}</span>
            </div>""", unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ {t('admin.no_customers')}")
            st.session_state['admin_selected_customer_id'] = None
            st.session_state['checkout_customer_data'] = None

    
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
                            # تحديد العميل الحقيقي (إذا كان الأدمن يعمل نيابة عن عميل)
                            if st.session_state.user.get('role') == 'admin' and st.session_state.get('admin_selected_customer_id'):
                                save_user_id = st.session_state['admin_selected_customer_id']
                            else:
                                save_user_id = st.session_state.user['id']
                            # حفظ المعاملة كمسودة أو تحديثها
                            if 'last_transaction_id' not in st.session_state:
                                 # ربط الموظف لاحتساب العمولة
                                 chk_emp = db.get_employee_by_user_id(st.session_state.user['id'])
                                 chk_emp_id = chk_emp['id'] if chk_emp else None
                                 tr_id = db.create_transaction(save_user_id, car_data, estimated_price, current_analysis, employee_id=chk_emp_id)
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
                             
                             # جلب مسار الصورة من قاعدة البيانات
                             _db_img = DatabaseManager()
                             _tx_id = st.session_state.get('last_transaction_id') or st.session_state.get('current_contract_id')
                             _img_path = ''
                             if _tx_id:
                                 try:
                                     import sqlite3
                                     _conn = sqlite3.connect(str(_db_img.db_path))
                                     _conn.row_factory = sqlite3.Row
                                     _cur = _conn.cursor()
                                     _cur.execute('SELECT image_path FROM transactions WHERE id = ?', (_tx_id,))
                                     _row = _cur.fetchone()
                                     if _row and _row['image_path'] and _row['image_path'] != 'stored_in_session':
                                         _img_path = _row['image_path']
                                     _conn.close()
                                 except:
                                     pass
                             # Fallback: from car_data or session state
                             if not _img_path:
                                 _img_path = car_data.get('image_path', '') if isinstance(car_data, dict) else ''
                             if not _img_path or _img_path == 'stored_in_session':
                                 _img_path = st.session_state.get('car_image_path', '')

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
                                 # صورة السيارة
                                 'image_path': _img_path,
                                 # البيانات المالية
                                 'down_payment': contract_down_payment,
                                 'remaining_amount': estimated_price - contract_down_payment,
                                 'monthly_installment': contract_monthly,
                                 'installment_count': contract_installment_count,
                                 'interest_rate': selected_interest if 'selected_interest' in dir() else 0,
                                 'car_details': json.dumps(car_data if isinstance(car_data, dict) else {})
                             }
                             gen = InvoiceGenerator()
                             # استخدام بيانات العميل الحقيقي (وليس الأدمن)
                             if st.session_state.user.get('role') == 'admin' and st.session_state.get('checkout_customer_data'):
                                 contract_user_data = st.session_state['checkout_customer_data']
                             elif st.session_state.user.get('role') == 'admin' and st.session_state.get('admin_selected_customer_id'):
                                 contract_user_data = DatabaseManager().get_user_by_id(st.session_state['admin_selected_customer_id']) or st.session_state.user
                             else:
                                 contract_user_data = st.session_state.user
                             c_path = gen.generate_contract('DRAFT', dummy_contract, contract_user_data, st.session_state.get('language', 'de'))
                             st.session_state['chk_draft_contract'] = c_path
                         except Exception as e:
                             st.error(f"❌ {e}")
                    
                    if 'chk_draft_contract' in st.session_state:
                         with open(st.session_state['chk_draft_contract'], "rb") as f:
                             pdf_bytes = f.read()
                             st.download_button(f"⬇️ {t('buttons.download')}", pdf_bytes, file_name="Draft_Contract.pdf", key="dl_chk_contract", use_container_width=True)
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
                             
                             # تحديد بيانات العميل الحقيقي للفاتورة
                             if st.session_state.user.get('role') == 'admin' and st.session_state.get('checkout_customer_data'):
                                 inv_customer = st.session_state['checkout_customer_data']
                             elif st.session_state.user.get('role') == 'admin' and st.session_state.get('admin_selected_customer_id'):
                                 inv_customer = DatabaseManager().get_user_by_id(st.session_state['admin_selected_customer_id']) or st.session_state.user
                             else:
                                 inv_customer = st.session_state.user
                             
                             # بناء بيانات العقد للفواتير
                             contract_for_invoice = {
                                 'id': st.session_state.get('current_contract_id') or st.session_state.get('last_transaction_id', 'DRAFT'),
                                 'estimated_price': estimated_price,
                                 'total_price': final_contract_amount if 'final_contract_amount' in dir() else estimated_price,
                                 'down_payment': down_payment if 'down_payment' in dir() else 0,
                                 'installment_count': invoice_installment_count,
                                 'monthly_installment': invoice_monthly_amount,
                                 'created_at': datetime.now().strftime('%Y-%m-%d'),
                                 'full_name': inv_customer.get('full_name', 'N/A'),
                                 'id_number': inv_customer.get('id_number', ''),
                                 'phone': inv_customer.get('phone', ''),
                                 'street_name': inv_customer.get('street_name', ''),
                                 'building_number': inv_customer.get('building_number', ''),
                                 'postal_code': inv_customer.get('postal_code', ''),
                                 'city': inv_customer.get('city', ''),
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
                             pdf_bytes_inv = f.read()
                             st.download_button(f"⬇️ {t('buttons.download')}", pdf_bytes_inv, file_name="All_Invoices.pdf", key="dl_chk_invoice", use_container_width=True)
                # --- زر التأكيد (يظهر للكل) ---
                st.write("---")
                
                # === عرض رقم القسط التالي المطلوب دفعه ===
                current_contract_id_for_info = st.session_state.get('current_contract_id')
                all_installments_paid = False
                
                if current_contract_id_for_info and (t('checkout.choose_installment_plan') in plan_type or "Installments" in plan_type):
                    try:
                        next_inst = db.get_next_pending_installment(current_contract_id_for_info)
                        if next_inst:
                            if next_inst.get('completed'):
                                st.success(f"✅ {t('checkout.all_installments_paid')}")
                                all_installments_paid = True
                            else:
                                inst_num = next_inst.get('installment_number', 1)
                                total_inst = next_inst.get('total_installments', 0)
                                inst_amount = next_inst.get('amount_due', 0)
                                due_date = next_inst.get('due_date', '')
                                paid_count = next_inst.get('paid_count', 0)
                                
                                st.markdown(f"""
                                <div style="background: linear-gradient(135deg, #0E1117 0%, #1a2e1a 100%); 
                                            padding: 15px; border-radius: 10px; border: 2px solid #4CAF50; margin: 10px 0;">
                                    <h4 style="color: #4CAF50; margin: 0;">📋 {t('checkout.next_installment_info')}</h4>
                                    <table style="width: 100%; color: #fff; margin-top: 10px;">
                                        <tr>
                                            <td style="padding: 5px 0;">🔢 {t('checkout.installment_number')}:</td>
                                            <td style="font-weight: bold; color: #4facfe;">{inst_num} / {total_inst}</td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 5px 0;">✅ {t('checkout.paid_installments')}:</td>
                                            <td style="font-weight: bold; color: #4CAF50;">{paid_count}</td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 5px 0;">💰 {t('checkout.amount')}:</td>
                                            <td style="font-weight: bold;">{inst_amount:,.2f} €</td>
                                        </tr>
                                    </table>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if due_date:
                                    st.info(f"📅 {t('checkout.due_date')}: {due_date}")
                    except Exception:
                        pass  # إذا فشل الاستعلام لا نوقف الصفحة
                
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
                                    # Fix: Pass customer data (not admin) to generate_receipt
                                    receipt_user = user_full_data if 'user_full_data' in dir() else st.session_state.user
                                    pdf_path = gen.generate_receipt(f"INV-{pay_id}", {'amount': amount_to_pay, 'method': pay_method, 'date': datetime.now().strftime('%Y-%m-%d'), 'ref': result.get('ai_data', {}).get('ref_number')}, summary, receipt_user)
                                    
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
