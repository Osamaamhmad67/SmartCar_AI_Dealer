"""
utils/pdf_report.py - Professional PDF Report Generator
SmartCar AI-Dealer
"""
import io
from datetime import datetime


class PDFReportGenerator:
    """Generate professional PDF reports with charts data"""

    @staticmethod
    def generate_summary_report() -> bytes:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib.colors import HexColor
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from utils.report_generator import ReportGenerator
        
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=1.5*cm, bottomMargin=1.5*cm)
        styles = getSampleStyleSheet()
        
        gold = HexColor('#D4AF37')
        dark = HexColor('#1a1a2e')
        
        title_style = ParagraphStyle('Title', parent=styles['Title'], textColor=dark, fontSize=20)
        heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], textColor=gold, fontSize=14)
        
        elements = []
        
        # Title
        elements.append(Paragraph("🏎️ SmartCar AI-Dealer", title_style))
        elements.append(Paragraph(f"Monthly Report - {datetime.now().strftime('%B %Y')}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Get data
        data = ReportGenerator.get_monthly_summary()
        
        # Summary table
        elements.append(Paragraph("📊 Overview", heading_style))
        elements.append(Spacer(1, 10))
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Evaluations', str(data['total_transactions'])],
            ['Total Revenue', f"€{data['total_revenue']:,.2f}"],
            ['Average Price', f"€{data['avg_price']:,.2f}"],
            ['Highest Price', f"€{data['max_price']:,.2f}"],
            ['New Customers', str(data['new_users'])],
            ['Transaction Growth', f"{data['trans_growth']:+.1f}%"],
            ['Revenue Growth', f"{data['revenue_growth']:+.1f}%"],
        ]
        
        table = Table(summary_data, colWidths=[8*cm, 8*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), dark),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f8f8'), HexColor('#ffffff')]),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        # Top brands
        if data['top_brands']:
            elements.append(Paragraph("🏆 Top Brands", heading_style))
            elements.append(Spacer(1, 10))
            brand_data = [['Brand', 'Count']] + [[b[0], str(b[1])] for b in data['top_brands']]
            brand_table = Table(brand_data, colWidths=[10*cm, 6*cm])
            brand_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), gold),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
            ]))
            elements.append(brand_table)
        
        elements.append(Spacer(1, 30))
        elements.append(Paragraph(f"Generated: {datetime.now().strftime('%d.%m.%Y %H:%M')}", styles['Normal']))
        
        doc.build(elements)
        return buf.getvalue()
