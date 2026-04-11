"""Insert the Jan–Jul 2025 independent study / R&D period as a new experience entry."""
from datetime import date
from backend.app import app
from backend import db
from backend.models.experience import Experience, ExperienceTranslation


EN_DESC = """- Built and shipped my <strong>portfolio engine</strong> from scratch as an end-to-end side project: a full-stack <strong>Flask + SQLAlchemy + Jinja2</strong> application with PDF generation via <strong>WeasyPrint</strong>, multi-language translations (EN/ES), a CV caching service, and an admin panel — the same app currently serving this CV
- Ran hands-on <strong>Snowflake research</strong> in a self-provisioned sandbox — query patterns, cost mechanics, orchestration trade-offs — building the baseline that made me effective during the <strong>Snowflake → ClickHouse migration</strong> at the retail client contract later that year"""

ES_DESC = """- Construcción y puesta en producción de mi <strong>motor de portafolio</strong> desde cero como side project end-to-end: aplicación full-stack en <strong>Flask + SQLAlchemy + Jinja2</strong> con generación de PDF vía <strong>WeasyPrint</strong>, traducciones multilenguaje (EN/ES), un servicio de caché de CV y un panel de administración — la misma aplicación que sirve este CV
- Investigación hands-on de <strong>Snowflake</strong> en un sandbox auto-provisionado — patrones de consulta, mecánica de costos, trade-offs de orquestación — construyendo la base que me hizo efectivo durante la <strong>migración Snowflake → ClickHouse</strong> en el contrato retail más adelante ese mismo año"""


with app.app_context():
    # Guard against double-insert
    existing = Experience.query.filter_by(slug="independent-study-2025").first()
    if existing:
        print(f"ERROR: Experience already exists: {existing.slug}")
        raise SystemExit(1)

    exp = Experience(
        slug="independent-study-2025",
        company="Independent Study & Technical R&D",
        location="Remote",
        start_date=date(2025, 1, 1),
        end_date=date(2025, 7, 31),
        current=False,
    )
    db.session.add(exp)
    db.session.flush()  # get exp.id

    en_trans = ExperienceTranslation(
        experience_id=exp.id,
        lang="en",
        title="Independent Study & Technical R&D",
        subtitle="Data Platform & Full-Stack Engineering",
        description=EN_DESC,
    )
    es_trans = ExperienceTranslation(
        experience_id=exp.id,
        lang="es",
        title="Estudio Independiente e I+D Técnica",
        subtitle="Plataformas de Datos e Ingeniería Full-Stack",
        description=ES_DESC,
    )
    db.session.add_all([en_trans, es_trans])
    db.session.commit()

    print(f"INSERTED: slug={exp.slug}, company={exp.company}, "
          f"dates={exp.start_date}..{exp.end_date}, current={exp.current}")

    # Verify full list in reverse chronological order
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
