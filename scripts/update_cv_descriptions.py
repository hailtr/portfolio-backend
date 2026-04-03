"""
One-time script to update experience descriptions with metric-rich content.
Source: CV_Rafael_Ortiz_Microsoft.html baseline.

Usage: python scripts/update_cv_descriptions.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app
from backend import db
from backend.models.experience import ExperienceTranslation

# Map: experience slug -> {lang: new_description}
UPDATES = {
    "upwork-senior-data-engineer": {
        "en": (
            "- Cloud forensic analysis for US logistics: <strong>93% cost reduction (~$360k/year)</strong> via right-sizing, reserved instances, and architecture redesign\n"
            "- Built Python + LLM tools to refactor <strong>2,000+ SQL objects in 5 days</strong>, accelerating legacy-to-Snowflake migration by months\n"
            "- Migrated analytics to ClickHouse for EU client: query times from <strong>minutes to milliseconds</strong>; rebuilt pipeline with Airflow + dbt\n"
            "- Standardized IaC (Terraform, Docker) for fintech; implemented PII masking, encryption at rest, and ID obfuscation"
        ),
        "es": (
            "- Análisis forense cloud para logística en EE.UU.: <strong>93% de reducción de costos (~$360k/año)</strong> mediante right-sizing, instancias reservadas y rediseño de arquitectura\n"
            "- Herramientas Python + LLM para refactorizar <strong>2,000+ objetos SQL en 5 días</strong>, acelerando migración legacy a Snowflake por meses\n"
            "- Migración de analytics a ClickHouse para cliente EU: tiempos de consulta de <strong>minutos a milisegundos</strong>; pipeline reconstruido con Airflow + dbt\n"
            "- Estandarización de IaC (Terraform, Docker) para fintech; enmascaramiento PII, cifrado en reposo y ofuscación de IDs"
        ),
    },
    "apextech-honor-solutions-architect": {
        "en": (
            "- Migrated <strong>200 MB/month Excel master file</strong> (daily version conflicts, 3 business units) into Microsoft Fabric lakehouses via Azure Data Factory\n"
            "- Deployed Power BI with Row-Level Security for <strong>50+ stakeholders</strong>; replaced WhatsApp-based reporting with governed self-service analytics\n"
            "- ETL pipelines processing <strong>~500K records/day</strong> into Delta Lake; authored runbooks and trained staff for independent maintenance"
        ),
        "es": (
            "- Migración de <strong>archivo maestro Excel de 200 MB/mes</strong> (conflictos de versión diarios, 3 unidades de negocio) a lakehouses en Microsoft Fabric vía Azure Data Factory\n"
            "- Power BI con Row-Level Security para <strong>50+ stakeholders</strong>; reemplazo de reportes vía WhatsApp por analytics self-service gobernado\n"
            "- Pipelines ETL procesando <strong>~500K registros/día</strong> en Delta Lake; documentación de runbooks y capacitación al equipo para mantenimiento autónomo"
        ),
    },
    "thermogroup-mystic-data-engineer": {
        "en": (
            "- Enterprise Power BI with RLS and drill-through for <strong>8 departments</strong>; presented KPIs to C-level weekly\n"
            "- Power Automate: 12+ flows saving <strong>25 hrs/week</strong>; built Power Apps forms for field data capture; compliance pipelines reducing incidents by <strong>~70%</strong>\n"
            "- Administered SQL Server: <strong>40+ stored procedures</strong>, triggers, index tuning, permissions, maintenance plans"
        ),
        "es": (
            "- Power BI empresarial con RLS y drill-through para <strong>8 departamentos</strong>; presentación de KPIs a C-level semanalmente\n"
            "- Power Automate: 12+ flujos ahorrando <strong>25 hrs/semana</strong>; formularios Power Apps para captura en campo; pipelines de compliance reduciendo incidentes en <strong>~70%</strong>\n"
            "- Administración de SQL Server: <strong>40+ stored procedures</strong>, triggers, tuning de índices, permisos, planes de mantenimiento"
        ),
    },
    "austranet-infra-data": {
        "en": (
            "- Automated Azure cloud inventory with Python + Azure Functions: <strong>300+ assets</strong> cataloged, ~15% unused resources identified\n"
            "- Data governance in GRC: backups for <strong>50+ databases</strong>, disaster recovery, compliance auditing. Earned <strong>AZ-900</strong>"
        ),
        "es": (
            "- Inventario cloud Azure automatizado con Python + Azure Functions: <strong>300+ activos</strong> catalogados, ~15% recursos ociosos identificados\n"
            "- Gobernanza de datos en GRC: respaldos de <strong>50+ bases de datos</strong>, recuperación ante desastres, auditoría de compliance. Certificación <strong>AZ-900</strong>"
        ),
    },
    "walmart-bi-consultant": {
        "en": (
            "- Power BI dashboards for Walmart supply chain partners (<strong>150+ SKUs</strong>); migrated Excel to automated SQL Server pipelines\n"
            "- ETL from Profit Plus / SQL Server to Power BI; stored procedures, permissions management, database performance tuning"
        ),
        "es": (
            "- Dashboards Power BI para partners de cadena de suministro Walmart (<strong>150+ SKUs</strong>); migración de Excel a pipelines automatizados en SQL Server\n"
            "- ETL desde Profit Plus / SQL Server a Power BI; stored procedures, gestión de permisos, tuning de rendimiento de bases de datos"
        ),
    },
    "uc-chile-coordinator": {
        "en": (
            "- SharePoint + Power Query workflows (<strong>5,000+ records</strong>/semester); Power BI dashboards + Power Automate flows, <strong>~60%</strong> faster turnaround"
        ),
        "es": (
            "- Flujos SharePoint + Power Query (<strong>5,000+ registros</strong>/semestre); dashboards Power BI + flujos Power Automate, <strong>~60%</strong> más rápido en tiempos de respuesta"
        ),
    },
}


def main():
    with app.app_context():
        from backend.models.experience import Experience
        updated = 0

        for slug, langs in UPDATES.items():
            exp = Experience.query.filter_by(slug=slug).first()
            if not exp:
                print(f"  SKIP: experience '{slug}' not found")
                continue

            for lang, new_desc in langs.items():
                trans = next((t for t in exp.translations if t.lang == lang), None)
                if not trans:
                    print(f"  SKIP: no {lang} translation for '{slug}'")
                    continue

                trans.description = new_desc
                updated += 1
                print(f"  OK: {slug} [{lang}]")

        db.session.commit()
        print(f"\nDone. Updated {updated} translations.")


if __name__ == "__main__":
    main()
