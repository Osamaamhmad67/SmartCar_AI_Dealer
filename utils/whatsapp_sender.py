"""
utils/whatsapp_sender.py - WhatsApp Notifications
SmartCar AI-Dealer
"""
import urllib.parse


class WhatsAppSender:
    """Send WhatsApp messages via wa.me links and API"""

    @staticmethod
    def generate_link(phone: str, message: str) -> str:
        """Generate WhatsApp click-to-chat link"""
        phone_clean = phone.replace('+', '').replace(' ', '').replace('-', '')
        msg_encoded = urllib.parse.quote(message)
        return f"https://wa.me/{phone_clean}?text={msg_encoded}"

    @staticmethod
    def send_reminder(phone: str, customer_name: str, car_info: str, amount: float, due_date: str) -> str:
        """Generate installment reminder WhatsApp link"""
        message = (
            f"🏎️ SmartCar AI-Dealer\n\n"
            f"Sehr geehrte/r {customer_name},\n\n"
            f"Dies ist eine freundliche Erinnerung an Ihre fällige Rate:\n\n"
            f"🚗 Fahrzeug: {car_info}\n"
            f"💰 Betrag: €{amount:,.2f}\n"
            f"📅 Fällig am: {due_date}\n\n"
            f"Bitte überweisen Sie den Betrag rechtzeitig.\n\n"
            f"Mit freundlichen Grüßen\n"
            f"SmartCar AI-Dealer Team"
        )
        return WhatsAppSender.generate_link(phone, message)

    @staticmethod
    def send_tuv_reminder(phone: str, customer_name: str, car_info: str, tuv_date: str) -> str:
        """Generate TÜV reminder WhatsApp link"""
        message = (
            f"🏎️ SmartCar AI-Dealer\n\n"
            f"Sehr geehrte/r {customer_name},\n\n"
            f"⚠️ TÜV-Erinnerung:\n\n"
            f"🚗 Fahrzeug: {car_info}\n"
            f"📅 TÜV-Ablauf: {tuv_date}\n\n"
            f"Bitte vereinbaren Sie rechtzeitig einen TÜV-Termin.\n\n"
            f"Mit freundlichen Grüßen\n"
            f"SmartCar AI-Dealer Team"
        )
        return WhatsAppSender.generate_link(phone, message)

    @staticmethod
    def send_welcome(phone: str, customer_name: str) -> str:
        """Generate welcome message link"""
        message = (
            f"🏎️ Willkommen bei SmartCar AI-Dealer!\n\n"
            f"Hallo {customer_name},\n\n"
            f"Vielen Dank für Ihr Vertrauen! 🎉\n"
            f"Wir freuen uns, Sie als Kunden begrüßen zu dürfen.\n\n"
            f"Bei Fragen stehen wir Ihnen jederzeit zur Verfügung.\n\n"
            f"Mit freundlichen Grüßen\n"
            f"SmartCar AI-Dealer Team"
        )
        return WhatsAppSender.generate_link(phone, message)
