"""
utils/logger.py - نظام السجلات الذكي
SmartCar AI-Dealer
إدارة تتبع الأخطاء، مراقبة العمليات، وتوثيق نشاط المستخدمين
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from config import Config

def setup_logger(name: str = "SmartCarAI") -> logging.Logger:
    """
    إعداد وتهيئة المسجل (Logger) مع دعم تدوير الملفات (Rotating Files)
    لمنع امتلاء مساحة التخزين.
    """
    # 1. التأكد من وجود مجلد السجلات
    log_dir = Config.LOGS_DIR
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / "app.log"
    
    # 2. إنشاء المسجل
    logger = logging.getLogger(name)
    
    # منع تكرار السجلات إذا تم استدعاء الدالة أكثر من مرة
    if logger.hasHandlers():
        return logger
        
    logger.setLevel(getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO))

    # 3. تنسيق السجلات (Formatter)
    # [الوقت] [المستوى] [اسم الملف:السطر] الرسالة
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 4. معالج الملفات (File Handler) - تدوير الملف كل 5 ميجابايت والاحتفاظ بـ 5 نسخ
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=5*1024*1024, 
        backupCount=5, 
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 5. معالج المنصة (Console Handler) - للعرض في الـ Terminal أثناء التطوير
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

def log_api_failure(provider: str, error_msg: str):
    """وظيفة مخصصة لتسجيل فشل الاتصال بالذكاء الاصطناعي"""
    logger = logging.getLogger("SmartCarAI.API")
    logger.error(f"⚠️ API Failure | Provider: {provider} | Error: {error_msg}")

def log_transaction(user_id: int, action: str, details: str):
    """وظيفة مخصصة لتسجيل العمليات المالية المهمة"""
    logger = logging.getLogger("SmartCarAI.Audit")
    logger.info(f"💰 Transaction | User: {user_id} | Action: {action} | Details: {details}")

# تعيين المسجل في Config ليكون متاحاً لجميع الملفات
Config.logger = setup_logger()