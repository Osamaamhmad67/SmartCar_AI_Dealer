"""
utils/api_server.py - REST API for SmartCar
SmartCar AI-Dealer
To run: python utils/api_server.py
"""
from flask import Flask, jsonify, request
import sqlite3
from config import Config

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/api/cars', methods=['GET'])
def get_cars():
    """Get available cars"""
    conn = get_db()
    brand = request.args.get('brand', '')
    limit = request.args.get('limit', 50, type=int)
    
    q = "SELECT id, brand, model, manufacture_year, estimated_price, mileage, fuel_type, color, transmission, horsepower FROM transactions WHERE estimated_price > 0"
    params = []
    if brand:
        q += " AND LOWER(brand) LIKE LOWER(?)"
        params.append(f"%{brand}%")
    q += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    
    rows = conn.execute(q, params).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    """Get single car details"""
    conn = get_db()
    row = conn.execute("SELECT * FROM transactions WHERE id=?", (car_id,)).fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    return jsonify({'error': 'Not found'}), 404


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    conn = get_db()
    total_cars = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    avg_price = conn.execute("SELECT AVG(estimated_price) FROM transactions WHERE estimated_price > 0").fetchone()[0] or 0
    conn.close()
    return jsonify({'total_cars': total_cars, 'total_users': total_users, 'avg_price': round(avg_price, 2)})


@app.route('/api/brands', methods=['GET'])
def get_brands():
    """Get brand statistics"""
    conn = get_db()
    rows = conn.execute("SELECT brand, COUNT(*) as count FROM transactions GROUP BY brand ORDER BY count DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


if __name__ == '__main__':
    app.run(port=5000, debug=True)
