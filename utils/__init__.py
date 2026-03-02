"""
utils/__init__.py - Utilities package initialization (Lazy Loading)
تم تحسين الاستيرادات لتحميل المكونات عند الحاجة فقط
"""


def __getattr__(name):
    """Lazy import: يتم تحميل كل مكون فقط عند استدعائه"""
    _imports = {
        'ImageValidator': ('.validation', 'ImageValidator'),
        'validate_car_image': ('.validation', 'validate_car_image'),
        'PDFBaseGenerator': ('.pdf_generator', 'PDFGenerator'),
        'InvoiceGenerator': ('.invoice_generator', 'InvoiceGenerator'),
        'InstallmentInvoiceGenerator': ('.installment_invoice', 'InstallmentInvoiceGenerator'),
        'NotificationManager': ('.notifier', 'NotificationManager'),
        'CacheManager': ('.cache_manager', 'CacheManager'),
        'DocumentScanner': ('.ocr_scanner', 'DocumentScanner'),
        'PaymentProcessor': ('.payment_processor', 'PaymentProcessor'),
        'ImageCleanupManager': ('.cleanup', 'ImageCleanupManager'),
        'setup_logger': ('.logger', 'setup_logger'),
        'GeneralUtils': ('.general_utils', 'GeneralUtils'),
        'PricePredictor': ('.predictor', 'PricePredictor'),
    }

    if name in _imports:
        module_path, attr_name = _imports[name]
        import importlib
        module = importlib.import_module(module_path, __package__)
        return getattr(module, attr_name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    'ImageValidator',
    'validate_car_image',
    'PDFBaseGenerator',
    'InvoiceGenerator',
    'InstallmentInvoiceGenerator',
    'NotificationManager',
    'CacheManager',
    'DocumentScanner',
    'PaymentProcessor',
    'ImageCleanupManager',
    'setup_logger',
    'GeneralUtils',
    'PricePredictor'
]