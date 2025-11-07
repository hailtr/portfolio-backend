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
    
    def generate_cv_pdf(self, cv_data, lang='es'):
        """
        Generate PDF from CV HTML template.
        
        Args:
            cv_data: Dict with CV data in JSON Resume format
            lang: Language code (e.g., 'es', 'en')
        
        Returns:
            BytesIO object with PDF content
        """
        # Render HTML template with CV data
        html_string = render_template('cv.html', cv_data=cv_data, lang=lang)
        
        # Get CSS file path
        css_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'static',
            'styles',
            'cv.css'
        )
        
        # Generate PDF
        # WeasyPrint can fetch online images automatically
        base_url = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        html = HTML(string=html_string, base_url=base_url)
        
        # Load CSS if it exists
        css = None
        if os.path.exists(css_path):
            css = CSS(filename=css_path)
        
        # Generate PDF bytes
        # WeasyPrint will automatically fetch online images (http/https URLs)
        pdf_bytes = BytesIO()
        html.write_pdf(pdf_bytes, stylesheets=[css] if css else None)
        pdf_bytes.seek(0)
        
        return pdf_bytes
