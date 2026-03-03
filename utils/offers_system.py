"""
utils/offers_system.py - Special Offers & Discount Codes
SmartCar AI-Dealer - نظام العروض والخصومات
"""
import sqlite3, string, random
from datetime import datetime
from config import Config


class OffersSystem:
    """Manage special offers and discount codes"""

    @staticmethod
    def _ensure_table():
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS offers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                description TEXT,
                discount_type TEXT DEFAULT 'percentage',
                discount_value REAL NOT NULL,
                max_uses INTEGER DEFAULT 1,
                current_uses INTEGER DEFAULT 0,
                valid_from TEXT,
                valid_until TEXT,
                active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit(); conn.close()

    @staticmethod
    def generate_code(length=8) -> str:
        chars = string.ascii_uppercase + string.digits
        return 'SC-' + ''.join(random.choices(chars, k=length))

    @staticmethod
    def create_offer(description: str, discount_type: str, discount_value: float,
                     max_uses: int = 1, valid_until: str = None, code: str = None) -> str:
        OffersSystem._ensure_table()
        if not code:
            code = OffersSystem.generate_code()
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.execute("""
            INSERT INTO offers (code, description, discount_type, discount_value, max_uses, valid_until)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (code, description, discount_type, discount_value, max_uses, valid_until))
        conn.commit(); conn.close()
        return code

    @staticmethod
    def validate_code(code: str) -> dict:
        OffersSystem._ensure_table()
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        offer = conn.execute("SELECT * FROM offers WHERE code=? AND active=1", (code,)).fetchone()
        conn.close()
        
        if not offer:
            return {'valid': False, 'error': 'Invalid code'}
        if offer['current_uses'] >= offer['max_uses']:
            return {'valid': False, 'error': 'Code expired (max uses reached)'}
        if offer['valid_until'] and offer['valid_until'] < datetime.now().isoformat():
            return {'valid': False, 'error': 'Code expired'}
        
        return {
            'valid': True,
            'discount_type': offer['discount_type'],
            'discount_value': offer['discount_value'],
            'description': offer['description']
        }

    @staticmethod
    def apply_discount(code: str, original_price: float) -> dict:
        result = OffersSystem.validate_code(code)
        if not result['valid']:
            return result
        
        if result['discount_type'] == 'percentage':
            discount = original_price * (result['discount_value'] / 100)
        else:
            discount = result['discount_value']
        
        final_price = max(0, original_price - discount)
        
        # Increment usage
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.execute("UPDATE offers SET current_uses = current_uses + 1 WHERE code=?", (code,))
        conn.commit(); conn.close()
        
        return {
            'valid': True,
            'original_price': original_price,
            'discount': discount,
            'final_price': final_price,
            'description': result['description']
        }

    @staticmethod
    def get_all_offers() -> list:
        OffersSystem._ensure_table()
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM offers ORDER BY created_at DESC").fetchall()
        conn.close()
        return [dict(r) for r in rows]
