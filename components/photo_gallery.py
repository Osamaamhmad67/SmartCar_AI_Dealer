"""
components/photo_gallery.py - Car Photo Gallery
SmartCar AI-Dealer - معرض صور السيارة
"""
import streamlit as st
import os, base64
from utils.i18n import t


def render_photo_gallery(transaction_id: int = None, image_path: str = None):
    """Render zoomable photo gallery for a car"""
    
    images = []
    
    # Get images from transaction folder
    if transaction_id:
        img_dir = os.path.join('uploads', str(transaction_id))
        if os.path.exists(img_dir):
            for f in os.listdir(img_dir):
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    images.append(os.path.join(img_dir, f))
    
    # Single image
    if image_path and os.path.exists(image_path):
        if image_path not in images:
            images.append(image_path)
    
    if not images:
        st.info(t('gallery.no_images', 'No images available'))
        return
    
    st.markdown(f"### 📸 {t('gallery.title', 'Photo Gallery')} ({len(images)})")
    
    # Thumbnails row
    if len(images) > 1:
        cols = st.columns(min(len(images), 5))
        for i, img_path in enumerate(images[:5]):
            with cols[i]:
                if st.button(f"📷 {i+1}", key=f"gal_thumb_{i}", use_container_width=True):
                    st.session_state['gallery_selected'] = i
    
    # Main image display with zoom
    selected_idx = st.session_state.get('gallery_selected', 0)
    if selected_idx < len(images):
        img_path = images[selected_idx]
        
        try:
            with open(img_path, 'rb') as f:
                img_bytes = f.read()
            b64 = base64.b64encode(img_bytes).decode()
            ext = img_path.split('.')[-1].lower()
            mime = 'jpeg' if ext in ('jpg', 'jpeg') else ext
            
            st.markdown(f"""
            <div style="text-align: center; background: #16213e; padding: 15px; border-radius: 15px;">
                <img src="data:image/{mime};base64,{b64}" 
                     style="max-width: 100%; max-height: 500px; border-radius: 10px; cursor: zoom-in;
                            transition: transform 0.3s;"
                     onclick="this.style.transform = this.style.transform === 'scale(2)' ? 'scale(1)' : 'scale(2)'"
                     alt="Car Photo {selected_idx + 1}">
                <p style="color: #a0a0c0; margin-top: 8px;">
                    📷 {t('gallery.photo', 'Photo')} {selected_idx + 1} / {len(images)}
                </p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ {e}")
    
    # Navigation
    if len(images) > 1:
        nav1, nav2 = st.columns(2)
        with nav1:
            if st.button(f"⬅️ {t('gallery.prev', 'Previous')}", key="gal_prev", use_container_width=True):
                st.session_state['gallery_selected'] = max(0, selected_idx - 1)
                st.rerun()
        with nav2:
            if st.button(f"➡️ {t('gallery.next', 'Next')}", key="gal_next", use_container_width=True):
                st.session_state['gallery_selected'] = min(len(images) - 1, selected_idx + 1)
                st.rerun()
