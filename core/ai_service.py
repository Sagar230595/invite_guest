"""Gemini 3.8 Flash AI service for invitation card crafting, copywriting, and multimodal analysis."""
import os
import io
import json
import re
from typing import Generator, List, Optional, Tuple, Any
from PIL import Image

from google import genai
from google.genai import types

from config.settings import GEMINI_API_KEY, DEFAULT_MODEL, FALLBACK_MODELS


INVITATION_SYSTEM_PROMPT = """You are "Invito AI", a master invitation card copywriter, luxury stationery designer, and celebrations etiquette expert.
Your mission is to help users design memorable, elegant, and impactful invitation cards for any occasion (Weddings, Birthdays, Anniversaries, Baby Showers, Corporate Galas, Graduations, Housewarmings, Festive Parties, etc.).

When working with users:
1. Warm, Celebratory & Creative Tone: Provide thoughtful phrasing, poetic verses, respectful traditional wording, or chic modern copy based on user needs.
2. Multimodal Capability: If the user provides a sample photo or PDF card, analyze its color palette, aesthetic theme, font vibe, and structure, and offer tailored ideas or replicate its best elements.
3. Structured Output For Instant Card Import:
Whenever you propose or refine an invitation card, provide your friendly suggestions and creative thoughts, and THEN provide a JSON block inside ```json and ``` with the complete card details.
The JSON format must strictly follow:
```json
{
  "template_id": "engagement_sparkle | royal_wedding | botanical_wedding | birthday_bash | baby_shower | corporate_gala | golden_anniversary | graduation | diwali_festive",
  "headline": "Short invite header / blessing / family greeting (e.g. Together with their families... / Join us to celebrate...)",
  "title": "Main couple / honoree names / event title (e.g. Aarav & Meera)",
  "event_type": "Event subtitle (e.g. Wedding Ceremony & Reception / 30th Birthday Soirée)",
  "host_names": "Names of hosts / parents (e.g. Hosted with love by the Sharma Family)",
  "date": "Full date (e.g. Saturday, December 18, 2026)",
  "time": "Time details (e.g. 6:30 PM Onwards)",
  "venue": "Full venue name and city (e.g. The Grand Lotus Ballroom, Mumbai)",
  "rsvp": "Contact info / phone / email for RSVP (e.g. RSVP to Rahul: +91 98765 43210)",
  "dress_code": "Attire guidance (e.g. Black Tie / Traditional Indian Elegance)",
  "special_note": "Gift policy / special note (e.g. Your blessings are our greatest gift / Valet parking available)",
  "bg_color": "Hex color code for card background (e.g. #4A0E17)",
  "text_color": "Hex color code for primary text (e.g. #FFFDF7)",
  "primary_color": "Hex color code for gold/accent/frame (e.g. #D4AF37)"
}
```
Always ensure the JSON is valid and complete so the user can import it to their card canvas in 1 click!
"""


def is_api_key_configured() -> bool:
    """Check if the Gemini API key is present in environment or settings."""
    key = os.getenv("GEMINI_API_KEY", "").strip() or GEMINI_API_KEY
    return bool(key and len(key) > 5)


def get_gemini_client() -> Optional[genai.Client]:
    """Initializes and returns a Google GenAI Client instance."""
    key = os.getenv("GEMINI_API_KEY", "").strip() or GEMINI_API_KEY
    if not key:
        return None
    try:
        return genai.Client(api_key=key)
    except Exception:
        return None


def extract_card_json(response_text: str) -> Optional[dict]:
    """Extracts the structured JSON block from the assistant's reply if present."""
    if not response_text:
        return None
    
    # Try finding fenced ```json ... ``` blocks
    pattern = r"```json\s*(\{.*?\})\s*```"
    match = re.search(pattern, response_text, re.DOTALL)
    if match:
        json_str = match.group(1).strip()
        try:
            return json.loads(json_str)
        except Exception:
            pass

    # Fallback to finding outermost curly braces
    try:
        start_idx = response_text.find("{")
        end_idx = response_text.rfind("}")
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            candidate = response_text[start_idx : end_idx + 1]
            data = json.loads(candidate)
            if "title" in data or "event_type" in data or "venue" in data:
                return data
    except Exception:
        pass

    return None


