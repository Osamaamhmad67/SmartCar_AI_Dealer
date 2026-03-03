"""
utils/datev_export.py - DATEV CSV Export
SmartCar AI-Dealer - German accounting standard export
"""
import csv, io, sqlite3
from datetime import datetime
from config import Config


class DATEVExporter:
    """Export transactions in DATEV-compatible CSV format"""

    @staticmethod
    def export_transactions(start_date=None, end_date=None) -> str:
        """Generate DATEV CSV content for transactions"""
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        
        query = """
            SELECT t.id, t.brand, t.model, t.estimated_price, t.created_at,
                   t.fuel_type, t.mileage, t.manufacture_year,
                   u.full_name, u.email
            FROM transactions t
            JOIN users u ON t.user_id = u.id
            WHERE 1=1
        """
        params = []
        if start_date:
            query += " AND t.created_at >= ?"; params.append(start_date)
        if end_date:
            query += " AND t.created_at <= ?"; params.append(end_date)
        query += " ORDER BY t.created_at DESC"
        
        rows = conn.execute(query, params).fetchall()
        conn.close()

        output = io.StringIO()
        writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_ALL)
        
        # DATEV header
        writer.writerow([
            'Umsatz (ohne Soll/Haben-Kz)', 'Soll/Haben-Kennzeichen',
            'WKZ Umsatz', 'Kurs', 'Basis-Umsatz', 'WKZ Basis-Umsatz',
            'Konto', 'Gegenkonto (ohne BU-Schlüssel)', 'BU-Schlüssel',
            'Belegdatum', 'Belegfeld 1', 'Belegfeld 2',
            'Skonto', 'Buchungstext'
        ])
        
        for row in rows:
            price = row['estimated_price'] or 0
            date_str = row['created_at'][:10].replace('-', '') if row['created_at'] else ''
            # DATEV format: DDMM
            if len(date_str) == 8:
                datev_date = date_str[6:8] + date_str[4:6]
            else:
                datev_date = ''
            
            writer.writerow([
                f"{price:.2f}".replace('.', ','),  # German decimal
                'S',  # Soll (debit)
                'EUR', '', '', '',
                '8400',  # Revenue account
                '10000',  # Customer account
                '',
                datev_date,
                f"RE-{row['id']}",  # Invoice reference
                f"{row['brand']} {row['model']}",
                '', 
                f"Fahrzeugbewertung {row['brand']} {row['model']} - {row['full_name']}"
            ])
        
        return output.getvalue()

    @staticmethod
    def export_invoices(start_date=None, end_date=None) -> str:
        """Export invoices in DATEV format"""
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        
        query = """
            SELECT i.id, i.amount_due, i.due_date, i.status, i.installment_number,
                   c.id as contract_id, c.total_amount
            FROM invoices i
            JOIN contracts c ON i.contract_id = c.id
            WHERE 1=1
        """
        params = []
        if start_date:
            query += " AND i.due_date >= ?"; params.append(start_date)
        if end_date:
            query += " AND i.due_date <= ?"; params.append(end_date)
        query += " ORDER BY i.due_date DESC"
        
        try:
            rows = conn.execute(query, params).fetchall()
        except Exception:
            rows = []
        conn.close()

        output = io.StringIO()
        writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_ALL)
        
        writer.writerow([
            'Umsatz', 'Soll/Haben', 'WKZ', 'Konto', 'Gegenkonto',
            'Belegdatum', 'Belegfeld 1', 'Status', 'Buchungstext'
        ])
        
        for row in rows:
            amount = row['amount_due'] or 0
            date_str = (row['due_date'] or '')[:10].replace('-', '')
            datev_date = date_str[6:8] + date_str[4:6] if len(date_str) == 8 else ''
            
            writer.writerow([
                f"{amount:.2f}".replace('.', ','),
                'S', 'EUR', '1400', '8400',
                datev_date,
                f"INV-{row['contract_id']}-{row['installment_number']}",
                row['status'],
                f"Rate {row['installment_number']} Vertrag #{row['contract_id']}"
            ])
        
        return output.getvalue()
