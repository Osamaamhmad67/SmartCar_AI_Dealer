"""
utils/invoice_generator.py - مولد الفواتير المالية الاحترافية
SmartCar AI-Dealer
توليد تقارير PDF تشمل تفاصيل السيارة، السعر التقديري، والضريبة
"""

import os
import json
from datetime import datetime
from pathlib import Path
from fpdf import FPDF
from config import Config
from .general_utils import GeneralUtils
import streamlit as st
from .i18n import t, get_direction

# Arabic RTL text fix
import arabic_reshaper
from bidi.algorithm import get_display

def fix_arabic(text):
    """تصحيح النص العربي للعرض الصحيح في PDF - مع عكس الاتجاه"""
    if text is None:
        return ""
    text = str(text)
    # Check if text contains Arabic characters
    if any('\u0600' <= c <= '\u06FF' for c in text):
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    return text

def reshape_arabic_only(text):
    """إعادة تشكيل النص العربي فقط - بدون عكس الاتجاه (للخطوط التي تدعم العربية)"""
    if text is None:
        return ""
    text = str(text)
    # Check if text contains Arabic characters
    if any('\u0600' <= c <= '\u06FF' for c in text):
        return arabic_reshaper.reshape(text)
    return text

# قاموس ترجمة القيم الشائعة
TRANSLATIONS = {
    # Nationality / الجنسية
    'ألماني': {'en': 'German', 'de': 'Deutsch', 'ar': 'ألماني'},
    'ألمانية': {'en': 'German', 'de': 'Deutsch', 'ar': 'ألمانية'},
    'Deutsch': {'en': 'German', 'de': 'Deutsch', 'ar': 'ألماني'},
    'German': {'en': 'German', 'de': 'Deutsch', 'ar': 'ألماني'},
    'سوري': {'en': 'Syrian', 'de': 'Syrisch', 'ar': 'سوري'},
    'سورية': {'en': 'Syrian', 'de': 'Syrisch', 'ar': 'سورية'},
    'Syrian': {'en': 'Syrian', 'de': 'Syrisch', 'ar': 'سوري'},
    'عراقي': {'en': 'Iraqi', 'de': 'Irakisch', 'ar': 'عراقي'},
    'Iraqi': {'en': 'Iraqi', 'de': 'Irakisch', 'ar': 'عراقي'},
    'لبناني': {'en': 'Lebanese', 'de': 'Libanesisch', 'ar': 'لبناني'},
    'Lebanese': {'en': 'Lebanese', 'de': 'Libanesisch', 'ar': 'لبناني'},
    'مصري': {'en': 'Egyptian', 'de': 'Ägyptisch', 'ar': 'مصري'},
    'Egyptian': {'en': 'Egyptian', 'de': 'Ägyptisch', 'ar': 'مصري'},
    'تركي': {'en': 'Turkish', 'de': 'Türkisch', 'ar': 'تركي'},
    'Turkish': {'en': 'Turkish', 'de': 'Türkisch', 'ar': 'تركي'},
    
    # License Type / نوع الرخصة
    'رخصة': {'en': 'License', 'de': 'Führerschein', 'ar': 'رخصة'},
    'رخصة قيادة': {'en': 'Driving License', 'de': 'Führerschein', 'ar': 'رخصة قيادة'},
    'رخصة سيارة': {'en': 'Car License', 'de': 'PKW-Führerschein', 'ar': 'رخصة سيارة'},
    'License': {'en': 'License', 'de': 'Führerschein', 'ar': 'رخصة'},
    'Führerschein': {'en': 'Driving License', 'de': 'Führerschein', 'ar': 'رخصة قيادة'},
    'B': {'en': 'B', 'de': 'B', 'ar': 'B'},
    'A': {'en': 'A', 'de': 'A', 'ar': 'A'},
    
    # Condition / الحالة
    'ممتازة': {'en': 'Excellent', 'de': 'Ausgezeichnet', 'ar': 'ممتازة'},
    'جيدة جداً': {'en': 'Very Good', 'de': 'Sehr Gut', 'ar': 'جيدة جداً'},
    'جيدة': {'en': 'Good', 'de': 'Gut', 'ar': 'جيدة'},
    'مقبولة': {'en': 'Acceptable', 'de': 'Akzeptabel', 'ar': 'مقبولة'},
    'Excellent': {'en': 'Excellent', 'de': 'Ausgezeichnet', 'ar': 'ممتازة'},
    'Very Good': {'en': 'Very Good', 'de': 'Sehr Gut', 'ar': 'جيدة جداً'},
    'Good': {'en': 'Good', 'de': 'Gut', 'ar': 'جيدة'},
    'Acceptable': {'en': 'Acceptable', 'de': 'Akzeptabel', 'ar': 'مقبولة'},
    
    # Fuel Type / نوع الوقود
    'بنزين': {'en': 'Petrol', 'de': 'Benzin', 'ar': 'بنزين'},
    'ديزل': {'en': 'Diesel', 'de': 'Diesel', 'ar': 'ديزل'},
    'كهربائي': {'en': 'Electric', 'de': 'Elektrisch', 'ar': 'كهربائي'},
    'هجين': {'en': 'Hybrid', 'de': 'Hybrid', 'ar': 'هجين'},
    'Petrol': {'en': 'Petrol', 'de': 'Benzin', 'ar': 'بنزين'},
    'Benzin': {'en': 'Petrol', 'de': 'Benzin', 'ar': 'بنزين'},
    'Diesel': {'en': 'Diesel', 'de': 'Diesel', 'ar': 'ديزل'},
    'Electric': {'en': 'Electric', 'de': 'Elektrisch', 'ar': 'كهربائي'},
    'Hybrid': {'en': 'Hybrid', 'de': 'Hybrid', 'ar': 'هجين'},
    
    # Colors / الألوان
    'أسود': {'en': 'Black', 'de': 'Schwarz', 'ar': 'أسود'},
    'أبيض': {'en': 'White', 'de': 'Weiß', 'ar': 'أبيض'},
    'فضي': {'en': 'Silver', 'de': 'Silber', 'ar': 'فضي'},
    'رمادي': {'en': 'Gray', 'de': 'Grau', 'ar': 'رمادي'},
    'أحمر': {'en': 'Red', 'de': 'Rot', 'ar': 'أحمر'},
    'أزرق': {'en': 'Blue', 'de': 'Blau', 'ar': 'أزرق'},
    'Black': {'en': 'Black', 'de': 'Schwarz', 'ar': 'أسود'},
    'White': {'en': 'White', 'de': 'Weiß', 'ar': 'أبيض'},
    'Silver': {'en': 'Silver', 'de': 'Silber', 'ar': 'فضي'},
    'Gray': {'en': 'Gray', 'de': 'Grau', 'ar': 'رمادي'},
    'Grey': {'en': 'Gray', 'de': 'Grau', 'ar': 'رمادي'},
    'Red': {'en': 'Red', 'de': 'Rot', 'ar': 'أحمر'},
    'Blue': {'en': 'Blue', 'de': 'Blau', 'ar': 'أزرق'},
}

def translate_value(value, target_lang='en'):
    """ترجمة قيمة إلى اللغة المطلوبة"""
    if not value or value == 'N/A':
        return value
    
    value_str = str(value).strip()
    
    if value_str in TRANSLATIONS:
        return TRANSLATIONS[value_str].get(target_lang, value_str)
    
    return value_str


