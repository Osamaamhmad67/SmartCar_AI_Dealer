"""
pages_app/profile_pages.py - صفحات الملف الشخصي
SmartCar AI-Dealer
"""

import streamlit as st
import streamlit.components.v1 as components
import os
import json
import base64
from pathlib import Path
from datetime import datetime
from utils.i18n import t, get_current_lang, is_rtl, rtl_tabs
from utils.invoice_generator import InvoiceGenerator
from config import Config
from db_manager import DatabaseManager
from auth import AuthManager
from components.html_components import (
    render_universal_header, get_profile_subheader_html, get_profile_stats_html
)
from components.navigation import navigate_to


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
