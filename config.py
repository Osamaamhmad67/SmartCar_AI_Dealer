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
    # نستخدم Path لضمان التوافق مع كافة أنظمة التشغيل
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
    
    # ===== 3. الذكاء الاصطناعي (Groq) =====
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")
    
    # ===== 4. نظام البريد الإلكتروني =====
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
    SENDER_NAME = os.getenv("SENDER_NAME", "SmartCar AI-Dealer")
    CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "support@smartcar-ai.com")
    SUPPORT_PHONE = os.getenv("SUPPORT_PHONE", "+49123456789")

    # ===== 5. محرك التسعير المتقدم ودعم اللغات (Advanced Pricing Engine) =====
    # مفاتيح ثابتة (Internal Keys) لضمان استقرار الحسابات المالية
    BASE_PRICES = {
        "sedan": int(os.getenv("BASE_PRICE_SEDAN", "35000")),
        "suv": int(os.getenv("BASE_PRICE_SUV", "45000")),
        "coupe": int(os.getenv("BASE_PRICE_COUPE", "40000")),
        "hybrid": int(os.getenv("BASE_PRICE_HYBRID", "50000")),
        "electric": int(os.getenv("BASE_PRICE_ELECTRIC", "55000")),
        "pickup": int(os.getenv("BASE_PRICE_PICKUP", "42000")),
        # أنواع هيكل جديدة
        "hatchback": int(os.getenv("BASE_PRICE_HATCHBACK", "28000")),
        "wagon": int(os.getenv("BASE_PRICE_WAGON", "37000")),
        "convertible": int(os.getenv("BASE_PRICE_CONVERTIBLE", "48000")),
        "van": int(os.getenv("BASE_PRICE_VAN", "38000")),
        "minivan": int(os.getenv("BASE_PRICE_MINIVAN", "35000")),
        "crossover": int(os.getenv("BASE_PRICE_CROSSOVER", "40000")),
        "limousine": int(os.getenv("BASE_PRICE_LIMOUSINE", "65000")),
        "sports": int(os.getenv("BASE_PRICE_SPORTS", "55000")),
    }
    
    # خريطة لربط المسميات بلغات مختلفة بالمفاتيح الثابتة أعلاه
    TYPE_MAPPING = {
        # العربية
        "سيدان": "sedan", "كوبيه": "coupe", "هايبرد": "hybrid",
        "كهربائية": "electric", "بيك أب": "pickup", "شاحنة": "pickup",
        "هاتشباك": "hatchback", "واغن": "wagon", "ستيشن": "wagon",
        "كابريوليه": "convertible", "مكشوفة": "convertible",
        "فان": "van", "مينيفان": "minivan", "كروس أوفر": "crossover",
        "ليموزين": "limousine", "رياضية": "sports", "سبورت": "sports",
        # English
        "sedan": "sedan", "suv": "suv", "coupe": "coupe", "hybrid": "hybrid",
        "electric": "electric", "pickup": "pickup", "hatchback": "hatchback",
        "wagon": "wagon", "estate": "wagon", "convertible": "convertible",
        "cabriolet": "convertible", "van": "van", "minivan": "minivan",
        "crossover": "crossover", "limousine": "limousine", "sports": "sports",
        "sport": "sports",
        # Deutsch
        "limousine": "sedan", "geländewagen": "suv", "elektro": "electric",
        "kombi": "wagon", "cabrio": "convertible", "kabriolett": "convertible",
        "transporter": "van", "kleinbus": "minivan", "sportwagen": "sports",
        "schrägheck": "hatchback", "fließheck": "hatchback",
    }

    # ===== 5.1 معاملات الماركات (35+ ماركة) =====
    BRAND_FACTORS = {
        # Premium German
        "porsche": 1.40, "mercedes": 1.30, "mercedes-benz": 1.30,
        "bmw": 1.25, "audi": 1.22,
        # Mainstream German
        "volkswagen": 1.12, "vw": 1.12, "opel": 1.00, "smart": 0.95,
        # Japanese
        "toyota": 1.15, "lexus": 1.22, "honda": 1.10, "acura": 1.12,
        "mazda": 1.08, "nissan": 1.05, "infiniti": 1.10,
        "subaru": 1.08, "mitsubishi": 1.02, "suzuki": 1.00,
        # Korean
        "hyundai": 1.08, "kia": 1.06, "genesis": 1.18,
        # American
        "tesla": 1.30, "ford": 1.05, "chevrolet": 1.02,
        "jeep": 1.08, "dodge": 1.02, "cadillac": 1.15,
        "lincoln": 1.12, "chrysler": 1.00, "gmc": 1.08, "ram": 1.05,
        # European
        "volvo": 1.15, "skoda": 1.06, "seat": 1.02, "cupra": 1.08,
        "renault": 1.00, "peugeot": 1.00, "citroen": 0.98, "ds": 1.05,
        "fiat": 0.95, "dacia": 0.88, "alfa romeo": 1.05, "lancia": 0.95,
        "mini": 1.08,
        # Luxury / Supercar
        "land rover": 1.25, "range rover": 1.30, "jaguar": 1.15,
        "maserati": 1.20, "bentley": 1.50, "rolls royce": 1.60,
        "rolls-royce": 1.60, "lamborghini": 1.55, "ferrari": 1.60,
        "aston martin": 1.45, "mclaren": 1.50, "bugatti": 1.70,
        "maybach": 1.55, "lotus": 1.35,
        # Chinese (growing in German market)
        "byd": 1.00, "nio": 1.02, "mg": 0.95, "xpeng": 0.98,
        "polestar": 1.10, "lynk & co": 0.98, "ora": 0.92,
        # Default
        "other": 1.00,
    }

    # ===== 5.2 معاملات نوع الوقود =====
    FUEL_FACTORS = {
        # العربية
        "كهربائية": 1.25, "هايبرد": 1.15, "بلاج إن هايبرد": 1.20,
        "ديزل": 1.05, "بنزين": 1.00, "غاز": 0.95, "أخرى": 1.00,
        # English
        "electric": 1.25, "hybrid": 1.15, "plug-in hybrid": 1.20,
        "diesel": 1.05, "petrol": 1.00, "gasoline": 1.00,
        "lpg": 0.95, "cng": 0.95, "hydrogen": 1.20, "other": 1.00,
        # Deutsch
        "elektro": 1.25, "benzin": 1.00, "wasserstoff": 1.20,
    }

    # ===== 5.3 معاملات ناقل الحركة =====
    TRANSMISSION_FACTORS = {
        # العربية
        "أوتوماتيك": 1.05, "يدوي": 0.95, "نصف أوتوماتيك": 1.02,
        # English
        "automatic": 1.05, "manual": 0.95, "semi-automatic": 1.02,
        "dsg": 1.07, "dct": 1.07, "cvt": 1.02, "tiptronic": 1.05,
        # Deutsch
        "automatik": 1.05, "schaltgetriebe": 0.95, "halbautomatik": 1.02,
        # Default
        "other": 1.00,
    }

    # ===== 5.4 معاملات نظام الدفع =====
    DRIVETRAIN_FACTORS = {
        # العربية
        "دفع أمامي": 1.00, "دفع خلفي": 1.00,
        "دفع رباعي": 1.08, "دفع كلي": 1.06,
        # English
        "fwd": 1.00, "rwd": 1.00, "awd": 1.08, "4wd": 1.06,
        "front-wheel": 1.00, "rear-wheel": 1.00,
        "all-wheel": 1.08, "four-wheel": 1.06,
        # Deutsch
        "frontantrieb": 1.00, "hinterradantrieb": 1.00,
        "allradantrieb": 1.08, "vierradantrieb": 1.06,
        "quattro": 1.08, "xdrive": 1.08, "4matic": 1.08,
        "4motion": 1.08,
        # Default
        "other": 1.00,
    }

    # ===== 5.5 معاملات اللون =====
    COLOR_FACTORS = {
        # الألوان الشائعة - أسهل بيعاً
        "أبيض": 1.02, "أسود": 1.02, "فضي": 1.02, "رمادي": 1.01,
        "white": 1.02, "black": 1.02, "silver": 1.02, "gray": 1.01, "grey": 1.01,
        "weiß": 1.02, "schwarz": 1.02, "silber": 1.02, "grau": 1.01,
        # ألوان متوسطة
        "أزرق": 1.00, "أحمر": 1.00, "كحلي": 1.01,
        "blue": 1.00, "red": 1.00, "navy": 1.01, "dark blue": 1.01,
        "blau": 1.00, "rot": 1.00, "dunkelblau": 1.01,
        # ألوان أقل طلباً
        "أخضر": 0.98, "أصفر": 0.97, "برتقالي": 0.97, "بنفسجي": 0.97,
        "green": 0.98, "yellow": 0.97, "orange": 0.97, "purple": 0.97,
        "grün": 0.98, "gelb": 0.97, "orange": 0.97, "lila": 0.97,
        "بني": 0.98, "بيج": 0.99, "ذهبي": 1.00,
        "brown": 0.98, "beige": 0.99, "gold": 1.00, "champagne": 1.00,
        "braun": 0.98,
        # Default
        "other": 1.00,
    }

    # ===== 5.6 معاملات فئة الانبعاثات (Euro) =====
    EMISSIONS_FACTORS = {
        "euro 6d": 1.03, "euro 6d-temp": 1.02,
        "euro 6c": 1.01, "euro 6b": 1.00, "euro 6": 1.00,
        "euro 5": 0.95, "euro 4": 0.88,
        "euro 3": 0.80, "euro 2": 0.72, "euro 1": 0.65,
        # العربية
        "يورو 6": 1.00, "يورو 5": 0.95, "يورو 4": 0.88,
        "يورو 3": 0.80,
        # بدون معلومات
        "unknown": 1.00, "other": 1.00,
    }

    # ===== 5.7 معاملات حجم المحرك (CC) =====
    ENGINE_SIZE_FACTORS = {
        "< 1000": 0.90, "1000-1400": 0.93, "1400-1600": 0.95,
        "1600-2000": 1.00, "2000-2500": 1.05, "2500-3000": 1.08,
        "3000-4000": 1.12, "4000+": 1.18,
    }

    # ===== 5.8 معاملات قوة المحرك (PS/HP) =====
    HORSEPOWER_FACTORS = {
        "< 75": 0.88, "75-100": 0.92, "100-130": 0.95,
        "130-150": 0.97, "150-200": 1.00, "200-250": 1.05,
        "250-300": 1.08, "300-400": 1.12, "400-500": 1.18,
        "500+": 1.25,
    }

    # ===== 5.9 معاملات تاريخ الحوادث =====
    ACCIDENT_FACTORS = {
        # العربية
        "بدون حوادث": 1.00, "حادث بسيط": 0.90,
        "حادث متوسط": 0.80, "حادث كبير": 0.70,
        "ضرر هيكلي": 0.50, "سيارة غرق": 0.40,
        # English
        "none": 1.00, "no accident": 1.00, "minor": 0.90,
        "moderate": 0.80, "major": 0.70,
        "structural": 0.50, "flood": 0.40, "fire": 0.35,
        # Deutsch
        "unfallfrei": 1.00, "leichter unfall": 0.90,
        "mittlerer unfall": 0.80, "schwerer unfall": 0.70,
        "strukturschaden": 0.50, "wasserschaden": 0.40,
        # Default
        "unknown": 0.95, "other": 0.95,
    }

    # ===== 5.10 معاملات الضمان المتبقي =====
    WARRANTY_FACTORS = {
        # العربية
        "أكثر من سنتين": 1.04, "سنة إلى سنتين": 1.02,
        "أقل من سنة": 1.00, "بدون ضمان": 0.98,
        # English
        "> 2 years": 1.04, "1-2 years": 1.02,
        "< 1 year": 1.00, "no warranty": 0.98, "none": 0.98,
        # Deutsch
        "> 2 Jahre": 1.04, "1-2 Jahre": 1.02,
        "< 1 Jahr": 1.00, "keine Garantie": 0.98,
        # Default
        "unknown": 1.00,
    }

    # ===== 5.11 معاملات دفتر الصيانة (Scheckheft) =====
    SERVICE_BOOK_FACTORS = {
        # العربية
        "كامل": 1.05, "جزئي": 1.00, "بدون": 0.95,
        # English
        "complete": 1.05, "full": 1.05, "partial": 1.00, "none": 0.95,
        # Deutsch
        "scheckheftgepflegt": 1.05, "vollständig": 1.05,
        "teilweise": 1.00, "ohne": 0.95,
        # Default
        "unknown": 1.00,
    }

    # ===== 5.12 مكافآت التجهيزات الإضافية (Equipment Bonuses) =====
    # كل قيمة تمثل نسبة الزيادة في السعر عند وجود الميزة
    EQUIPMENT_BONUSES = {
        "navigation": 0.015,          # نظام ملاحة: +1.5%
        "leather": 0.030,             # مقاعد جلد: +3%
        "sunroof": 0.020,             # فتحة سقف: +2%
        "panoramic_roof": 0.025,      # سقف بانوراما: +2.5%
        "heated_seats": 0.015,        # مقاعد مدفأة: +1.5%
        "ventilated_seats": 0.020,    # مقاعد مبردة: +2%
        "parking_sensors": 0.015,     # حساسات ركن: +1.5%
        "parking_camera": 0.020,      # كاميرا خلفية: +2%
        "camera_360": 0.025,          # كاميرا 360°: +2.5%
        "led_headlights": 0.015,      # إنارة LED: +1.5%
        "xenon_headlights": 0.010,    # إنارة زينون: +1%
        "matrix_led": 0.020,          # إنارة ماتريكس: +2%
        "adaptive_cruise": 0.030,     # كروز تكيفي: +3%
        "lane_assist": 0.015,         # مساعد المسار: +1.5%
        "blind_spot": 0.015,          # مراقبة النقطة العمياء: +1.5%
        "auto_parking": 0.020,        # ركن تلقائي: +2%
        "auto_climate": 0.010,        # تكييف أوتوماتيك: +1%
        "dual_climate": 0.015,        # تكييف منفصل: +1.5%
        "sport_package": 0.025,       # باقة رياضية: +2.5%
        "amg_package": 0.035,         # باقة AMG: +3.5%
        "m_package": 0.035,           # باقة M: +3.5%
        "s_line": 0.030,              # باقة S-Line: +3%
        "apple_carplay": 0.010,       # Apple CarPlay: +1%
        "android_auto": 0.010,        # Android Auto: +1%
        "wireless_charging": 0.005,   # شحن لاسلكي: +0.5%
        "heads_up_display": 0.020,    # شاشة عرض أمامية: +2%
        "keyless_entry": 0.010,       # دخول بدون مفتاح: +1%
        "ambient_lighting": 0.008,    # إضاءة محيطية: +0.8%
        "harman_kardon": 0.015,       # نظام صوت هارمان: +1.5%
        "bose_sound": 0.015,          # نظام صوت بوز: +1.5%
        "burmester_sound": 0.020,     # نظام صوت بورميستر: +2%
        "tow_hook": 0.010,            # خطاف سحب: +1%
        "roof_rack": 0.005,           # حامل سقف: +0.5%
        "winter_tires": 0.010,        # إطارات شتوية: +1%
        "spare_key": 0.010,           # مفتاح احتياطي: +1%
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
        """إنشاء مجلدات النظام آلياً لضمان عدم حدوث خطأ FileNotFoundError"""
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

    @classmethod
    def get_factor(cls, factor_dict: dict, key_input: str, default: float = 1.0) -> float:
        """دالة عامة لجلب أي معامل من قاموس - تدعم أي لغة"""
        if not key_input:
            return default
        key = key_input.lower().strip()
        return factor_dict.get(key, default)

    @classmethod
    def get_transmission_factor(cls, transmission: str) -> float:
        return cls.get_factor(cls.TRANSMISSION_FACTORS, transmission)

    @classmethod
    def get_drivetrain_factor(cls, drivetrain: str) -> float:
        return cls.get_factor(cls.DRIVETRAIN_FACTORS, drivetrain)

    @classmethod
    def get_color_factor(cls, color: str) -> float:
        return cls.get_factor(cls.COLOR_FACTORS, color)

    @classmethod
    def get_emissions_factor(cls, emissions_class: str) -> float:
        return cls.get_factor(cls.EMISSIONS_FACTORS, emissions_class)

    @classmethod
    def get_accident_factor(cls, accident_history: str) -> float:
        return cls.get_factor(cls.ACCIDENT_FACTORS, accident_history, default=0.95)

    @classmethod
    def get_warranty_factor(cls, warranty: str) -> float:
        return cls.get_factor(cls.WARRANTY_FACTORS, warranty)

    @classmethod
    def get_service_book_factor(cls, service_book: str) -> float:
        return cls.get_factor(cls.SERVICE_BOOK_FACTORS, service_book)

    @classmethod
    def get_engine_size_factor(cls, cc: int) -> float:
        """جلب معامل حجم المحرك بناءً على السعة اللترية"""
        if cc <= 0:
            return 1.0
        if cc < 1000:
            return 0.90
        elif cc < 1400:
            return 0.93
        elif cc < 1600:
            return 0.95
        elif cc < 2000:
            return 1.00
        elif cc < 2500:
            return 1.05
        elif cc < 3000:
            return 1.08
        elif cc < 4000:
            return 1.12
        else:
            return 1.18

    @classmethod
    def get_horsepower_factor(cls, hp: int) -> float:
        """جلب معامل قوة المحرك بناءً على الحصان"""
        if hp <= 0:
            return 1.0
        if hp < 75:
            return 0.88
        elif hp < 100:
            return 0.92
        elif hp < 130:
            return 0.95
        elif hp < 150:
            return 0.97
        elif hp < 200:
            return 1.00
        elif hp < 250:
            return 1.05
        elif hp < 300:
            return 1.08
        elif hp < 400:
            return 1.12
        elif hp < 500:
            return 1.18
        else:
            return 1.25

    @classmethod
    def calculate_equipment_bonus(cls, equipment_list: list) -> float:
        """حساب مكافأة التجهيزات الإضافية"""
        if not equipment_list:
            return 1.0
        total_bonus = 0.0
        for item in equipment_list:
            key = item.lower().strip().replace(" ", "_")
            total_bonus += cls.EQUIPMENT_BONUSES.get(key, 0.0)
        # الحد الأقصى للمكافأة 25%
        return 1.0 + min(total_bonus, 0.25)

    @classmethod
    def validate_config(cls):
        """التحقق من صحة الإعدادات الحيوية للنظام"""
        required_vars = ["GROQ_API_KEY", "APP_SECRET_KEY"]
        missing = [var for var in required_vars if not getattr(cls, var, None)]
        
        if missing:
            print(f"⚠️ Warning: Missing configuration variables: {', '.join(missing)}")
            # لا نوقف التطبيق هنا، فقط تحذير
