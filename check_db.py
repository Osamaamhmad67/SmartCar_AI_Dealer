"""سكربت للتحقق من جداول قاعدة البيانات"""
import sqlite3

conn = sqlite3.connect('smartcar_dealer.db')
cursor = conn.cursor()

# عرض جميع الجداول
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("📋 الجداول الموجودة:")
for t in tables:
    print(f"  - {t[0]}")

# التحقق من جدول الحضور
try:
    count = cursor.execute("SELECT COUNT(*) FROM attendance_logs").fetchone()[0]
    print(f"\n✅ جدول attendance_logs موجود - عدد السجلات: {count}")
except:
    print("\n❌ جدول attendance_logs غير موجود")

# التحقق من جدول تعديلات الرواتب
try:
    count = cursor.execute("SELECT COUNT(*) FROM salary_adjustments").fetchone()[0]
    print(f"✅ جدول salary_adjustments موجود - عدد السجلات: {count}")
except:
    print("❌ جدول salary_adjustments غير موجود")

conn.close()
