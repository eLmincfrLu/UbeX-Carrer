from app.database.connection import db
from app.models import User
from app.utils.security import is_university_email


class AuthService:
    @staticmethod
    def register(email: str, password: str, full_name: str, role: str, **extra) -> tuple[User | None, str | None]:
        email = (email or "").strip().lower()
        if not is_university_email(email) and role in ("student", "teacher", "university"):
            return None, "Only official university email domains are allowed for this role."
        if User.query.filter_by(email=email).first():
            return None, "An account with this email already exists."
        if role not in ("student", "teacher", "university", "partner"):
            return None, "Invalid role selected."

        user = User(
            email=email,
            full_name=full_name.strip(),
            role=role,
            university=extra.get("university"),
            department=extra.get("department"),
            gpa=float(extra.get("gpa") or 0),
            verified=True,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user, None

    @staticmethod
    def authenticate(email: str, password: str) -> tuple[User | None, str | None]:
        user = User.query.filter_by(email=(email or "").strip().lower()).first()
        if not user or not user.check_password(password):
            return None, "Invalid email or password."
        return user, None