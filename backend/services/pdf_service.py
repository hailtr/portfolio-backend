"""
PDF generation service for CV/Resume.

Supports two modes:
1. Microservice mode (production): Calls external PDF service (GCP Cloud Run)
2. Local mode (development): Uses WeasyPrint directly
"""

from io import BytesIO
import os
import re
import requests
import logging

logger = logging.getLogger(__name__)

# Get microservice URL from environment
PDF_SERVICE_URL = os.getenv("PDF_SERVICE_URL")

# Try to import WeasyPrint for local fallback
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except (OSError, ImportError) as e:
    WEASYPRINT_AVAILABLE = False
    WEASYPRINT_ERROR = str(e)


class PDFService:
    """Service for generating PDFs from HTML templates"""

    def __init__(self):
        """Initialize PDF service"""
        self.use_microservice = bool(PDF_SERVICE_URL)
        
        if self.use_microservice:
            logger.info(f"PDFService using microservice at: {PDF_SERVICE_URL}")
        elif WEASYPRINT_AVAILABLE:
            logger.info("PDFService using local WeasyPrint")
        else:
            raise RuntimeError(
                f"No PDF generation method available. "
                f"Set PDF_SERVICE_URL or install WeasyPrint. "
                f"WeasyPrint error: {WEASYPRINT_ERROR}"
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
        # Prepare HTML content
        html_string, css_content = self._prepare_html(cv_data, lang)
        
        if self.use_microservice:
            return self._generate_via_microservice(html_string, css_content, lang)
        else:
            return self._generate_locally(html_string, lang)

    def _prepare_html(self, cv_data, lang):
        """Prepare HTML and CSS content for PDF generation"""
        # Get absolute paths for static files
        backend_dir = os.path.dirname(os.path.dirname(__file__))
        static_dir = os.path.join(backend_dir, "static")
        css_path = os.path.join(static_dir, "styles", "cv.css")
        images_dir = os.path.join(static_dir, "images")

        # Prepare image path for template (absolute path for WeasyPrint)
        profile_img_path = os.path.join(images_dir, "profilepicture.jpg")
        if os.path.exists(profile_img_path):
            profile_img_url = f"file://{profile_img_path}".replace("\\", "/")
        else:
            profile_img_url = None

        # Render HTML template with CV data
        from flask import render_template
        html_string = render_template(
            "cv.html", cv_data=cv_data, lang=lang, profile_img_abs_path=profile_img_url
        )

        # Load CSS
        css_content = ""
        if os.path.exists(css_path):
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            # Add font import
            font_import = "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');\n"
            css_content = font_import + css_content

        return html_string, css_content

    def _generate_via_microservice(self, html_string, css_content, lang):
        """Generate PDF via external microservice"""
        try:
            # Inject CSS into HTML before sending
            if css_content:
                html_string = re.sub(
                    r'<link[^>]*href="[^"]*cv\.css"[^>]*>',
                    f'<style>{css_content}</style>',
                    html_string
                )
                if '<style>' not in html_string:
                    html_string = html_string.replace('</head>', f'<style>{css_content}</style></head>')
            
            # Call microservice
            response = requests.post(
                f"{PDF_SERVICE_URL}/generate",
                json={
                    "html_content": html_string,
                    "lang": lang
                },
                timeout=60  # 60 second timeout
            )
            
            if response.status_code != 200:
                error_msg = response.json().get("error", "Unknown error")
                raise Exception(f"Microservice error: {error_msg}")
            
            # Return PDF bytes
            pdf_bytes = BytesIO(response.content)
            pdf_bytes.seek(0)
            return pdf_bytes
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Microservice request failed: {e}")
            
            # Fallback to local if WeasyPrint is available
            if WEASYPRINT_AVAILABLE:
                logger.info("Falling back to local WeasyPrint")
                return self._generate_locally_with_css(html_string, css_content, lang)
            raise

    def _generate_locally(self, html_string, lang):
        """Generate PDF locally using WeasyPrint"""
        if not WEASYPRINT_AVAILABLE:
            raise RuntimeError(f"WeasyPrint not available: {WEASYPRINT_ERROR}")
        
        backend_dir = os.path.dirname(os.path.dirname(__file__))
        html = HTML(string=html_string, base_url=backend_dir)
        
        pdf_bytes = BytesIO()
        html.write_pdf(pdf_bytes)
        pdf_bytes.seek(0)
        
        return pdf_bytes

    def _generate_locally_with_css(self, html_string, css_content, lang):
        """Generate PDF locally with pre-injected CSS"""
        if not WEASYPRINT_AVAILABLE:
            raise RuntimeError(f"WeasyPrint not available: {WEASYPRINT_ERROR}")
        
        # CSS should already be injected in html_string
        backend_dir = os.path.dirname(os.path.dirname(__file__))
        html = HTML(string=html_string, base_url=backend_dir)
        
        pdf_bytes = BytesIO()
        html.write_pdf(pdf_bytes)
        pdf_bytes.seek(0)
        
        return pdf_bytes

