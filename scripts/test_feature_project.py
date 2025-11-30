from backend import create_app, db
from backend.models.project import Project

app = create_app()

with app.app_context():
    project = Project.query.first()
    if project:
        print(f"Marking project '{project.slug}' as featured for CV...")
        project.is_featured_cv = True
        db.session.commit()
        print("Done.")
    else:
        print("No projects found.")
