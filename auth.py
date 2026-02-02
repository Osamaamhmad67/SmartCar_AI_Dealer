"""
auth.py - مدير المصادقة والأمان
SmartCar AI-Dealer
إدارة تسجيل الدخول، تشفير كلمات المرور، وحماية الجلسات
"""

import bcrypt
import streamlit as st
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from db_manager import DatabaseManager
from config import Config

class AuthManager:
    """المسؤول عن التحقق من الهوية وإدارة صلاحيات الوصول"""

    def __init__(self):
        self.db = DatabaseManager()
        self.logger = Config.logger
        # عدد جولات التشفير (تؤخذ من الإعدادات)
        self.rounds = Config.BCRYPT_ROUNDS

    def hash_password(self, password: str) -> str:
        """تشفير كلمة المرور باستخدام خوارزمية bcrypt"""
        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def check_password(self, password: str, hashed_password: str) -> bool:
        """التحقق من مطابقة كلمة المرور المدخلة مع المشفرة"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception:
            return False

    def login(self, username_or_email: str, password: str) -> bool:
        """
        محاولة تسجيل الدخول وتوثيق الجلسة في Streamlit
        """
        user = self.db.get_user_by_username(username_or_email)
        
        if user:
            # التحقق من أن الحساب ليس مقفلاً
            if user.get('locked_until') and datetime.now() < datetime.fromisoformat(user['locked_until']):
                st.error("⚠️ الحساب مقفل مؤقتاً بسبب محاولات خاطئة متكررة.")
                return False

            if self.check_password(password, user['password_hash']):
                # تسجيل دخول ناجح
                self.db.record_login_attempt(user['username'], success=True)
                
                # تخزين بيانات المستخدم في جلسة Streamlit
                st.session_state['logged_in'] = True
                st.session_state['user'] = {
                    'id': user['id'],
                    'username': user['username'],
                    'full_name': user['full_name'],
                    'role': user['role'], # 'admin' or 'user'
                    'email': user['email']
                }
                
                if self.logger:
                    self.logger.info(f"👤 User logged in: {user['username']}")
                return True
            else:
                # تسجيل محاولة خاطئة
                self.db.record_login_attempt(user['username'], success=False)
                st.error("❌ كلمة المرور غير صحيحة.")
        else:
            st.error("❌ اسم المستخدم أو البريد غير موجود.")
            
        return False

    def register_user(self, username: str, email: str, password: str, full_name: str, phone: str = None) -> tuple:
        """
        تسجيل مستخدم جديد في النظام
        Returns: (success: bool, message: str, user_id: int or None)
        """
        try:
            hashed_pw = self.hash_password(password)
            with self.db.get_connection() as conn:
                cursor = conn.execute('''
                    INSERT INTO users (username, email, password_hash, full_name, phone, role)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (username, email, hashed_pw, full_name, phone, 'user'))
                user_id = cursor.lastrowid
            
            if self.logger:
                self.logger.info(f"🆕 New user registered: {username}")
            return True, "تم إنشاء الحساب بنجاح", user_id
        except Exception as e:
            if "UNIQUE" in str(e):
                return False, "اسم المستخدم أو البريد الإلكتروني مسجل مسبقاً", None
            else:
                return False, f"خطأ أثناء التسجيل: {str(e)}", None

    @staticmethod
    def logout():
        """إنهاء الجلسة ومسح بيانات المستخدم"""
        for key in ['logged_in', 'user']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    @staticmethod
    def is_logged_in() -> bool:
        """التحقق من حالة تسجيل الدخول الحالية"""
        return st.session_state.get('logged_in', False)

    @staticmethod
    def get_current_user() -> Optional[Dict]:
        """الحصول على بيانات المستخدم الحالي من الجلسة"""
        return st.session_state.get('user')

    @staticmethod
    def is_admin() -> bool:
        """التحقق مما إذا كان المستخدم الحالي لديه صلاحيات مشرف"""
        user = st.session_state.get('user')
        return user is not None and user.get('role') == 'admin'

    def login_user(self, username: str, password: str):
        """
        تسجيل الدخول وإرجاع النتيجة للتعامل معها خارجياً
        Returns: (success: bool, message: str, user_data: dict)
        """
        user = self.db.get_user_by_username(username)
        
        if not user:
            return False, "اسم المستخدم أو البريد غير موجود", None
            
        # التحقق من أن الحساب ليس مقفلاً
        if user.get('locked_until') and datetime.now() < datetime.fromisoformat(user['locked_until']):
            return False, "الحساب مقفل مؤقتاً بسبب محاولات خاطئة متكررة", None

        if self.check_password(password, user['password_hash']):
            # تسجيل دخول ناجح
            self.db.record_login_attempt(user['username'], success=True)
            
            user_data = {
                'id': user['id'],
                'username': user['username'],
                'full_name': user['full_name'],
                'role': user['role'],
                'email': user['email']
            }
            if self.logger:
                self.logger.info(f"👤 User logged in: {user['username']}")
                
            return True, "تم تسجيل الدخول بنجاح", user_data
        else:
            # تسجيل محاولة خاطئة
            self.db.record_login_attempt(user['username'], success=False)
            return False, "كلمة المرور غير صحيحة", None

    def generate_reset_token(self, email: str) -> tuple:
        """
        إنشاء رمز إعادة تعيين كلمة المرور
        Returns: (success: bool, message: str, token: str or None)
        """
        import secrets
        
        user = self.db.get_user_by_username(email)
        
        if not user:
            # نرجع نجاح وهمي لمنع تسريب معلومات عن المستخدمين المسجلين
            return True, "إذا كان البريد مسجلاً ستصلك رسالة قريباً", None
        
        # إنشاء رمز عشوائي آمن
        token = secrets.token_urlsafe(32)
        
        # حفظ الرمز في قاعدة البيانات (يمكن تخزينه في جدول منفصل أو في الإعدادات)
        # هذا التنفيذ البسيط يحفظه في ذاكرة الجلسة للتبسيط
        if 'reset_tokens' not in st.session_state:
            st.session_state.reset_tokens = {}
        
        st.session_state.reset_tokens[token] = {
            'email': email,
            'expires': datetime.now() + timedelta(hours=1)
        }
        
        if self.logger:
            self.logger.info(f"🔑 Password reset token generated for: {email}")
        
        return True, "تم إرسال رابط إعادة التعيين إلى بريدك الإلكتروني", token

