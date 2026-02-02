# 1. استخدام نسخة مستقرة وخفيفة من بايثون 3.11
FROM python:3.11-slim

# 2. ضبط متغيرات البيئة لضمان استقرار بايثون داخل الحاوية
# منع إنشاء ملفات .pyc وتسريع ظهور السجلات (Logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. تحديد مجلد العمل الأساسي
WORKDIR /app

# 4. تثبيت مكتبات النظام الضرورية (للتعامل مع الصور والخطوط والمعالجة)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    libgl1-mesa-glx \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# 5. نسخ ملف المكتبات أولاً لاستغلال خاصية الـ Caching في Docker
COPY requirements.txt .

# 6. تثبيت مكتبات بايثون المطلوبة
RUN pip install --no-cache-dir -r requirements.txt

# 7. نسخ كافة ملفات المشروع إلى داخل الحاوية
COPY . .

# 8. إنشاء المجلدات الحيوية لضمان عدم فشل النظام عند التشغيل لأول مرة
RUN mkdir -p uploads invoices logs .cache data backups fonts

# 9. فتح المنفذ الافتراضي لتطبيق Streamlit
EXPOSE 8501

# 10. فحص حالة الحاوية لضمان عمل التطبيق باستمرار
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 11. الأمر النهائي لتشغيل التطبيق فور تشغيل الحاوية
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]