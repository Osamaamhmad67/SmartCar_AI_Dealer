"""
components/dialogs.py - نوافذ الحوار
SmartCar AI-Dealer
"""

import streamlit as st
from utils.i18n import t


# ======================

@st.dialog(t('nav.features'), width="large")
def show_features_dialog():
    """عرض ميزات التطبيق"""
    st.session_state['show_features'] = False
    
    st.markdown(f"""
## ✨ {t('features.title')}

---

### 🤖 {t('features.ai_recognition_title')}
{t('features.ai_recognition_desc')}

---

### 💰 {t('features.ai_pricing_title')}
{t('features.ai_pricing_desc')}

---

### 🔒 {t('features.data_protection_title')}
{t('features.data_protection_desc')}

---

### 🧾 {t('features.invoices_title')}
{t('features.invoices_desc')}

---

### 🌍 {t('features.multilingual_title')}
{t('features.multilingual_desc')}

---

### 📊 {t('features.dashboard_title')}
{t('features.dashboard_desc')}

---

### 👥 {t('features.employee_title')}
{t('features.employee_desc')}

---

### 📱 {t('features.easy_use_title')}
{t('features.easy_use_desc')}
    """)
    
    if st.button(t('buttons.close'), use_container_width=True, type="primary"):
        st.rerun()



# ======================
# دالة عن التطبيق
# ======================

@st.dialog(t('nav.about'), width="large")
def show_about_dialog():
    """عرض معلومات عن التطبيق"""
    st.session_state['show_about'] = False
    
    st.markdown(f"""
## ℹ️ {t('about.title')}

---

# 🏎️ SmartCar AI-Dealer
### {t('about.version')}

---

{t('about.description')}

---

## {t('about.main_features')}

- 🤖 {t('about.feature1')}
- 💰 {t('about.feature2')}
- 🔒 {t('about.feature3')}
- 🧾 {t('about.feature4')}
- 🌍 {t('about.feature5')}

---

## {t('about.developer')}
**{t('about.developer_name')}**

---

© 2024 SmartCar AI-Dealer. {t('about.rights')}
    """)
    
    if st.button(t('buttons.close'), use_container_width=True, type="primary"):
        st.rerun()


# ======================
# دالة عرض المساعدة
# ======================

@st.dialog(t('nav.help'), width="large")
def show_help_dialog():
    """عرض دليل سير العمل"""
    st.session_state['show_help'] = False
    
    st.markdown(f"""
## 📖 {t('help.title')}

### 🏎️ {t('help.workflow_title')}

---

#### 📸 {t('help.step1_title')}
{t('help.step1_desc')}

---

#### 📝 {t('help.step2_title')}
{t('help.step2_desc')}

---

#### 💰 {t('help.step3_title')}
{t('help.step3_desc')}

---

#### 💳 {t('help.step4_title')}
{t('help.step4_desc')}

---

#### 📄 {t('help.step5_title')}
{t('help.step5_desc')}

---

### 💡 {t('help.tips_title')}
    """)
    
    # عرض النصائح بتنسيق مخصص - نص أبيض واضح
    tips_html = f"""
    <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 15px;">
        <div style="background: linear-gradient(135deg, #1e5631 0%, #2d7a46 100%); padding: 12px 16px; border-radius: 8px; border-right: 4px solid #28a745;">
            <span style="color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-weight: 500;">✅ {t('help.tip1')}</span>
        </div>
        <div style="background: linear-gradient(135deg, #1e5631 0%, #2d7a46 100%); padding: 12px 16px; border-radius: 8px; border-right: 4px solid #28a745;">
            <span style="color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-weight: 500;">✅ {t('help.tip2')}</span>
        </div>
        <div style="background: linear-gradient(135deg, #1e5631 0%, #2d7a46 100%); padding: 12px 16px; border-radius: 8px; border-right: 4px solid #28a745;">
            <span style="color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-weight: 500;">✅ {t('help.tip3')}</span>
        </div>
    </div>
    """
    st.markdown(tips_html, unsafe_allow_html=True)
    
    if st.button(t('buttons.close'), use_container_width=True, type="primary"):
        st.rerun()


# ======================
# الشريط الجانبي
