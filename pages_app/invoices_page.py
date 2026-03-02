"""
pages_app/invoices_page.py - صفحة الفواتير
SmartCar AI-Dealer
"""

import streamlit as st
import streamlit.components.v1 as components
import os
import base64
from datetime import datetime
from utils.i18n import t, get_current_lang, is_rtl, rtl_tabs
from config import Config
from db_manager import DatabaseManager
from components.html_components import render_universal_header, get_invoices_subheader_html
from components.navigation import navigate_to


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
