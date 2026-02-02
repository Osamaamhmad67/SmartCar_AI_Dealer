
import sqlite3
from pathlib import Path
import sys

# Ensure we can find config
sys.path.append(str(Path(__file__).parent.parent))
from config import Config

def migrate_database():
    print(f"Checking database at: {Config.DATABASE_PATH}")
    
    if not Config.DATABASE_PATH.exists():
        print("Database file found.")
        return

    conn = sqlite3.connect(str(Config.DATABASE_PATH))
    cursor = conn.cursor()
    
    try:
        # Check existing columns in employees
        cursor.execute("PRAGMA table_info(employees)")
        existing_columns = [row[1] for row in cursor.fetchall()]
        print(f"Current columns in 'employees': {existing_columns}")
        
        # Columns to add
        new_columns = {
            'last_name': 'TEXT',
            'phone': 'TEXT',
            'email': 'TEXT',
            'address': 'TEXT',
            'annual_leave': 'INTEGER DEFAULT 30',
            'sick_leave': 'INTEGER DEFAULT 0',
            'unpaid_leave': 'INTEGER DEFAULT 0',
            'notes': 'TEXT'
        }
        
        for col_name, col_type in new_columns.items():
            if col_name not in existing_columns:
                print(f"Adding '{col_name}' column to employees...")
                cursor.execute(f"ALTER TABLE employees ADD COLUMN {col_name} {col_type}")
            else:
                print(f"'{col_name}' column already exists.")

        # Create activity_logs table
        print("Checking 'activity_logs' table...")
        cursor.execute('''CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action_type TEXT NOT NULL,
            details TEXT,
            ip_address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )''')
        print("'activity_logs' table verified/created.")
            
        conn.commit()
        print("Migration completed successfully.")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
