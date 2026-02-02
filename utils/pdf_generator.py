"""
utils/pdf_generator.py - المولد الأساسي لملفات PDF
SmartCar AI-Dealer
إدارة إعدادات الصفحات، الخطوط، وتنسيقات المستندات العامة
"""

from fpdf import FPDF
from config import Config
from datetime import datetime

class PDFGenerator(FPDF):
    """كلاس قاعدي مخصص لتوليد مستندات PDF بهوية النظام الموحدة"""

    def __init__(self):
        super().__init__()
        self.app_name = Config.APP_NAME
        self.add_font_support()

    def add_font_support(self):
        """إضافة دعم الخطوط العربية واللاتينية المحددة في الإعدادات"""
        # جلب مسارات الخطوط من ملف الإعدادات
        regular_font = str(Config.FONTS_DIR / Config.FONT_REGULAR)
        bold_font = str(Config.FONTS_DIR / Config.FONT_BOLD)

        # محاولة تحميل الخطوط (تتطلب وجود ملفات الخطوط في مجلد fonts)
        try:
            # استخدام Cairo لدعم اللغة العربية بشكل احترافي
            self.add_font("Cairo", "", regular_font, unicode=True)
            self.add_font("Cairo", "B", bold_font, unicode=True)
        except Exception:
            # في حال عدم توفر ملفات الخطوط، النظام سيعتمد على Arial كبديل افتراضي
            pass

    def header(self):
        """تعريف الترويسة الموحدة لكل صفحات المستند"""
        # تعيين اللون الذهبي الخاص بالعلامة التجارية
        self.set_text_color(184, 134, 11) # Dark Goldenrod
        self.set_font("Arial", 'B', 16)
        
        # اسم الشركة في الأعلى
        self.cell(0, 10, self.app_name, ln=True, align='L')
        
        # تاريخ وتوقيت الإصدار في الجهة المقابلة
        self.set_font("Arial", 'I', 8)
        self.set_text_color(100)
        self.cell(0, 10, f"Document Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='R')
        
        # رسم خط فاصل جمالي
        self.set_draw_color(184, 134, 11)
        self.set_line_width(0.5)
        self.line(10, 32, 200, 32)
        self.ln(15)

    def footer(self):
        """تعريف تذييل الصفحة الموحد"""
        # الانتقال إلى 1.5 سم من أسفل الصفحة
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.set_text_color(150)
        
        # رقم الصفحة وحقوق الملكية لعام 2026
        page_text = f"Page {self.page_no()} | {self.app_name} Financial Systems © 2026"
        self.cell(0, 10, page_text, align='C')

    def create_styled_table(self, header, data):
        """دالة مساعدة لإنشاء جداول بيانات منسقة واحترافية"""
        self.set_font("Arial", 'B', 12)
        self.set_fill_color(245, 245, 245) # رمادي فاتح جداً للخلفية
        
        # رسم الرؤوس
        for col in header:
            self.cell(95, 10, col, 1, 0, 'C', True)
        self.ln()

        # رسم البيانات
        self.set_font("Arial", '', 11)
        self.set_text_color(50)
        for row in data:
            self.cell(95, 10, str(row[0]), 1)
            self.cell(95, 10, str(row[1]), 1)
            self.ln()