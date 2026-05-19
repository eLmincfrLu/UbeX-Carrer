from app.database.connection import db


class Vacancy(db.Model):
    __tablename__ = "vacancies"

    id = db.Column(db.Integer, primary_key=True)
    partner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(160), nullable=False)
    company_name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(80))
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.Text, default="")
    min_gpa = db.Column(db.Float, default=0.0)
    employment_type = db.Column(db.String(40), default="Full-time")
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    partner = db.relationship("User", backref="vacancies", foreign_keys=[partner_id])
    applications = db.relationship("Application", backref="vacancy", lazy=True)


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    vacancy_id = db.Column(db.Integer, db.ForeignKey("vacancies.id"), nullable=False)
    match_score = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(30), default="pending")
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    __table_args__ = (db.UniqueConstraint("student_id", "vacancy_id"),)