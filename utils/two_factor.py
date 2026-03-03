"""
utils/two_factor.py - Two-Factor Authentication (2FA)
SmartCar AI-Dealer
"""
import pyotp
import qrcode
import io
import base64
import sqlite3
from config import Config


class TwoFactorAuth:
    """TOTP-based two-factor authentication"""

    @staticmethod
    def generate_secret(user_id: int) -> str:
        """Generate and store a new TOTP secret for user"""
        secret = pyotp.random_base32()
        try:
            conn = sqlite3.connect(Config.DATABASE_PATH)
            conn.execute("UPDATE users SET totp_secret=? WHERE id=?", (secret, user_id))
            conn.commit()
            conn.close()
        except Exception:
            # Column might not exist, add it
            conn = sqlite3.connect(Config.DATABASE_PATH)
            try:
                conn.execute("ALTER TABLE users ADD COLUMN totp_secret TEXT")
            except Exception:
                pass
            try:
                conn.execute("ALTER TABLE users ADD COLUMN totp_enabled INTEGER DEFAULT 0")
            except Exception:
                pass
            conn.execute("UPDATE users SET totp_secret=? WHERE id=?", (secret, user_id))
            conn.commit()
            conn.close()
        return secret

    @staticmethod
    def get_qr_code(secret: str, username: str) -> bytes:
        """Generate QR code image for authenticator app"""
        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(name=username, issuer_name="SmartCar AI-Dealer")
        
        qr = qrcode.make(uri)
        buf = io.BytesIO()
        qr.save(buf, format='PNG')
        return buf.getvalue()

    @staticmethod
    def verify_code(secret: str, code: str) -> bool:
        """Verify a TOTP code"""
        totp = pyotp.TOTP(secret)
        return totp.verify(code)

    @staticmethod
    def enable_2fa(user_id: int):
        """Enable 2FA for a user"""
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.execute("UPDATE users SET totp_enabled=1 WHERE id=?", (user_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def disable_2fa(user_id: int):
        """Disable 2FA for a user"""
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.execute("UPDATE users SET totp_enabled=0, totp_secret=NULL WHERE id=?", (user_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def is_enabled(user_id: int) -> bool:
        """Check if 2FA is enabled"""
        try:
            conn = sqlite3.connect(Config.DATABASE_PATH)
            row = conn.execute("SELECT totp_enabled FROM users WHERE id=?", (user_id,)).fetchone()
            conn.close()
            return bool(row and row[0])
        except Exception:
            return False

    @staticmethod
    def get_secret(user_id: int) -> str:
        """Get stored TOTP secret"""
        try:
            conn = sqlite3.connect(Config.DATABASE_PATH)
            row = conn.execute("SELECT totp_secret FROM users WHERE id=?", (user_id,)).fetchone()
            conn.close()
            return row[0] if row else None
        except Exception:
            return None
