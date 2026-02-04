"""فحص قواعد البيانات الموجودة"""
import sqlite3

databases = ['smartcar.db', 'smartcar_dealer.db', 'data/smartcar.db']

for db_name in databases:
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        print(f"\n📁 {db_name}:")
        if tables:
            for t in tables:
                print(f"   - {t[0]}")
        else:
            print("   (فارغ)")
        conn.close()
    except Exception as e:
        print(f"\n❌ {db_name}: {e}")
