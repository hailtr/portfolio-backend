"""
PDF generation service for CV/Resume.

Uses WeasyPrint for server-side PDF generation.
WeasyPrint works perfectly on Railway (Linux) - no Windows fallback needed.
"""

from io import BytesIO
import os
import re

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
        from flask import render_template
        html_string = render_template(
            "cv.html", cv_data=cv_data, lang=lang, profile_img_abs_path=profile_img_url
        )

        # Load and inject CSS directly into HTML to avoid file path issues
        # This is critical for production environments where WeasyPrint can't resolve Flask's url_for()
        if os.path.exists(css_path):
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            # Use minimal font weights for smaller PDF (was 300,400,500,600,700 = ~1MB)
            # Only load 400 (regular) and 700 (bold) = much smaller
            font_import = "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');\n"
            css_content = font_import + css_content
            
            # Inject CSS inline by replacing the link tag or appending to head
            # Try multiple patterns to catch different renderings of url_for
            # Pattern 1: Match any link tag to cv.css
            html_string = re.sub(
                r'<link[^>]*href="[^"]*cv\.css"[^>]*>',
                f'<style>{css_content}</style>',
                html_string
            )
            # If no replacement occurred (pattern didn't match), inject before </head>
            if '<style>' not in html_string:
                html_string = html_string.replace('</head>', f'<style>{css_content}</style></head>')

        # Generate PDF - no need for separate stylesheet since CSS is now inline
        html = HTML(string=html_string, base_url=backend_dir)

        # Generate PDF bytes
        pdf_bytes = BytesIO()
        html.write_pdf(pdf_bytes)
        pdf_bytes.seek(0)

        return pdf_bytes

