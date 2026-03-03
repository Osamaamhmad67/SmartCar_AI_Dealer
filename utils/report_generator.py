"""
utils/report_generator.py - Auto Monthly PDF Reports
SmartCar AI-Dealer
"""
import sqlite3, json
from datetime import datetime, timedelta
from config import Config


class ReportGenerator:
    """Generate monthly sales and performance reports"""

    @staticmethod
    def get_monthly_summary(year=None, month=None) -> dict:
        """Get monthly business summary data"""
        if not year:
            now = datetime.now()
            year, month = now.year, now.month

        conn = sqlite3.connect(Config.DB_PATH)
        c = conn.cursor()

        # Transactions this month
        c.execute("""
            SELECT COUNT(*), COALESCE(SUM(estimated_price), 0), 
                   COALESCE(AVG(estimated_price), 0), COALESCE(MAX(estimated_price), 0)
            FROM transactions 
            WHERE strftime('%Y', created_at) = ? AND strftime('%m', created_at) = ?
        """, (str(year), f"{month:02d}"))
        row = c.fetchone()
        
        # Top brands this month
        c.execute("""
            SELECT brand, COUNT(*) as cnt FROM transactions
            WHERE strftime('%Y', created_at) = ? AND strftime('%m', created_at) = ?
            GROUP BY brand ORDER BY cnt DESC LIMIT 5
        """, (str(year), f"{month:02d}"))
        top_brands = c.fetchall()

        # New users this month
        c.execute("""
            SELECT COUNT(*) FROM users
            WHERE strftime('%Y', created_at) = ? AND strftime('%m', created_at) = ?
        """, (str(year), f"{month:02d}"))
        new_users = c.fetchone()[0]

        # Previous month comparison
        if month == 1:
            prev_year, prev_month = year - 1, 12
        else:
            prev_year, prev_month = year, month - 1

        c.execute("""
            SELECT COUNT(*), COALESCE(SUM(estimated_price), 0)
            FROM transactions 
            WHERE strftime('%Y', created_at) = ? AND strftime('%m', created_at) = ?
        """, (str(prev_year), f"{prev_month:02d}"))
        prev = c.fetchone()
        
        conn.close()

        return {
            'year': year, 'month': month,
            'total_transactions': row[0],
            'total_revenue': row[1],
            'avg_price': row[2],
            'max_price': row[3],
            'top_brands': top_brands,
            'new_users': new_users,
            'prev_transactions': prev[0],
            'prev_revenue': prev[1],
            'trans_growth': ((row[0] - prev[0]) / max(prev[0], 1)) * 100,
            'revenue_growth': ((row[1] - prev[1]) / max(prev[1], 1)) * 100
        }

    @staticmethod
    def format_report_text(data: dict) -> str:
        """Format report as readable text"""
        months_de = ['', 'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',
                     'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
        month_name = months_de[data['month']]
        
        brands_text = '\n'.join([f"  • {b[0]}: {b[1]} Fahrzeuge" for b in data['top_brands']]) if data['top_brands'] else '  Keine Daten'
        
        trans_arrow = '📈' if data['trans_growth'] >= 0 else '📉'
        rev_arrow = '📈' if data['revenue_growth'] >= 0 else '📉'
        
        return f"""
═══════════════════════════════════════
   🏎️ SmartCar AI-Dealer
   Monatsbericht {month_name} {data['year']}
═══════════════════════════════════════

📊 ÜBERSICHT
  • Bewertungen: {data['total_transactions']} {trans_arrow} ({data['trans_growth']:+.1f}%)
  • Gesamtumsatz: €{data['total_revenue']:,.2f} {rev_arrow} ({data['revenue_growth']:+.1f}%)
  • Durchschnittspreis: €{data['avg_price']:,.2f}
  • Höchster Preis: €{data['max_price']:,.2f}

🏆 TOP MARKEN
{brands_text}

👥 NEUE KUNDEN: {data['new_users']}

═══════════════════════════════════════
   Erstellt am: {datetime.now().strftime('%d.%m.%Y %H:%M')}
═══════════════════════════════════════
"""
