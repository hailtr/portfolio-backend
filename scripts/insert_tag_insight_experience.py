"""Insert the Tag Insight Upwork contract as a new experience entry."""
from datetime import date
from backend.app import app
from backend import db
from backend.models.experience import Experience, ExperienceTranslation


EN_DESC = """- Designed and built the full <strong>ClickHouse + Redpanda streaming architecture</strong> for a SaaS product automating <strong>data quality monitoring for retail e-commerce sites</strong> — owning the end-to-end flow from browser <strong>pixel events</strong> through <strong>Redpanda producers and consumers</strong> into a <strong>medallion lakehouse on ClickHouse</strong> (bronze / silver / gold)
- Modeled the silver and gold layers with <strong>ReplacingMergeTree</strong> tables and <strong>materialized views</strong> for dedup-on-write and incremental aggregation, keeping the customer-facing data quality dashboards backed by fresh marts without the cost of reprocessing raw pixel events at query time"""

ES_DESC = """- Diseño y construcción de la arquitectura completa de <strong>streaming en ClickHouse + Redpanda</strong> para un producto SaaS que automatiza el <strong>monitoreo de data quality en sitios de e-commerce retail</strong> — cubriendo el flujo end-to-end desde <strong>eventos de pixel</strong> del navegador, pasando por <strong>productores y consumidores en Redpanda</strong>, hasta un <strong>lakehouse medallion sobre ClickHouse</strong> (bronze / silver / gold)
- Modelado de las capas silver y gold con tablas <strong>ReplacingMergeTree</strong> y <strong>vistas materializadas</strong> para dedup-on-write y agregación incremental, manteniendo los dashboards de data quality del cliente respaldados por marts frescos sin el costo de reprocesar los eventos de pixel crudos en cada consulta"""


with app.app_context():
    # Guard against double-insert
    existing = Experience.query.filter_by(slug="tag-insight-data-architect").first()
    if existing:
        print(f"ERROR: Experience already exists: {existing.slug}")
        raise SystemExit(1)

    exp = Experience(
        slug="tag-insight-data-architect",
        company="Tag Insight (Upwork Contract)",
        location="Remote",
        start_date=date(2026, 2, 1),
        end_date=date(2026, 3, 31),
        current=False,
    )
    db.session.add(exp)
    db.session.flush()  # get exp.id

    en_trans = ExperienceTranslation(
        experience_id=exp.id,
        lang="en",
        title="Tag Insight (Upwork Contract)",
        subtitle="Data Architect",
        description=EN_DESC,
    )
    es_trans = ExperienceTranslation(
        experience_id=exp.id,
        lang="es",
        title="Tag Insight (Contrato Upwork)",
        subtitle="Arquitecto de Datos",
        description=ES_DESC,
    )
    db.session.add_all([en_trans, es_trans])
    db.session.commit()

    print(f"INSERTED: slug={exp.slug}, company={exp.company}, "
          f"dates={exp.start_date}..{exp.end_date}, current={exp.current}")

    # Verify full list
    all_exp = Experience.query.order_by(Experience.start_date.desc()).all()
    print(f"\nTotal experiences: {len(all_exp)}")
    for e in all_exp:
        print(f"  - {e.slug} ({e.start_date}..{e.end_date})")

    # Invalidate CV caches
    try:
        from backend.services.cv_cache import invalidate_all_cv_cache
        invalidate_all_cv_cache()
        print("\nCV caches invalidated")
    except Exception as e:
        print(f"(cache invalidation skipped: {e})")
