"""
🔄 صفحة CRM — متابعة العملاء
SmartCar AI-Dealer
"""

import streamlit as st
from datetime import datetime, date
from db_manager import DatabaseManager
from utils.i18n import t
from components.html_components import render_universal_header
from components.navigation import navigate_to


def crm_page():
    """صفحة CRM — نظام متابعة العملاء"""
    # التحقق من صلاحيات المشرف
    if st.session_state.user.get('role') != 'admin':
        st.error(f"⛔ {t('messages.error')}")
        navigate_to('home')
        return

    render_universal_header(t('crm.title', 'CRM — Customer Follow-up'), "🔄 " + t('crm.subtitle', 'Customer Management'))

    db = DatabaseManager()

    # Due Follow-ups Alert
    due_list = db.get_due_followups()
    if due_list:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #e74c3c22, #c0392b22); border: 1px solid #e74c3c55;
                    border-radius: 12px; padding: 15px; margin-bottom: 15px;">
            <span style="color: #e74c3c; font-weight: bold; font-size: 1.1em;">
                ⚠️ {t('crm.due_alert', 'Follow-ups Due')} — {len(due_list)} {t('crm.customers', 'customer(s)')}
            </span>
        </div>
        """, unsafe_allow_html=True)

    # Status counts
    all_followups = db.get_all_followups()
    statuses = {'new': 0, 'contacted': 0, 'negotiating': 0, 'closed': 0, 'lost': 0}
    for f in all_followups:
        s = f.get('status', 'new')
        if s in statuses:
            statuses[s] += 1

    # Status cards
    status_config = [
        ('🆕', t('crm.new', 'New'), statuses['new'], '#3498db'),
        ('📞', t('crm.contacted', 'Contacted'), statuses['contacted'], '#f39c12'),
        ('🤝', t('crm.negotiating', 'Negotiating'), statuses['negotiating'], '#9b59b6'),
        ('✅', t('crm.closed', 'Closed'), statuses['closed'], '#27ae60'),
        ('❌', t('crm.lost', 'Lost'), statuses['lost'], '#e74c3c'),
    ]
    cols = st.columns(5)
    for i, (icon, label, count, color) in enumerate(status_config):
        with cols[i]:
            st.markdown(f"""
            <div style="background: #16213e; padding: 12px; border-radius: 10px; text-align: center; border-top: 3px solid {color};">
                <div style="font-size: 1.3em;">{icon}</div>
                <div style="color: {color}; font-size: 1.6em; font-weight: bold;">{count}</div>
                <div style="color: #a0a0c0; font-size: 0.8em;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Add New Customer
    with st.expander(f"➕ {t('crm.add_customer', 'Add New Customer')}", expanded=False):
        with st.form("crm_new_customer"):
            nc1, nc2 = st.columns(2)
            with nc1:
                c_name = st.text_input(f"👤 {t('crm.customer_name', 'Customer Name')}*")
                c_phone = st.text_input(f"📞 {t('crm.phone', 'Phone')}")
                c_email = st.text_input(f"📧 {t('crm.email', 'Email')}")
            with nc2:
                c_interest = st.text_input(f"🚗 {t('crm.car_interest', 'Car Interest')}", placeholder="e.g. BMW X5 2024")
                c_followup = st.date_input(f"📅 {t('crm.next_followup', 'Next Follow-up Date')}", value=date.today())
                c_notes = st.text_area(f"📝 {t('crm.notes', 'Notes')}", height=80)

            # Employee assignment
            employees = db.get_all_employees()
            emp_options = {0: f"— {t('crm.unassigned', 'Unassigned')} —"}
            for e in employees:
                emp_options[e['id']] = f"{e['first_name']} {e.get('last_name', '')}"
            c_emp = st.selectbox(f"👨‍💼 {t('crm.assign_employee', 'Assign Employee')}", options=list(emp_options.keys()), format_func=lambda x: emp_options[x])

            if st.form_submit_button(f"✅ {t('crm.add', 'Add Customer')}", type="primary", use_container_width=True):
                if c_name:
                    db.create_followup(
                        customer_name=c_name, phone=c_phone, email=c_email,
                        car_interest=c_interest, notes=c_notes,
                        next_followup_date=str(c_followup),
                        assigned_employee_id=c_emp if c_emp else None
                    )
                    st.success(f"✅ {t('crm.added', 'Customer added!')}")
                    st.rerun()
                else:
                    st.warning(t('crm.name_required', 'Customer name is required'))

    st.markdown("---")

    # Filter
    filter_col1, filter_col2 = st.columns([2, 3])
    with filter_col1:
        status_filter = st.selectbox(
            f"🔍 {t('crm.filter_status', 'Filter by Status')}",
            ['all', 'new', 'contacted', 'negotiating', 'closed', 'lost'],
            format_func=lambda x: t(f'crm.{x}', x.title()) if x != 'all' else t('crm.all', 'All')
        )

    # Customer List
    followups = db.get_all_followups(status_filter if status_filter != 'all' else None)

    st.subheader(f"📋 {t('crm.customer_list', 'Customer List')} ({len(followups)})")

    if followups:
        for fu in followups:
            status = fu.get('status', 'new')
            status_colors = {'new': '#3498db', 'contacted': '#f39c12', 'negotiating': '#9b59b6', 'closed': '#27ae60', 'lost': '#e74c3c'}
            status_icons = {'new': '🆕', 'contacted': '📞', 'negotiating': '🤝', 'closed': '✅', 'lost': '❌'}
            color = status_colors.get(status, '#a0a0c0')
            icon = status_icons.get(status, '❔')

            is_overdue = False
            if fu.get('next_followup_date') and status not in ('closed', 'lost'):
                try:
                    fu_date = datetime.strptime(fu['next_followup_date'], '%Y-%m-%d').date()
                    is_overdue = fu_date <= date.today()
                except (ValueError, TypeError):
                    pass

            overdue_badge = '<span style="background:#e74c3c; color:white; padding:2px 6px; border-radius:8px; font-size:0.7em; margin-left:8px;">⚠️ OVERDUE</span>' if is_overdue else ''

            st.markdown(f"""
            <div style="background: #16213e; padding: 14px 18px; border-radius: 12px; margin: 8px 0; border-left: 4px solid {color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="background: {color}22; color: {color}; padding: 2px 10px; border-radius: 12px; font-size: 0.8em;">{icon} {status.upper()}</span>
                        <span style="color: white; font-weight: bold; margin-left: 10px; font-size: 1.1em;">{fu['customer_name']}</span>
                        {overdue_badge}
                    </div>
                    <div style="text-align: right;">
                        <span style="color: #a0a0c0;">📅 {fu.get('next_followup_date', '-')}</span>
                    </div>
                </div>
                <div style="margin-top: 6px; color: #a0a0c0; font-size: 0.9em;">
                    {'📞 ' + fu['phone'] + ' &nbsp;|&nbsp; ' if fu.get('phone') else ''}
                    {'📧 ' + fu['email'] + ' &nbsp;|&nbsp; ' if fu.get('email') else ''}
                    {'🚗 ' + fu['car_interest'] if fu.get('car_interest') else ''}
                </div>
                {'<div style="margin-top: 4px; color: #e0e0e0; font-size: 0.85em;">📝 ' + fu["notes"][:150] + '</div>' if fu.get('notes') else ''}
                {'<div style="margin-top: 4px; color: #D4AF37; font-size: 0.85em;">👨‍💼 ' + fu.get("employee_name", "") + '</div>' if fu.get('employee_name') and fu['employee_name'].strip() else ''}
            </div>
            """, unsafe_allow_html=True)

            # Action buttons
            ac1, ac2, ac3, ac4, ac5 = st.columns(5)
            with ac1:
                if status != 'contacted' and status not in ('closed', 'lost'):
                    if st.button(f"📞 {t('crm.mark_contacted', 'Contacted')}", key=f"crm_contact_{fu['id']}"):
                        db.update_followup(fu['id'], status='contacted')
                        st.rerun()
            with ac2:
                if status not in ('negotiating', 'closed', 'lost'):
                    if st.button(f"🤝 {t('crm.mark_negotiating', 'Negotiating')}", key=f"crm_nego_{fu['id']}"):
                        db.update_followup(fu['id'], status='negotiating')
                        st.rerun()
            with ac3:
                if status != 'closed':
                    if st.button(f"✅ {t('crm.mark_closed', 'Closed')}", key=f"crm_close_{fu['id']}"):
                        db.update_followup(fu['id'], status='closed')
                        st.rerun()
            with ac4:
                if status != 'lost':
                    if st.button(f"❌ {t('crm.mark_lost', 'Lost')}", key=f"crm_lost_{fu['id']}"):
                        db.update_followup(fu['id'], status='lost')
                        st.rerun()
            with ac5:
                if st.button(f"🗑️ {t('crm.delete', 'Delete')}", key=f"crm_del_{fu['id']}"):
                    db.delete_followup(fu['id'])
                    st.rerun()

            # Edit expander
            with st.expander(f"✏️ {t('crm.edit', 'Edit')} — {fu['customer_name']}", expanded=False):
                with st.form(f"crm_edit_{fu['id']}"):
                    e1, e2 = st.columns(2)
                    with e1:
                        ed_name = st.text_input(t('crm.customer_name', 'Name'), value=fu.get('customer_name', ''), key=f"ename_{fu['id']}")
                        ed_phone = st.text_input(t('crm.phone', 'Phone'), value=fu.get('phone', '') or '', key=f"ephone_{fu['id']}")
                        ed_email = st.text_input(t('crm.email', 'Email'), value=fu.get('email', '') or '', key=f"eemail_{fu['id']}")
                    with e2:
                        ed_interest = st.text_input(t('crm.car_interest', 'Interest'), value=fu.get('car_interest', '') or '', key=f"eint_{fu['id']}")
                        try:
                            default_date = datetime.strptime(fu.get('next_followup_date', ''), '%Y-%m-%d').date() if fu.get('next_followup_date') else date.today()
                        except (ValueError, TypeError):
                            default_date = date.today()
                        ed_date = st.date_input(t('crm.next_followup', 'Follow-up'), value=default_date, key=f"edate_{fu['id']}")
                        ed_notes = st.text_area(t('crm.notes', 'Notes'), value=fu.get('notes', '') or '', key=f"enotes_{fu['id']}", height=60)

                    if st.form_submit_button(f"💾 {t('crm.save', 'Save')}", type="primary", use_container_width=True):
                        db.update_followup(fu['id'],
                            customer_name=ed_name, phone=ed_phone, email=ed_email,
                            car_interest=ed_interest, next_followup_date=str(ed_date), notes=ed_notes
                        )
                        st.success(f"✅ {t('crm.updated', 'Updated!')}")
                        st.rerun()
    else:
        st.info(t('crm.no_customers', 'No customers found. Add your first customer above!'))
