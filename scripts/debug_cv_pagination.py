"""Render CV PDFs locally and dump per-page content to find the orphan."""
import os
os.environ.pop("PDF_SERVICE_URL", None)  # force local WeasyPrint

from backend.app import app
from backend.routes.cv import build_cv_from_models
from backend.services.pdf_service import PDFService


def dump_pdf(path, label):
    import fitz
    doc = fitz.open(path)
    print(f"\n{'=' * 100}")
    print(f"{label}  |  {path}")
    print(f"pages: {len(doc)}")
    print(f"{'=' * 100}")
    for i, page in enumerate(doc, start=1):
        text = page.get_text("text")
        lines = [ln for ln in text.split("\n") if ln.strip()]
        print(f"\n--- PAGE {i}  ({len(lines)} non-empty lines) ---")
        print(f"  first 3: {lines[:3]}")
        print(f"  last  5: {lines[-5:]}")
        print(f"  total chars: {sum(len(l) for l in lines)}")
    doc.close()


with app.app_context():
    svc = PDFService()
    for lang in ("en", "es"):
        cv_data = build_cv_from_models(lang)
        print(f"\n### {lang.upper()} CONTENT METRICS ###")
        print(f"  experiences: {len(cv_data['work'])}")
        total_hl = sum(len(j.get('highlights', [])) for j in cv_data['work'])
        print(f"  total highlights: {total_hl}")
        print(f"  skills categories: {len(cv_data['skills'])}")
        total_skills = sum(len(s.get('skill_items', [])) for s in cv_data['skills'])
        print(f"  total skill items: {total_skills}")
        print(f"  education: {len(cv_data['education'])}")
        print(f"  certifications: {len(cv_data['certifications'])}")
        print(f"  languages: {len(cv_data['languages'])}")
        print(f"  summary length: {len(cv_data['basics'].get('summary', ''))}")

        pdf_bytes = svc.generate_cv_pdf(cv_data, lang)
        out = f"/tmp/cv_debug_{lang}.pdf"
        os.makedirs("/tmp", exist_ok=True)
        with open(out, "wb") as f:
            f.write(pdf_bytes.read())

        dump_pdf(out, f"CV {lang.upper()}")
