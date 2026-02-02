"""
utils/general_utils.py - الأدوات المساعدة العامة
SmartCar AI-Dealer
تنسيق البيانات، معالجة النصوص، ووظائف التحويل المساعدة
"""

import re
from datetime import datetime
from typing import Union

class GeneralUtils:
    """مجموعة من الوظائف الساكنة لتنظيف وتنسيق البيانات عبر النظام"""

    @staticmethod
    def format_currency(amount: Union[int, float], lang: str = 'Deutsch') -> str:
        """
        تنسيق المبالغ المالية مع العملة المناسبة بناءً على اللغة
        """
        try:
            formatted_amount = f"{float(amount):,.2f}"
            
            if lang.lower() == 'deutsch' or lang.lower() == 'german':
                # التنسيق الألماني يستخدم النقطة للآلاف والفاصلة للقروش
                res = formatted_amount.replace(',', 'X').replace('.', ',').replace('X', '.')
                return f"{res} €"
            elif lang.lower() == 'عربي' or lang.lower() == 'arabic':
                return f"{formatted_amount} يورو"
            else:
                return f"€{formatted_amount}"
        except Exception:
            return f"{amount} €"

    @staticmethod
    def clean_text(text: str) -> str:
        """تنظيف النصوص من الرموز الغريبة والمسافات الزائدة"""
        if not text:
            return ""
        # إزالة علامات Markdown والرموز الخاصة
        clean = re.sub(r'[#*`_]', '', text)
        return clean.strip()

    @staticmethod
    def get_time_greeting(lang: str = 'Deutsch') -> str:
        """إرجاع تحية بناءً على وقت اليوم واللغة المختارة"""
        hour = datetime.now().hour
        if lang.lower() == 'عربي':
            if hour < 12: return "صباح الخير"
            return "مساء الخير"
        elif lang.lower() == 'deutsch':
            if hour < 12: return "Guten Morgen"
            if hour < 18: return "Guten Tag"
            return "Guten Abend"
        else:
            if hour < 12: return "Good Morning"
            return "Good Evening"

    @staticmethod
    def validate_email(email: str) -> bool:
        """التحقق من صحة صيغة البريد الإلكتروني باستخدام Regex"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def calculate_age(birth_year: int) -> int:
        """حساب العمر بناءً على السنة الحالية"""
        return datetime.now().year - birth_year