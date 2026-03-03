"""
utils/car_pipeline.py - Car Status Pipeline
SmartCar AI-Dealer - مراحل حالة السيارة
"""
import sqlite3
from datetime import datetime
from config import Config


class CarPipeline:
    """Track car through stages: received → inspected → priced → listed → sold"""

    STAGES = ['received', 'inspected', 'priced', 'listed', 'sold']
    STAGE_INFO = {
        'received': {'icon': '📥', 'color': '#3498db', 'label': 'Empfangen'},
        'inspected': {'icon': '🔍', 'color': '#f39c12', 'label': 'Geprüft'},
        'priced': {'icon': '💰', 'color': '#9b59b6', 'label': 'Bewertet'},
        'listed': {'icon': '📋', 'color': '#1abc9c', 'label': 'Gelistet'},
        'sold': {'icon': '✅', 'color': '#27ae60', 'label': 'Verkauft'},
    }

    @staticmethod
    def _ensure_table():
        conn = sqlite3.connect(Config.DB_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS car_pipeline (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id INTEGER NOT NULL,
                stage TEXT DEFAULT 'received',
                updated_by INTEGER,
                notes TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (transaction_id) REFERENCES transactions(id)
            )
        """)
        conn.commit(); conn.close()

    @staticmethod
    def set_stage(transaction_id: int, stage: str, user_id: int = None, notes: str = None):
        CarPipeline._ensure_table()
        conn = sqlite3.connect(Config.DB_PATH)
        conn.execute("INSERT INTO car_pipeline (transaction_id, stage, updated_by, notes) VALUES (?,?,?,?)",
                     (transaction_id, stage, user_id, notes))
        conn.commit(); conn.close()

    @staticmethod
    def get_current_stage(transaction_id: int) -> str:
        CarPipeline._ensure_table()
        conn = sqlite3.connect(Config.DB_PATH)
        row = conn.execute("SELECT stage FROM car_pipeline WHERE transaction_id=? ORDER BY updated_at DESC LIMIT 1",
                          (transaction_id,)).fetchone()
        conn.close()
        return row[0] if row else 'received'

    @staticmethod
    def get_history(transaction_id: int) -> list:
        CarPipeline._ensure_table()
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM car_pipeline WHERE transaction_id=? ORDER BY updated_at ASC",
                           (transaction_id,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def render_pipeline_html(current_stage: str) -> str:
        stages_html = ""
        reached = True
        for stage in CarPipeline.STAGES:
            info = CarPipeline.STAGE_INFO[stage]
            if stage == current_stage:
                bg = info['color']
                reached = False
            elif reached:
                bg = info['color']
            else:
                bg = '#333'
            
            stages_html += f"""
            <div style="text-align:center; flex:1;">
                <div style="background:{bg}; width:40px; height:40px; border-radius:50%; 
                            display:inline-flex; align-items:center; justify-content:center; font-size:1.2em;">
                    {info['icon']}
                </div>
                <div style="color:{'white' if bg != '#333' else '#666'}; font-size:0.75em; margin-top:4px;">
                    {info['label']}
                </div>
            </div>
            """
        
        return f'<div style="display:flex; justify-content:space-between; padding:15px; background:#16213e; border-radius:10px;">{stages_html}</div>'
