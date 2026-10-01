import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.user import User
from app.core.config import settings
from app.core.security import get_password_hash

def seed_admin(db: Session = None):
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        admin_email = settings.FIRST_ADMIN_EMAIL
        existing = db.query(User).filter(User.email == admin_email).first()
        if not existing:
            admin = User(
                full_name=settings.FIRST_ADMIN_NAME,
                email=admin_email,
                password_hash=get_password_hash(settings.FIRST_ADMIN_PASSWORD),
                role="admin",
                is_active=True,
                is_email_verified=True,
                auth_provider="local"
            )
            db.add(admin)
            db.commit()
            print(f"Admin user seeded successfully: {admin_email}")
        else:
            # Ensure admin role and verified status and update password hash
            existing.role = "admin"
            existing.password_hash = get_password_hash(settings.FIRST_ADMIN_PASSWORD)
            existing.is_active = True
            existing.is_email_verified = True
            db.commit()
            print(f"Admin user updated: {admin_email} (status verified, password updated)")
    except Exception as e:
        db.rollback()
        print(f"Error seeding admin: {e}")
        raise
    finally:
        if close_db:
            db.close()

if __name__ == "__main__":
    seed_admin()
