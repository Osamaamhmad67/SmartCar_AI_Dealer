"""
pages_app/showcase_page.py - Public Showcase
SmartCar AI-Dealer - عرض السيارات المتاحة للعملاء
"""
import streamlit as st
from db_manager import DatabaseManager
from utils.i18n import t


def showcase_page():
    """صفحة عرض السيارات المتاحة للعملاء"""
    db = DatabaseManager()
    
    st.markdown(f"""
    <div style="text-align: center; padding: 30px 0;">
        <h1 style="color: #D4AF37; margin: 0;">🏎️ {t('showcase.title', 'Available Cars')}</h1>
        <p style="color: #a0a0c0; font-size: 1.1em;">{t('showcase.subtitle', 'Browse our premium vehicle collection')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filters
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        brand_f = st.text_input(f"🔍 {t('showcase.search', 'Search brand')}", key="sc_brand")
    with fc2:
        sort_opt = st.selectbox(f"📊 {t('showcase.sort', 'Sort by')}", 
            [t('showcase.newest', 'Newest'), t('showcase.price_low', 'Price: Low'), t('showcase.price_high', 'Price: High')],
            key="sc_sort")
    with fc3:
        max_price = st.slider(f"💰 {t('showcase.max_price', 'Max Price')}", 0, 200000, 200000, 5000, key="sc_maxp")
    
    st.markdown("---")
    
    try:
        with db.get_connection() as conn:
            query = """
                SELECT t.brand, t.model, t.manufacture_year, t.estimated_price,
                       t.mileage, t.fuel_type, t.condition, t.color,
                       t.transmission, t.horsepower, t.engine_cc,
                       COALESCE(t.inventory_status, 'available') as status,
                       t.created_at
                FROM transactions t
                WHERE COALESCE(t.inventory_status, 'available') = 'available'
                AND t.estimated_price > 0
            """
            params = []
            
            if brand_f:
                query += " AND LOWER(t.brand) LIKE LOWER(?)"; params.append(f"%{brand_f}%")
            if max_price < 200000:
                query += " AND t.estimated_price <= ?"; params.append(max_price)
            
            # Sort
            if sort_opt == t('showcase.price_low', 'Price: Low'):
                query += " ORDER BY t.estimated_price ASC"
            elif sort_opt == t('showcase.price_high', 'Price: High'):
                query += " ORDER BY t.estimated_price DESC"
            else:
                query += " ORDER BY t.created_at DESC"
            
            cursor = conn.cursor()
            cursor.execute(query, params)
            cols = [d[0] for d in cursor.description]
            cars = [dict(zip(cols, r)) for r in cursor.fetchall()]
        
        st.caption(f"🚗 {len(cars)} {t('showcase.found', 'vehicles found')}")
        
        # Car cards - 3 per row
        for i in range(0, len(cars), 3):
            row_cols = st.columns(3)
            for j, col in enumerate(row_cols):
                if i + j >= len(cars): break
                car = cars[i + j]
                with col:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1a1a2e, #16213e);
                                border-radius: 15px; padding: 20px; margin-bottom: 15px;
                                border: 1px solid #D4AF3733;
                                box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
                        <h3 style="color: #D4AF37; margin: 0 0 5px 0;">🏎️ {car.get('brand', '')}</h3>
                        <p style="color: white; font-size: 1.1em; margin: 0;">{car.get('model', '')} {car.get('manufacture_year', '')}</p>
                        <div style="color: #a0a0c0; font-size: 0.85em; margin: 10px 0; line-height: 1.8;">
                            🛣️ {car.get('mileage', 0):,.0f} km &nbsp;|&nbsp;
                            ⛽ {car.get('fuel_type', '-')} &nbsp;|&nbsp;
                            ⚙️ {car.get('transmission', '-')}<br>
                            🐎 {car.get('horsepower', '-')} PS &nbsp;|&nbsp;
                            🏭 {car.get('engine_cc', '-')} cc &nbsp;|&nbsp;
                            🎨 {car.get('color', '-')}
                        </div>
                        <div style="background: linear-gradient(90deg, #D4AF3722, transparent);
                                    padding: 12px; border-radius: 8px; margin-top: 10px;">
                            <span style="color: #4CAF50; font-size: 1.5em; font-weight: bold;">€{car.get('estimated_price', 0):,.0f}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        if not cars:
            st.info(f"🔍 {t('showcase.no_cars', 'No cars match your criteria')}")
    
    except Exception as e:
        st.error(f"❌ {e}")
