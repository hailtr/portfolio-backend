"""Rewrite the Walmart experience: drop fake Teamcore/Ilabora attribution, reframe SKU context, honest built-from-zero story."""
from datetime import date
from backend.app import app
from backend import db
from backend.models.experience import Experience


EN_DESC = """- Built Power BI dashboards monitoring <strong>near-real-time stock</strong> for the <strong>150+ critical SKUs</strong> a pandemic-era Walmart Chile last-mile delivery operation actually ran on — the high-turnover items the whole logistics flow depended on — across warehouses and delivery routes
- Stood up the first structured daily reporting cycle for the program (none existed before): replaced manual Excel pulls with <strong>SQL Server pipelines feeding a star-schema model</strong> for sales, inventory, and delivery KPIs, moving the operation from no daily visibility to <strong>same-day numbers</strong>"""

ES_DESC = """- Construcción de dashboards en Power BI para monitoreo de stock en <strong>near-real-time</strong> de los <strong>150+ SKUs críticos</strong> sobre los que operaba una operación de last-mile delivery de Walmart Chile en plena pandemia — los ítems de alta rotación de los que dependía todo el flujo logístico — cubriendo bodegas y rutas de despacho
- Puesta en marcha del primer ciclo estructurado de reportería diaria del programa (no existía ninguno antes): reemplazo de extracciones manuales en Excel por <strong>pipelines sobre SQL Server alimentando un modelo star-schema</strong> para KPIs de ventas, inventario y entregas, llevando la operación de cero visibilidad diaria a <strong>números del mismo día</strong>"""


with app.app_context():
    exp = Experience.query.filter_by(slug="walmart-bi-consultant").first()
    if not exp:
        exp = Experience.query.filter(Experience.slug.like("walmart%")).first()
    if not exp:
        print("ERROR: Walmart experience not found")
        raise SystemExit(1)

    print(f"BEFORE: slug={exp.slug}, company={exp.company}, "
          f"dates={exp.start_date}..{exp.end_date}, current={exp.current}")

    # Update experience columns
    exp.slug = "walmart-chile-bi-developer"
    exp.company = "Walmart Chile (via logistics outsourcer)"
    exp.location = "On-site, Santiago, Chile"
    exp.start_date = date(2022, 8, 1)
    exp.end_date = date(2023, 7, 1)
    exp.current = False

    # Update translations
    for trans in exp.translations:
        if trans.lang == "en":
            trans.title = "Walmart Chile (via logistics outsourcer)"
            trans.subtitle = "BI Developer"
            trans.description = EN_DESC
        elif trans.lang == "es":
            trans.title = "Walmart Chile (vía outsourcer logístico)"
            trans.subtitle = "BI Developer"
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
