"""
components/reviews_component.py - Customer Reviews System
SmartCar AI-Dealer - نظام تقييمات العملاء
"""
import streamlit as st
import sqlite3
from datetime import datetime
from config import Config
from utils.i18n import t


def _ensure_reviews_table():
    conn = sqlite3.connect(Config.DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()


def render_reviews():
    """Render reviews section"""
    _ensure_reviews_table()
    user = st.session_state.get('user', {})
    
    st.markdown(f"""
    <div style="text-align: center; padding: 15px 0;">
        <h2 style="color: #D4AF37;">⭐ {t('reviews.title', 'Customer Reviews')}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    conn = sqlite3.connect(Config.DB_PATH)
    conn.row_factory = sqlite3.Row
    stats = conn.execute("SELECT COUNT(*) as cnt, AVG(rating) as avg_r FROM reviews").fetchone()
    total = stats['cnt']
    avg = stats['avg_r'] or 0
    
    s1, s2, s3 = st.columns(3)
    s1.metric(f"⭐ {t('reviews.average', 'Average')}", f"{avg:.1f}/5")
    s2.metric(f"📊 {t('reviews.total', 'Total Reviews')}", total)
    stars_display = '⭐' * round(avg) + '☆' * (5 - round(avg))
    s3.metric(t('reviews.rating', 'Rating'), stars_display)
    
    # Submit review
    if user:
        with st.expander(f"✍️ {t('reviews.write', 'Write a Review')}", expanded=False):
            with st.form("review_form"):
                rating = st.slider(t('reviews.your_rating', 'Your Rating'), 1, 5, 5, key="rev_rating")
                comment = st.text_area(t('reviews.comment', 'Comment'), max_chars=500, key="rev_comment")
                
                if st.form_submit_button(f"✅ {t('reviews.submit', 'Submit')}", use_container_width=True, type="primary"):
                    try:
                        conn2 = sqlite3.connect(Config.DB_PATH)
                        conn2.execute("INSERT INTO reviews (user_id, username, rating, comment) VALUES (?, ?, ?, ?)",
                            (user['id'], user.get('full_name', user.get('username', '')), rating, comment))
                        conn2.commit(); conn2.close()
                        st.success(f"✅ {t('reviews.thanks', 'Thank you for your review!')}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ {e}")
    
    st.markdown("---")
    
    # Show reviews
    reviews = conn.execute("SELECT * FROM reviews ORDER BY created_at DESC LIMIT 20").fetchall()
    conn.close()
    
    for rev in reviews:
        stars = '⭐' * rev['rating'] + '☆' * (5 - rev['rating'])
        date = rev['created_at'][:10] if rev['created_at'] else ''
        st.markdown(f"""
        <div style="background: #16213e; padding: 15px; border-radius: 10px; margin: 8px 0; border-left: 4px solid #D4AF37;">
            <div style="display: flex; justify-content: space-between;">
                <span style="color: white; font-weight: bold;">👤 {rev['username'] or 'Anonymous'}</span>
                <span style="color: #a0a0c0;">{date}</span>
            </div>
            <div style="margin: 5px 0;">{stars}</div>
            <p style="color: #a0a0c0; margin: 5px 0;">{rev['comment'] or ''}</p>
        </div>
        """, unsafe_allow_html=True)
    
    if not reviews:
        st.info(t('reviews.no_reviews', 'No reviews yet. Be the first!'))
