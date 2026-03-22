"""
📱 لوحة تحكم الموظف - Employee Dashboard Page
SmartCar AI-Dealer
"""

import streamlit as st
import sqlite3
from config import Config
from db_manager import DatabaseManager
from utils.i18n import t
from components.html_components import render_universal_header


def employee_dashboard_page():
    """صفحة لوحة تحكم الموظف الشخصية"""
    render_universal_header(t('emp_dash.title', 'My Dashboard'), f"📱 {t('emp_dash.subtitle', 'Personal Performance')}")

    db = DatabaseManager()
    user = st.session_state.get('user', {})
    user_id = user.get('id')

    # Try to find employee record
    employee = db.get_employee_by_user_id(user_id) if user_id else None
    employee_id = employee['id'] if employee else None
    emp_name = f"{employee['first_name']} {employee.get('last_name', '')}" if employee else user.get('full_name', user.get('username', ''))

    conn = sqlite3.connect(Config.DATABASE_PATH)

    # Personal stats
    if employee_id:
        total = conn.execute("SELECT COUNT(*) FROM transactions WHERE employee_id=?", (employee_id,)).fetchone()[0]
        revenue = conn.execute("SELECT COALESCE(SUM(estimated_price),0) FROM transactions WHERE employee_id=?", (employee_id,)).fetchone()[0]
        avg_price = conn.execute("SELECT COALESCE(AVG(estimated_price),0) FROM transactions WHERE employee_id=?", (employee_id,)).fetchone()[0]
        this_month = conn.execute("SELECT COUNT(*) FROM transactions WHERE employee_id=? AND created_at >= date('now','start of month')", (employee_id,)).fetchone()[0]
        this_month_rev = conn.execute("SELECT COALESCE(SUM(estimated_price),0) FROM transactions WHERE employee_id=? AND created_at >= date('now','start of month')", (employee_id,)).fetchone()[0]
    else:
        total = conn.execute("SELECT COUNT(*) FROM transactions WHERE user_id=?", (user_id,)).fetchone()[0]
        revenue = conn.execute("SELECT COALESCE(SUM(estimated_price),0) FROM transactions WHERE user_id=?", (user_id,)).fetchone()[0]
        avg_price = conn.execute("SELECT COALESCE(AVG(estimated_price),0) FROM transactions WHERE user_id=?", (user_id,)).fetchone()[0]
        this_month = conn.execute("SELECT COUNT(*) FROM transactions WHERE user_id=? AND created_at >= date('now','start of month')", (user_id,)).fetchone()[0]
        this_month_rev = conn.execute("SELECT COALESCE(SUM(estimated_price),0) FROM transactions WHERE user_id=? AND created_at >= date('now','start of month')", (user_id,)).fetchone()[0]

    # Commission
    commission_rate = 0.03
    total_commission = revenue * commission_rate
    month_commission = this_month_rev * commission_rate

    # Rank
    all_emps = conn.execute("""
        SELECT employee_id, COUNT(*) as cnt FROM transactions 
        WHERE employee_id IS NOT NULL GROUP BY employee_id ORDER BY cnt DESC
    """).fetchall()
    rank = '-'
    for i, row in enumerate(all_emps, 1):
        if row[0] == employee_id:
            rank = f"#{i}"
            break

    # Header with name
    st.markdown(f"""
    <div style="text-align: center; padding: 15px 0;">
        <h2 style="color: #D4AF37; margin-bottom: 5px;">👤 {emp_name}</h2>
        <span style="color: #a0a0c0; font-size: 0.9em;">{employee.get('job_title', t('emp_dash.employee', 'Employee')) if employee else t('emp_dash.user', 'User')}</span>
        <span style="background: #D4AF3722; color: #D4AF37; padding: 4px 12px; border-radius: 20px; margin-left: 10px; font-size: 0.9em;">🏆 {rank}</span>
    </div>
    """, unsafe_allow_html=True)

    # 6 Metric Cards
    metrics = [
        ('🛒', t('emp_dash.total_sales', 'Total Sales'), str(total), '#D4AF37'),
        ('💰', t('emp_dash.revenue', 'Revenue'), f"€{revenue:,.0f}", '#4CAF50'),
        ('📊', t('emp_dash.avg_price', 'Avg Price'), f"€{avg_price:,.0f}", '#3498db'),
        ('📅', t('emp_dash.this_month', 'This Month'), str(this_month), '#9b59b6'),
        ('💵', t('emp_dash.commission', 'Commission'), f"€{total_commission:,.0f}", '#e67e22'),
        ('🏆', t('emp_dash.rank', 'Rank'), rank, '#D4AF37'),
    ]

    cols = st.columns(6)
    for i, (icon, label, value, color) in enumerate(metrics):
        with cols[i]:
            st.markdown(f"""
            <div style="background: #16213e; padding: 14px; border-radius: 12px; text-align: center; border-top: 3px solid {color};">
                <div style="font-size: 1.4em;">{icon}</div>
                <div style="color: {color}; font-size: 1.3em; font-weight: bold;">{value}</div>
                <div style="color: #a0a0c0; font-size: 0.75em;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Monthly Target Progress
    target_sales = st.sidebar.number_input(t('emp_dash.monthly_target', 'Monthly Target'), value=10, min_value=1, key="emp_target")
    pct = min((this_month / max(target_sales, 1)) * 100, 100)
    bar_color = '#27ae60' if pct >= 80 else '#f39c12' if pct >= 50 else '#e74c3c'

    st.subheader(f"🎯 {t('emp_dash.target_progress', 'Monthly Target Progress')}")
    st.markdown(f"""
    <div style="background: #16213e; padding: 18px; border-radius: 12px; margin-bottom: 15px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: white; font-weight: bold;">{this_month} / {target_sales} {t('emp_dash.sales_label', 'sales')}</span>
            <span style="color: {bar_color}; font-weight: bold;">{pct:.0f}%</span>
        </div>
        <div style="background: #1a1a2e; border-radius: 10px; height: 12px;">
            <div style="background: {bar_color}; width: {pct:.0f}%; height: 12px; border-radius: 10px; transition: width 0.5s;"></div>
        </div>
        <div style="text-align: center; margin-top: 8px; color: #a0a0c0; font-size: 0.9em;">
            💵 {t('emp_dash.month_commission', 'This Month Commission')}: <span style="color: #4CAF50; font-weight: bold;">€{month_commission:,.0f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    dash_col1, dash_col2 = st.columns(2)

    with dash_col1:
        # Monthly sales trend (last 6 months)
        st.subheader(f"📈 {t('emp_dash.monthly_trend', 'Monthly Trend')}")
        try:
            import plotly.graph_objects as go

            if employee_id:
                months_data = conn.execute("""
                    SELECT strftime('%Y-%m', created_at) as month, COUNT(*) as cnt, 
                           COALESCE(SUM(estimated_price), 0) as rev
                    FROM transactions WHERE employee_id=?
                    GROUP BY month ORDER BY month DESC LIMIT 6
                """, (employee_id,)).fetchall()
            else:
                months_data = conn.execute("""
                    SELECT strftime('%Y-%m', created_at) as month, COUNT(*) as cnt,
                           COALESCE(SUM(estimated_price), 0) as rev
                    FROM transactions WHERE user_id=?
                    GROUP BY month ORDER BY month DESC LIMIT 6
                """, (user_id,)).fetchall()

            if months_data:
                months_data = list(reversed(months_data))
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=[r[0] for r in months_data],
                    y=[r[1] for r in months_data],
                    name=t('emp_dash.sales_label', 'Sales'),
                    marker_color='#D4AF37'
                ))
                fig.add_trace(go.Scatter(
                    x=[r[0] for r in months_data],
                    y=[r[2] for r in months_data],
                    name=t('emp_dash.revenue', 'Revenue'),
                    yaxis='y2',
                    line=dict(color='#4CAF50', width=3),
                    mode='lines+markers'
                ))
                fig.update_layout(
                    template='plotly_dark',
                    yaxis2=dict(title=t('emp_dash.revenue', '€'), overlaying='y', side='right'),
                    legend=dict(orientation='h', y=1.12)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(t('emp_dash.no_data', 'No sales data yet'))
        except Exception:
            st.info(t('emp_dash.no_data', 'No sales data yet'))

    with dash_col2:
        # Leaderboard
        st.subheader(f"🏅 {t('emp_dash.leaderboard', 'Team Leaderboard')}")
        top_emps = conn.execute("""
            SELECT e.first_name || ' ' || COALESCE(e.last_name, '') as name,
                   COUNT(t.id) as sales,
                   COALESCE(SUM(t.estimated_price), 0) as revenue
            FROM employees e
            LEFT JOIN transactions t ON t.employee_id = e.id
            WHERE e.is_active = 1
            GROUP BY e.id
            ORDER BY sales DESC
            LIMIT 5
        """).fetchall()

        if top_emps and any(r[1] > 0 for r in top_emps):
            for i, row in enumerate(top_emps, 1):
                medal = '🥇' if i == 1 else '🥈' if i == 2 else '🥉' if i == 3 else f'#{i}'
                is_me = employee and row[0].strip() == emp_name.strip()
                bg = '#1a3a2e' if is_me else '#16213e'
                border = 'border: 1px solid #D4AF37;' if is_me else ''
                st.markdown(f"""
                <div style="background: {bg}; padding: 10px 14px; border-radius: 10px; margin: 4px 0; display: flex; justify-content: space-between; align-items: center; {border}">
                    <span style="color: white;">{medal} {row[0]} {'⭐' if is_me else ''}</span>
                    <span>
                        <span style="color: #D4AF37; font-weight: bold;">{row[1]} {t('emp_dash.sales_label', 'sales')}</span>
                        <span style="color: #4CAF50; margin-left: 10px;">€{row[2]:,.0f}</span>
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(t('emp_dash.no_leaderboard', 'No employee sales data yet'))

    st.markdown("---")

    # Recent Sales
    st.subheader(f"🕐 {t('emp_dash.recent_sales', 'Recent Sales')}")
    if employee_id:
        recent = conn.execute("""
            SELECT brand, model, manufacture_year, estimated_price, created_at 
            FROM transactions WHERE employee_id=? ORDER BY created_at DESC LIMIT 10
        """, (employee_id,)).fetchall()
    else:
        recent = conn.execute("""
            SELECT brand, model, manufacture_year, estimated_price, created_at 
            FROM transactions WHERE user_id=? ORDER BY created_at DESC LIMIT 10
        """, (user_id,)).fetchall()

    if recent:
        for r in recent:
            st.markdown(f"""
            <div style="background: #16213e; padding: 8px 14px; border-radius: 8px; margin: 4px 0; display: flex; justify-content: space-between; align-items: center;">
                <span style="color: white;">🏎️ {r[0] or '-'} {r[1] or '-'} ({r[2] or '-'})</span>
                <span>
                    <span style="color: #4CAF50; font-weight: bold;">€{(r[3] or 0):,.0f}</span>
                    <span style="color: #a0a0c0; font-size: 0.8em; margin-left: 10px;">{(r[4] or '')[:10]}</span>
                </span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info(t('emp_dash.no_sales', 'No sales yet'))

    conn.close()
