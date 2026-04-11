"""Dump profile data for review."""
from backend.app import app
from backend.models.profile import Profile

with app.app_context():
    profile = Profile.query.first()
    if not profile:
        print("NO PROFILE FOUND")
        raise SystemExit(1)

    print("=" * 100)
    print(f"NAME:         {profile.name}")
    print(f"EMAIL:        {profile.email}")
    print(f"LOCATION:     {profile.location}")
    print(f"SOCIAL LINKS: {profile.social_links}")
    print(f"AVATAR:       {getattr(profile, 'avatar_url', '(n/a)')}")
    print("=" * 100)

    for trans in profile.translations:
        print(f"\n--- [{trans.lang}] ---")
        print(f"ROLE:    {trans.role}")
        print(f"TAGLINE: {trans.tagline}")
        print(f"BIO:")
        if trans.bio:
            for line in trans.bio.split("\n"):
                print(f"    {line}")
        else:
            print("    (empty)")
        print(f"BIO LENGTH: {len(trans.bio) if trans.bio else 0} chars")
    print("\n" + "=" * 100)
