"""
create_admin.py - سكريبت تهيئة النظام وإنشاء حساب المدير
SmartCar AI-Dealer
يستخدم لإنشاء الجداول وحساب المشرف الأول (Super Admin)
"""

import sys
from pathlib import Path
from datetime import datetime

# إضافة المسار الحالي لضمان استيراد الملفات المحلية
sys.path.append(str(Path(__file__).parent))

from db_manager import DatabaseManager
from auth import AuthManager
from config import Config

def initialize_system():
    """تهيئة المجلدات وقاعدة البيانات وإنشاء حساب المدير"""
    print(f"🚀 Starting {Config.APP_NAME} initialization...")
    
    # 1. إنشاء مجلدات النظام (uploads, logs, invoices, etc.)
    Config.create_directories()
    print("✅ System directories created.")

    # 2. تهيئة مدير قاعدة البيانات والمصادقة
    db = DatabaseManager()
    auth = AuthManager()

    # 3. بيانات حساب المدير (يمكنك تغييرها من هنا)
    admin_username = "admin"
    admin_email = "admin@smartcar.com"
    admin_password = "admin123"  # يرجى تغييرها بعد أول تسجيل دخول
    admin_full_name = "System Administrator"

    print(f"🛠️ Checking for admin account: {admin_username}...")

    try:
        # التحقق مما إذا كان المدير موجوداً مسبقاً
        existing_admin = db.get_user_by_username(admin_username)
        
        if existing_admin:
            print(f"⚠️ Admin '{admin_username}' already exists. Skipping creation.")
        else:
            # تشفير كلمة المرور وإدراج الحساب بصلاحيات admin
            hashed_pw = auth.hash_password(admin_password)
            
            with db.get_connection() as conn:
                conn.execute('''
                    INSERT INTO users (
                        username, email, password_hash, full_name, role, is_active
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (admin_username, admin_email, hashed_pw, admin_full_name, 'admin', 1))
            
            print("=" * 40)
            print("✅ ADMIN ACCOUNT CREATED SUCCESSFULLY!")
            print(f"   Username: {admin_username}")
            print(f"   Password: {admin_password}")
            print(f"   Role:     Administrator")
            print("=" * 40)
            print("👉 Please change your password after logging in for the first time.")

        # 4. إضافة إعدادات النظام الافتراضية
        with db.get_connection() as conn:
            conn.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", 
                        ('system_version', '"2.0.0"'))
            conn.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", 
                        ('last_cleanup', f'"{datetime.now().isoformat()}"'))

        print("\n✨ System is ready to use!")
        print("Run the app using: streamlit run app.py")

    except Exception as e:
        print(f"❌ Critical error during initialization: {str(e)}")

if __name__ == "__main__":
    initialize_system()