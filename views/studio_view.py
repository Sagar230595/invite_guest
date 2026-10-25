"""Card Studio & Customizer Page view for Invito AI."""
import streamlit as st
from PIL import Image
from config.settings import ASPECT_RATIOS, BORDER_STYLES, FONT_OPTIONS
from core.qr_generator import generate_qr_code
from templates.card_renderer import render_invitation_html, pil_to_base64_uri
from ui.components import render_top_navbar


def render_studio_page():
    """Renders the comprehensive Card Studio editor with real-time live preview."""
    render_top_navbar("✏️ Card Studio")
    active_name = st.session_state.get("selected_template_name", "Custom Design")
    st.markdown("## ✏️ Invitation Card Studio")
    st.markdown(
        f"Active Canvas: **{active_name}** — Every edit you make updates the preview immediately. "
        "When finished, proceed to **Export & Share** for high-res downloads."
    )

    card_data = st.session_state.card_data
    card_theme = st.session_state.card_theme

    col_form, col_view = st.columns([1.15, 0.85], gap="large")

    with col_form:
        # Section 1: Core Event Content
        with st.expander("📝 1. Event Core Information", expanded=True):
            card_data["title"] = st.text_input(
                "Main Names / Honoree / Event Title *",
                value=card_data.get("title", ""),
                placeholder="e.g. Aarav & Meera / Liam is Turning 30!",
                help="The most prominent headline text on your invitation.",
            )

            card_data["event_type"] = st.text_input(
                "Event Subtitle / Occasion",
                value=card_data.get("event_type", ""),
                placeholder="e.g. Wedding Ceremony & Reception / Annual Awards Gala",
            )

            card_data["headline"] = st.text_area(
                "Opening Blessing / Headline Greeting",
                value=card_data.get("headline", ""),
                height=80,
                placeholder="e.g. Together with their families / You are warmly invited to celebrate...",
            )

            card_data["host_names"] = st.text_input(
                "Host(s) / Presented By",
                value=card_data.get("host_names", ""),
                placeholder="e.g. Cordially invited by Mr. & Mrs. Sharma / Presented by Apex Group",
            )

        # Section 2: Date, Time & Venue
        with st.expander("📍 2. Date, Time & Venue Details", expanded=True):
            c_date, c_time = st.columns(2)
            with c_date:
                card_data["date"] = st.text_input(
                    "Event Date *",
                    value=card_data.get("date", ""),
                    placeholder="e.g. Saturday, December 18, 2026",
                )
            with c_time:
                card_data["time"] = st.text_input(
                    "Event Time",
                    value=card_data.get("time", ""),
                    placeholder="e.g. 6:30 PM Onwards",
                )

            card_data["venue"] = st.text_area(
                "Venue Name & Full Address *",
                value=card_data.get("venue", ""),
                height=80,
                placeholder="e.g. The Grand Palace Ballroom, 100 Marina Way, San Francisco, CA",
            )

        # Section 3: RSVP, Attire & Notes
        with st.expander("💌 3. RSVP, Dress Code & Special Notes", expanded=False):
            c_rsvp, c_dress = st.columns(2)
            with c_rsvp:
                card_data["rsvp"] = st.text_input(
                    "RSVP Contact Details",
                    value=card_data.get("rsvp", ""),
                    placeholder="e.g. RSVP to Rahul: +91 98765 43210 by Nov 1st",
                )
            with c_dress:
                card_data["dress_code"] = st.text_input(
                    "Dress Code / Attire",
                    value=card_data.get("dress_code", ""),
                    placeholder="e.g. Black Tie / Festive Indian / Garden Chic",
                )

            card_data["special_note"] = st.text_area(
                "Special Message / Gift Note / Instructions",
                value=card_data.get("special_note", ""),
                height=80,
                placeholder="e.g. No boxed gifts please. Complimentary valet parking at North Gate.",
            )

        # Section 4: Dynamic QR Code
        with st.expander("📱 4. Interactive QR Code (Google Maps or WhatsApp)", expanded=False):
            enable_qr = st.checkbox("Include QR Code on Card", value=st.session_state.get("enable_qr", True))
            st.session_state.enable_qr = enable_qr

            if enable_qr:
                qr_link = st.text_input(
                    "QR Code Destination Link (Google Maps location or RSVP WhatsApp link)",
                    value=card_data.get("qr_link", "https://maps.google.com"),
                    help="Guests scan this code with their smartphone camera to open Google Maps or message you on WhatsApp!",
                )
                card_data["qr_link"] = qr_link

        # Section 5: Photo / Emblem / Monogram
        with st.expander("📷 5. Optional Photo or Monogram Emblem", expanded=False):
            uploaded_photo = st.file_uploader(
                "Upload Honoree Photo, Couple Picture, or Logo",
                type=["png", "jpg", "jpeg", "webp"],
                key="studio_photo_uploader",
                help="Uploaded image will be gracefully centered in an elegant circular gold-bordered frame at the top of your card.",
            )
            if uploaded_photo:
                try:
                    st.session_state.user_photo = Image.open(uploaded_photo).convert("RGB")
                    st.success("✅ Photo loaded successfully!")
                except Exception as e:
                    st.error(f"Error loading image: {e}")
            elif st.session_state.get("user_photo") and st.button("Remove Active Photo", key="btn_remove_photo"):
                st.session_state.user_photo = None
                st.rerun()

        # Section 6: Visual Styling & Google Fonts
        with st.expander("🎨 6. Card Styling, Dimensions & Colors", expanded=False):
            aspect_choice = st.selectbox(
                "Card Format / Aspect Ratio:",
                options=list(ASPECT_RATIOS.keys()),
                index=0,
                key="studio_aspect_ratio_select",
            )
            st.session_state.aspect_ratio = aspect_choice

            border_choice = st.selectbox(
                "Border & Frame Style:",
                options=BORDER_STYLES,
                index=0,
                key="studio_border_style_select",
            )
            st.session_state.border_style = border_choice

            c_c1, c_c2, c_c3 = st.columns(3)
            with c_c1:
                bg_col = st.color_picker(
                    "Background Color",
                    value=card_theme.get("bg_color", "#4A0E17"),
                    key="studio_bg_picker",
                )
                card_theme["bg_color"] = bg_col
                card_theme["card_bg_gradient"] = f"linear-gradient(145deg, {bg_col} 0%, #1A1A1A 100%)"
            with c_c2:
                primary_col = st.color_picker(
                    "Gold / Primary Accent",
                    value=card_theme.get("primary_color", "#D4AF37"),
                    key="studio_primary_picker",
                )
                card_theme["primary_color"] = primary_col
                card_theme["border_color"] = primary_col
            with c_c3:
                text_col = st.color_picker(
                    "Text Color",
                    value=card_theme.get("text_color", "#FFFDF7"),
                    key="studio_text_picker",
                )
                card_theme["text_color"] = text_col

            title_font_key = st.selectbox(
                "Main Title Typography (Google Fonts):",
                options=list(FONT_OPTIONS.keys()),
                index=0,
                key="studio_font_select",
            )
            card_theme["font_family_title"] = FONT_OPTIONS[title_font_key]

    with col_view:
        st.markdown("#### 👁️ Real-Time Live Preview")

        # Compute QR Code if enabled
        qr_uri = None
        if st.session_state.get("enable_qr", True) and card_data.get("qr_link"):
            _, qr_uri = generate_qr_code(
                data=card_data["qr_link"],
                fill_color=card_theme.get("bg_color", "#1A1A1A"),
            )

        # Photo URI
        photo_uri = pil_to_base64_uri(st.session_state.get("user_photo"))

        # Render HTML Card
        card_html = render_invitation_html(
            card_data=card_data,
            theme=card_theme,
            aspect_ratio=st.session_state.get("aspect_ratio", "Portrait (5:7 - Classic Stationery)"),
            qr_data_uri=qr_uri,
            photo_data_uri=photo_uri,
            border_style_choice=st.session_state.get("border_style", "Double Thin & Gold Foil Line"),
            include_wrapper=True,
        )

        st.components.v1.html(card_html, height=750, scrolling=True)

        # Quick Links
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        c_nav1, c_nav2 = st.columns(2)
        with c_nav1:
            if st.button("🤖 Need AI Wording?", use_container_width=True):
                st.switch_page("views/ai_chat_view.py")
        with c_nav2:
            if st.button("📥 Ready to Export →", type="primary", use_container_width=True):
                st.switch_page("views/export_view.py")


if __name__ == "__main__" or True:
    render_studio_page()
