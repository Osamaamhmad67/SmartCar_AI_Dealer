"""
pages_app/predict_pages.py - صفحات تقييم السعر والنتائج
SmartCar AI-Dealer
"""

import streamlit as st
import streamlit.components.v1 as components
import os
import base64
import json
import time
from io import BytesIO
from datetime import datetime
from datetime import timedelta
from PIL import Image
from utils.i18n import t, get_current_lang, is_rtl, rtl_tabs
from config import Config
from db_manager import DatabaseManager
from groq_client import CarAIClient as GroqCarAnalyzer
from utils.predictor import PricePredictor
from utils.notifier import NotificationManager
from utils.invoice_generator import InvoiceGenerator
from components.html_components import (
    render_universal_header, get_predict_subheader_html,
    get_results_page_html, get_analysis_results_html, get_section_header_html
)
from components.navigation import navigate_to


# ======================
# دالة جلب مواصفات المحرك تلقائياً
# ======================
_car_specs_cache = None

def get_car_specs(brand: str, model: str) -> dict:
    """جلب CC و PS تلقائياً بناءً على الماركة والموديل"""
    global _car_specs_cache
    if _car_specs_cache is None:
        specs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'car_specs.json')
        try:
            with open(specs_path, 'r', encoding='utf-8') as f:
                _car_specs_cache = json.load(f)
        except:
            _car_specs_cache = {}
    
    if not brand or not _car_specs_cache:
        return {'cc': 0, 'ps': 0}
    
    # بحث عن الماركة (مطابقة مرنة)
    brand_data = None
    brand_lower = brand.strip().lower()
    for key in _car_specs_cache:
        if key.lower() == brand_lower or brand_lower.startswith(key.lower()) or key.lower().startswith(brand_lower):
            brand_data = _car_specs_cache[key]
            break
    
    if not brand_data:
        return {'cc': 0, 'ps': 0}
    
    if not model:
        default = brand_data.get('_default', {'cc': 0, 'ps': 0})
        return default
    
    # بحث عن الموديل (مطابقة مرنة)
    model_lower = model.strip().lower()
    for key in brand_data:
        if key == '_default':
            continue
        if key.lower() == model_lower or model_lower in key.lower() or key.lower() in model_lower:
            return brand_data[key]
    
    # إذا لم يُعثر على الموديل، نستخدم القيمة الافتراضية للماركة
    return brand_data.get('_default', {'cc': 0, 'ps': 0})


# ======================
# مكونات واجهة المستخدم
# ======================

