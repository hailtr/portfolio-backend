"""Update profile role, tagline, and bio — fix the busted numbers, own the contractor identity."""
from backend.app import app
from backend import db
from backend.models.profile import Profile


EN_ROLE = "Senior Data Engineer"
EN_TAGLINE = "Streaming pipelines, lakehouse architectures, and Microsoft data platforms"
EN_BIO = (
    "Senior Data Engineer specializing in modernizing complex data architectures, "
    "optimizing cloud spend, and untangling intricate legacy pipelines. Whether working "
    "as an independent contractor or as part of a full-time team, I take deep ownership "
    "of my projects from architecture to deployment. I thrive in challenging environments—"
    "taming undocumented ERPs, restructuring Snowflake costs, and building scalable lakehouses. "
    "I work fast, meet clients wherever they are (AWS, Azure, GCP), and deliver robust platforms "
    "with a focus on maintainability. Stack I live in: ClickHouse, Airflow, dbt, Redpanda, "
    "Microsoft Fabric. Open to high-impact Senior/Lead roles or consulting contracts where I can "
    "build systems I am proud of alongside a collaborative team."
)

ES_ROLE = "Ingeniero de Datos Senior"
ES_TAGLINE = "Pipelines de streaming, arquitecturas lakehouse y plataformas de datos Microsoft"
ES_BIO = (
    "Ingeniero de Datos Senior especializado en modernizar arquitecturas complejas, "
    "optimizar costos en la nube y desenredar pipelines legacy. Ya sea como consultor "
    "independiente o como parte de un equipo full-time, asumo un profundo nivel de ownership "
    "en mis proyectos desde el diseño hasta el despliegue. Me destaco resolviendo problemas de "
    "alto impacto: domando ERPs sin documentar, reestructurando facturación de Snowflake y "
    "construyendo lakehouses escalables. Trabajo con agilidad, adaptándome a la nube de la "
    "empresa (AWS, Azure, GCP), y entrego plataformas robustas con un enfoque en la mantenibilidad. "
    "Stack con el que vivo: ClickHouse, Airflow, dbt, Redpanda, Microsoft Fabric. Abierto a roles "
    "Senior/Lead o contratos de consultoría donde pueda construir sistemas de los que me sienta "
    "orgulloso junto a un gran equipo."
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
