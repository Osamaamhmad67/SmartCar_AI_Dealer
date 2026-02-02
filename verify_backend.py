"""
verify_backend.py - أداة التحقق من صحة النظام
SmartCar AI-Dealer
فحص الاتصال بالذكاء الاصطناعي، قاعدة البيانات، والمسارات الحيوية
"""

import os
import sys
from pathlib import Path
from config import Config
from db_manager import DatabaseManager
from groq_base import GroqBaseClient

def check_step(name: str, status: bool, message: str = ""):
    """طباعة نتيجة الفحص بشكل منظم"""
    symbol = "✅" if status else "❌"
    msg = f"{symbol} {name}"
    if message:
        msg += f" - {message}"
    print(msg)
    return status

def verify_all():
    print(f"--- Checking {Config.APP_NAME} Backend Systems ---\n")
    all_passed = True

    # 1. التحقق من وجود ملف .env
    env_exists = Path(".env").exists()
    if not check_step("Environment File (.env)", env_exists, "Missing file if failed"):
        all_passed = False

    # 2. التحقق من إعدادات المسارات
    Config.create_directories()
    check_step("Directory Structure", True, "Created/Verified all folders")

    # 3. التحقق من مفتاح API لـ Groq
    has_api_key = len(Config.GROQ_API_KEY) > 10
    if not check_step("Groq API Key Configuration", has_api_key, "Key looks too short or missing"):
        all_passed = False

    # 4. اختبار الاتصال الفعلي بـ Groq
    try:
        groq_test = GroqBaseClient()
        connection_ok = groq_test._check_api_status()
        if not check_step("Groq API Connection", connection_ok, "Could not reach Groq servers"):
            all_passed = False
    except Exception as e:
        check_step("Groq API Connection", False, str(e))
        all_passed = False

    # 5. التحقق من قاعدة البيانات
    try:
        db = DatabaseManager()
        with db.get_connection() as conn:
            conn.execute("SELECT 1")
        check_step("Database Connection", True, f"Connected to {Config.DATABASE_PATH}")
    except Exception as e:
        check_step("Database Connection", False, str(e))
        all_passed = False

    # 6. التحقق من ملفات الخطوط (ضرورية للفواتير)
    fonts_exist = (Config.FONTS_DIR / Config.FONT_REGULAR).exists()
    if not check_step("System Fonts", fonts_exist, "Missing Arabic fonts in /fonts folder"):
        # لا نوقف النظام بسبب الخطوط لكن ننبه المستخدم
        pass

    print("\n--- Verification Summary ---")
    if all_passed:
        print("🚀 All systems are GO! You can now run the app.")
    else:
        print("⚠️ Some systems failed. Please check the logs and .env file.")
        sys.exit(1)

if __name__ == "__main__":
    verify_all()