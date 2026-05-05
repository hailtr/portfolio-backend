import sqlite3
import os

db_path = r"c:\Users\PC\Documents\Rafael\Portafolio\portfolio-backend\instance\portfolio.db"
if not os.path.exists(db_path):
    print("DB not found at", db_path)
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

english_bio = """Senior Data Engineer specializing in modernizing complex data architectures, optimizing cloud spend, and untangling intricate legacy pipelines. Whether working as an independent contractor or as part of a full-time team, I take deep ownership of my projects from architecture to deployment. I thrive in challenging environments—taming undocumented ERPs, restructuring Snowflake costs, and building scalable lakehouses. 

I work fast, meet clients wherever they are (AWS, Azure, GCP), and deliver robust platforms with a focus on maintainability. Stack I live in: ClickHouse, Airflow, dbt, Redpanda, Microsoft Fabric. Open to high-impact Senior/Lead roles or consulting contracts where I can build systems I am proud of alongside a collaborative team."""

spanish_bio = """Ingeniero de Datos Senior especializado en modernizar arquitecturas complejas, optimizar costos en la nube y desenredar pipelines legacy. Ya sea como consultor independiente o como parte de un equipo full-time, asumo un profundo nivel de ownership en mis proyectos desde el diseño hasta el despliegue. Me destaco resolviendo problemas de alto impacto: domando ERPs sin documentar, reestructurando facturación de Snowflake y construyendo lakehouses escalables.

Trabajo con agilidad, adaptándome a la nube de la empresa (AWS, Azure, GCP), y entrego plataformas robustas con un enfoque en la mantenibilidad. Stack con el que vivo: ClickHouse, Airflow, dbt, Redpanda, Microsoft Fabric. Abierto a roles Senior/Lead o contratos de consultoría donde pueda construir sistemas de los que me sienta orgulloso junto a un gran equipo."""

cursor.execute("UPDATE profile_translations SET bio = ? WHERE lang = 'en'", (english_bio,))
cursor.execute("UPDATE profile_translations SET bio = ? WHERE lang = 'es'", (spanish_bio,))

conn.commit()
print(f"Updated {cursor.rowcount} rows for spanish (if 1 it worked)")
conn.close()
