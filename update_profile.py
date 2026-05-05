import os
from dotenv import load_dotenv
load_dotenv()

from backend.app import app
from backend import db
from backend.models.profile import Profile, ProfileTranslation

english_bio = """Senior Data Engineer specializing in modernizing complex data architectures, optimizing cloud spend, and untangling intricate legacy pipelines. Whether working as an independent contractor or as part of a full-time team, I take deep ownership of my projects from architecture to deployment. I thrive in challenging environments—taming undocumented ERPs, restructuring Snowflake costs, and building scalable lakehouses. 

I work fast, meet clients wherever they are (AWS, Azure, GCP), and deliver robust platforms with a focus on maintainability. Stack I live in: ClickHouse, Airflow, dbt, Redpanda, Microsoft Fabric. Open to high-impact Senior/Lead roles or consulting contracts where I can build systems I am proud of alongside a collaborative team."""

spanish_bio = """Ingeniero de Datos Senior especializado en modernizar arquitecturas complejas, optimizar costos en la nube y desenredar pipelines legacy. Ya sea como consultor independiente o como parte de un equipo full-time, asumo un profundo nivel de ownership en mis proyectos desde el diseño hasta el despliegue. Me destaco resolviendo problemas de alto impacto: domando ERPs sin documentar, reestructurando facturación de Snowflake y construyendo lakehouses escalables.

Trabajo con agilidad, adaptándome a la nube de la empresa (AWS, Azure, GCP), y entrego plataformas robustas con un enfoque en la mantenibilidad. Stack con el que vivo: ClickHouse, Airflow, dbt, Redpanda, Microsoft Fabric. Abierto a roles Senior/Lead o contratos de consultoría donde pueda construir sistemas de los que me sienta orgulloso junto a un gran equipo."""

with app.app_context():
    profiles = Profile.query.all()
    if not profiles:
        print("No profiles found")
    else:
        profile = profiles[0]
        print(f"Updating profile: {profile.name}")
        for translation in profile.translations:
            if translation.lang == 'en':
                translation.bio = english_bio
                print("Updated English bio")
            elif translation.lang == 'es':
                translation.bio = spanish_bio
                print("Updated Spanish bio")
        
        db.session.commit()
        print("Database commit successful.")
