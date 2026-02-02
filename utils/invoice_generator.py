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
    """تصحيح النص العربي للعرض الصحيح في PDF"""
    if text is None:
        return ""
    text = str(text)
    # Check if text contains Arabic characters
    if any('\u0600' <= c <= '\u06FF' for c in text):
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    return text

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

    def generate_contract(self, contract_id, contract_data: dict, user_data: dict) -> str:
        """
        إنشاء عقد PDF شامل يتضمن:
        - بيانات العميل الكاملة (الاسم، الهوية، الجنسية، الهاتف، الرخصة)
        - العنوان الكامل (الشارع، رقم البناء، الرمز البريدي، المدينة)
        - بيانات السيارة بالتفصيل مع الصورة
        - التفاصيل المالية (كاش أو تقسيط، عدد الأقساط، مقدار كل قسط)
        """
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
        pdf.cell(0, 12, "Vehicle Purchase Contract", ln=True, align='C')
        pdf.set_font(font_name, '', 10)
        pdf.cell(0, 8, f"Contract #: {contract_id} | Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
        
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)
        
        # ===== Section 1: Customer Information with Full Address =====
        pdf.set_fill_color(79, 172, 254)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(font_name, 'B', 12)
        pdf.cell(0, 10, "  SECTION 1: CUSTOMER INFORMATION", ln=True, fill=True)
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
            ("Full Name", user_data.get('full_name', 'N/A')),
            ("ID Number", user_data.get('id_number', 'N/A')),
            ("Nationality", user_data.get('nationality', 'N/A')),
            ("Date of Birth", user_data.get('birth_date', user_data.get('date_of_birth', 'N/A'))),
            ("Phone", user_data.get('phone', 'N/A')),
            ("Email", user_data.get('email', 'N/A')),
            ("Address", full_address),
            ("License Number", user_data.get('license_number', 'N/A')),
            ("License Type", user_data.get('license_type', 'N/A')),
            ("License Expiry", user_data.get('license_expiry', 'N/A')),
        ]
        
        for label, value in customer_fields:
            pdf.cell(60, 6, f"{label}:", border=0)
            pdf.cell(0, 6, fix_arabic(str(value) if value else 'N/A'), border=0, ln=True)
        
        pdf.ln(5)
        
        # ===== Section 2: Vehicle Details with Image =====
        pdf.set_fill_color(67, 233, 123)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(font_name, 'B', 12)
        pdf.cell(0, 10, "  SECTION 2: VEHICLE DETAILS", ln=True, fill=True)
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
            ("Car Type", contract_data.get('car_type', 'N/A')),
            ("Brand", contract_data.get('brand', contract_data.get('vehicle_type', 'N/A'))),
            ("Model", contract_data.get('model', contract_data.get('vehicle_model', 'N/A'))),
            ("Year", contract_data.get('manufacture_year', 'N/A')),
            ("VIN", contract_data.get('vehicle_vin', contract_data.get('vin', 'N/A'))),
            ("Plate Number", contract_data.get('vehicle_plate', contract_data.get('plate', 'N/A'))),
            ("Color", contract_data.get('color', 'N/A')),
            ("Fuel Type", contract_data.get('fuel_type', 'N/A')),
            ("Mileage", f"{contract_data.get('mileage', 0):,} km"),
            ("Condition", condition_val),
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
        pdf.cell(0, 10, "  SECTION 3: FINANCIAL DETAILS", ln=True, fill=True)
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
            if months > 0 and monthly > 0:
                payment_method = "Installment / " + fix_arabic("تقسيط")
            else:
                payment_method = "Cash / " + fix_arabic("كاش")
        
        # عرض طريقة الدفع بشكل بارز
        pdf.set_font(font_name, 'B', 12)
        pdf.set_fill_color(76, 175, 80) if "Cash" in payment_method else pdf.set_fill_color(255, 193, 7)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, f"  Payment Method: {fix_arabic(payment_method) if any(ord(c) > 127 for c in payment_method) else payment_method}", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font(font_name, '', 11)
        pdf.ln(3)
        
        financial_fields = [
            ("Total Vehicle Price", f"{total_price:,.2f} EUR"),
        ]
        
        # إذا كان تقسيط، أضف تفاصيل الأقساط
        if "Installment" in payment_method or months > 0:
            financial_fields.extend([
                ("Down Payment", f"{down_payment:,.2f} EUR"),
                ("Remaining Amount", f"{remaining:,.2f} EUR"),
                ("Interest Rate", f"{interest:.2f}%"),
                ("Number of Installments", f"{months} months"),
                ("Monthly Installment", f"{monthly:,.2f} EUR"),
            ])
        else:
            # كاش
            financial_fields.append(("Payment Status", "Full Payment / " + fix_arabic("دفع كامل")))
        
        for label, value in financial_fields:
            pdf.cell(80, 6, f"{label}:", border=0)
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