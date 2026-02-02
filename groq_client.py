"""
groq_client.py - المحلل الذكي للسيارات
SmartCar AI-Dealer
تحليل صور السيارات، اكتشاف الأضرار، واستخراج المواصفات الفنية
"""

from typing import Dict, Any
from groq_base import GroqBaseClient
from config import Config

class CarAIClient(GroqBaseClient):
    """العميل المتخصص في تحليل رؤية الحاسوب للسيارات"""

    def analyze_car_image(self, image_bytes: bytes, user_lang: str = "Deutsch") -> Dict[str, Any]:
        """
        إرسال صورة السيارة للذكاء الاصطناعي لاستخراج البيانات التقنية والحالة.
        """
        
        # البرومبت المطور لضمان دقة التحليل المالي والتقني
        prompt = f"""
        You are a SENIOR automotive expert with 20+ years of experience identifying cars.
        Your specialty is distinguishing between similar-looking vehicles from different brands.
        
        CRITICAL IDENTIFICATION RULES:
        1. CAREFULLY examine the car badge/logo - zoom in mentally on:
           - Front grille emblem
           - Rear boot/trunk badge
           - Steering wheel logo (if interior visible)
           - Wheel center caps
        
        2. PAY SPECIAL ATTENTION to distinguishing these similar brands:
           - Volkswagen vs Skoda vs Seat (all VW Group - different logos!)
           - Toyota vs Lexus
           - Nissan vs Infiniti
           - Honda vs Acura
           - Hyundai vs Kia vs Genesis
        
        3. LOOK FOR model-specific features:
           - Tail light shapes (unique per model)
           - Grille design patterns
           - Body proportions and silhouette
           - Door handle styles
        
        Analyze this car image and provide a detailed report in {user_lang}.
        
        Extract the following information and return it ONLY as a JSON object:
        1. brand: (MUST be accurate - check logo carefully! e.g., Skoda, not VW if it's a Skoda)
        2. model: (e.g., Fabia, Golf, Octavia - be specific)
        3. manufacture_year: (Estimate based on model generation face-lift features)
        4. car_type: (Choose from: sedan, suv, coupe, hybrid, electric, pickup, hatchback, wagon)
        5. condition_score: (A float between 0.1 and 1.0, where 1.0 is showroom condition)
        6. detected_damages: (List of visible issues like scratches, dents, or 'None')
        7. color: (Visible exterior color)
        8. summary: (A brief professional assessment of the vehicle)
        9. brand_confidence: (Float 0.0-1.0 - how certain are you about the brand identification?)
        10. identification_clues: (What visual evidence led to your brand/model identification?)

        Rules:
        - Be VERY careful about brand identification - double-check the logo!
        - If image quality is poor or logo not visible, set brand_confidence low
        - Be objective about the condition_score. 
        - If the image is not a car, return {{"error": "Not a vehicle"}}.
        - Use exactly the JSON keys provided.
        """

        try:
            # تحويل الصورة إلى Base64
            base64_image = self._encode_image(image_bytes)

            # طلب التحليل من نموذج Vision
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
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
                # تفعيل نمط JSON لضمان استقرار استخراج البيانات
                response_format={"type": "json_object"},
                temperature=0.2 # درجة حرارة منخفضة لضمان دقة الحقائق التقنية
            )

            # معالجة الرد
            raw_content = response.choices[0].message.content
            analysis_result = self._parse_json_response(raw_content)

            if self.logger:
                self.logger.info(f"🚗 Analysis Complete: {analysis_result.get('brand')} {analysis_result.get('model')}")

            return analysis_result

        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ AI Analysis Failed: {str(e)}")
            return {"error": "فشل الاتصال بمحرك التحليل", "details": str(e)}

    def quick_validate_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        تحقق سريع من أن الصورة تحتوي على سيارة قبل إجراء التحليل المكلف.
        """
        try:
            base64_image = self._encode_image(image_bytes)
            prompt = "Is there a vehicle (car, truck, motorcycle) visible in this image? Ignore if it is on a screen or digital display. Answer JSON: {\"is_valid\": boolean, \"message\": \"short reason\"}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                        ],
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.0,
                max_tokens=50
            )
            return self._parse_json_response(response.choices[0].message.content)
        except Exception as e:
            # في حالة الفشل، نفترض أنها صالحة لنسمح بالتحليل الكامل
            if self.logger: self.logger.warning(f"Quick validation failed: {e}")
            return {"is_valid": True, "message": "Skipped validation"}

    def analyze_car_from_multiple_angles(self, images_dict: Dict[str, bytes]) -> Dict[str, Any]:
        """
        تحليل شامل باستخدام صور متعددة (أمامية، جانبية، داخلية)
        """
        try:
            # 1. تجهيز الرسالة بالمحتوى المتعدد
            messages_content = []
            
            # إضافة وصف النص
            prompt = """
            Analyze these car images (Front, Side, Interior) and provide a comprehensive report used for official dealer appraisal.
            
            Synthesize information from all angles to determine:
            1. estimated_brand: (Best guess based on logos/grille)
            2. estimated_model: (Model name)
            3. manufacture_year: (Estimate range)
            4. estimated_type: (Choose from: sedan, suv, coupe, hybrid, electric, pickup)
            5. color: (Dominant color)
            6. doors: (Number of doors, e.g., 2, 4, 5)
            7. fuel_type: (Infer from fuel cap/exhaust/badges: Benzin, Diesel, Hybrid, Elektro)
            8. engine_cylinders: (Estimate based on model: 3, 4, 6, 8, 12, or 'Unknown')
            9. engine_displacement_cc: (Estimate based on model trim, e.g., 2000, 3000, or 'Unknown')
            10. engine_horsepower: (Estimate based on model specs, e.g., 150, 300, or 'Unknown')
            11. transmission: (Automatic, Manual)
            12. drivetrain: (FWD, RWD, AWD, 4WD)
            13. seats: (Number of seats, e.g., 2, 4, 5, 7)
            14. estimated_trim: (e.g., M Sport, AMG, S-Line, LE, XLE, or 'Standard')
            15. interior_type: (Leather, Fabric, Alcantara)
            16. interior_color: (Black, Beige, Red, Grey)
            17. features: (List of visible features: Sunroof, LED Lights, Navigation, Alloy Wheels, Leather Seats, etc.)
            18. exterior_condition: (Excellent, Good, Fair, Poor - based on scratches/dents)
            19. interior_condition: (Clean, Worn, Damaged - if interior image exists)
            20. visible_damage: (List of specific damages found on any image, or ['None'])
            21. estimated_price_range: {{"min": number, "max": number}} (In Euro, based on market value)
            22. confidence: (Float 0.0 to 1.0, how sure are you about the model?)
            23. success: true (Always true if analysis works)

            Return ONLY valid JSON.
            """
            messages_content.append({"type": "text", "text": prompt})

            # إضافة الصور المتاحة
            for label, img_bytes in images_dict.items():
                if img_bytes:
                    base64_img = self._encode_image(img_bytes)
                    messages_content.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_img}",
                            "detail": "high"
                        }
                    })

            # 2. إرسال الطلب
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": messages_content}],
                response_format={"type": "json_object"},
                temperature=0.3
            )

            # 3. معالجة النتيجة
            return self._parse_json_response(response.choices[0].message.content)

        except Exception as e:
            if self.logger: self.logger.error(f"Multi-angle analysis failed: {e}")
            return {"success": False, "error": str(e)}

    def identify_damage_areas(self, image_bytes: bytes) -> str:
        """وظيفة مخصصة لوصف الأضرار بشكل إنشائي مفصل (اختياري)"""
        # يمكن استخدامها في التقارير المطولة التي تسبق الفاتورة
        prompt = "Describe only the physical damages or wear and tear visible on this car in detail."
        # ... (تنفيذ مشابه للدالة أعلاه)
        pass