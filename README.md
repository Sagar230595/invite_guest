# 💌 Invito AI — Luxury Multipage Invitation Card Studio

A modern, low-latency multipage Streamlit web application designed for creating, styling, and customizing luxury invitation cards. Featuring a specialized AI Assistant powered by Google's **`gemini-3.8-flash`** model with multimodal support (upload sample photos & PDFs), curated famous designer templates, interactive QR code generation, real-time live preview, and high-resolution PNG & PDF export.

---

## 🌟 Multipage Architecture

The app is now structured as a **Multipage Application** using Streamlit's native `st.navigation`:

1. **🏠 Studio Home (`views/home.py`)**:
   - Executive launchpad with hero branding and feature highlights.
   - Quick launch cards to jump directly into Templates, AI Co-Designer, or the Editor.
   - **Active Canvas Spotlight**: Live preview of your active card with 1-click quick downloads.

2. **🌟 Template Gallery (`views/templates_view.py`)**:
   - Filterable catalog of 8 designer templates across weddings, birthdays, baby showers, galas, and festivals.
   - Color palette swatches, category badges, live interactive previews, and 1-click template selection.

3. **✏️ Card Studio (`views/studio_view.py`)**:
   - Split-screen workspace: Left = deep detail & visual controls, Right = sticky real-time live card preview.
   - Full control over names, dates, times, venues, RSVP info, attire, Google Maps QR code, photo emblems, and Google Fonts.

4. **🤖 AI Assistant (`views/ai_chat_view.py`)**:
   - Master invitation copywriter powered by **`gemini-3.8-flash`** with real-time streaming.
   - Multimodal analysis: upload reference photos or PDF invitations.
   - **1-Click Card Import**: Automatically imports generated event details into your card canvas.

5. **📥 Export & Share (`views/export_view.py`)**:
   - 🖼️ **High-Resolution PNG** (1200 x 1680 print quality).
   - 📄 **Print-Ready PDF** (vector canvas rendering).
   - 💬 **WhatsApp Ready Message** (formatted with emojis and spacing ready to copy).
   - 📋 **Embeddable HTML Code**.

---

## 📂 Project Structure

```text
invite_guest/
├── app.py                      # Multipage router with st.navigation & sidebar branding
├── requirements.txt            # Python dependencies
├── .env                        # Local environment file for GEMINI_API_KEY
├── .env.example                # Example environment template
├── README.md                   # Project documentation
│
├── views/
│   ├── home.py                 # Studio Home & Executive Launchpad
│   ├── templates_view.py       # Curated Designer Templates Gallery
│   ├── studio_view.py          # Interactive Card Studio & Live Customizer
│   ├── ai_chat_view.py         # Gemini 3.8 Flash Multimodal AI Assistant
│   └── export_view.py          # Export & Share Studio (PNG, PDF, WhatsApp)
│
├── config/
│   ├── __init__.py
│   └── settings.py             # App configurations, constants & Gemini 3.8 Flash model config
│
├── core/
│   ├── __init__.py
│   ├── ai_service.py           # Gemini 3.8 Flash client, streaming chat & JSON extraction
│   ├── file_parser.py          # Multimodal PDF and Image reference parser
│   ├── exporter.py             # High-res PNG & print-ready PDF generator (ReportLab & Pillow)
│   └── qr_generator.py         # Dynamic QR code generator (Google Maps & WhatsApp)
│
├── templates/
│   ├── __init__.py
│   ├── template_data.py        # 8 famous templates library with themes & defaults
│   └── card_renderer.py        # Real-time responsive HTML/CSS invitation card renderer
│
└── ui/
    ├── __init__.py
    ├── styles.py               # Glassmorphic dark luxury CSS styles & typography
    └── components.py           # Header banner & status badges
```

---

## 🚀 Quickstart Guide

### 1. Configure Your Gemini API Key
Open the `.env` file in the project folder and set your API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-3.8-flash
```

> **Note**: As requested, **there is no API key input in the UI sidebar**; it is securely read directly from `.env`.

### 2. Launch the Application
```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

Open your browser at **`http://localhost:8501`**.
