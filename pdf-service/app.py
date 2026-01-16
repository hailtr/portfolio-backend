"""
PDF Generation Microservice for Google Cloud Run
Receives CV data and returns generated PDF bytes
"""

from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import os
from io import BytesIO

app = Flask(__name__)
CORS(app, origins=os.getenv("ALLOWED_ORIGINS", "*").split(","))

# Lazy load WeasyPrint (heavy import)
_weasyprint = None
def get_weasyprint():
    global _weasyprint
    if _weasyprint is None:
        from weasyprint import HTML
        _weasyprint = HTML
    return _weasyprint


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "pdf-generator"}), 200


@app.route("/generate", methods=["POST"])
def generate_pdf():
    """
    Generate PDF from CV data
    
    Expected JSON body:
    {
        "html_content": "<html>...</html>",
        "css_content": "...",  # Optional
        "lang": "en"
    }
    
    Returns: PDF bytes
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        html_content = data.get("html_content")
        css_content = data.get("css_content", "")
        lang = data.get("lang", "en")
        
        if not html_content:
            return jsonify({"error": "html_content is required"}), 400
        
        # If CSS is provided separately, inject it
        if css_content and "<style>" not in html_content:
            html_content = html_content.replace(
                "</head>",
                f"<style>{css_content}</style></head>"
            )
        
        # Generate PDF
        HTML = get_weasyprint()
        html = HTML(string=html_content)
        
        pdf_bytes = BytesIO()
        html.write_pdf(pdf_bytes)
        pdf_bytes.seek(0)
        
        # Generate filename
        filename = f"Rafael_Ortiz_CV_{'ES' if lang == 'es' else 'EN'}.pdf"
        
        return Response(
            pdf_bytes.getvalue(),
            mimetype="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Type": "application/pdf"
            }
        )
        
    except Exception as e:
        app.logger.error(f"PDF generation failed: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/generate-from-template", methods=["POST"])
def generate_from_template():
    """
    Generate PDF from CV data using built-in template
    
    Expected JSON body:
    {
        "cv_data": {...},  # Full CV data object
        "lang": "en"
    }
    """
    try:
        from jinja2 import Environment, BaseLoader
        
        data = request.json
        cv_data = data.get("cv_data")
        lang = data.get("lang", "en")
        template_html = data.get("template")  # Optional: custom template
        css = data.get("css", "")
        
        if not cv_data:
            return jsonify({"error": "cv_data is required"}), 400
        
        if not template_html:
            return jsonify({"error": "template is required"}), 400
        
        # Render template
        env = Environment(loader=BaseLoader())
        template = env.from_string(template_html)
        html_content = template.render(cv_data=cv_data, lang=lang)
        
        # Inject CSS
        if css:
            html_content = html_content.replace(
                "</head>",
                f"<style>{css}</style></head>"
            )
        
        # Generate PDF
        HTML = get_weasyprint()
        html = HTML(string=html_content)
        
        pdf_bytes = BytesIO()
        html.write_pdf(pdf_bytes)
        pdf_bytes.seek(0)
        
        filename = f"Rafael_Ortiz_CV_{'ES' if lang == 'es' else 'EN'}.pdf"
        
        return Response(
            pdf_bytes.getvalue(),
            mimetype="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Type": "application/pdf"
            }
        )
        
    except Exception as e:
        app.logger.error(f"PDF generation failed: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
