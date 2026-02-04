"""
مولد رموز QR للموظفين
QR Code Generator for Employee Attendance System
"""

import io
from typing import Optional, Tuple

# نحتاج مكتبة qrcode - إذا غير موجودة سنستخدم بديل نصي
try:
    import qrcode
    from qrcode.image.pure import PymagingImage
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False


def generate_qr_code(data: str, size: int = 200) -> Optional[bytes]:
    """
    توليد صورة QR Code من النص
    
    Args:
        data: النص المراد تحويله لـ QR
        size: حجم الصورة بالبكسل
    
    Returns:
        bytes: محتوى الصورة كـ PNG، أو None إذا فشل
    """
    if not QR_AVAILABLE:
        return None
    
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # تحويل لـ bytes
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return buffer.getvalue()
    except Exception as e:
        print(f"Error generating QR: {e}")
        return None


def generate_employee_qr_card(
    employee_name: str,
    employee_id: int,
    qr_token: str,
    company_name: str = "SmartCar AI Dealer"
) -> Optional[bytes]:
    """
    توليد بطاقة QR للموظف مع اسمه ورقمه
    
    Args:
        employee_name: اسم الموظف
        employee_id: رقم الموظف
        qr_token: رمز QR الفريد
        company_name: اسم الشركة
    
    Returns:
        bytes: صورة البطاقة
    """
    if not QR_AVAILABLE:
        return None
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # إنشاء QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=8,
            border=2,
        )
        qr.add_data(qr_token)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # إنشاء البطاقة
        card_width = 400
        card_height = 500
        card = Image.new('RGB', (card_width, card_height), 'white')
        draw = ImageDraw.Draw(card)
        
        # رسم الإطار
        draw.rectangle([5, 5, card_width-5, card_height-5], outline='#D4AF37', width=3)
        
        # اسم الشركة
        draw.text((card_width//2, 30), company_name, fill='#1a1a2e', anchor='mm')
        
        # خط فاصل
        draw.line([(20, 60), (card_width-20, 60)], fill='#D4AF37', width=2)
        
        # لصق QR في المنتصف
        qr_size = 250
        qr_img = qr_img.resize((qr_size, qr_size))
        qr_x = (card_width - qr_size) // 2
        card.paste(qr_img, (qr_x, 80))
        
        # اسم الموظف
        draw.text((card_width//2, 360), employee_name, fill='#1a1a2e', anchor='mm')
        
        # رقم الموظف
        draw.text((card_width//2, 400), f"ID: {employee_id}", fill='#666666', anchor='mm')
        
        # الرمز
        draw.text((card_width//2, 440), f"Token: {qr_token}", fill='#888888', anchor='mm')
        
        # تحويل لـ bytes
        buffer = io.BytesIO()
        card.save(buffer, format='PNG')
        buffer.seek(0)
        
        return buffer.getvalue()
        
    except Exception as e:
        print(f"Error generating QR card: {e}")
        return generate_qr_code(qr_token)


def decode_qr_from_image(image_bytes: bytes) -> Optional[str]:
    """
    قراءة رمز QR من صورة
    
    Args:
        image_bytes: محتوى الصورة
    
    Returns:
        str: النص المُستخرج من QR، أو None
    """
    try:
        from PIL import Image
        from pyzbar import pyzbar
        
        image = Image.open(io.BytesIO(image_bytes))
        decoded = pyzbar.decode(image)
        
        if decoded:
            return decoded[0].data.decode('utf-8')
        return None
        
    except ImportError:
        print("pyzbar not installed - QR decoding not available")
        return None
    except Exception as e:
        print(f"Error decoding QR: {e}")
        return None


def create_simple_qr_text(token: str) -> str:
    """
    إنشاء تمثيل نصي بسيط لـ QR (للعرض في الطرفية)
    """
    return f"""
╔══════════════════════════════╗
║        ATTENDANCE QR         ║
╠══════════════════════════════╣
║                              ║
║     Token: {token[:8]}...     ║
║                              ║
║   Scan with SmartCar App     ║
║                              ║
╚══════════════════════════════╝
"""
