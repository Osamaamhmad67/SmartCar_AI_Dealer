from db_manager import DatabaseManager

db = DatabaseManager()

print("=== EMPLOYEES (جدول الموظفين) ===")
emps = db.get_all_employees()
for e in emps:
    print(f"ID:{e['id']} | job_title:{e.get('job_title')} | Name:{e.get('first_name')} {e.get('last_name')} | Email:{e.get('email')}")

admin_titles = ['Admin', 'Administrator', 'مدير النظام', 'Systemadministrator', 'آدمن', 'مدير']

print("\n=== ADMINS (الآدمنز - job_title in admin_titles) ===")
admins = [e for e in emps if e.get('job_title') in admin_titles]
for e in admins:
    print(f"ID:{e['id']} | Name:{e.get('first_name')} {e.get('last_name')}")
print(f"المجموع: {len(admins)} آدمن")

print("\n=== REGULAR EMPLOYEES (الموظفين العاديين) ===")
admin_emails = ['maria@web.com', 'adam@smartcar.com']  # من جدول users
regular_emps = [e for e in emps 
                if e.get('email') not in admin_emails 
                and e.get('job_title') not in admin_titles]
for e in regular_emps:
    print(f"ID:{e['id']} | Name:{e.get('first_name')} {e.get('last_name')}")
print(f"المجموع: {len(regular_emps)} موظف عادي")
