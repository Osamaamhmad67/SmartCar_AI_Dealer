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