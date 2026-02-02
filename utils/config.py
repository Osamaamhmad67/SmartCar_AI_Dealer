"""
config.py - مركز التحكم وإدارة الإعدادات المتكامل
SmartCar AI-Dealer
إدارة المسارات، الأمان، معاملات التسعير، ودعم اللغات الثلاث
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

class Config:
    """فئة إدارة جميع إعدادات التطبيق وضمان تكاملها"""
    
    # ===== 1. المسارات الأساسية (BASE PATHS) =====
    # نستخدم Path لضمان التوافق مع Windows (C:\\Users\\...)
    BASE_DIR = Path(__file__).parent.absolute()
    
    CACHE_DIR = BASE_DIR / ".cache"
    BACKUPS_DIR = BASE_DIR / "backups"
    DATA_DIR = BASE_DIR / "data"
    FONTS_DIR = BASE_DIR / "fonts"
    INVOICES_DIR = BASE_DIR / "invoices"
    LOGS_DIR = BASE_DIR / "logs"
    UPLOADS_DIR = BASE_DIR / "uploads"
    
    # ===== 2. إعدادات الهوية والأمان =====
    APP_NAME = os.getenv("APP_NAME", "SmartCar AI-Dealer")
    APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "default-secret-key-change-me")
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # قاعدة البيانات
    DATABASE_PATH = BASE_DIR / os.getenv("DATABASE_PATH", "smartcar.db")
    DATABASE_ENCRYPTION_KEY = os.getenv("DATABASE_ENCRYPTION_KEY", "")
    
    # ===== 3. الذكاء الاصطناعي (Groq) =====
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.2-11b-vision-preview")
    
    # ===== 4. نظام البريد الإلكتروني =====
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
    SENDER_NAME = os.getenv("SENDER_NAME", "SmartCar AI-Dealer")
    CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "support@smartcar-ai.com")
    SUPPORT_PHONE = os.getenv("SUPPORT_PHONE", "+49123456789")

    # ===== 5. محرك التسعير ودعم اللغات (Language Integration) =====
    # نستخدم مفاتيح ثابتة (Internal Keys) لتجنب الأخطاء عند تغيير اللغة في الواجهة
    BASE_PRICES = {
        "sedan": int(os.getenv("BASE_PRICE_SEDAN", "50000")),
        "suv": int(os.getenv("BASE_PRICE_SUV", "60000")),
        "coupe": int(os.getenv("BASE_PRICE_COUPE", "55000")),
        "hybrid": int(os.getenv("BASE_PRICE_HYBRID", "65000")),
        "electric": int(os.getenv("BASE_PRICE_ELECTRIC", "70000")),
        "pickup": int(os.getenv("BASE_PRICE_PICKUP", "58000")),
    }
    
    # خريطة لربط المسميات بلغات مختلفة بالمفاتيح الثابتة أعلاه
    TYPE_MAPPING = {
        # العربية
        "سيدان": "sedan", "suv": "suv", "كوبيه": "coupe", "هايبرد": "hybrid", "كهربائية": "electric", "بيك أب": "pickup",
        # English
        "sedan": "sedan", "coupe": "coupe", "hybrid": "hybrid", "electric": "electric", "pickup": "pickup",
        # Deutsch
        "limousine": "sedan", "geländewagen": "suv", "elektro": "electric"
    }

    BRAND_FACTORS = {
        "toyota": 1.15, "bmw": 1.25, "mercedes": 1.30, "audi": 1.20,
        "tesla": 1.30, "porsche": 1.35, "other": 1.00
    }

    # ===== 6. الأمان والحدود =====
    BCRYPT_ROUNDS = int(os.getenv("BCRYPT_ROUNDS", "12"))
    SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", "120"))
    MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))
    MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024
    ALLOWED_IMAGE_TYPES = os.getenv("ALLOWED_IMAGE_TYPES", "jpg,jpeg,png,webp").split(",")

    # ===== 7. الخطوط (Fonts) =====
    FONT_REGULAR = "Cairo-Regular.ttf"
    FONT_BOLD = "Cairo-Bold.ttf"

    # ===== 8. التهيئة (Initialization) =====
    logger = None

    @classmethod
    def create_directories(cls):
        """إنشاء مجلدات النظام آلياً عند بدء التطبيق"""
        dirs = [cls.CACHE_DIR, cls.BACKUPS_DIR, cls.DATA_DIR, cls.FONTS_DIR, 
                cls.INVOICES_DIR, cls.LOGS_DIR, cls.UPLOADS_DIR]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_base_price(cls, car_type_input: str) -> int:
        """جلب السعر الأساسي بناءً على نوع السيارة بأي لغة كانت"""
        key = cls.TYPE_MAPPING.get(car_type_input.lower().strip(), "sedan")
        return cls.BASE_PRICES.get(key, 50000)

    @classmethod
    def get_brand_factor(cls, brand_input: str) -> float:
        """جلب معامل الماركة مع معالجة ذكية للنصوص"""
        brand = brand_input.lower().strip()
        return cls.BRAND_FACTORS.get(brand, cls.BRAND_FACTORS["other"])