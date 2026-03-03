"""
utils/car_card_export.py - Export Car Card as Image
SmartCar AI-Dealer
"""
import io, base64


class CarCardExporter:
    """Generate shareable car card images"""

    @staticmethod
    def generate_card_html(car: dict) -> str:
        """Generate HTML for a car card"""
        price = car.get('estimated_price', 0)
        return f"""
        <div style="width:400px; background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 20px; 
                    padding: 25px; font-family: Arial; color: white; border: 2px solid #D4AF3766;">
            <div style="text-align: center; border-bottom: 1px solid #D4AF3733; padding-bottom: 15px;">
                <div style="font-size: 12px; color: #D4AF37;">🏎️ SmartCar AI-Dealer</div>
                <h2 style="margin: 5px 0; color: #D4AF37;">{car.get('brand', '')} {car.get('model', '')}</h2>
                <div style="font-size: 2em; color: #4CAF50; font-weight: bold;">€{price:,.0f}</div>
            </div>
            <table style="width: 100%; margin-top: 15px; font-size: 13px;">
                <tr><td style="color:#a0a0c0; padding:4px;">📅 Year</td><td style="text-align:right;">{car.get('manufacture_year','')}</td></tr>
                <tr><td style="color:#a0a0c0; padding:4px;">🛣️ Mileage</td><td style="text-align:right;">{car.get('mileage',0):,.0f} km</td></tr>
                <tr><td style="color:#a0a0c0; padding:4px;">⛽ Fuel</td><td style="text-align:right;">{car.get('fuel_type','')}</td></tr>
                <tr><td style="color:#a0a0c0; padding:4px;">⚙️ Transmission</td><td style="text-align:right;">{car.get('transmission','')}</td></tr>
                <tr><td style="color:#a0a0c0; padding:4px;">🐎 HP</td><td style="text-align:right;">{car.get('horsepower','')}</td></tr>
                <tr><td style="color:#a0a0c0; padding:4px;">🎨 Color</td><td style="text-align:right;">{car.get('color','')}</td></tr>
                <tr><td style="color:#a0a0c0; padding:4px;">📋 Condition</td><td style="text-align:right;">{car.get('condition','')}</td></tr>
            </table>
            <div style="text-align: center; margin-top: 15px; color: #a0a0c0; font-size: 10px;">
                SmartCar AI-Dealer | www.smartcar-dealer.de
            </div>
        </div>
        """

    @staticmethod
    def get_card_download(car: dict) -> str:
        """Return HTML card as downloadable content"""
        html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{margin:0;display:flex;justify-content:center;align-items:center;min-height:100vh;background:#0a0a14;}}</style></head><body>
        {CarCardExporter.generate_card_html(car)}
        </body></html>"""
        return html
