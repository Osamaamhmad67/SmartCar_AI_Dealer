"""
🚗 صفحة مخزون السيارات - Car Inventory Page
SmartCar AI-Dealer
عرض وإدارة جميع السيارات المقيّمة مع فلاتر البحث وإدارة الحالة
"""

import streamlit as st
from db_manager import DatabaseManager
from utils.i18n import t
import os


def inventory_page():
    """صفحة إدارة مخزون السيارات"""
    db = DatabaseManager()
    user = st.session_state.get('user', {})
    is_admin = user.get('role') == 'admin'
    
    st.markdown(f"""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #D4AF37; margin: 0;">🚗 {t('inventory.title', 'Car Inventory')}</h1>
        <p style="color: #a0a0c0;">{t('inventory.subtitle', 'Browse and manage available vehicles')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # === Filters Section ===
    with st.expander(f"🔍 {t('inventory.filters', 'Filters')}", expanded=True):
        filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
        
        with filter_col1:
            brand_filter = st.text_input(
                t('inventory.brand_filter', 'Brand'),
                placeholder=t('inventory.all_brands', 'All brands...'),
                key="inv_brand"
            )
        
        with filter_col2:
            status_options = [
                t('inventory.all_status', 'All'),
                t('inventory.available', 'Available'),
                t('inventory.reserved', 'Reserved'),
                t('inventory.sold', 'Sold')
            ]
            status_filter = st.selectbox(
                t('inventory.status_filter', 'Status'),
                status_options,
                key="inv_status"
            )
        
        with filter_col3:
            price_min = st.number_input(
                t('inventory.price_min', 'Min Price (€)'),
                min_value=0, value=0, step=1000,
                key="inv_price_min"
            )
        
        with filter_col4:
            price_max = st.number_input(
                t('inventory.price_max', 'Max Price (€)'),
                min_value=0, value=500000, step=1000,
                key="inv_price_max"
            )
    
    # === Load Cars from Database ===
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT t.id, t.brand, t.model, t.manufacture_year, t.car_type,
                       t.estimated_price, t.condition, t.mileage,
                       t.image_path, t.created_at,
                       'available' as inventory_status,
                       u.full_name as owner_name
                FROM transactions t
                JOIN users u ON t.user_id = u.id
                WHERE t.estimated_price > 0
            """
            params = []
            
            if brand_filter:
                query += " AND LOWER(t.brand) LIKE LOWER(?)"
                params.append(f"%{brand_filter}%")
            
            if price_min > 0:
                query += " AND t.estimated_price >= ?"
                params.append(price_min)
            
            if price_max < 500000:
                query += " AND t.estimated_price <= ?"
                params.append(price_max)
            
            # Status filter
            status_map = {
                status_options[1]: 'available',
                status_options[2]: 'reserved',
                status_options[3]: 'sold'
            }
            if status_filter != status_options[0] and status_filter in status_map:
                pass  # inventory_status not yet in DB schema
            
            query += " ORDER BY t.created_at DESC"
            
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            cars = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # === Statistics Bar ===
        total = len(cars)
        available_count = sum(1 for c in cars if c.get('inventory_status') == 'available')
        reserved_count = sum(1 for c in cars if c.get('inventory_status') == 'reserved')
        sold_count = sum(1 for c in cars if c.get('inventory_status') == 'sold')
        
        stat1, stat2, stat3, stat4 = st.columns(4)
        stat1.metric(f"📊 {t('inventory.total', 'Total')}", total)
        stat2.metric(f"✅ {t('inventory.available', 'Available')}", available_count)
        stat3.metric(f"📌 {t('inventory.reserved', 'Reserved')}", reserved_count)
        stat4.metric(f"🏷️ {t('inventory.sold', 'Sold')}", sold_count)
        
        st.markdown("---")
        
        if not cars:
            st.info(f"🔍 {t('inventory.no_cars', 'No cars found matching your criteria')}")
            return
        
        # === Car Cards Grid ===
        cols_per_row = 3
        for i in range(0, len(cars), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                idx = i + j
                if idx >= len(cars):
                    break
                
                car = cars[idx]
                brand = car.get('brand', 'N/A')
                model = car.get('model', car.get('car_type', 'N/A'))
                year = car.get('manufacture_year', '')
                price = car.get('estimated_price', 0)
                mileage = car.get('mileage', 0)
                condition = car.get('condition', 'N/A')
                status = car.get('inventory_status', 'available')
                car_id = car.get('id')
                
                # Status colors
                status_colors = {
                    'available': ('#27ae60', '✅'),
                    'reserved': ('#f39c12', '📌'),
                    'sold': ('#e74c3c', '🏷️')
                }
                s_color, s_icon = status_colors.get(status, ('#27ae60', '✅'))
                
                # Status labels
                status_labels = {
                    'available': t('inventory.available', 'Available'),
                    'reserved': t('inventory.reserved', 'Reserved'),
                    'sold': t('inventory.sold', 'Sold')
                }
                s_label = status_labels.get(status, status)
                
                with col:
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                        border-radius: 15px;
                        padding: 20px;
                        margin-bottom: 15px;
                        border: 1px solid {s_color}33;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <h3 style="color: #D4AF37; margin: 0; font-size: 1.1em;">🏎️ {brand}</h3>
                            <span style="
                                background: {s_color}22;
                                color: {s_color};
                                padding: 3px 10px;
                                border-radius: 20px;
                                font-size: 0.8em;
                                border: 1px solid {s_color}55;
                            ">{s_icon} {s_label}</span>
                        </div>
                        <p style="color: white; font-size: 1em; margin: 5px 0;">{model} {year}</p>
                        <div style="color: #a0a0c0; font-size: 0.85em; margin: 10px 0;">
                            <span>🛣️ {mileage:,.0f} km</span> &nbsp;|&nbsp;
                            <span>⭐ {condition}/10</span>
                        </div>
                        <div style="
                            background: linear-gradient(90deg, #D4AF3722, transparent);
                            padding: 10px;
                            border-radius: 8px;
                            margin-top: 10px;
                        ">
                            <span style="color: #4CAF50; font-size: 1.4em; font-weight: bold;">€{price:,.0f}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Admin can change status
                    if is_admin:
                        new_status = st.selectbox(
                            t('inventory.change_status', 'Status'),
                            ['available', 'reserved', 'sold'],
                            index=['available', 'reserved', 'sold'].index(status) if status in ['available', 'reserved', 'sold'] else 0,
                            key=f"status_{car_id}",
                            label_visibility="collapsed"
                        )
                        if new_status != status:
                            try:
                                st.info(f"Status update: {new_status}")
                            except Exception as e:
                                st.error(f"❌ {e}")
    
    except Exception as e:
        st.error(f"❌ {t('messages.error', 'Error')}: {e}")
