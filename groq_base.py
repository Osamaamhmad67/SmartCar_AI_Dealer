"""
groq_base.py - العميل الأساسي للاتصال بمنصة Groq Cloud
SmartCar AI-Dealer
إدارة تشفير الصور، تهيئة الـ API، ومعالجة استجابات نماذج Vision
"""

import base64
import json
import re
from typing import Dict, Any, Optional
from groq import Groq
from config import Config

class GroqBaseClient:
    """الفئة الأساسية للتعامل مع Groq API - تدعم نماذج النصوص والرؤية"""

    def __init__(self):
        """تهيئة العميل باستخدام المفتاح والنموذج من الإعدادات"""
        self.api_key = Config.GROQ_API_KEY
        self.model = Config.GROQ_MODEL
        self.logger = Config.logger
        
        # التأكد من وجود مفتاح API قبل التشغيل
        if not self.api_key:
            if self.logger:
                self.logger.error("❌ Groq API Key is missing in .env file!")
            raise ValueError("Groq API Key not found.")

        # إنشاء عميل Groq
        self.client = Groq(api_key=self.api_key)

    def _encode_image(self, image_bytes: bytes) -> str:
        """تحويل بيانات الصورة من بايتات إلى نص Base64 للارسال عبر الـ API"""
        try:
            return base64.b64encode(image_bytes).decode('utf-8')
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ Error encoding image: {str(e)}")
            raise

    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """
        استخراج ومعالجة نصوص JSON من ردود الذكاء الاصطناعي.
        تتعامل مع الحالات التي يضيف فيها النموذج نصوصاً توضيحية خارج الـ JSON.
        """
        try:
            # محاولة البحث عن كود JSON داخل علامات الاستشهاد ```json ... ```
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                clean_content = json_match.group(1)
            else:
                # إذا لم توجد علامات، نبحث عن أول { وآخر }
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                if start != -1 and end != 0:
                    clean_content = response_text[start:end]
                else:
                    clean_content = response_text

            return json.loads(clean_content)
            
        except json.JSONDecodeError as e:
            if self.logger:
                self.logger.error(f"❌ JSON Parsing Error: {str(e)} | Content: {response_text}")
            return {"error": "فشل في معالجة البيانات المستخرجة", "raw_content": response_text}

    def _check_api_status(self) -> bool:
        """فحص بسيط للتأكد من استقرار الاتصال بالـ API"""
        try:
            # محاولة طلب قائمة الموديلات المتاحة كفحص سريع
            self.client.models.list()
            return True
        except Exception:
            return False