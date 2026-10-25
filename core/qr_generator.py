"""Dynamic QR Code generator for invitations (Google Maps venue or WhatsApp RSVP)."""
import io
import base64
from typing import Tuple, Optional
import qrcode
from PIL import Image


def generate_qr_code(
    data: str,
    fill_color: str = "#1A1A1A",
    back_color: str = "#FFFFFF",
    box_size: int = 8,
    border: int = 2,
) -> Tuple[Optional[Image.Image], Optional[str]]:
    """Generates a QR code and returns both PIL Image and base64 Data URI."""
    if not data or not data.strip():
        return None, None

    clean_data = data.strip()
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=box_size,
            border=border,
        )
        qr.add_data(clean_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

        # Create base64 representation
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        b64_str = base64.b64encode(buf.getvalue()).decode("utf-8")
        data_uri = f"data:image/png;base64,{b64_str}"

        return img, data_uri
    except Exception:
        return None, None
