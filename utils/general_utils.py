"""
utils/general_utils.py - الأدوات المساعدة العامة
تنسيق العملات، الألوان، والتعامل مع النصوص
"""

class GeneralUtils:
    """كلاس يحتوي على وظائف مساعدة لتنسيق واجهة المستخدم"""

    @staticmethod
    def format_currency(amount, lang='Deutsch'):
        """تنسيق المبلغ المالي بناءً على اللغة"""
        try:
            val = float(amount)
            if lang == "عربي":
                return f"{val:,.2f} يورو"
            return f"{val:,.2f} €"
        except:
            return f"{amount} €"

    @staticmethod
    def get_status_color(status):
        """إرجاع رمز اللون بناءً على حالة التحقق"""
        colors = {
            'verified': '#2ecc71',    # أخضر
            'pending': '#f1c40f',     # أصفر
            'failed': '#e74c3c',      # أحمر
            'manual_review': '#3498db' # أزرق
        }
        return colors.get(status, '#7f8c8d')