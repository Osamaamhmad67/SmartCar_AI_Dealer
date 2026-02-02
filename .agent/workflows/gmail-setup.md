# إعداد Gmail App Password

## المشكلة
خطأ: `535, b'5.7.8 Username and Password not accepted'`

## الحل

### 1. تفعيل المصادقة الثنائية
- اذهب إلى: https://myaccount.google.com/security
- فعّل "2-Step Verification"

### 2. إنشاء كلمة مرور التطبيق
- اذهب إلى: https://myaccount.google.com/apppasswords
- اختر "Mail" و "Windows Computer"
- اضغط "Generate"
- ستحصل على كلمة مرور من 16 حرف

### 3. تحديث ملف .env
```env
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx
```

**ملاحظة:** استخدم App Password فقط، وليس كلمة مرور حسابك العادية.
