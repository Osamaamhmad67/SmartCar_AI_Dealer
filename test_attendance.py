"""اختبار نظام الحضور والانصراف"""
from db_manager import DatabaseManager
from datetime import datetime

db = DatabaseManager()

# جلب أول موظف نشط
employees = db.get_all_employees()
active_employees = [e for e in employees if e.get('is_active')]

if not active_employees:
    print("❌ لا يوجد موظفين نشطين للاختبار")
    exit()

emp = active_employees[0]
print(f"📋 اختبار مع الموظف: {emp['first_name']} {emp.get('last_name', '')} (ID: {emp['id']})")
print(f"   الراتب الشهري: €{emp.get('monthly_salary', 0)}")
print("-" * 50)

# 1. تسجيل حضور
print("\n1️⃣ تسجيل الحضور...")
result = db.record_check_in(emp['id'])
if result['success']:
    print(f"   ✅ تم تسجيل الحضور في {result['time']}")
else:
    print(f"   ⚠️ {result['message']}")

# 2. عرض حالة اليوم
print("\n2️⃣ حالة اليوم...")
today_record = db.get_attendance_today(emp['id'])
if today_record:
    print(f"   📅 التاريخ: {today_record['date']}")
    print(f"   🕒 الحضور: {today_record['check_in']}")
    print(f"   🕕 الانصراف: {today_record['check_out'] or 'لم يسجل'}")
    print(f"   ⏱️ الساعات: {today_record['net_worked_hours']}")
    print(f"   📊 الحالة: {today_record['status']}")
else:
    print("   ❌ لا يوجد سجل اليوم")

# 3. تسجيل انصراف (اختياري - يمكن تعليقه)
# input("\nاضغط Enter لتسجيل الانصراف...")
# print("\n3️⃣ تسجيل الانصراف...")
# result = db.record_check_out(emp['id'])
# if result['success']:
#     print(f"   ✅ تم تسجيل الانصراف")
#     print(f"   ⏱️ ساعات العمل: {result['net_worked_hours']:.2f}")
#     adj = result.get('adjustment', {})
#     if adj.get('type') == 'overtime':
#         print(f"   💰 عمل إضافي: +{adj['hours']:.1f}h (+€{adj['amount']:.2f})")
#     elif adj.get('type') == 'deduction':
#         print(f"   ⚠️ خصم: -{adj['hours']:.1f}h (-€{adj['amount']:.2f})")
# else:
#     print(f"   ❌ {result['message']}")

print("\n" + "=" * 50)
print("✅ اختبار نظام الحضور اكتمل!")
