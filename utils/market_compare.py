"""
utils/market_compare.py - Market Price Comparison
SmartCar AI-Dealer - مقارنة أسعار السوق
"""
import sqlite3
from config import Config


class MarketComparator:
    """Compare car prices with internal market data"""

    @staticmethod
    def get_comparison(brand: str, model: str, year: int, mileage: float, estimated_price: float) -> dict:
        """Compare price against similar cars in our database"""
        try:
            conn = sqlite3.connect(Config.DATABASE_PATH)
            cursor = conn.cursor()
            
            # Find similar cars (same brand, ±2 years, ±30k km)
            cursor.execute("""
                SELECT estimated_price, mileage, manufacture_year
                FROM transactions
                WHERE LOWER(brand) = LOWER(?)
                AND ABS(manufacture_year - ?) <= 2
                AND ABS(mileage - ?) <= 30000
                AND estimated_price > 0
                AND id NOT IN (SELECT id FROM transactions WHERE estimated_price = ?)
            """, (brand, year, mileage, estimated_price))
            
            similar = cursor.fetchall()
            conn.close()
            
            if not similar:
                return {
                    'has_data': False,
                    'message': 'No similar vehicles in database for comparison'
                }
            
            prices = [r[0] for r in similar]
            avg_price = sum(prices) / len(prices)
            min_price = min(prices)
            max_price = max(prices)
            
            # Price position
            if estimated_price < avg_price * 0.9:
                position = 'below_market'
                position_label = '📉 Below Market'
                position_color = '#27ae60'
            elif estimated_price > avg_price * 1.1:
                position = 'above_market'
                position_label = '📈 Above Market'
                position_color = '#e74c3c'
            else:
                position = 'fair_price'
                position_label = '✅ Fair Price'
                position_color = '#3498db'
            
            diff_percent = ((estimated_price - avg_price) / avg_price) * 100
            
            return {
                'has_data': True,
                'similar_count': len(similar),
                'avg_price': avg_price,
                'min_price': min_price,
                'max_price': max_price,
                'position': position,
                'position_label': position_label,
                'position_color': position_color,
                'diff_percent': diff_percent,
                'estimated_price': estimated_price
            }
        except Exception as e:
            return {'has_data': False, 'message': str(e)}
