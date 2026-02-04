"""سكربت لإنشاء جداول الحضور والرواتب"""
import sqlite3

conn = sqlite3.connect('smartcar_dealer.db')
cursor = conn.cursor()

# إنشاء جدول سجل الحضور
cursor.execute('''CREATE TABLE IF NOT EXISTS attendance_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    date DATE NOT NULL,
    check_in DATETIME,
    check_out DATETIME,
    net_worked_hours REAL DEFAULT 0,
    break_deducted INTEGER DEFAULT 0,
    status TEXT DEFAULT 'incomplete',
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
)''')

# إنشاء جدول تعديلات الراتب
cursor.execute('''CREATE TABLE IF NOT EXISTS salary_adjustments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    date DATE NOT NULL,
    adjustment_type TEXT NOT NULL,
    hours REAL DEFAULT 0,
    amount REAL DEFAULT 0,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
)''')

# إضافة عمود QR للموظفين إذا لم يكن موجوداً
try:
    cursor.execute("ALTER TABLE employees ADD COLUMN qr_token TEXT")
    print("✅ تم إضافة عمود qr_token لجدول employees")
except:
    print("ℹ️ عمود qr_token موجود مسبقاً")

conn.commit()
conn.close()

print("✅ تم إنشاء جدول attendance_logs")
print("✅ تم إنشاء جدول salary_adjustments")
print("\n🎉 اكتملت عملية إنشاء الجداول!")
