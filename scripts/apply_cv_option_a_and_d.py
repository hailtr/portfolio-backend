"""Apply Option A (compress early career + independent study) + Option D (stack chips).

A. Rewrite Walmart / Austranet / Independent Study descriptions as single compact paragraphs.
D. Set clean stack chip tags for the 4 full-bullet experiences: Tag Insight, Payless (US retail),
   HONOR, Mystic Brands. Existing stale tag associations on those experiences are cleared first.
"""
from backend.app import app
from backend import db
from backend.models.experience import Experience, ExperienceTranslation
from backend.models.tag import Tag


# ============================================================
# CHIP TAG LISTS — 5 chips per experience, narrative order
# ============================================================
EXPERIENCE_TAGS = {
    "tag-insight-data-architect": [
        "ClickHouse", "Kafka", "Redpanda", "Medallion", "Materialized Views",
    ],
    "us-retail-data-architect-contract": [
        "Snowflake", "ClickHouse", "Airflow", "dbt", "S3",
    ],
    "honor-solutions-engineer": [
        "Microsoft Fabric", "Power BI", "DAX / RLS", "Flask", "PostgreSQL",
    ],
    "mystic-brands-data-engineer": [
        "SQL Server", "Power BI", "Power Query M", "Python", "Power Apps",
    ],
}


# ============================================================
# COMPRESSED ONE-LINER DESCRIPTIONS
# ============================================================
WALMART_EN = (
    "Stood up the first structured daily reporting cycle for Walmart Chile's pandemic "
    "last-mile delivery program (via logistics outsourcer) — "
    "<strong>Power BI</strong> + <strong>SQL Server</strong> star-schema pipelines "
    "tracking near-real-time stock for <strong>150+ critical SKUs</strong>, "
    "replacing the manual Excel extracts nobody was maintaining."
)
WALMART_ES = (
    "Estructuré el primer ciclo de reporting diario del programa de logística de última "
    "milla de Walmart Chile en pandemia (vía outsourcer) — pipelines en "
    "<strong>Power BI</strong> + modelo estrella en <strong>SQL Server</strong> "
    "monitoreando stock casi en tiempo real de <strong>150+ SKUs críticos</strong>, "
    "reemplazando las extracciones manuales en Excel que nadie mantenía."
)

AUSTRANET_EN = (
    "Shipped a <strong>Python + Azure Functions</strong> pipeline cataloging 300+ cloud "
    "assets across Azure SQL and on-prem SQL Server for a Microsoft Silver Partner, "
    "closing the ownership loop that drove decommissioning of the ~15% idle stack. "
    "Also reverse-engineered <strong>ASP.NET</strong> backup automation covering "
    "<strong>50+ databases</strong> with zero documentation."
)
AUSTRANET_ES = (
    "Implementé un pipeline en <strong>Python + Azure Functions</strong> catalogando "
    "300+ activos cloud entre Azure SQL y SQL Server on-prem para un Microsoft Silver "
    "Partner, cerrando el ciclo de ownership que llevó al decomisionado del ~15% de "
    "stack ocioso. Adicional: automaticé backups reverse-engineered para "
    "<strong>50+ bases de datos</strong> de una aplicación <strong>ASP.NET</strong> "
    "sin documentación."
)

INDEPENDENT_EN = (
    "Built the <strong>portfolio engine serving this CV</strong> from scratch — "
    "a full-stack <strong>Flask + SQLAlchemy + Jinja2</strong> application with "
    "<strong>WeasyPrint</strong> PDF generation, EN/ES translations, Redis-backed "
    "CV caching, and an admin panel. Hands-on <strong>Snowflake</strong> research "
    "in a self-provisioned sandbox primed the Snowflake → ClickHouse migration at "
    "the retail client contract later that year."
)
INDEPENDENT_ES = (
    "Construí el <strong>motor de portafolio que sirve este CV</strong> desde cero — "
    "aplicación full-stack en <strong>Flask + SQLAlchemy + Jinja2</strong> con "
    "generación de PDF vía <strong>WeasyPrint</strong>, traducciones EN/ES, caché de "
    "CV respaldado por Redis y panel de administración. Investigación hands-on de "
    "<strong>Snowflake</strong> en sandbox auto-provisionado que preparó la migración "
    "Snowflake → ClickHouse en el contrato retail más adelante ese mismo año."
)

