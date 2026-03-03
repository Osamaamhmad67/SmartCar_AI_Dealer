"""
utils/backup_manager.py - Automated Backup System
SmartCar AI-Dealer
"""
import shutil, os, glob
from datetime import datetime
from config import Config


class BackupManager:
    """Automated database backup with scheduling"""

    BACKUP_DIR = os.path.join(os.path.dirname(Config.DATABASE_PATH), 'backups')

    @staticmethod
    def create_backup() -> str:
        os.makedirs(BackupManager.BACKUP_DIR, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(BackupManager.BACKUP_DIR, f'smartcar_backup_{timestamp}.db')
        shutil.copy2(Config.DATABASE_PATH, backup_path)
        return backup_path

    @staticmethod
    def list_backups() -> list:
        os.makedirs(BackupManager.BACKUP_DIR, exist_ok=True)
        backups = glob.glob(os.path.join(BackupManager.BACKUP_DIR, '*.db'))
        result = []
        for b in sorted(backups, reverse=True):
            size = os.path.getsize(b)
            name = os.path.basename(b)
            result.append({'path': b, 'name': name, 'size': size, 'size_mb': size / 1024 / 1024})
        return result

    @staticmethod
    def restore_backup(backup_path: str) -> bool:
        if not os.path.exists(backup_path):
            return False
        # Create safety backup first
        safety = BackupManager.create_backup()
        shutil.copy2(backup_path, Config.DATABASE_PATH)
        return True

    @staticmethod
    def delete_backup(backup_path: str):
        if os.path.exists(backup_path):
            os.remove(backup_path)

    @staticmethod
    def cleanup_old_backups(keep_count: int = 10):
        backups = BackupManager.list_backups()
        if len(backups) > keep_count:
            for old in backups[keep_count:]:
                BackupManager.delete_backup(old['path'])

    @staticmethod
    def get_db_size() -> float:
        return os.path.getsize(Config.DATABASE_PATH) / 1024 / 1024

    @staticmethod
    def render_backup_ui():
        import streamlit as st
        from utils.i18n import t
        
        st.markdown(f"### 🔄 {t('backup.title', 'Backup Manager')}")
        
        db_size = BackupManager.get_db_size()
        st.metric(f"💾 {t('backup.db_size', 'Database Size')}", f"{db_size:.2f} MB")
        
        b1, b2 = st.columns(2)
        with b1:
            if st.button(f"💾 {t('backup.create', 'Create Backup')}", type="primary", use_container_width=True):
                path = BackupManager.create_backup()
                BackupManager.cleanup_old_backups()
                st.success(f"✅ Backup created: {os.path.basename(path)}")
        with b2:
            if st.button(f"🗑️ {t('backup.cleanup', 'Cleanup Old')}", use_container_width=True):
                BackupManager.cleanup_old_backups(5)
                st.success("✅ Old backups cleaned")
        
        st.markdown("---")
        backups = BackupManager.list_backups()
        for bk in backups:
            st.markdown(f"""
            <div style="background: #16213e; padding: 8px 12px; border-radius: 8px; margin: 3px 0; border-left: 3px solid #27ae60;">
                <b style="color: white;">💾 {bk['name']}</b>
                <span style="color: #a0a0c0; float: right;">{bk['size_mb']:.2f} MB</span>
            </div>""", unsafe_allow_html=True)
        
        if not backups:
            st.info(t('backup.no_backups', 'No backups yet'))
