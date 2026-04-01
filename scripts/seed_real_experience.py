"""
Seed real experience data into the portfolio database.

Replaces placeholder data with 6 real experience entries,
adds Microsoft + Data skill categories, DuocUC education,
and updates the profile.

Usage:
    python scripts/seed_real_experience.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app, db
from backend.models.profile import Profile, ProfileTranslation
from backend.models.experience import Experience, ExperienceTranslation
from backend.models.education import Education, EducationTranslation, Course
from backend.models.skill import Skill, SkillTranslation, SkillCategory, SkillCategoryTranslation
from backend.models.tag import Tag
from datetime import date


# ============================================
# DATA DEFINITIONS
# ============================================

EXPERIENCES = [
    {
        "slug": "uc-chile-coordinator",
        "company": "Pontificia Universidad Católica de Chile",
        "location": "Remote",
        "start_date": date(2021, 3, 1),
        "end_date": date(2022, 7, 1),
        "current": False,
        "translations": {
            "es": {
                "title": "Pontificia Universidad Católica de Chile",
                "subtitle": "Asistente de Coordinación",
                "description": (
                    "- Apoyo en coordinación académica y administrativa para programas de educación continua\n"
                    "- Gestión de bases de datos de estudiantes y generación de reportes con Excel y herramientas internas\n"
                    "- Automatización de procesos repetitivos de seguimiento y comunicación\n"
                    "- Coordinación logística de actividades académicas en modalidad remota"
                ),
            },
            "en": {
                "title": "Pontificia Universidad Católica de Chile",
                "subtitle": "Coordinator Assistant",
                "description": (
                    "- Supported academic and administrative coordination for continuing education programs\n"
                    "- Managed student databases and generated reports using Excel and internal tools\n"
                    "- Automated repetitive tracking and communication processes\n"
                    "- Coordinated logistics for remote academic activities"
                ),
            },
        },
        "tags": ["Excel", "Data Management"],
    },
    {
        "slug": "walmart-bi-consultant",
        "company": "Walmart Ecosystem (via Teamcore/Ilabora)",
        "location": "On-site, Santiago, Chile",
        "start_date": date(2022, 8, 1),
        "end_date": date(2023, 7, 1),
        "current": False,
        "translations": {
            "es": {
                "title": "Ecosistema Walmart (vía Teamcore/Ilabora)",
                "subtitle": "Consultor BI",
                "description": (
                    "- Desarrollo de dashboards y reportes en Power BI para operaciones de retail a gran escala\n"
                    "- Modelado de datos con DAX y diseño de modelos dimensionales para métricas de ventas e inventario\n"
                    "- Integración de fuentes de datos múltiples usando Power Query y SQL Server\n"
                    "- Colaboración con equipos de negocio para traducir requerimientos en soluciones analíticas"
                ),
            },
            "en": {
                "title": "Walmart Ecosystem (via Teamcore/Ilabora)",
                "subtitle": "BI Consultant",
                "description": (
                    "- Developed dashboards and reports in Power BI for large-scale retail operations\n"
                    "- Data modeling with DAX and dimensional model design for sales and inventory metrics\n"
                    "- Integrated multiple data sources using Power Query and SQL Server\n"
                    "- Collaborated with business teams to translate requirements into analytical solutions"
                ),
            },
        },
        "tags": ["Power BI", "SQL Server", "DAX", "Power Query"],
    },
    {
        "slug": "austranet-infra-data",
        "company": "Austranet",
        "location": "Hybrid, Santiago, Chile",
        "start_date": date(2023, 8, 1),
        "end_date": date(2023, 11, 1),
        "current": False,
        "translations": {
            "es": {
                "title": "Austranet",
                "subtitle": "Ingeniero de Infraestructura y Datos",
                "description": (
                    "- Diseño e implementación de pipelines de datos en Azure Data Factory\n"
                    "- Administración de infraestructura cloud en Azure (VMs, networking, storage)\n"
                    "- Configuración de entornos de desarrollo y automatización con PowerShell y Terraform\n"
                    "- Monitoreo y optimización de recursos cloud para reducción de costos"
                ),
            },
            "en": {
                "title": "Austranet",
                "subtitle": "Infrastructure & Data Engineer",
                "description": (
                    "- Designed and implemented data pipelines in Azure Data Factory\n"
                    "- Managed cloud infrastructure on Azure (VMs, networking, storage)\n"
                    "- Set up development environments and automation with PowerShell and Terraform\n"
                    "- Monitored and optimized cloud resources for cost reduction"
                ),
            },
        },
        "tags": ["Azure", "Azure Data Factory", "Terraform", "PowerShell"],
    },
    {
        "slug": "thermogroup-mystic-data-engineer",
        "company": "Thermogroup / Mystic Brands",
        "location": "On-site, Venezuela",
        "start_date": date(2024, 1, 1),
        "end_date": date(2024, 12, 1),
        "current": False,
        "translations": {
            "es": {
                "title": "Thermogroup / Mystic Brands",
                "subtitle": "Ingeniero de Datos / BI",
                "description": (
                    "- Arquitectura e implementación de data warehouse en Microsoft Fabric y Synapse\n"
                    "- Desarrollo de modelos semánticos con DAX y Row-Level Security (RLS) en Power BI\n"
                    "- Creación de pipelines ETL/ELT con Azure Data Factory y Dataflows\n"
                    "- Automatización de procesos de negocio con Power Automate y Power Apps\n"
                    "- Diseño de portales internos con Power Pages para gestión operativa"
                ),
            },
            "en": {
                "title": "Thermogroup / Mystic Brands",
                "subtitle": "Data Engineer / BI",
                "description": (
                    "- Architected and implemented data warehouse on Microsoft Fabric and Synapse\n"
                    "- Developed semantic models with DAX and Row-Level Security (RLS) in Power BI\n"
                    "- Built ETL/ELT pipelines with Azure Data Factory and Dataflows\n"
                    "- Automated business processes with Power Automate and Power Apps\n"
                    "- Designed internal portals with Power Pages for operational management"
                ),
            },
        },
        "tags": ["Microsoft Fabric", "Power BI", "Synapse", "Power Automate", "Power Apps", "Azure Data Factory", "DAX"],
    },
    {
        "slug": "apextech-honor-solutions-architect",
        "company": "Apextech / HONOR",
        "location": "On-site, Venezuela",
        "start_date": date(2025, 1, 1),
        "end_date": date(2025, 11, 1),
        "current": False,
        "translations": {
            "es": {
                "title": "Apextech / HONOR",
                "subtitle": "Ingeniero de Datos / Arquitecto de Soluciones",
                "description": (
                    "- Diseño de arquitectura de datos end-to-end con Microsoft Fabric y Delta Lake\n"
                    "- Implementación de soluciones de analytics avanzadas con Synapse y Spark\n"
                    "- Desarrollo de Azure Functions y APIs para integración de sistemas\n"
                    "- Liderazgo técnico en migración de infraestructura legacy a cloud\n"
                    "- Optimización de costos cloud y gobernanza de datos"
                ),
            },
            "en": {
                "title": "Apextech / HONOR",
                "subtitle": "Data Engineer / Solutions Architect",
                "description": (
                    "- Designed end-to-end data architecture with Microsoft Fabric and Delta Lake\n"
                    "- Implemented advanced analytics solutions with Synapse and Spark\n"
                    "- Developed Azure Functions and APIs for system integration\n"
                    "- Technical leadership in legacy infrastructure migration to cloud\n"
                    "- Cloud cost optimization and data governance"
                ),
            },
        },
        "tags": ["Microsoft Fabric", "Delta Lake", "Synapse", "Azure Functions", "Spark"],
    },
    {
        "slug": "upwork-senior-data-engineer",
        "company": "Upwork (Freelance)",
        "location": "Remote",
        "start_date": date(2025, 12, 1),
        "end_date": None,
        "current": True,
        "translations": {
            "es": {
                "title": "Upwork (Freelance)",
                "subtitle": "Senior Data Engineer & Arquitecto FinOps",
                "description": (
                    "- Consultoría especializada en arquitectura de datos y optimización de costos cloud (FinOps)\n"
                    "- Diseño e implementación de pipelines de datos con Snowflake, BigQuery, dbt y Airflow\n"
                    "- Desarrollo de microservicios y APIs en Go y Python\n"
                    "- Soluciones multi-cloud: Azure (Fabric, ADF), AWS (S3, Lambda, Athena, VPC) y GCP (BigQuery)\n"
                    "- Automatización de infraestructura con Terraform y Docker"
                ),
            },
            "en": {
                "title": "Upwork (Freelance)",
                "subtitle": "Senior Data Engineer & FinOps Architect",
                "description": (
                    "- Specialized consulting in data architecture and cloud cost optimization (FinOps)\n"
                    "- Designed and implemented data pipelines with Snowflake, BigQuery, dbt, and Airflow\n"
                    "- Developed microservices and APIs in Go and Python\n"
                    "- Multi-cloud solutions: Azure (Fabric, ADF), AWS (S3, Lambda, Athena, VPC), and GCP (BigQuery)\n"
                    "- Infrastructure automation with Terraform and Docker"
                ),
            },
        },
        "tags": ["Go", "Python", "Snowflake", "dbt", "Airflow", "Terraform", "Docker", "AWS", "BigQuery"],
    },
]

DUOCUC_EDUCATION = {
    "slug": "duocuc-informatica",
    "institution": "DuocUC",
    "location": "Santiago, Chile",
    "start_date": date(2020, 3, 1),
    "end_date": date(2022, 12, 1),
    "current": False,
    "translations": {
        "es": {
            "title": "Ingeniería en Informática",
            "subtitle": "Analista Programador",
            "description": "Formación técnica en desarrollo de software, bases de datos y redes.",
        },
        "en": {
            "title": "Computer Science Engineering",
            "subtitle": "Software Analyst & Programmer",
            "description": "Technical training in software development, databases, and networking.",
        },
    },
}

# Microsoft skill category + skills
MICROSOFT_SKILLS = {
    "category": {
        "slug": "microsoft",
        "order": 2,
        "translations": {
            "es": "Microsoft",
            "en": "Microsoft",
        },
    },
    "skills": [
        {"slug": "microsoft-fabric", "name": "Microsoft Fabric", "proficiency": 90, "order": 0},
        {"slug": "power-bi", "name": "Power BI", "proficiency": 95, "order": 1},
        {"slug": "azure", "name": "Azure", "proficiency": 85, "order": 2},
        {"slug": "power-automate", "name": "Power Automate", "proficiency": 85, "order": 3},
        {"slug": "power-apps", "name": "Power Apps", "proficiency": 80, "order": 4},
        {"slug": "power-pages", "name": "Power Pages", "proficiency": 75, "order": 5},
        {"slug": "azure-data-factory", "name": "Azure Data Factory", "proficiency": 90, "order": 6},
        {"slug": "azure-functions", "name": "Azure Functions", "proficiency": 80, "order": 7},
        {"slug": "sql-server", "name": "SQL Server", "proficiency": 85, "order": 8},
        {"slug": "dax-rls", "name": "DAX / RLS", "proficiency": 90, "order": 9},
        {"slug": "synapse", "name": "Synapse", "proficiency": 85, "order": 10},
    ],
}

# Additional Data skills to add
DATA_SKILLS = {
    "category_slug": "data",  # Will look up or create
    "category": {
        "slug": "data",
        "order": 3,
        "translations": {
            "es": "Datos",
            "en": "Data",
        },
    },
    "skills": [
        {"slug": "snowflake", "name": "Snowflake", "proficiency": 80, "order": 0},
        {"slug": "clickhouse", "name": "ClickHouse", "proficiency": 70, "order": 1},
        {"slug": "delta-lake", "name": "Delta Lake", "proficiency": 85, "order": 2},
        {"slug": "dbt", "name": "dbt", "proficiency": 80, "order": 3},
        {"slug": "airflow", "name": "Airflow", "proficiency": 75, "order": 4},
        {"slug": "spark", "name": "Spark", "proficiency": 75, "order": 5},
        {"slug": "etl-elt", "name": "ETL / ELT", "proficiency": 90, "order": 6},
    ],
}

# AWS skills
AWS_SKILLS = {
    "category": {
        "slug": "aws",
        "order": 4,
        "translations": {
            "es": "AWS",
            "en": "AWS",
        },
    },
    "skills": [
        {"slug": "aws-s3", "name": "S3", "proficiency": 80, "order": 0},
        {"slug": "aws-lambda", "name": "Lambda", "proficiency": 75, "order": 1},
        {"slug": "aws-athena", "name": "Athena", "proficiency": 75, "order": 2},
        {"slug": "aws-vpc", "name": "VPC", "proficiency": 70, "order": 3},
        {"slug": "aws-glue", "name": "Glue", "proficiency": 70, "order": 4},
    ],
}

# GCP skills
GCP_SKILLS = {
    "category": {
        "slug": "gcp",
        "order": 5,
        "translations": {
            "es": "GCP",
            "en": "GCP",
        },
    },
    "skills": [
        {"slug": "bigquery", "name": "BigQuery", "proficiency": 80, "order": 0},
        {"slug": "cloud-storage", "name": "Cloud Storage", "proficiency": 70, "order": 1},
    ],
}

PROFILE_UPDATE = {
    "translations": {
        "es": {
            "role": "Senior Data Engineer & Arquitecto de Soluciones",
            "tagline": "Ingeniería de datos multi-cloud, soluciones Microsoft y backend en Go",
            "bio": (
                "Ingeniero de datos con experiencia en el ecosistema Microsoft (Fabric, Power BI, Azure, Synapse), "
                "AWS (S3, Lambda, Athena, VPC) y GCP (BigQuery). "
                "Stack moderno de datos: Snowflake, dbt, Airflow, Spark. "
                "Desarrollo backend en Go y Python, con enfoque en arquitectura de soluciones, "
                "optimización de costos cloud (FinOps) y automatización de infraestructura con Terraform y Docker."
            ),
        },
        "en": {
            "role": "Senior Data Engineer & Solutions Architect",
            "tagline": "Multi-cloud data engineering, Microsoft solutions, and Go backend",
            "bio": (
                "Data engineer experienced in the Microsoft ecosystem (Fabric, Power BI, Azure, Synapse), "
                "AWS (S3, Lambda, Athena, VPC), and GCP (BigQuery). "
                "Modern data stack: Snowflake, dbt, Airflow, Spark. "
                "Backend development in Go and Python, focused on solutions architecture, "
                "cloud cost optimization (FinOps), and infrastructure automation with Terraform and Docker."
            ),
        },
    },
}


# ============================================
# SEED FUNCTIONS
# ============================================


def seed_experiences():
    """Delete existing experiences and insert 6 real ones."""
    print("\n💼 Seeding experiences...")

    # Delete all existing experiences (cascade deletes translations + tags)
    count = Experience.query.count()
    if count > 0:
        Experience.query.delete()
        db.session.flush()
        print(f"   🗑️  Deleted {count} existing experience(s)")

    for data in EXPERIENCES:
        exp = Experience(
            slug=data["slug"],
            company=data["company"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            current=data["current"],
        )

        for lang, trans_data in data["translations"].items():
            trans = ExperienceTranslation(
                lang=lang,
                title=trans_data["title"],
                subtitle=trans_data["subtitle"],
                description=trans_data["description"],
            )
            exp.translations.append(trans)

        for tag_name in data.get("tags", []):
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                slug = tag_name.lower().replace(" ", "-").replace(".", "").replace("+", "plus").replace("/", "-")
                tag = Tag(name=tag_name, slug=slug)
            exp.tags.append(tag)

        db.session.add(exp)
        print(f"   ✅ {exp.company} — {data['translations']['en']['subtitle']}")

    print(f"   📊 Total: {len(EXPERIENCES)} experiences")


def seed_microsoft_skills():
    """Add Microsoft skill category and 11 skills."""
    print("\n🔷 Seeding Microsoft skills...")

    cat_data = MICROSOFT_SKILLS["category"]

    # Check if category already exists
    cat = SkillCategory.query.filter_by(slug=cat_data["slug"]).first()
    if not cat:
        cat = SkillCategory(slug=cat_data["slug"], order=cat_data["order"])
        for lang, name in cat_data["translations"].items():
            cat.translations.append(SkillCategoryTranslation(lang=lang, name=name))
        db.session.add(cat)
        db.session.flush()  # Get the ID
        print(f"   📁 Created category: {cat_data['slug']}")
    else:
        print(f"   📁 Category already exists: {cat_data['slug']}")

    for skill_data in MICROSOFT_SKILLS["skills"]:
        existing = Skill.query.filter_by(slug=skill_data["slug"]).first()
        if existing:
            print(f"   ⏭️  Skill exists: {skill_data['name']}")
            continue

        skill = Skill(
            slug=skill_data["slug"],
            proficiency=skill_data["proficiency"],
            order=skill_data["order"],
            category_id=cat.id,
            is_visible_cv=True,
            is_visible_portfolio=True,
        )
        for lang in ["es", "en"]:
            skill.translations.append(
                SkillTranslation(lang=lang, name=skill_data["name"])
            )
        db.session.add(skill)
        print(f"   ✅ {skill_data['name']}")

    print(f"   📊 Total Microsoft skills: {len(MICROSOFT_SKILLS['skills'])}")


def seed_data_skills():
    """Add Data skill category and 7 skills."""
    print("\n📊 Seeding Data skills...")

    cat_data = DATA_SKILLS["category"]

    # Check if category already exists
    cat = SkillCategory.query.filter_by(slug=cat_data["slug"]).first()
    if not cat:
        cat = SkillCategory(slug=cat_data["slug"], order=cat_data["order"])
        for lang, name in cat_data["translations"].items():
            cat.translations.append(SkillCategoryTranslation(lang=lang, name=name))
        db.session.add(cat)
        db.session.flush()
        print(f"   📁 Created category: {cat_data['slug']}")
    else:
        print(f"   📁 Category already exists: {cat_data['slug']}")

    for skill_data in DATA_SKILLS["skills"]:
        existing = Skill.query.filter_by(slug=skill_data["slug"]).first()
        if existing:
            print(f"   ⏭️  Skill exists: {skill_data['name']}")
            continue

        skill = Skill(
            slug=skill_data["slug"],
            proficiency=skill_data["proficiency"],
            order=skill_data["order"],
            category_id=cat.id,
            is_visible_cv=True,
            is_visible_portfolio=True,
        )
        for lang in ["es", "en"]:
            skill.translations.append(
                SkillTranslation(lang=lang, name=skill_data["name"])
            )
        db.session.add(skill)
        print(f"   ✅ {skill_data['name']}")

    print(f"   📊 Total Data skills: {len(DATA_SKILLS['skills'])}")


def seed_cloud_skills(skill_group, label):
    """Generic seeder for a skill group (AWS, GCP, etc.)."""
    print(f"\n☁️  Seeding {label} skills...")

    cat_data = skill_group["category"]

    cat = SkillCategory.query.filter_by(slug=cat_data["slug"]).first()
    if not cat:
        cat = SkillCategory(slug=cat_data["slug"], order=cat_data["order"])
        for lang, name in cat_data["translations"].items():
            cat.translations.append(SkillCategoryTranslation(lang=lang, name=name))
        db.session.add(cat)
        db.session.flush()
        print(f"   📁 Created category: {cat_data['slug']}")
    else:
        print(f"   📁 Category already exists: {cat_data['slug']}")

    for skill_data in skill_group["skills"]:
        existing = Skill.query.filter_by(slug=skill_data["slug"]).first()
        if existing:
            print(f"   ⏭️  Skill exists: {skill_data['name']}")
            continue

        skill = Skill(
            slug=skill_data["slug"],
            proficiency=skill_data["proficiency"],
            order=skill_data["order"],
            category_id=cat.id,
            is_visible_cv=True,
            is_visible_portfolio=True,
        )
        for lang in ["es", "en"]:
            skill.translations.append(
                SkillTranslation(lang=lang, name=skill_data["name"])
            )
        db.session.add(skill)
        print(f"   ✅ {skill_data['name']}")

    print(f"   📊 Total {label} skills: {len(skill_group['skills'])}")


def seed_education():
    """Add DuocUC education (keep existing entries)."""
    print("\n🎓 Seeding education...")

    data = DUOCUC_EDUCATION
    existing = Education.query.filter_by(slug=data["slug"]).first()
    if existing:
        print(f"   ⏭️  Already exists: {data['institution']}")
        return

    edu = Education(
        slug=data["slug"],
        institution=data["institution"],
        location=data["location"],
        start_date=data["start_date"],
        end_date=data["end_date"],
        current=data["current"],
    )

    for lang, trans_data in data["translations"].items():
        trans = EducationTranslation(
            lang=lang,
            title=trans_data["title"],
            subtitle=trans_data["subtitle"],
            description=trans_data["description"],
        )
        edu.translations.append(trans)

    db.session.add(edu)
    print(f"   ✅ {data['institution']} — {data['translations']['en']['title']}")


def update_profile():
    """Update profile role and bio."""
    print("\n📝 Updating profile...")

    profile = Profile.query.first()
    if not profile:
        print("   ⚠️  No profile found, skipping")
        return

    for trans in profile.translations:
        lang_data = PROFILE_UPDATE["translations"].get(trans.lang)
        if lang_data:
            trans.role = lang_data["role"]
            trans.tagline = lang_data["tagline"]
            trans.bio = lang_data["bio"]
            print(f"   ✅ Updated {trans.lang}: {lang_data['role']}")


def clear_cv_cache():
    """Clear CV cache so new data is reflected."""
    print("\n🧹 Clearing CV cache...")
    try:
        from backend.services.cv_cache import invalidate_all_cv_cache
        invalidate_all_cv_cache()
        print("   ✅ CV and PDF caches cleared")
    except Exception as e:
        print(f"   ⚠️  Could not clear cache: {e}")


# ============================================
# MAIN
# ============================================


def main():
    print("=" * 50)
    print("🌱 SEED: Real Experience & Skills")
    print("=" * 50)

    with app.app_context():
        try:
            seed_experiences()
            seed_microsoft_skills()
            seed_data_skills()
            seed_cloud_skills(AWS_SKILLS, "AWS")
            seed_cloud_skills(GCP_SKILLS, "GCP")
            seed_education()
            update_profile()

            db.session.commit()
            print("\n✅ All data committed successfully!")

            clear_cv_cache()

            print("\n🌐 Verify your data:")
            print("   Experiences: /api/experience")
            print("   Skills:      /api/skills")
            print("   Profile:     /api/profile")
            print("   CV:          /cv")
            print("=" * 50)

        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Seed failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    main()
