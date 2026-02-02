
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
        # Check existing columns
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"Current columns in 'users': {columns}")
        
        # Add failed_attempts if missing
        if 'failed_attempts' not in columns:
            print("Adding 'failed_attempts' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN failed_attempts INTEGER DEFAULT 0")
        else:
            print("'failed_attempts' column already exists.")
            
        # Add locked_until if missing
        if 'locked_until' not in columns:
            print("Adding 'locked_until' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN locked_until TIMESTAMP")
        else:
            print("'locked_until' column already exists.")
            
        conn.commit()
        print("Migration completed successfully.")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
