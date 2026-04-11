"""Rewrite the Austranet experience: close the 15% loop, add ASP.NET backup bullet, drop AZ-900/GRC padding."""
from datetime import date
from backend.app import app
from backend import db
from backend.models.experience import Experience


EN_DESC = """- Built a <strong>Python + Azure Functions</strong> pipeline automating the Azure cloud inventory for a Microsoft Silver Partner: cataloged <strong>300+ assets across subscriptions</strong>, routed findings to resource owners, and triggered decommissioning of the majority of ~15% flagged as idle
- Built and shipped automated backup tooling for an internal <strong>ASP.NET</strong> application backed by <strong>50+ databases across on-prem SQL Server and Azure SQL</strong>, reverse-engineered from scratch with zero internal documentation"""

ES_DESC = """- Construcción de un pipeline en <strong>Python + Azure Functions</strong> que automatiza el inventario cloud de Azure para un Microsoft Silver Partner: catalogación de <strong>300+ recursos a través de subscripciones</strong>, ruteo de hallazgos a sus dueños correspondientes, y desmantelamiento de la mayoría del ~15% marcado como ocioso
- Desarrollo y entrega de herramientas de respaldo automatizado para una aplicación interna en <strong>ASP.NET</strong> sustentada por <strong>50+ bases de datos entre SQL Server on-prem y Azure SQL</strong>, trabajo de ingeniería inversa partiendo desde cero sin documentación interna"""


with app.app_context():
    exp = Experience.query.filter_by(slug="austranet-infra-data").first()
    if not exp:
        exp = Experience.query.filter(Experience.slug.like("austranet%")).first()
    if not exp:
        print("ERROR: Austranet experience not found")
        raise SystemExit(1)

    print(f"BEFORE: slug={exp.slug}, company={exp.company}, "
          f"dates={exp.start_date}..{exp.end_date}, current={exp.current}")

    # Update experience columns
    exp.slug = "austranet-infra-data-engineer"
    exp.company = "Austranet"
    exp.location = "Hybrid, Santiago, Chile"
    exp.start_date = date(2023, 8, 1)
    exp.end_date = date(2023, 11, 1)
    exp.current = False

    # Update translations
    for trans in exp.translations:
        if trans.lang == "en":
            trans.title = "Austranet"
            trans.subtitle = "Infrastructure & Data Engineer"
            trans.description = EN_DESC
        elif trans.lang == "es":
            trans.title = "Austranet"
            trans.subtitle = "Ingeniero de Infraestructura y Datos"
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