def pil_to_part(pil_image: Image.Image) -> types.Part:
    """Converts a PIL Image into a types.Part for Gemini multimodal request."""
    buf = io.BytesIO()
    # Save as JPEG for fast transmission & low latency
    pil_image.save(buf, format="JPEG", quality=85)
    return types.Part.from_bytes(data=buf.getvalue(), mime_type="image/jpeg")


def stream_ai_chat(
    messages: List[dict],
    attached_images: Optional[List[Image.Image]] = None,
    document_text: Optional[str] = None,
    model_name: str = DEFAULT_MODEL,
) -> Generator[str, None, None]:
    """Streams response from Gemini 3.8 Flash model with multimodal input support."""
    client = get_gemini_client()
    if not client:
        yield (
            "⚠️ **Gemini API Key is missing!**\n\n"
            "Please open your `.env` file in the project folder and set:\n"
            "```env\n"
            "GEMINI_API_KEY=your_actual_gemini_api_key_here\n"
            "```\n"
            "Then refresh or send another message. In the meantime, you can still customize and download all invitation templates manually!"
        )
        return

    # Build contents array
    contents: List[Any] = []

    # Inject system instruction & conversation context
    context_prefix = (
        f"[SYSTEM INSTRUCTION]\n{INVITATION_SYSTEM_PROMPT}\n\n"
        "[CONVERSATION HISTORY]\n"
    )

    for msg in messages[:-1]:
        role_label = "User" if msg["role"] == "user" else "Assistant"
        context_prefix += f"{role_label}: {msg['content']}\n"

    last_user_prompt = messages[-1]["content"] if messages else "Hello! Help me make an invitation card."

    # If there are attached images or document text, append them to the request
    if document_text and document_text.strip():
        last_user_prompt += f"\n\n[ATTACHED SAMPLE DOCUMENT / CARD TEXT EXTRACT]:\n{document_text.strip()}"

    contents.append(f"{context_prefix}\nUser: {last_user_prompt}\nAssistant:")

    if attached_images:
        for img in attached_images[:3]:  # Limit to 3 images to prevent latency lag
            contents.append(pil_to_part(img))

    # Try streaming with requested model (gemini-3.8-flash), falling back if needed
    models_to_try = [model_name] + [m for m in FALLBACK_MODELS if m != model_name]
    
    stream_success = False
    last_exception = None

    for candidate_model in models_to_try:
        try:
            response_stream = client.models.generate_content_stream(
                model=candidate_model,
                contents=contents,
            )
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text
            stream_success = True
            break
        except Exception as e:
            last_exception = e
            # Try next fallback model
            continue

    if not stream_success:
        err_msg = str(last_exception)
        yield (
            f"❌ **AI Service Notice**: Could not complete request with model `{model_name}`.\n\n"
            f"Details: `{err_msg}`\n\n"
            "Tip: Ensure your `GEMINI_API_KEY` in `.env` is valid and active on [Google AI Studio](https://aistudio.google.com/)."
        )


def quick_enhance_copy(
    event_type: str,
    title: str,
    tone: str = "elegant",
    model_name: str = DEFAULT_MODEL,
) -> Optional[dict]:
    """Generates rapid wording suggestions for a card."""
    client = get_gemini_client()
    if not client:
        return None

    prompt = (
        f"Generate a polished, {tone} invitation card wording for:\n"
        f"Event: {event_type}\n"
        f"Honoree / Couple: {title}\n\n"
        "Return ONLY a JSON block with: headline, event_type, dress_code, special_note."
    )

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        return extract_card_json(response.text or "")
    except Exception:
        return None
