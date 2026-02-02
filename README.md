# 🚗 SmartCar AI-Dealer: Advanced Dealership Management System

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-v1.30-red.svg)
![Groq AI](https://img.shields.io/badge/AI-Groq%20Llama%203.2-orange.svg)

**SmartCar AI-Dealer** هو نظام متكامل لإدارة معارض السيارات، يعتمد على الذكاء الاصطناعي (Groq Vision) لتقديم تقييمات دقيقة وفورية للسيارات بناءً على الصور، مع نظام مالي شامل لإدارة الرواتب، الضرائب، والجرد السنوي.

---

## ✨ المميزات الرئيسية (Core Features)

* **🤖 AI Car Appraisal:** تحليل صور السيارات واستخراج الماركة، الموديل، الحالة التقنية، وتقدير الأضرار آلياً.
* **⚖️ Weighted Pricing Engine:** خوارزمية تسعير مرجحة (60% للحالة، 25% للممشى، 15% للعمر) لضمان دقة مالية متناهية.
* **📑 Professional Invoicing:** توليد فواتير PDF احترافية تدعم ضريبة القيمة المضافة (VAT) والهوية البصرية للشركة.
* **🔍 Document OCR:** مسح هويات العملاء ورخص القيادة واستخراج البيانات منها آلياً.
* **💰 Financial Dashboard:** لوحة تحكم إدارية للجرد السنوي تشمل الأرباح، الديون، ورواتب الموظفين (Urlaubsgeld/Feiertagsgeld).
* **🔐 Enterprise Security:** نظام مصادقة قوي باستخدام تشفير `bcrypt` مع إدارة كاملة للأدوار (Admin/User).
* **🐳 Docker Ready:** دعم كامل لبيئات التطوير والإنتاج عبر Docker و Docker Compose.

---

## 🛠️ التقنيات المستخدمة (Tech Stack)

* **Frontend:** Streamlit (واجهة تفاعلية سريعة).
* **Backend:** Python 3.11.
* **AI Engine:** Groq Cloud API (Llama 3.2 Vision).
* **Database:** SQLite (مع دعم نمط WAL للسرعة).
* **PDF Core:** FPDF2.
* **DevOps:** Docker, Docker Compose.

---

## 🚀 تعليمات التثبيت (Installation)

### 1. المتطلبات الأساسية
تأكد من تثبيت Python 3.11 أو Docker على جهازك.

### 2. إعداد البيئة
```bash
# استنساخ المستودع
git clone [https://github.com/yourusername/smartcar-ai-dealer.git](https://github.com/yourusername/smartcar-ai-dealer.git)
cd smartcar-ai-dealer

# إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # في ويندوز: venv\Scripts\activate

# تثبيت المكتبات
pip install -r requirements.txt