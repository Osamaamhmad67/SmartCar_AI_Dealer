"""
utils/notifier.py - مدير الإشعارات المتكامل
SmartCar AI-Dealer
إدارة تنبيهات النظام، رسائل البريد الإلكتروني، وإشعارات واجهة المستخدم
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import streamlit as st
from config import Config

class NotificationManager:
    """مسؤول عن إرسال الإشعارات عبر قنوات مختلفة (Email, UI, System)"""

    def __init__(self):
        self.logger = Config.logger
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.sender_email = Config.SENDER_EMAIL
        self.sender_password = Config.SENDER_PASSWORD
        self.app_name = Config.APP_NAME

    @property
    def email_configured(self) -> bool:
        """التحقق من صحة إعدادات البريد الإلكتروني"""
        return bool(self.sender_email and self.sender_password and self.smtp_server)

    def send_invoice_email(self, recipient_email: str, invoice_path: str, user_data: dict, transaction_data: dict) -> dict:
        """إرسال الفاتورة مع المرفق"""
        from email.mime.application import MIMEApplication
        from pathlib import Path

        if not self.email_configured:
            return {'success': False, 'message': 'Email not configured'}

        try:
            subject = f"فاتورة تقييم سيارة: {transaction_data.get('brand')} {transaction_data.get('model')}"
            body = f"""
            <h3>مرحباً {user_data.get('full_name')}،</h3>
            <p>شكراً لاستخدامك {self.app_name}.</p>
            <p>مرفق طيه فاتورة تقييم سيارتك.</p>
            <br>
            <p>مع تحيات فريق العمل،</p>
            <p>{self.app_name}</p>
            """
            
            msg = MIMEMultipart()
            msg['From'] = f"{Config.SENDER_NAME} <{self.sender_email}>"
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))

            # إرفاق ملف الفاتورة
            path = Path(invoice_path)
            if path.exists():
                with open(path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=path.name)
                part['Content-Disposition'] = f'attachment; filename="{path.name}"'
                msg.attach(part)
            else:
                return {'success': False, 'message': 'Invoice file not found'}

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            return {'success': True, 'message': 'Email sent successfully'}

        except Exception as e:
            if self.logger: self.logger.error(f"Email error: {e}")
            return {'success': False, 'message': str(e)}

    def send_email(self, recipient_email: str, subject: str, body: str, is_html: bool = False) -> bool:
        """إرسال رسالة بريد إلكتروني رسمية"""
        if not self.sender_email or not self.sender_password:
            if self.logger: self.logger.warning("⚠️ إعدادات SMTP غير مكتملة. لم يتم إرسال البريد.")
            return False

        try:
            msg = MIMEMultipart()
            msg['From'] = f"{Config.SENDER_NAME} <{self.sender_email}>"
            msg['To'] = recipient_email
            msg['Subject'] = subject

            content_type = 'html' if is_html else 'plain'
            msg.attach(MIMEText(body, content_type))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # تأمين الاتصال
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            if self.logger: self.logger.info(f"📧 تم إرسال بريد بنجاح إلى: {recipient_email}")
            return True

        except Exception as e:
            if self.logger: self.logger.error(f"❌ فشل إرسال البريد الإلكتروني: {str(e)}")
            return False

    def notify_admin_of_high_value(self, car_details: dict, estimated_price: float):
        """إخطار المشرف عند تقييم سيارة ذات قيمة عالية (أكبر من 100,000 يورو)"""
        if estimated_price > 100000:
            subject = f"🚨 High Value Car Alert: {car_details.get('brand')} {car_details.get('model')}"
            body = f"""
            <h3>High Value Appraisal Detected</h3>
            <p>A car with estimated value of <b>{estimated_price:,.2f} €</b> has been processed.</p>
            <ul>
                <li><b>User:</b> {st.session_state.get('user', {}).get('full_name', 'Guest')}</li>
                <li><b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
            </ul>
            """
            self.send_email(Config.CONTACT_EMAIL, subject, body, is_html=True)

    @staticmethod
    def show_ui_message(message: str, type: str = "success"):
        """عرض رسائل ملونة في واجهة Streamlit"""
        if type == "success":
            st.success(f"✅ {message}")
        elif type == "error":
            st.error(f"❌ {message}")
        elif type == "warning":
            st.warning(f"⚠️ {message}")
        elif type == "info":
            st.info(f"ℹ️ {message}")

    def send_invoice_notification(self, user_email: str, invoice_path: str):
        """إرسال رابط الفاتورة أو تأكيد صدورها للمستخدم"""
        subject = f"Your Car Appraisal Invoice - {self.app_name}"
        body = f"Hello, your car appraisal report has been generated. You can find it in your dashboard under the history section."
        self.send_email(user_email, subject, body)

    def check_upcoming_installments(self, days_ahead: int = 3) -> list:
        """فحص الأقساط القادمة خلال عدد أيام محدد"""
        from db_manager import DatabaseManager
        db = DatabaseManager()
        results = []
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT i.id, i.amount_due, i.due_date, i.installment_number,
                           c.id as contract_id, u.email, u.full_name,
                           u.first_name, u.last_name
                    FROM invoices i
                    JOIN contracts c ON i.contract_id = c.id
                    JOIN users u ON c.user_id = u.id
                    WHERE i.status = 'pending'
                    AND i.due_date BETWEEN date('now') AND date('now', '+' || ? || ' days')
                    ORDER BY i.due_date ASC
                """, (days_ahead,))
                columns = [desc[0] for desc in cursor.description]
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error checking installments: {e}")
        return results

    def send_installment_reminder(self, installment_data: dict) -> bool:
        """إرسال تذكير بالقسط عبر البريد الإلكتروني"""
        email = installment_data.get('email', '')
        if not email:
            return False
        
        name = installment_data.get('full_name') or f"{installment_data.get('first_name', '')} {installment_data.get('last_name', '')}".strip()
        amount = installment_data.get('amount_due', 0)
        due_date = installment_data.get('due_date', '')
        inst_num = installment_data.get('installment_number', 0)
        contract_id = installment_data.get('contract_id', '')
        
        subject = f"⏰ Payment Reminder - Installment #{inst_num} - {self.app_name}"
        body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0;">🏎️ {self.app_name}</h1>
                <p style="color: rgba(255,255,255,0.8);">Payment Reminder / Zahlungserinnerung</p>
            </div>
            <div style="background: #1a1a2e; padding: 30px; color: white;">
                <h2 style="color: #D4AF37;">Dear {name},</h2>
                <p>This is a friendly reminder that your installment payment is due soon:</p>
                <div style="background: #16213e; padding: 20px; border-radius: 10px; border-left: 4px solid #D4AF37; margin: 20px 0;">
                    <p><strong>Contract:</strong> #{contract_id}</p>
                    <p><strong>Installment:</strong> #{inst_num}</p>
                    <p><strong>Amount:</strong> <span style="color: #4CAF50; font-size: 1.3em;">€{amount:,.2f}</span></p>
                    <p><strong>Due Date:</strong> <span style="color: #FF9800;">{due_date}</span></p>
                </div>
                <p>Please ensure timely payment to avoid late fees.</p>
                <p style="color: #a0a0c0; font-size: 0.9em; margin-top: 30px;">Best regards,<br>{self.app_name} Team</p>
            </div>
        </div>
        """
        return self.send_email(email, subject, body, is_html=True)

    def check_tuv_expiry(self, days_ahead: int = 30) -> list:
        """فحص السيارات التي ينتهي فحصها TÜV خلال عدد أيام محدد"""
        from db_manager import DatabaseManager
        db = DatabaseManager()
        results = []
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT t.id, t.brand, t.model, t.manufacture_year,
                           u.email, u.full_name, u.first_name, u.last_name,
                           c.vehicle_plate
                    FROM transactions t
                    JOIN users u ON t.user_id = u.id
                    LEFT JOIN contracts c ON c.transaction_id = t.id
                    WHERE t.created_at >= date('now', '-1 year')
                    ORDER BY t.created_at DESC
                """)
                columns = [desc[0] for desc in cursor.description]
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error checking TÜV: {e}")
        return results

    def send_tuv_reminder(self, car_data: dict) -> bool:
        """إرسال تذكير بانتهاء TÜV"""
        email = car_data.get('email', '')
        if not email:
            return False
        
        name = car_data.get('full_name') or f"{car_data.get('first_name', '')} {car_data.get('last_name', '')}".strip()
        brand = car_data.get('brand', '')
        model = car_data.get('model', '')
        plate = car_data.get('vehicle_plate', 'N/A')

        subject = f"⚠️ TÜV Reminder - {brand} {model} - {self.app_name}"
        body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #f39c12 0%, #e74c3c 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0;">🏎️ {self.app_name}</h1>
                <p style="color: rgba(255,255,255,0.8);">TÜV Reminder / TÜV-Erinnerung</p>
            </div>
            <div style="background: #1a1a2e; padding: 30px; color: white;">
                <h2 style="color: #f39c12;">Dear {name},</h2>
                <p>Your vehicle TÜV inspection is expiring soon:</p>
                <div style="background: #16213e; padding: 20px; border-radius: 10px; border-left: 4px solid #f39c12; margin: 20px 0;">
                    <p><strong>Vehicle:</strong> {brand} {model}</p>
                    <p><strong>Plate:</strong> {plate}</p>
                </div>
                <p>Please schedule a TÜV inspection appointment as soon as possible.</p>
                <p style="color: #a0a0c0; font-size: 0.9em; margin-top: 30px;">Best regards,<br>{self.app_name} Team</p>
            </div>
        </div>
        """
        return self.send_email(email, subject, body, is_html=True)

    def run_all_reminders(self) -> dict:
        """تشغيل جميع التذكيرات دفعة واحدة"""
        results = {'installments_sent': 0, 'installments_found': 0, 'tuv_found': 0, 'errors': []}
        
        # Installment reminders
        upcoming = self.check_upcoming_installments(days_ahead=7)
        results['installments_found'] = len(upcoming)
        for inst in upcoming:
            try:
                if self.send_installment_reminder(inst):
                    results['installments_sent'] += 1
            except Exception as e:
                results['errors'].append(str(e))
        
        # TÜV reminders
        tuv_cars = self.check_tuv_expiry(days_ahead=30)
        results['tuv_found'] = len(tuv_cars)
        
        return results
