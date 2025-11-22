"""
PDF generation service for CV/Resume.

Uses WeasyPrint for server-side PDF generation.
WeasyPrint works perfectly on Railway (Linux) - no Windows fallback needed.
"""

from io import BytesIO
from flask import render_template
import os

try:
    from weasyprint import HTML, CSS

    WEASYPRINT_AVAILABLE = True
except (OSError, ImportError) as e:
    WEASYPRINT_AVAILABLE = False
    WEASYPRINT_ERROR = str(e)


class PDFService:
    """Service for generating PDFs from HTML templates"""

    def __init__(self):
        """Initialize PDF service"""
        if not WEASYPRINT_AVAILABLE:
            raise RuntimeError(
                f"WeasyPrint is not available. Error: {WEASYPRINT_ERROR}\n"
                "On Railway (Linux), install system dependencies in your Dockerfile or Railway config:\n"
                "apt-get update && apt-get install -y libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info"
            )

    def generate_cv_pdf(self, cv_data, lang="es"):
        """
        Generate PDF from CV HTML template.

        Args:
            cv_data: Dict with CV data in JSON Resume format
            lang: Language code (e.g., 'es', 'en')

        Returns:
            BytesIO object with PDF content
        """
        # Get absolute paths for static files
        backend_dir = os.path.dirname(os.path.dirname(__file__))
        static_dir = os.path.join(backend_dir, "static")
        css_path = os.path.join(static_dir, "styles", "cv.css")
        images_dir = os.path.join(static_dir, "images")

        # Prepare image path for template (absolute path for WeasyPrint)
        profile_img_path = os.path.join(images_dir, "profilepicture.jpg")
        if os.path.exists(profile_img_path):
            # Use file:// URL for WeasyPrint
            profile_img_url = f"file://{profile_img_path}".replace("\\", "/")
        else:
            profile_img_url = None

        # Render HTML template with CV data and absolute image path
        html_string = render_template(
            "cv.html", cv_data=cv_data, lang=lang, profile_img_abs_path=profile_img_url
        )

        # Generate PDF with absolute base URL
        base_url = backend_dir
        html = HTML(string=html_string, base_url=base_url)

        # Load CSS if it exists
        css = None
        if os.path.exists(css_path):
            css = CSS(filename=css_path)

        # Generate PDF bytes
        pdf_bytes = BytesIO()
        html.write_pdf(pdf_bytes, stylesheets=[css] if css else None)
        pdf_bytes.seek(0)

        return pdf_bytes
