"""Rewrite the Apextech/HONOR experience with corrected dates and locked content."""
from datetime import date
from backend.app import app
from backend import db
from backend.models.experience import Experience


EN_DESC = """- Replaced a weekly manual consolidation workflow — staff merging data from the client's custom ERP, WhatsApp group messages, and a legacy ERP into a <strong>200 MB Excel master file</strong> — with a <strong>Microsoft Fabric lakehouse</strong> (Delta tables, Data Pipelines) covering 3 business units and <strong>1,200+ stores</strong>
- Built the <strong>Power BI semantic model with Row-Level Security</strong> across promoter, supervisor, and manager tiers; delivered the HR bonus-payment report consolidating sales across all 1,200 stores, replacing a manual WhatsApp → ERP → Excel cycle
- Built a <strong>Flask + PostgreSQL + SQLAlchemy</strong> internal web app (TailwindCSS, role-based auth, approval workflows, audit trails) formalizing supervisor-driven store provisioning and staff assignment; its operational data fed the Fabric lakehouse as a governed upstream source, closing the loop between operational systems and analytics"""

ES_DESC = """- Reemplazo del proceso manual semanal de consolidación — staff fusionando datos del ERP propio del cliente, mensajes de grupos de WhatsApp y un ERP legado en un <strong>archivo maestro de Excel de 200 MB</strong> — por un <strong>lakehouse en Microsoft Fabric</strong> (tablas Delta, Data Pipelines) cubriendo 3 unidades de negocio y <strong>más de 1.200 tiendas</strong>
- Construcción del <strong>modelo semántico de Power BI con Row-Level Security</strong> para promotores, supervisores y gerentes; entrega del reporte de bonos de RR.HH. consolidando ventas en las 1.200 tiendas, reemplazando el ciclo manual WhatsApp → ERP → Excel
- Desarrollo de una aplicación web interna en <strong>Flask + PostgreSQL + SQLAlchemy</strong> (TailwindCSS, autenticación por rol, flujos de aprobación, trazabilidad) que formaliza el aprovisionamiento de tiendas y asignación de personal por parte de supervisores; sus datos operacionales alimentan el lakehouse de Fabric como fuente gobernada, cerrando el ciclo entre los sistemas operacionales y la capa analítica"""


with app.app_context():
    exp = Experience.query.filter_by(slug="apextech-honor-solutions-architect").first()
    if not exp:
        # Try alternate slug spellings
        exp = Experience.query.filter(Experience.slug.like("apextech%")).first()
    if not exp:
        print("ERROR: Apextech experience not found")
        raise SystemExit(1)

    print(f"BEFORE: slug={exp.slug}, company={exp.company}, "
          f"dates={exp.start_date}..{exp.end_date}, current={exp.current}")

    # Update experience columns
    exp.slug = "honor-solutions-engineer"
    exp.company = "HONOR"
    exp.location = "Venezuela (on-site)"
    exp.start_date = date(2025, 8, 1)
    exp.end_date = date(2025, 10, 31)
    exp.current = False

    # Update translations
    for trans in exp.translations:
        if trans.lang == "en":
            trans.title = "HONOR"
            trans.subtitle = "Solutions Engineer"
            trans.description = EN_DESC
        elif trans.lang == "es":
            trans.title = "HONOR"
            trans.subtitle = "Solutions Engineer"
            trans.description = ES_DESC

    db.session.commit()

    print(f"AFTER:  slug={exp.slug}, company={exp.company}, "
          f"dates={exp.start_date}..{exp.end_date}, current={exp.current}")
    print("Translations updated for: en, es")

    # Invalidate CV caches
    try:
        from backend.services.cv_cache import invalidate_all_cv_cache
        invalidate_all_cv_cache()
        print("CV caches invalidated")
    except Exception as e:
        print(f"(cache invalidation skipped: {e})")