COMPRESSED_DESCRIPTIONS = {
    "walmart-chile-bi-developer": (WALMART_EN, WALMART_ES),
    "austranet-infra-data-engineer": (AUSTRANET_EN, AUSTRANET_ES),
    "independent-study-2025": (INDEPENDENT_EN, INDEPENDENT_ES),
}


def slugify(name):
    return name.lower().replace(" ", "-").replace("/", "-").replace("--", "-").strip("-")


def get_or_create_tag(name):
    """Look up tag by name (case-sensitive); create if missing."""
    existing = Tag.query.filter_by(name=name).first()
    if existing:
        return existing
    slug = slugify(name)
    # Ensure slug uniqueness
    if Tag.query.filter_by(slug=slug).first():
        slug = f"{slug}-chip"
    t = Tag(name=name, slug=slug)
    db.session.add(t)
    db.session.flush()
    print(f"  CREATE tag: name={name!r} slug={slug!r}")
    return t


with app.app_context():
    # ============================================================
    # 1. Compress 3 experiences to single-paragraph summaries
    # ============================================================
    print("=" * 90)
    print("COMPRESS EXPERIENCES (Option A)")
    print("=" * 90)
    for slug, (en_desc, es_desc) in COMPRESSED_DESCRIPTIONS.items():
        exp = Experience.query.filter_by(slug=slug).first()
        if not exp:
            print(f"  SKIP: {slug} (not found)")
            continue
        print(f"\n  {slug}")
        for tr in exp.translations:
            if tr.lang == "en":
                tr.description = en_desc
                print(f"    EN: {en_desc[:90]}...")
            elif tr.lang == "es":
                tr.description = es_desc
                print(f"    ES: {es_desc[:90]}...")
        # Also clear any existing stack tags on compressed experiences
        # (they render compact — no chip row)
        if exp.tags:
            print(f"    clearing {len(exp.tags)} stale tags: {[t.name for t in exp.tags]}")
            exp.tags = []

    db.session.flush()

    # ============================================================
    # 2. Set clean stack chip tags for the 4 full-bullet experiences
    # ============================================================
    print("\n" + "=" * 90)
    print("STACK CHIPS (Option D)")
    print("=" * 90)
    for slug, tag_names in EXPERIENCE_TAGS.items():
        exp = Experience.query.filter_by(slug=slug).first()
        if not exp:
            print(f"  SKIP: {slug} (not found)")
            continue
        print(f"\n  {slug}")
        if exp.tags:
            print(f"    clearing {len(exp.tags)} old: {[t.name for t in exp.tags]}")
        new_tags = [get_or_create_tag(name) for name in tag_names]
        exp.tags = new_tags
        print(f"    setting: {[t.name for t in new_tags]}")

    db.session.commit()

    # ============================================================
    # VERIFY
    # ============================================================
    print("\n" + "=" * 90)
    print("AFTER")
    print("=" * 90)
    exps = Experience.query.order_by(Experience.start_date.desc()).all()
    for e in exps:
        has_full = any(
            any(ln.strip().startswith(("-", "*", "•", "·"))
                for ln in (tr.description or "").split("\n"))
            for tr in e.translations
        )
        mode = "FULL" if has_full else "COMPACT"
        tags_str = ", ".join(sorted(t.name for t in e.tags)) if e.tags else "(no chips)"
        print(f"  [{mode:<7}] {e.slug}")
        print(f"            chips: {tags_str}")

    # Invalidate caches
    try:
        from backend.services.cv_cache import invalidate_all_cv_cache
        invalidate_all_cv_cache()
        print("\nCV caches invalidated")
    except Exception as e:
        print(f"(cache invalidation skipped: {e})")
