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
        # معدّلة بناءً على معايير السوق الألماني
        self.w_condition = 0.50  # وزن الحالة الفنية
        self.w_mileage = 0.35    # وزن الممشى (الاستهلاك الميكانيكي) - الأهم!
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
        # معتمد على معايير السوق الألماني (تدريجي)
        mileage = int(analysis_data.get('mileage', 50000))
        if mileage < 30000:
            m = 0.95  # سيارة شبه جديدة
        elif mileage < 60000:
            m = max(0.65, 1.0 - ((mileage - 30000) / 300000))
        elif mileage < 120000:
            m = max(0.40, 0.65 - ((mileage - 60000) * 0.000012))
        elif mileage < 200000:
            m = max(0.20, 0.40 - ((mileage - 120000) * 0.000020))
        else:
            m = 0.15  # ممشى مرتفع جداً

        # 4. حساب معامل العمر (Age Factor - A)
        # معتمد على معايير السوق الألماني (خسارة 25% السنة الأولى، 50% بعد 3 سنوات)
        year = int(analysis_data.get('manufacture_year', self.current_year))
        age = max(0, self.current_year - year)
        if age == 0:
            a = 1.0  # سيارة جديدة
        elif age == 1:
            a = 0.75  # خسارة 25% في السنة الأولى
        elif age <= 3:
            a = max(0.50, 0.75 - ((age - 1) * 0.125))  # 50% بعد 3 سنوات
        elif age <= 5:
            a = max(0.35, 0.50 - ((age - 3) * 0.075))  # 35% بعد 5 سنوات
        elif age <= 10:
            a = max(0.20, 0.35 - ((age - 5) * 0.03))
        else:
            a = max(0.10, 0.20 - ((age - 10) * 0.02))

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

        # 8. حساب معامل نوع الوقود (Fuel Factor)
        fuel_type = analysis_data.get('fuel_type', 'بنزين')
        fuel_factor = Config.FUEL_FACTORS.get(fuel_type, 1.0)

        # 9. تطبيق المعادلة المرجحة النهائية
        # حساب العامل المرجح الإجمالي (Weighted Factor)
        weighted_factor = (self.w_condition * c) + (self.w_mileage * m) + (self.w_age * a)
        
        # السعر النهائي = الأساسي * المرجح * الماركة * الملاك * الصيانة * التوف * الوقود
        final_price = base_price * weighted_factor * brand_factor * owner_penalty * maintenance_bonus * tuv_factor * fuel_factor

        return round(final_price, 2)

    def get_price_range(self, estimated_price: float) -> tuple:
        """إرجاع نطاق سعري (هامش 5%) لتقديم عرض مرن للعميل"""
        lower_bound = estimated_price * 0.95
        upper_bound = estimated_price * 1.05
        return round(lower_bound, 2), round(upper_bound, 2)