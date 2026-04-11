"""Dump CV rendered HTML + skills/contact raw data for layout debugging."""
from backend.app import app
from backend.routes.cv import build_cv_from_models


with app.app_context():
    for lang in ("en", "es"):
        cv = build_cv_from_models(lang)
        print("=" * 100)
        print(f"LANG: {lang}")
        print("=" * 100)

        print("\n--- BASICS ---")
        b = cv["basics"]
        print(f"  name:     {b['name']}")
        print(f"  label:    {b['label']}")
        print(f"  email:    {b['email']}")
        print(f"  phone:    {b['phone']}")
        print(f"  location: {b['location']}")
        print(f"  profiles:")
        for p in b["profiles"]:
            print(f"    - network={p['network']:<15} username={p['username']}")

        print(f"\n--- SKILLS ({len(cv['skills'])} categories) ---")
        for cat in cv["skills"]:
            items = cat.get("skill_items", [])
            names = [i["name"] for i in items]
            print(f"  [{cat['name']}]  ({len(items)} items)")
            print(f"     {', '.join(names)}")

        print(f"\n--- WORK ({len(cv['work'])} entries) ---")
        for j in cv["work"]:
            hl_count = len(j.get("highlights", []))
            print(f"  - {j['startDate']}..{j['endDate']:<12}  {j['position']:<35}  @  {j['company']}  ({hl_count} highlights)")

        print()

    # Now render the HTML through Flask test_client
    with app.test_client() as client:
        print("\n" + "=" * 100)
        print("RENDERED HTML SNIPPETS (EN)")
        print("=" * 100)
        resp = client.get("/cv?lang=en")
        html = resp.data.decode("utf-8")

        # Extract header block
        import re
        m = re.search(r'<header class="header">.*?</header>', html, re.DOTALL)
        if m:
            print("\n--- HEADER HTML ---")
            print(m.group(0))

        # Extract skills section
        m = re.search(r'<!-- SKILLS -->.*?</section>', html, re.DOTALL)
        if m:
            print("\n--- SKILLS HTML (first 1500 chars) ---")
            print(m.group(0)[:1500])
