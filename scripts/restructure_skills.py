"""Restructure skills into 5 clean categories: Microsoft & Azure, Data & Streaming, AWS, GCP, Core Engineering.

Removes duplication, drops un-defendable skills (Spark, Power Pages, Synapse, etc.),
renames verbose skill labels, and reorders everything.
"""
from backend.app import app
from backend import db
from backend.models.skill import Skill, SkillCategory, SkillCategoryTranslation, SkillTranslation


def get_cat(slug):
    return SkillCategory.query.filter_by(slug=slug).first()


def get_skill(slug):
    return Skill.query.filter_by(slug=slug).first()


def set_cat_translations(cat, en_name, es_name):
    existing = {t.lang: t for t in cat.translations}
    if "en" in existing:
        existing["en"].name = en_name
    else:
        db.session.add(SkillCategoryTranslation(category_id=cat.id, lang="en", name=en_name))
    if "es" in existing:
        existing["es"].name = es_name
    else:
        db.session.add(SkillCategoryTranslation(category_id=cat.id, lang="es", name=es_name))


def set_skill_translations(skill, en_name, es_name):
    existing = {t.lang: t for t in skill.translations}
    if "en" in existing:
        existing["en"].name = en_name
    else:
        db.session.add(SkillTranslation(skill_id=skill.id, lang="en", name=en_name, description=""))
    if "es" in existing:
        existing["es"].name = es_name
    else:
        db.session.add(SkillTranslation(skill_id=skill.id, lang="es", name=es_name, description=""))


def create_skill(slug, cat_id, order, en_name, es_name, proficiency=80):
    s = Skill(
        slug=slug,
        category_id=cat_id,
        order=order,
        proficiency=proficiency,
        is_visible_cv=True,
        is_visible_portfolio=True,
    )
    db.session.add(s)
    db.session.flush()
    set_skill_translations(s, en_name, es_name)
    print(f"  CREATE skill: {slug} ({en_name})")
    return s


