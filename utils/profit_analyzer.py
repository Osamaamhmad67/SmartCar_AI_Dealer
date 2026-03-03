"""
utils/profit_analyzer.py - Profit Analysis
SmartCar AI-Dealer - تحليل الأرباح
"""
import sqlite3
from config import Config


class ProfitAnalyzer:
    """Analyze profit margins per car and overall"""

    @staticmethod
    def get_car_profit(transaction_id: int) -> dict:
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM transactions WHERE id=?", (transaction_id,)).fetchone()
        conn.close()
        if not row: return {'has_data': False}
        
        price = row['estimated_price'] or 0
        margin_pct = row['profit_margin'] or 0
        profit = price * (margin_pct / 100) if margin_pct else 0
        
        return {
            'has_data': True,
            'estimated_price': price,
            'profit_margin_pct': margin_pct,
            'profit_amount': profit,
            'cost': price - profit
        }

    @staticmethod
    def get_total_profit_report() -> dict:
        conn = sqlite3.connect(Config.DB_PATH)
        c = conn.cursor()
        
        c.execute("""
            SELECT COUNT(*) as total,
                   COALESCE(SUM(estimated_price), 0) as revenue,
                   COALESCE(AVG(profit_margin), 0) as avg_margin,
                   COALESCE(SUM(estimated_price * profit_margin / 100), 0) as total_profit
            FROM transactions WHERE estimated_price > 0
        """)
        overall = c.fetchone()
        
        c.execute("""
            SELECT brand, COUNT(*) as cnt,
                   SUM(estimated_price) as revenue,
                   AVG(profit_margin) as avg_margin,
                   SUM(estimated_price * COALESCE(profit_margin,0) / 100) as profit
            FROM transactions WHERE estimated_price > 0
            GROUP BY brand ORDER BY profit DESC LIMIT 10
        """)
        by_brand = c.fetchall()
        
        c.execute("""
            SELECT strftime('%Y-%m', created_at) as month,
                   SUM(estimated_price) as revenue,
                   SUM(estimated_price * COALESCE(profit_margin,0) / 100) as profit
            FROM transactions WHERE estimated_price > 0
            GROUP BY month ORDER BY month DESC LIMIT 12
        """)
        by_month = c.fetchall()
        
        conn.close()
        return {
            'total_cars': overall[0],
            'total_revenue': overall[1],
            'avg_margin': overall[2],
            'total_profit': overall[3],
            'by_brand': [{'brand': r[0], 'count': r[1], 'revenue': r[2], 'avg_margin': r[3], 'profit': r[4]} for r in by_brand],
            'by_month': [{'month': r[0], 'revenue': r[1], 'profit': r[2]} for r in by_month]
        }
