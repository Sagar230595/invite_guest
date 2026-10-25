"""File parser module to process sample photos and PDF invitations."""
import io
from dataclasses import dataclass
from typing import Optional, List
from PIL import Image
import pypdf


@dataclass
class ParsedDocument:
    filename: str
    file_type: str
    text_content: str
    preview_image: Optional[Image.Image] = None
    all_images: Optional[List[Image.Image]] = None
    error: Optional[str] = None

    @property
    def is_image(self) -> bool:
        return self.file_type.lower() in ["png", "jpg", "jpeg", "webp"]

    @property
    def is_pdf(self) -> bool:
        return self.file_type.lower() == "pdf"


def process_image_upload(uploaded_file, max_dim: int = 1600) -> ParsedDocument:
    """Processes an uploaded image file, optimizing its size for AI analysis."""
    try:
        image = Image.open(uploaded_file)
        # Convert RGBA / P / CMYK to RGB
        if image.mode in ("RGBA", "LA"):
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            image = background
        elif image.mode != "RGB":
            image = image.convert("RGB")

        # Downscale if excessively large to keep latency ultra-low
        if max(image.size) > max_dim:
            image.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)

        return ParsedDocument(
            filename=uploaded_file.name,
            file_type=uploaded_file.name.split(".")[-1].lower(),
            text_content="[Image reference provided]",
            preview_image=image,
            all_images=[image],
        )
    except Exception as e:
        return ParsedDocument(
            filename=uploaded_file.name,
            file_type="image",
            text_content="",
            error=f"Failed to process image: {str(e)}",
        )


def process_pdf_upload(uploaded_file, max_pages: int = 5) -> ParsedDocument:
    """Processes an uploaded PDF invitation card, extracting text and embedded graphics."""
    try:
        pdf_bytes = uploaded_file.read()
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        
        extracted_texts = []
        extracted_images = []

        total_pages = min(len(reader.pages), max_pages)
        for idx in range(total_pages):
            page = reader.pages[idx]
            page_text = page.extract_text() or ""
            if page_text.strip():
                extracted_texts.append(f"--- Page {idx + 1} ---\n{page_text.strip()}")

            # Extract any embedded sample artwork/images
            try:
                for img_file in page.images:
                    img_data = img_file.data
                    pil_img = Image.open(io.BytesIO(img_data)).convert("RGB")
                    if pil_img.size[0] > 100 and pil_img.size[1] > 100:  # ignore tiny icons
                        extracted_images.append(pil_img)
                        if len(extracted_images) >= 3:
                            break
            except Exception:
                pass

        full_text = "\n\n".join(extracted_texts).strip()
        if not full_text and not extracted_images:
            full_text = "[PDF card uploaded with vector artwork or scanned image]"

        preview = extracted_images[0] if extracted_images else None

        return ParsedDocument(
            filename=uploaded_file.name,
            file_type="pdf",
            text_content=full_text,
            preview_image=preview,
            all_images=extracted_images,
        )
    except Exception as e:
        return ParsedDocument(
            filename=uploaded_file.name,
            file_type="pdf",
            text_content="",
            error=f"Failed to process PDF: {str(e)}",
        )


def parse_uploaded_file(uploaded_file) -> Optional[ParsedDocument]:
    """Unified handler for processing sample files."""
    if uploaded_file is None:
        return None

    filename = uploaded_file.name.lower()
    if filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
        return process_image_upload(uploaded_file)
    elif filename.endswith(".pdf"):
        return process_pdf_upload(uploaded_file)
    else:
        return ParsedDocument(
            filename=uploaded_file.name,
            file_type="unsupported",
            text_content="",
            error="Unsupported file format. Please upload PNG, JPG, WEBP, or PDF.",
        )
