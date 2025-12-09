"""
Quick PDF generation test script.
Run inside Docker: docker run --rm -v ${PWD}:/app portfolio-backend python scripts/test_pdf_generation.py
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_pdf_generation():
    """Test PDF generation with mock data"""
    print("=" * 60)
    print("PDF Generation Test")
    print("=" * 60)
    
    # Check WeasyPrint availability
    try:
        from weasyprint import HTML
        print("✅ WeasyPrint is available")
    except Exception as e:
        print(f"❌ WeasyPrint not available: {e}")
        return False
    
    # Check CSS file
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    css_path = os.path.join(backend_dir, "backend", "static", "styles", "cv.css")
    
    if os.path.exists(css_path):
        print(f"✅ CSS file exists: {css_path}")
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        print(f"   CSS size: {len(css_content)} bytes")
    else:
        print(f"❌ CSS file NOT found: {css_path}")
        return False
    
    # Create minimal test HTML with your CV structure
    test_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>CV Test</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            {css_content}
        </style>
    </head>
    <body class="cv-mode">
        <div class="cv-container">
            <aside class="cv-sidebar">
                <div class="profile-section">
                    <h1 class="name">Test Name</h1>
                    <h2 class="role">Test Role</h2>
                </div>
                <div class="sidebar-section">
                    <h3 class="section-title">Skills</h3>
                    <div class="skill-tags">
                        <span class="skill-tag">Python</span>
                        <span class="skill-tag">Flask</span>
                    </div>
                </div>
            </aside>
            <main class="cv-main">
                <section class="main-section">
                    <h3 class="section-title">Professional Profile</h3>
                    <p class="summary-text">This is a test summary with <strong>bold text</strong>.</p>
                </section>
                <section class="main-section">
                    <h3 class="section-title">Work Experience</h3>
                    <div class="timeline-item">
                        <div class="timeline-header">
                            <h4 class="position">Software Engineer</h4>
                            <span class="date">2020 - Present</span>
                        </div>
                        <div class="company-name">Test Company</div>
                        <p class="job-summary">Test description with HTML:</p>
                        <ul class="job-highlights">
                            <li>First accomplishment</li>
                            <li>Second accomplishment</li>
                        </ul>
                    </div>
                </section>
            </main>
        </div>
    </body>
    </html>
    """
    
    print("\n📄 Generating PDF...")
    try:
        from io import BytesIO
        html = HTML(string=test_html, base_url=backend_dir)
        pdf_bytes = BytesIO()
        html.write_pdf(pdf_bytes)
        pdf_bytes.seek(0)
        pdf_size = len(pdf_bytes.getvalue())
        print(f"✅ PDF generated successfully! Size: {pdf_size} bytes")
        
        # Save to file for inspection
        output_path = os.path.join(backend_dir, "test_cv.pdf")
        with open(output_path, 'wb') as f:
            f.write(pdf_bytes.getvalue())
        print(f"📁 PDF saved to: {output_path}")
        
        return True
        
    except Exception as e:
        import traceback
        print(f"❌ PDF generation failed: {e}")
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = test_pdf_generation()
    sys.exit(0 if success else 1)