def render_progress_bar(current_step):
    """عرض شريط التقدم"""
    steps = {
        1: t('predict.step1_title'),
        2: t('predict.step2_title'),
        3: t('predict.step3_title')
    }
    
    st.markdown("""
    <style>
    .progress-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
        position: fixed;
        top: 80px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 99999;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 10px 40px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        border-radius: 50px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        width: auto;
        min-width: 600px;
        max-width: 90%;
    }
    .progress-container::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 40px;
        right: 40px;
        width: auto;
        height: 4px;
        background: #e0e0e0;
        z-index: 0;
        transform: translateY(-50%);
    }
    .step {
        position: relative;
        z-index: 1;
        background: white;
        width: 35px;
        height: 35px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid #e0e0e0;
        font-weight: bold;
        color: #7f8c8d;
        font-size: 14px;
        transition: all 0.3s ease;
    }
    .step.active {
        background: #4facfe;
        color: white;
        border-color: #4facfe;
        transform: scale(1.1);
        box-shadow: 0 0 10px rgba(79, 172, 254, 0.4);
    }
    .step.completed {
        background: #38ef7d;
        color: white;
        border-color: #38ef7d;
    }
    .step-label {
        position: absolute;
        top: 45px;
        left: 50%;
        transform: translateX(-50%);
        white-space: nowrap;
        font-size: 12px;
        color: #555;
        font-weight: 500;
        background: rgba(255,255,255,0.9);
        padding: 2px 8px;
        border-radius: 10px;
    }
    .step.active .step-label {
        color: #4facfe;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # بناء HTML للشريط
    html_content = '<div class="progress-container">'
    for step_num, label in steps.items():
        if step_num < current_step:
            cls = "step completed"
            icon = "✓"
        elif step_num == current_step:
            cls = "step active"
            icon = str(step_num)
        else:
            cls = "step"
            icon = str(step_num)
            
        html_content += f'<div class="{cls}">{icon}<div class="step-label">{label}</div></div>'
    
    html_content += '</div>'
    
    st.markdown(html_content, unsafe_allow_html=True)


# ======================
# صفحة تقدير السعر
# ======================

def predict_page():
    """صفحة تقدير السعر"""
    render_progress_bar(1)
    
    # تحميل بيانات العميل من قاعدة البيانات
    if st.session_state.get('user'):
        db = DatabaseManager()
        fresh_user = db.get_user_by_id(st.session_state.user['id'])
        if fresh_user:
            st.session_state.user = fresh_user
    
    st.session_state.user = fresh_user

    # Render universal header
    render_universal_header(t('nav.predict'), "🏎️ " + t('predict.ai_evaluation'))
    
    st.markdown("---")
    
    # الخطوة 1: رفع الصورة
    st.subheader(f"📸 {t('predict.step1_title')}")
    
    # اختيار طريقة الحصول على الصورة
    image_tab1, image_tab2 = rtl_tabs([f"📁 {t('predict.upload_image')}", f"📷 {t('predict.capture_image')}"])
    
    images_to_analyze = {}
    main_image_bytes = None
    
    with image_tab1:
        st.markdown(f"### 📸 {t('predict.upload_images')}")
        st.info(f"💡 {t('predict.upload_hint')}")
        
        col_up1, col_up2, col_up3 = st.columns(3)
        
        with col_up1:
            st.markdown(f"**1. {t('predict.front_image')}**")
            front_img = st.file_uploader(t('predict.front_image'), type=['jpg', 'jpeg', 'png', 'webp'], key="up_front")
        
        with col_up2:
            st.markdown(f"**2. {t('predict.side_image')}**")
            side_img = st.file_uploader(t('predict.side_image'), type=['jpg', 'jpeg', 'png', 'webp'], key="up_side")
            
        with col_up3:
            st.markdown(f"**3. {t('predict.interior_image')}**")
            interior_img = st.file_uploader(t('predict.interior_image'), type=['jpg', 'jpeg', 'png', 'webp'], key="up_interior")

        # صف ثاني: المؤخرة + المحرك
        col_up4, col_up5, _ = st.columns(3)
        
        with col_up4:
            st.markdown(f"**4. {t('predict.rear_image', 'Rear View')}** 🔙")
            rear_img = st.file_uploader(t('predict.rear_image', 'Rear view'), type=['jpg', 'jpeg', 'png', 'webp'], key="up_rear")
        
        with col_up5:
            st.markdown(f"**5. {t('predict.engine_image', 'Engine')}** ⚙️")
            engine_img = st.file_uploader(t('predict.engine_image', 'Engine compartment'), type=['jpg', 'jpeg', 'png', 'webp'], key="up_engine")

        # تجميع الصور
        
        if front_img:
            images_to_analyze['front'] = front_img.getvalue()
            main_image_bytes = front_img.getvalue()
            
        if side_img:
            images_to_analyze['side'] = side_img.getvalue()
            
        if interior_img:
            images_to_analyze['interior'] = interior_img.getvalue()

        if rear_img:
            images_to_analyze['rear'] = rear_img.getvalue()
            
        if engine_img:
            images_to_analyze['engine'] = engine_img.getvalue()


    with image_tab2:
        # تلميح مهم للمستخدم
        st.warning(f"📸 {t('predict.camera_tip', 'Get close to the car and make sure the brand LOGO is clearly visible for accurate identification!')}")
        
        # الكاميرا (دائماً الصورة الأمامية متاحة)
        st.markdown(f"##### 1. {t('predict.front_image')}")
        
        # تصغير الكاميرا إلى 50% مع معالجة الصورة (قص الحواف)
        cam_col1, cam_col2, cam_col3 = st.columns([1, 2, 1])
        with cam_col2:
            camera_front = st.camera_input(t('predict.take_front_photo'), key="cam_front")
            if camera_front:
                # معالجة الصورة لقص الزوائد الجانبية (15% من كل جانب)
                try:
                    img = Image.open(camera_front)
                    width, height = img.size
                    
                    # إضافة slider للتكبير (Zoom)
                    zoom_level = st.slider(
                        f"🔍 {t('predict.zoom_level', 'Zoom Level')}",
                        min_value=1.0,
                        max_value=3.0,
                        value=1.0,
                        step=0.1,
                        key="front_zoom",
                        help=t('predict.zoom_help', 'Zoom in to capture the brand logo more clearly')
                    )
                    
                    # حساب منطقة القص بناءً على مستوى التكبير
                    if zoom_level > 1.0:
                        # حساب حجم المنطقة المقصوصة (كلما زاد الزوم، صغرت المنطقة)
                        crop_ratio = 1.0 / zoom_level
                        new_width = width * crop_ratio
                        new_height = height * crop_ratio
                        
                        # حساب إحداثيات القص من المركز
                        left = (width - new_width) / 2
                        top = (height - new_height) / 2
                        right = left + new_width
                        bottom = top + new_height
                    else:
                        # الزوم الافتراضي: قص 15% من الجوانب فقط
                        left = width * 0.15
                        top = 0
                        right = width * 0.85
                        bottom = height
                    
                    img_cropped = img.crop((left, top, right, bottom))
                    
                    # عرض الصورة المقصوصة للمستخدم
                    st.image(img_cropped, caption=f"📷 {t('predict.zoomed_preview', 'Zoomed Preview')} ({zoom_level}x)", use_container_width=True)
                    
                    # تحويل الصورة المقصوصة إلى bytes
                    buf = BytesIO()
                    img_cropped.save(buf, format="JPEG")
                    main_image_bytes = buf.getvalue()
                    images_to_analyze['front'] = main_image_bytes
                    
                    st.success(f"✅ {t('predict.image_processed_success')}")
                except Exception as e:
                    st.error(f"❌ {t('predict.image_process_error')}: {e}")
                    # في حالة الخطأ، نستخدم الصورة الأصلية
                    images_to_analyze['front'] = camera_front.getvalue()
                    main_image_bytes = camera_front.getvalue()


        
        # خيار التقاط صور إضافية
        if st.checkbox(f"📸 {t('predict.enable_multi_cam')}", key="enable_multi_cam"):
            col_cam_side, col_cam_int = st.columns(2)
            
            with col_cam_side:
                st.markdown(f"##### {t('predict.side_image_header')}")
                camera_side = st.camera_input(t('predict.take_side_photo'), key="cam_side")
                if camera_side:
                    images_to_analyze['side'] = camera_side.getvalue()
            
            with col_cam_int:
                st.markdown(f"##### {t('predict.interior_image_header')}")
                camera_interior = st.camera_input(t('predict.take_interior_photo'), key="cam_interior")
                if camera_interior:
                    images_to_analyze['interior'] = camera_interior.getvalue()

    if main_image_bytes:
        # حفظ الصورة الرئيسية للعرض
        st.session_state.uploaded_image = main_image_bytes
        
        # عرض الصور المرفوعة
        st.markdown("---")
        st.markdown(f"### 🖼️ {t('admin.selected_images')}")
        
        num_images = len(images_to_analyze)
        if num_images == 1:
            # إذا كانت صورة واحدة، نعرضها بحجم أصغر (50% تقريباً) وفي المنتصف
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                for label, img_data in images_to_analyze.items():
                    localized_label = t(f'predict.label_{label}') if t(f'predict.label_{label}') else label
                    st.image(img_data, caption=t('predict.image_caption', label=localized_label), use_container_width=True)
        else:
            # عرض متعدد (أعمدة متساوية)
            disp_cols = st.columns(num_images)
            for idx, (label, img_data) in enumerate(images_to_analyze.items()):
                with disp_cols[idx]:
                    localized_label = t(f'predict.label_{label}') if t(f'predict.label_{label}') else label
                    st.image(img_data, caption=t('predict.image_caption', label=localized_label), use_container_width=True)
        
        # التحقق الأولي (توفير التكلفة)
        st.markdown("---")
        col_check, col_analyze = st.columns([1, 1])
        
        with col_check:
            st.warning(f"🔄 {t('admin.verifying_image')}")
            # التحقق السريع (أقل تكلفة)
            analyzer = GroqCarAnalyzer()
            validation = analyzer.quick_validate_image(main_image_bytes)
            
            if validation['is_valid']:
                st.success(f"✅ **{t('admin.valid_image')}**")
                valid_car = True
            else:
                st.error(f"❌ **{t('admin.alert')}:** {validation['message']}")
                st.warning(t('admin.upload_clear_image'))
                valid_car = False
        
        with col_analyze:
            if valid_car:
                if st.button(f"🤖 {t('admin.ai_full_analysis')}", type="primary"):
                    with st.spinner(t('admin.analyzing_images')):
                        try:
                            # استخدام التحليل المتعدد
                            analysis_result = analyzer.analyze_car_from_multiple_angles(images_to_analyze)
                            
                            st.session_state.analysis_result = analysis_result
                            st.session_state.car_details['analysis'] = analysis_result
                            
                            if analysis_result.get('success'):
                                st.success(f"✅ {t('messages.success')}")
                                st.rerun()
                            else:
                                st.warning(f"⚠️ {analysis_result.get('error', t('messages.error'))}")
                        except Exception as e:
                            st.error(f"❌ {t('messages.error')}: {str(e)}")
            else:
                st.button(f"🤖 {t('predict.analyzing')}", disabled=True, help=t('predict.upload_hint'))
    
    # عرض نتائج التحليل
    if st.session_state.get('analysis_result') and st.session_state.analysis_result.get('success'):
        st.markdown("---")
        analysis = st.session_state.analysis_result
        
        # استدعاء المكون الجديد بدلاً من الكود القديم
        get_analysis_results_html(analysis)
        
        # Legacy expander restored by user request
        with st.expander(f"📊 {t('predict.analysis_details')}", expanded=True):
            st.write(f"**{t('predict.expected_brand')}:** {analysis.get('estimated_brand', t('messages.unknown'))}")
            st.write(f"**{t('predict.expected_model')}:** {analysis.get('estimated_model', t('messages.unknown'))}")
            st.write(f"**{t('predict.color')}:** {analysis.get('color', t('messages.unknown'))}")
            
            # Use dynamic condition map
            cond_map = {
                'Excellent': t('predict.cond_excellent'), 
                'Good': t('predict.cond_good'), 
                'Fair': t('predict.cond_fair'), 
                'Poor': t('predict.cond_poor')
            }
            raw_cond = analysis.get('exterior_condition', analysis.get('condition', 'Good'))
            condition = cond_map.get(raw_cond, raw_cond)
            
            st.write(f"**حالة الهيكل الخارجي:** {condition}")
            
            damages = analysis.get('visible_damage', [])
            if damages and damages != ['لا يوجد'] and damages != ['None']:
                st.write(f"**الأضرار المرئية:** {', '.join(damages)}")
            else:
                st.write("**الأضرار المرئية:** لا توجد أضرار ظاهرة")
            
            if analysis.get('notes'):
                st.write(f"**ملاحظات:** {analysis.get('notes')}")

    
    # الخطوة 2: معلومات إضافية
    if st.session_state.uploaded_image:
        st.markdown("<br>", unsafe_allow_html=True)
        get_section_header_html(f"📊 {t('admin.step2_car_info')}")
        
        st.info(f"💡 {t('predict.upload_hint')}")
        
        # استخراج القيم من التحليل
        analysis = st.session_state.get('analysis_result') or {}
        has_analysis = analysis.get('success', False) if analysis else False
        
        # تحديد نوع السيارة من التحليل
        car_type_options = [t('admin.car_type_sedan'), t('admin.car_type_suv'), t('admin.car_type_coupe'), t('admin.car_type_hybrid'), t('admin.car_type_electric'), t('admin.car_type_pickup')]
        default_type_index = 0
        if analysis.get('estimated_type'):
            estimated_type = analysis.get('estimated_type', '')
            for i, opt in enumerate(car_type_options):
                if opt in estimated_type or estimated_type in opt:
                    default_type_index = i
                    break
        
        # استخراج القيم الافتراضية
        default_year = 2020
        year_range = analysis.get('estimated_year_range', '')
        if year_range and year_range != 'غير معروف':
            try:
                import re
                years = re.findall(r'20\d{2}', str(year_range))
                if years:
                    default_year = int(years[-1])
            except:
                pass

        default_brand = analysis.get('estimated_brand', '') if analysis.get('estimated_brand') != 'غير معروف' else ""
        default_model = analysis.get('estimated_model', '') if analysis.get('estimated_model') != 'غير معروف' else ""

        # تخطيط 4 أعمدة للمدخلات (الصف الأول: البيانات الأساسية)
        c1, c2, c3, c4 = st.columns(4)
        
        # تخطيط 4 أعمدة للمدخلات (الصف الثاني: المواصفات)
        c5, c6, c7, c8 = st.columns(4)

        # تخطيط 4 أعمدة للمدخلات (الصف الثالث: التوف والصيانة)
        c9, c10, c11, c12 = st.columns(4)
        
        # تخطيط 4 أعمدة للمدخلات (الصف الرابع: اللون والمقاعد)
        c13, c14, c15, c16 = st.columns(4)

        # تخطيط 4 أعمدة (الصف الخامس: ناقل الحركة، الدفع، الانبعاثات، المحرك)
        c17, c18, c19, c20 = st.columns(4)

        # تخطيط 4 أعمدة (الصف السادس: قوة المحرك، الحوادث، الضمان، دفتر الصيانة)
        c21, c22, c23, c24 = st.columns(4)

        # تخطيط كامل (الصف السابع: التجهيزات الإضافية)
        equip_container = st.container()

        if has_analysis:
            # الصف الأول
            with c1:
                car_type = st.text_input(t('predict.car_type'), value=car_type_options[default_type_index], disabled=True, key="live_type")
            with c2:
                brand = st.text_input(t('predict.brand'), value=default_brand, disabled=True, key="live_brand")
            with c3:
                model = st.text_input(t('predict.model'), value=default_model, disabled=True, key="live_model")
            with c4:
                manufacture_year = st.number_input(t('predict.year'), min_value=1990, max_value=datetime.now().year + 1, value=default_year, disabled=True, key="live_year")
            
            # منطق قفل نوع الوقود
            fuel_options = [t('admin.fuel_gasoline'), t('admin.fuel_diesel'), t('admin.fuel_hybrid'), t('admin.fuel_electric')]
            analyzed_fuel = analysis.get('fuel_type', '')
            fuel_idx = 0
            fuel_disabled = False
            if analyzed_fuel in fuel_options:
                fuel_idx = fuel_options.index(analyzed_fuel)
                fuel_disabled = True
            
            # منطق الحالة
            # منطق الحالة
            cond_map_form = {
                'Excellent': t('admin.condition_excellent'), 'Good': t('admin.condition_good'), 'Fair': t('admin.condition_fair'), 'Poor': t('admin.condition_poor')
            }
            raw_cond_form = analysis.get('exterior_condition', analysis.get('condition', ''))
            default_condition = cond_map_form.get(raw_cond_form, t('admin.condition_good'))
            
            condition_options = [t('admin.condition_excellent'), t('admin.condition_very_good'), t('admin.condition_good'), t('admin.condition_fair'), t('admin.condition_poor')]
            cond_idx = 2
            if default_condition in condition_options:
                cond_idx = condition_options.index(default_condition)

            # الصف الثاني
            with c5:
                fuel_type = st.selectbox(t('admin.fuel_type'), fuel_options, index=fuel_idx, disabled=fuel_disabled, key="live_fuel")
            with c6:
                condition = st.selectbox(t('admin.car_condition_label'), condition_options, index=cond_idx, help=t('admin.car_condition_label'), key="live_condition")
            with c7:
                mileage = st.number_input(t('admin.mileage_km'), min_value=0, max_value=1000000, value=0, step=1000, help=t('admin.mileage_km'), key="live_mileage")
            with c8:
                previous_owners = st.number_input(t('admin.previous_owners'), min_value=1, max_value=10, value=1, step=1, help=t('admin.previous_owners'), key="live_owners")
            
            # الصف الثالث (التوف والصيانة)
            with c9:
                tuv_start = st.date_input(t('admin.tuv_start'), value=datetime.now(), format="DD/MM/YYYY", key="live_tuv_start")
            with c10:
                default_end = datetime.now() + timedelta(days=365)
                tuv_end = st.date_input(t('admin.tuv_end'), value=default_end, format="DD/MM/YYYY", key="live_tuv_end")
            with c11:
                # حساب المدة المتبقية
                tuv_remaining_days = (tuv_end - datetime.now().date()).days
                tuv_months = int(tuv_remaining_days / 30)
                
                tuv_display = f"{tuv_months} {t('admin.month')}"
                if tuv_months < 0: tuv_display = t('admin.expired')
                
                st.metric(t('admin.tuv_remaining'), tuv_display)
                
            with c12:
                maintenance_opt = st.selectbox(t('admin.maintenance'), [t('admin.maintenance_yes'), t('admin.maintenance_no')], index=0, key="live_maintenance")
                has_maintenance = (maintenance_opt == t('admin.maintenance_yes'))
            
            # الصف الرابع (اللون والمقاعد)
            default_color = analysis.get('color', '').lower().strip()
            color_options = [t('admin.color_white'), t('admin.color_black'), t('admin.color_gray'), t('admin.color_silver'), t('admin.color_red'), t('admin.color_blue'), t('admin.color_green'), t('admin.color_brown'), t('admin.color_gold'), t('admin.color_other')]
            
            # خريطة الألوان الإنجليزية للفهرس
            color_mapping = {
                'white': 0, 'weiß': 0, 'weiss': 0, 'أبيض': 0,
                'black': 1, 'schwarz': 1, 'أسود': 1,
                'gray': 2, 'grey': 2, 'grau': 2, 'رمادي': 2,
                'silver': 3, 'silber': 3, 'فضي': 3,
                'red': 4, 'rot': 4, 'أحمر': 4,
                'blue': 5, 'blau': 5, 'أزرق': 5,
                'green': 6, 'grün': 6, 'gruen': 6, 'أخضر': 6,
                'brown': 7, 'braun': 7, 'بني': 7,
                'gold': 8, 'golden': 8, 'ذهبي': 8,
            }
            
            color_idx = 0
            if default_color:
                # البحث في الخريطة أولاً
                for color_key, idx in color_mapping.items():
                    if color_key in default_color:
                        color_idx = idx
                        break
            
            with c13:
                color = st.selectbox(t('admin.car_color'), color_options, index=color_idx, key="live_color")
            with c14:
                seats = st.number_input(t('admin.seats_count'), min_value=2, max_value=9, value=5, key="live_seats")
            with c15:
                st.write("")  # فارغ
            with c16:
                st.write("")  # فارغ

            # الصف الخامس - المواصفات التقنية الإضافية
            with c17:
                transmission_options = [t('admin.trans_automatic'), t('admin.trans_manual'), t('admin.trans_dsg'), t('admin.trans_cvt')]
                transmission = st.selectbox(t('admin.transmission'), transmission_options, index=0, key="live_transmission")
            with c18:
                drivetrain_options = [t('admin.drive_fwd'), t('admin.drive_rwd'), t('admin.drive_awd'), t('admin.drive_4wd')]
                drivetrain = st.selectbox(t('admin.drivetrain'), drivetrain_options, index=0, key="live_drivetrain")
            with c19:
                emissions_options = ['Euro 6d', 'Euro 6', 'Euro 5', 'Euro 4', 'Euro 3']
                emissions_class = st.selectbox(t('admin.emissions_class'), emissions_options, index=0, key="live_emissions")
            with c20:
                # ملء تلقائي CC من بيانات الماركة/الموديل
                ai_cc = int(analysis.get('engine_cc', 0))
                if ai_cc == 0:
                    auto_specs = get_car_specs(default_brand, default_model)
                    ai_cc = auto_specs.get('cc', 0)
                engine_cc = st.number_input(t('admin.engine_cc'), min_value=0, max_value=8000, value=ai_cc, step=100, key="live_engine_cc")

            # الصف السادس - قوة المحرك والحالة
            with c21:
                # ملء تلقائي PS من بيانات الماركة/الموديل
                ai_ps = int(analysis.get('horsepower', 0))
                if ai_ps == 0:
                    auto_specs = get_car_specs(default_brand, default_model)
                    ai_ps = auto_specs.get('ps', 0)
                horsepower = st.number_input(t('admin.horsepower'), min_value=0, max_value=1500, value=ai_ps, step=10, key="live_hp")
            with c22:
                accident_options = [t('admin.accident_none'), t('admin.accident_minor'), t('admin.accident_moderate'), t('admin.accident_major'), t('admin.accident_structural')]
                accident_history = st.selectbox(t('admin.accident_history'), accident_options, index=0, key="live_accident")
            with c23:
                warranty_options = [t('admin.warranty_2plus'), t('admin.warranty_1to2'), t('admin.warranty_less1'), t('admin.warranty_none')]
                warranty = st.selectbox(t('admin.warranty'), warranty_options, index=0, key="live_warranty")
            with c24:
                service_options = [t('admin.service_complete'), t('admin.service_partial'), t('admin.service_none')]
                service_book = st.selectbox(t('admin.service_book'), service_options, index=0, key="live_service")

            # الصف السابع - التجهيزات الإضافية
            with equip_container:
                st.markdown(f"**{t('admin.equipment')}**")
                eq_cols = st.columns(5)
                equipment_items = []
                equip_keys = [
                    ('leather', 'admin.equip_leather'), ('navigation', 'admin.equip_navigation'),
                    ('sunroof', 'admin.equip_sunroof'), ('panoramic_roof', 'admin.equip_panoramic'),
                    ('heated_seats', 'admin.equip_heated_seats'), ('parking_sensors', 'admin.equip_parking_sensors'),
                    ('parking_camera', 'admin.equip_parking_camera'), ('led_headlights', 'admin.equip_led'),
                    ('adaptive_cruise', 'admin.equip_cruise'), ('apple_carplay', 'admin.equip_carplay'),
                    ('sport_package', 'admin.equip_sport'), ('keyless_entry', 'admin.equip_keyless'),
                    ('ambient_lighting', 'admin.equip_ambient'), ('heads_up_display', 'admin.equip_hud'),
                    ('camera_360', 'admin.equip_cam360'),
                ]
                for idx, (key, label_key) in enumerate(equip_keys):
                    with eq_cols[idx % 5]:
                        if st.checkbox(t(label_key), key=f"equip_{key}"):
                            equipment_items.append(key)

        else:
            # وضع يدوي
            with c1:
                car_type = st.selectbox(f"{t('admin.car_type_required')} *", car_type_options, index=0, key="live_type_man")
            with c2:
                brand = st.text_input(f"{t('admin.brand_required')} *", value="", key="live_brand_man")
            with c3:
                model = st.text_input(t('admin.model_optional'), value="", key="live_model_man")
            with c4:
                manufacture_year = st.number_input(f"{t('admin.manufacture_year')} *", min_value=1990, max_value=datetime.now().year + 1, value=2020, key="live_year_man")
            
            with c5:
                fuel_type = st.selectbox(f"{t('admin.fuel_type')} *", [t('admin.fuel_gasoline'), t('admin.fuel_diesel'), t('admin.fuel_hybrid'), t('admin.fuel_electric')], index=0, key="live_fuel_man")
            with c6:
                condition = st.selectbox(f"{t('admin.car_condition')} *", [t('admin.condition_excellent'), t('admin.condition_very_good'), t('admin.condition_good'), t('admin.condition_fair'), t('admin.condition_poor')], index=2, key="live_condition_man")
            with c7:
                mileage = st.number_input(f"{t('admin.mileage_km')} *", min_value=0, max_value=1000000, value=50000, step=1000, key="live_mileage_man")
            with c8:
                previous_owners = st.number_input(t('admin.previous_owners'), min_value=1, max_value=10, value=1, step=1, key="live_owners_man")
            
            # الصف الثالث (التوف والصيانة) - يدوي
            with c9:
                tuv_start = st.date_input(t('admin.tuv_start'), value=datetime.now(), format="DD/MM/YYYY", key="live_tuv_start_man")
            with c10:
                default_end = datetime.now() + timedelta(days=365)
                tuv_end = st.date_input(t('admin.tuv_end'), value=default_end, format="DD/MM/YYYY", key="live_tuv_end_man")
            with c11:
                tuv_remaining_days = (tuv_end - datetime.now().date()).days
                tuv_months = int(tuv_remaining_days / 30)
                
                tuv_display = f"{tuv_months} {t('admin.month')}"
                if tuv_months < 0: 
                    tuv_display = f"{t('admin.expired')} ❌"
                
                st.metric(t('admin.tuv_remaining'), tuv_display)
                
                # عرض التأثير بشكل منفصل لضمان ظهوره
                if tuv_months > 12:
                    st.caption(f"**:green[{t('admin.price_increase_tuv')} 📈]**")
                elif tuv_months < 3:
                    st.caption(f"**:red[{t('admin.price_decrease_tuv')} 📉]**")
                else:
                    st.caption(f"**:grey[{t('admin.price_neutral_tuv')} 😐]**")
            with c12:
                maintenance_opt = st.selectbox(t('admin.maintenance'), [t('admin.maintenance_yes'), t('admin.maintenance_no')], index=0, key="live_maintenance_man")
                has_maintenance = (maintenance_opt == t('admin.maintenance_yes'))
            
            # الصف الرابع (اللون والمقاعد) - يدوي
            color_options = [t('admin.color_white'), t('admin.color_black'), t('admin.color_gray'), t('admin.color_silver'), t('admin.color_red'), t('admin.color_blue'), t('admin.color_green'), t('admin.color_brown'), t('admin.color_gold'), t('admin.color_other')]
            with c13:
                color = st.selectbox(t('admin.car_color'), color_options, index=0, key="live_color_man")
            with c14:
                seats = st.number_input(t('admin.seats_count'), min_value=2, max_value=9, value=5, key="live_seats_man")
            with c15:
                st.write("")  # فارغ
            with c16:
                st.write("")  # فارغ

            # الصف الخامس - المواصفات التقنية (يدوي)
            with c17:
                transmission_options = [t('admin.trans_automatic'), t('admin.trans_manual'), t('admin.trans_dsg'), t('admin.trans_cvt')]
                transmission = st.selectbox(t('admin.transmission'), transmission_options, index=0, key="live_transmission_man")
            with c18:
                drivetrain_options = [t('admin.drive_fwd'), t('admin.drive_rwd'), t('admin.drive_awd'), t('admin.drive_4wd')]
                drivetrain = st.selectbox(t('admin.drivetrain'), drivetrain_options, index=0, key="live_drivetrain_man")
            with c19:
                emissions_options = ['Euro 6d', 'Euro 6', 'Euro 5', 'Euro 4', 'Euro 3']
                emissions_class = st.selectbox(t('admin.emissions_class'), emissions_options, index=0, key="live_emissions_man")
            with c20:
                # ملء تلقائي CC من بيانات الماركة/الموديل (الوضع اليدوي)
                man_specs = get_car_specs(brand, model)
                man_cc = man_specs.get('cc', 0)
                engine_cc = st.number_input(t('admin.engine_cc'), min_value=0, max_value=8000, value=man_cc, step=100, key="live_engine_cc_man",
                                           help=f"💡 Auto: {man_cc} cc" if man_cc > 0 else None)

            # الصف السادس - يدوي
            with c21:
                man_ps = man_specs.get('ps', 0)
                horsepower = st.number_input(t('admin.horsepower'), min_value=0, max_value=1500, value=man_ps, step=10, key="live_hp_man",
                                            help=f"💡 Auto: {man_ps} PS" if man_ps > 0 else None)
            with c22:
                accident_options = [t('admin.accident_none'), t('admin.accident_minor'), t('admin.accident_moderate'), t('admin.accident_major'), t('admin.accident_structural')]
                accident_history = st.selectbox(t('admin.accident_history'), accident_options, index=0, key="live_accident_man")
            with c23:
                warranty_options = [t('admin.warranty_2plus'), t('admin.warranty_1to2'), t('admin.warranty_less1'), t('admin.warranty_none')]
                warranty = st.selectbox(t('admin.warranty'), warranty_options, index=0, key="live_warranty_man")
            with c24:
                service_options = [t('admin.service_complete'), t('admin.service_partial'), t('admin.service_none')]
                service_book = st.selectbox(t('admin.service_book'), service_options, index=0, key="live_service_man")

            # الصف السابع - التجهيزات (يدوي)
            with equip_container:
                st.markdown(f"**{t('admin.equipment')}**")
                eq_cols = st.columns(5)
                equipment_items = []
                equip_keys = [
                    ('leather', 'admin.equip_leather'), ('navigation', 'admin.equip_navigation'),
                    ('sunroof', 'admin.equip_sunroof'), ('panoramic_roof', 'admin.equip_panoramic'),
                    ('heated_seats', 'admin.equip_heated_seats'), ('parking_sensors', 'admin.equip_parking_sensors'),
                    ('parking_camera', 'admin.equip_parking_camera'), ('led_headlights', 'admin.equip_led'),
                    ('adaptive_cruise', 'admin.equip_cruise'), ('apple_carplay', 'admin.equip_carplay'),
                    ('sport_package', 'admin.equip_sport'), ('keyless_entry', 'admin.equip_keyless'),
                    ('ambient_lighting', 'admin.equip_ambient'), ('heads_up_display', 'admin.equip_hud'),
                    ('camera_360', 'admin.equip_cam360'),
                ]
                for idx, (key, label_key) in enumerate(equip_keys):
                    with eq_cols[idx % 5]:
                        if st.checkbox(t(label_key), key=f"equip_{key}_man"):
                            equipment_items.append(key)

        # معاينة السعر المباشرة
        st.markdown("<br>", unsafe_allow_html=True)
        get_section_header_html(f"👁️ {t('admin.live_price_preview')}")
        
        if brand: # حساب فقط عند وجود البيانات الأساسية
            try:
                # تهيئة الكائن
                predictor = PricePredictor()
                
                # نستخدم القيم المباشرة من السيشن لضمان التحديث اللحظي
                current_condition = st.session_state.get("live_condition", condition)
                current_mileage = st.session_state.get("live_mileage", mileage)
                current_owners = st.session_state.get("live_owners", previous_owners)
                # حساب ال TUV من الودجت مباشرة
                # ملاحظة: التاريخ لا يمكن الوصول له بسهولة من ال session state بنفس طريقة النص، لذا نستخدم القيم المحسوبة
                
                # تحويل الحالة النصية إلى رقمية
                condition_map = {
                    'ممتازة': 1.0, 'جيدة جداً': 0.9, 'جيدة': 0.8,
                    'مقبولة': 0.6, 'سيئة': 0.4, 'سيئة جداً': 0.2
                }
                c_score = condition_map.get(current_condition, 0.8)

                # تجهيز البيانات كـ Dictionary كما يتوقعها PricePredictor
                live_data = {
                    'car_type': car_type,
                    'brand': brand,
                    'condition_score': c_score,
                    'mileage': current_mileage,
                    'manufacture_year': manufacture_year,
                    'fuel_type': fuel_type,
                    'owners': current_owners,
                    'maintenance': has_maintenance,
                    'tuv_months': tuv_months,
                    'transmission': transmission,
                    'drivetrain': drivetrain,
                    'color': color,
                    'emissions_class': emissions_class,
                    'engine_cc': engine_cc,
                    'horsepower': horsepower,
                    'accident_history': accident_history,
                    'warranty': warranty,
                    'service_book': service_book,
                    'equipment': equipment_items,
                }
                
                # توقع السعر
                with st.spinner(t('admin.updating_price')):
                     live_price = predictor.predict_price(live_data)

                
                # عرض السعر في بطاقة ملونة
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #000000 0%, #333333 100%);
                    padding: 20px;
                    border-radius: 15px;
                    color: white;
                    text-align: center;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                    margin-top: 10px;
                    border: 1px solid rgba(255,255,255,0.2);">
                    <small style="opacity: 0.8">السعر التقديري الحالي</small>
                    <h1 style="color: white; margin: 10px 0; font-size: 2.5em;">${live_price:,.0f}</h1>
                    <div style="font-size: 0.9em; opacity: 0.7; margin-top: 5px;">
                        {car_type} | {manufacture_year} | {condition}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"{t('admin.calculating')} ({e})")
        else:
            st.info(t('admin.enter_car_data'))

        st.markdown("---")
        if st.button(f"✅ {t('admin.approve_result')}", type="primary", use_container_width=True):
             if not brand:
                 st.error(f"⚠️ {t('admin.enter_brand')}")
             else:
                 # حفظ البيانات
                 st.session_state.car_details.update({
                     'car_type': car_type,
                     'brand': brand,
                     'model': model,
                     'manufacture_year': manufacture_year,
                     'mileage': mileage,
                     'fuel_type': fuel_type,
                     'color': color,
                     'seats': seats,
                     'previous_owners': previous_owners,
                     'tuv_months': tuv_months,
                     'maintenance_history': has_maintenance,
                     'condition': condition,
                     'transmission': transmission,
                     'drivetrain': drivetrain,
                     'emissions_class': emissions_class,
                     'engine_cc': engine_cc,
                     'horsepower': horsepower,
                     'accident_history': accident_history,
                     'warranty': warranty,
                     'service_book': service_book,
                     'equipment': equipment_items,
                 })
                 navigate_to('results')


# ======================
# صفحة النتائج
# ======================

def results_page():
    """صفحة عرض النتائج"""
    render_progress_bar(3)
    
    # Render universal header
    render_universal_header(t('results.title'), "📊 " + t('results.evaluation_results'))
    
    # التحقق من وجود البيانات
    if not st.session_state.uploaded_image or not st.session_state.car_details:
        st.error(f"⚠️ {t('messages.error')}")
        if st.button(f"← {t('buttons.back')}"):
            navigate_to('predict')
        return
    
    car_data = st.session_state.car_details
    analysis = car_data.get('analysis', {})
    
    # تقدير السعر
    # تقدير السعر
    with st.spinner(t('messages.loading')):
        predictor = PricePredictor()
        
        # تحويل الحالة النصية إلى رقمية
        condition_map = {
            'ممتازة': 1.0, 'جيدة جداً': 0.9, 'جيدة': 0.8,
            'مقبولة': 0.6, 'سيئة': 0.4, 'سيئة جداً': 0.2
        }
        c_str = car_data.get('condition', 'جيدة')
        c_score = condition_map.get(c_str, 0.8)
        
        predict_data = {
            'car_type': car_data.get('car_type', 'سيدان'),
            'brand': car_data.get('brand', 'أخرى'),
            'condition_score': c_score,
            'mileage': car_data.get('mileage', 50000),
            'manufacture_year': car_data.get('manufacture_year', 2020),
            'fuel_type': car_data.get('fuel_type', 'بنزين'),
            'owners': car_data.get('previous_owners', 1),
            'tuv_months': car_data.get('tuv_months', 0),
            'maintenance': car_data.get('maintenance_history', False),
            'transmission': car_data.get('transmission', ''),
            'drivetrain': car_data.get('drivetrain', ''),
            'color': car_data.get('color', ''),
            'emissions_class': car_data.get('emissions_class', ''),
            'engine_cc': car_data.get('engine_cc', 0),
            'horsepower': car_data.get('horsepower', 0),
            'accident_history': car_data.get('accident_history', ''),
            'warranty': car_data.get('warranty', ''),
            'service_book': car_data.get('service_book', ''),
            'equipment': car_data.get('equipment', []),
        }
        
        estimated_price = predictor.predict_price(predict_data)
        min_p, max_p = predictor.get_price_range(estimated_price)
        price_range = {'min': min_p, 'max': max_p}
        
        st.session_state.prediction_data = {'estimated_price': estimated_price, 'price_range': price_range}
    
    # عرض النتيجة الرئيسية باستخدام التصميم الجديد
    # استخلاص الثقة من تحليل الذكاء الاصطناعي
    confidence_str = analysis.get('confidence_score', '90%').replace('%', '')
    try:
        confidence_pct = int(confidence_str)
    except:
        confidence_pct = 90
        
    confidence = 'عالية' if confidence_pct > 80 else 'متوسطة'
    
    # مكونات السعر (سنستخدم قيم افتراضية ومحسوبة للعرض)
    comp = {
        'base_price': estimated_price * 0.5, # قيمة افتراضية للعرض
        'condition': {'factor': 1.0, 'contribution': 0}, 
        'mileage': {'factor': 1.0, 'contribution': 0}, 
        'age': {'factor': 1.0, 'contribution': 0},
        'brand_factor': 1.0, # Note: using brand_factor (flat key) as expected by line 887
        'fuel_factor': 1.0,
        'owners_factor': 1.0,
        'tuv_factor': 1.0,
        'maintenance_factor': 1.0
    }
    
    # استدعاء الواجهة الموحدة
    get_results_page_html(
        estimated_price, 
        price_range, 
        confidence, 
        confidence_pct, 
        car_data, 
        comp
    )
    
    st.markdown("---")
    
    st.markdown("---")
    
    # أزرار الإجراءات
    st.subheader(f"📄 {t('admin.action_options')}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # التحقق إذا كان الأدمن - عرض خيار اختيار العميل
        if st.session_state.user.get('role') == 'admin':
            if not st.session_state.get('admin_save_mode'):
                if st.button("💾 حفظ التقدير", use_container_width=True):
                    st.session_state['admin_save_mode'] = True
                    st.rerun()
            
            if st.session_state.get('admin_save_mode'):
                st.markdown("""
                <div style="background: linear-gradient(135deg, #0E1117 0%, #161B22 100%); 
                            padding: 15px; border-radius: 10px; border: 2px solid #D4AF37; margin: 10px 0;">
                    <h4 style="color: #D4AF37; margin: 0;">👤 اختر العميل الحقيقي</h4>
                    <p style="color: #a0a0c0; font-size: 0.9rem; margin: 5px 0 0 0;">سيتم ربط هذا التقدير بالعميل المختار</p>
                </div>
                """, unsafe_allow_html=True)
                
                db = DatabaseManager()
                all_users = db.get_all_users()
                # استبعاد الأدمن من القائمة
                customers = [u for u in all_users if u.get('role') != 'admin']
                
                if customers:
                    customer_options = {f"{u.get('full_name') or u.get('username')} ({u.get('email')})": u for u in customers}
                    
                    selected_customer_key = st.selectbox(
                        t('admin.customer'),
                        options=list(customer_options.keys()),
                        key="admin_customer_select"
                    )
                    
                    selected_customer = customer_options.get(selected_customer_key)
                    
                    save_col1, save_col2 = st.columns(2)
                    with save_col1:
                        if st.button(f"✅ {t('admin.save_for_customer')}", use_container_width=True, type="primary"):
                            try:
                                car_image = st.session_state.get('uploaded_image')
                                # ربط الموظف/الآدمن الذي أجرى التسعير للعمولة
                                admin_emp = db.get_employee_by_user_id(st.session_state.user['id'])
                                emp_id = admin_emp['id'] if admin_emp else None
                                transaction_id = db.create_transaction(
                                    user_id=selected_customer['id'],  # ID العميل وليس الأدمن
                                    car_data=car_data,
                                    estimated_price=estimated_price,
                                    condition_analysis=analysis,
                                    car_image_bytes=car_image,
                                    employee_id=emp_id
                                )
                                
                                st.session_state.last_transaction_id = transaction_id
                                st.session_state['admin_save_mode'] = False
                                # حفظ بيانات العميل المختار لاستخدامها في إنشاء الفاتورة
                                st.session_state['selected_customer_for_invoice'] = selected_customer
                                st.success(f"✅ {t('admin.estimate_saved_for_customer')}: {selected_customer.get('full_name') or selected_customer.get('username')}")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ {t('admin.save_error')}: {e}")
                    
                    with save_col2:
                        if st.button(f"❌ {t('admin.cancel')}", use_container_width=True):
                            st.session_state['admin_save_mode'] = False
                            st.rerun()
                else:
                    st.warning(f"⚠️ {t('admin.no_customers')}")
                    if st.button(f"❌ {t('admin.cancel')}", use_container_width=True):
                        st.session_state['admin_save_mode'] = False
                        st.rerun()
        else:
            # المستخدم العادي - حفظ مباشر
            if st.button(f"💾 {t('admin.save_estimate')}", use_container_width=True):
                try:
                    db = DatabaseManager()
                    car_image = st.session_state.get('uploaded_image')
                    # ربط الموظف لاحتساب العمولة
                    user_emp = db.get_employee_by_user_id(st.session_state.user['id'])
                    emp_id = user_emp['id'] if user_emp else None
                    transaction_id = db.create_transaction(
                        user_id=st.session_state.user['id'],
                        car_data=car_data,
                        estimated_price=estimated_price,
                        condition_analysis=analysis,
                        car_image_bytes=car_image,
                        employee_id=emp_id
                    )
                    
                    st.session_state.last_transaction_id = transaction_id
                    st.success(f"✅ {t('admin.estimate_saved')}")
                except Exception as e:
                    st.error(f"❌ {t('admin.save_error')}: {e}")
    
    with col2:
        if st.button(f"💳 {t('admin.go_to_payment')}", use_container_width=True, type="primary"):
            # حفظ السعر للخطوة القادمة
            st.session_state.last_price = estimated_price
            
            # التحقق من توثيق الهوية قبل الانتقال للدفع
            user = st.session_state.user
            is_verified = bool(user.get('id_number') and user.get('nationality') and user.get('license_number'))
            
            if is_verified:
                navigate_to('checkout')
            else:
                st.warning(f"⚠️ {t('admin.verify_id_first')}")
                navigate_to('verify_identity')
    
    with col3:
        if st.button(f"📧 {t('invoices.send_email')}", use_container_width=True):
            try:
                # إنشاء الفاتورة أولاً إذا لم تكن موجودة
                if not st.session_state.get('invoice_path'):
                    generator = InvoiceGenerator()
                    transaction_data = {
                        'id': st.session_state.get('last_transaction_id', datetime.now().strftime('%Y%m%d%H%M%S')),
                        'estimated_price': prediction_result['estimated_price'],
                        **car_data
                    }
                    
                    # استخدام بيانات العميل المختار إذا كان الآدمن هو من أنشأ العقد
                    customer_for_invoice = st.session_state.get('selected_customer_for_invoice', st.session_state.user)
                    
                    invoice_path = generator.generate_car_invoice(
                        transaction_data,
                        customer_for_invoice  # استخدام بيانات العميل الصحيحة
                    )
                    st.session_state.invoice_path = invoice_path
                
                # إرسال البريد
                notifier = NotificationManager()
                
                # استخدام بيانات العميل المختار إذا كان الآدمن هو من أنشأ العقد
                customer_for_invoice = st.session_state.get('selected_customer_for_invoice', st.session_state.user)
                
                if not notifier.email_configured:
                    st.warning(f"⚠️ {t('admin.email_incomplete')}")
                else:
                    result = notifier.send_invoice_email(
                        recipient_email=customer_for_invoice['email'],  # بريد العميل الصحيح
                        invoice_path=st.session_state.invoice_path,
                        user_data=customer_for_invoice,  # بيانات العميل الصحيحة
                        transaction_data={
                            'estimated_price': prediction_result['estimated_price'],
                            **car_data
                        }
                    )
                    
                    if result['success']:
                        st.success(f"✅ {t('messages.success')}")
                    else:
                        st.error(f"❌ {result['message']}")
            except Exception as e:
                st.error(f"❌ {t('messages.error')}: {e}")
    
    st.markdown("---")
    
    # أزرار التنقل
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"🏎️ {t('results.new_evaluation')}", use_container_width=True):
            # مسح البيانات السابقة
            st.session_state.uploaded_image = None
            st.session_state.car_details = {}
            st.session_state.analysis_result = None
            st.session_state.prediction_data = None
            navigate_to('predict')
    
    with col2:
        if st.button(f"✏️ {t('buttons.edit')}", use_container_width=True, help=t('buttons.back')):
            navigate_to('predict')
            
    with col3:
        if st.button(f"🏠 {t('nav.home')}", type="secondary", use_container_width=True):
            navigate_to('home')


# ======================
# صفحة الفواتير
