"""Optional local demo data. Set DEMO_ADMIN_PASSWORD before running."""
import os
from passlib.context import CryptContext
from backend.models import User, Prompt, PromptVersion, UserRole, PromptStatus, SessionLocal, Base, engine

Base.metadata.create_all(bind=engine)
pwd = os.getenv("DEMO_ADMIN_PASSWORD")
if not pwd or len(pwd) < 12:
    raise SystemExit("Set DEMO_ADMIN_PASSWORD to at least 12 characters before seeding")
with SessionLocal() as db:
    if db.query(User).filter(User.username == "demo_admin").first():
        print("Demo admin already exists; no changes made")
    else:
        user = User(username="demo_admin", hashed_password=CryptContext(schemes=["bcrypt"]).hash(pwd), role=UserRole.ADMIN.value)
        db.add(user)
        db.flush()
        prompt = Prompt(name="Summarize Email", description="Summarize an email concisely")
        db.add(prompt)
        db.flush()
        db.add(PromptVersion(prompt_id=prompt.id, version_number=1, text="Summarize this email in three bullet points.", status=PromptStatus.APPROVED.value, created_by_id=user.id))
        db.commit()
        print("Created demo_admin and sample prompt")