class ContractPDF(FPDF):
    """فئة PDF مخصصة للعقود مع ترقيم الصفحات"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font_name = "Arial"
    
    def footer(self):
        """إضافة ترقيم الصفحات في أسفل كل صفحة"""
        self.set_y(-10)
        self.set_font(self.font_name, '', 8)
        self.set_text_color(128, 128, 128)
        # Page X of Y
        page_text = f"Page {self.page_no()}/{{nb}}"
        self.cell(0, 10, page_text, 0, 0, 'C')


class InvoiceGenerator:
    """مسؤول عن تحويل بيانات المعاملات إلى وثائق PDF رسمية"""

    def __init__(self):
        self.output_dir = Config.INVOICES_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        # مسارات الخطوط لدعم اللغة العربية (إذا توفرت)
        self.font_path = str(Config.FONTS_DIR / Config.FONT_REGULAR)
        self.font_bold_path = str(Config.FONTS_DIR / Config.FONT_BOLD)
        
        # Fallback to Windows Arial if Cairo is missing
        if not os.path.exists(self.font_path):
            if os.path.exists("C:/Windows/Fonts/arial.ttf"):
                self.font_path = "C:/Windows/Fonts/arial.ttf"
                self.font_bold_path = "C:/Windows/Fonts/arialbd.ttf"
            else:
                self.font_path = None # Will rely on standard font and sanitization

    def generate_car_invoice(self, transaction_data: dict, user_data: dict, lang='Deutsch') -> str:
        """
        إنشاء فاتورة تقييم سيارة
        :param transaction_data: بيانات السيارة والسعر
        :param user_data: بيانات العميل أو الموظف
        :param lang: لغة الفاتورة
        :return: المسار الكامل لملف PDF الناتج
        """
        invoice_id = f"INV-{datetime.now().strftime('%Y%m%d')}-{transaction_data.get('id', '000')}"
        filename = f"{invoice_id}.pdf"
        file_path = self.output_dir / filename

        pdf = FPDF()
        pdf.add_page()
        
        # Add Unicode font
        font_name = "Arial" # Default standard
        if self.font_path and os.path.exists(self.font_path):
            try:
                # Note: fpdf (v1.7.x) uses add_font(family, style, fname, uni=True)
                # But sometimes it's better to give it a custom name to avoid conflict
                pdf.add_font('CustomArial', '', self.font_path, uni=True)
                pdf.add_font('CustomArial', 'B', self.font_bold_path, uni=True)
                font_name = 'CustomArial'
            except Exception as e:
                print(f"Font loading error: {e}")
        
        # إعداد الألوان (أسود وذهبي للبراند)
        pdf.set_fill_color(200, 160, 0) # لون ذهبي خفيف للترويسة
        
        # 1. الترويسة (Header)
        pdf.set_font(font_name, 'B', 16)
        pdf.cell(0, 10, Config.APP_NAME, ln=True, align='C')
        pdf.set_font(font_name, '', 10)
        pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='R')
        pdf.line(10, 30, 200, 30)

        # 2. بيانات العميل (Client Info)
        pdf.ln(10)
        pdf.set_font(font_name, 'B', 12)
        pdf.cell(0, 10, "Client Information / Kundeninformationen:", ln=True)
        pdf.set_font(font_name, '', 11)
        client_name = user_data.get('full_name', 'Guest User')
        pdf.cell(0, 8, f"Name: {fix_arabic(client_name)}", ln=True)
        pdf.cell(0, 8, f"Username: {user_data.get('username', 'N/A')}", ln=True)

        # 3. تفاصيل السيارة (Car Details)
        pdf.ln(5)
        pdf.set_font(font_name, 'B', 12)
        pdf.cell(0, 10, "Vehicle Details / Fahrzeugdetails:", ln=True, fill=True)
        pdf.set_font(font_name, '', 11)
        
        details = [
            ("Brand / Marke", transaction_data.get('brand', 'Unknown')),
            ("Model / Modell", transaction_data.get('model', 'Unknown')),
            ("Year / Baujahr", str(transaction_data.get('manufacture_year', 'N/A'))),
            ("Mileage / KM-Stand", f"{transaction_data.get('mileage', 0):,} km"),
            ("Condition / Zustand", transaction_data.get('condition_analysis', 'Standard'))
        ]

        for label, value in details:
            pdf.cell(50, 8, f"{label}:", border=0)
            pdf.cell(0, 8, f"{value}", border=0, ln=True)

        # 4. التفاصيل المالية (Financial Summary)
        pdf.ln(10)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        base_price = float(transaction_data.get('estimated_price', 0))
        vat_amount = base_price * 0.15
        total_price = base_price + vat_amount

        pdf.set_font(font_name, 'B', 12)
        pdf.cell(100, 10, "Description", border=1)
        pdf.cell(0, 10, "Amount", border=1, ln=True, align='C')
        
        pdf.set_font(font_name, '', 11)
        pdf.cell(100, 10, "Estimated Vehicle Value", border=1)
        pdf.cell(0, 10, GeneralUtils.format_currency(base_price, lang), border=1, ln=True, align='R')
        
        pdf.cell(100, 10, "VAT (15%)", border=1)
        pdf.cell(0, 10, GeneralUtils.format_currency(vat_amount, lang), border=1, ln=True, align='R')
        
        pdf.set_font(font_name, 'B', 12)
        pdf.cell(100, 10, "Total Estimated Price", border=1)
        pdf.cell(0, 10, GeneralUtils.format_currency(total_price, lang), border=1, ln=True, align='R')

        # 5. التذييل (Footer)
        pdf.set_y(-30)
        pdf.set_font(font_name, '', 8) # Reduced to regular to avoid missing Italic font crash
        pdf.cell(0, 10, "This is an AI-generated estimation. Prices may vary based on physical inspection.", ln=True, align='C')
        pdf.cell(0, 5, f"Contact: {Config.CONTACT_EMAIL} | Phone: {Config.SUPPORT_PHONE}", align='C')

        pdf.output(str(file_path))
        return str(file_path)

    def generate_contract(self, contract_id, contract_data: dict, user_data: dict, lang: str = 'en') -> str:
        """
        إنشاء عقد PDF شامل يتضمن:
        - بيانات العميل الكاملة (الاسم، الهوية، الجنسية، الهاتف، الرخصة)
        - العنوان الكامل (الشارع، رقم البناء، الرمز البريدي، المدينة)
        - بيانات السيارة بالتفصيل مع الصورة
        - التفاصيل المالية (كاش أو تقسيط، عدد الأقساط، مقدار كل قسط)
        
        lang: اللغة ('ar' للعربية، 'de' للألمانية، 'en' للإنجليزية)
        """
        # قاموس التسميات بثلاث لغات
        labels = {
            'title': {'en': 'Vehicle Purchase Contract', 'de': 'Fahrzeugkaufvertrag', 'ar': 'عقد شراء مركبة'},
            'contract_info': {'en': 'Contract #: {id} | Date: {date}', 'de': 'Vertrag Nr.: {id} | Datum: {date}', 'ar': 'رقم العقد: {id} | التاريخ: {date}'},
            'section_customer': {'en': 'SECTION 1: CUSTOMER INFORMATION', 'de': 'ABSCHNITT 1: KUNDENINFORMATIONEN', 'ar': 'القسم 1: معلومات العميل'},
            'section_vehicle': {'en': 'SECTION 2: VEHICLE DETAILS', 'de': 'ABSCHNITT 2: FAHRZEUGDATEN', 'ar': 'القسم 2: تفاصيل المركبة'},
            'section_financial': {'en': 'SECTION 3: FINANCIAL DETAILS', 'de': 'ABSCHNITT 3: FINANZDATEN', 'ar': 'القسم 3: التفاصيل المالية'},
            'section_terms': {'en': 'SECTION 4: TERMS & CONDITIONS', 'de': 'ABSCHNITT 4: GESCHÄFTSBEDINGUNGEN', 'ar': 'القسم 4: الشروط والأحكام'},
            'section_signature': {'en': 'SECTION 5: SIGNATURES', 'de': 'ABSCHNITT 5: UNTERSCHRIFTEN', 'ar': 'القسم 5: التوقيعات'},
            # Customer fields
            'full_name': {'en': 'Full Name', 'de': 'Vollständiger Name', 'ar': 'الاسم الكامل'},
            'id_number': {'en': 'ID Number', 'de': 'Ausweisnummer', 'ar': 'رقم الهوية'},
            'nationality': {'en': 'Nationality', 'de': 'Staatsangehörigkeit', 'ar': 'الجنسية'},
            'date_of_birth': {'en': 'Date of Birth', 'de': 'Geburtsdatum', 'ar': 'تاريخ الميلاد'},
            'phone': {'en': 'Phone', 'de': 'Telefon', 'ar': 'الهاتف'},
            'email': {'en': 'Email', 'de': 'E-Mail', 'ar': 'البريد الإلكتروني'},
            'address': {'en': 'Address', 'de': 'Adresse', 'ar': 'العنوان'},
            'license_number': {'en': 'License Number', 'de': 'Führerscheinnummer', 'ar': 'رقم الرخصة'},
            'license_type': {'en': 'License Type', 'de': 'Führerscheintyp', 'ar': 'نوع الرخصة'},
            'license_expiry': {'en': 'License Expiry', 'de': 'Führerscheinablauf', 'ar': 'انتهاء الرخصة'},
            # Vehicle fields
            'car_type': {'en': 'Car Type', 'de': 'Fahrzeugtyp', 'ar': 'نوع السيارة'},
            'brand': {'en': 'Brand', 'de': 'Marke', 'ar': 'العلامة التجارية'},
            'model': {'en': 'Model', 'de': 'Modell', 'ar': 'الموديل'},
            'year': {'en': 'Year', 'de': 'Baujahr', 'ar': 'سنة الصنع'},
            'vin': {'en': 'VIN', 'de': 'Fahrgestellnummer', 'ar': 'رقم الهيكل'},
            'plate': {'en': 'Plate Number', 'de': 'Kennzeichen', 'ar': 'رقم اللوحة'},
            'color': {'en': 'Color', 'de': 'Farbe', 'ar': 'اللون'},
            'fuel_type': {'en': 'Fuel Type', 'de': 'Kraftstoffart', 'ar': 'نوع الوقود'},
            'mileage': {'en': 'Mileage', 'de': 'Kilometerstand', 'ar': 'المسافة المقطوعة'},
            'condition': {'en': 'Condition', 'de': 'Zustand', 'ar': 'الحالة'},
            # Financial fields
            'total_price': {'en': 'Total Price', 'de': 'Gesamtpreis', 'ar': 'السعر الإجمالي'},
            'payment_method': {'en': 'Payment Method', 'de': 'Zahlungsmethode', 'ar': 'طريقة الدفع'},
            'down_payment': {'en': 'Down Payment', 'de': 'Anzahlung', 'ar': 'الدفعة المقدمة'},
            'monthly_installment': {'en': 'Monthly Installment', 'de': 'Monatliche Rate', 'ar': 'القسط الشهري'},
            'installment_count': {'en': 'Number of Installments', 'de': 'Anzahl der Raten', 'ar': 'عدد الأقساط'},
            'remaining_amount': {'en': 'Remaining Amount', 'de': 'Restbetrag', 'ar': 'المبلغ المتبقي'},
            # Signature fields
            'buyer_signature': {'en': 'Buyer Signature', 'de': 'Unterschrift Käufer', 'ar': 'توقيع المشتري'},
            'seller_signature': {'en': 'Seller Signature', 'de': 'Unterschrift Verkäufer', 'ar': 'توقيع البائع'},
            'date': {'en': 'Date', 'de': 'Datum', 'ar': 'التاريخ'},
        }
        
        def L(key):
            """الحصول على التسمية باللغة المختارة"""
            return labels.get(key, {}).get(lang, labels.get(key, {}).get('en', key))
        
        filename = f"Contract-{contract_id}-{datetime.now().strftime('%Y%m%d')}.pdf"
        file_path = self.output_dir / filename

        pdf = ContractPDF()
        pdf.alias_nb_pages()  # تفعيل ترقيم الصفحات الإجمالي
        pdf.add_page()
        pdf.set_auto_page_break(True, margin=15)  # زيادة الهامش لترقيم الصفحات
        
        font_name = "Arial"
        if self.font_path and os.path.exists(self.font_path):
            try:
                pdf.add_font('CustomArial', '', self.font_path, uni=True)
                pdf.add_font('CustomArial', 'B', self.font_bold_path, uni=True)
                font_name = 'CustomArial'
            except:
                pass
        pdf.font_name = font_name  # تحديث الخط في فئة ContractPDF
        
        # ===== Header =====
        pdf.set_fill_color(30, 30, 50)
        pdf.rect(0, 0, 210, 35, 'F')
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(font_name, 'B', 20)
        pdf.set_xy(10, 8)
        pdf.cell(0, 12, fix_arabic(L('title')), ln=True, align='C')
        pdf.set_font(font_name, '', 10)
        contract_info = L('contract_info').format(id=contract_id, date=datetime.now().strftime('%Y-%m-%d %H:%M'))
        pdf.cell(0, 8, fix_arabic(contract_info), ln=True, align='C')
        
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)

        
        # ===== Section 1: Customer Information with Full Address =====
        pdf.set_fill_color(79, 172, 254)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(font_name, 'B', 12)
        pdf.cell(0, 10, fix_arabic("  " + L('section_customer')), ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font(font_name, '', 11)
        pdf.ln(3)
        
        # بناء العنوان الكامل
        address_parts = [
            user_data.get('street_name', ''),
            user_data.get('building_number', ''),
            user_data.get('postal_code', ''),
            user_data.get('city', '')
        ]
        full_address = ' - '.join([p for p in address_parts if p]) or user_data.get('address', 'N/A')
        
        customer_fields = [
            (L('full_name'), user_data.get('full_name', 'N/A')),
            (L('id_number'), user_data.get('id_number', 'N/A')),
            (L('nationality'), translate_value(user_data.get('nationality', 'N/A'), lang)),
            (L('date_of_birth'), user_data.get('birth_date', user_data.get('date_of_birth', 'N/A'))),
            (L('phone'), user_data.get('phone', 'N/A')),
            (L('email'), user_data.get('email', 'N/A')),
            (L('address'), full_address),
            (L('license_number'), user_data.get('license_number', 'N/A')),
            (L('license_type'), translate_value(user_data.get('license_type', 'N/A'), lang)),
            (L('license_expiry'), user_data.get('license_expiry', 'N/A')),
        ]
        
        for label, value in customer_fields:
            pdf.cell(60, 6, f"{label}:", border=0)
            pdf.cell(0, 6, fix_arabic(str(value) if value else 'N/A'), border=0, ln=True)
        
        pdf.ln(5)
        
        # ===== Section 2: Vehicle Details with Image =====
        pdf.set_fill_color(67, 233, 123)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(font_name, 'B', 12)
        pdf.cell(0, 10, fix_arabic("  " + L('section_vehicle')), ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font(font_name, '', 11)
        pdf.ln(3)
        
        # صورة السيارة إذا كانت متوفرة
        image_path = contract_data.get('image_path', '')
        if image_path and image_path != 'stored_in_session' and os.path.exists(image_path):
            try:
                pdf.image(image_path, x=140, y=pdf.get_y(), w=60)
            except:
                pass
        
        # Parse condition if it's JSON
        condition_raw = contract_data.get('condition', contract_data.get('condition_analysis', 'Standard'))
        if isinstance(condition_raw, str) and condition_raw.startswith('{'):
            try:
                cond_obj = json.loads(condition_raw)
                condition_val = cond_obj.get('condition', 'Standard')
            except:
                condition_val = 'Standard'
        else:
            condition_val = str(condition_raw)[:50] if condition_raw else 'Standard'
        
        vehicle_fields = [
            (L('car_type'), contract_data.get('car_type', 'N/A')),
            (L('brand'), contract_data.get('brand', contract_data.get('vehicle_type', 'N/A'))),
            (L('model'), contract_data.get('model', contract_data.get('vehicle_model', 'N/A'))),
            (L('year'), contract_data.get('manufacture_year', 'N/A')),
            (L('vin'), contract_data.get('vehicle_vin', contract_data.get('vin', 'N/A'))),
            (L('plate'), contract_data.get('vehicle_plate', contract_data.get('plate', 'N/A'))),
            (L('color'), translate_value(contract_data.get('color', 'N/A'), lang)),
            (L('fuel_type'), translate_value(contract_data.get('fuel_type', 'N/A'), lang)),
            (L('mileage'), f"{contract_data.get('mileage', 0):,} km"),
            (L('condition'), translate_value(condition_val, lang)),
        ]
        
        for label, value in vehicle_fields:
            pdf.cell(60, 6, f"{label}:", border=0)
            val_str = fix_arabic(str(value) if value else 'N/A')
            if len(str(val_str)) > 50:
                val_str = str(val_str)[:47] + "..."
            pdf.cell(70, 6, val_str, border=0, ln=True)
        
        # AI Analysis Notes (if available)
        ai_notes = contract_data.get('ai_analysis', contract_data.get('damage_notes', ''))
        if ai_notes:
            pdf.ln(3)
            pdf.set_font(font_name, 'B', 10)
            pdf.cell(0, 8, "AI Analysis Notes:", ln=True)
            pdf.set_font(font_name, '', 9)
            pdf.multi_cell(0, 6, fix_arabic(str(ai_notes)[:500]))
        
        pdf.ln(5)
        
        # ===== Section 3: Financial Details (كاش أو تقسيط) =====
        pdf.set_fill_color(251, 194, 235)
        pdf.set_text_color(50, 50, 50)
        pdf.set_font(font_name, 'B', 12)
        pdf.cell(0, 10, fix_arabic("  " + L('section_financial')), ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font(font_name, '', 11)
        pdf.ln(3)
        
        total_price = float(contract_data.get('total_price', contract_data.get('estimated_price', 0)))
        down_payment = float(contract_data.get('down_payment', 0))
        remaining = float(contract_data.get('remaining_amount', total_price - down_payment))
        monthly = float(contract_data.get('monthly_installment', 0))
        months = int(contract_data.get('installment_count', 0))
        interest = float(contract_data.get('interest_rate', 0)) * 100
        
        # تحديد طريقة الدفع (كاش أو تقسيط)
        payment_method = contract_data.get('payment_method', '')
        if not payment_method:
            # تحديد تلقائي بناءً على عدد الأقساط
            cash_labels = {'en': 'Cash', 'de': 'Bar', 'ar': 'كاش'}
            installment_labels = {'en': 'Installment', 'de': 'Ratenzahlung', 'ar': 'تقسيط'}
            if months > 0 and monthly > 0:
                payment_method = installment_labels.get(lang, 'Installment')
            else:
                payment_method = cash_labels.get(lang, 'Cash')
        
        # عرض طريقة الدفع بشكل بارز
        pdf.set_font(font_name, 'B', 12)
        pdf.set_fill_color(76, 175, 80) if "Cash" in payment_method or "Bar" in payment_method or "كاش" in payment_method else pdf.set_fill_color(255, 193, 7)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, f"  {L('payment_method')}: {fix_arabic(payment_method)}", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font(font_name, '', 11)
        pdf.ln(3)
        
        financial_fields = [
            (L('total_price'), f"{total_price:,.2f} EUR"),
        ]
        
        # إذا كان تقسيط، أضف تفاصيل الأقساط
        is_installment = "Installment" in payment_method or "Ratenzahlung" in payment_method or "تقسيط" in payment_method or months > 0
        if is_installment:
            financial_fields.extend([
                (L('down_payment'), f"{down_payment:,.2f} EUR"),
                (L('remaining_amount'), f"{remaining:,.2f} EUR"),
                (L('installment_count'), f"{months}"),
                (L('monthly_installment'), f"{monthly:,.2f} EUR"),
            ])
        
        for label, value in financial_fields:
            pdf.cell(80, 6, f"{fix_arabic(label)}:", border=0)
            pdf.set_font(font_name, 'B', 11)
            pdf.cell(0, 6, str(value), border=0, ln=True)
            pdf.set_font(font_name, '', 11)
        
        # Get user's language for proper text direction (needed for signatures)
        lang_code = st.session_state.get('language', 'de')
        is_rtl = lang_code == 'ar'
        
        # Helper function for contract text
        def get_contract_label(key):
            text = t(key)
            return fix_arabic(text) if is_rtl else text
        
        
        # ===== Section 4: GDPR Data Protection =====
        pdf.add_page()  # صفحة جديدة لـ GDPR
        
        # Note: is_rtl and lang_code already defined above
        is_rtl = lang_code == 'ar'
        
        # Section 4 banner
        pdf.set_fill_color(100, 149, 237)  # Cornflower blue
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(font_name, 'B', 12)
        section_title = fix_arabic(t('gdpr.section_title')) if is_rtl else t('gdpr.section_title')
        pdf.cell(0, 10, f"  SECTION 4: {section_title}", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(3)
        
        # GDPR Section Header
        pdf.set_fill_color(100, 149, 237)  # Cornflower blue
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(font_name, 'B', 10)
        info_header = fix_arabic(t('gdpr.info_header')) if is_rtl else t('gdpr.info_header')
        pdf.cell(0, 8, f"  {info_header}", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font(font_name, '', 9)
        pdf.ln(3)
        
        # Seller info from config
        seller_name = Config.APP_NAME
        seller_address = getattr(Config, 'COMPANY_ADDRESS', 'Germany')
        seller_phone = Config.SUPPORT_PHONE
        seller_email = Config.CONTACT_EMAIL
        
        # Helper function for translated text
        def get_gdpr_text(key):
            text = t(key)
            return fix_arabic(text) if is_rtl else text
        
        # 1. Data Controller
        pdf.set_font(font_name, 'B', 9)
        pdf.cell(0, 5, get_gdpr_text('gdpr.data_controller_title'), ln=True)
        pdf.set_font(font_name, '', 8)
        controller_text = f"{get_gdpr_text('gdpr.data_controller_text')}\n{seller_name}\nAddress: {seller_address}\nPhone: {seller_phone} | Email: {seller_email}"
        pdf.multi_cell(0, 4, controller_text)
        pdf.ln(2)
        
        # 2. Purpose and Legal Basis
        pdf.set_font(font_name, 'B', 9)
        pdf.cell(0, 5, get_gdpr_text('gdpr.purpose_title'), ln=True)
        pdf.set_font(font_name, '', 8)
        pdf.multi_cell(0, 4, get_gdpr_text('gdpr.purpose_text'))
        pdf.ln(2)
        
        # 3. Data Recipients
        pdf.set_font(font_name, 'B', 9)
        pdf.cell(0, 5, get_gdpr_text('gdpr.recipients_title'), ln=True)
        pdf.set_font(font_name, '', 8)
        pdf.multi_cell(0, 4, get_gdpr_text('gdpr.recipients_text'))
        pdf.ln(2)
        
        # 4. Storage Period
        pdf.set_font(font_name, 'B', 9)
        pdf.cell(0, 5, get_gdpr_text('gdpr.storage_title'), ln=True)
        pdf.set_font(font_name, '', 8)
        pdf.multi_cell(0, 4, get_gdpr_text('gdpr.storage_text'))
        pdf.ln(2)
        
        # 5. Your Rights
        pdf.set_font(font_name, 'B', 9)
        pdf.cell(0, 5, get_gdpr_text('gdpr.rights_title'), ln=True)
        pdf.set_font(font_name, '', 8)
        pdf.multi_cell(0, 4, get_gdpr_text('gdpr.rights_text'))
        pdf.ln(2)
        
        # 6. Data Provision Obligation
        pdf.set_font(font_name, 'B', 9)
        pdf.cell(0, 5, get_gdpr_text('gdpr.provision_title'), ln=True)
        pdf.set_font(font_name, '', 8)
        pdf.multi_cell(0, 4, get_gdpr_text('gdpr.provision_text'))
        pdf.ln(2)
        
        # 7. Withdrawal of Consent
        pdf.set_font(font_name, 'B', 9)
        pdf.cell(0, 5, get_gdpr_text('gdpr.withdrawal_title'), ln=True)
        pdf.set_font(font_name, '', 8)
        pdf.multi_cell(0, 4, get_gdpr_text('gdpr.withdrawal_text'))
        pdf.ln(2)
        
        # 8. Right to Complain
        pdf.set_font(font_name, 'B', 9)
        pdf.cell(0, 5, get_gdpr_text('gdpr.complaint_title'), ln=True)
        pdf.set_font(font_name, '', 8)
        pdf.multi_cell(0, 4, get_gdpr_text('gdpr.complaint_text'))
        pdf.ln(3)
        
        # Acknowledgment checkbox area with checkmarks
        pdf.set_fill_color(240, 240, 240)
        pdf.rect(10, pdf.get_y(), 190, 20, 'F')
        pdf.set_xy(12, pdf.get_y() + 3)
        pdf.set_font(font_name, 'B', 10)
        pdf.cell(0, 5, f"[X]  {get_gdpr_text('gdpr.checkbox_read')}", ln=True)
        pdf.set_xy(12, pdf.get_y() + 2)
        pdf.cell(0, 5, f"[X]  {get_gdpr_text('gdpr.checkbox_consent')}", ln=True)
        
        pdf.ln(10)
        
        # ===== Signatures at end of GDPR page (Page 2) =====
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(8)
        
        # Get buyer and seller names
        buyer_name = user_data.get('full_name', 'N/A')
        seller_name = Config.APP_NAME
        
        # Signature lines
        pdf.cell(90, 6, "_________________________", align='C')
        pdf.cell(0, 6, "_________________________", align='C', ln=True)
        
        # Labels - استخدام الترجمة الصحيحة حسب لغة المستخدم
        pdf.set_font(font_name, '', 9)
        buyer_sig_label = fix_arabic(t('contract.buyer_signature')) if is_rtl else t('contract.buyer_signature')
        seller_sig_label = fix_arabic(t('contract.seller_signature')) if is_rtl else t('contract.seller_signature')
        pdf.cell(90, 5, buyer_sig_label, align='C')
        pdf.cell(0, 5, seller_sig_label, align='C', ln=True)
        
        # Names (Bold)
        pdf.set_font(font_name, 'B', 10)
        buyer_display = fix_arabic(buyer_name)
        pdf.cell(90, 6, buyer_display, align='C')
        pdf.cell(0, 6, seller_name, align='C', ln=True)
        
        # Date
        pdf.set_font(font_name, '', 9)
        pdf.ln(3)
        date_label = fix_arabic(t('gdpr.date')) if is_rtl else t('gdpr.date')
        pdf.cell(0, 5, f"{date_label}: {datetime.now().strftime('%Y-%m-%d')}", align='C', ln=True)
        
        # ===== Section 5: Marketing Consent =====
        pdf.add_page()  # صفحة جديدة للموافقة على التسويق
        
        # Helper function for marketing translated text
        def get_marketing_text(key):
            text = t(key)
            return fix_arabic(text) if is_rtl else text
        
        # Section 5 banner
        pdf.set_fill_color(76, 175, 80)  # Green color for optional consent
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(font_name, 'B', 12)
        pdf.cell(0, 10, f"  SECTION 5: {get_marketing_text('marketing.section_title')}", ln=True, fill=True)
        pdf.set_font(font_name, '', 9)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 6, get_marketing_text('marketing.subtitle'), ln=True, align='C')
        pdf.set_text_color(0, 0, 0)
        pdf.ln(3)
        
        # Marketing consent text
        pdf.set_font(font_name, '', 11)
        pdf.set_fill_color(245, 245, 245)
        pdf.rect(10, pdf.get_y(), 190, 40, 'F')
        pdf.set_xy(15, pdf.get_y() + 5)
        pdf.multi_cell(180, 6, get_marketing_text('marketing.consent_text'))
        pdf.ln(10)
        
        # Checkbox options
        pdf.set_font(font_name, 'B', 11)
        pdf.ln(5)
        
        # Yes checkbox
        pdf.set_xy(20, pdf.get_y())
        pdf.cell(8, 8, "", border=1)  # Checkbox
        pdf.set_xy(30, pdf.get_y() + 1)
        pdf.cell(0, 6, get_marketing_text('marketing.checkbox_yes'), ln=True)
        pdf.ln(5)
        
        # No checkbox
        pdf.set_xy(20, pdf.get_y())
        pdf.cell(8, 8, "", border=1)  # Checkbox
        pdf.set_xy(30, pdf.get_y() + 1)
        pdf.cell(0, 6, get_marketing_text('marketing.checkbox_no'), ln=True)
        pdf.ln(15)
        
        # Note about voluntary nature
        pdf.set_font(font_name, '', 9)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 6, get_marketing_text('marketing.note'), ln=True, align='C')
        pdf.set_text_color(0, 0, 0)
        pdf.ln(15)
        
        # ===== Footer =====
        pdf.set_y(-55)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        pdf.set_font(font_name, '', 9)
        
        # Get translated footer text
        def get_contract_text(key):
            text = t(key)
            return fix_arabic(text) if is_rtl else text
        
        pdf.cell(0, 6, get_contract_text('contract.footer_text'), ln=True, align='C')
        pdf.ln(5)
        
        # Get buyer and seller names
        buyer_name = user_data.get('full_name', 'N/A')
        seller_name = Config.APP_NAME
        
        # Signature lines with names
        pdf.cell(90, 6, "_________________________", align='C')
        pdf.cell(0, 6, "_________________________", align='C', ln=True)
        
        # Labels
        pdf.set_font(font_name, '', 9)
        pdf.cell(90, 5, get_contract_text('contract.buyer_signature'), align='C')
        pdf.cell(0, 5, get_contract_text('contract.seller_signature'), align='C', ln=True)
        
        # Names
        pdf.set_font(font_name, 'B', 9)
        # Always apply fix_arabic to handle Arabic names
        buyer_display = fix_arabic(buyer_name)
        pdf.cell(90, 5, buyer_display, align='C')
        pdf.cell(0, 5, seller_name, align='C', ln=True)
        
        # التذييل يُدار تلقائياً بواسطة ContractPDF.footer() 
        # لا حاجة لإضافة خط تذييل إضافي هنا
        
        pdf.output(str(file_path))
        return str(file_path)

    def generate_receipt(self, receipt_id: str, payment_data: dict, summary: dict, user_data: dict) -> str:
        """إنشاء إيصال دفع PDF"""
        filename = f"Receipt-{receipt_id}-{datetime.now().strftime('%Y%m%d%H%M')}.pdf"
        file_path = self.output_dir / filename

        pdf = FPDF()
        pdf.add_page()
        
        font_name = "Arial"
        if self.font_path and os.path.exists(self.font_path):
            try:
                pdf.add_font('CustomArial', '', self.font_path, uni=True)
                pdf.add_font('CustomArial', 'B', self.font_bold_path, uni=True)
                font_name = 'CustomArial'
            except:
                pass
        
        # Header
        pdf.set_font(font_name, 'B', 16)
        pdf.cell(0, 12, "Payment Receipt", ln=True, align='C')
        pdf.set_font(font_name, '', 10)
        pdf.cell(0, 8, f"Receipt #: {receipt_id}", ln=True, align='C')
        pdf.line(10, 30, 200, 30)
        pdf.ln(10)
        
        # Client - تطبيق fix_arabic على اسم العميل
        pdf.set_font(font_name, 'B', 11)
        client_name = fix_arabic(user_data.get('full_name', 'N/A'))
        pdf.cell(0, 8, f"Client: {client_name}", ln=True)
        pdf.ln(5)
        
        # Payment Details - تطبيق fix_arabic على طريقة الدفع
        pdf.set_font(font_name, '', 11)
        pdf.cell(0, 8, f"Amount: {float(payment_data.get('amount', 0)):,.2f} EUR", ln=True)
        payment_method = fix_arabic(str(payment_data.get('method', 'N/A')))
        pdf.cell(0, 8, f"Method: {payment_method}", ln=True)
        pdf.cell(0, 8, f"Date: {payment_data.get('date', datetime.now().strftime('%Y-%m-%d'))}", ln=True)
        pdf.cell(0, 8, f"Reference: {payment_data.get('ref', 'N/A')}", ln=True)
        
        # Footer
        pdf.set_y(-30)
        pdf.set_font(font_name, '', 8)
        pdf.cell(0, 8, f"{Config.APP_NAME} | Thank you for your payment!", align='C')
        
        pdf.output(str(file_path))
        return str(file_path)

    def generate_salary_invoice(self, employee_data: dict, month: int, year: int, 
                                 other_deductions: float = 0, has_children: bool = True,
                                 church_tax: bool = False, tax_class: int = 1, lang: str = 'de') -> str:
        """
        إنشاء كشف راتب PDF احترافي مع اقتطاعات الضرائب الألمانية المفصلة (2025)
        
        :param employee_data: بيانات الموظف
        :param month: الشهر (1-12)
        :param year: السنة
        :param other_deductions: خصومات إضافية
        :param has_children: هل لديه أطفال (يؤثر على Pflegeversicherung)
        :param church_tax: هل يدفع ضريبة الكنيسة
        :param tax_class: الفئة الضريبية (1-6)
        :param lang: اللغة ('ar', 'de', 'en')
        :return: مسار ملف PDF
        """
        
        # === نسب الاقتطاعات الألمانية 2025 (حصة الموظف) ===
        GERMAN_RATES_EMPLOYEE = {
            'rentenversicherung': 0.093,      # تأمين التقاعد 9.3%
            'arbeitslosenversicherung': 0.013, # تأمين البطالة 1.3%
            'krankenversicherung': 0.073,      # التأمين الصحي 7.3%
            'kranken_zusatz': 0.0125,          # إضافة التأمين الصحي 1.25%
            'pflegeversicherung': 0.018,       # تأمين الرعاية (مع أطفال) 1.8%
            'pflegeversicherung_kinderlos': 0.023,  # تأمين الرعاية (بدون أطفال) 2.3%
            'solidaritaetszuschlag': 0.055,    # رسم التضامن 5.5% من ضريبة الدخل
            'kirchensteuer': 0.09,             # ضريبة الكنيسة 9% من ضريبة الدخل (اختياري)
        }
        
        # === نسب حصة صاحب العمل من التأمينات الاجتماعية ===
        GERMAN_RATES_EMPLOYER = {
            'rentenversicherung': 0.093,       # تأمين التقاعد 9.3%
            'arbeitslosenversicherung': 0.013, # تأمين البطالة 1.3%
            'krankenversicherung': 0.073,      # التأمين الصحي 7.3%
            'kranken_zusatz': 0.0125,          # إضافة التأمين الصحي 1.25%
            'pflegeversicherung': 0.018,       # تأمين الرعاية 1.8% (ثابت لصاحب العمل)
        }
        
        # سقف الاشتراكات الشهرية 2025
        BEITRAGSBEMESSUNGSGRENZE = {
            'rente_arbeitslosen': 8050,  # €96,600 سنوياً / 12
            'kranken_pflege': 5512.50,   # €66,150 سنوياً / 12
        }
        
        # حساب ضريبة الدخل المقدرة (Lohnsteuer) حسب الفئة الضريبية
        def calculate_income_tax(annual_gross, tax_class):
            """حساب ضريبة الدخل السنوية التقريبية"""
            # الإعفاء الضريبي الأساسي 2025
            grundfreibetrag = 12084
            
            if annual_gross <= grundfreibetrag:
                return 0
            
            taxable = annual_gross - grundfreibetrag
            
            # نسب ضريبية تقريبية حسب الفئة
            if tax_class in [1, 4]:
                if taxable <= 17000: rate = 0.14
                elif taxable <= 55000: rate = 0.24
                elif taxable <= 266000: rate = 0.42
                else: rate = 0.45
            elif tax_class == 3:  # متزوج - دخل وحيد
                rate = 0.12 if taxable <= 30000 else 0.22
            elif tax_class == 5:  # متزوج - دخل ثانوي
                rate = 0.30 if taxable <= 20000 else 0.38
            elif tax_class == 6:  # وظيفة ثانية
                rate = 0.35
            else:
                rate = 0.20
            
            return taxable * rate
        
        # قاموس التسميات متعدد اللغات
        labels = {
            'title': {'en': 'Salary Slip', 'de': 'Gehaltsabrechnung', 'ar': 'كشف الراتب'},
            'employee_name': {'en': 'Employee Name', 'de': 'Mitarbeitername', 'ar': 'اسم الموظف'},
            'job_title': {'en': 'Job Title', 'de': 'Berufsbezeichnung', 'ar': 'المسمى الوظيفي'},
            'employee_id': {'en': 'Employee ID', 'de': 'Mitarbeiter-Nr.', 'ar': 'رقم الموظف'},
            'tax_class': {'en': 'Tax Class', 'de': 'Steuerklasse', 'ar': 'الفئة الضريبية'},
            'payment_period': {'en': 'Payment Period', 'de': 'Zahlungszeitraum', 'ar': 'فترة الدفع'},
            'gross_salary': {'en': 'Gross Salary', 'de': 'Bruttogehalt', 'ar': 'الراتب الإجمالي'},
            'holiday_bonus': {'en': 'Holiday Bonus', 'de': 'Feiertagsgeld', 'ar': 'بدل العطلات'},
            'vacation_bonus': {'en': 'Vacation Bonus', 'de': 'Urlaubsgeld', 'ar': 'بدل الإجازات'},
            'total_earnings': {'en': 'Total Earnings', 'de': 'Gesamtbezüge', 'ar': 'إجمالي المستحقات'},
            
            # الضرائب
            'taxes': {'en': 'Taxes', 'de': 'Steuern', 'ar': 'الضرائب'},
            'lohnsteuer': {'en': 'Income Tax', 'de': 'Lohnsteuer', 'ar': 'ضريبة الدخل'},
            'solidaritaetszuschlag': {'en': 'Solidarity Surcharge', 'de': 'Solidaritätszuschlag', 'ar': 'رسم التضامن'},
            'kirchensteuer': {'en': 'Church Tax', 'de': 'Kirchensteuer', 'ar': 'ضريبة الكنيسة'},
            
            # التأمينات الاجتماعية
            'sozialversicherung': {'en': 'Social Insurance', 'de': 'Sozialversicherung', 'ar': 'التأمين الاجتماعي'},
            'employee_share': {'en': 'Employee Share', 'de': 'Arbeitnehmeranteil', 'ar': 'حصة الموظف'},
            'employer_share': {'en': 'Employer Share', 'de': 'Arbeitgeberanteil', 'ar': 'حصة صاحب العمل'},
            'rentenversicherung': {'en': 'Pension Insurance', 'de': 'Rentenversicherung', 'ar': 'تأمين التقاعد'},
            'arbeitslosenversicherung': {'en': 'Unemployment Ins.', 'de': 'Arbeitslosenversicherung', 'ar': 'تأمين البطالة'},
            'krankenversicherung': {'en': 'Health Insurance', 'de': 'Krankenversicherung', 'ar': 'التأمين الصحي'},
            'pflegeversicherung': {'en': 'Long-term Care Ins.', 'de': 'Pflegeversicherung', 'ar': 'تأمين الرعاية'},
            'total_employer_cost': {'en': 'Total Employer Cost', 'de': 'Arbeitgeber-Gesamtkosten', 'ar': 'إجمالي تكلفة صاحب العمل'},
            
            'other_deductions': {'en': 'Other Deductions', 'de': 'Sonstige Abzüge', 'ar': 'خصومات أخرى'},
            'total_deductions': {'en': 'Total Deductions', 'de': 'Gesamtabzüge', 'ar': 'إجمالي الخصومات'},
            'net_salary': {'en': 'Net Salary', 'de': 'Nettogehalt', 'ar': 'صافي الراتب'},
            'generated_on': {'en': 'Generated on', 'de': 'Erstellt am', 'ar': 'تاريخ الإصدار'},
            'month_names': {
                'en': ['', 'January', 'February', 'March', 'April', 'May', 'June', 
                       'July', 'August', 'September', 'October', 'November', 'December'],
                'de': ['', 'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',
                       'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'],
                'ar': ['', 'يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو',
                       'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
            }
        }
        
        def L(key):
            """جلب التسمية باللغة المحددة"""
            return labels.get(key, {}).get(lang, labels.get(key, {}).get('en', key))
        
        # استخراج البيانات
        first_name = employee_data.get('first_name', '')
        last_name = employee_data.get('last_name', '')
        full_name = f"{first_name} {last_name}".strip()
        job_title = employee_data.get('job_title', 'N/A')
        emp_id = employee_data.get('id', 'N/A')
        
        gross_salary = float(employee_data.get('monthly_salary', 0) or 0)
        
        # بدل العطلات وبدل الإجازات يُصرفان فقط في شهر ديسمبر (12)
        if month == 12:
            holiday_bonus = float(employee_data.get('feiertags_geld', 0) or 0)
            vacation_bonus = float(employee_data.get('urlaubsgeld', 0) or 0)
        else:
            holiday_bonus = 0.0
            vacation_bonus = 0.0
        
        total_earnings = gross_salary + holiday_bonus + vacation_bonus
        
        # === حساب الاقتطاعات الألمانية المفصلة ===
        
        # 1. ضريبة الدخل (Lohnsteuer)
        annual_gross = gross_salary * 12
        annual_tax = calculate_income_tax(annual_gross, tax_class)
        lohnsteuer = annual_tax / 12
        
        # 2. رسم التضامن (Solidaritätszuschlag) - 5.5% من ضريبة الدخل
        solidaritaetszuschlag = lohnsteuer * GERMAN_RATES_EMPLOYEE['solidaritaetszuschlag']
        
        # 3. ضريبة الكنيسة (Kirchensteuer) - اختياري
        kirchensteuer = lohnsteuer * GERMAN_RATES_EMPLOYEE['kirchensteuer'] if church_tax else 0
        
        total_taxes = lohnsteuer + solidaritaetszuschlag + kirchensteuer
        
        # 4. التأمينات الاجتماعية - حصة الموظف
        # الراتب الخاضع للتأمين (مع السقف)
        sv_brutto_rente = min(gross_salary, BEITRAGSBEMESSUNGSGRENZE['rente_arbeitslosen'])
        sv_brutto_kranken = min(gross_salary, BEITRAGSBEMESSUNGSGRENZE['kranken_pflege'])
        
        # حصة الموظف
        rentenversicherung = sv_brutto_rente * GERMAN_RATES_EMPLOYEE['rentenversicherung']
        arbeitslosenversicherung = sv_brutto_rente * GERMAN_RATES_EMPLOYEE['arbeitslosenversicherung']
        krankenversicherung = sv_brutto_kranken * (GERMAN_RATES_EMPLOYEE['krankenversicherung'] + GERMAN_RATES_EMPLOYEE['kranken_zusatz'])
        pflege_rate_employee = GERMAN_RATES_EMPLOYEE['pflegeversicherung'] if has_children else GERMAN_RATES_EMPLOYEE['pflegeversicherung_kinderlos']
        pflegeversicherung = sv_brutto_kranken * pflege_rate_employee
        
        total_sozialversicherung = rentenversicherung + arbeitslosenversicherung + krankenversicherung + pflegeversicherung
        
        # 5. حصة صاحب العمل من التأمينات الاجتماعية
        rentenversicherung_ag = sv_brutto_rente * GERMAN_RATES_EMPLOYER['rentenversicherung']
        arbeitslosenversicherung_ag = sv_brutto_rente * GERMAN_RATES_EMPLOYER['arbeitslosenversicherung']
        krankenversicherung_ag = sv_brutto_kranken * (GERMAN_RATES_EMPLOYER['krankenversicherung'] + GERMAN_RATES_EMPLOYER['kranken_zusatz'])
        pflegeversicherung_ag = sv_brutto_kranken * GERMAN_RATES_EMPLOYER['pflegeversicherung']
        
        total_arbeitgeber = rentenversicherung_ag + arbeitslosenversicherung_ag + krankenversicherung_ag + pflegeversicherung_ag
        
        # إجمالي الخصومات من راتب الموظف
        total_deductions = total_taxes + total_sozialversicherung + other_deductions
        
        # صافي الراتب
        net_salary = total_earnings - total_deductions
        
        # اسم الشهر - لا نطبق fix_arabic على اسم الشهر لأنه يشوهه
        month_name_display = L('month_names')[month] if 1 <= month <= 12 else str(month)
        
        # === إنشاء PDF ===
        filename = f"Salary-{emp_id}-{year}{month:02d}-{datetime.now().strftime('%H%M%S')}.pdf"
        file_path = self.output_dir / filename
        
        pdf = FPDF()
        pdf.add_page()
        
        font_name = "Arial"
        if self.font_path and os.path.exists(self.font_path):
            try:
                pdf.add_font('CustomArial', '', self.font_path, uni=True)
                pdf.add_font('CustomArial', 'B', self.font_bold_path, uni=True)
                font_name = 'CustomArial'
            except:
                pass
        
        # === الهيدر ===
        pdf.set_fill_color(26, 26, 46)
        pdf.rect(0, 0, 210, 40, 'F')
        
        pdf.set_font(font_name, 'B', 20)
        pdf.set_text_color(212, 175, 75)
        title = fix_arabic(L('title')) if lang == 'ar' else L('title')
        pdf.set_xy(10, 12)
        pdf.cell(0, 12, title, align='C')
        
        pdf.set_font(font_name, '', 12)
        pdf.set_text_color(255, 255, 255)
        pdf.set_xy(10, 26)
        # استخدام fix_arabic على النص العربي
        if lang == 'ar':
            period_label_fixed = fix_arabic(L('payment_period'))
            month_fixed = fix_arabic(month_name_display)
            pdf.cell(0, 8, f"{period_label_fixed}: {month_fixed} {year}", align='C')
        else:
            period_label = L('payment_period')
            pdf.cell(0, 8, f"{period_label}: {month_name_display} {year}", align='C')
        
        pdf.ln(30)
        pdf.set_text_color(0, 0, 0)
        
        # === معلومات الموظف ===
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font(font_name, 'B', 10)
        
        y_start = 48
        pdf.set_xy(10, y_start)
        
        # صف الموظف
        emp_name_label = fix_arabic(L('employee_name')) if lang == 'ar' else L('employee_name')
        emp_name_val = fix_arabic(full_name) if lang == 'ar' else full_name
        pdf.cell(45, 7, f"{emp_name_label}:", fill=True)
        pdf.set_font(font_name, '', 10)
        pdf.cell(50, 7, emp_name_val)
        
        pdf.set_font(font_name, 'B', 10)
        tax_label = fix_arabic(L('tax_class')) if lang == 'ar' else L('tax_class')
        pdf.cell(35, 7, f"{tax_label}:", fill=True)
        pdf.set_font(font_name, '', 10)
        pdf.cell(0, 7, str(tax_class))
        pdf.ln(8)
        
        pdf.set_font(font_name, 'B', 10)
        job_label = fix_arabic(L('job_title')) if lang == 'ar' else L('job_title')
        job_val = fix_arabic(job_title) if lang == 'ar' else job_title
        pdf.cell(45, 7, f"{job_label}:", fill=True)
        pdf.set_font(font_name, '', 10)
        pdf.cell(50, 7, job_val)
        
        pdf.set_font(font_name, 'B', 10)
        id_label = fix_arabic(L('employee_id')) if lang == 'ar' else L('employee_id')
        pdf.cell(35, 7, f"{id_label}:", fill=True)
        pdf.set_font(font_name, '', 10)
        pdf.cell(0, 7, str(emp_id))
        pdf.ln(12)
        
        # دالة رسم الصفوف
        def draw_row(label, amount, bold=False, rate_pct=None):
            pdf.set_font(font_name, 'B' if bold else '', 9)
            lbl = fix_arabic(label) if lang == 'ar' else label
            if rate_pct:
                # للعربية: النسبة قبل النص
                if lang == 'ar':
                    pdf.cell(100, 6, f"  ({rate_pct}%) {lbl}")
                else:
                    pdf.cell(100, 6, f"  {lbl} ({rate_pct}%)")
            else:
                pdf.cell(100, 6, f"  {lbl}")
            pdf.cell(0, 6, f"{amount:,.2f} EUR", align='R')
            pdf.ln()
        
        # === المستحقات ===
        pdf.set_fill_color(34, 139, 34)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(font_name, 'B', 11)
        earnings_title = fix_arabic(L('total_earnings')) if lang == 'ar' else L('total_earnings')
        pdf.cell(0, 8, f"  {earnings_title}", fill=True, ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)
        
        draw_row(L('gross_salary'), gross_salary)
        if holiday_bonus > 0:
            draw_row(L('holiday_bonus'), holiday_bonus)
        if vacation_bonus > 0:
            draw_row(L('vacation_bonus'), vacation_bonus)
        
        pdf.set_draw_color(100, 100, 100)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(1)
        draw_row(L('total_earnings'), total_earnings, bold=True)
        pdf.ln(6)
        
        # === الضرائب ===
        pdf.set_fill_color(255, 140, 0)  # Orange for taxes
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(font_name, 'B', 11)
        taxes_title = fix_arabic(L('taxes')) if lang == 'ar' else L('taxes')
        pdf.cell(0, 8, f"  {taxes_title}", fill=True, ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)
        
        draw_row(L('lohnsteuer'), lohnsteuer)
        draw_row(L('solidaritaetszuschlag'), solidaritaetszuschlag, rate_pct="5.5")
        if church_tax and kirchensteuer > 0:
            draw_row(L('kirchensteuer'), kirchensteuer, rate_pct="9")
        
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(1)
        draw_row(L('taxes'), total_taxes, bold=True)
        pdf.ln(6)
        
        # === التأمينات الاجتماعية - حصة الموظف ===
        pdf.set_fill_color(70, 130, 180)  # Steel blue for social insurance
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(font_name, 'B', 11)
        sv_title = fix_arabic(f"{L('sozialversicherung')} - {L('employee_share')}") if lang == 'ar' else f"{L('sozialversicherung')} - {L('employee_share')}"
        pdf.cell(0, 8, f"  {sv_title}", fill=True, ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)
        
        draw_row(L('rentenversicherung'), rentenversicherung, rate_pct="9.3")
        draw_row(L('arbeitslosenversicherung'), arbeitslosenversicherung, rate_pct="1.3")
        draw_row(L('krankenversicherung'), krankenversicherung, rate_pct="8.55")
        pflege_pct = "1.8" if has_children else "2.3"
        draw_row(L('pflegeversicherung'), pflegeversicherung, rate_pct=pflege_pct)
        
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(1)
        draw_row(L('employee_share'), total_sozialversicherung, bold=True)
        
        if other_deductions > 0:
            pdf.ln(4)
            draw_row(L('other_deductions'), other_deductions)
        
        pdf.ln(6)
        
        # === حصة صاحب العمل من التأمينات ===
        pdf.set_fill_color(102, 51, 153)  # Purple for employer share
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(font_name, 'B', 11)
        ag_title = fix_arabic(f"{L('sozialversicherung')} - {L('employer_share')}") if lang == 'ar' else f"{L('sozialversicherung')} - {L('employer_share')}"
        pdf.cell(0, 8, f"  {ag_title}", fill=True, ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)
        
        draw_row(L('rentenversicherung'), rentenversicherung_ag, rate_pct="9.3")
        draw_row(L('arbeitslosenversicherung'), arbeitslosenversicherung_ag, rate_pct="1.3")
        draw_row(L('krankenversicherung'), krankenversicherung_ag, rate_pct="8.55")
        draw_row(L('pflegeversicherung'), pflegeversicherung_ag, rate_pct="1.8")
        
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(1)
        draw_row(L('employer_share'), total_arbeitgeber, bold=True)
        
        pdf.ln(6)
        
        # === إجمالي الخصومات ===
        pdf.set_fill_color(220, 53, 69)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(font_name, 'B', 10)
        pdf.cell(100, 8, f"  {L('total_deductions')}", fill=True)
        pdf.set_font(font_name, 'B', 12)
        pdf.cell(0, 8, f"-{total_deductions:,.2f} EUR", align='R', fill=True)
        pdf.ln(12)
        
        # === صافي الراتب ===
        pdf.set_fill_color(212, 175, 75)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font(font_name, 'B', 14)
        net_label = fix_arabic(L('net_salary')) if lang == 'ar' else L('net_salary')
        pdf.cell(100, 12, f"  {net_label}", fill=True)
        pdf.set_font(font_name, 'B', 16)
        pdf.cell(0, 12, f"{net_salary:,.2f} EUR", align='R', fill=True)
        pdf.ln(15)
        
        # === الفوتر ===
        pdf.set_font(font_name, '', 8)
        pdf.set_text_color(128, 128, 128)
        gen_label = fix_arabic(L('generated_on')) if lang == 'ar' else L('generated_on')
        pdf.cell(0, 6, f"{gen_label}: {datetime.now().strftime('%Y-%m-%d %H:%M')}", align='C')
        pdf.ln(4)
        pdf.cell(0, 6, f"{Config.APP_NAME} | {Config.CONTACT_EMAIL}", align='C')
        
        pdf.output(str(file_path))
        
        # إرجاع بيانات الحساب للحفظ في قاعدة البيانات
        self._last_salary_calculation = {
            'gross_salary': gross_salary,
            'holiday_bonus': holiday_bonus,
            'vacation_bonus': vacation_bonus,
            'total_earnings': total_earnings,
            'lohnsteuer': lohnsteuer,
            'solidaritaetszuschlag': solidaritaetszuschlag,
            'kirchensteuer': kirchensteuer,
            'total_taxes': total_taxes,
            'rentenversicherung': rentenversicherung,
            'arbeitslosenversicherung': arbeitslosenversicherung,
            'krankenversicherung': krankenversicherung,
            'pflegeversicherung': pflegeversicherung,
            'total_sozialversicherung': total_sozialversicherung,
            # حصة صاحب العمل
            'rentenversicherung_ag': rentenversicherung_ag,
            'arbeitslosenversicherung_ag': arbeitslosenversicherung_ag,
            'krankenversicherung_ag': krankenversicherung_ag,
            'pflegeversicherung_ag': pflegeversicherung_ag,
            'total_arbeitgeber': total_arbeitgeber,
            'other_deductions': other_deductions,
            'total_deductions': total_deductions,
            'net_salary': net_salary
        }
        
        return str(file_path)

