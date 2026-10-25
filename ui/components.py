"""Reusable UI components for Invito AI, including luxury top navigation."""
import streamlit as st
from config.settings import APP_NAME, APP_TAGLINE, DEFAULT_MODEL
from core.ai_service import is_api_key_configured

PAGE_ROUTES = {
    "🏠 Studio Home": "views/home.py",
    "🌟 Template Gallery": "views/templates_view.py",
    "✏️ Card Studio": "views/studio_view.py",
    "🤖 AI Assistant": "views/ai_chat_view.py",
    "📥 Export & Share": "views/export_view.py",
}


def render_top_navbar(current_label: str = "🏠 Studio Home"):
    """Renders the luxury top navigation bar without any sidebar."""
    ai_status = (
        '<span style="color: #4ade80; font-size: 0.8rem; font-weight: 600;">● AI Active</span>'
        if is_api_key_configured()
        else '<span style="color: #fbbf24; font-size: 0.8rem; font-weight: 600;">○ Key in .env needed</span>'
    )

    active_title = st.session_state.card_data.get("title", "Aarav & Meera")
    active_tpl = st.session_state.get("selected_template_name", "Royal Rajputana")

    # Brand & Status Header Row
    top_header_html = f"""
    <div class="invito-top-navbar">
        <div style="display: flex; align-items: center; gap: 14px; flex-wrap: wrap;">
            <div>
                <span class="invito-brand-logo">💌 {APP_NAME}</span>
                <span class="invito-brand-tagline">Haute Stationery & AI Co-Design</span>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
            <div class="invito-status-pill">
                <span>Active Card:</span> <strong style="color: #FFFDF7;">{active_title}</strong>
                <span style="color: #D4AF37; opacity: 0.85;">({active_tpl})</span>
            </div>
            <div class="invito-status-pill">
                <span>⚡ Model:</span> <strong>{DEFAULT_MODEL}</strong>
            </div>
            <div class="invito-status-pill">
                {ai_status}
            </div>
        </div>
    </div>
    """
    st.markdown(top_header_html, unsafe_allow_html=True)

    # Multipage Navigation Pill Bar
    nav_labels = list(PAGE_ROUTES.keys())
    selected_page = st.segmented_control(
        "Multipage Navigation",
        options=nav_labels,
        default=current_label,
        key=f"nav_selector_{current_label.replace(' ', '_')}",
        label_visibility="collapsed",
    )

    if selected_page and selected_page != current_label:
        st.switch_page(PAGE_ROUTES[selected_page])

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
