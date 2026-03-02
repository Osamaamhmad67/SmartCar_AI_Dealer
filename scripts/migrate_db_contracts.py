"""
migrate_db.py - سكربت ترحيل قاعدة البيانات
يقوم بإنشاء الجداول الجديدة (contracts, invoices) دون حذف البيانات الموجودة
"""

import sqlite3
from config import Config

def migrate():
    db_path = str(Config.DATABASE_PATH)
    print(f"Migrating database: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. إنشاء جدول العقود إذا لم يكن موجوداً
    print("Creating contracts table if not exists...")
    cursor.execute('''CREATE TABLE IF NOT EXISTS contracts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        transaction_id INTEGER,
        total_price REAL NOT NULL,
        down_payment REAL DEFAULT 0,
        remaining_amount REAL NOT NULL,
        installment_count INTEGER NOT NULL,
        monthly_installment REAL NOT NULL,
        interest_rate REAL DEFAULT 0,
        late_fee_type TEXT DEFAULT 'fixed',
        late_fee_amount REAL DEFAULT 50,
        grace_period_days INTEGER DEFAULT 3,
        payment_due_day INTEGER DEFAULT 1,
        status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        closed_at TIMESTAMP,
        vehicle_vin TEXT,
        vehicle_type TEXT,
        vehicle_model TEXT,
        vehicle_plate TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (transaction_id) REFERENCES transactions(id)
    )''')
    
    # 2. إنشاء جدول الفواتير إذا لم يكن موجوداً
    print("Creating invoices table if not exists...")
    cursor.execute('''CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_number TEXT UNIQUE NOT NULL,
        contract_id INTEGER NOT NULL,
        installment_number INTEGER NOT NULL,
        amount_due REAL NOT NULL,
        amount_paid REAL DEFAULT 0,
        late_fee REAL DEFAULT 0,
        due_date DATE NOT NULL,
        payment_date DATE,
        status TEXT DEFAULT 'pending',
        qr_hash TEXT,
        previous_qr_hash TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (contract_id) REFERENCES contracts(id)
    )''')
    
    conn.commit()
    conn.close()
    
    print("✅ Migration complete! Tables created successfully.")
    print("You can now restart the application.")

if __name__ == "__main__":
    migrate()
