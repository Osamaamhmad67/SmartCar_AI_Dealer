"""Reset password for specific user"""
from auth import AuthManager
from db_manager import DatabaseManager

def reset_password():
    auth = AuthManager()
    db = DatabaseManager()
    
    username = 'rajaa'
    new_password = 'Rajaa@#$1967'
    
    # Generate new hash
    new_hash = auth.hash_password(new_password)
    print(f"New hash generated for {username}")
    
    # Update in database
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET password_hash = ? WHERE username = ?', (new_hash, username))
        print(f"Updated {cursor.rowcount} row(s)")
    
    # Verify
    user = db.get_user_by_username(username)
    result = auth.check_password(new_password, user['password_hash'])
    print(f"Password verification: {result}")

if __name__ == '__main__':
    reset_password()
