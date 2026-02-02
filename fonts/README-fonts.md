# 🔤 الخطوط العربية لـ SmartCar AI-Dealer

## الخطوط المطلوبة

لتفعيل دعم اللغة العربية بشكل كامل في الفواتير، تحتاج إلى تحميل الخطوط التالية:

### 1. خط Cairo

- **Cairo-Regular.ttf** - الخط الأساسي
- **Cairo-Bold.ttf** - الخط الغامق للعناوين

## طريقة التحميل

### من Google Fonts (مستحسن)

1. اذهب إلى [Google Fonts - Cairo](https://fonts.google.com/specimen/Cairo)
2. اضغط على "Download family"
3. فك الضغط عن الملف
4. انسخ الملفات التالية إلى هذا المجلد:
   - `Cairo-Regular.ttf`
   - `Cairo-Bold.ttf`

### باستخدام سطر الأوامر (Linux/Mac)

```bash
# تحميل مباشر
curl -L "https://github.com/ArtifexSoftware/mupdf-fonts/raw/main/fonts/noto/NotoNaskhArabic-Regular.ttf" -o Cairo-Regular.ttf
curl -L "https://github.com/ArtifexSoftware/mupdf-fonts/raw/main/fonts/noto/NotoNaskhArabic-Bold.ttf" -o Cairo-Bold.ttf
```

### باستخدام PowerShell (Windows)

```powershell
# تحميل الخطوط
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ArtifexSoftware/mupdf-fonts/main/fonts/noto/NotoNaskhArabic-Regular.ttf" -OutFile "Cairo-Regular.ttf"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ArtifexSoftware/mupdf-fonts/main/fonts/noto/NotoNaskhArabic-Bold.ttf" -OutFile "Cairo-Bold.ttf"
```

## التحقق من التثبيت

بعد تحميل الخطوط، تأكد من وجودها:

```bash
ls -la fonts/
# يجب أن ترى:
# Cairo-Regular.ttf
# Cairo-Bold.ttf
```

## خطوط بديلة

إذا لم تستطع تحميل خط Cairo، يمكنك استخدام:

- **Amiri** - خط عربي كلاسيكي
- **Noto Naskh Arabic** - خط Google
- **Scheherazade** - خط SIL

## ملاحظات

- تأكد من أن الملفات بصيغة `.ttf`
- إذا كان الخط بصيغة أخرى (`.otf`)، حوّله إلى TTF
- الخطوط ضرورية لإنشاء فواتير PDF باللغة العربية
