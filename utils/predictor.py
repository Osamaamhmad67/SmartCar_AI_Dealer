"""
utils/predictor.py - محرك تقدير الأسعار الذكي
SmartCar AI-Dealer
تطبيق خوارزمية التسعير المرجح بناءً على تحليل الذكاء الاصطناعي (60/25/15)
"""

from config import Config

class PricePredictor:
    """المسؤول عن حساب السعر النهائي للسيارة بناءً على المعايير الثلاثة المعتمدة"""

    def __init__(self):
        # الأوزان المرجحة المعتمدة في دستور النظام (Weighted Pricing Model)
        self.w_condition = 0.60  # وزن الحالة الفنية
        self.w_mileage = 0.25    # وزن الممشى (الاستهلاك الميكانيكي)
        self.w_age = 0.15        # وزن العمر الزمني
        self.current_year = 2026

    def predict_price(self, analysis_data: dict) -> float:
        """
        حساب السعر التقديري بناءً على البيانات المستخرجة من الصورة والمدخلات.
        المعادلة: Price = BasePrice * (Wc*C + Wm*M + Wa*A) * BrandFactor
        """
        # 1. جلب السعر الأساسي ومعامل الماركة من Config
        car_type = analysis_data.get('car_type', 'sedan')
        brand = analysis_data.get('brand', 'other')

        base_price = Config.get_base_price(car_type)
        brand_factor = Config.get_brand_factor(brand)

        # 2. حساب معامل الحالة (Condition Factor - C)
        # القيمة من 0.1 إلى 1.0 مستخرجة من رؤية الحاسوب
        c = float(analysis_data.get('condition_score', 0.8))

        # 3. حساب معامل الممشى (Mileage Factor - M)
        # نفترض أن العمر الافتراضي للممشى المؤثر هو 250,000 كم
        mileage = int(analysis_data.get('mileage', 50000))
        m = max(0.1, 1 - (mileage / 250000))

        # 4. حساب معامل العمر (Age Factor - A)
        # نفترض أن تأثير العمر يضمحل بشكل كبير بعد 15 سنة
        year = int(analysis_data.get('manufacture_year', self.current_year))
        age = max(0, self.current_year - year)
        a = max(0.1, 1 - (age / 15))

        # 5. حساب معامل الملاك (Owners Factor)
        # خصم 2% لكل مالك إضافي بعد الأول
        owners = int(analysis_data.get('owners', 1))
        owner_penalty = max(0.7, 1.0 - (max(0, owners - 1) * 0.02))

        # 6. حساب معامل الصيانة (Maintenance Factor)
        # زيادة 5% للصيانة المنتظمة
        has_maintenance = analysis_data.get('maintenance', False)
        maintenance_bonus = 1.05 if has_maintenance else 1.0

        # 7. حساب معامل التوف (TÜV Factor)
        # +2% إذا أكثر من سنة، -3% إذا أقل من 3 شهور
        tuv_months = int(analysis_data.get('tuv_months', 12))
        tuv_factor = 1.0
        if tuv_months > 12:
            tuv_factor = 1.02
        elif tuv_months < 3:
            tuv_factor = 0.97

        # 8. تطبيق المعادلة المرجحة النهائية
        # حساب العامل المرجح الإجمالي (Weighted Factor)
        weighted_factor = (self.w_condition * c) + (self.w_mileage * m) + (self.w_age * a)
        
        # السعر النهائي = الأساسي * المرجح * الماركة * الملاك * الصيانة * التوف
        final_price = base_price * weighted_factor * brand_factor * owner_penalty * maintenance_bonus * tuv_factor

        return round(final_price, 2)

    def get_price_range(self, estimated_price: float) -> tuple:
        """إرجاع نطاق سعري (هامش 5%) لتقديم عرض مرن للعميل"""
        lower_bound = estimated_price * 0.95
        upper_bound = estimated_price * 1.05
        return round(lower_bound, 2), round(upper_bound, 2)