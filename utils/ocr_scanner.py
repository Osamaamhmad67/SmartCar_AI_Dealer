"""
utils/ocr_scanner.py - ماسح الوثائق الذكي (OCR)
SmartCar AI-Dealer
استخراج البيانات من الهويات ورخص القيادة باستخدام رؤية الحاسوب
"""

from groq_base import GroqBaseClient

class DocumentScanner(GroqBaseClient):
    """ماسح الوثائق الذكي المعتمد على نموذج رؤية Groq"""

    def scan_document(self, image_bytes: bytes, lang: str = "عربي") -> dict:
        """
        تحليل وثيقة (هوية، رخصة) واستخراج البيانات الأساسية منها.
        :param image_bytes: بيانات الصورة بالبايت
        :param lang: لغة استخراج البيانات
        :return: قاموس يحتوي على البيانات المستخرجة
        """
        prompt = f"""
        Identify and extract information from this document.
        Return a JSON object with exactly these keys:
        - full_name (الاسم الكامل)
        - id_number (رقم الهوية أو الوثيقة)
        - expiry_date (تاريخ الانتهاء)
        - document_type (نوع الوثيقة مثل: هوية، رخصة قيادة)
        
        The output must be in {lang}.
        Return ONLY the JSON object.
        """

        try:
            # استخدام العميل الأساسي لإرسال الصورة
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{self._encode_image(image_bytes)}"
                                },
                            },
                        ],
                    }
                ],
                # الالتزام بتنسيق JSON عبر البرومبت
            )

            content = response.choices[0].message.content
            return self._parse_json_response(content)

        except Exception as e:
            # محاولة تسجيل الخطأ إذا كان المسجل متاحاً
            if hasattr(self, 'logger') and self.logger:
                self.logger.error(f"OCR Scan Error: {str(e)}")
            return {"error": "فشل مسح الوثيقة", "details": str(e)}

    def validate_id(self, extracted_data: dict) -> bool:
        """
        التحقق من أن البيانات المستخرجة كافية ومكتملة.
        """
        required_keys = ['full_name', 'id_number', 'expiry_date']
        # التأكد من وجود المفاتيح وأن قيمها ليست فارغة
        return all(key in extracted_data and extracted_data[key] for key in required_keys)

    def scan_id_card(self, image_bytes: bytes) -> dict:
        """مسح بطاقة الهوية واستخراج البيانات"""
        prompt = """
        Extract information from this ID card image.
        IMPORTANT: Keep all extracted text EXACTLY as written on the card. Do NOT translate names, places, or any text.
        If the card is in German, keep it in German. If in Arabic, keep it in Arabic.
        
        Return a JSON object with these keys:
        - full_name (الاسم الكامل - exactly as on card)
        - id_number (رقم الهوية)
        - nationality (الجنسية - exactly as on card)
        - birth_date (تاريخ الميلاد)
        - expiry_date (تاريخ الانتهاء)
        
        If any field is unclear write "غير واضح".
        Return ONLY the JSON object.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self._encode_image(image_bytes)}"}}
                    ]
                }]
            )
            return self._parse_json_response(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}

    def scan_driver_license(self, image_bytes: bytes) -> dict:
        """مسح رخصة القيادة واستخراج البيانات"""
        prompt = """
        Extract information from this driver's license image.
        IMPORTANT: Keep all extracted text EXACTLY as written on the license. Do NOT translate names, places, or any text.
        If the license is in German, keep it in German. If in Arabic, keep it in Arabic.
        
        Return a JSON object with these keys:
        - full_name (الاسم الكامل - exactly as on license)
        - license_number (رقم الرخصة)
        - license_type (نوع الرخصة - exactly as on license)
        - expiry_date (تاريخ الانتهاء)
        - issue_date (تاريخ الإصدار)
        
        If any field is unclear write "غير واضح".
        Return ONLY the JSON object.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self._encode_image(image_bytes)}"}}
                    ]
                }]
            )
            return self._parse_json_response(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}