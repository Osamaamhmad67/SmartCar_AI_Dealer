"""
utils/validation.py - نظام التحقق من جودة الصور والبيانات
SmartCar AI-Dealer
ضمان صلاحية الصور المرفوعة قبل إرسالها للتحليل لتقليل التكاليف ومنع الأخطاء
"""

import io
from PIL import Image
import numpy as np
from typing import Dict, Tuple, Union
from config import Config

class ImageValidator:
    """كلاس متخصص في فحص جودة وصحة صور السيارات والوثائق"""

    def __init__(self):
        self.max_size = Config.MAX_UPLOAD_SIZE_BYTES
        self.allowed_types = Config.ALLOWED_IMAGE_TYPES

    def validate(self, image_bytes: bytes) -> Dict[str, Union[bool, str]]:
        """
        إجراء فحص شامل للصورة المستلمة
        :return: قاموس يحتوي على نتيجة الفحص ورسالة الخطأ إن وجدت
        """
        # 1. فحص حجم الملف
        if len(image_bytes) > self.max_size:
            return {
                'is_valid': False, 
                'msg_key': 'err_file_too_large', 
                'details': f"Max size: {Config.MAX_UPLOAD_SIZE_MB}MB"
            }

        try:
            # 2. فحص إمكانية فتح الصورة (ليست تالفة)
            img = Image.open(io.BytesIO(image_bytes))
            img.verify() # فحص أولي للبيانات
            
            # إعادة فتح الصورة للعمليات المتقدمة لأن verify() تغلق الملف
            img = Image.open(io.BytesIO(image_bytes))
            
            # 3. فحص الأبعاد (لضمان وضوح كافٍ للذكاء الاصطناعي)
            width, height = img.size
            if width < 300 or height < 300:
                return {'is_valid': False, 'msg_key': 'err_low_resolution'}

            # 4. فحص الإضاءة (Brightness)
            # نحول الصورة إلى تدرج الرمادي ونحسب المتوسط
            data = np.array(img.convert('L'))
            brightness = np.mean(data)
            
            if brightness < 40: # معتمة جداً
                return {'is_valid': True, 'has_warning': True, 'msg_key': 'warn_too_dark'}
            elif brightness > 230: # ساطعة جداً
                return {'is_valid': True, 'has_warning': True, 'msg_key': 'warn_too_bright'}

            return {'is_valid': True, 'msg_key': 'success'}

        except Exception as e:
            return {'is_valid': False, 'msg_key': 'err_corrupted', 'details': str(e)}

def validate_car_image(image_bytes: bytes) -> Tuple[bool, str]:
    """
    دالة مساعدة سريعة للاستخدام المباشر في واجهة Streamlit
    :return: (True/False, رسالة النجاح أو الخطأ)
    """
    validator = ImageValidator()
    result = validator.validate(image_bytes)
    
    # تحويل مفاتيح الرسائل إلى نصوص مفهومة (يمكن ربطها بملف لغات)
    messages = {
        'success': "صورة صالحة للتحليل",
        'err_file_too_large': "حجم الملف كبير جداً",
        'err_low_resolution': "دقة الصورة منخفضة جداً، يرجى رفع صورة أوضح",
        'warn_too_dark': "الصورة معتمة، قد تكون النتائج غير دقيقة",
        'warn_too_bright': "إضاءة الصورة قوية جداً",
        'err_corrupted': "ملف الصورة تالف أو غير مدعوم"
    }
    
    return result['is_valid'], messages.get(result.get('msg_key', 'err_corrupted'))