"""
pages_app/tasks_page.py - Employee Task Management
SmartCar AI-Dealer - إدارة المهام
"""
import streamlit as st
import sqlite3
from datetime import datetime
from config import Config
from utils.i18n import t


def _ensure_table():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            assigned_to INTEGER,
            assigned_name TEXT,
            created_by INTEGER,
            priority TEXT DEFAULT 'normal',
            status TEXT DEFAULT 'pending',
            due_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (assigned_to) REFERENCES users(id)
        )
    """)
    conn.commit(); conn.close()


def tasks_page():
    """Employee task management page"""
    _ensure_table()
    user = st.session_state.get('user', {})
    is_admin = user.get('role') == 'admin'
    
    st.markdown(f"""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #D4AF37;">📋 {t('tasks.title', 'Task Management')}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    
    if is_admin:
        pending = conn.execute("SELECT COUNT(*) as c FROM tasks WHERE status='pending'").fetchone()['c']
        progress = conn.execute("SELECT COUNT(*) as c FROM tasks WHERE status='in_progress'").fetchone()['c']
        done = conn.execute("SELECT COUNT(*) as c FROM tasks WHERE status='completed'").fetchone()['c']
    else:
        pending = conn.execute("SELECT COUNT(*) as c FROM tasks WHERE assigned_to=? AND status='pending'", (user['id'],)).fetchone()['c']
        progress = conn.execute("SELECT COUNT(*) as c FROM tasks WHERE assigned_to=? AND status='in_progress'", (user['id'],)).fetchone()['c']
        done = conn.execute("SELECT COUNT(*) as c FROM tasks WHERE assigned_to=? AND status='completed'", (user['id'],)).fetchone()['c']
    
    s1, s2, s3 = st.columns(3)
    s1.metric(f"⏳ {t('tasks.pending', 'Pending')}", pending)
    s2.metric(f"🔄 {t('tasks.in_progress', 'In Progress')}", progress)
    s3.metric(f"✅ {t('tasks.completed', 'Completed')}", done)
    
    st.markdown("---")
    
    # Create task (admin only)
    if is_admin:
        with st.expander(f"➕ {t('tasks.create', 'Create Task')}", expanded=False):
            with st.form("task_create_form"):
                tc1, tc2 = st.columns(2)
                with tc1:
                    title = st.text_input(t('tasks.task_title', 'Title'), key="task_title")
                    priority = st.selectbox(t('tasks.priority', 'Priority'), ['normal', 'high', 'urgent'], key="task_priority")
                with tc2:
                    due_date = st.date_input(t('tasks.due_date', 'Due Date'), key="task_due")
                    # Get employees for assignment
                    try:
                        from db_manager import DatabaseManager
                        db = DatabaseManager()
                        employees = db.get_all_employees() if hasattr(db, 'get_all_employees') else []
                        emp_names = ['Unassigned'] + [f"{e.get('first_name','')} {e.get('last_name','')}" for e in employees]
                        assigned = st.selectbox(t('tasks.assign', 'Assign to'), emp_names, key="task_assign")
                    except:
                        assigned = st.text_input(t('tasks.assign', 'Assign to'), key="task_assign")
                
                description = st.text_area(t('tasks.description', 'Description'), key="task_desc")
                
                if st.form_submit_button(f"✅ {t('tasks.create', 'Create')}", use_container_width=True, type="primary"):
                    if title:
                        conn2 = sqlite3.connect(Config.DATABASE_PATH)
                        conn2.execute("INSERT INTO tasks (title, description, assigned_name, created_by, priority, due_date) VALUES (?,?,?,?,?,?)",
                                     (title, description, assigned if assigned != 'Unassigned' else None, user['id'], priority, str(due_date)))
                        conn2.commit(); conn2.close()
                        st.success(f"✅ {t('tasks.created', 'Task created!')}")
                        st.rerun()
    
    # Task list
    status_filter = st.selectbox(t('tasks.filter', 'Filter'), ['all', 'pending', 'in_progress', 'completed'], key="tasks_filter")
    
    q = "SELECT * FROM tasks"
    params = []
    if not is_admin:
        q += " WHERE assigned_to=?"
        params.append(user['id'])
        if status_filter != 'all':
            q += " AND status=?"
            params.append(status_filter)
    elif status_filter != 'all':
        q += " WHERE status=?"
        params.append(status_filter)
    q += " ORDER BY CASE priority WHEN 'urgent' THEN 1 WHEN 'high' THEN 2 ELSE 3 END, created_at DESC"
    
    tasks = conn.execute(q, params).fetchall()
    conn.close()
    
    priority_colors = {'normal': '#3498db', 'high': '#f39c12', 'urgent': '#e74c3c'}
    status_icons = {'pending': '⏳', 'in_progress': '🔄', 'completed': '✅'}
    
    for task in tasks:
        color = priority_colors.get(task['priority'], '#3498db')
        icon = status_icons.get(task['status'], '⏳')
        due = task['due_date'] or ''
        
        with st.expander(f"{icon} {task['title']} {'🔴' if task['priority']=='urgent' else '🟡' if task['priority']=='high' else ''}"):
            st.write(f"**{t('tasks.description', 'Description')}:** {task['description'] or '-'}")
            st.write(f"**{t('tasks.assign', 'Assigned to')}:** {task['assigned_name'] or '-'}")
            st.write(f"**📅 Due:** {due}")
            
            if task['status'] != 'completed':
                bc1, bc2 = st.columns(2)
                with bc1:
                    if task['status'] == 'pending':
                        if st.button(f"🔄 Start", key=f"start_{task['id']}"):
                            conn2 = sqlite3.connect(Config.DATABASE_PATH)
                            conn2.execute("UPDATE tasks SET status='in_progress' WHERE id=?", (task['id'],))
                            conn2.commit(); conn2.close(); st.rerun()
                with bc2:
                    if st.button(f"✅ Complete", key=f"done_{task['id']}"):
                        conn2 = sqlite3.connect(Config.DATABASE_PATH)
                        conn2.execute("UPDATE tasks SET status='completed' WHERE id=?", (task['id'],))
                        conn2.commit(); conn2.close(); st.rerun()
