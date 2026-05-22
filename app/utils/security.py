import re
from functools import wraps

from flask import abort
from flask_login import current_user

ALLOWED_EMAIL_DOMAINS = (
    "edu.az",
    "university.edu.az",
    "ubex.local",
)

ROLE_DASHBOARD = {
    "student": "student.dashboard",
    "teacher": "teacher.dashboard",
    "university": "university.dashboard",
    "partner": "partner.dashboard",
}


def is_university_email(email: str) -> bool:
    if not email or "@" not in email:
        return False
    domain = email.split("@", 1)[1].lower()
    return any(domain == d or domain.endswith("." + d) for d in ALLOWED_EMAIL_DOMAINS)


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role not in roles:
                abort(403)
            return view(*args, **kwargs)

        return wrapped

    return decorator


def parse_skills(raw: str | None) -> list[str]:
    if not raw:
        return []
    parts = re.split(r"[,;|]", raw)
    return [p.strip() for p in parts if p.strip()]