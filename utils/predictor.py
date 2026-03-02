"""
utils/predictor.py - محرك تقدير الأسعار المتقدم
SmartCar AI-Dealer
نظام تسعير شامل يعتمد على 30+ عامل مؤثر في قيمة السيارة
يدعم السيارات الجديدة والمستعملة - متوافق مع معايير السوق الألماني (DAT/Schwacke)
"""

from config import Config

class PricePredictor:
    """محرك التسعير المتقدم - يدمج جميع العوامل المؤثرة في قيمة السيارة"""

    def __init__(self):
        # الأوزان المرجحة الأساسية (Weighted Pricing Model)
        self.w_condition = 0.50  # وزن الحالة الفنية
        self.w_mileage = 0.35   # وزن الممشى
        self.w_age = 0.15       # وزن العمر الزمني
        self.current_year = 2026

    def predict_price(self, analysis_data: dict) -> float:
        """
        حساب السعر التقديري الشامل بناءً على جميع العوامل المتاحة.
        
        المعادلة المتقدمة:
        Price = BasePrice × WeightedCore × BrandF × FuelF × TransF × DriveF 
                × ColorF × EmissionsF × EngineSizeF × HorsepowerF 
                × OwnerF × MaintenanceF × TÜVF × WarrantyF 
                × AccidentF × ServiceBookF × EquipmentBonus
        
        العوامل غير المتوفرة تأخذ القيمة الافتراضية 1.0 (لا تأثير)
        """
        # ======= المرحلة 1: البيانات الأساسية =======
        car_type = analysis_data.get('car_type', 'sedan')
        brand = analysis_data.get('brand', 'other')

        base_price = Config.get_base_price(car_type)
        brand_factor = Config.get_brand_factor(brand)

        # ======= المرحلة 2: النواة المرجحة (Condition + Mileage + Age) =======
        
        # 2A. معامل الحالة (Condition Factor - C)
        c = float(analysis_data.get('condition_score', 0.8))

        # 2B. معامل الممشى (Mileage Factor - M)
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

        # 2C. معامل العمر (Age Factor - A)
        year = int(analysis_data.get('manufacture_year', self.current_year))
        age = max(0, self.current_year - year)
        if age == 0:
            a = 1.0   # سيارة جديدة
        elif age == 1:
            a = 0.75  # خسارة 25% في السنة الأولى
        elif age <= 3:
            a = max(0.50, 0.75 - ((age - 1) * 0.125))
        elif age <= 5:
            a = max(0.35, 0.50 - ((age - 3) * 0.075))
        elif age <= 10:
            a = max(0.20, 0.35 - ((age - 5) * 0.03))
        else:
            a = max(0.10, 0.20 - ((age - 10) * 0.02))

        # النواة المرجحة
        weighted_core = (self.w_condition * c) + (self.w_mileage * m) + (self.w_age * a)

        # ======= المرحلة 3: المعاملات الإضافية (Additional Factors) =======

        # 3A. معامل الملاك (Owners Factor) — خصم 2% لكل مالك إضافي
        owners = int(analysis_data.get('owners', 1))
        owner_penalty = max(0.7, 1.0 - (max(0, owners - 1) * 0.02))

        # 3B. معامل الصيانة (Maintenance Factor) — +5% للصيانة المنتظمة
        has_maintenance = analysis_data.get('maintenance', False)
        maintenance_bonus = 1.05 if has_maintenance else 1.0

        # 3C. معامل التوف (TÜV Factor)
        tuv_months = int(analysis_data.get('tuv_months', 12))
        tuv_factor = 1.0
        if tuv_months > 12:
            tuv_factor = 1.02
        elif tuv_months < 3:
            tuv_factor = 0.97

        # 3D. معامل نوع الوقود (Fuel Factor)
        fuel_type = analysis_data.get('fuel_type', '')
        fuel_factor = Config.get_factor(Config.FUEL_FACTORS, fuel_type) if fuel_type else 1.0

        # ======= المرحلة 4: المعاملات الجديدة المتقدمة =======

        # 4A. ناقل الحركة (Transmission)
        transmission = analysis_data.get('transmission', '')
        transmission_factor = Config.get_transmission_factor(transmission) if transmission else 1.0

        # 4B. نظام الدفع (Drivetrain)
        drivetrain = analysis_data.get('drivetrain', '')
        drivetrain_factor = Config.get_drivetrain_factor(drivetrain) if drivetrain else 1.0

        # 4C. اللون (Color)
        color = analysis_data.get('color', '')
        color_factor = Config.get_color_factor(color) if color else 1.0

        # 4D. فئة الانبعاثات (Emissions Class)
        emissions = analysis_data.get('emissions_class', '')
        emissions_factor = Config.get_emissions_factor(emissions) if emissions else 1.0

        # 4E. حجم المحرك (Engine Size CC)
        engine_cc = int(analysis_data.get('engine_cc', 0))
        engine_size_factor = Config.get_engine_size_factor(engine_cc) if engine_cc > 0 else 1.0

        # 4F. قوة المحرك (Horsepower)
        horsepower = int(analysis_data.get('horsepower', 0))
        hp_factor = Config.get_horsepower_factor(horsepower) if horsepower > 0 else 1.0

        # 4G. تاريخ الحوادث (Accident History)
        accident = analysis_data.get('accident_history', '')
        accident_factor = Config.get_accident_factor(accident) if accident else 1.0

        # 4H. الضمان المتبقي (Remaining Warranty)
        warranty = analysis_data.get('warranty', '')
        warranty_factor = Config.get_warranty_factor(warranty) if warranty else 1.0

        # 4I. دفتر الصيانة (Service Book)
        service_book = analysis_data.get('service_book', '')
        service_book_factor = Config.get_service_book_factor(service_book) if service_book else 1.0

        # 4J. التجهيزات الإضافية (Equipment Bonuses)
        equipment = analysis_data.get('equipment', [])
        equipment_bonus = Config.calculate_equipment_bonus(equipment) if equipment else 1.0

        # ======= المرحلة 5: المعادلة النهائية =======
        final_price = (
            base_price
            * weighted_core
            * brand_factor
            * fuel_factor
            * transmission_factor
            * drivetrain_factor
            * color_factor
            * emissions_factor
            * engine_size_factor
            * hp_factor
            * owner_penalty
            * maintenance_bonus
            * tuv_factor
            * warranty_factor
            * accident_factor
            * service_book_factor
            * equipment_bonus
        )

        return round(final_price, 2)

    def get_price_range(self, estimated_price: float) -> tuple:
        """إرجاع نطاق سعري (هامش 5%) لتقديم عرض مرن للعميل"""
        lower_bound = estimated_price * 0.95
        upper_bound = estimated_price * 1.05
        return round(lower_bound, 2), round(upper_bound, 2)

    def get_price_breakdown(self, analysis_data: dict) -> dict:
        """
        إرجاع تفاصيل حساب السعر لعرضها للعميل أو المسؤول.
        يوضح تأثير كل عامل بشكل منفصل.
        """
        car_type = analysis_data.get('car_type', 'sedan')
        brand = analysis_data.get('brand', 'other')
        base_price = Config.get_base_price(car_type)
        
        breakdown = {
            "base_price": base_price,
            "brand": brand,
            "brand_factor": Config.get_brand_factor(brand),
            "car_type": car_type,
        }

        # إضافة كل العوامل المتوفرة
        factor_map = {
            "transmission": ("transmission", Config.get_transmission_factor),
            "drivetrain": ("drivetrain", Config.get_drivetrain_factor),
            "color": ("color", Config.get_color_factor),
            "emissions_class": ("emissions_class", Config.get_emissions_factor),
            "accident_history": ("accident_history", Config.get_accident_factor),
            "warranty": ("warranty", Config.get_warranty_factor),
            "service_book": ("service_book", Config.get_service_book_factor),
        }

        for data_key, (display_key, getter) in factor_map.items():
            value = analysis_data.get(data_key, '')
            if value:
                breakdown[f"{display_key}_value"] = value
                breakdown[f"{display_key}_factor"] = getter(value)

        # العوامل العددية
        engine_cc = int(analysis_data.get('engine_cc', 0))
        if engine_cc > 0:
            breakdown["engine_cc"] = engine_cc
            breakdown["engine_size_factor"] = Config.get_engine_size_factor(engine_cc)

        horsepower = int(analysis_data.get('horsepower', 0))
        if horsepower > 0:
            breakdown["horsepower"] = horsepower
            breakdown["horsepower_factor"] = Config.get_horsepower_factor(horsepower)

        # التجهيزات
        equipment = analysis_data.get('equipment', [])
        if equipment:
            breakdown["equipment_list"] = equipment
            breakdown["equipment_bonus"] = Config.calculate_equipment_bonus(equipment)

        # السعر النهائي
        breakdown["final_price"] = self.predict_price(analysis_data)
        low, high = self.get_price_range(breakdown["final_price"])
        breakdown["price_range"] = {"low": low, "high": high}

        return breakdown