"""Custom CSS and styling system for the Invito AI multipage application without a sidebar."""
import streamlit as st


def inject_custom_css():
    """Injects high-end luxury styling and complete sidebar removal into the Streamlit app."""
    custom_css = """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Cinzel:wght@600;700;800;900&family=Marcellus&display=swap');

    :root {
        --primary-gold: #D4AF37;
        --secondary-gold: #F3E5AB;
        --dark-gold: #997819;
        --dark-bg: #0B0E14;
        --card-bg: rgba(20, 24, 36, 0.72);
        --card-hover-bg: rgba(28, 34, 52, 0.88);
        --border-gold: rgba(212, 175, 55, 0.28);
        --border-gold-bright: rgba(212, 175, 55, 0.65);
        --text-light: #F8F9FA;
        --text-muted: #94A3B8;
        --accent-glow: 0 8px 32px 0 rgba(212, 175, 55, 0.16);
    }

    /* 🚫 COMPLETELY REMOVE SIDEBAR AND ITS TOGGLE BUTTONS */
    [data-testid="stSidebar"],
    [data-testid="collapsedControl"],
    section[data-testid="stSidebar"],
    button[data-testid="stSidebarCollapseButton"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Main Container & Full-Width Background */
    .stApp {
        background: radial-gradient(ellipse at 15% 5%, #181d2f 0%, #0c0f17 55%, #07090e 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: var(--text-light);
    }

    .stMainBlockContainer {
        max-width: 1350px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* Top Brand & Status Navigation Bar */
    .invito-top-navbar {
        background: linear-gradient(135deg, rgba(28, 22, 38, 0.85) 0%, rgba(14, 17, 26, 0.95) 100%);
        border: 1px solid var(--border-gold);
        border-radius: 18px;
        padding: 18px 26px;
        margin-bottom: 12px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), var(--accent-glow);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 14px;
        backdrop-filter: blur(16px);
    }

    .invito-brand-logo {
        font-family: 'Cinzel', serif;
        font-size: 1.85rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFDF7 0%, #D4AF37 50%, #F3E5AB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1.2px;
        margin-right: 12px;
    }

    .invito-brand-tagline {
        color: #94A3B8;
        font-size: 0.82rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        border-left: 1px solid rgba(212, 175, 55, 0.3);
        padding-left: 12px;
    }

    .invito-status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        background: rgba(212, 175, 55, 0.08);
        border: 1px solid var(--border-gold);
        border-radius: 20px;
        color: var(--primary-gold);
        font-size: 0.78rem;
        letter-spacing: 0.4px;
    }

    /* Luxury Segmented Control Multipage Switcher */
    [data-testid="stSegmentedControl"] {
        background: rgba(16, 20, 32, 0.85) !important;
        border: 1px solid var(--border-gold) !important;
        border-radius: 14px !important;
        padding: 6px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35) !important;
        gap: 6px !important;
    }

    [data-testid="stSegmentedControl"] button {
        border-radius: 10px !important;
        padding: 8px 20px !important;
        font-size: 0.90rem !important;
        font-weight: 600 !important;
        color: #94A3B8 !important;
        border: 1px solid transparent !important;
        transition: all 0.25s ease !important;
    }

    [data-testid="stSegmentedControl"] button:hover {
        color: #FFFDF7 !important;
        background: rgba(212, 175, 55, 0.12) !important;
        border-color: rgba(212, 175, 55, 0.25) !important;
    }

    [data-testid="stSegmentedControl"] button[aria-checked="true"] {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.3) 0%, rgba(212, 175, 55, 0.12) 100%) !important;
        color: #FFFDF7 !important;
        border-color: var(--primary-gold) !important;
        box-shadow: 0 4px 16px rgba(212, 175, 55, 0.28) !important;
        font-weight: 700 !important;
    }

    /* Hero Banner for Studio Home */
    .hero-banner {
        background: linear-gradient(135deg, rgba(32, 26, 46, 0.85) 0%, rgba(16, 19, 29, 0.95) 100%);
        border: 1px solid var(--border-gold-bright);
        border-radius: 24px;
        padding: 38px 42px;
        margin-bottom: 28px;
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.5), var(--accent-glow);
        position: relative;
        overflow: hidden;
    }

    .hero-banner::after {
        content: "✦";
        position: absolute;
        top: 20px;
        right: 30px;
        font-size: 3.5rem;
        color: rgba(212, 175, 55, 0.12);
        font-family: serif;
    }

    .hero-title {
        font-family: 'Cinzel', serif;
        font-size: 2.85rem;
        font-weight: 800;
        line-height: 1.15;
        background: linear-gradient(135deg, #FFFFFF 0%, #F5E6BE 40%, #D4AF37 80%, #997819 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: 1.5px;
    }

    .hero-subtitle {
        color: #CBD5E1;
        font-size: 1.08rem;
        margin-top: 12px;
        max-width: 720px;
        line-height: 1.6;
        font-weight: 400;
    }

    .hero-badge-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 20px;
        flex-wrap: wrap;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 16px;
        background: rgba(212, 175, 55, 0.12);
        border: 1px solid var(--border-gold);
        border-radius: 30px;
        color: var(--primary-gold);
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* Action Cards on Home Page */
    .hub-action-card {
        background: linear-gradient(145deg, rgba(22, 27, 42, 0.85) 0%, rgba(15, 18, 28, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 24px;
        transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }

    .hub-action-card:hover {
        transform: translateY(-6px);
        border-color: var(--primary-gold);
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.55), 0 0 24px rgba(212, 175, 55, 0.22);
        background: linear-gradient(145deg, rgba(28, 34, 52, 0.95) 0%, rgba(18, 22, 34, 0.98) 100%);
    }

    .hub-card-icon {
        font-size: 2.2rem;
        margin-bottom: 12px;
    }

    .hub-card-title {
        font-family: 'Cinzel', serif;
        font-size: 1.3rem;
        color: #FFFDF7;
        margin: 0 0 8px 0;
        font-weight: 700;
    }

    .hub-card-desc {
        color: var(--text-muted);
        font-size: 0.88rem;
        line-height: 1.5;
        margin-bottom: 16px;
    }

    /* Template Showcase Cards */
    .template-card {
        background: linear-gradient(145deg, rgba(20, 25, 38, 0.85) 0%, rgba(14, 17, 26, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 22px;
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.35);
    }

    .template-card:hover {
        transform: translateY(-5px);
        border-color: var(--primary-gold);
        box-shadow: 0 14px 32px rgba(0, 0, 0, 0.5), 0 0 24px rgba(212, 175, 55, 0.2);
    }

    .template-badge {
        font-size: 0.75rem;
        padding: 4px 12px;
        border-radius: 20px;
        background: rgba(212, 175, 55, 0.16);
        color: var(--primary-gold);
        border: 1px solid rgba(212, 175, 55, 0.35);
        font-weight: 700;
        letter-spacing: 0.4px;
        width: fit-content;
        margin-bottom: 8px;
    }

    /* Color Swatch Dots */
    .color-swatch-bar {
        display: flex;
        align-items: center;
        gap: 6px;
        margin: 10px 0 14px 0;
    }

    .color-swatch-dot {
        width: 18px;
        height: 18px;
        border-radius: 50%;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.35);
    }

    /* Input Fields & Textareas */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        background-color: rgba(16, 20, 32, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        border-radius: 12px !important;
        color: #FFFDF7 !important;
        font-size: 0.92rem !important;
        transition: all 0.2s ease !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-gold) !important;
        box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.3) !important;
        background-color: rgba(20, 25, 40, 0.95) !important;
    }

    /* Streamlit Buttons */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        letter-spacing: 0.4px !important;
        padding: 10px 22px !important;
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #E5C058 0%, #C49826 50%, #997819 100%) !important;
        color: #0B0E14 !important;
        border: 1px solid #FFE896 !important;
        font-weight: 700 !important;
        box-shadow: 0 6px 18px rgba(212, 175, 55, 0.38) !important;
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(212, 175, 55, 0.55) !important;
    }

    .stButton > button[kind="secondary"]:hover {
        border-color: var(--primary-gold) !important;
        color: #FFFDF7 !important;
        transform: translateY(-2px);
    }

    /* Apply AI Button Box */
    .apply-card-box {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.18) 0%, rgba(26, 32, 48, 0.9) 100%);
        border: 1px solid var(--primary-gold);
        border-radius: 14px;
        padding: 16px 20px;
        margin: 14px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 14px;
        box-shadow: 0 8px 24px rgba(212, 175, 55, 0.18);
    }

    /* Glassmorphic Section Containers */
    .glass-panel {
        background: var(--card-bg);
        border: 1px solid var(--border-gold);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(14px);
        margin-bottom: 20px;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
