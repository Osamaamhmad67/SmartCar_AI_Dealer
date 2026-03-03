"""
utils/email_templates.py - Professional HTML Email Templates
SmartCar AI-Dealer
"""


class EmailTemplates:
    """Pre-built HTML email templates"""

    HEADER = """
    <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
        <h1 style="color: #D4AF37; margin: 0;">🏎️ SmartCar AI-Dealer</h1>
    </div>
    """

    FOOTER = """
    <div style="background: #0a0a14; padding: 20px; text-align: center; color: #a0a0c0; font-size: 12px; border-radius: 0 0 10px 10px;">
        <p>© 2024 SmartCar AI-Dealer | <a href="#" style="color: #D4AF37;">Impressum</a> | <a href="#" style="color: #D4AF37;">Datenschutz</a></p>
        <p>Diese E-Mail wurde automatisch generiert.</p>
    </div>
    """

    @staticmethod
    def wrap(content: str) -> str:
        return f"""
        <div style="max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif; background: #1a1a2e;">
            {EmailTemplates.HEADER}
            <div style="padding: 30px; background: #16213e; color: white;">
                {content}
            </div>
            {EmailTemplates.FOOTER}
        </div>
        """

    @staticmethod
    def welcome(customer_name: str) -> str:
        return EmailTemplates.wrap(f"""
            <h2 style="color: #D4AF37;">Willkommen, {customer_name}! 🎉</h2>
            <p>Vielen Dank für Ihre Registrierung bei SmartCar AI-Dealer.</p>
            <p>Mit unserem KI-System können Sie:</p>
            <ul style="color: #a0a0c0;">
                <li>📷 Fahrzeuge per Foto bewerten lassen</li>
                <li>💰 Faire Marktpreise erhalten</li>
                <li>📄 Professionelle Verträge erstellen</li>
                <li>📊 Ihre Transaktionen verfolgen</li>
            </ul>
            <p style="text-align: center; margin-top: 20px;">
                <a href="#" style="background: #D4AF37; color: black; padding: 12px 30px; border-radius: 25px; text-decoration: none; font-weight: bold;">
                    Jetzt starten →
                </a>
            </p>
        """)

    @staticmethod
    def invoice(customer_name: str, invoice_id: str, amount: float, due_date: str) -> str:
        return EmailTemplates.wrap(f"""
            <h2 style="color: #D4AF37;">Rechnung #{invoice_id}</h2>
            <p>Sehr geehrte/r {customer_name},</p>
            <div style="background: #1a1a2e; padding: 20px; border-radius: 10px; margin: 15px 0; border-left: 4px solid #D4AF37;">
                <p><b>Rechnungsnummer:</b> {invoice_id}</p>
                <p><b>Betrag:</b> <span style="color: #4CAF50; font-size: 1.3em;">€{amount:,.2f}</span></p>
                <p><b>Fällig am:</b> {due_date}</p>
            </div>
            <p>Bitte überweisen Sie den Betrag rechtzeitig.</p>
        """)

    @staticmethod
    def appointment_confirm(customer_name: str, date: str, time: str, apt_type: str) -> str:
        return EmailTemplates.wrap(f"""
            <h2 style="color: #D4AF37;">Terminbestätigung ✅</h2>
            <p>Sehr geehrte/r {customer_name},</p>
            <p>Ihr Termin wurde bestätigt:</p>
            <div style="background: #1a1a2e; padding: 20px; border-radius: 10px; margin: 15px 0; border-left: 4px solid #27ae60;">
                <p>📅 <b>Datum:</b> {date}</p>
                <p>🕐 <b>Uhrzeit:</b> {time}</p>
                <p>📋 <b>Typ:</b> {apt_type}</p>
            </div>
            <p>Wir freuen uns auf Ihren Besuch!</p>
        """)

    @staticmethod
    def payment_received(customer_name: str, amount: float, remaining: float) -> str:
        return EmailTemplates.wrap(f"""
            <h2 style="color: #27ae60;">Zahlung erhalten ✅</h2>
            <p>Sehr geehrte/r {customer_name},</p>
            <p>Wir bestätigen den Eingang Ihrer Zahlung:</p>
            <div style="background: #1a1a2e; padding: 20px; border-radius: 10px; margin: 15px 0;">
                <p>💰 <b>Eingegangen:</b> <span style="color: #4CAF50;">€{amount:,.2f}</span></p>
                <p>📊 <b>Restbetrag:</b> €{remaining:,.2f}</p>
            </div>
            <p>Vielen Dank!</p>
        """)
