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
        You are an EXPERT automotive forensic analyst specializing in brand identification.
        
        ⚠️ MANDATORY FIRST STEP - LOGO ANALYSIS ⚠️
        Before identifying the brand, you MUST first describe what you see in the logo/emblem:
        - What shape is the logo? (circle, oval, wings, letters, animal, etc.)
        - What symbols or letters are visible?
        - What color is the emblem?
        
        🔴 CRITICAL: VW GROUP BRAND DIFFERENTIATION 🔴
        These brands look similar but have COMPLETELY DIFFERENT LOGOS:
        
        | Brand      | Logo Description                                           |
        |------------|-----------------------------------------------------------|
        | SKODA      | Green/Silver WINGED ARROW pointing right (like a bird)   |
        | Volkswagen | VW letters inside a CIRCLE                                |
        | SEAT       | Silver 'S' letter or stylized SEAT text                   |
        | Audi       | Four overlapping RINGS                                    |
        
        🔴 SKODA FABIA vs VW GOLF - KEY DIFFERENCES 🔴
        - Skoda Fabia: More angular headlights, SKODA text on rear
        - Skoda Fabia: Winged arrow emblem on grille and steering wheel
        - VW Golf: Rounded headlights, VW badge on grille
        - If you see a WINGED ARROW logo, it is SKODA, NOT VW!
        
        Analyze this car image and provide a detailed report in {user_lang}.
        
        Extract the following information and return it ONLY as a JSON object:
        1. logo_description: (MANDATORY - Describe what you see in the logo/emblem FIRST)
        2. brand: (Based ONLY on the logo you described above)
        3. model: (e.g., Fabia, Golf, Octavia - be specific)
        4. manufacture_year: (Estimate based on model generation)
        5. car_type: (sedan, suv, coupe, hybrid, electric, pickup, hatchback, wagon)
        6. condition_score: (Float 0.1-1.0, where 1.0 is showroom condition)
        7. detected_damages: (List of visible issues or 'None')
        8. color: (Visible exterior color)
        9. summary: (Brief professional assessment)
        10. brand_confidence: (Float 0.0-1.0 - how certain about brand?)
        11. detected_equipment: (List of ONLY the equipment you can VISUALLY CONFIRM from the image. Use ONLY these exact keys:
            "leather", "navigation", "sunroof", "panoramic_roof", "heated_seats", "ventilated_seats",
            "parking_sensors", "parking_camera", "camera_360", "led_headlights", "xenon_headlights", "matrix_led",
            "adaptive_cruise", "lane_assist", "blind_spot", "auto_parking",
            "auto_climate", "dual_climate", "sport_package", "amg_package", "m_package", "s_line",
            "apple_carplay", "android_auto", "wireless_charging", "heads_up_display",
            "keyless_entry", "ambient_lighting", "harman_kardon", "bose_sound", "burmester_sound",
            "tow_hook", "roof_rack", "winter_tires", "spare_key"
            IMPORTANT: Only include items you can SEE evidence of in the photo. Look for:
            - Badges/logos: AMG, M, S-Line, BOSE, Harman Kardon, Burmester
            - Exterior: LED/Xenon lights, sunroof, panoramic roof, roof rack, tow hook, parking sensors
            - Interior: leather seats, navigation screen, ambient lighting, dual climate controls
            Return empty list [] if nothing is visible.)

        🚨 VALIDATION RULES 🚨
        - If logo_description mentions "wing" or "arrow" → brand MUST be "Skoda"
        - If logo_description mentions "VW" or "letters in circle" → brand MUST be "Volkswagen"
        - If you cannot see the logo clearly, set brand_confidence below 0.5
        - If the image is not a car, return {{"error": "Not a vehicle"}}
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
                temperature=0.1 # درجة حرارة منخفضة جداً لضمان دقة أكبر
            )

            # معالجة الرد
            raw_content = response.choices[0].message.content
            analysis_result = self._parse_json_response(raw_content)
            
            # 🔧 POST-PROCESSING: تصحيح الماركة بناءً على وصف الشعار
            analysis_result = self._validate_and_correct_brand(analysis_result)

            if self.logger:
                self.logger.info(f"[CAR] Analysis Complete: {analysis_result.get('brand')} {analysis_result.get('model')}")

            return analysis_result

        except Exception as e:
            if self.logger:
                self.logger.error(f"[ERROR] AI Analysis Failed: {str(e)}")
            return {"error": "فشل الاتصال بمحرك التحليل", "details": str(e)}
    
    def _validate_and_correct_brand(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        تصحيح الماركة تلقائياً بناءً على وصف الشعار
        """
        logo_desc = result.get('logo_description', '').lower()
        current_brand = result.get('brand', '').lower()
        
        # إذا وصف الشعار يحتوي على "wing" أو "arrow" → Skoda
        skoda_keywords = ['wing', 'arrow', 'winged', 'bird', 'flying', 'skoda']
        vw_keywords = ['vw', 'volkswagen', 'circle', 'letters']
        
        for keyword in skoda_keywords:
            if keyword in logo_desc:
                if current_brand in ['volkswagen', 'vw']:
                    result['brand'] = 'Skoda'
                    result['model'] = result.get('model', '').replace('Golf', 'Fabia').replace('Polo', 'Fabia')
                    result['brand_corrected'] = True
                    if self.logger:
                        self.logger.info(f"[FIX] Brand corrected: VW -> Skoda (logo: {logo_desc[:50]})")
                break
        
        # إذا وصف الشعار يحتوي على "VW" → Volkswagen
        for keyword in vw_keywords:
            if keyword in logo_desc and 'skoda' not in logo_desc:
                if current_brand == 'skoda':
                    result['brand'] = 'Volkswagen'
                    result['brand_corrected'] = True
                    if self.logger:
                        self.logger.info(f"[FIX] Brand corrected: Skoda -> VW (logo: {logo_desc[:50]})")
                break
        
        return result

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
            24. detected_equipment: (List of equipment VISUALLY CONFIRMED from ALL images. Use ONLY these exact keys:
                "leather", "navigation", "sunroof", "panoramic_roof", "heated_seats", "ventilated_seats",
                "parking_sensors", "parking_camera", "camera_360", "led_headlights", "xenon_headlights", "matrix_led",
                "adaptive_cruise", "lane_assist", "blind_spot", "auto_parking",
                "auto_climate", "dual_climate", "sport_package", "amg_package", "m_package", "s_line",
                "apple_carplay", "android_auto", "wireless_charging", "heads_up_display",
                "keyless_entry", "ambient_lighting", "harman_kardon", "bose_sound", "burmester_sound",
                "tow_hook", "roof_rack", "winter_tires", "spare_key"
                LOOK FOR: badges (AMG/M/S-Line/BOSE/Burmester), LED headlights, sunroof, panoramic roof,
                leather interior, navigation screen, ambient lighting, roof rack, tow hook, dual climate knobs,
                parking sensors on bumper, keyless start button. Return [] if nothing confirmed.)

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