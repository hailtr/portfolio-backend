"""Replace the Upwork/Payless-merged experience with the locked Data Architect — Contract entry."""
from datetime import date
from backend.app import app
from backend import db
from backend.models.experience import Experience


EN_DESC = """- Cut <strong>$60K/month</strong> from client's data stack by replacing Workato orchestration with Airflow and eliminating full-refresh ETL with CDC — the root driver of their Snowflake bill
- Rebuilt the analytics layer as a <strong>medallion lakehouse on S3 + ClickHouse</strong>: Hive-partitioned Parquet, ClickPipes ingestion, ReplacingMergeTree tables + materialized views, dbt-managed transformations and schema migrations, and ClickHouse projections for query acceleration
- Collapsed <strong>1,200 Workato recipes + 124 Snowflake stored procedures</strong> into <strong>10 Airflow DAGs</strong> (~50 tasks each), replacing an unmaintainable orchestration sprawl with a unified, observable pipeline
- Migrated <strong>~1,350 data objects</strong> from Snowflake to ClickHouse across the full medallion stack — ~1,000 bronze (ERP), ~200 silver (warehouse), ~150 gold (marts) — <strong>in ~5 days</strong> using Python + LLM tooling I built for dialect translation, DDL generation, and error debugging"""

ES_DESC = """- Reducción de <strong>$60K/mes</strong> en el stack de datos del cliente: reemplazo de orquestación Workato por Airflow y eliminación de ETL full-refresh por CDC — causa raíz del descontrol del gasto en Snowflake
- Reconstrucción de la capa analítica como <strong>lakehouse medallion sobre S3 + ClickHouse</strong>: Parquet particionado (Hive), ingesta con ClickPipes, tablas ReplacingMergeTree + vistas materializadas, transformaciones y migraciones de esquema con dbt, y proyecciones de ClickHouse para aceleración de consultas
- Consolidación de <strong>1.200 recipes de Workato + 124 stored procedures de Snowflake</strong> en <strong>10 DAGs de Airflow</strong> (~50 tareas cada uno), sustituyendo una orquestación insostenible por un pipeline unificado y observable
- Migración de <strong>~1.350 objetos de datos</strong> de Snowflake a ClickHouse a lo largo del stack medallion completo — ~1.000 bronze (ERP), ~200 silver (warehouse), ~150 gold (marts) — <strong>en ~5 días</strong> usando herramientas Python + LLM que construí para traducción de dialecto, generación de DDL y depuración de errores"""


with app.app_context():
    exp = Experience.query.filter_by(slug="upwork-senior-data-engineer").first()
    if not exp:
        print("ERROR: 'upwork-senior-data-engineer' slug not found")
        raise SystemExit(1)

    print(f"BEFORE: slug={exp.slug}, company={exp.company}, "
          f"dates={exp.start_date}..{exp.end_date}, current={exp.current}")

    # Update experience columns
    exp.slug = "us-retail-data-architect-contract"
    exp.company = "US Retail Client (Contract)"
    exp.location = "Remote"
    exp.start_date = date(2025, 12, 1)
    exp.end_date = date(2026, 2, 28)
    exp.current = False

    # Update translations
    for trans in exp.translations:
        if trans.lang == "en":
            trans.title = "US Retail Client (Contract)"
            trans.subtitle = "Data Architect"
            trans.description = EN_DESC
        elif trans.lang == "es":
            trans.title = "Cliente Retail EE.UU. (Contrato)"
            trans.subtitle = "Arquitecto de Datos"
            trans.description = ES_DESC

    db.session.commit()

    print(f"AFTER:  slug={exp.slug}, company={exp.company}, "
          f"dates={exp.start_date}..{exp.end_date}, current={exp.current}")
    print("Translations updated for: en, es")

    # Invalidate CV caches so the next render reflects changes
    try:
        from backend.services.cv_cache import invalidate_all_cv_cache
        invalidate_all_cv_cache()
        print("CV caches invalidated")
    except Exception as e:
        print(f"(cache invalidation skipped: {e})")
