"""High-fidelity HTML & CSS Invitation Card Renderer with live preview and pixel-perfect WYSIWYG export."""
import base64
import io
from typing import Optional
from PIL import Image

GOOGLE_FONTS_IMPORT = """
@import url('https://fonts.googleapis.com/css2?family=Alex+Brush&family=Cinzel:wght@400;600;700;900&family=Dancing+Script:wght@500;700&family=Great+Vibes&family=Lora:ital,wght@0,400;0,600;1,400&family=Marcellus&family=Montserrat:wght@300;400;600;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Poppins:wght@300;400;600&display=swap');
"""


def pil_to_base64_uri(img: Optional[Image.Image]) -> Optional[str]:
    """Converts a PIL image to a base64 Data URI."""
    if img is None:
        return None
    try:
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{b64}"
    except Exception:
        return None


def get_aspect_ratio_dimensions(aspect_ratio_name: str) -> dict:
    """Returns CSS max-width and min-height based on chosen aspect ratio."""
    if "9:16" in aspect_ratio_name or "Story" in aspect_ratio_name:
        return {"max_width": "420px", "min_height": "750px", "ratio": "9/16"}
    elif "1:1" in aspect_ratio_name or "Square" in aspect_ratio_name:
        return {"max_width": "540px", "min_height": "540px", "ratio": "1/1"}
    elif "7:5" in aspect_ratio_name or "Landscape" in aspect_ratio_name:
        return {"max_width": "680px", "min_height": "480px", "ratio": "7/5"}
    else:  # Portrait 5:7
        return {"max_width": "500px", "min_height": "690px", "ratio": "5/7"}


