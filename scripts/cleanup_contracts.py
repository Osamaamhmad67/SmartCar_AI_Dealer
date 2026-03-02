"""
سكربت تنظيف قاعدة البيانات - حذف العقود غير المكتملة
قم بتشغيله من مجلد المشروع: python cleanup_contracts.py
"""

from db_manager import DatabaseManager

def cleanup_incomplete_contracts():
    db = DatabaseManager()
    
    # 1. إنشاء نسخة احتياطية
    print("=" * 50)
    print("📦 Creating backup...")
    backup_path = db.backup_database()
    print(f"✅ Backup created: {backup_path}")
    print("=" * 50)
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        # 2. عرض الإحصائيات الحالية
        print("\n📊 CURRENT DATABASE STATISTICS:")
        print("-" * 40)
        
        cursor.execute('SELECT COUNT(*), status FROM contracts GROUP BY status')
        contracts_stats = cursor.fetchall()
        print("Contracts by Status:")
        for row in contracts_stats:
            print(f"   {row[1]}: {row[0]}")
        
        cursor.execute('SELECT COUNT(*) FROM transactions')
        tx_count = cursor.fetchone()[0]
        print(f"\nTotal Transactions: {tx_count}")
        
        # 3. تحديد ما سيتم حذفه
        cursor.execute("""
            SELECT id FROM contracts 
            WHERE status NOT IN ('completed', 'paid') OR status IS NULL
        """)
        to_delete = [row[0] for row in cursor.fetchall()]
        print(f"\n⚠️ Contracts to DELETE: {len(to_delete)}")
        
        if len(to_delete) == 0:
            print("✅ No incomplete contracts to delete!")
            return
        
        # 4. تأكيد الحذف
        confirm = input("\n🔴 Are you sure you want to delete these contracts? (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ Operation cancelled.")
            return
        
        # 5. حذف العقود غير المكتملة فقط
        print("\n🗑️ Deleting incomplete contracts...")
        
        cursor.execute("""
            DELETE FROM contracts 
            WHERE status NOT IN ('completed', 'paid') OR status IS NULL
        """)
        deleted_contracts = cursor.rowcount
        
        conn.commit()
        
        # 6. عرض النتائج
        print("\n" + "=" * 50)
        print("✅ CLEANUP COMPLETED!")
        print("=" * 50)
        print(f"   Deleted Contracts: {deleted_contracts}")
        
        # 7. عرض الإحصائيات الجديدة
        print("\n📊 NEW DATABASE STATISTICS:")
        print("-" * 40)
        cursor.execute('SELECT COUNT(*) FROM contracts')
        print(f"   Remaining Contracts: {cursor.fetchone()[0]}")
        cursor.execute('SELECT COUNT(*) FROM transactions')
        print(f"   Remaining Transactions: {cursor.fetchone()[0]}")
        
        print(f"\n💾 Backup available at: {backup_path}")

if __name__ == "__main__":
    cleanup_incomplete_contracts()
