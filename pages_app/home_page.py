"""
pages_app/home_page.py - الصفحة الرئيسية
SmartCar AI-Dealer
"""

import streamlit as st
import streamlit.components.v1 as components
import os
import base64
import json
from datetime import datetime, timedelta
from utils.i18n import t, get_current_lang, is_rtl, rtl_tabs
from config import Config
from db_manager import DatabaseManager
from components.html_components import (
    render_universal_header, get_home_subheader_html,
    get_admin_dashboard_html, get_section_header_html
)
from utils.notifier import NotificationManager


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
                    user_label = f"👤 {admin_user.get('full_name') or admin_user.get('username', 'User')} - {admin_user.get('email', '')}"
                    with st.expander(user_label, expanded=False):
                        # === البيانات الأساسية ===
                        st.markdown(f"#### 📋 {t('admin.basic_info', 'Basic Information')}")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write(f"**{t('admin.username')}:** {admin_user.get('username', '-')}")
                            st.write(f"**{t('profile.full_name', 'Full Name')}:** {admin_user.get('full_name', '-')}")
                            st.write(f"**{t('admin.email')}:** {admin_user.get('email', '-')}")
                        
                        with col2:
                            st.write(f"**{t('profile.phone', 'Phone')}:** {admin_user.get('phone', '-')}")
                            st.write(f"**{t('profile.gender', 'Gender')}:** {admin_user.get('gender', '-')}")
                            st.write(f"**{t('profile.date_of_birth', 'Date of Birth')}:** {admin_user.get('date_of_birth') or admin_user.get('birth_date', '-')}")
                        
                        with col3:
                            st.write(f"**{t('admin.role')}:** {admin_user.get('role', 'user')}")
                            status = f"{t('admin.active')} ✅" if admin_user.get('is_active') else f"{t('admin.inactive')} ❌"
                            st.write(f"**{t('admin.status')}:** {status}")
                            st.write(f"**{t('profile.preferred_language', 'Language')}:** {admin_user.get('preferred_language', '-')}")
                        
                        # === بيانات الهوية ===
                        id_number = admin_user.get('id_number')
                        nationality = admin_user.get('nationality')
                        if id_number or nationality:
                            st.markdown(f"#### 🪪 {t('profile.id_card', 'ID Card')}")
                            id_col1, id_col2 = st.columns(2)
                            with id_col1:
                                st.write(f"**{t('profile.id_number', 'ID Number')}:** {id_number or '-'}")
                                st.write(f"**{t('profile.nationality', 'Nationality')}:** {nationality or '-'}")
                            with id_col2:
                                st.write(f"**{t('profile.birth_date', 'Birth Date')}:** {admin_user.get('birth_date', '-')}")
                                st.write(f"**{t('profile.expiry_date', 'Expiry Date')}:** {admin_user.get('expiry_date', '-')}")
                        
                        # === بيانات الرخصة ===
                        license_no = admin_user.get('license_number')
                        if license_no:
                            st.markdown(f"#### 🏎️ {t('profile.driver_license', 'Driver License')}")
                            lic_col1, lic_col2 = st.columns(2)
                            with lic_col1:
                                st.write(f"**{t('profile.license_number', 'License No.')}:** {license_no}")
                                st.write(f"**{t('profile.license_type', 'License Type')}:** {admin_user.get('license_type', '-')}")
                            with lic_col2:
                                st.write(f"**{t('profile.issue_date', 'Issue Date')}:** {admin_user.get('issue_date', '-')}")
                                st.write(f"**{t('profile.license_expiry', 'License Expiry')}:** {admin_user.get('license_expiry', '-')}")
                        
                        # === العنوان ===
                        has_address = any(admin_user.get(f) for f in ['street_name', 'city', 'postal_code', 'address'])
                        if has_address:
                            st.markdown(f"#### 📍 {t('profile.address', 'Address')}")
                            addr_col1, addr_col2 = st.columns(2)
                            with addr_col1:
                                if admin_user.get('address'):
                                    st.write(f"**{t('profile.address', 'Address')}:** {admin_user.get('address')}")
                                if admin_user.get('street_name'):
                                    st.write(f"**{t('profile.street', 'Street')}:** {admin_user.get('street_name')} {admin_user.get('building_number', '')}")
                            with addr_col2:
                                if admin_user.get('postal_code') or admin_user.get('city'):
                                    st.write(f"**{t('profile.city', 'City')}:** {admin_user.get('postal_code', '')} {admin_user.get('city', '')}")
                        
                        # === بيانات النظام ===
                        st.markdown(f"#### ⚙️ {t('admin.system_info', 'System Info')}")
                        sys_col1, sys_col2 = st.columns(2)
                        with sys_col1:
                            st.write(f"**{t('admin.registration_date')}:** {str(admin_user.get('created_at', ''))[:10]}")
                            st.write(f"**{t('admin.last_login')}:** {str(admin_user.get('last_login', ''))[:19]}")
                        with sys_col2:
                            st.write(f"**{t('admin.failed_attempts', 'Failed Login Attempts')}:** {admin_user.get('failed_attempts', 0)}")
                            locked = admin_user.get('locked_until')
                            if locked:
                                st.write(f"**{t('admin.locked_until', 'Locked Until')}:** {locked}")
                        
                        st.markdown("---")
                        
                        # Show success message if role was just saved
                        if st.session_state.get(f"role_saved_{admin_user.get('id')}"):
                            st.success(f"✅ {t('messages.success')} - {t('admin.save_role')}")
                            st.session_state[f"role_saved_{admin_user.get('id')}"] = False
                        
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
                        
                        # Row 2: Enable/Disable
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
                        st.markdown(f"#### 🔐 {t('admin.change_password', 'Change Password')}")
                        # عرض الهاش المختصر
                        pwd_hash = admin_user.get('password_hash', '')
                        if pwd_hash:
                            st.code(f"Hash: {pwd_hash[:20]}...{pwd_hash[-10:]}", language=None)
                        
                        pass_col1, pass_col2, pass_col3 = st.columns([2, 2, 1])
                        with pass_col1:
                            new_password = st.text_input(
                                t('admin.new_password', 'New Password'),
                                type="password",
                                key=f"new_pass_{admin_user.get('id')}"
                            )
                        with pass_col2:
                            confirm_password = st.text_input(
                                t('admin.confirm_password', 'Confirm Password'),
                                type="password",
                                key=f"confirm_pass_{admin_user.get('id')}"
                            )
                        with pass_col3:
                            st.write("")  # spacing
                            st.write("")
                            if st.button(f"💾 {t('admin.save_password', 'Save')}", key=f"save_pass_{admin_user.get('id')}", type="primary"):
                                if new_password and confirm_password:
                                    if new_password == confirm_password:
                                        from auth import AuthManager
                                        auth = AuthManager()
                                        hashed = auth.hash_password(new_password)
                                        db.update_user(admin_user.get('id'), password_hash=hashed)
                                        st.success(f"✅ {t('messages.success')}")
                                        st.rerun()
                                    else:
                                        st.error(f"❌ {t('admin.passwords_not_match', 'Passwords do not match')}")
                                else:
                                    st.error(f"❌ {t('admin.enter_password', 'Please enter password')}")
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
            from datetime import datetime
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
                                        📋 {t('predict.condition')}: {safe_get(car_info, 'condition')} |
                                        ⚙️ {t('predict.transmission', 'Transmission')}: {safe_get(car_info, 'transmission')} |
                                        🔧 {t('predict.drivetrain', 'Drivetrain')}: {safe_get(car_info, 'drivetrain')}<br>
                                        🏭 {t('predict.engine_cc', 'Engine CC')}: {safe_get(car_info, 'engine_cc')} |
                                        🐎 {t('predict.horsepower', 'PS')}: {safe_get(car_info, 'horsepower')} |
                                        🌿 {t('predict.emissions', 'Emissions')}: {safe_get(car_info, 'emissions_class')}<br>
                                        💥 {t('predict.accident', 'Accident')}: {safe_get(car_info, 'accident_history')} |
                                        🛡️ {t('predict.warranty', 'Warranty')}: {safe_get(car_info, 'warranty')} |
                                        📖 {t('predict.service_book', 'Service Book')}: {safe_get(car_info, 'service_book')}<br>
                                        🎯 {t('predict.equipment', 'Equipment')}: {safe_get(car_info, 'equipment', '-')}
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
                                            📋 {t('predict.condition')}: {safe_val(direct_condition)} |
                                            ⚙️ {t('predict.transmission', 'Transmission')}: {safe_val(c.get('transmission', '-'))} |
                                            🔧 {t('predict.drivetrain', 'Drivetrain')}: {safe_val(c.get('drivetrain', '-'))}<br>
                                            🏭 {t('predict.engine_cc', 'Engine CC')}: {safe_val(c.get('engine_cc', '-'))} |
                                            🐎 {t('predict.horsepower', 'PS')}: {safe_val(c.get('horsepower', '-'))} |
                                            🌿 {t('predict.emissions', 'Emissions')}: {safe_val(c.get('emissions_class', '-'))}<br>
                                            💥 {t('predict.accident', 'Accident')}: {safe_val(c.get('accident_history', '-'))} |
                                            🛡️ {t('predict.warranty', 'Warranty')}: {safe_val(c.get('warranty', '-'))} |
                                            📖 {t('predict.service_book', 'Service Book')}: {safe_val(c.get('service_book', '-'))}<br>
                                            🎯 {t('predict.equipment', 'Equipment')}: {safe_val(c.get('equipment', '-'))}
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


