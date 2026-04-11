"""Update profile role, tagline, and bio — fix the busted numbers, own the contractor identity."""
from backend.app import app
from backend import db
from backend.models.profile import Profile


EN_ROLE = "Senior Data Engineer"
EN_TAGLINE = "Streaming pipelines, lakehouse architectures, and Microsoft data platforms"
EN_BIO = (
    "Senior data engineer, independent. I take on the messes nobody else wants — "
    "undocumented ERPs, out-of-control Snowflake bills, orchestration sprawls built "
    "by people long gone. I work fast, meet clients wherever they're already running "
    "(AWS, Azure, GCP), and ship platforms teams can run without me. "
    "Stack I live in: ClickHouse, Airflow, dbt, Redpanda, Microsoft Fabric."
)

ES_ROLE = "Ingeniero de Datos Senior"
ES_TAGLINE = "Pipelines de streaming, arquitecturas lakehouse y plataformas de datos Microsoft"
ES_BIO = (
    "Ingeniero de datos senior, independiente. Me hago cargo de los desastres que nadie "
    "más quiere — ERPs sin documentar, facturas de Snowflake descontroladas, marañas de "
    "orquestación construidas por gente que se fue hace años. Trabajo rápido, en la nube "
    "donde el cliente ya esté (AWS, Azure, GCP), y entrego plataformas que los equipos "
    "pueden mantener sin mí. Stack con el que vivo: ClickHouse, Airflow, dbt, Redpanda, "
    "Microsoft Fabric."
)


with app.app_context():
    profile = Profile.query.first()
    if not profile:
        print("ERROR: Profile not found")
        raise SystemExit(1)

    print(f"Profile: {profile.name}")
    for trans in profile.translations:
        print(f"\nBEFORE [{trans.lang}]:")
        print(f"  role:    {trans.role}")
        print(f"  tagline: {trans.tagline}")
        print(f"  bio:     {trans.bio[:120] if trans.bio else '(empty)'}...")

    for trans in profile.translations:
        if trans.lang == "en":
            trans.role = EN_ROLE
            trans.tagline = EN_TAGLINE
            trans.bio = EN_BIO
        elif trans.lang == "es":
            trans.role = ES_ROLE
            trans.tagline = ES_TAGLINE
            trans.bio = ES_BIO

    db.session.commit()

    # Verify
    for trans in profile.translations:
        print(f"\nAFTER [{trans.lang}]:")
        print(f"  role:    {trans.role}")
        print(f"  tagline: {trans.tagline}")
        print(f"  bio:     {trans.bio}")

    # Invalidate CV caches
    try:
        from backend.services.cv_cache import invalidate_all_cv_cache
        invalidate_all_cv_cache()
        print("\nCV caches invalidated")
    except Exception as e:
        print(f"(cache invalidation skipped: {e})")
