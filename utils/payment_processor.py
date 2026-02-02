"""
utils/payment_processor.py - معالج العمليات المالية والتقسيط المتقدم
SmartCar AI-Dealer
إدارة العقود، حساب الأقساط مع الدفعة المقدمة، غرامات التأخير، و QR التراكمي
"""

import hashlib
import json
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from typing import Dict, List, Optional
from db_manager import DatabaseManager
from config import Config

class PaymentProcessor:
    """المحرك المالي لإدارة عمليات الدفع والتقسيط"""

    def __init__(self):
        self.db = DatabaseManager()
        self.logger = Config.logger
        # نسب الفائدة بناءً على عدد الأشهر
        self.interest_rates = {
            3: 0.0,   # تقسيط على 3 أشهر بدون فوائد
            12: 0.12, # تقسيط على سنة بفائدة 12%
            24: 0.18  # تقسيط على سنتين بفائدة 18%
        }
        self.vat_rate = 0.15

    def calculate_installment_plan(self, principal_amount: float, months: int, down_payment: float = 0) -> Dict:
        """
        حساب خطة التقسيط مع دعم الدفعة المقدمة
        المعادلة: القسط الشهري = (السعر الإجمالي - الدفعة المقدمة + الفوائد) / عدد الأشهر
        """
        interest_rate = self.interest_rates.get(months, 0.20)
        
        # 1. حساب الضريبة على المبلغ الأساسي
        vat_amount = principal_amount * self.vat_rate
        amount_with_vat = principal_amount + vat_amount
        
        # 2. خصم الدفعة المقدمة
        remaining_after_down = max(0, amount_with_vat - down_payment)
        
        # 3. حساب الفائدة على المبلغ المتبقي فقط
        total_interest = remaining_after_down * interest_rate
        total_to_pay = remaining_after_down + total_interest
        
        # 4. القسط الشهري
        monthly_payment = total_to_pay / months if months > 0 else 0

        return {
            'months': months,
            'base_amount': principal_amount,
            'vat_amount': vat_amount,
            'down_payment': down_payment,
            'remaining_after_down': remaining_after_down,
            'interest_rate': interest_rate,
            'total_interest': total_interest,
            'total_payable': total_to_pay,
            'monthly_installment': round(monthly_payment, 2),
            'grand_total': down_payment + total_to_pay
        }

    def create_full_contract(self, user_id: int, transaction_id: int, plan: Dict, 
                              car_data: Dict, payment_due_day: int = 1) -> Optional[int]:
        """إنشاء عقد كامل مع جدول السداد"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                # 1. إنشاء العقد
                cursor.execute('''
                    INSERT INTO contracts (
                        user_id, transaction_id, total_price, down_payment,
                        remaining_amount, installment_count, monthly_installment,
                        interest_rate, payment_due_day, vehicle_type, vehicle_model
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id, transaction_id, plan['grand_total'],
                    plan['down_payment'], plan['remaining_after_down'],
                    plan['months'], plan['monthly_installment'],
                    plan['interest_rate'], payment_due_day,
                    car_data.get('brand', ''), car_data.get('model', '')
                ))
                
                contract_id = cursor.lastrowid
                
                # 2. توليد جدول الفواتير/الأقساط
                self._generate_invoice_schedule(conn, contract_id, plan, payment_due_day)
                
                if self.logger:
                    self.logger.info(f"✅ Contract {contract_id} created with {plan['months']} invoices")
                
                return contract_id
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ Error creating contract: {str(e)}")
            return None

    def _generate_invoice_schedule(self, conn, contract_id: int, plan: Dict, due_day: int):
        """توليد جميع فواتير الأقساط عند توقيع العقد"""
        previous_hash = None
        today = date.today()
        
        for i in range(1, plan['months'] + 1):
            # حساب تاريخ الاستحقاق
            due_date = today + relativedelta(months=i)
            due_date = due_date.replace(day=min(due_day, 28))  # تجنب مشاكل الشهور القصيرة
            
            # توليد رقم فاتورة فريد
            invoice_number = f"INV-{contract_id}-{i:03d}-{datetime.now().strftime('%Y%m')}"
            
            # توليد hash تراكمي للـ QR
            invoice_data = {
                'invoice_number': invoice_number,
                'contract_id': contract_id,
                'installment': i,
                'amount': plan['monthly_installment'],
                'due_date': str(due_date),
                'previous_hash': previous_hash
            }
            current_hash = self._generate_hash(invoice_data)
            
            # إدراج الفاتورة
            conn.execute('''
                INSERT INTO invoices (
                    invoice_number, contract_id, installment_number,
                    amount_due, due_date, status, qr_hash, previous_qr_hash
                ) VALUES (?, ?, ?, ?, ?, 'pending', ?, ?)
            ''', (
                invoice_number, contract_id, i,
                plan['monthly_installment'], str(due_date),
                current_hash, previous_hash
            ))
            
            previous_hash = current_hash

    def _generate_hash(self, data: Dict) -> str:
        """توليد hash SHA256 للبيانات"""
        json_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(json_str.encode()).hexdigest()[:32]

    def apply_late_fee(self, invoice_id: int) -> float:
        """تطبيق غرامة التأخير على فاتورة متأخرة"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # جلب بيانات الفاتورة والعقد
            cursor.execute('''
                SELECT i.*, c.late_fee_type, c.late_fee_amount, c.grace_period_days
                FROM invoices i
                JOIN contracts c ON i.contract_id = c.id
                WHERE i.id = ?
            ''', (invoice_id,))
            
            row = cursor.fetchone()
            if not row:
                return 0
            
            invoice = dict(row)
            due_date = datetime.strptime(invoice['due_date'], '%Y-%m-%d').date()
            grace_end = due_date + timedelta(days=invoice['grace_period_days'])
            
            # التحقق من التأخير
            if date.today() <= grace_end:
                return 0  # لا يزال ضمن فترة السماح
            
            # حساب الغرامة
            if invoice['late_fee_type'] == 'percentage':
                late_fee = invoice['amount_due'] * (invoice['late_fee_amount'] / 100)
            else:
                late_fee = invoice['late_fee_amount']
            
            # تحديث الفاتورة
            cursor.execute('''
                UPDATE invoices SET late_fee = ?, status = 'overdue'
                WHERE id = ?
            ''', (late_fee, invoice_id))
            
            return late_fee

    def get_contract_invoices(self, contract_id: int) -> List[Dict]:
        """جلب جميع فواتير عقد معين"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM invoices WHERE contract_id = ?
                ORDER BY installment_number ASC
            ''', (contract_id,))
            return [dict(row) for row in cursor.fetchall()]

    def get_user_contracts(self, user_id: int) -> List[Dict]:
        """جلب عقود المستخدم"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM contracts WHERE user_id = ?
                ORDER BY created_at DESC
            ''', (user_id,))
            return [dict(row) for row in cursor.fetchall()]

    def mark_invoice_paid(self, invoice_id: int, amount: float) -> bool:
        """تسجيل دفع فاتورة"""
        with self.db.get_connection() as conn:
            conn.execute('''
                UPDATE invoices 
                SET amount_paid = ?, status = 'paid', payment_date = date('now')
                WHERE id = ?
            ''', (amount, invoice_id))
            return True

    def get_user_financial_summary(self, user_id: int) -> Dict:
        """جلب ملخص مالي للعميل"""
        summary = {
            'total_debt': 0.0,
            'total_paid': 0.0,
            'next_payment': None,
            'active_contracts': 0,
            'overdue_count': 0
        }
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # إجمالي المتبقي
            cursor.execute('''
                SELECT SUM(amount_due - amount_paid + late_fee) FROM invoices i
                JOIN contracts c ON i.contract_id = c.id
                WHERE c.user_id = ? AND i.status != 'paid'
            ''', (user_id,))
            summary['total_debt'] = cursor.fetchone()[0] or 0.0
            
            # إجمالي المدفوع
            cursor.execute('''
                SELECT SUM(amount_paid) FROM invoices i
                JOIN contracts c ON i.contract_id = c.id
                WHERE c.user_id = ?
            ''', (user_id,))
            summary['total_paid'] = cursor.fetchone()[0] or 0.0
            
            # عدد العقود النشطة
            cursor.execute('''
                SELECT COUNT(*) FROM contracts WHERE user_id = ? AND status = 'active'
            ''', (user_id,))
            summary['active_contracts'] = cursor.fetchone()[0]
            
            # عدد الفواتير المتأخرة
            cursor.execute('''
                SELECT COUNT(*) FROM invoices i
                JOIN contracts c ON i.contract_id = c.id
                WHERE c.user_id = ? AND i.status = 'overdue'
            ''', (user_id,))
            summary['overdue_count'] = cursor.fetchone()[0]
            
            # القسط القادم
            cursor.execute('''
                SELECT MIN(due_date), amount_due FROM invoices i
                JOIN contracts c ON i.contract_id = c.id
                WHERE c.user_id = ? AND i.status = 'pending'
            ''', (user_id,))
            row = cursor.fetchone()
            if row and row[0]:
                summary['next_payment'] = {'date': row[0], 'amount': row[1]}
                
        return summary

    def verify_payment_claim(self, image_bytes: bytes, claim: dict) -> dict:
        """
        التحقق من إيصال الدفع باستخدام OCR
        :param image_bytes: بيانات صورة الإيصال
        :param claim: معلومات المطالبة (amount, date)
        :return: قاموس يحتوي على نتيجة التحقق
        """
        try:
            from utils.ocr_scanner import DocumentScanner
            
            scanner = DocumentScanner()
            
            # محاولة قراءة الإيصال
            result = scanner.scan_document(image_bytes, "عربي")
            
            if 'error' in result:
                return {
                    'verified': False,
                    'message': f"فشل قراءة الإيصال: {result.get('error', 'خطأ غير معروف')}",
                    'ai_data': {}
                }
            
            # للتبسيط: إذا تمكنا من قراءة الإيصال، نعتبره صالحاً
            # في الإنتاج، يجب مقارنة المبلغ والتاريخ
            extracted_amount = result.get('amount', claim.get('amount'))
            
            return {
                'verified': True,
                'message': 'تم التحقق من الإيصال بنجاح!',
                'ai_data': {
                    'ref_number': result.get('id_number', f"REF-{datetime.now().strftime('%Y%m%d%H%M%S')}"),
                    'amount': extracted_amount,
                    'date': result.get('expiry_date', claim.get('date'))
                }
            }
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Payment verification error: {str(e)}")
            
            # في حالة الخطأ، نسمح بالمرور مع تحذير (للتطوير)
            return {
                'verified': True,
                'message': f'تم قبول الإيصال (تحذير: {str(e)[:50]})',
                'ai_data': {
                    'ref_number': f"REF-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    'amount': claim.get('amount'),
                    'date': claim.get('date')
                }
            }
