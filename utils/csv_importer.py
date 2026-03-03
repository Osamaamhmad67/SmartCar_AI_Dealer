"""
utils/csv_importer.py - CSV Import for Car Data
SmartCar AI-Dealer
"""
import csv, io, sqlite3
from datetime import datetime
from config import Config


class CSVImporter:
    """Import car data from CSV files"""

    EXPECTED_COLUMNS = ['brand', 'model', 'manufacture_year', 'mileage', 'estimated_price',
                        'fuel_type', 'condition', 'color', 'transmission', 'horsepower', 'engine_cc']

    @staticmethod
    def parse_csv(file_content: bytes) -> dict:
        """Parse CSV and return preview + validation"""
        try:
            text = file_content.decode('utf-8-sig')
        except:
            text = file_content.decode('latin-1')
        
        reader = csv.DictReader(io.StringIO(text), delimiter=';')
        rows = list(reader)
        
        if not rows:
            return {'success': False, 'error': 'Empty CSV file', 'rows': []}
        
        columns = list(rows[0].keys())
        
        return {
            'success': True,
            'columns': columns,
            'row_count': len(rows),
            'rows': rows,
            'preview': rows[:5]
        }

    @staticmethod
    def import_to_db(rows: list, user_id: int) -> dict:
        """Import parsed rows into transactions table"""
        conn = sqlite3.connect(Config.DATABASE_PATH)
        imported = 0
        errors = []
        
        for i, row in enumerate(rows):
            try:
                conn.execute("""
                    INSERT INTO transactions (user_id, brand, model, manufacture_year, mileage, 
                        estimated_price, fuel_type, condition, color, transmission, horsepower, 
                        engine_cc, car_type, inventory_status, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'available', ?)
                """, (
                    user_id,
                    row.get('brand', ''), row.get('model', ''),
                    int(row.get('manufacture_year', 0) or 0),
                    float(row.get('mileage', 0) or 0),
                    float(row.get('estimated_price', 0) or 0),
                    row.get('fuel_type', ''), row.get('condition', ''),
                    row.get('color', ''), row.get('transmission', ''),
                    row.get('horsepower', ''), row.get('engine_cc', ''),
                    row.get('car_type', row.get('model', '')),
                    datetime.now().isoformat()
                ))
                imported += 1
            except Exception as e:
                errors.append(f"Row {i+1}: {e}")
        
        conn.commit(); conn.close()
        return {'imported': imported, 'errors': errors, 'total': len(rows)}
