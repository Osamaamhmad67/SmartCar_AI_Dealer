"""
pages_app/admin_page.py - لوحة تحكم المشرف
SmartCar AI-Dealer
"""

import streamlit as st
import streamlit.components.v1 as components
import os
import base64
import json
from datetime import datetime, timedelta
from io import BytesIO
from utils.i18n import t, get_current_lang, is_rtl, rtl_tabs
from config import Config
from db_manager import DatabaseManager
from components.html_components import (
    render_universal_header, get_admin_stats_html,
    get_admin_dashboard_html, get_section_header_html
)
from components.navigation import navigate_to
from utils.cache_manager import CacheManager
from utils.invoice_generator import InvoiceGenerator


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
        [t('admin.statistics'), '📊 مبيعات الموظفين', t('admin.users'), t('admin.employees'), t('admin.transactions'), t('admin.financial_settings'), f"📋 {t('admin.audit_log', 'Audit Log')}", f"📈 {t('admin.kpi', 'KPI Dashboard')}", f"📊 {t('admin.monthly_report', 'Monthly Report')}"]
    )
    
    db = DatabaseManager()
    
    if admin_menu == t('admin.statistics'):
        stats = db.get_statistics()
        
        # تنسيق احترافي للإحصائيات
        # تنسيق احترافي للإحصائيات (Unified Dashboard)
        get_admin_dashboard_html(stats)
        
        st.markdown("---")
        st.subheader(f"📊 {t('charts.advanced_analytics', 'Advanced Analytics')}")
        
        # Lazy import - تحميل المكتبات فقط عند الحاجة
        import pandas as pd
        import matplotlib.pyplot as plt
        import matplotlib as mpl
        import seaborn as sns
        
        # إعداد الخط لدعم العربية في الرسوم البيانية
        mpl.rcParams['font.family'] = 'sans-serif'
        mpl.rcParams['font.sans-serif'] = ['Tahoma', 'Arial', 'DejaVu Sans']
        mpl.rcParams['axes.unicode_minus'] = False
        
        # الحصول على بيانات التحليل مع caching
        @st.cache_data(ttl=300)  # Cache لمدة 5 دقائق
        def get_cached_transactions():
            return db.get_all_transactions()
        
        transactions = get_cached_transactions()
        
        if transactions and len(transactions) > 0:
            # تحويل إلى DataFrame
            df = pd.DataFrame(transactions)
            
            # تكوين Seaborn
            sns.set_theme(style="whitegrid", palette="muted")
            sns.set_context("notebook", font_scale=1.1)
            
            # عمودان للرسوم البيانية
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.markdown(f"### 🏎️ {t('charts.car_type_distribution', 'Car Type Distribution')}")
                if 'car_type' in df.columns and not df['car_type'].isna().all():
                    fig1, ax1 = plt.subplots(figsize=(8, 5))
                    car_counts = df['car_type'].value_counts()
                    sns.barplot(x=car_counts.values, y=car_counts.index, ax=ax1, palette="viridis")
                    ax1.set_xlabel(t('charts.count', 'Count'))
                    ax1.set_ylabel(t('charts.car_type', 'Car Type'))
                    plt.tight_layout()
                    st.pyplot(fig1)
                    plt.close()
                else:
                    st.info(t('charts.no_data', 'Not enough data'))
            
            with chart_col2:
                st.markdown(f"### 🏷️ {t('charts.avg_price_by_brand', 'Average Price by Brand')}")
                if 'brand' in df.columns and 'estimated_price' in df.columns:
                    brand_prices = df.groupby('brand')['estimated_price'].mean().sort_values(ascending=False).head(10)
                    if not brand_prices.empty:
                        fig2, ax2 = plt.subplots(figsize=(8, 5))
                        sns.barplot(x=brand_prices.values, y=brand_prices.index, ax=ax2, palette="rocket_r")
                        ax2.set_xlabel(t('charts.avg_price', 'Average Price (€)'))
                        ax2.set_ylabel(t('charts.brand', 'Brand'))
                        plt.tight_layout()
                        st.pyplot(fig2)
                        plt.close()
                    else:
                        st.info(t('charts.no_data', 'Not enough data'))
                else:
                    st.info(t('charts.no_data', 'Not enough data'))
            
            # رسم بياني خطي للمعاملات عبر الزمن
            st.markdown(f"### 📈 {t('charts.transactions_over_time', 'Transactions Over Time')}")
            if 'created_at' in df.columns:
                df['date'] = pd.to_datetime(df['created_at']).dt.date
                daily_counts = df.groupby('date').size()
                
                if len(daily_counts) > 0:
                    fig3, ax3 = plt.subplots(figsize=(12, 4))
                    sns.lineplot(x=daily_counts.index, y=daily_counts.values, ax=ax3, marker='o', color='#4CAF50', linewidth=2)
                    ax3.set_xlabel(t('charts.date', 'Date'))
                    ax3.set_ylabel(t('charts.transaction_count', 'Transaction Count'))
                    ax3.grid(True, alpha=0.3)
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    st.pyplot(fig3)
                    plt.close()
                else:
                    st.info(t('charts.no_transactions', 'No transactions to display'))
        else:
            st.info(f"📊 {t('charts.no_data_for_charts', 'Not enough data to generate charts')}")
    
    elif admin_menu == '📊 مبيعات الموظفين':
        st.subheader(f"📊 {t('charts.employee_sales_tracking', 'Employee Sales & Commission Tracking')}")
        
        # اختيار الشهر والسنة
        col_month, col_year = st.columns(2)
        with col_month:
            current_month = datetime.now().month
            month = st.selectbox(t('charts.month', 'Month'), list(range(1, 13)), index=current_month-1)
        with col_year:
            current_year = datetime.now().year
            year = st.number_input(t('charts.year', 'Year'), min_value=2020, max_value=2030, value=current_year)
        
        # نسبة العمولة
        commission_rate = st.slider(t('charts.commission_rate', 'Commission Rate %'), min_value=1.0, max_value=10.0, value=3.0, step=0.5) / 100
        
        # جلب البيانات مع caching
        @st.cache_data(ttl=180)  # Cache لمدة 3 دقائق
        def get_cached_sales_summary(month, year, rate):
            return db.get_all_employees_sales_summary(month, year, rate)
        
        sales_summary = get_cached_sales_summary(month, year, commission_rate)
        
        if not sales_summary:
            st.warning(f"⚠️ {t('charts.no_employees', 'No employees in the system')}")
        else:
            st.markdown("---")
            
            # جدول المبيعات
            st.markdown(f"### 📋 {t('charts.sales_summary', 'Sales & Salary Summary')}")
            
            for emp_data in sales_summary:
                with st.expander(f"👤 {emp_data['name']} - {t('charts.total', 'Total')}: {emp_data['total_salary']:.2f} €"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(f"🏁 {t('charts.sales_count', 'Sales Count')}", emp_data['sales_count'])
                        st.metric(f"💶 {t('charts.total_sales', 'Total Sales')}", f"{emp_data['total_sales']:.2f} €")
                    
                    with col2:
                        st.metric(f"💼 {t('charts.base_salary', 'Base Salary')}", f"{emp_data['monthly_salary']:.2f} €")
                        st.metric(f"🎁 {t('charts.commission', 'Commission')}", f"{emp_data['commission']:.2f} €")
                    
                    with col3:
                        st.metric(f"💰 {t('charts.monthly_total', 'Monthly Total')}", f"{emp_data['total_salary']:.2f} €", delta=f"+{emp_data['commission']:.2f} €")
            
            st.markdown("---")
            
            # الرسوم البيانية
            st.subheader(f"📊 {t('charts.visual_analytics', 'Visual Analytics')}")
            
            # Lazy import - تحميل المكتبات فقط عند الحاجة
            import pandas as pd
            import matplotlib.pyplot as plt
            import matplotlib as mpl
            import seaborn as sns
            
            # إعداد الخط لدعم العربية
            mpl.rcParams['font.family'] = 'sans-serif'
            mpl.rcParams['font.sans-serif'] = ['Tahoma', 'Arial', 'DejaVu Sans']
            mpl.rcParams['axes.unicode_minus'] = False
            
            # إعداد البيانات للرسوم
            df_sales = pd.DataFrame(sales_summary)
            
            if len(df_sales) > 0:
                # تكوين Seaborn
                sns.set_theme(style="whitegrid", palette="muted")
                
                # رسمان في صف واحد
                chart_col1, chart_col2 = st.columns(2)
                
                with chart_col1:
                    st.markdown(f"### 🏷️ {t('charts.employee_sales_comparison', 'Employee Sales Comparison')}")
                    fig1, ax1 = plt.subplots(figsize=(8, 5))
                    sns.barplot(data=df_sales, x='total_sales', y='name', ax=ax1, palette="viridis")
                    ax1.set_xlabel(t('charts.total_sales', 'Total Sales') + ' (€)')
                    ax1.set_ylabel(t('charts.employee', 'Employee'))
                    plt.tight_layout()
                    st.pyplot(fig1)
                    plt.close()
                
                with chart_col2:
                    st.markdown(f"### 💰 {t('charts.salary_comparison', 'Salary Comparison (Base + Commission)')}")
                    fig2, ax2 = plt.subplots(figsize=(8, 5))
                    
                    # إعداد بيانات الرواتب
                    x_pos = range(len(df_sales))
                    ax2.barh(x_pos, df_sales['monthly_salary'], label=t('charts.base_salary', 'Base Salary'), color='#4CAF50')
                    ax2.barh(x_pos, df_sales['commission'], left=df_sales['monthly_salary'], label=t('charts.commission', 'Commission'), color='#FFC107')
                    
                    ax2.set_yticks(x_pos)
                    ax2.set_yticklabels(df_sales['name'])
                    ax2.set_xlabel(t('charts.amount', 'Amount') + ' (€)')
                    ax2.set_ylabel(t('charts.employee', 'Employee'))
                    ax2.legend()
                    plt.tight_layout()
                    st.pyplot(fig2)
                    plt.close()
                
                # رسم بياني للعد
                st.markdown(f"### 🏁 {t('charts.sales_per_employee', 'Sales Per Employee')}")
                fig3, ax3 = plt.subplots(figsize=(12, 4))
                sns.barplot(data=df_sales, x='name', y='sales_count', ax=ax3, palette="rocket_r")
                ax3.set_xlabel(t('charts.employee', 'Employee'))
                ax3.set_ylabel(t('charts.sales_count', 'Sales Count'))
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig3)
                plt.close()
            else:
                st.info(t('charts.no_sales_data', 'No sales data for this month'))
    
    elif admin_menu == t('admin.users'):
        st.subheader(f"👥 {t('admin.users')}")
        
        users = db.get_all_users()
        
        if users:
            for user in users:
                with st.expander(f"👤 {user.get('full_name') or user.get('username', 'User')} - {user.get('email', '')}"):
                    # === البيانات الأساسية ===
                    st.markdown(f"#### 📋 {t('admin.basic_info', 'Basic Information')}")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**{t('admin.username')}:** {user.get('username', '-')}")
                        st.write(f"**{t('profile.full_name', 'Full Name')}:** {user.get('full_name', '-')}")
                        st.write(f"**{t('admin.email')}:** {user.get('email', '-')}")
                    
                    with col2:
                        st.write(f"**{t('profile.phone', 'Phone')}:** {user.get('phone', '-')}")
                        st.write(f"**{t('profile.gender', 'Gender')}:** {user.get('gender', '-')}")
                        st.write(f"**{t('profile.date_of_birth', 'Date of Birth')}:** {user.get('date_of_birth') or user.get('birth_date', '-')}")
                    
                    with col3:
                        st.write(f"**{t('admin.role')}:** {user.get('role', 'user')}")
                        status = f"{t('admin.active')} ✅" if user.get('is_active') else f"{t('admin.inactive')} ❌"
                        st.write(f"**{t('admin.status')}:** {status}")
                        st.write(f"**{t('profile.preferred_language', 'Language')}:** {user.get('preferred_language', '-')}")
                    
                    # === بيانات الهوية ===
                    id_number = user.get('id_number')
                    nationality = user.get('nationality')
                    if id_number or nationality:
                        st.markdown(f"#### 🪪 {t('profile.id_card', 'ID Card')}")
                        id_col1, id_col2 = st.columns(2)
                        with id_col1:
                            st.write(f"**{t('profile.id_number', 'ID Number')}:** {id_number or '-'}")
                            st.write(f"**{t('profile.nationality', 'Nationality')}:** {nationality or '-'}")
                        with id_col2:
                            st.write(f"**{t('profile.birth_date', 'Birth Date')}:** {user.get('birth_date', '-')}")
                            st.write(f"**{t('profile.expiry_date', 'Expiry Date')}:** {user.get('expiry_date', '-')}")
                    
                    # === بيانات الرخصة ===
                    license_no = user.get('license_number')
                    if license_no:
                        st.markdown(f"#### 🏎️ {t('profile.driver_license', 'Driver License')}")
                        lic_col1, lic_col2 = st.columns(2)
                        with lic_col1:
                            st.write(f"**{t('profile.license_number', 'License No.')}:** {license_no}")
                            st.write(f"**{t('profile.license_type', 'License Type')}:** {user.get('license_type', '-')}")
                        with lic_col2:
                            st.write(f"**{t('profile.issue_date', 'Issue Date')}:** {user.get('issue_date', '-')}")
                            st.write(f"**{t('profile.license_expiry', 'License Expiry')}:** {user.get('license_expiry', '-')}")
                    
                    # === العنوان ===
                    has_address = any(user.get(f) for f in ['street_name', 'city', 'postal_code', 'address'])
                    if has_address:
                        st.markdown(f"#### 📍 {t('profile.address', 'Address')}")
                        addr_col1, addr_col2 = st.columns(2)
                        with addr_col1:
                            if user.get('address'):
                                st.write(f"**{t('profile.address', 'Address')}:** {user.get('address')}")
                            if user.get('street_name'):
                                st.write(f"**{t('profile.street', 'Street')}:** {user.get('street_name')} {user.get('building_number', '')}")
                        with addr_col2:
                            if user.get('postal_code') or user.get('city'):
                                st.write(f"**{t('profile.city', 'City')}:** {user.get('postal_code', '')} {user.get('city', '')}")
                    
                    # === بيانات النظام ===
                    st.markdown(f"#### ⚙️ {t('admin.system_info', 'System Info')}")
                    sys_col1, sys_col2 = st.columns(2)
                    with sys_col1:
                        st.write(f"**{t('admin.registration_date')}:** {str(user.get('created_at', ''))[:10]}")
                        st.write(f"**{t('admin.last_login')}:** {str(user.get('last_login', ''))[:19]}")
                    with sys_col2:
                        st.write(f"**{t('admin.failed_attempts', 'Failed Login Attempts')}:** {user.get('failed_attempts', 0)}")
                        locked = user.get('locked_until')
                        if locked:
                            st.write(f"**{t('admin.locked_until', 'Locked Until')}:** {locked}")
                    
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
                    st.markdown(f"#### 🔐 {t('admin.change_password', 'Change Password')}")
                    # عرض الهاش المختصر
                    pwd_hash = user.get('password_hash', '')
                    if pwd_hash:
                        st.code(f"Hash: {pwd_hash[:20]}...{pwd_hash[-10:]}", language=None)
                    
                    pass_col1, pass_col2, pass_col3 = st.columns([2, 2, 1])
                    with pass_col1:
                        new_password = st.text_input(
                            t('admin.new_password', 'New Password'),
                            type="password",
                            key=f"new_pass_{user.get('id')}"
                        )
                    with pass_col2:
                        confirm_password = st.text_input(
                            t('admin.confirm_password', 'Confirm Password'),
                            type="password",
                            key=f"confirm_pass_{user.get('id')}"
                        )
                    with pass_col3:
                        st.write("")  # spacing
                        st.write("")
                        if st.button(f"💾 {t('admin.save_password', 'Save')}", key=f"save_pass_{user.get('id')}", type="primary"):
                            if new_password and confirm_password:
                                if new_password == confirm_password:
                                    from auth import AuthManager
                                    auth = AuthManager()
                                    hashed = auth.hash_password(new_password)
                                    db.update_user(user.get('id'), password_hash=hashed)
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
                
                st.markdown("---")
                
                # 3. Monthly Revenue Trend with Profit
                st.subheader(f"💰 {t('admin.monthly_revenue', 'Monthly Revenue Trend')}")
                
                df_trans['month'] = df_trans['created_at'].dt.to_period('M').astype(str)
                monthly_rev = df_trans.groupby('month').agg(
                    revenue=('estimated_price', 'sum'),
                    count=('estimated_price', 'count')
                ).reset_index()
                monthly_rev.columns = [t('admin.month', 'Month'), t('admin.revenue', 'Revenue (€)'), t('admin.count', 'Count')]
                
                rev_col1, rev_col2 = st.columns(2)
                
                with rev_col1:
                    fig_rev = go.Figure()
                    fig_rev.add_trace(go.Bar(
                        x=monthly_rev[t('admin.month', 'Month')],
                        y=monthly_rev[t('admin.revenue', 'Revenue (€)')],
                        name=t('admin.revenue', 'Revenue'),
                        marker_color='#4CAF50'
                    ))
                    fig_rev.add_trace(go.Scatter(
                        x=monthly_rev[t('admin.month', 'Month')],
                        y=monthly_rev[t('admin.revenue', 'Revenue (€)')],
                        name=t('admin.trend', 'Trend'),
                        line=dict(color='#FF9800', width=3),
                        mode='lines+markers'
                    ))
                    fig_rev.update_layout(
                        title=t('admin.monthly_revenue_chart', '📈 Monthly Revenue & Trend'),
                        barmode='group',
                        template='plotly_dark'
                    )
                    st.plotly_chart(fig_rev, use_container_width=True)
                
                with rev_col2:
                    # Price Distribution Histogram
                    fig_hist = px.histogram(
                        df_trans, x='estimated_price',
                        nbins=20,
                        title=t('admin.price_distribution', '📊 Price Distribution'),
                        labels={'estimated_price': t('admin.price', 'Price (€)'), 'count': t('admin.count', 'Count')},
                        color_discrete_sequence=['#E91E63']
                    )
                    fig_hist.update_layout(template='plotly_dark')
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                st.markdown("---")
                
                # 4. Top 5 Models & Employee Performance
                st.subheader(f"🏆 {t('admin.performance_analysis', 'Performance Analysis')}")
                
                perf_col1, perf_col2 = st.columns(2)
                
                with perf_col1:
                    # Top 5 Most Evaluated Models
                    df_trans['full_model'] = df_trans['brand'].fillna('') + ' ' + df_trans['car_type'].fillna('')
                    top_models = df_trans['full_model'].value_counts().head(5).reset_index()
                    top_models.columns = [t('admin.model', 'Model'), t('admin.count', 'Count')]
                    
                    fig_top = px.bar(
                        top_models, x=t('admin.count', 'Count'), y=t('admin.model', 'Model'),
                        orientation='h',
                        title=t('admin.top_models', '🥇 Top 5 Most Evaluated'),
                        color=t('admin.count', 'Count'),
                        color_continuous_scale='Viridis'
                    )
                    fig_top.update_layout(template='plotly_dark', yaxis={'categoryorder': 'total ascending'})
                    st.plotly_chart(fig_top, use_container_width=True)
                
                with perf_col2:
                    # Employee Performance
                    try:
                        with db.get_connection() as conn:
                            df_emp = pd.read_sql_query("""
                                SELECT e.first_name || ' ' || COALESCE(e.last_name, '') as name,
                                       COUNT(t.id) as sales,
                                       COALESCE(SUM(t.estimated_price), 0) as total_value
                                FROM employees e
                                LEFT JOIN transactions t ON t.employee_id = e.id
                                GROUP BY e.id
                                ORDER BY sales DESC
                                LIMIT 10
                            """, conn)
                        
                        if not df_emp.empty and df_emp['sales'].sum() > 0:
                            fig_emp = px.bar(
                                df_emp, x='sales', y='name',
                                orientation='h',
                                title=t('admin.employee_ranking', '👥 Employee Sales Ranking'),
                                color='total_value',
                                color_continuous_scale='Blues',
                                labels={'sales': t('admin.sales', 'Sales'), 'name': t('admin.employee', 'Employee'), 'total_value': t('admin.value', 'Value (€)')}
                            )
                            fig_emp.update_layout(template='plotly_dark', yaxis={'categoryorder': 'total ascending'})
                            st.plotly_chart(fig_emp, use_container_width=True)
                        else:
                            st.info(t('admin.no_employee_sales', 'No employee sales data yet'))
                    except Exception:
                        st.info(t('admin.no_employee_sales', 'No employee sales data yet'))
                
                st.markdown("---")
                
                # 📈 Demand Forecast
                st.subheader(f"📈 {t('admin.demand_forecast', 'Demand Forecast')}")
                try:
                    df_monthly = df_trans.set_index('created_at').resample('M').size().reset_index(name='count')
                    if len(df_monthly) >= 3:
                        # Simple moving average forecast
                        df_monthly['forecast'] = df_monthly['count'].rolling(window=3, min_periods=1).mean()
                        
                        # Add 3 future months
                        last_date = df_monthly['created_at'].max()
                        last_avg = df_monthly['forecast'].iloc[-1]
                        future_dates = pd.date_range(last_date + pd.DateOffset(months=1), periods=3, freq='M')
                        df_future = pd.DataFrame({'created_at': future_dates, 'count': [None]*3, 'forecast': [last_avg]*3})
                        df_all = pd.concat([df_monthly, df_future], ignore_index=True)
                        
                        import plotly.graph_objects as go
                        fig_fc = go.Figure()
                        fig_fc.add_trace(go.Bar(x=df_all['created_at'], y=df_all['count'], name=t('admin.actual', 'Actual'), marker_color='#3498db'))
                        fig_fc.add_trace(go.Scatter(x=df_all['created_at'], y=df_all['forecast'], name=t('admin.forecast', 'Forecast'), 
                            line=dict(color='#D4AF37', width=3, dash='dash'), mode='lines+markers'))
                        fig_fc.update_layout(template='plotly_dark', title=t('admin.monthly_forecast', '📈 Monthly Transactions + 3-Month Forecast'))
                        st.plotly_chart(fig_fc, use_container_width=True)
                    else:
                        st.info(t('admin.need_more_data', 'Need at least 3 months of data for forecast'))
                except Exception as e:
                    st.info(f"{t('admin.forecast_unavailable', 'Forecast unavailable')}: {e}")
                
                st.markdown("---")
                
                # 5. Quick Stats Summary Cards
                st.subheader(f"📋 {t('admin.quick_summary', 'Quick Summary')}")
                
                qs1, qs2, qs3, qs4 = st.columns(4)
                avg_price = df_trans['estimated_price'].mean()
                max_price = df_trans['estimated_price'].max()
                total_revenue = df_trans['estimated_price'].sum()
                this_month = df_trans[df_trans['created_at'].dt.month == pd.Timestamp.now().month]
                
                qs1.metric(t('admin.avg_price', 'Avg Price'), f"€{avg_price:,.0f}")
                qs2.metric(t('admin.max_price', 'Max Price'), f"€{max_price:,.0f}")
                qs3.metric(t('admin.total_revenue', 'Total Revenue'), f"€{total_revenue:,.0f}")
                qs4.metric(t('admin.this_month', 'This Month'), f"{len(this_month)} {t('admin.transactions_label', 'transactions')}")
                

            else:
                st.info(t('admin.no_chart_data'))
                
        except Exception as e:
            st.error(f"{t('messages.error')}: {e}")
            
    elif admin_menu == t('admin.financial_settings'):
        st.subheader(f"⚙️ {t('admin.system_settings')}")
        
        # Excel Export
        if st.button(f"📊 {t('admin.export_excel', 'Export All Data (Excel)')}", use_container_width=True, type="primary"):
            try:
                from utils.excel_export import ExcelExporter
                data = ExcelExporter.export_all_data()
                st.download_button("⬇️ Download Excel", data, 
                    file_name=f"SmartCar_Export_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="dl_excel")
            except Exception as e:
                st.error(f"❌ {e}")
        
        st.markdown("---")
        
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
            
            st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
            
            # Notification Reminders Button
            if st.button(f"🔔 {t('admin.send_reminders', 'Send Reminders')}", use_container_width=True, help="Send installment & TÜV reminders"):
                with st.spinner(t('admin.sending_reminders', 'Sending reminders...')):
                    try:
                        from utils.notifier import NotificationManager
                        notifier = NotificationManager()
                        results = notifier.run_all_reminders()
                        
                        st.success(f"""
                        ✅ {t('admin.reminders_sent', 'Reminders processed!')}
                        - 📋 {t('admin.installments_found', 'Installments due')}: {results['installments_found']}
                        - 📧 {t('admin.reminders_emailed', 'Emails sent')}: {results['installments_sent']}
                        - 🚗 {t('admin.tuv_found', 'TÜV checks')}: {results['tuv_found']}
                        """)
                        
                        if results['errors']:
                            st.warning(f"⚠️ {len(results['errors'])} errors occurred")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        

        # DATEV Export Section
        st.markdown("---")
        st.markdown(f"### 📊 {t('admin.datev_export', 'DATEV Export')}")
        st.caption(t('admin.datev_hint', 'Export data in DATEV-compatible CSV format for German accounting'))
        
        datev_c1, datev_c2 = st.columns(2)
        with datev_c1:
            if st.button(f"📊 {t('admin.export_transactions', 'Export Transactions CSV')}", use_container_width=True):
                try:
                    from utils.datev_export import DATEVExporter
                    csv_data = DATEVExporter.export_transactions()
                    st.download_button("⬇️ Download DATEV Transactions", csv_data, 
                        file_name=f"DATEV_Transactions_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv", key="dl_datev_trans")
                except Exception as e:
                    st.error(f"❌ {e}")
        with datev_c2:
            if st.button(f"🧾 {t('admin.export_invoices', 'Export Invoices CSV')}", use_container_width=True):
                try:
                    from utils.datev_export import DATEVExporter
                    csv_data = DATEVExporter.export_invoices()
                    st.download_button("⬇️ Download DATEV Invoices", csv_data,
                        file_name=f"DATEV_Invoices_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv", key="dl_datev_inv")
                except Exception as e:
                    st.error(f"❌ {e}")

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


    elif admin_menu == f"📋 {t('admin.audit_log', 'Audit Log')}":
        st.subheader(f"📋 {t('admin.audit_log', 'Audit Log')}")
        
        from utils.audit_logger import AuditLogger
        
        # Stats
        audit_stats = AuditLogger.get_stats()
        s1, s2, s3 = st.columns(3)
        s1.metric(t('admin.total_events', 'Total Events'), audit_stats['total'])
        s2.metric(t('admin.today_events', 'Today'), audit_stats['today'])
        s3.metric(t('admin.top_action', 'Top Action'), audit_stats['top_actions'][0][0] if audit_stats['top_actions'] else '-')
        
        st.markdown("---")
        
        # Filters
        f1, f2, f3 = st.columns(3)
        with f1:
            action_filter = st.selectbox(t('admin.filter_action', 'Filter Action'), 
                [''] + ['login', 'logout', 'login_failed', 'user_create', 'transaction_create', 'contract_create', 'invoice_create', 'payment_record', 'settings_change', 'ai_analysis', 'backup_create'],
                key="audit_action_filter")
        with f2:
            user_filter = st.text_input(t('admin.filter_user', 'Filter User'), key="audit_user_filter")
        with f3:
            limit = st.number_input(t('admin.limit', 'Limit'), min_value=10, max_value=500, value=50, step=10)
        
        logs = AuditLogger.get_logs(limit=limit, 
            action_filter=action_filter if action_filter else None,
            user_filter=user_filter if user_filter else None)
        
        if logs:
            action_colors = {
                'login': '#27ae60', 'logout': '#95a5a6', 'login_failed': '#e74c3c',
                'transaction_create': '#3498db', 'contract_create': '#9b59b6',
                'invoice_create': '#f39c12', 'payment_record': '#2ecc71',
                'settings_change': '#e67e22', 'ai_analysis': '#1abc9c',
                'backup_create': '#34495e', 'user_create': '#2980b9'
            }
            
            for log_entry in logs:
                action = log_entry.get('action', '')
                color = action_colors.get(action, '#7f8c8d')
                created = log_entry.get('created_at', '')[:19]
                user = log_entry.get('username', '-')
                details = log_entry.get('details', '')
                entity = f"{log_entry.get('entity_type', '')} #{log_entry.get('entity_id', '')}" if log_entry.get('entity_type') else ''
                
                st.markdown(f"""
                <div style="background: #16213e; padding: 10px 15px; border-radius: 8px; margin: 5px 0; border-left: 4px solid {color}; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="background: {color}22; color: {color}; padding: 2px 8px; border-radius: 12px; font-size: 0.8em;">{action}</span>
                        <span style="color: white; margin-left: 10px;">👤 {user}</span>
                        <span style="color: #a0a0c0; margin-left: 10px;">{entity}</span>
                    </div>
                    <span style="color: #a0a0c0; font-size: 0.8em;">🕐 {created}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(t('admin.no_audit_logs', 'No audit logs found'))

    elif admin_menu == f"📈 {t('admin.kpi', 'KPI Dashboard')}":
        st.subheader(f"📈 {t('admin.kpi', 'KPI Dashboard')}")
        
        stats = db.get_statistics()
        
        # KPI targets (configurable)
        targets = {
            'monthly_sales': st.sidebar.number_input(t('admin.target_sales', 'Target Sales/Month'), value=20, key="kpi_sales"),
            'monthly_revenue': st.sidebar.number_input(t('admin.target_revenue', 'Target Revenue (€)'), value=200000, step=10000, key="kpi_rev"),
            'monthly_users': st.sidebar.number_input(t('admin.target_users', 'Target New Users'), value=10, key="kpi_users"),
        }
        
        import pandas as pd
        # Get current month data
        with db.get_connection() as conn:
            current_month = pd.Timestamp.now().strftime('%Y-%m')
            cur_sales = pd.read_sql_query(f"SELECT COUNT(*) as c FROM transactions WHERE created_at LIKE '{current_month}%'", conn).iloc[0]['c']
            cur_revenue = pd.read_sql_query(f"SELECT COALESCE(SUM(estimated_price),0) as r FROM transactions WHERE created_at LIKE '{current_month}%'", conn).iloc[0]['r']
            cur_users = pd.read_sql_query(f"SELECT COUNT(*) as c FROM users WHERE created_at LIKE '{current_month}%'", conn).iloc[0]['c']
        
        kpis = [
            ('🛒', t('admin.sales', 'Sales'), cur_sales, targets['monthly_sales']),
            ('💰', t('admin.revenue', 'Revenue'), cur_revenue, targets['monthly_revenue']),
            ('👥', t('admin.new_users', 'New Users'), cur_users, targets['monthly_users']),
        ]
        
        cols = st.columns(3)
        for i, (icon, label, actual, target) in enumerate(kpis):
            with cols[i]:
                pct = min((actual / max(target, 1)) * 100, 100)
                color = '#27ae60' if pct >= 80 else '#f39c12' if pct >= 50 else '#e74c3c'
                st.markdown(f"""
                <div style="background: #16213e; padding: 20px; border-radius: 15px; text-align: center; border: 1px solid {color}33;">
                    <div style="font-size: 2em;">{icon}</div>
                    <div style="color: #D4AF37; font-weight: bold;">{label}</div>
                    <div style="color: white; font-size: 1.8em; font-weight: bold;">{actual:,.0f}</div>
                    <div style="color: #a0a0c0;">/ {target:,.0f} target</div>
                    <div style="background: #1a1a2e; border-radius: 10px; height: 8px; margin-top: 10px;">
                        <div style="background: {color}; width: {pct:.0f}%; height: 8px; border-radius: 10px;"></div>
                    </div>
                    <div style="color: {color}; font-size: 0.9em; margin-top: 5px;">{pct:.0f}%</div>
                </div>
                """, unsafe_allow_html=True)

    elif admin_menu == f"📊 {t('admin.monthly_report', 'Monthly Report')}":
        st.subheader(f"📊 {t('admin.monthly_report', 'Monthly Report')}")
        
        from utils.report_generator import ReportGenerator
        
        rc1, rc2 = st.columns(2)
        with rc1:
            report_year = st.number_input("Year", value=datetime.now().year, key="rep_year")
        with rc2:
            report_month = st.number_input("Month", min_value=1, max_value=12, value=datetime.now().month, key="rep_month")
        
        if st.button(f"📊 {t('admin.generate_report', 'Generate Report')}", type="primary", use_container_width=True):
            data = ReportGenerator.get_monthly_summary(int(report_year), int(report_month))
            report_text = ReportGenerator.format_report_text(data)
            
            st.code(report_text)
            
            st.download_button(f"⬇️ Download Report", report_text, 
                file_name=f"Report_{report_year}_{report_month:02d}.txt",
                mime="text/plain", key="dl_report")
            
            # WhatsApp share
            from utils.whatsapp_sender import WhatsAppSender
            wa_link = WhatsAppSender.generate_link("", f"SmartCar Report {report_month}/{report_year}")
            st.markdown(f"[📱 Share via WhatsApp]({wa_link})")



# ======================
# دالة عرض الميزات
