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
        conn = sqlite3.connect(Config.DATABASE_PATH)
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
        conn = sqlite3.connect(Config.DATABASE_PATH)
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

    @staticmethod
    def get_monthly_profit_chart_data() -> list:
        """Monthly revenue vs cost vs profit for Plotly charts"""
        conn = sqlite3.connect(Config.DATABASE_PATH)
        c = conn.cursor()
        c.execute("""
            SELECT strftime('%Y-%m', created_at) as month,
                   COUNT(*) as sales_count,
                   COALESCE(SUM(estimated_price), 0) as revenue,
                   COALESCE(SUM(estimated_price * COALESCE(profit_margin, 0) / 100), 0) as profit,
                   COALESCE(SUM(estimated_price - estimated_price * COALESCE(profit_margin, 0) / 100), 0) as cost
            FROM transactions WHERE estimated_price > 0
            GROUP BY month ORDER BY month ASC
        """)
        rows = c.fetchall()
        conn.close()
        return [{'month': r[0], 'sales_count': r[1], 'revenue': r[2], 'profit': r[3], 'cost': r[4]} for r in rows]

    @staticmethod
    def get_brand_profit_ranking() -> list:
        """Profit per brand sorted by total profit"""
        conn = sqlite3.connect(Config.DATABASE_PATH)
        c = conn.cursor()
        c.execute("""
            SELECT brand,
                   COUNT(*) as cnt,
                   COALESCE(SUM(estimated_price), 0) as revenue,
                   COALESCE(AVG(COALESCE(profit_margin, 0)), 0) as avg_margin,
                   COALESCE(SUM(estimated_price * COALESCE(profit_margin, 0) / 100), 0) as profit
            FROM transactions WHERE estimated_price > 0 AND brand IS NOT NULL AND brand != ''
            GROUP BY brand ORDER BY profit DESC LIMIT 15
        """)
        rows = c.fetchall()
        conn.close()
        return [{'brand': r[0], 'count': r[1], 'revenue': r[2], 'avg_margin': r[3], 'profit': r[4]} for r in rows]

    @staticmethod
    def get_top_profitable_cars(limit: int = 10) -> list:
        """Top N highest-profit individual sales"""
        conn = sqlite3.connect(Config.DATABASE_PATH)
        c = conn.cursor()
        c.execute("""
            SELECT id, brand, model, manufacture_year, estimated_price,
                   COALESCE(profit_margin, 0) as margin,
                   COALESCE(estimated_price * profit_margin / 100, 0) as profit,
                   created_at
            FROM transactions WHERE estimated_price > 0 AND profit_margin > 0
            ORDER BY profit DESC LIMIT ?
        """, (limit,))
        rows = c.fetchall()
        conn.close()
        return [{'id': r[0], 'brand': r[1], 'model': r[2], 'year': r[3], 
                 'price': r[4], 'margin': r[5], 'profit': r[6], 'date': r[7]} for r in rows]

    @staticmethod
    def get_profit_summary() -> dict:
        """Summary cards data: total profit, avg margin, best month, best brand"""
        conn = sqlite3.connect(Config.DATABASE_PATH)
        c = conn.cursor()
        
        # Overall
        c.execute("""
            SELECT COALESCE(SUM(estimated_price * COALESCE(profit_margin, 0) / 100), 0),
                   COALESCE(AVG(COALESCE(profit_margin, 0)), 0),
                   COALESCE(SUM(estimated_price), 0),
                   COUNT(*)
            FROM transactions WHERE estimated_price > 0
        """)
        row = c.fetchone()
        total_profit = row[0]
        avg_margin = row[1]
        total_revenue = row[2]
        total_count = row[3]
        
        # Best month
        c.execute("""
            SELECT strftime('%Y-%m', created_at) as month,
                   COALESCE(SUM(estimated_price * COALESCE(profit_margin, 0) / 100), 0) as profit
            FROM transactions WHERE estimated_price > 0
            GROUP BY month ORDER BY profit DESC LIMIT 1
        """)
        best_month_row = c.fetchone()
        best_month = best_month_row[0] if best_month_row else '-'
        best_month_profit = best_month_row[1] if best_month_row else 0
        
        # Best brand
        c.execute("""
            SELECT brand,
                   COALESCE(SUM(estimated_price * COALESCE(profit_margin, 0) / 100), 0) as profit
            FROM transactions WHERE estimated_price > 0 AND brand IS NOT NULL AND brand != ''
            GROUP BY brand ORDER BY profit DESC LIMIT 1
        """)
        best_brand_row = c.fetchone()
        best_brand = best_brand_row[0] if best_brand_row else '-'
        best_brand_profit = best_brand_row[1] if best_brand_row else 0
        
        conn.close()
        return {
            'total_profit': total_profit,
            'avg_margin': avg_margin,
            'total_revenue': total_revenue,
            'total_count': total_count,
            'best_month': best_month,
            'best_month_profit': best_month_profit,
            'best_brand': best_brand,
            'best_brand_profit': best_brand_profit
        }
