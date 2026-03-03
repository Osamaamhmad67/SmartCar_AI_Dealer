"""
pages_app/appointments_page.py - Appointment Booking System
SmartCar AI-Dealer - نظام حجز المواعيد
"""
import streamlit as st
import sqlite3
from datetime import datetime, timedelta
from db_manager import DatabaseManager
from utils.i18n import t
from config import Config


def _ensure_table():
    """Create appointments table if not exists"""
    conn = sqlite3.connect(Config.DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            customer_name TEXT,
            phone TEXT,
            appointment_type TEXT NOT NULL,
            preferred_date TEXT NOT NULL,
            preferred_time TEXT NOT NULL,
            car_brand TEXT,
            car_model TEXT,
            notes TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()


def appointments_page():
    """صفحة حجز المواعيد"""
    _ensure_table()
    db = DatabaseManager()
    user = st.session_state.get('user', {})
    is_admin = user.get('role') == 'admin'
    
    st.markdown(f"""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #D4AF37;">🗓️ {t('appointments.title', 'Appointments')}</h1>
        <p style="color: #a0a0c0;">{t('appointments.subtitle', 'Book a test drive or inspection')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if is_admin:
        _admin_view()
    else:
        _customer_view(user)


def _customer_view(user):
    """Customer booking form"""
    st.subheader(f"📝 {t('appointments.book_new', 'Book New Appointment')}")
    
    with st.form("appointment_form"):
        col1, col2 = st.columns(2)
        with col1:
            apt_type = st.selectbox(
                t('appointments.type', 'Type'),
                [t('appointments.test_drive', 'Test Drive'), 
                 t('appointments.inspection', 'Inspection'),
                 t('appointments.consultation', 'Consultation')],
                key="apt_type"
            )
            preferred_date = st.date_input(
                t('appointments.date', 'Date'),
                min_value=datetime.now().date() + timedelta(days=1),
                key="apt_date"
            )
        with col2:
            preferred_time = st.selectbox(
                t('appointments.time', 'Time'),
                ['09:00', '10:00', '11:00', '12:00', '14:00', '15:00', '16:00', '17:00'],
                key="apt_time"
            )
            car_brand = st.text_input(t('appointments.car', 'Car (optional)'), key="apt_car")
        
        notes = st.text_area(t('appointments.notes', 'Notes'), key="apt_notes", max_chars=500)
        
        if st.form_submit_button(f"✅ {t('appointments.submit', 'Book Appointment')}", use_container_width=True, type="primary"):
            try:
                conn = sqlite3.connect(Config.DB_PATH)
                conn.execute("""
                    INSERT INTO appointments (user_id, customer_name, phone, appointment_type, preferred_date, preferred_time, car_brand, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (user['id'], user.get('full_name', ''), user.get('phone', ''),
                      apt_type, str(preferred_date), preferred_time, car_brand, notes))
                conn.commit()
                conn.close()
                st.success(f"✅ {t('appointments.booked', 'Appointment booked successfully!')}")
                st.balloons()
            except Exception as e:
                st.error(f"❌ {e}")
    
    # My appointments
    st.markdown("---")
    st.subheader(f"📋 {t('appointments.my_appointments', 'My Appointments')}")
    try:
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM appointments WHERE user_id=? ORDER BY preferred_date DESC", (user['id'],)).fetchall()
        conn.close()
        
        for apt in rows:
            status_colors = {'pending': '#f39c12', 'confirmed': '#27ae60', 'cancelled': '#e74c3c'}
            color = status_colors.get(apt['status'], '#7f8c8d')
            st.markdown(f"""
            <div style="background: #16213e; padding: 12px; border-radius: 10px; margin: 8px 0; border-left: 4px solid {color};">
                <b style="color: #D4AF37;">🗓️ {apt['preferred_date']} - {apt['preferred_time']}</b>
                <span style="background: {color}22; color: {color}; padding: 2px 8px; border-radius: 12px; margin-left: 10px;">{apt['status']}</span><br>
                <span style="color: #a0a0c0;">📋 {apt['appointment_type']} {('| 🚗 ' + apt['car_brand']) if apt['car_brand'] else ''}</span>
            </div>
            """, unsafe_allow_html=True)
        
        if not rows:
            st.info(t('appointments.no_appointments', 'No appointments yet'))
    except Exception as e:
        st.error(f"❌ {e}")


def _admin_view():
    """Admin: manage all appointments"""
    st.subheader(f"📋 {t('appointments.all', 'All Appointments')}")
    
    status_filter = st.selectbox("Filter", ['all', 'pending', 'confirmed', 'cancelled'], key="apt_filter")
    
    try:
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        q = "SELECT * FROM appointments"
        if status_filter != 'all':
            q += f" WHERE status='{status_filter}'"
        q += " ORDER BY preferred_date DESC"
        rows = conn.execute(q).fetchall()
        conn.close()
        
        for apt in rows:
            status_colors = {'pending': '#f39c12', 'confirmed': '#27ae60', 'cancelled': '#e74c3c'}
            color = status_colors.get(apt['status'], '#7f8c8d')
            
            with st.expander(f"🗓️ {apt['preferred_date']} {apt['preferred_time']} - {apt['customer_name'] or 'N/A'}"):
                st.write(f"**Type:** {apt['appointment_type']}")
                st.write(f"**Phone:** {apt['phone'] or '-'}")
                st.write(f"**Car:** {apt['car_brand'] or '-'}")
                st.write(f"**Notes:** {apt['notes'] or '-'}")
                
                c1, c2 = st.columns(2)
                with c1:
                    if apt['status'] == 'pending':
                        if st.button(f"✅ Confirm", key=f"conf_{apt['id']}"):
                            conn2 = sqlite3.connect(Config.DB_PATH)
                            conn2.execute("UPDATE appointments SET status='confirmed' WHERE id=?", (apt['id'],))
                            conn2.commit(); conn2.close()
                            st.rerun()
                with c2:
                    if apt['status'] != 'cancelled':
                        if st.button(f"❌ Cancel", key=f"canc_{apt['id']}"):
                            conn2 = sqlite3.connect(Config.DB_PATH)
                            conn2.execute("UPDATE appointments SET status='cancelled' WHERE id=?", (apt['id'],))
                            conn2.commit(); conn2.close()
                            st.rerun()
        
        if not rows:
            st.info("No appointments found")
    except Exception as e:
        st.error(f"❌ {e}")
