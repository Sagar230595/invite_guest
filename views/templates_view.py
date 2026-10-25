"""Template Gallery Page view for Invito AI."""
import streamlit as st
from templates.template_data import TEMPLATES, get_all_categories
from templates.card_renderer import render_invitation_html
from ui.components import render_top_navbar


def apply_template_to_session(template: dict):
    """Applies the selected template to the user's active session state."""
    st.session_state.card_data = dict(template["defaults"])
    st.session_state.card_theme = dict(template["theme"])
    st.session_state.selected_template_id = template["id"]
    st.session_state.selected_template_name = template["name"]
    st.toast(f"🎉 Applied '{template['name']}'! Ready to customize in the Studio.", icon="✨")


def render_templates_page():
    """Renders the comprehensive Template Showcase page."""
    render_top_navbar("🌟 Template Gallery")
    st.markdown("## 🌟 Curated Designer Templates")
    st.markdown(
        "Browse our collection of hand-crafted invitation card templates. "
        "Selecting any template immediately populates the canvas, which you can customize in the **Card Studio**."
    )

    # Category Filter
    categories = get_all_categories()
    selected_cat = st.segmented_control(
        "Filter by Event Type:",
        options=categories,
        default="All Categories",
        label_visibility="collapsed",
    ) or "All Categories"

    filtered_templates = [
        t for t in TEMPLATES
        if selected_cat == "All Categories" or t["category"] == selected_cat
    ]

    st.markdown(f"<div style='font-size: 0.82rem; color: #94A3B8; margin-bottom: 16px;'>Showing {len(filtered_templates)} template(s)</div>", unsafe_allow_html=True)

    # 2-Column Grid
    cols = st.columns(2, gap="large")
    for idx, template in enumerate(filtered_templates):
        col = cols[idx % 2]
        theme = template["theme"]
        with col:
            # Color swatches
            swatch_html = f"""
            <div class="color-swatch-bar">
                <span style="font-size: 0.72rem; color: #94A3B8; margin-right: 4px;">Palette:</span>
                <div class="color-swatch-dot" style="background-color: {theme.get('bg_color', '#121212')};" title="Background"></div>
                <div class="color-swatch-dot" style="background-color: {theme.get('primary_color', '#D4AF37')};" title="Accent Gold"></div>
                <div class="color-swatch-dot" style="background-color: {theme.get('secondary_color', '#E5D4B8')};" title="Secondary"></div>
                <div class="color-swatch-dot" style="background-color: {theme.get('text_color', '#FFFFFF')};" title="Text"></div>
            </div>
            """

            st.markdown(f"""
            <div class="template-card">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <span class="template-badge">{template['badge']}</span>
                        <span style="font-size: 0.76rem; color: #A0AEC0;">{template['category']}</span>
                    </div>
                    <h3 style="margin: 8px 0 4px 0; color: #FFFDF7; font-size: 1.3rem; font-family: 'Cinzel', serif;">{template['name']}</h3>
                    <p style="color: #94A3B8; font-size: 0.86rem; margin-bottom: 6px; line-height: 1.45;">{template['description']}</p>
                    {swatch_html}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Miniature visual preview
            mini_html = render_invitation_html(
                card_data=template["defaults"],
                theme=template["theme"],
                aspect_ratio="Portrait (5:7 - Classic Stationery)",
                border_style_choice="Double Thin & Gold Foil Line",
                include_wrapper=True,
            )
            with st.expander(f"👁️ Preview '{template['name']}' Live Card", expanded=(idx < 2)):
                st.components.v1.html(mini_html, height=520, scrolling=True)

            # Use template action
            c_use, c_goto = st.columns([1.2, 0.8])
            with c_use:
                if st.button(f"✨ Select '{template['name']}'", key=f"btn_use_{template['id']}", type="primary", use_container_width=True):
                    apply_template_to_session(template)
                    st.rerun()
            with c_goto:
                if st.session_state.get("selected_template_id") == template["id"]:
                    if st.button("Open Studio →", key=f"btn_goto_{template['id']}", use_container_width=True):
                        st.switch_page("views/studio_view.py")

            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)


if __name__ == "__main__" or True:
    render_templates_page()