def render_invitation_html(
    card_data: dict,
    theme: dict,
    aspect_ratio: str = "Portrait (5:7 - Classic Stationery)",
    qr_data_uri: Optional[str] = None,
    photo_data_uri: Optional[str] = None,
    border_style_choice: str = "Double Thin & Gold Foil Line",
    include_wrapper: bool = True,
    show_export_buttons: bool = False,
    card_filename: str = "invitation_card",
) -> str:
    """Renders complete HTML/CSS for the invitation card, with optional 100% WYSIWYG export buttons."""
    dims = get_aspect_ratio_dimensions(aspect_ratio)

    # Theme parameters with fallbacks
    bg_gradient = theme.get("card_bg_gradient", "linear-gradient(145deg, #1A1A1A, #2C2C2C)")
    text_color = theme.get("text_color", "#FFFDF7")
    primary_color = theme.get("primary_color", "#D4AF37")
    secondary_color = theme.get("secondary_color", "#E5D4B8")
    font_title = theme.get("font_family_title", "'Cinzel', serif")
    font_body = theme.get("font_family_body", "'Lora', serif")
    font_accent = theme.get("font_family_accent", "'Alex Brush', cursive")

    # Border style CSS rules
    if border_style_choice == "Ornate Royal Vintage Filigree":
        border_css = f"outline: 2px solid {primary_color}; outline-offset: -12px; border: 1px solid rgba(255,255,255,0.25);"
    elif border_style_choice == "Modern Minimalist Inset Border":
        border_css = f"border: 1px solid {primary_color}; box-shadow: inset 0 0 0 8px rgba(0,0,0,0.2);"
    elif border_style_choice == "Geometric Art Deco Corners":
        border_css = f"border: 2px solid {primary_color}; outline: 1px dashed {secondary_color}; outline-offset: -8px;"
    elif border_style_choice == "Clean Solid Luxury Border":
        border_css = f"border: 3px solid {primary_color};"
    elif border_style_choice == "None / Borderless":
        border_css = "border: none;"
    else:  # Default Double Thin & Gold Foil Line
        border_css = f"border: 2px solid {primary_color}; box-shadow: inset 0 0 0 6px rgba(0,0,0,0.3), inset 0 0 0 7px {primary_color};"

    # Card content fields
    headline = card_data.get("headline", "").replace("\n", "<br>")
    title = card_data.get("title", "")
    event_type = card_data.get("event_type", "")
    host_names = card_data.get("host_names", "")
    date_str = card_data.get("date", "")
    time_str = card_data.get("time", "")
    venue_str = card_data.get("venue", "").replace("\n", "<br>")
    rsvp_str = card_data.get("rsvp", "")
    dress_code = card_data.get("dress_code", "")
    special_note = card_data.get("special_note", "")

    # Optional photo/monogram block
    photo_html = ""
    if photo_data_uri:
        photo_html = f"""
        <div style="margin: 10px auto 14px auto; text-align: center;">
            <img src="{photo_data_uri}" 
                 alt="Event Emblem" 
                 style="width: 82px; height: 82px; object-fit: cover; border-radius: 50%; border: 2px solid {primary_color}; box-shadow: 0 4px 12px rgba(0,0,0,0.35);" />
        </div>
        """

    # Optional QR code block
    qr_html = ""
    if qr_data_uri:
        qr_html = f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 10px;">
            <div style="background: #ffffff; padding: 5px; border-radius: 8px; border: 1px solid {primary_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.3); line-height: 0;">
                <img src="{qr_data_uri}" alt="Scan QR Code" style="width: 68px; height: 68px; display: block;" />
            </div>
            <span style="font-size: 0.65rem; color: {secondary_color}; margin-top: 4px; letter-spacing: 0.8px; text-transform: uppercase;">
                Scan for Venue / RSVP
            </span>
        </div>
        """

    # Optional dress code / special note
    extras_html = ""
    if dress_code or special_note:
        extras_parts = []
        if dress_code:
            extras_parts.append(f"""
                <span style="font-size: 0.72rem; color: {secondary_color}; letter-spacing: 0.5px;">
                    ✨ <strong>Attire:</strong> {dress_code}
                </span>
            """)
        if special_note:
            extras_parts.append(f"""
                <div style="font-size: 0.70rem; color: rgba(255,255,255,0.78); font-style: italic; margin-top: 4px; max-width: 90%;">
                    "{special_note}"
                </div>
            """)
        extras_html = f"""
        <div style="margin-top: 12px; display: flex; flex-direction: column; align-items: center; gap: 3px;">
            {"".join(extras_parts)}
        </div>
        """

    card_core = f"""
    <div id="invitation-card" style="
        width: 100%;
        max-width: {dims['max_width']};
        min-height: {dims['min_height']};
        margin: 0 auto;
        background: {bg_gradient};
        color: {text_color};
        padding: 36px 28px;
        border-radius: 16px;
        {border_css}
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.45), 0 0 30px rgba(212, 175, 55, 0.12);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        text-align: center;
        box-sizing: border-box;
        position: relative;
        overflow: hidden;
        font-family: {font_body};
    ">
        <!-- Luxury corner ornaments -->
        <div style="position: absolute; top: 12px; left: 14px; color: {primary_color}; font-size: 1.1rem; opacity: 0.75;">✦</div>
        <div style="position: absolute; top: 12px; right: 14px; color: {primary_color}; font-size: 1.1rem; opacity: 0.75;">✦</div>
        <div style="position: absolute; bottom: 12px; left: 14px; color: {primary_color}; font-size: 1.1rem; opacity: 0.75;">✦</div>
        <div style="position: absolute; bottom: 12px; right: 14px; color: {primary_color}; font-size: 1.1rem; opacity: 0.75;">✦</div>

        <!-- Header / Headline Section -->
        <div style="width: 100%; margin-bottom: 8px;">
            {photo_html}
            <div style="
                font-family: {font_accent};
                font-size: 1.25rem;
                color: {primary_color};
                line-height: 1.3;
                letter-spacing: 0.5px;
                margin-bottom: 6px;
            ">
                {headline}
            </div>
            {f'<div style="font-size: 0.78rem; letter-spacing: 1.2px; text-transform: uppercase; color: {secondary_color}; opacity: 0.9; margin-top: 4px;">{host_names}</div>' if host_names else ''}
        </div>

        <!-- Divider Line -->
        <div style="display: flex; align-items: center; justify-content: center; width: 60%; margin: 6px auto;">
            <div style="flex: 1; height: 1px; background: linear-gradient(to right, transparent, {primary_color});"></div>
            <span style="color: {primary_color}; padding: 0 8px; font-size: 0.8rem;">❦</span>
            <div style="flex: 1; height: 1px; background: linear-gradient(to left, transparent, {primary_color});"></div>
        </div>

        <!-- Main Title / Couple / Honoree Names -->
        <div style="width: 100%; margin: 12px 0;">
            <h1 style="
                font-family: {font_title};
                font-size: 2.15rem;
                font-weight: 700;
                color: {primary_color};
                margin: 0;
                line-height: 1.15;
                letter-spacing: 1.5px;
                text-shadow: 0 2px 8px rgba(0,0,0,0.4);
            ">
                {title}
            </h1>
            <div style="
                font-size: 0.88rem;
                font-weight: 400;
                color: {secondary_color};
                margin-top: 8px;
                letter-spacing: 1px;
                text-transform: uppercase;
            ">
                {event_type}
            </div>
        </div>

        <!-- Date & Time Section (Pill badge format) -->
        <div style="
            width: 90%;
            background: rgba(0, 0, 0, 0.22);
            border: 1px solid rgba(212, 175, 55, 0.35);
            border-radius: 10px;
            padding: 10px 14px;
            margin: 8px auto;
            backdrop-filter: blur(4px);
        ">
            <div style="font-size: 0.95rem; font-weight: 600; color: {text_color}; letter-spacing: 0.5px;">
                🗓️ {date_str}
            </div>
            {f'<div style="font-size: 0.82rem; color: {primary_color}; margin-top: 4px; letter-spacing: 0.5px;">⏰ {time_str}</div>' if time_str else ''}
        </div>

        <!-- Venue / Location Section -->
        <div style="width: 100%; margin: 8px 0;">
            <div style="font-size: 0.72rem; letter-spacing: 1.5px; text-transform: uppercase; color: {primary_color}; margin-bottom: 3px;">
                📍 Venue
            </div>
            <div style="font-size: 0.88rem; color: {text_color}; line-height: 1.35; max-width: 88%; margin: 0 auto;">
                {venue_str}
            </div>
        </div>

        <!-- Extras (Dress Code & Special Note) -->
        {extras_html}

        <!-- QR Code & RSVP Section -->
        <div style="width: 100%; margin-top: 10px; border-top: 1px dashed rgba(212,175,55,0.3); padding-top: 10px;">
            {qr_html}
            {f'<div style="font-size: 0.76rem; color: {text_color}; margin-top: 8px; letter-spacing: 0.4px;"><strong>RSVP:</strong> {rsvp_str}</div>' if rsvp_str else ''}
        </div>
    </div>
    """

    if not include_wrapper:
        return card_core

    # WYSIWYG Export Scripts and Buttons
    export_buttons_html = ""
    export_scripts = ""
    if show_export_buttons:
        export_buttons_html = f"""
        <div style="display: flex; justify-content: center; gap: 14px; margin-bottom: 22px; flex-wrap: wrap;">
            <button id="btn-export-png" onclick="exportExactPNG()" style="
                background: linear-gradient(135deg, #E5C058 0%, #C49826 50%, #997819 100%);
                color: #0B0E14;
                border: 1px solid #FFE896;
                padding: 12px 24px;
                border-radius: 12px;
                font-weight: 700;
                font-size: 0.95rem;
                cursor: pointer;
                display: inline-flex;
                align-items: center;
                gap: 8px;
                box-shadow: 0 4px 18px rgba(212, 175, 55, 0.45);
                font-family: 'Plus Jakarta Sans', sans-serif;
                transition: transform 0.2s ease;
            ">
                📸 Download Exact Preview as PNG (300 DPI)
            </button>
            <button id="btn-export-pdf" onclick="exportExactPDF()" style="
                background: rgba(22, 27, 42, 0.95);
                color: #F8F9FA;
                border: 1px solid rgba(212, 175, 55, 0.5);
                padding: 12px 24px;
                border-radius: 12px;
                font-weight: 600;
                font-size: 0.95rem;
                cursor: pointer;
                display: inline-flex;
                align-items: center;
                gap: 8px;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
                font-family: 'Plus Jakarta Sans', sans-serif;
                transition: transform 0.2s ease;
            ">
                📄 Download Exact Preview as PDF
            </button>
        </div>
        """

        export_scripts = f"""
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
        <script>
        async function exportExactPNG() {{
            const btn = document.getElementById('btn-export-png');
            const originalText = btn.innerHTML;
            btn.innerHTML = '⏳ Rendering 300 DPI PNG...';
            btn.disabled = true;

            try {{
                await document.fonts.ready;
                await new Promise(r => setTimeout(r, 150));

                const card = document.getElementById('invitation-card');
                const canvas = await html2canvas(card, {{
                    scale: 3, // Ultra-sharp 300 DPI retina print quality
                    useCORS: true,
                    allowTaint: true,
                    backgroundColor: null,
                    logging: false,
                }});

                const link = document.createElement('a');
                link.download = '{card_filename}.png';
                link.href = canvas.toDataURL('image/png', 1.0);
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }} catch (err) {{
                alert('PNG export error: ' + err);
            }} finally {{
                btn.innerHTML = originalText;
                btn.disabled = false;
            }}
        }}

        async function exportExactPDF() {{
            const btn = document.getElementById('btn-export-pdf');
            const originalText = btn.innerHTML;
            btn.innerHTML = '⏳ Generating PDF...';
            btn.disabled = true;

            try {{
                await document.fonts.ready;
                await new Promise(r => setTimeout(r, 150));

                const card = document.getElementById('invitation-card');
                const canvas = await html2canvas(card, {{
                    scale: 3,
                    useCORS: true,
                    allowTaint: true,
                    backgroundColor: null,
                    logging: false,
                }});

                const imgData = canvas.toDataURL('image/png', 1.0);
                const {{ jsPDF }} = window.jspdf;
                const isLandscape = canvas.width > canvas.height;
                const pdf = new jsPDF({{
                    orientation: isLandscape ? 'landscape' : 'portrait',
                    unit: 'pt',
                    format: [canvas.width / 3, canvas.height / 3]
                }});
                pdf.addImage(imgData, 'PNG', 0, 0, canvas.width / 3, canvas.height / 3);
                pdf.save('{card_filename}.pdf');
            }} catch (err) {{
                alert('PDF export error: ' + err);
            }} finally {{
                btn.innerHTML = originalText;
                btn.disabled = false;
            }}
        }}
        </script>
        """

    return f"""
    <style>
        {GOOGLE_FONTS_IMPORT}
        #invitation-card * {{
            box-sizing: border-box;
            -webkit-font-smoothing: antialiased;
        }}
        button:hover {{
            transform: translateY(-2px);
        }}
    </style>
    <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; width: 100%; padding: 10px 0;">
        {export_buttons_html}
        {card_core}
    </div>
    {export_scripts}
    """
