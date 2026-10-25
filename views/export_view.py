"""Export & Share Studio Page view for Invito AI with 100% WYSIWYG fidelity only."""
import streamlit as st
from core.qr_generator import generate_qr_code
from templates.card_renderer import render_invitation_html, pil_to_base64_uri
from ui.components import render_top_navbar


def render_export_page():
    """Renders the Export & Sharing studio exclusively with 100% WYSIWYG downloads."""
    render_top_navbar("📥 Export & Share")
    st.markdown("## 📥 Export & Share Studio")
    st.markdown(
        "Download your finalized invitation card with **100% WYSIWYG (What You See Is What You Get) accuracy** "
        "matching your live preview."
    )

    card_data = st.session_state.card_data
    card_theme = st.session_state.card_theme
    aspect = st.session_state.get("aspect_ratio", "Portrait (5:7 - Classic Stationery)")
    border_style = st.session_state.get("border_style", "Double Thin & Gold Foil Line")

    # Generate QR & photo components
    qr_uri = None
    if st.session_state.get("enable_qr", True) and card_data.get("qr_link"):
        _, qr_uri = generate_qr_code(
            data=card_data["qr_link"],
            fill_color=card_theme.get("bg_color", "#1A1A1A"),
        )

    user_photo = st.session_state.get("user_photo")
    photo_uri = pil_to_base64_uri(user_photo)

    safe_filename = "".join([c if c.isalnum() else "_" for c in card_data.get("title", "invitation")]).strip("_")

    col_l, col_center, col_r = st.columns([0.15, 0.7, 0.15])

    with col_center:
        st.markdown("#### 🌟 100% WYSIWYG Print & Digital Card")
        st.markdown(
            "<span style='font-size: 0.88rem; color: #94A3B8;'>Click the buttons below to download the exact card rendered on your screen (with real Google Fonts & Emojis):</span>",
            unsafe_allow_html=True,
        )

        html_code = render_invitation_html(
            card_data=card_data,
            theme=card_theme,
            aspect_ratio=aspect,
            qr_data_uri=qr_uri,
            photo_data_uri=photo_uri,
            border_style_choice=border_style,
            include_wrapper=True,
            show_export_buttons=True,
            card_filename=f"invitation_{safe_filename}",
        )
        st.components.v1.html(html_code, height=900, scrolling=True)


if __name__ == "__main__" or True:
    render_export_page()
