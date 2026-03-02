"""
chatbot_component.py - Customer AI Chatbot
SmartCar AI-Dealer
"""

import streamlit as st
from utils.i18n import t


def render_chatbot():
    """Render chatbot in sidebar"""
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    if 'chat_open' not in st.session_state:
        st.session_state.chat_open = False

    with st.sidebar:
        if st.button(f"💬 {t('chat.title', 'AI Assistant')}", use_container_width=True,
                    type="primary" if st.session_state.chat_open else "secondary"):
            st.session_state.chat_open = not st.session_state.chat_open
            st.rerun()

    if not st.session_state.chat_open:
        return

    with st.container():
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1a2e, #16213e);
                    border: 1px solid #D4AF3755; border-radius: 15px;
                    padding: 20px; margin: 10px 0;">
            <h3 style="color: #D4AF37; text-align: center;">💬 {t('chat.title', 'AI Assistant')}</h3>
            <p style="color: #a0a0c0; text-align: center; font-size: 0.85em;">
                {t('chat.subtitle', 'Ask me about cars, prices, or services!')}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Quick Questions
        st.markdown(f"**{t('chat.quick_questions', 'Quick Questions')}:**")
        qc1, qc2 = st.columns(2)
        with qc1:
            if st.button(f"💰 {t('chat.q_price', 'Pricing?')}", use_container_width=True, key="q1"):
                _quick("pricing")
            if st.button(f"📋 {t('chat.q_inst', 'Installments?')}", use_container_width=True, key="q2"):
                _quick("installment")
        with qc2:
            if st.button(f"📷 {t('chat.q_ai', 'AI Analysis?')}", use_container_width=True, key="q3"):
                _quick("ai")
            if st.button(f"📞 {t('chat.q_contact', 'Contact?')}", use_container_width=True, key="q4"):
                _quick("contact")

        st.markdown("---")

        # Messages
        chat_box = st.container(height=300)
        with chat_box:
            for msg in st.session_state.chat_messages:
                if msg['role'] == 'user':
                    st.chat_message("user").write(msg['content'])
                else:
                    st.chat_message("assistant", avatar="🏎️").write(msg['content'])

        # Input
        user_input = st.chat_input(t('chat.placeholder', 'Type your question...'), key="chat_input")
        if user_input:
            st.session_state.chat_messages.append({'role': 'user', 'content': user_input})
            response = _ai_response(user_input)
            st.session_state.chat_messages.append({'role': 'assistant', 'content': response})
            st.rerun()


def _quick(topic):
    """Pre-built quick answers"""
    qa = {
        "pricing": ("How is pricing done?",
            "Our AI analyzes 20+ factors:\n• Brand & Model\n• Year & Mileage\n"
            "• Condition (1-10)\n• TÜV & Equipment\n• Market trends\n\nUpload a photo for instant estimate! 📷"),
        "installment": ("Installment plans?",
            "Flexible plans available:\n• Down payment from 20%\n• 6-48 monthly installments\n"
            "• Competitive rates\n• Online tracking\n• QR-verified invoices 💰"),
        "ai": ("How does AI analysis work?",
            "1. 📷 Upload car photos\n2. 🤖 AI identifies brand, model, color\n"
            "3. 🔍 Condition assessment\n4. 💰 Price estimate\n5. 📄 Professional report\n\nResults in seconds! 🚀"),
        "contact": ("Contact info?",
            "📧 support@smartcar-ai.com\n📞 +49 123 456 789\n"
            "🕐 Mon-Sat 9:00-18:00\n📍 Visit our showroom\n\nHappy to help! 😊")
    }
    if topic in qa:
        q, a = qa[topic]
        st.session_state.chat_messages.append({'role': 'user', 'content': q})
        st.session_state.chat_messages.append({'role': 'assistant', 'content': a})
        st.rerun()


def _ai_response(message):
    """Get response from Groq AI"""
    try:
        from groq_base import GroqBaseClient
        client = GroqBaseClient()

        system = ("You are a helpful AI assistant for SmartCar AI-Dealer, a car dealership. "
                  "Help with: pricing, installments, services, car buying advice. "
                  "Be friendly, professional, concise. Answer in the user's language. "
                  "Keep responses under 150 words.")

        messages = [{"role": "system", "content": system}]
        for msg in st.session_state.chat_messages[-6:]:
            messages.append({"role": msg['role'], "content": msg['content']})
        messages.append({"role": "user", "content": message})

        resp = client.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )
        return resp.choices[0].message.content

    except Exception:
        return t('chat.error', "Sorry, I couldn't process your request. Please contact support@smartcar-ai.com 📧")
