"""
utils/excel_export.py - Excel Data Export
SmartCar AI-Dealer
"""
import io, sqlite3
from config import Config


class ExcelExporter:
    """Export all data as Excel files"""

    @staticmethod
    def export_all_data() -> bytes:
        import pandas as pd
        conn = sqlite3.connect(Config.DATABASE_PATH)
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Transactions
            try:
                df = pd.read_sql_query("SELECT * FROM transactions ORDER BY created_at DESC", conn)
                df.to_excel(writer, sheet_name='Transactions', index=False)
            except: pass
            
            # Users
            try:
                df = pd.read_sql_query("SELECT id, username, full_name, email, phone, role, created_at FROM users", conn)
                df.to_excel(writer, sheet_name='Users', index=False)
            except: pass
            
            # Contracts
            try:
                df = pd.read_sql_query("SELECT * FROM contracts ORDER BY created_at DESC", conn)
                df.to_excel(writer, sheet_name='Contracts', index=False)
            except: pass
            
            # Employees
            try:
                df = pd.read_sql_query("SELECT * FROM employees", conn)
                df.to_excel(writer, sheet_name='Employees', index=False)
            except: pass
            
            # Appointments
            try:
                df = pd.read_sql_query("SELECT * FROM appointments ORDER BY preferred_date DESC", conn)
                df.to_excel(writer, sheet_name='Appointments', index=False)
            except: pass
            
            # Audit Log
            try:
                df = pd.read_sql_query("SELECT * FROM audit_log ORDER BY created_at DESC LIMIT 1000", conn)
                df.to_excel(writer, sheet_name='Audit Log', index=False)
            except: pass
        
        conn.close()
        return output.getvalue()
