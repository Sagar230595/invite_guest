"""Application configuration settings for Invito AI."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory & Load .env
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

# Application Metadata
APP_NAME = "Invito AI"
APP_TAGLINE = "Smart Invitation Card Studio & AI Assistant"
APP_ICON = "💌"
APP_VERSION = "2.0.0"

# Gemini AI Settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip() or "gemini-3.8-flash"

# Fallback models in case the target tier or environment requires it
FALLBACK_MODELS = [
    DEFAULT_MODEL,
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
]

# Supported File Types for Reference Upload
SUPPORTED_IMAGE_TYPES = ["png", "jpg", "jpeg", "webp"]
SUPPORTED_DOC_TYPES = ["pdf"]
ALL_SUPPORTED_UPLOADS = SUPPORTED_IMAGE_TYPES + SUPPORTED_DOC_TYPES

# Card Aspect Ratios
ASPECT_RATIOS = {
    "Portrait (5:7 - Classic Stationery)": {"ratio": "5/7", "width": 500, "height": 700},
    "Story / WhatsApp (9:16 - Mobile Full)": {"ratio": "9/16", "width": 450, "height": 800},
    "Square (1:1 - Instagram & Social)": {"ratio": "1/1", "width": 550, "height": 550},
    "Landscape (7:5 - Wide Deluxe)": {"ratio": "7/5", "width": 700, "height": 500},
}

# Event Categories
EVENT_CATEGORIES = [
    "Wedding & Reception",
    "Engagement & Ring Ceremony",
    "Birthday Celebration",
    "Anniversary & Jubilee",
    "Baby Shower & Welcome Baby",
    "Corporate Gala & Conference",
    "Graduation Ceremony",
    "Festive & Cultural Gathering",
    "Housewarming & Pooja",
    "Dinner Party & Cocktails",
]

# Google Fonts Options
FONT_OPTIONS = {
    "Cinzel (Regal & Classical)": "'Cinzel', serif",
    "Playfair Display (Luxury & Romantic)": "'Playfair Display', serif",
    "Great Vibes (Graceful Calligraphy)": "'Great Vibes', cursive",
    "Alex Brush (Elegant Cursive)": "'Alex Brush', cursive",
    "Montserrat (Modern Sleek Sans)": "'Montserrat', sans-serif",
    "Poppins (Friendly & Contemporary)": "'Poppins', sans-serif",
    "Lora (Editorial Warm Serif)": "'Lora', serif",
    "Marcellus (Sculpted Dignity)": "'Marcellus', serif",
    "Dancing Script (Playful Festive)": "'Dancing Script', cursive",
}

# Border Ornaments
BORDER_STYLES = [
    "Double Thin & Gold Foil Line",
    "Ornate Royal Vintage Filigree",
    "Modern Minimalist Inset Border",
    "Geometric Art Deco Corners",
    "Floral Botanical Frame",
    "Clean Solid Luxury Border",
    "None / Borderless",
]
