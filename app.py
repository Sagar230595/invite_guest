"""Invito AI - Multipage Streamlit Application for Luxury Invitation Cards (No Sidebar)."""
import streamlit as st
from config.settings import APP_NAME, APP_TAGLINE, APP_ICON
from templates.template_data import TEMPLATES
from ui.styles import inject_custom_css

# 1. Page Configuration (Sidebar collapsed by default)
st.set_page_config(
    page_title=f"{APP_NAME} — {APP_TAGLINE}",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Inject Luxury Custom CSS (Removes sidebar completely)
inject_custom_css()

# 3. Initialize Shared Session State
def init_session_state():
    if "card_data" not in st.session_state:
        default_tpl = TEMPLATES[0]
        st.session_state.card_data = dict(default_tpl["defaults"])
        st.session_state.card_theme = dict(default_tpl["theme"])
        st.session_state.selected_template_id = default_tpl["id"]
        st.session_state.selected_template_name = default_tpl["name"]
        st.session_state.aspect_ratio = "Portrait (5:7 - Classic Stationery)"
        st.session_state.border_style = "Double Thin & Gold Foil Line"
        st.session_state.enable_qr = True
        st.session_state.user_photo = None
        st.session_state.uploaded_sample = None

init_session_state()

# 4. Define Multipage Pages (Position hidden, navigated via top luxury navbar)
page_home = st.Page("views/home.py", title="Studio Home", icon="🏠", default=True)
page_templates = st.Page("views/templates_view.py", title="Template Gallery", icon="🌟")
page_studio = st.Page("views/studio_view.py", title="Card Studio", icon="✏️")
page_ai = st.Page("views/ai_chat_view.py", title="AI Assistant", icon="🤖")
page_export = st.Page("views/export_view.py", title="Export & Share", icon="📥")

pg = st.navigation(
    [page_home, page_templates, page_studio, page_ai, page_export],
    position="hidden",
)

# 5. Run Active Page
pg.run()
