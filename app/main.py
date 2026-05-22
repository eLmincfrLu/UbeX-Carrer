import json
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_login import LoginManager, current_user

from app.database.connection import db
from app.models import (
    Application,
    Certificate,
    PartnerOrganization,
    Reference,
    User,
    Vacancy,
)
from app.routes.auth_routes import auth_bp
from app.routes.partner_routes import partner_bp
from app.routes.student_routes import student_bp
from app.routes.teacher_routes import teacher_bp
from app.routes.university_routes import university_bp
from app.routes.vacancy_routes import vacancy_bp
from app.services.analytics_service import AnalyticsService

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "database.db"
CV_UPLOAD_FOLDER = BASE_DIR / "uploads" / "cvs"


def ensure_user_cv_columns():
    from sqlalchemy import inspect, text

    inspector = inspect(db.engine)
    if "users" not in inspector.get_table_names():
        return
    existing = {c["name"] for c in inspector.get_columns("users")}
    alters = []
    if "cv_filename" not in existing:
        alters.append("ALTER TABLE users ADD COLUMN cv_filename VARCHAR(255)")
    if "cv_analysis_json" not in existing:
        alters.append("ALTER TABLE users ADD COLUMN cv_analysis_json TEXT")
    if "cv_uploaded_at" not in existing:
        alters.append("ALTER TABLE users ADD COLUMN cv_uploaded_at DATETIME")
    with db.engine.connect() as conn:
        for stmt in alters:
            conn.execute(text(stmt))
        conn.commit()


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "ubex-dev-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["CV_UPLOAD_FOLDER"] = str(CV_UPLOAD_FOLDER)
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(university_bp)
    app.register_blueprint(partner_bp)
    app.register_blueprint(vacancy_bp)

    @app.route("/api/analytics/chart")
    def analytics_chart():
        role = current_user.role if current_user.is_authenticated else "university"
        user = current_user if current_user.is_authenticated else None
        return jsonify(AnalyticsService.chart_payload(user, role))

    @app.cli.command("seed")
    def seed_command():
        seed_database()
        print("Database seeded.")

    with app.app_context():
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        CV_UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
        db.create_all()
        ensure_user_cv_columns()
        if User.query.count() == 0:
            seed_database()

    return app


def seed_database():
    demo_skills = json.dumps(
        [
            {"name": "Python", "score": 88, "verified": True},
            {"name": "Data Analysis", "score": 82, "verified": True},
            {"name": "SQL", "score": 76, "verified": True},
            {"name": "Machine Learning", "score": 71, "verified": True},
            {"name": "Project Management", "score": 65, "verified": True},
        ]
    )

    users = [
        ("student@university.edu.az", "student123", "Aysel Mammadova", "student", 3.7),
        ("teacher@university.edu.az", "teacher123", "Dr. Elvin Hasanov", "teacher", 0),
        ("admin@university.edu.az", "uni123", "UBEx University Admin", "university", 0),
        ("hr@partner.ubex.local", "partner123", "TechCorp HR", "partner", 0),
    ]
    for email, pwd, name, role, gpa in users:
        u = User(
            email=email,
            full_name=name,
            role=role,
            university="UBEx Pilot University",
            department="Computer Science" if role == "student" else "Faculty",
            gpa=gpa,
            skills_json=demo_skills if role == "student" else "[]",
            verified=True,
        )
        u.set_password(pwd)
        db.session.add(u)
    db.session.flush()

    student = User.query.filter_by(email="student@university.edu.az").first()
    if student:
        student.cv_filename = "demo_cv.pdf"
        student.cv_analysis = {
            "summary": "Demo: AI analyzed CV and extracted verified technical skills.",
            "strengths": ["Python", "Data Analysis", "SQL"],
            "skills": student.skills,
            "experience_years": 1,
            "suggested_roles": ["Junior Python Developer"],
        }
    teacher = User.query.filter_by(email="teacher@university.edu.az").first()
    partner = User.query.filter_by(email="hr@partner.ubex.local").first()

    db.session.add(
        Certificate(
            user_id=student.id,
            title="Python for Data Science",
            issuer="UBEx Academy",
            issue_date="2025-06",
            verified=True,
        )
    )
    db.session.add(
        Reference(
            student_id=student.id,
            author_id=teacher.id,
            content="Outstanding project delivery and strong analytical thinking.",
            rating=5,
        )
    )
    db.session.add_all(
        [
            PartnerOrganization(
                name="TechCorp",
                industry="Technology",
                website="https://example.com",
                description="Hiring verified junior talent via UBEx.",
            ),
            PartnerOrganization(
                name="DataFlow",
                industry="Analytics",
                website="https://example.com",
                description="Data-driven teams powered by university intelligence.",
            ),
        ]
    )
    vacancy = Vacancy(
        partner_id=partner.id,
        title="Junior Python Developer",
        company_name="TechCorp",
        location="Baku",
        description="Build data pipelines and internal tools with a verified skill profile.",
        required_skills="Python, SQL, Data Analysis",
        min_gpa=3.2,
        employment_type="Full-time",
        is_active=True,
    )
    db.session.add(vacancy)
    db.session.commit()


app = create_app()

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "1") == "1", port=5000)