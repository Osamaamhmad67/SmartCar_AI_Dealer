"""
utils/cleanup.py - إدارة تنظيف البيانات المهملة
SmartCar AI-Dealer
تحسين الأداء وضمان تكامل التقارير مع واجهة المشرف
"""
import os
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Set

from config import Config
from db_manager import DatabaseManager

class ImageCleanupManager:
    """مدير تنظيف الصور غير المستخدمة لضمان كفاءة التخزين"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.logger = Config.logger
        self.images_dir = Config.UPLOADS_DIR
        # التأكد من وجود المجلد لتجنب أخطاء المسح
        self.images_dir.mkdir(parents=True, exist_ok=True)
    
    def cleanup_orphaned_images(self, retention_hours: int = 24) -> Dict[str, any]:
        """
        حذف الصور التي لا ترتبط بأي معاملة والتي مر عليها وقت محدد.
        تم تحسينها لتعيد بيانات واضحة لواجهة المشرف (Admin Dashboard).
        """
        report = {
            'scanned_files': 0,
            'deleted_files': 0,
            'freed_space_mb': 0.0,
            'errors': [],
            'start_time': datetime.now().isoformat()
        }
        
        try:
            # 1. جمع كل أسماء الملفات المستخدمة فعلياً في قاعدة البيانات
            used_images: Set[str] = set()
            
            with self.db.get_connection() as conn:
                # تفعيل Row factory للوصول للبيانات بأسماء الأعمدة
                conn.row_factory = None # نستخدم الافتراضي هنا للسرعة
                cursor = conn.cursor()
                
                # جلب الصور من العمود الرئيسي والتحليل
                cursor.execute("SELECT image_path, condition_analysis FROM transactions")
                rows = cursor.fetchall()
                
                for row in rows:
                    img_p, analysis = row
                    # إضافة الصورة الرئيسية
                    if img_p:
                        used_images.add(Path(img_p).name)
                    
                    # استخراج الصور المخفية داخل JSON التحليل (AI Analysis)
                    if analysis:
                        try:
                            # التحقق إذا كان نصاً أو قاموساً
                            data = json.loads(analysis) if isinstance(analysis, str) else analysis
                            self._extract_image_filenames(data, used_images)
                        except:
                            pass
            
            # 2. تحديد وقت القطع (Cutoff Time)
            cutoff_time = time.time() - (retention_hours * 3600)
            
            # 3. مسح المجلد وحذف الملفات غير المستخدمة والقديمة
            if not self.images_dir.exists():
                return report

            # نستخدم rglob للبحث في المجلدات الفرعية أيضاً إن وجدت
            for file_path in self.images_dir.rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']:
                    report['scanned_files'] += 1
                    
                    filename = file_path.name
                    mtime = file_path.stat().st_mtime
                    
                    # الشرط: ليست مستخدمة في DB وتجاوزت مدة الاحتفاظ
                    if filename not in used_images and mtime < cutoff_time:
                        file_size = file_path.stat().st_size
                        try:
                            file_path.unlink()
                            report['deleted_files'] += 1
                            report['freed_space_mb'] += (file_size / (1024 * 1024))
                        except Exception as e:
                            report['errors'].append(f"Error deleting {filename}: {str(e)}")

            if self.logger and report['deleted_files'] > 0:
                self.logger.info(f"Cleanup finished: Deleted {report['deleted_files']} files.")

        except Exception as e:
            error_msg = f"Fatal error in cleanup: {str(e)}"
            report['errors'].append(error_msg)
            if self.logger:
                self.logger.error(error_msg)
                
        # تقريب المساحة المحررة لرقمين عشريين
        report['freed_space_mb'] = round(report['freed_space_mb'], 2)
        return report

    def _extract_image_filenames(self, data: any, names_set: Set[str]):
        """دالة مساعدة لاستخراج أسماء الملفات من أي هيكل بيانات (JSON/List/Dict)"""
        if isinstance(data, dict):
            for key, value in data.items():
                # نبحث عن المفاتيح التي قد تحتوي على مسارات صور
                if any(x in key.lower() for x in ['path', 'image', 'img', 'url']):
                    if isinstance(value, str) and any(value.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                        names_set.add(Path(value).name)
                self._extract_image_filenames(value, names_set)
        elif isinstance(data, list):
            for item in data:
                self._extract_image_filenames(item, names_set)