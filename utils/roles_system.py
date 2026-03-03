"""
utils/roles_system.py - Role-Based Access Control
SmartCar AI-Dealer - نظام الصلاحيات
"""
import sqlite3
from config import Config


class RolesSystem:
    """Custom roles with granular permissions"""

    ROLES = {
        'admin': {
            'label': '👑 Admin',
            'permissions': ['all'],
            'description': 'Full access to everything'
        },
        'manager': {
            'label': '📊 Manager',
            'permissions': ['view_dashboard', 'manage_employees', 'manage_inventory', 'view_reports',
                           'manage_transactions', 'export_data', 'manage_appointments', 'view_audit'],
            'description': 'Can manage employees, inventory, and view reports'
        },
        'accountant': {
            'label': '🧮 Accountant',
            'permissions': ['view_dashboard', 'view_reports', 'manage_invoices', 'export_data',
                           'datev_export', 'manage_payments'],
            'description': 'Financial access, invoices, DATEV export'
        },
        'sales': {
            'label': '🛒 Sales',
            'permissions': ['create_transaction', 'manage_inventory', 'view_showcase',
                           'manage_appointments', 'send_messages', 'view_own_stats'],
            'description': 'Create transactions, manage cars, handle appointments'
        },
        'viewer': {
            'label': '👁️ Viewer',
            'permissions': ['view_dashboard', 'view_showcase', 'view_reports'],
            'description': 'Read-only access to reports and showcase'
        }
    }

    @staticmethod
    def get_role_info(role: str) -> dict:
        return RolesSystem.ROLES.get(role, RolesSystem.ROLES['viewer'])

    @staticmethod
    def has_permission(role: str, permission: str) -> bool:
        role_info = RolesSystem.get_role_info(role)
        if 'all' in role_info['permissions']:
            return True
        return permission in role_info['permissions']

    @staticmethod
    def get_all_roles() -> list:
        return [(k, v['label'], v['description']) for k, v in RolesSystem.ROLES.items()]

    @staticmethod
    def check_access(required_permission: str) -> bool:
        """Check if current user has required permission"""
        import streamlit as st
        user = st.session_state.get('user', {})
        role = user.get('role', 'viewer')
        return RolesSystem.has_permission(role, required_permission)

    @staticmethod
    def require_permission(permission: str):
        """Decorator-style check - shows error if no permission"""
        import streamlit as st
        if not RolesSystem.check_access(permission):
            st.error(f"🔒 Access Denied: You need '{permission}' permission")
            st.stop()

    @staticmethod
    def update_user_role(user_id: int, new_role: str):
        if new_role not in RolesSystem.ROLES:
            raise ValueError(f"Invalid role: {new_role}")
        conn = sqlite3.connect(Config.DB_PATH)
        conn.execute("UPDATE users SET role=? WHERE id=?", (new_role, user_id))
        conn.commit(); conn.close()

    @staticmethod
    def render_role_badge(role: str) -> str:
        info = RolesSystem.get_role_info(role)
        colors = {'admin': '#D4AF37', 'manager': '#3498db', 'accountant': '#27ae60', 'sales': '#9b59b6', 'viewer': '#7f8c8d'}
        color = colors.get(role, '#7f8c8d')
        return f'<span style="background:{color}22; color:{color}; padding:2px 8px; border-radius:12px; font-size:0.8em;">{info["label"]}</span>'
