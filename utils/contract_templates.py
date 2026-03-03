"""
utils/contract_templates.py - Contract Template System
SmartCar AI-Dealer - قوالب العقود المتعددة
"""


class ContractTemplates:
    """Pre-defined contract templates"""

    TEMPLATES = {
        'purchase': {
            'name': 'Kaufvertrag',
            'name_ar': 'عقد بيع',
            'icon': '🛒',
            'fields': ['buyer', 'seller', 'vehicle', 'price', 'payment_method', 'delivery_date'],
            'clauses': [
                'Der Verkäufer verkauft das o.g. Fahrzeug an den Käufer.',
                'Der Kaufpreis ist bei Übergabe des Fahrzeugs fällig.',
                'Das Fahrzeug wird in dem Zustand verkauft, in dem es sich bei Übergabe befindet.',
                'Der Verkäufer versichert, dass das Fahrzeug frei von Rechten Dritter ist.',
                'Die Übergabe des Fahrzeugs erfolgt am vereinbarten Liefertermin.',
            ]
        },
        'lease': {
            'name': 'Mietvertrag',
            'name_ar': 'عقد إيجار',
            'icon': '📋',
            'fields': ['tenant', 'landlord', 'vehicle', 'monthly_rent', 'duration', 'start_date'],
            'clauses': [
                'Der Vermieter überlässt dem Mieter das o.g. Fahrzeug zur Nutzung.',
                'Die Miete ist monatlich im Voraus zu entrichten.',
                'Der Mieter verpflichtet sich, das Fahrzeug pfleglich zu behandeln.',
                'Reparaturen aufgrund normaler Abnutzung trägt der Vermieter.',
                'Bei Vertragsende ist das Fahrzeug in ordnungsgemäßem Zustand zurückzugeben.',
            ]
        },
        'installment': {
            'name': 'Ratenkaufvertrag',
            'name_ar': 'عقد تقسيط',
            'icon': '💰',
            'fields': ['buyer', 'seller', 'vehicle', 'total_price', 'down_payment', 'monthly_rate', 'num_installments'],
            'clauses': [
                'Der Kaufpreis wird in Raten gemäß dem vereinbarten Zahlungsplan beglichen.',
                'Die Anzahlung ist bei Vertragsabschluss fällig.',
                'Bei Zahlungsverzug von mehr als 30 Tagen kann der Verkäufer vom Vertrag zurücktreten.',
                'Das Eigentum geht erst nach vollständiger Bezahlung auf den Käufer über.',
                'Vorzeitige Tilgung ist jederzeit möglich.',
            ]
        },
        'warranty': {
            'name': 'Garantievertrag',
            'name_ar': 'عقد ضمان',
            'icon': '🛡️',
            'fields': ['vehicle', 'warranty_period', 'coverage', 'max_amount'],
            'clauses': [
                'Der Garantiegeber übernimmt die Reparaturkosten für die versicherten Komponenten.',
                'Die Garantie gilt für den o.g. Zeitraum ab Kaufdatum.',
                'Verschleißteile sind von der Garantie ausgenommen.',
                'Ein Selbstbehalt von €150 je Schadensfall ist vom Käufer zu tragen.',
                'Die Garantie erlischt bei unsachgemäßer Behandlung des Fahrzeugs.',
            ]
        }
    }

    @staticmethod
    def get_template(template_type: str) -> dict:
        return ContractTemplates.TEMPLATES.get(template_type, {})

    @staticmethod
    def get_all_types() -> list:
        return [(k, v['icon'], v['name'], v['name_ar']) for k, v in ContractTemplates.TEMPLATES.items()]

    @staticmethod
    def render_clauses(template_type: str) -> str:
        template = ContractTemplates.TEMPLATES.get(template_type, {})
        clauses = template.get('clauses', [])
        return '\n'.join([f"§{i+1} {c}" for i, c in enumerate(clauses)])
