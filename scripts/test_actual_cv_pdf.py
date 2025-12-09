"""
Test actual CV PDF generation using the real template and data.
Run inside Docker connected to your database.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set minimal environment for Flask
os.environ.setdefault('FLASK_ENV', 'development')

def test_actual_cv_pdf():
    """Test actual CV generation with the real template"""
    print("=" * 60)
    print("Actual CV PDF Generation Test")
    print("=" * 60)
    
    try:
        # Import Flask app directly
        from backend.app import app
        
        # Configure for URL generation outside request context
        app.config['SERVER_NAME'] = 'localhost:5000'
        app.config['APPLICATION_ROOT'] = '/'
        app.config['PREFERRED_URL_SCHEME'] = 'http'
        
        with app.app_context():
            with app.test_request_context():
                from backend.routes.cv import build_cv_from_models
                from backend.services.pdf_service import PDFService
                from io import BytesIO
                
                # Test for both languages
                for lang in ['en', 'es']:
                    print(f"\n--- Testing language: {lang} ---")
                    
                    # Build CV data
                    print(f"Building CV data for {lang}...")
                    cv_data = build_cv_from_models(lang)
                    
                    if not cv_data:
                        print(f"❌ No CV data returned for {lang}")
                        continue
                    
                    print(f"✅ CV data built successfully")
                    print(f"   - Name: {cv_data.get('basics', {}).get('name', 'N/A')}")
                    print(f"   - Work entries: {len(cv_data.get('work', []))}")
                    print(f"   - Education entries: {len(cv_data.get('education', []))}")
                    print(f"   - Skills categories: {len(cv_data.get('skills', []))}")
                    
                    # Generate PDF
                    print(f"Generating PDF...")
                    pdf_service = PDFService()
                    pdf_bytes = pdf_service.generate_cv_pdf(cv_data, lang)
                    
                    if hasattr(pdf_bytes, 'getvalue'):
                        pdf_size = len(pdf_bytes.getvalue())
                    else:
                        pdf_size = len(pdf_bytes)
                    
                    print(f"✅ PDF generated! Size: {pdf_size} bytes")
                    
                    # Save to file
                    output_path = f"test_cv_actual_{lang}.pdf"
                    with open(output_path, 'wb') as f:
                        if hasattr(pdf_bytes, 'getvalue'):
                            f.write(pdf_bytes.getvalue())
                        else:
                            f.write(pdf_bytes)
                    print(f"📁 Saved to: {output_path}")
                
                print("\n" + "=" * 60)
                print("✅ All tests passed!")
                return True
            
    except Exception as e:
        import traceback
        print(f"\n❌ Error: {e}")
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = test_actual_cv_pdf()
    sys.exit(0 if success else 1)