with app.app_context():
    # ============================================================
    # 1. DELETE obsolete skills (drops + superseded duplicates)
    # ============================================================
    obsolete = [
        "power-pages",            # never in any experience bullet
        "synapse",                # superseded by Fabric in narrative
        "spark",                  # no Spark in any experience bullet
        "etl-elt",                # chip clutter, implied by rest
        "aws-s3-ec2-glue-lambda", # old catch-all pill, split into individual AWS chips
        "gcp",                    # old catch-all pill (skill, not category)
        "azure",                  # old catch-all pill, merged into Microsoft & Azure
        "aws-vpc",                # too vague for a CV chip
        "rest-api",               # implied by Flask/backend work
    ]
    for slug in obsolete:
        s = get_skill(slug)
        if s:
            print(f"  DELETE skill: {slug}")
            db.session.delete(s)
    db.session.flush()

    # ============================================================
    # 2. Microsoft (id=4) → Microsoft & Azure
    # ============================================================
    micro = get_cat("microsoft")
    assert micro, "category 'microsoft' missing"
    micro.slug = "microsoft-azure"
    micro.order = 1
    set_cat_translations(micro, "Microsoft & Azure", "Microsoft & Azure")

    micro_updates = [
        ("microsoft-fabric",    0, "Microsoft Fabric",    "Microsoft Fabric",    90),
        ("power-bi",            1, "Power BI",            "Power BI",            90),
        ("dax-rls",             2, "DAX / RLS",           "DAX / RLS",           85),
        # power-query-m slot=3 (created below)
        ("power-apps",          4, "Power Apps",          "Power Apps",          80),
        ("power-automate",      5, "Power Automate",      "Power Automate",      80),
        ("azure-data-factory",  6, "Azure Data Factory",  "Azure Data Factory",  80),
        ("azure-functions",     7, "Azure Functions",     "Azure Functions",     80),
        # azure-sql slot=8 (created below)
        ("sql-server",          9, "SQL Server",          "SQL Server",          85),
    ]
    for slug, order, en, es, prof in micro_updates:
        s = get_skill(slug)
        if s:
            s.order = order
            s.category_id = micro.id
            s.proficiency = prof
            set_skill_translations(s, en, es)

    if not get_skill("power-query-m"):
        create_skill("power-query-m", micro.id, 3, "Power Query M", "Power Query M", 85)
    if not get_skill("azure-sql"):
        create_skill("azure-sql", micro.id, 8, "Azure SQL", "Azure SQL", 80)

    # ============================================================
    # 3. Data (id=5) + Modern Data Stack (id=2) → Data & Streaming
    # ============================================================
    data_cat = get_cat("data")
    assert data_cat, "category 'data' missing"
    data_cat.slug = "data-streaming"
    data_cat.order = 2
    set_cat_translations(data_cat, "Data & Streaming", "Datos & Streaming")

    data_updates = [
        ("clickhouse",  0, "ClickHouse",         "ClickHouse",         90),
        ("snowflake",   1, "Snowflake",          "Snowflake",          85),
        ("redpanda",    2, "Redpanda (Kafka)",   "Redpanda (Kafka)",   85),
        ("airflow",     3, "Airflow",            "Airflow",            80),
        ("dbt",         4, "dbt",                "dbt",                85),
        ("delta-lake",  5, "Delta Lake",         "Delta Lake",         75),
        ("postgresql",  6, "PostgreSQL",         "PostgreSQL",         90),
        ("redis",       7, "Redis",              "Redis",              80),
    ]
    for slug, order, en, es, prof in data_updates:
        s = get_skill(slug)
        if s:
            s.order = order
            s.category_id = data_cat.id
            s.proficiency = prof
            set_skill_translations(s, en, es)

    # ============================================================
    # 4. AWS (id=6) — keep, reorder, add EC2
    # ============================================================
    aws = get_cat("aws")
    assert aws, "category 'aws' missing"
    aws.order = 3
    set_cat_translations(aws, "AWS", "AWS")

    aws_updates = [
        ("aws-s3",     0, "S3",     "S3",     85),
        ("aws-lambda", 1, "Lambda", "Lambda", 80),
        ("aws-glue",   2, "Glue",   "Glue",   75),
        ("aws-athena", 3, "Athena", "Athena", 75),
    ]
    for slug, order, en, es, prof in aws_updates:
        s = get_skill(slug)
        if s:
            s.order = order
            s.category_id = aws.id
            s.proficiency = prof
            set_skill_translations(s, en, es)

    if not get_skill("aws-ec2"):
        create_skill("aws-ec2", aws.id, 4, "EC2", "EC2", 75)

    # ============================================================
    # 5. GCP (id=7) — keep, add Cloud Run + Pub/Sub, reorder
    # ============================================================
    gcp = get_cat("gcp")
    assert gcp, "category 'gcp' missing"
    gcp.order = 4
    set_cat_translations(gcp, "GCP", "GCP")

    if not get_skill("gcp-cloud-run"):
        create_skill("gcp-cloud-run", gcp.id, 0, "Cloud Run", "Cloud Run", 85)

    cs = get_skill("cloud-storage")
    if cs:
        cs.order = 1
        cs.category_id = gcp.id
        cs.proficiency = 80
        set_skill_translations(cs, "Cloud Storage", "Cloud Storage")

    bq = get_skill("bigquery")
    if bq:
        bq.order = 2
        bq.category_id = gcp.id
        bq.proficiency = 80
        set_skill_translations(bq, "BigQuery", "BigQuery")

    if not get_skill("gcp-pubsub"):
        create_skill("gcp-pubsub", gcp.id, 3, "Pub/Sub", "Pub/Sub", 75)

    # ============================================================
    # 6. Core Engineering (id=3) — absorb docker/terraform/linux, drop rest-api
    # ============================================================
    core = get_cat("core-engineering")
    assert core, "category 'core-engineering' missing"
    core.order = 5
    set_cat_translations(core, "Core Engineering", "Ingeniería de Software")

    core_updates = [
        ("go-concurrency", 0, "Go",                                "Go",                                75),
        ("python",         1, "Python (Flask, Pandas, AsyncIO)",   "Python (Flask, Pandas, AsyncIO)",   90),
        ("sql-modeling",   2, "SQL",                               "SQL",                               90),
        ("docker",         3, "Docker",                            "Docker",                            85),
        ("terraform",      4, "Terraform",                         "Terraform",                         70),
        ("git-cicd",       5, "Git / CI/CD",                       "Git / CI/CD",                       85),
        ("linux",          6, "Linux / Bash",                      "Linux / Bash",                      80),
        ("pytest",         7, "Pytest",                            "Pytest",                            75),
    ]
    for slug, order, en, es, prof in core_updates:
        s = get_skill(slug)
        if s:
            s.order = order
            s.category_id = core.id
            s.proficiency = prof
            set_skill_translations(s, en, es)

    db.session.flush()

    # ============================================================
    # 7. DELETE obsolete categories (modern-data-stack, cloud-infrastructure)
    # ============================================================
    for cat_slug in ("modern-data-stack", "cloud-infrastructure"):
        c = get_cat(cat_slug)
        if c:
            # Safety: any skills still pointing here get deleted
            remaining = list(c.skills)
            if remaining:
                print(f"  WARNING: {cat_slug} still has orphans: {[s.slug for s in remaining]}")
                for s in remaining:
                    print(f"  DELETE orphan skill: {s.slug}")
                    db.session.delete(s)
                db.session.flush()
            print(f"  DELETE category: {cat_slug}")
            db.session.delete(c)

    db.session.commit()

    # ============================================================
    # VERIFY
    # ============================================================
    print("\n" + "=" * 90)
    print("AFTER")
    print("=" * 90)
    cats = SkillCategory.query.order_by(SkillCategory.order).all()
    total = 0
    for c in cats:
        en = next((t.name for t in c.translations if t.lang == "en"), "?")
        items = sorted(c.skills, key=lambda x: x.order)
        total += len(items)
        print(f"\n[{c.order}] {en} ({c.slug})  — {len(items)} items")
        for s in items:
            en_name = next((t.name for t in s.translations if t.lang == "en"), "?")
            key = "*" if (s.proficiency or 0) >= 80 else " "
            print(f"    {key} {s.order}: {en_name}  (prof={s.proficiency})")
    print(f"\nTOTAL: {total} skills across {len(cats)} categories")

    # Invalidate caches
    try:
        from backend.services.cv_cache import invalidate_all_cv_cache
        invalidate_all_cv_cache()
        print("\nCV caches invalidated")
    except Exception as e:
        print(f"(cache invalidation skipped: {e})")
