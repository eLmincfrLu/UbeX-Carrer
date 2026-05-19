from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.database.connection import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, index=True)
    university = db.Column(db.String(120))
    department = db.Column(db.String(120))
    bio = db.Column(db.Text)
    gpa = db.Column(db.Float, default=0.0)
    skills_json = db.Column(db.Text, default="[]")
    verified = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    certificates = db.relationship("Certificate", backref="owner", lazy=True)
    applications = db.relationship("Application", backref="student", lazy=True)
    references = db.relationship(
        "Reference",
        foreign_keys="Reference.student_id",
        backref="student",
        lazy=True,
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def skills(self) -> list[dict]:
        import json

        try:
            data = json.loads(self.skills_json or "[]")
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

    @skills.setter
    def skills(self, value: list[dict]) -> None:
        import json

        self.skills_json = json.dumps(value)