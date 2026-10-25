"""Studio Home & Executive Launchpad view for Invito AI with 100% WYSIWYG card export."""
import streamlit as st
from config.settings import DEFAULT_MODEL
from templates.template_data import TEMPLATES
from templates.card_renderer import render_invitation_html, pil_to_base64_uri
from core.qr_generator import generate_qr_code
from core.ai_service import is_api_key_configured
from ui.components import render_top_navbar


def render_home_page():
    """Renders the attractive Studio Home dashboard."""
    # Top Luxury Navigation Bar
    render_top_navbar("🏠 Studio Home")

    # 1. Hero Banner
    ai_status_text = "AI Ready" if is_api_key_configured() else "Key in .env needed"
    st.markdown(f"""
    <div class="hero-banner">
        <h1 class="hero-title">Create Breathtaking Invitations with AI</h1>
        <p class="hero-subtitle">
            Welcome to <strong>Invito AI Studio</strong> — craft bespoke, luxury invitations for weddings,
            engagements, milestone birthdays, corporate galas, baby showers, and festive celebrations. Choose from world-class designer templates,
            co-design with <strong>Gemini 3.8 Flash</strong>, or upload reference photos and PDFs to recreate any style in seconds.
        </p>
        <div class="hero-badge-row">
            <span class="hero-badge">⚡ Powered by {DEFAULT_MODEL}</span>
            <span class="hero-badge">👑 9+ Curated Luxury Templates</span>
            <span class="hero-badge">📱 Smart QR Code Maps & WhatsApp RSVP</span>
            <span class="hero-badge">🎯 100% WYSIWYG 300 DPI Print PDF & PNG</span>
            <span class="hero-badge">● {ai_status_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. How It Works: 3-Step Creation Workflow
    st.markdown("### 🚀 How Invito Works")
    step_col1, step_col2, step_col3 = st.columns(3, gap="medium")
    with step_col1:
        st.markdown("""
        <div class="glass-panel" style="height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">1️⃣</div>
            <h4 style="color: #D4AF37; margin: 0 0 6px 0; font-family: 'Cinzel', serif;">Pick or Upload</h4>
            <p style="color: #94A3B8; font-size: 0.85rem; line-height: 1.5; margin: 0;">
                Choose from 9 curated luxury templates, start from scratch, or upload reference invitation photos & PDFs for the AI to inspect.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with step_col2:
        st.markdown(f"""
        <div class="glass-panel" style="height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">2️⃣</div>
            <h4 style="color: #D4AF37; margin: 0 0 6px 0; font-family: 'Cinzel', serif;">AI Co-Designer</h4>
            <p style="color: #94A3B8; font-size: 0.85rem; line-height: 1.5; margin: 0;">
                Tell <strong>Gemini 3.8 Flash</strong> about your event. Get poetic rhymes, royal blessings, or formal copy with 1-click import to your card canvas.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with step_col3:
        st.markdown("""
        <div class="glass-panel" style="height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">3️⃣</div>
            <h4 style="color: #D4AF37; margin: 0 0 6px 0; font-family: 'Cinzel', serif;">100% WYSIWYG Export</h4>
            <p style="color: #94A3B8; font-size: 0.85rem; line-height: 1.5; margin: 0;">
                Download pixel-perfect 300 DPI retina PNGs and print-ready PDFs matching your live preview down to the exact pixel, with zero distortion.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # 3. Three Interactive Quick Action Cards
    st.markdown("### ⚡ Quick Navigation")
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.markdown("""
        <div class="hub-action-card">
            <div>
                <div class="hub-card-icon">🌟</div>
                <h3 class="hub-card-title">Designer Templates</h3>
                <p class="hub-card-desc">
                    Explore curated stationery for Royal Weddings, Rose Gold Engagements, Botanical Galas, and Starlight Birthdays.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore All Templates →", key="home_btn_templates", type="primary", use_container_width=True):
            st.switch_page("views/templates_view.py")

    with c2:
        st.markdown(f"""
        <div class="hub-action-card">
            <div>
                <div class="hub-card-icon">🤖</div>
                <h3 class="hub-card-title">Gemini AI Assistant</h3>
                <p class="hub-card-desc">
                    Chat with your specialized invitation copywriter. Upload sample photos or PDF cards to replicate design vibes with 1-click import.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch AI Chatbot →", key="home_btn_ai", type="primary", use_container_width=True):
            st.switch_page("views/ai_chat_view.py")

    with c3:
        st.markdown("""
        <div class="hub-action-card">
            <div>
                <div class="hub-card-icon">✏️</div>
                <h3 class="hub-card-title">Card Studio</h3>
                <p class="hub-card-desc">
                    Fine-tune names, dates, venue, RSVP, custom photos, Google Maps QR codes, Google Fonts typography, and color schemes.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Card Studio →", key="home_btn_studio", type="primary", use_container_width=True):
            st.switch_page("views/studio_view.py")

    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

    # 4. Active Canvas Spotlight
    card_data = st.session_state.card_data
    card_theme = st.session_state.card_theme
    active_name = st.session_state.get("selected_template_name", "Custom Design")

    st.markdown("### 🎨 Active Canvas Spotlight")
    st.markdown(f"Currently styling: **{active_name}** — your changes synchronize in real-time across all studio pages.")

    col_preview, col_info = st.columns([1.15, 0.85], gap="large")

    with col_preview:
        # Generate QR code
        qr_uri = None
        if st.session_state.get("enable_qr", True) and card_data.get("qr_link"):
            _, qr_uri = generate_qr_code(
                data=card_data["qr_link"],
                fill_color=card_theme.get("bg_color", "#1A1A1A"),
            )
        photo_uri = pil_to_base64_uri(st.session_state.get("user_photo"))

        safe_filename = "".join([c if c.isalnum() else "_" for c in card_data.get("title", "invitation")]).strip("_")

        mini_html = render_invitation_html(
            card_data=card_data,
            theme=card_theme,
            aspect_ratio=st.session_state.get("aspect_ratio", "Portrait (5:7 - Classic Stationery)"),
            qr_data_uri=qr_uri,
            photo_data_uri=photo_uri,
            border_style_choice=st.session_state.get("border_style", "Double Thin & Gold Foil Line"),
            include_wrapper=True,
            show_export_buttons=True,
            card_filename=f"invitation_{safe_filename}",
        )
        st.components.v1.html(mini_html, height=730, scrolling=True)

    with col_info:
        st.markdown(f"""
        <div class="glass-panel">
            <h4 style="color: #D4AF37; margin-top: 0; font-family: 'Cinzel', serif; font-size: 1.25rem;">
                💌 {card_data.get('title', 'Celebration')}
            </h4>
            <div style="font-size: 0.88rem; color: #CBD5E1; margin-bottom: 14px;">
                <strong>Occasion:</strong> {card_data.get('event_type', 'Celebration')}
            </div>
            <div style="font-size: 0.84rem; color: #94A3B8; line-height: 1.6; margin-bottom: 16px;">
                📅 <strong>Date:</strong> {card_data.get('date', 'TBD')}<br>
                ⏰ <strong>Time:</strong> {card_data.get('time', 'TBD')}<br>
                📍 <strong>Venue:</strong> {card_data.get('venue', 'TBD')}<br>
                👔 <strong>Attire:</strong> {card_data.get('dress_code', 'Formal / Festive')}<br>
                📱 <strong>QR Link:</strong> {card_data.get('qr_link', 'None')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### ⚡ Quick Actions")
        c_edit, c_exp = st.columns(2)
        with c_edit:
            if st.button("✏️ Customize Details", key="spotlight_edit", use_container_width=True):
                st.switch_page("views/studio_view.py")
        with c_exp:
            if st.button("📥 Full Export Studio", key="spotlight_export", type="primary", use_container_width=True):
                st.switch_page("views/export_view.py")

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-panel" style="padding: 14px 16px;">
            <span style="color: #D4AF37; font-weight: 600; font-size: 0.85rem;">🎯 100% WYSIWYG Guarantee</span>
            <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 4px; line-height: 1.45;">
                Click the gold download buttons directly above the card to download your design with 100% exact fidelity.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 5. Featured Trending Templates Carousel
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    st.markdown("### 🔥 Featured Trending Templates")
    st.markdown("Popular stationery designs ready to use in 1 click:")

    featured_cols = st.columns(3, gap="medium")
    for i, tpl in enumerate(TEMPLATES[:3]):
        with featured_cols[i]:
            theme = tpl["theme"]
            st.markdown(f"""
            <div class="template-card">
                <div>
                    <span class="template-badge">{tpl['badge']}</span>
                    <h4 style="margin: 6px 0 2px 0; color: #FFFDF7; font-family: 'Cinzel', serif;">{tpl['name']}</h4>
                    <span style="font-size: 0.74rem; color: #A0AEC0;">{tpl['category']}</span>
                    <p style="color: #94A3B8; font-size: 0.82rem; margin-top: 8px; line-height: 1.4;">{tpl['description']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"✨ Select '{tpl['name']}'", key=f"feat_btn_{tpl['id']}", use_container_width=True):
                st.session_state.card_data = dict(tpl["defaults"])
                st.session_state.card_theme = dict(tpl["theme"])
                st.session_state.selected_template_id = tpl["id"]
                st.session_state.selected_template_name = tpl["name"]
                st.toast(f"Applied '{tpl['name']}'!", icon="✨")
                st.rerun()


# Essential module-level entrypoint
if __name__ == "__main__" or True:
    render_home_page()
