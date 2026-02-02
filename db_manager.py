"""
db_manager.py - المحرك المتقدم لإدارة قاعدة البيانات والنظام المالي
SmartCar AI-Dealer
إدارة المستخدمين، المعاملات، الموظفين (HR)، والإعدادات العامة
"""

import sqlite3
import threading
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Set
from contextlib import contextmanager

from config import Config

class DatabaseManager:
    """مدير قاعدة البيانات SQLite الاحترافي بنمط Singleton لضمان استقرار الاتصال"""
    _instance = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_path: Optional[Path] = None):
        if DatabaseManager._initialized: return
        with DatabaseManager._lock:
            if not DatabaseManager._initialized:
                self.db_path = db_path or Config.DATABASE_PATH
                self.logger = Config.logger
                self._init_database()
                DatabaseManager._initialized = True

    @contextmanager
    def get_connection(self):
        """توفير اتصال آمن مع دعم نمط WAL لسرعة المعالجة المتزامنة"""
        conn = None
        try:
            conn = sqlite3.connect(str(self.db_path), timeout=30)
            conn.row_factory = sqlite3.Row
            # تفعيل العلاقات المنطقية ونمط الكتابة السريع
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("PRAGMA journal_mode = WAL")
            yield conn
            conn.commit()
        except Exception as e:
            if conn: conn.rollback()
            raise e
        finally:
            if conn: conn.close()

    def _init_database(self):
        """تأسيس الجداول الأربعة الرئيسية للنظام (الأمن، العمليات، HR، الإعدادات)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. جدول المستخدمين (الأمن والمصادقة)
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL, 
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL, 
                full_name TEXT,
                phone TEXT,
                role TEXT DEFAULT 'user',
                is_active INTEGER DEFAULT 1, 
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP, 
                failed_attempts INTEGER DEFAULT 0, 
                locked_until TIMESTAMP,
                id_number TEXT,
                nationality TEXT,
                birth_date TEXT,
                expiry_date TEXT,
                license_number TEXT,
                license_type TEXT,
                license_expiry TEXT,
                issue_date TEXT
            )''')
            
            # إضافة الأعمدة الجديدة للتوافق مع قواعد البيانات القديمة
            new_columns = [
                ('phone', 'TEXT'), ('id_number', 'TEXT'), ('nationality', 'TEXT'),
                ('birth_date', 'TEXT'), ('expiry_date', 'TEXT'), ('license_number', 'TEXT'),
                ('license_type', 'TEXT'), ('license_expiry', 'TEXT'), ('issue_date', 'TEXT'),
                ('date_of_birth', 'TEXT'), ('gender', 'TEXT'), ('address', 'TEXT'),
                ('license_class', 'TEXT'), ('blood_type', 'TEXT'), ('preferred_language', 'TEXT'),
                # حقول العنوان المنفصلة
                ('street_name', 'TEXT'), ('building_number', 'TEXT'), 
                ('postal_code', 'TEXT'), ('city', 'TEXT')
            ]
            for col_name, col_type in new_columns:
                try:
                    cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
                except sqlite3.OperationalError:
                    pass  # العمود موجود مسبقاً


            # 2. جدول المعاملات (تقييم السيارات)
            cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                user_id INTEGER NOT NULL,
                car_type TEXT, brand TEXT, model TEXT, 
                manufacture_year INTEGER, 
                mileage INTEGER, 
                estimated_price REAL NOT NULL, 
                condition_analysis TEXT,
                image_path TEXT, 
                invoice_path TEXT, 
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )''')
            
            # إضافة أعمدة جديدة لجدول المعاملات (نوع الوقود، الحالة، اللون)
            trans_new_columns = [
                ('fuel_type', 'TEXT'),
                ('condition', 'TEXT'),
                ('color', 'TEXT')
            ]
            for col_name, col_type in trans_new_columns:
                try:
                    cursor.execute(f"ALTER TABLE transactions ADD COLUMN {col_name} {col_type}")
                except sqlite3.OperationalError:
                    pass  # العمود موجود مسبقاً

            # 3. جدول الموظفين (النظام المالي - HR)
            cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                first_name TEXT NOT NULL,
                last_name TEXT,
                phone TEXT,
                email TEXT,
                address TEXT,
                monthly_salary REAL DEFAULT 0, 
                hire_date DATE, 
                is_active INTEGER DEFAULT 1,
                urlaubsgeld REAL DEFAULT 0, 
                feiertags_geld REAL DEFAULT 0,
                annual_leave INTEGER DEFAULT 30,
                sick_leave INTEGER DEFAULT 0,
                unpaid_leave INTEGER DEFAULT 0,
                notes TEXT
            )''')
            
            # إضافة الأعمدة الجديدة لجدول الموظفين للتوافق مع قواعد البيانات القديمة
            emp_new_columns = [
                ('last_name', 'TEXT'), ('phone', 'TEXT'), ('email', 'TEXT'),
                ('address', 'TEXT'), ('annual_leave', 'INTEGER DEFAULT 30'),
                ('sick_leave', 'INTEGER DEFAULT 0'), ('unpaid_leave', 'INTEGER DEFAULT 0'),
                ('special_leave', 'INTEGER DEFAULT 0'),
                ('job_title', 'TEXT'), ('user_id', 'INTEGER'),
                ('notes', 'TEXT')
            ]
            for col_name, col_type in emp_new_columns:
                try:
                    cursor.execute(f"ALTER TABLE employees ADD COLUMN {col_name} {col_type}")
                except sqlite3.OperationalError:
                    pass  # العمود موجود مسبقاً

            # 3.5 جدول سجلات الإجازات المرضية (Sick Leave Records)
            cursor.execute('''CREATE TABLE IF NOT EXISTS sick_leave_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                user_id INTEGER,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                days_count INTEGER NOT NULL,
                reason TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )''')

            # 4. جدول الإعدادات العامة
            cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY, 
                value TEXT
            )''')
            
            # 5. جدول العقود (نظام التقسيط المتقدم)
            cursor.execute('''CREATE TABLE IF NOT EXISTS contracts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                transaction_id INTEGER,
                total_price REAL NOT NULL,
                down_payment REAL DEFAULT 0,
                remaining_amount REAL NOT NULL,
                installment_count INTEGER NOT NULL,
                monthly_installment REAL NOT NULL,
                interest_rate REAL DEFAULT 0,
                late_fee_type TEXT DEFAULT 'fixed',
                late_fee_amount REAL DEFAULT 50,
                grace_period_days INTEGER DEFAULT 3,
                payment_due_day INTEGER DEFAULT 1,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                closed_at TIMESTAMP,
                vehicle_vin TEXT,
                vehicle_type TEXT,
                vehicle_model TEXT,
                vehicle_plate TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (transaction_id) REFERENCES transactions(id)
            )''')
            
            # 6. جدول الفواتير/الأقساط (Payment Schedule)
            cursor.execute('''CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number TEXT UNIQUE NOT NULL,
                contract_id INTEGER NOT NULL,
                installment_number INTEGER NOT NULL,
                amount_due REAL NOT NULL,
                amount_paid REAL DEFAULT 0,
                late_fee REAL DEFAULT 0,
                due_date DATE NOT NULL,
                payment_date DATE,
                status TEXT DEFAULT 'pending',
                qr_hash TEXT,
                previous_qr_hash TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (contract_id) REFERENCES contracts(id)
            )''')
            
            # 7. جدول الدفعات (Payment Records)
            cursor.execute('''CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                payment_method TEXT NOT NULL,
                proof_path TEXT,
                reference_number TEXT,
                status TEXT DEFAULT 'pending',
                verified_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (contract_id) REFERENCES contracts(id)
            )''')
            
            # ترقية جدول payments إذا كان موجوداً بدون بعض الأعمدة
            try:
                cursor.execute("SELECT proof_path FROM payments LIMIT 1")
            except sqlite3.OperationalError:
                # العمود غير موجود، أضفه
                cursor.execute("ALTER TABLE payments ADD COLUMN proof_path TEXT")
                
            try:
                cursor.execute("SELECT reference_number FROM payments LIMIT 1")
            except sqlite3.OperationalError:
                cursor.execute("ALTER TABLE payments ADD COLUMN reference_number TEXT")
                
            try:
                cursor.execute("SELECT verified_at FROM payments LIMIT 1")
            except sqlite3.OperationalError:
                cursor.execute("ALTER TABLE payments ADD COLUMN verified_at TIMESTAMP")
            
            # ترقية جدول contracts لإضافة الأعمدة الجديدة
            contracts_new_columns = [
                ('car_details', 'TEXT'),
                ('total_amount', 'REAL'),
                ('paid_amount', 'REAL DEFAULT 0'),
                ('next_payment_date', 'DATE'),
                ('reschedule_reason', 'TEXT')
            ]
            for col_name, col_type in contracts_new_columns:
                try:
                    cursor.execute(f"ALTER TABLE contracts ADD COLUMN {col_name} {col_type}")
                except sqlite3.OperationalError:
                    pass  # العمود موجود مسبقاً


    # ===== 1. إدارة المستخدمين والأمان =====
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, username))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """جلب بيانات المستخدم بواسطة المعرف الفريد"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_all_users(self) -> List[Dict]:
        """جلب جميع المستخدمين مرتبين حسب تاريخ الإنشاء"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
            return [dict(row) for row in cursor.fetchall()]

    def update_user(self, user_id: int, **kwargs):
        """تحديث بيانات المستخدم بشكل ديناميكي"""
        if not kwargs: return
        
        allowed_fields = {
            'role', 'is_active', 'full_name', 'email', 'phone', 'locked_until', 'failed_attempts',
            # حقول الهوية
            'id_number', 'nationality', 'birth_date', 'expiry_date', 'date_of_birth', 'gender', 'address',
            # حقول رخصة القيادة
            'license_number', 'license_type', 'license_expiry', 'issue_date', 'license_class', 'blood_type',
            # اللغة المفضلة
            'preferred_language',
            # حقول العنوان المنفصلة
            'street_name', 'building_number', 'postal_code', 'city'
        }
        updates = []
        params = []
        
        for k, v in kwargs.items():
            if k in allowed_fields:
                updates.append(f"{k} = ?")
                params.append(v)
        
        if not updates: return
        
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        params.append(user_id)
        
        with self.get_connection() as conn:
            conn.execute(query, params)



    def record_login_attempt(self, username: str, success: bool):
        with self.get_connection() as conn:
            if success:
                conn.execute("UPDATE users SET failed_attempts = 0, last_login = ? WHERE username = ?", (datetime.now(), username))
            else:
                conn.execute("UPDATE users SET failed_attempts = failed_attempts + 1 WHERE username = ?", (username,))

    def log_activity(self, user_id: int, action_type: str, details: str, ip_address: str = None):
        """تسجيل نشاط إداري أو نظامي"""
        try:
            with self.get_connection() as conn:
                conn.execute('''
                    INSERT INTO activity_logs (user_id, action_type, details, ip_address)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, action_type, details, ip_address))
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to log activity: {e}") 

    # ===== 2. سجلات العمليات والإحصائيات =====

    def create_transaction(self, user_id: int, car_data: Dict, estimated_price: float, condition_analysis: Dict, car_image_bytes: bytes = None) -> int:
        """إنشاء سجل معاملة جديد وحفظ البيانات"""
        import base64
        
        # تحويل الصورة إلى base64 إذا وجدت
        image_path = None
        if car_image_bytes:
            # هنا يمكنك حفظ الصورة في ملف فعلي، لكن للتبسيط سنقوم بتخزين مسار نصي أو تجاهلها حالياً
            # في التطبيق الحقيقي، يجب حفظ الصورة في مجلد static/uploads
            # سنقوم فقط بتخزين نص يدل على وجود صورة
            image_path = "stored_in_session" 

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO transactions (
                    user_id, car_type, brand, model, manufacture_year, 
                    mileage, estimated_price, condition_analysis, image_path,
                    fuel_type, condition, color
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                car_data.get('car_type', 'Unknown'),
                car_data.get('brand', 'Unknown'),
                car_data.get('model', 'Unknown'),
                car_data.get('manufacture_year', 2020),
                car_data.get('mileage', 0),
                estimated_price,
                json.dumps(condition_analysis, ensure_ascii=False),
                image_path,
                car_data.get('fuel_type', ''),
                car_data.get('condition', ''),
                car_data.get('color', '')
            ))
            return cursor.lastrowid

    def update_transaction_invoice(self, transaction_id: int, invoice_path: str):
        """تحديث مسار الفاتورة للمعاملة"""
        with self.get_connection() as conn:
            conn.execute("UPDATE transactions SET invoice_path = ? WHERE id = ?", (str(invoice_path), transaction_id))

    def delete_transaction(self, transaction_id: int) -> bool:
        """حذف معاملة من قاعدة البيانات"""
        try:
            with self.get_connection() as conn:
                conn.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
            return True
        except Exception:
            return False

    def update_transaction(self, transaction_id: int, updates: Dict = None, **kwargs) -> bool:
        """تحديث بيانات معاملة"""
        # دمج kwargs مع updates
        if updates is None:
            updates = {}
        updates.update(kwargs)
        
        if not updates:
            return False
        
        allowed_fields = {'car_type', 'brand', 'model', 'manufacture_year', 'mileage', 'estimated_price', 'condition_analysis', 'fuel_type', 'condition', 'color'}
        update_parts = []
        params = []
        
        for key, value in updates.items():
            if key in allowed_fields:
                update_parts.append(f"{key} = ?")
                params.append(value)
        
        if not update_parts:
            return False
        
        try:
            query = f"UPDATE transactions SET {', '.join(update_parts)} WHERE id = ?"
            params.append(transaction_id)
            with self.get_connection() as conn:
                conn.execute(query, params)
            return True
        except Exception:
            return False


    def get_user_transactions(self, user_id: int, limit: Optional[int] = None) -> List[Dict]:
        """جلب العمليات التاريخية للمستخدم مع إمكانية تحديد العدد"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM transactions WHERE user_id = ? ORDER BY created_at DESC"
            params = [user_id]
            if limit:
                query += " LIMIT ?"
                params.append(limit)
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_user_contracts(self, user_id: int) -> List[Dict]:
        """جلب العقود النشطة للمستخدم (محاكاة من المعاملات)"""
        transactions = self.get_user_transactions(user_id)
        contracts = []
        for t in transactions:
            # محاكاة بيانات العقد من المعاملة
            contract = {
                'id': t['id'],
                'user_id': t['user_id'],
                'car_details': json.dumps({'brand': t.get('brand', 'Unknown'), 'model': t.get('model', 'Unknown')}),
                'total_amount': t.get('estimated_price', 0),
                'paid_amount': 0, # لم يتم تفعيل الدفع بعد
                'status': 'active',
                'created_at': t.get('created_at')
            }
            contracts.append(contract)
        return contracts

    def get_all_contracts_with_users(self) -> List[Dict]:
        """جلب جميع العقود مع بيانات المستخدمين للوحة الإدارة"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT t.*, 
                       u.full_name, u.email, u.username, u.phone,
                       u.id_number, u.nationality, u.birth_date,
                       u.license_number, u.license_type, u.license_expiry
                FROM transactions t
                JOIN users u ON t.user_id = u.id
                ORDER BY t.created_at DESC
            ''')
            contracts = []
            for row in cursor.fetchall():
                contract = dict(row)
                contract['total_amount'] = contract.get('estimated_price', 0)
                contract['plan_type'] = 'Full'
                contracts.append(contract)
            return contracts

    def get_contract_payments(self, contract_id: int) -> List[Dict]:
        """جلب سجل الدفعات لعقد معين (محاكاة - لا يوجد جدول دفعات حالياً)"""
        # حالياً نرجع قائمة فارغة لأن جدول الدفعات غير موجود
        # يمكن إنشاء جدول payments لاحقاً
        return []
    
    def delete_transaction(self, transaction_id: int) -> bool:
        """حذف معاملة من قاعدة البيانات"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
            return cursor.rowcount > 0

    def get_contract_summary(self, contract_id: int) -> Dict:
        """جلب ملخص العقد للفاتورة"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM transactions WHERE id = ?', (contract_id,))
            row = cursor.fetchone()
            if row:
                t = dict(row)
                return {
                    'car_type': t.get('car_type', 'Unknown'),
                    'brand': t.get('brand', 'Unknown'),
                    'model': t.get('model', 'Unknown'),
                    'estimated_price': t.get('estimated_price', 0),
                    'created_at': t.get('created_at')
                }
            return {}

    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        with self.get_connection() as conn:
            res = conn.execute("SELECT COUNT(*), SUM(estimated_price) FROM transactions WHERE user_id = ?", (user_id,)).fetchone()
            return {'count': res[0] or 0, 'total_val': res[1] or 0.0}

    def get_transactions_by_year(self, year: int) -> List[Dict]:
        """جلب جميع المعاملات لسنة معينة"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT t.*, u.full_name, u.username
                FROM transactions t
                LEFT JOIN users u ON t.user_id = u.id
                WHERE strftime('%Y', t.created_at) = ?
                ORDER BY t.created_at DESC
            ''', (str(year),))
            return [dict(row) for row in cursor.fetchall()]


    def get_statistics(self) -> Dict[str, Any]:
        """تجميع إحصائيات النظام الشاملة للوحة تحكم المسؤول"""
        stats = {}
        with self.get_connection() as conn:
            # إحصائيات عامة
            stats['total_users'] = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            stats['total_transactions'] = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
            stats['total_estimated_value'] = conn.execute("SELECT SUM(estimated_price) FROM transactions").fetchone()[0] or 0.0
            stats['total_invoices'] = conn.execute("SELECT COUNT(*) FROM transactions WHERE invoice_path IS NOT NULL").fetchone()[0]
            
            # إحصائيات زمنية (اليوم، الأسبوع، الشهر، السنة)
            for period, fmt in [('today', '%Y-%m-%d'), ('week', '%Y-%W'), ('month', '%Y-%m'), ('year', '%Y')]:
                current = datetime.now().strftime(fmt.replace('%', '')) # Simple approximation, better to use SQL strftime
                # Using SQL strftime for accurate periods
                if period == 'today':
                    val = conn.execute("SELECT COUNT(*) FROM transactions WHERE date(created_at) = date('now')").fetchone()[0]
                elif period == 'week':
                    val = conn.execute("SELECT COUNT(*) FROM transactions WHERE strftime('%Y-%W', created_at) = strftime('%Y-%W', 'now')").fetchone()[0]
                elif period == 'month':
                    val = conn.execute("SELECT COUNT(*) FROM transactions WHERE strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')").fetchone()[0]
                elif period == 'year':
                    val = conn.execute("SELECT COUNT(*) FROM transactions WHERE strftime('%Y', created_at) = strftime('%Y', 'now')").fetchone()[0]
                
                stats[f'{period}_transactions'] = val
                
        return stats

    # ===== 3. الجرد السنوي والنظام المالي (Accounting) =====

    def get_annual_report(self, year: int) -> Dict[str, float]:
        """حساب إجمالي الدخل والمصاريف والأرباح السنوية"""
        with self.get_connection() as conn:
            # الدخل من عمليات تقييم السيارات
            income = conn.execute("SELECT SUM(estimated_price) FROM transactions WHERE strftime('%Y', created_at) = ?", (str(year),)).fetchone()[0] or 0.0
            
            # المصاريف تشمل الرواتب السنوية والمكافآت (Urlaubsgeld/Feiertagsgeld)
            expenses = conn.execute("SELECT SUM(monthly_salary * 12 + urlaubsgeld + feiertags_geld) FROM employees WHERE is_active = 1").fetchone()[0] or 0.0
            
            return {
                'income': income, 
                'expenses': expenses, 
                'profit': income - expenses
            }

    def get_available_years(self) -> List[int]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT strftime('%Y', created_at) as year FROM transactions")
            years = [int(row['year']) for row in cursor.fetchall() if row['year']]
            return sorted(years, reverse=True) if years else [datetime.now().year]

    # ===== 3.1 إدارة الموظفين (Employee Management) =====

    def create_employee(self, **kwargs):
        """إضافة موظف جديد"""
        query = '''
            INSERT INTO employees (
                first_name, last_name, phone, email, address, 
                monthly_salary, annual_leave, sick_leave, unpaid_leave, 
                feiertags_geld, urlaubsgeld, notes, is_active, user_id, job_title
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
        '''
        params = (
            kwargs.get('first_name'), kwargs.get('last_name'),
            kwargs.get('phone'), kwargs.get('email'), kwargs.get('address'),
            kwargs.get('monthly_salary', 0), kwargs.get('annual_leave', 30),
            kwargs.get('sick_leave', 0), kwargs.get('unpaid_leave', 0),
            kwargs.get('feiertags_geld', 0), kwargs.get('urlaubsgeld', 0),
            kwargs.get('notes'), kwargs.get('user_id'), kwargs.get('job_title')
        )
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.lastrowid

    def get_all_employees(self) -> List[Dict]:
        """جلب جميع الموظفين"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employees ORDER BY is_active DESC, first_name ASC")
            return [dict(row) for row in cursor.fetchall()]

    def update_employee(self, emp_id: int, **kwargs):
        """تحديث بيانات موظف"""
        if not kwargs: return
        
        allowed = {'first_name', 'last_name', 'phone', 'email', 'address', 
                   'monthly_salary', 'is_active', 'notes', 'job_title', 'user_id',
                   'annual_leave', 'sick_leave', 'unpaid_leave', 'special_leave',
                   'feiertags_geld', 'urlaubsgeld', 'hire_date'}
        
        updates = []
        params = []
        for k, v in kwargs.items():
            if k in allowed:
                updates.append(f"{k} = ?")
                params.append(v)
        
        if not updates: return
        
        query = f"UPDATE employees SET {', '.join(updates)} WHERE id = ?"
        params.append(emp_id)
        
        with self.get_connection() as conn:
            conn.execute(query, params)

    def delete_employee(self, emp_id: int):
        """حذف موظف نهائياً مع حذف السجلات المرتبطة"""
        with self.get_connection() as conn:
            # حذف سجلات الإجازات المرضية المرتبطة أولاً
            conn.execute("DELETE FROM sick_leave_records WHERE employee_id = ?", (emp_id,))
            # ثم حذف الموظف
            conn.execute("DELETE FROM employees WHERE id = ?", (emp_id,))

    def get_employee_by_user_id(self, user_id: int) -> Optional[Dict]:
        """جلب بيانات الموظف المرتبط بحساب مستخدم معين"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # البحث بواسطة user_id مباشرة أولاً، ثم email كاحتياطي
            cursor.execute('SELECT * FROM employees WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            
            # محاولة البحث عن طريق البريد الإلكتروني كاحتياطي
            user = self.get_user_by_id(user_id)
            if user and user.get('email'):
                cursor.execute('SELECT * FROM employees WHERE email = ?', (user['email'],))
                row = cursor.fetchone()
                return dict(row) if row else None
            return None

    # ===== 3.4 إدارة سجلات الإجازات المرضية =====

    def add_sick_leave_record(self, employee_id: int = None, user_id: int = None, 
                               start_date: str = None, end_date: str = None, 
                               days_count: int = 0, reason: str = None) -> int:
        """إضافة سجل إجازة مرضية جديد"""
        query = '''
            INSERT INTO sick_leave_records (employee_id, user_id, start_date, end_date, days_count, reason)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (employee_id, user_id, start_date, end_date, days_count, reason))
            return cursor.lastrowid

    def get_sick_leave_records(self, employee_id: int = None, user_id: int = None) -> List[Dict]:
        """جلب سجلات الإجازات المرضية لموظف أو مستخدم"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if employee_id:
                cursor.execute('''
                    SELECT * FROM sick_leave_records 
                    WHERE employee_id = ? 
                    ORDER BY start_date DESC
                ''', (employee_id,))
            elif user_id:
                cursor.execute('''
                    SELECT * FROM sick_leave_records 
                    WHERE user_id = ? 
                    ORDER BY start_date DESC
                ''', (user_id,))
            else:
                cursor.execute('SELECT * FROM sick_leave_records ORDER BY start_date DESC')
            return [dict(row) for row in cursor.fetchall()]

    def get_total_sick_leave_days(self, employee_id: int = None, user_id: int = None) -> int:
        """حساب مجموع أيام الإجازات المرضية"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if employee_id:
                cursor.execute('SELECT SUM(days_count) FROM sick_leave_records WHERE employee_id = ?', (employee_id,))
            elif user_id:
                cursor.execute('SELECT SUM(days_count) FROM sick_leave_records WHERE user_id = ?', (user_id,))
            else:
                return 0
            result = cursor.fetchone()[0]
            return result if result else 0

    def delete_sick_leave_record(self, record_id: int) -> bool:
        """حذف سجل إجازة مرضية"""
        try:
            with self.get_connection() as conn:
                conn.execute("DELETE FROM sick_leave_records WHERE id = ?", (record_id,))
            return True
        except Exception:
            return False

    # ===== 3.5 إدارة العقود =====

    def update_contract(self, contract_id: int, **kwargs) -> bool:
        """تحديث بيانات العقد (الأقساط، الدفعة المقدمة، طريقة الدفع، إلخ)"""
        if not kwargs:
            return False
        
        allowed_fields = {
            'total_price', 'total_amount', 'down_payment', 'remaining_amount',
            'installment_count', 'monthly_installment', 'interest_rate',
            'late_fee_type', 'late_fee_amount', 'grace_period_days',
            'payment_due_day', 'status', 'payment_method',
            'vehicle_vin', 'vehicle_type', 'vehicle_model', 'vehicle_plate'
        }
        
        updates = []
        params = []
        
        for key, value in kwargs.items():
            if key in allowed_fields:
                updates.append(f"{key} = ?")
                params.append(value)
        
        if not updates:
            return False
        
        try:
            query = f"UPDATE contracts SET {', '.join(updates)} WHERE id = ?"
            params.append(contract_id)
            with self.get_connection() as conn:
                conn.execute(query, params)
            return True
        except Exception:
            return False
    
    def update_contract_schedule(self, contract_id: int, **kwargs) -> bool:
        """تحديث جدولة العقد (يوم الاستحقاق، فترة السماح، التأجيل)"""
        updates = []
        params = []
        
        if 'due_day' in kwargs:
            updates.append("payment_due_day = ?")
            params.append(kwargs['due_day'])
        if 'grace' in kwargs:
            updates.append("grace_period_days = ?")
            params.append(kwargs['grace'])
        if 'next_date' in kwargs:
            updates.append("next_payment_date = ?")
            params.append(kwargs['next_date'])
        if 'reason' in kwargs:
            updates.append("reschedule_reason = ?")
            params.append(kwargs['reason'])
        
        if not updates:
            return False
        
        try:
            query = f"UPDATE contracts SET {', '.join(updates)} WHERE id = ?"
            params.append(contract_id)
            with self.get_connection() as conn:
                conn.execute(query, params)
            return True
        except Exception:
            return False

    # ===== 4. الصيانة والبيانات العامة =====

    def get_all_used_image_paths(self) -> Set[str]:
        """جلب كافة مسارات الصور المرتبطة بمعاملات لمنع حذفها أثناء التنظيف"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT image_path FROM transactions")
            return {row['image_path'] for row in cursor.fetchall() if row['image_path']}

    def get_setting(self, key: str, default: Any = None) -> Any:
        """جلب إعدادات النظام المخزنة بتنسيق JSON"""
        with self.get_connection() as conn:
            row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
            if row:
                try:
                    return json.loads(row['value'])
                except:
                    return row['value']
            return default

    def set_setting(self, key: str, value: Any):
        """حفظ إعداد في قاعدة البيانات"""
        with self.get_connection() as conn:
            # استخدام REPLACE لتحديث أو إنشاء الإعداد
            conn.execute(
                "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                (key, json.dumps(value, ensure_ascii=False))
            )

    # ===== 5. العقود والدفعات =====

    def backup_database(self) -> str:
        """إنشاء نسخة احتياطية من قاعدة البيانات"""
        import shutil
        from datetime import datetime
        backup_dir = Path(__file__).parent / "backups"
        backup_dir.mkdir(exist_ok=True)
        backup_path = backup_dir / f"smartcar_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy2(self.db_path, backup_path)
        return str(backup_path)

    def create_contract(self, user_id: int, car_data: Dict, total_amount: float, **kwargs) -> int:
        """إنشاء عقد جديد مع جدول الأقساط"""
        from datetime import date, timedelta
        from dateutil.relativedelta import relativedelta
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. إنشاء سجل في جدول transactions (للتوافق القديم)
            cursor.execute('''
                INSERT INTO transactions (
                    user_id, car_type, brand, model, manufacture_year, 
                    mileage, estimated_price, condition_analysis
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                car_data.get('car_type', 'Unknown'),
                car_data.get('brand', 'Unknown'),
                car_data.get('model', 'Unknown'),
                car_data.get('manufacture_year', 2020),
                car_data.get('mileage', 0),
                total_amount,
                json.dumps(kwargs, ensure_ascii=False)
            ))
            transaction_id = cursor.lastrowid
            
            # 2. إنشاء سجل في جدول contracts الفعلي
            installment_count = kwargs.get('installments_count', 1)
            interest_rate = kwargs.get('interest_rate', 0)
            monthly_amount = kwargs.get('monthly_amount', total_amount)
            down_payment = kwargs.get('down_payment', 0)
            payment_due_day = kwargs.get('payment_due_day', 1)
            grace_period = kwargs.get('grace_period', 3)
            
            remaining = total_amount - down_payment
            
            cursor.execute('''
                INSERT INTO contracts (
                    user_id, transaction_id, total_price, down_payment,
                    remaining_amount, installment_count, monthly_installment,
                    interest_rate, payment_due_day, grace_period_days,
                    vehicle_type, vehicle_model, status, car_details
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active', ?)
            ''', (
                user_id, transaction_id, total_amount, down_payment,
                remaining, installment_count, monthly_amount,
                interest_rate, payment_due_day, grace_period,
                car_data.get('brand', ''), car_data.get('model', ''),
                json.dumps(car_data, ensure_ascii=False)
            ))
            contract_id = cursor.lastrowid
            
            # 3. إنشاء جدول الفواتير/الأقساط
            if installment_count > 1:
                today = date.today()
                
                for i in range(1, installment_count + 1):
                    # حساب تاريخ الاستحقاق
                    due_date = today + relativedelta(months=i)
                    try:
                        due_date = due_date.replace(day=min(payment_due_day, 28))
                    except ValueError:
                        due_date = due_date.replace(day=28)
                    
                    # رقم فاتورة فريد
                    from datetime import datetime
                    invoice_number = f"INV-{contract_id}-{i:03d}-{datetime.now().strftime('%Y%m')}"
                    
                    cursor.execute('''
                        INSERT INTO invoices (
                            invoice_number, contract_id, installment_number,
                            amount_due, due_date, status
                        ) VALUES (?, ?, ?, ?, ?, 'pending')
                    ''', (
                        invoice_number, contract_id, i,
                        monthly_amount, str(due_date)
                    ))
            
            return contract_id

    def add_payment(self, contract_id: int, amount: float, method: str, proof_path: str, ref: str) -> int:
        """إضافة دفعة جديدة في جدول payments"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # التحقق من وجود العقد أولاً، وإنشاء سجل مؤقت إذا لم يكن موجوداً
            cursor.execute("SELECT id FROM contracts WHERE id = ?", (contract_id,))
            if not cursor.fetchone():
                # إنشاء عقد مؤقت للسماح بتسجيل الدفعة
                cursor.execute('''
                    INSERT INTO contracts (id, user_id, car_details, total_amount, status)
                    VALUES (?, 1, '{}', ?, 'pending')
                ''', (contract_id, amount))
            
            cursor.execute('''
                INSERT INTO payments (contract_id, amount, payment_method, proof_path, reference_number, status)
                VALUES (?, ?, ?, ?, ?, 'pending')
            ''', (contract_id, amount, method, proof_path, ref))
            payment_id = cursor.lastrowid
            
            # تحديث حالة العقد فقط (بدون remaining_amount لأنه غير موجود)
            cursor.execute('''
                UPDATE contracts SET status = 'paid'
                WHERE id = ?
            ''', (contract_id,))
            
            return payment_id

    def verify_payment(self, payment_id: int) -> bool:
        """تأكيد دفعة وتحديث حالتها"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE payments SET status = 'verified', verified_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (payment_id,))
            return cursor.rowcount > 0
    
    def get_contract_payments(self, contract_id: int) -> List[Dict]:
        """جلب سجل الدفعات لعقد معين"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM payments WHERE contract_id = ? ORDER BY created_at DESC
            ''', (contract_id,))
            return [dict(row) for row in cursor.fetchall()]

    def update_contract_schedule(self, contract_id: int, **kwargs) -> bool:
        """تحديث جدولة العقد (موعد الدفع، فترة السماح، التأجيل)"""
        # placeholder - في التطبيق الحقيقي يجب تحديث جدول العقود
        # المعاملات المتوقعة: due_day, grace, next_date, reason
        return True

    def get_user_payment_preferences(self, user_id: int) -> Optional[Dict]:
        """جلب تفضيلات الدفع المحفوظة للمستخدم من آخر عقد"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # محاولة جلب آخر عقد للمستخدم من جدول contracts
            try:
                cursor.execute('''
                    SELECT c.*, 
                           (SELECT COUNT(*) FROM payments p WHERE p.contract_id = c.id) as payment_count
                    FROM contracts c 
                    WHERE c.user_id = ? 
                    ORDER BY c.created_at DESC 
                    LIMIT 1
                ''', (user_id,))
                row = cursor.fetchone()
            except Exception:
                row = None
            
            # إذا لم نجد في contracts، نحاول من transactions
            if row is None:
                try:
                    cursor.execute('''
                        SELECT t.*, 
                               (SELECT COUNT(*) FROM payments p WHERE p.contract_id = t.id) as payment_count
                        FROM transactions t 
                        WHERE t.user_id = ? 
                        ORDER BY t.created_at DESC 
                        LIMIT 1
                    ''', (user_id,))
                    row = cursor.fetchone()
                    
                    if row is None:
                        return None
                    
                    tx = dict(row)
                    # استخراج بيانات الأقساط من condition_analysis
                    months = 0
                    down_payment = 0
                    try:
                        analysis = json.loads(tx.get('condition_analysis', '{}') or '{}')
                        months = analysis.get('installments_count', 0) or 0
                        down_payment = analysis.get('down_payment', 0) or 0
                    except:
                        pass
                    
                    plan_type = 'full' if months <= 1 else 'installments'
                    
                    if months <= 3:
                        plan_choice_index = 0
                    elif months <= 12:
                        plan_choice_index = 1
                    else:
                        plan_choice_index = 2
                    
                    return {
                        'contract_id': tx.get('id'),
                        'plan_type': plan_type,
                        'plan_type_index': 0 if plan_type == 'full' else 1,
                        'months': months,
                        'plan_choice_index': plan_choice_index,
                        'down_payment': down_payment,
                        'payment_due_day': 1,
                        'grace_period': 3,
                        'payment_method': '',
                        'has_payments': tx.get('payment_count', 0) > 0
                    }
                except Exception:
                    return None
            
            contract = dict(row)
            
            # تحديد نوع الخطة بناءً على عدد الأقساط
            plan_type = 'full' if contract.get('installment_count', 0) <= 1 else 'installments'
            
            # تحديد الخيار المحدد للأشهر
            months = contract.get('installment_count', 0)
            if months <= 3:
                plan_choice_index = 0  # 3 أشهر
            elif months <= 12:
                plan_choice_index = 1  # 12 شهر
            else:
                plan_choice_index = 2  # 24 شهر
            
            return {
                'contract_id': contract.get('id'),
                'plan_type': plan_type,
                'plan_type_index': 0 if plan_type == 'full' else 1,
                'months': months,
                'plan_choice_index': plan_choice_index,
                'down_payment': contract.get('down_payment', 0),
                'payment_due_day': contract.get('payment_due_day', 1),
                'grace_period': contract.get('grace_period_days', 3),
                'payment_method': contract.get('payment_method', ''),
                'has_payments': contract.get('payment_count', 0) > 0
            }

    def has_contract_payments(self, contract_id: int) -> bool:
        """التحقق مما إذا كان العقد يحتوي على دفعات سابقة"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM payments WHERE contract_id = ?
            ''', (contract_id,))
            count = cursor.fetchone()[0]
            return count > 0

    def get_contract_installment_summary(self, contract_id: int) -> Dict:
        """جلب ملخص الأقساط للعقد: الإجمالي، المدفوع، المتبقي"""
        default_result = {
            'total_installments': 0,
            'paid_installments': 0,
            'remaining_installments': 0,
            'total_amount': 0,
            'paid_amount': 0,
            'remaining_amount': 0,
            'monthly_amount': 0
        }
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # محاولة جلب البيانات من جدول contracts أولاً
            try:
                cursor.execute('''
                    SELECT installment_count, monthly_installment, total_price 
                    FROM contracts WHERE id = ?
                ''', (contract_id,))
                contract_row = cursor.fetchone()
            except Exception:
                contract_row = None
            
            # إذا لم نجد في contracts، نحاول من transactions
            if contract_row is None:
                try:
                    cursor.execute('''
                        SELECT estimated_price, condition_analysis 
                        FROM transactions WHERE id = ?
                    ''', (contract_id,))
                    tx_row = cursor.fetchone()
                    if tx_row:
                        tx = dict(tx_row)
                        total_amount = tx.get('estimated_price', 0) or 0
                        # محاولة استخراج بيانات الأقساط من condition_analysis إذا كانت JSON
                        try:
                            import json
                            analysis = json.loads(tx.get('condition_analysis', '{}'))
                            installment_count = analysis.get('installments_count', 0) or 0
                            monthly_amount = analysis.get('monthly_amount', 0) or 0
                        except:
                            installment_count = 0
                            monthly_amount = 0
                        
                        # عدد الدفعات المسددة
                        cursor.execute('''
                            SELECT COUNT(*), COALESCE(SUM(amount), 0) 
                            FROM payments 
                            WHERE contract_id = ? AND status = 'verified'
                        ''', (contract_id,))
                        payment_row = cursor.fetchone()
                        paid_installments = payment_row[0] or 0
                        paid_amount = payment_row[1] or 0
                        
                        remaining_installments = max(0, installment_count - paid_installments)
                        remaining_amount = max(0, total_amount - paid_amount)
                        
                        return {
                            'total_installments': installment_count,
                            'paid_installments': paid_installments,
                            'remaining_installments': remaining_installments,
                            'total_amount': total_amount,
                            'paid_amount': paid_amount,
                            'remaining_amount': remaining_amount,
                            'monthly_amount': monthly_amount
                        }
                except Exception:
                    pass
                return default_result
            
            contract = dict(contract_row)
            total_installments = contract.get('installment_count', 0) or 0
            monthly_amount = contract.get('monthly_installment', 0) or 0
            total_amount = contract.get('total_price', 0) or 0
            
            # عدد الدفعات المسددة
            cursor.execute('''
                SELECT COUNT(*), COALESCE(SUM(amount), 0) 
                FROM payments 
                WHERE contract_id = ? AND status = 'verified'
            ''', (contract_id,))
            payment_row = cursor.fetchone()
            paid_installments = payment_row[0] or 0
            paid_amount = payment_row[1] or 0
            
            # حساب المتبقي
            remaining_installments = max(0, total_installments - paid_installments)
            remaining_amount = max(0, total_amount - paid_amount)
            
            return {
                'total_installments': total_installments,
                'paid_installments': paid_installments,
                'remaining_installments': remaining_installments,
                'total_amount': total_amount,
                'paid_amount': paid_amount,
                'remaining_amount': remaining_amount,
                'monthly_amount': monthly_amount
            }
