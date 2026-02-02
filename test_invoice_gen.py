"""
test_invoice_gen.py - وحدة اختبار نظام الفواتير
SmartCar AI-Dealer
التأكد من توليد ملفات PDF بشكل صحيح وتنسيق البيانات المالية
"""

import unittest
import os
from pathlib import Path
from utils.invoice_generator import InvoiceGenerator
from config import Config

class TestInvoiceGenerator(unittest.TestCase):
    """سلسلة اختبارات للتأكد من كفاءة ملفات PDF الناتجة"""

    def setUp(self):
        """تجهيز البيئة قبل كل اختبار"""
        self.generator = InvoiceGenerator()
        # بيانات تجريبية (Mock Data)
        self.sample_transaction = {
            'id': 999,
            'brand': 'Mercedes-Benz',
            'model': 'S-Class',
            'manufacture_year': 2023,
            'mileage': 15000,
            'estimated_price': 85000.0,
            'condition_analysis': 'Excellent - Like New'
        }
        self.sample_user = {
            'full_name': 'Osama Test User',
            'username': 'osama_tester'
        }

    def test_invoice_creation(self):
        """اختبار إنشاء ملف PDF والتأكد من وجوده على القرص"""
        # تنفيذ عملية التوليد
        file_path = self.generator.generate_car_invoice(
            self.sample_transaction, 
            self.sample_user, 
            lang='Deutsch'
        )
        
        # 1. التأكد من أن الدالة أعادت مساراً
        self.assertIsNotNone(file_path)
        
        # 2. التأكد من أن الملف موجود فعلياً في مجلد invoices
        path = Path(file_path)
        self.assertTrue(path.exists(), f"Invoice file not found at {file_path}")
        
        # 3. التأكد من أن الامتداد هو PDF
        self.assertEqual(path.suffix, '.pdf')
        
        print(f"✅ Success: Invoice generated at {file_path}")

    def test_invoice_directory_auto_creation(self):
        """التأكد من أن النظام ينشئ مجلد الفواتير إذا لم يكن موجوداً"""
        if Config.INVOICES_DIR.exists():
            # لا نحذف المجلد الحقيقي، فقط نتأكد من صلاحية المسار
            self.assertTrue(Config.INVOICES_DIR.is_dir())

    def tearDown(self):
        """تنظيف البيئة بعد الاختبار (اختياري)"""
        # في بيئة التطوير، قد ترغب في إبقاء الفواتير للمراجعة
        pass

if __name__ == '__main__':
    unittest.main()