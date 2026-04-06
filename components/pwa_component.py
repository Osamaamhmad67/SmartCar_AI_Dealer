"""
pwa_component.py - مكون PWA لتحويل التطبيق إلى تطبيق موبايل
يضيف manifest, service worker, وزر التثبيت
"""

import streamlit as st
import streamlit.components.v1 as components


def inject_pwa():
    """حقن أكواد PWA في التطبيق (يُستدعى مرة واحدة في main)"""
    
    pwa_html = """
    <script>
    // ===== PWA: Register Service Worker =====
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/app/static/sw.js', { scope: '/' })
            .then(reg => console.log('[PWA] SW registered:', reg.scope))
            .catch(err => console.log('[PWA] SW failed:', err));
    }

    // ===== PWA: Add manifest link =====
    if (!document.querySelector('link[rel="manifest"]')) {
        const link = document.createElement('link');
        link.rel = 'manifest';
        link.href = '/app/static/manifest.json';
        document.head.appendChild(link);
    }

    // ===== PWA: Add meta tags for mobile =====
    const metaTags = [
        {name: 'theme-color', content: '#D4AF37'},
        {name: 'apple-mobile-web-app-capable', content: 'yes'},
        {name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent'},
        {name: 'apple-mobile-web-app-title', content: 'SmartCar'},
        {name: 'mobile-web-app-capable', content: 'yes'},
        {name: 'viewport', content: 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no'}
    ];
    
    metaTags.forEach(({name, content}) => {
        if (!document.querySelector(`meta[name="${name}"]`)) {
            const meta = document.createElement('meta');
            meta.name = name;
            meta.content = content;
            document.head.appendChild(meta);
        }
    });

    // Apple touch icon
    if (!document.querySelector('link[rel="apple-touch-icon"]')) {
        const icon = document.createElement('link');
        icon.rel = 'apple-touch-icon';
        icon.href = '/app/static/icons/icon-192.png';
        document.head.appendChild(icon);
    }
    </script>
    """
    
    # حقن بدون إطار مرئي
    st.markdown(pwa_html, unsafe_allow_html=True)


def render_install_button():
    """زر تثبيت التطبيق (يظهر فقط إذا كان PWA متاحاً)"""
    
    install_html = """
    <div id="pwa-install-container" style="display:none; position:fixed; bottom:20px; right:20px; z-index:9999;">
        <button id="pwa-install-btn" onclick="installPWA()" style="
            background: linear-gradient(135deg, #D4AF37, #B8860B);
            color: #0E1117;
            border: none;
            padding: 12px 24px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 700;
            font-family: 'Cairo', sans-serif;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(212,175,55,0.4);
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
        ">
            📱 تثبيت التطبيق
        </button>
    </div>
    
    <script>
    let deferredPrompt = null;
    
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        const container = document.getElementById('pwa-install-container');
        if (container) container.style.display = 'block';
    });
    
    function installPWA() {
        if (!deferredPrompt) return;
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then((result) => {
            if (result.outcome === 'accepted') {
                console.log('[PWA] App installed!');
            }
            deferredPrompt = null;
            const container = document.getElementById('pwa-install-container');
            if (container) container.style.display = 'none';
        });
    }
    
    // Hide if already installed
    window.addEventListener('appinstalled', () => {
        const container = document.getElementById('pwa-install-container');
        if (container) container.style.display = 'none';
        console.log('[PWA] Already installed');
    });
    </script>
    """
    
    components.html(install_html, height=0)
