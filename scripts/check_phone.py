"""Check current phone stored in Profile.location JSON."""
import json
from backend.app import app
from backend.models.profile import Profile


with app.app_context():
    profile = Profile.query.first()
    if not profile:
        print("No profile found")
    else:
        print(f"Profile: {profile.name}")
        print(f"Location JSON: {json.dumps(profile.location, ensure_ascii=False, indent=2)}")
