"""
utils/installment_invoice.py - مولد فواتير الأقساط
SmartCar AI-Dealer
توليد فواتير PDF مع QR تراكمي ودعم الطباعة الجماعية
"""

import os
import hashlib
import json
import qrcode
from datetime import datetime
from pathlib import Path
from io import BytesIO
from fpdf import FPDF
from config import Config
from db_manager import DatabaseManager

# Arabic RTL fix
import arabic_reshaper
from bidi.algorithm import get_display

def fix_arabic(text):
    """تصحيح النص العربي للعرض الصحيح في PDF"""
    if text is None:
        return ""
    text = str(text)
    if any('\u0600' <= c <= '\u06FF' for c in text):
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    return text

class InstallmentInvoiceGenerator:
    """مولد فواتير الأقساط مع QR تراكمي"""

    def __init__(self):
        self.output_dir = Config.INVOICES_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.db = DatabaseManager()
        
        # الخطوط
        self.font_path = str(Config.FONTS_DIR / Config.FONT_REGULAR)
        self.font_bold_path = str(Config.FONTS_DIR / Config.FONT_BOLD)
        
        # Fallback
        if not os.path.exists(self.font_path):
            if os.path.exists("C:/Windows/Fonts/arial.ttf"):
                self.font_path = "C:/Windows/Fonts/arial.ttf"
                self.font_bold_path = "C:/Windows/Fonts/arialbd.ttf"
            else:
                self.font_path = None

    def generate_invoice_pdf(self, invoice_id: int, contract_data: dict, user_data: dict) -> str:
        """توليد فاتورة PDF لقسط واحد"""
        # جلب بيانات الفاتورة
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM invoices WHERE id = ?", (invoice_id,))
            invoice = dict(cursor.fetchone())

        filename = f"{invoice['invoice_number']}.pdf"
        file_path = self.output_dir / filename

        pdf = FPDF()
        pdf.add_page()
        
        font_name = self._setup_fonts(pdf)
        
        # === الترويسة ===
        pdf.set_fill_color(30, 30, 50)
        pdf.rect(0, 0, 210, 40, 'F')
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(font_name, 'B', 18)
        pdf.set_xy(10, 10)
        pdf.cell(0, 10, Config.APP_NAME, ln=True, align='C')
        pdf.set_font(font_name, '', 10)
        pdf.cell(0, 8, f"Invoice: {invoice['invoice_number']}", ln=True, align='C')
        
        pdf.set_text_color(0, 0, 0)
        pdf.ln(15)
        
        # === بيانات العميل ===
        pdf.set_font(font_name, 'B', 12)
        pdf.cell(0, 10, "Customer Information", ln=True)
        pdf.set_font(font_name, '', 11)
        pdf.cell(0, 7, f"Name: {user_data.get('full_name', 'N/A')}", ln=True)
        pdf.cell(0, 7, f"ID: {user_data.get('id_number', 'N/A')}", ln=True)
        pdf.ln(5)
        
        # === بيانات السيارة ===
        pdf.set_font(font_name, 'B', 12)
        pdf.cell(0, 10, "Vehicle Information", ln=True)
        pdf.set_font(font_name, '', 11)
        pdf.cell(0, 7, f"Type: {contract_data.get('vehicle_type', '')} {contract_data.get('vehicle_model', '')}", ln=True)
        pdf.cell(0, 7, f"VIN: {contract_data.get('vehicle_vin', 'N/A')}", ln=True)
        pdf.ln(5)
        
        # === تفاصيل الفاتورة ===
        pdf.set_font(font_name, 'B', 12)
        pdf.cell(0, 10, "Invoice Details", ln=True)
        
        # جدول
        pdf.set_font(font_name, 'B', 10)
        pdf.set_fill_color(79, 172, 254)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(60, 8, "Description", 1, 0, 'C', True)
        pdf.cell(40, 8, "Due Date", 1, 0, 'C', True)
        pdf.cell(40, 8, "Amount", 1, 0, 'C', True)
        pdf.cell(40, 8, "Status", 1, 1, 'C', True)
        
        pdf.set_font(font_name, '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(60, 8, f"Installment {invoice['installment_number']}", 1, 0, 'C')
        pdf.cell(40, 8, invoice['due_date'], 1, 0, 'C')
        pdf.cell(40, 8, f"{invoice['amount_due']:,.2f} EUR", 1, 0, 'C')
        
        status_color = {'pending': (255, 193, 7), 'paid': (76, 175, 80), 'overdue': (244, 67, 54)}
        color = status_color.get(invoice['status'], (128, 128, 128))
        pdf.set_text_color(*color)
        pdf.cell(40, 8, invoice['status'].upper(), 1, 1, 'C')
        pdf.set_text_color(0, 0, 0)
        
        # غرامة التأخير إن وجدت
        if invoice.get('late_fee', 0) > 0:
            pdf.set_text_color(244, 67, 54)
            pdf.cell(100, 8, "Late Fee:", 1, 0, 'C')
            pdf.cell(80, 8, f"{invoice['late_fee']:,.2f} EUR", 1, 1, 'C')
            pdf.set_text_color(0, 0, 0)
        
        # الإجمالي
        total_due = invoice['amount_due'] + invoice.get('late_fee', 0) - invoice.get('amount_paid', 0)
        pdf.set_font(font_name, 'B', 11)
        pdf.cell(100, 10, "TOTAL DUE:", 1, 0, 'R')
        pdf.set_text_color(76, 175, 80)
        pdf.cell(80, 10, f"{total_due:,.2f} EUR", 1, 1, 'C')
        pdf.set_text_color(0, 0, 0)
        
        pdf.ln(10)
        
        # === QR Code ===
        qr_data = self._generate_qr_data(invoice, contract_data)
        qr_image = self._create_qr_image(qr_data)
        
        # حفظ QR مؤقتاً
        qr_temp_path = self.output_dir / f"temp_qr_{invoice_id}.png"
        qr_image.save(str(qr_temp_path))
        
        pdf.set_font(font_name, '', 9)
        pdf.cell(0, 6, "Scan to Pay:", ln=True, align='C')
        pdf.image(str(qr_temp_path), x=80, w=50)
        
        # حذف الـ QR المؤقت
        qr_temp_path.unlink(missing_ok=True)
        
        pdf.ln(5)
        pdf.set_font(font_name, '', 8)
        pdf.cell(0, 5, f"QR Hash: {invoice.get('qr_hash', 'N/A')[:16]}...", ln=True, align='C')
        if invoice.get('previous_qr_hash'):
            pdf.cell(0, 5, f"Previous Hash: {invoice['previous_qr_hash'][:16]}...", ln=True, align='C')
        
        # === التذييل ===
        pdf.set_y(-25)
        pdf.set_font(font_name, '', 8)
        pdf.cell(0, 5, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
        pdf.cell(0, 5, f"{Config.CONTACT_EMAIL} | {Config.SUPPORT_PHONE}", align='C')
        
        pdf.output(str(file_path))
        return str(file_path)

    def generate_all_invoices(self, contract_id: int) -> str:
        """توليد جميع فواتير العقد في ملف PDF واحد - 3 فواتير في كل صفحة A4"""
        # جلب بيانات العقد والمستخدم مع حقول العنوان
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Try contracts table first with full user data including address
            cursor.execute("""
                SELECT c.*, u.full_name, u.id_number, u.phone,
                       u.street_name, u.building_number, u.postal_code, u.city
                FROM contracts c 
                JOIN users u ON c.user_id = u.id 
                WHERE c.id = ?
            """, (contract_id,))
            row = cursor.fetchone()
            
            if row is None:
                # Fallback to transactions table
                cursor.execute("""
                    SELECT t.*, u.full_name, u.id_number, u.phone,
                           u.street_name, u.building_number, u.postal_code, u.city
                    FROM transactions t 
                    JOIN users u ON t.user_id = u.id 
                    WHERE t.id = ?
                """, (contract_id,))
                row = cursor.fetchone()
            
            if row is None:
                raise ValueError(f"Contract/Transaction {contract_id} not found")
            
            contract = dict(row)
            
            # Check if invoices table exists and has records
            try:
                cursor.execute("SELECT * FROM invoices WHERE contract_id = ? ORDER BY installment_number", (contract_id,))
                invoice_rows = cursor.fetchall()
            except Exception:
                # Table doesn't exist yet
                invoice_rows = []
            
            if not invoice_rows:
                # No invoices exist - create a simple summary PDF instead
                return self._generate_summary_pdf(contract_id, contract)
            
            invoices = [dict(r) for r in invoice_rows]
        
        # بناء بيانات المستخدم مع العنوان الكامل
        user_data = {
            'full_name': contract.get('full_name', 'N/A'),
            'id_number': contract.get('id_number'),
            'phone': contract.get('phone', ''),
            'street_name': contract.get('street_name', ''),
            'building_number': contract.get('building_number', ''),
            'postal_code': contract.get('postal_code', ''),
            'city': contract.get('city', '')
        }
        # العنوان الكامل
        address_parts = [
            user_data.get('street_name', ''),
            user_data.get('building_number', ''),
            user_data.get('postal_code', ''),
            user_data.get('city', '')
        ]
        user_data['full_address'] = ' - '.join([p for p in address_parts if p])
        
        filename = f"All_Invoices_Contract_{contract_id}_{datetime.now().strftime('%Y%m%d')}.pdf"
        file_path = self.output_dir / filename
        
        pdf = FPDF()
        font_name = None
        
        # طباعة 3 فواتير في كل صفحة
        invoices_per_page = 3
        invoice_height = 90  # ارتفاع كل فاتورة بالمليمتر
        
        for i, invoice in enumerate(invoices):
            # إضافة صفحة جديدة كل 3 فواتير
            if i % invoices_per_page == 0:
                pdf.add_page()
                if font_name is None:
                    font_name = self._setup_fonts(pdf)
            
            # حساب موقع الفاتورة في الصفحة
            position_in_page = i % invoices_per_page
            y_start = 10 + (position_in_page * invoice_height)
            
            self._render_compact_invoice(pdf, font_name, invoice, contract, user_data, y_start)
            
            # خط فاصل بين الفواتير
            if position_in_page < invoices_per_page - 1 and i < len(invoices) - 1:
                pdf.set_draw_color(200, 200, 200)
                pdf.line(10, y_start + invoice_height - 5, 200, y_start + invoice_height - 5)
        
        pdf.output(str(file_path))
        return str(file_path)
    
    def _render_compact_invoice(self, pdf, font_name, invoice, contract, user_data, y_start):
        """رسم فاتورة مضغوطة - 3 في صفحة واحدة"""
        pdf.set_y(y_start)
        
        # === الترويسة - سطر واحد ===
        pdf.set_font(font_name, 'B', 10)
        pdf.set_fill_color(30, 30, 50)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 6, f"Invoice: {invoice['invoice_number']} | Contract: #{contract['id']} | Installment: {invoice['installment_number']}", 0, 1, 'C', True)
        pdf.set_text_color(0, 0, 0)
        
        # === بيانات العميل والعنوان ===
        pdf.set_font(font_name, '', 8)
        
        # الاسم والعنوان في سطر واحد
        customer_name = fix_arabic(user_data.get('full_name', 'N/A'))
        full_address = user_data.get('full_address', '-')
        pdf.cell(95, 5, f"Customer: {customer_name}", 0, 0)
        pdf.cell(95, 5, f"Address: {full_address}", 0, 1)
        
        # === جدول الفاتورة المضغوط ===
        pdf.set_font(font_name, 'B', 8)
        pdf.set_fill_color(79, 172, 254)
        pdf.set_text_color(255, 255, 255)
        
        col_widths = [45, 35, 35, 35, 40]
        headers = ["Description", "Due Date", "Amount", "Status", "QR Scan to Pay"]
        
        for j, (header, width) in enumerate(zip(headers, col_widths)):
            pdf.cell(width, 5, header, 1, 0, 'C', True)
        pdf.ln()
        
        pdf.set_font(font_name, '', 8)
        pdf.set_text_color(0, 0, 0)
        
        # صف البيانات
        pdf.cell(col_widths[0], 5, f"Installment {invoice['installment_number']}", 1, 0, 'C')
        pdf.cell(col_widths[1], 5, invoice['due_date'], 1, 0, 'C')
        pdf.cell(col_widths[2], 5, f"{invoice['amount_due']:,.2f} EUR", 1, 0, 'C')
        
        # حالة الدفع بلون
        status = invoice['status'].upper()
        status_colors = {'PENDING': (255, 193, 7), 'PAID': (76, 175, 80), 'OVERDUE': (244, 67, 54)}
        color = status_colors.get(status, (128, 128, 128))
        pdf.set_text_color(*color)
        pdf.cell(col_widths[3], 5, status, 1, 0, 'C')
        pdf.set_text_color(0, 0, 0)
        
        # QR Code
        qr_x = pdf.get_x()
        qr_y = pdf.get_y()
        pdf.cell(col_widths[4], 5, "", 1, 1, 'C')  # خلية فارغة للـ QR
        
        # إنشاء QR كود صغير
        qr_data = self._generate_qr_data(invoice, contract)
        qr_img = self._create_qr_image(qr_data)
        qr_temp = self.output_dir / f"temp_qr_{invoice['id']}_{contract['id']}.png"
        qr_img.save(str(qr_temp))
        
        # وضع QR في الخلية
        try:
            pdf.image(str(qr_temp), x=qr_x + 2, y=qr_y - 25, w=35)
        except:
            pass
        qr_temp.unlink(missing_ok=True)
        
        # === الإجمالي وغرامة التأخير ===
        total_due = invoice['amount_due'] + invoice.get('late_fee', 0) - invoice.get('amount_paid', 0)
        late_fee = invoice.get('late_fee', 0)
        
        pdf.set_font(font_name, '', 7)
        if late_fee > 0:
            pdf.set_text_color(244, 67, 54)
            pdf.cell(95, 4, f"Late Fee: {late_fee:,.2f} EUR", 0, 0, 'L')
            pdf.set_text_color(0, 0, 0)
        else:
            pdf.cell(95, 4, "", 0, 0)
        
        pdf.set_font(font_name, 'B', 8)
        pdf.set_text_color(76, 175, 80)
        pdf.cell(95, 4, f"TOTAL: {total_due:,.2f} EUR", 0, 1, 'R')
        pdf.set_text_color(0, 0, 0)
        
        # === رقم الفاتورة تحت الفاتورة ===
        pdf.set_font(font_name, '', 7)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 4, f"Invoice No: {invoice['invoice_number']}", 0, 1, 'C')
        pdf.set_text_color(0, 0, 0)
    
    def _generate_summary_pdf(self, contract_id: int, contract: dict) -> str:
        """توليد فواتير أقساط تلقائية بناءً على بيانات العقد"""
        filename = f"Invoices_Contract_{contract_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        file_path = self.output_dir / filename
        
        # استخراج بيانات الأقساط من العقد
        installment_count = int(contract.get('installment_count', 0))
        monthly_amount = float(contract.get('monthly_installment', 0))
        total_price = float(contract.get('estimated_price', contract.get('total_price', 0)))
        down_payment = float(contract.get('down_payment', 0))
        
        # إذا لم يكن هناك أقساط، توليد فاتورة واحدة (كاش)
        if installment_count <= 0 or monthly_amount <= 0:
            installment_count = 1
            monthly_amount = total_price - down_payment
        
        # بناء بيانات المستخدم
        user_data = {
            'full_name': contract.get('full_name', 'N/A'),
            'id_number': contract.get('id_number', ''),
            'phone': contract.get('phone', ''),
            'street_name': contract.get('street_name', ''),
            'building_number': contract.get('building_number', ''),
            'postal_code': contract.get('postal_code', ''),
            'city': contract.get('city', '')
        }
        address_parts = [
            user_data.get('street_name', ''),
            user_data.get('building_number', ''),
            user_data.get('postal_code', ''),
            user_data.get('city', '')
        ]
        user_data['full_address'] = ' - '.join([p for p in address_parts if p]) or 'N/A'
        
        pdf = FPDF()
        font_name = self._setup_fonts(pdf)
        
        # توليد فواتير وهمية بناءً على عدد الأقساط
        invoices_per_page = 3
        invoice_height = 90
        
        for i in range(installment_count):
            # إضافة صفحة جديدة كل 3 فواتير
            if i % invoices_per_page == 0:
                pdf.add_page()
            
            # حساب موقع الفاتورة في الصفحة
            position_in_page = i % invoices_per_page
            y_start = 10 + (position_in_page * invoice_height)
            
            # إنشاء بيانات فاتورة وهمية
            from dateutil.relativedelta import relativedelta
            try:
                start_date = datetime.strptime(str(contract.get('created_at', ''))[:10], '%Y-%m-%d')
            except:
                start_date = datetime.now()
            
            due_date = (start_date + relativedelta(months=i+1)).strftime('%Y-%m-%d')
            
            invoice = {
                'id': i + 1,
                'invoice_number': f"INV-{contract_id}-{i+1:03d}",
                'installment_number': i + 1,
                'amount_due': monthly_amount,
                'due_date': due_date,
                'status': 'pending',
                'late_fee': 0,
                'amount_paid': 0
            }
            
            self._render_compact_invoice(pdf, font_name, invoice, contract, user_data, y_start)
            
            # خط فاصل بين الفواتير
            if position_in_page < invoices_per_page - 1 and i < installment_count - 1:
                pdf.set_draw_color(200, 200, 200)
                pdf.line(10, y_start + invoice_height - 5, 200, y_start + invoice_height - 5)
        
        pdf.output(str(file_path))
        return str(file_path)

    def _setup_fonts(self, pdf) -> str:
        """إعداد الخطوط"""
        font_name = "Arial"
        if self.font_path and os.path.exists(self.font_path):
            try:
                pdf.add_font('CustomFont', '', self.font_path, uni=True)
                pdf.add_font('CustomFont', 'B', self.font_bold_path, uni=True)
                font_name = 'CustomFont'
            except:
                pass
        return font_name

    def _render_invoice_page(self, pdf, font_name, invoice, contract, user_data):
        """رسم صفحة فاتورة واحدة"""
        # ترويسة بسيطة
        pdf.set_font(font_name, 'B', 14)
        pdf.cell(0, 10, f"Invoice: {invoice['invoice_number']}", ln=True, align='C')
        pdf.set_font(font_name, '', 10)
        pdf.cell(0, 6, f"Contract #{contract['id']} | Installment {invoice['installment_number']}/{contract['installment_count']}", ln=True, align='C')
        pdf.ln(10)
        
        # التفاصيل
        pdf.set_font(font_name, '', 11)
        pdf.cell(50, 8, "Customer:", 0, 0)
        pdf.cell(0, 8, user_data.get('full_name', 'N/A'), 0, 1)
        pdf.cell(50, 8, "Vehicle:", 0, 0)
        pdf.cell(0, 8, f"{contract.get('vehicle_type', '')} {contract.get('vehicle_model', '')}", 0, 1)
        pdf.cell(50, 8, "Due Date:", 0, 0)
        pdf.cell(0, 8, invoice['due_date'], 0, 1)
        pdf.cell(50, 8, "Amount:", 0, 0)
        pdf.set_font(font_name, 'B', 11)
        pdf.cell(0, 8, f"{invoice['amount_due']:,.2f} EUR", 0, 1)
        pdf.set_font(font_name, '', 11)
        pdf.cell(50, 8, "Status:", 0, 0)
        pdf.cell(0, 8, invoice['status'].upper(), 0, 1)
        
        # QR
        qr_data = self._generate_qr_data(invoice, contract)
        qr_img = self._create_qr_image(qr_data)
        qr_temp = self.output_dir / f"temp_qr_{invoice['id']}.png"
        qr_img.save(str(qr_temp))
        pdf.ln(10)
        pdf.image(str(qr_temp), x=75, w=60)
        qr_temp.unlink(missing_ok=True)

    def _generate_qr_data(self, invoice: dict, contract: dict, customer_name: str = None) -> str:
        """توليد بيانات QR تتضمن:
        1. اسم العميل
        2. رقم الفاتورة
        3. رقم القسط
        4. مقدار القسط
        5. تاريخ تسديد القسط
        """
        company_name = Config.APP_NAME
        company_iban = "DE01234567890123123"
        company_bic = "SMART12345"
        
        # استخراج اسم العميل
        if customer_name is None:
            customer_name = contract.get('full_name', 'N/A')
        
        # بيانات الفاتورة
        invoice_number = invoice.get('invoice_number', 'N/A')
        installment_number = invoice.get('installment_number', 1)
        amount = invoice.get('amount_due', 0)
        due_date = invoice.get('due_date', 'N/A')
        
        # سبب التحويل مع كل البيانات المطلوبة
        verwendungszweck = f"Installment {installment_number}/{contract.get('installment_count', 1)} - {invoice_number}"
        
        # صيغة EPC QR مع كل البيانات
        qr_content = f"""BCD
002
1
SCT
{company_bic}
{company_name}
{company_iban}
EUR{amount:.2f}

{verwendungszweck}
Customer: {customer_name}
Invoice: {invoice_number}
Installment: {installment_number}
Amount: {amount:.2f} EUR
Due Date: {due_date}"""
        
        return qr_content

    def _create_qr_image(self, data: str):
        """توليد صورة QR"""
        qr = qrcode.QRCode(box_size=6, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        return qr.make_image(fill_color="#0E1117", back_color="white")
