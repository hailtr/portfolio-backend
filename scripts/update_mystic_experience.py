"""Full reframe of the Thermogroup/Mystic Brands experience as Mystic Brands C.A. — Data Engineer."""
from datetime import date
from backend.app import app
from backend import db
from backend.models.experience import Experience


EN_DESC = """- Hired to audit invoices manually; shipped a <strong>Python listener</strong> watching the ERP's internal message drop folder every 5 minutes, rewriting flat-file payloads on the fly to patch a tax-flag bug in <strong>ProfitPlus ERP</strong> (invoice vs. credit note) that was breaking SKU pricing — eliminating the manual job I was hired for and transparently fixing several downstream ERP metrics and reports as a side effect
- Reverse-engineered <strong>ProfitPlus ERP's</strong> undocumented SQL Server schema to build a <strong>centralized Power BI semantic model</strong> for the reporting layer; authored all ingestion in <strong>Power Query M</strong> unifying ERP tables with external Excel sources on a daily refresh cadence
- Shipped three production Power BI dashboards on the semantic model — sales (primary), near-real-time inventory, and logistics — replacing an Excel reporting cycle that previously took <strong>days</strong> to produce with <strong>same-day numbers</strong> for 5 departments
- Later engaged as external consultant to deliver a <strong>field-promoter performance review</strong> covering ~50 promoters: <strong>Power Apps</strong> form for daily inventory submissions, <strong>Power Automate</strong> pipeline landing the data into the existing Power BI semantic model, and a new dashboard tracking sales, SKUs, and revenue per promoter"""

ES_DESC = """- Contratado para auditar facturas manualmente; entregué un <strong>listener en Python</strong> monitoreando la carpeta interna de mensajes del ERP cada 5 minutos, reescribiendo payloads en formato plano al vuelo para parchar un bug de bandera fiscal en <strong>ProfitPlus ERP</strong> (factura vs. nota de crédito) que rompía el cálculo de precios de SKUs — eliminando el trabajo manual para el que fui contratado y corrigiendo de paso varias métricas y reportes internos del ERP como efecto colateral
- Ingeniería inversa del <strong>schema SQL Server no documentado de ProfitPlus ERP</strong> para construir un <strong>modelo semántico centralizado de Power BI</strong> para la capa de reportería; toda la ingesta en <strong>Power Query M</strong> unificando tablas del ERP con fuentes Excel externas con refresh diario
- Entregué tres dashboards de Power BI en producción sobre el modelo semántico — ventas (principal), inventarios near-real-time y logística — reemplazando un ciclo de reportería en Excel que antes tomaba <strong>días</strong> en producirse, ahora con entregas el <strong>mismo día</strong> para 5 departamentos
- Posteriormente contratado como consultor externo para entregar un <strong>sistema de evaluación de desempeño para promotores en campo</strong> cubriendo ~50 promotores: formulario en <strong>Power Apps</strong> para envío diario de inventarios, pipeline en <strong>Power Automate</strong> que lleva los datos al modelo semántico de Power BI existente, y un nuevo dashboard midiendo ventas, SKUs y facturación por promotor"""


with app.app_context():
    exp = Experience.query.filter_by(slug="thermogroup-mystic-data-engineer").first()
    if not exp:
        exp = Experience.query.filter(Experience.slug.like("thermogroup%")).first()
    if not exp:
        exp = Experience.query.filter(Experience.slug.like("mystic%")).first()
    if not exp:
        print("ERROR: Mystic/Thermogroup experience not found")
        raise SystemExit(1)

    print(f"BEFORE: slug={exp.slug}, company={exp.company}, "
          f"dates={exp.start_date}..{exp.end_date}, current={exp.current}")

    # Update experience columns
    exp.slug = "mystic-brands-data-engineer"
    exp.company = "Mystic Brands C.A."
    exp.location = "On-site, Venezuela"
    exp.start_date = date(2024, 1, 1)
    exp.end_date = date(2024, 12, 1)
    exp.current = False

    # Update translations
    for trans in exp.translations:
        if trans.lang == "en":
            trans.title = "Mystic Brands C.A."
            trans.subtitle = "Data Engineer"
            trans.description = EN_DESC
        elif trans.lang == "es":
            trans.title = "Mystic Brands C.A."
            trans.subtitle = "Ingeniero de Datos"
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
