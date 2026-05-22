from pathlib import Path

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.database.connection import db
from app.models import Application, Certificate, Reference, Vacancy
from app.services.analytics_service import AnalyticsService
from app.services.cv_service import CVService
from app.services.gemini_service import GeminiService
from app.utils.helpers import utcnow
from app.utils.security import role_required

student_bp = Blueprint("student", __name__, url_prefix="/student")


def _cv_folder() -> Path:
    return Path(current_app.config["CV_UPLOAD_FOLDER"])


@student_bp.route("/dashboard")
@login_required
@role_required("student")
def dashboard():
    stats = AnalyticsService.student_dashboard(current_user)
    return render_template("student_dashboard.html", stats=stats)


@student_bp.route("/cv", methods=["GET", "POST"])
@login_required
@role_required("student")
def upload_cv():
    if request.method == "POST":
        stored, err = CVService.save_upload(
            _cv_folder(),
            current_user.id,
            request.files.get("cv_file"),
        )
        if err:
            flash(err, "error")
            return redirect(url_for("student.upload_cv"))

        file_path = _cv_folder() / stored
        text = CVService.extract_text(file_path)
        if len(text.strip()) < 30:
            flash(
                "Could not read enough text from the file. Try PDF or TXT with selectable text.",
                "error",
            )
            return redirect(url_for("student.upload_cv"))

        analysis = GeminiService.analyze_cv(text)
        current_user.cv_filename = stored
        current_user.cv_uploaded_at = utcnow()
        current_user.cv_analysis = analysis
        current_user.skills = analysis.get("skills", [])
        db.session.commit()

        flash("CV analyzed by AI. Your skill dashboard is ready.", "success")
        return redirect(url_for("student.dashboard"))

    return render_template(
        "upload_cv.html",
        user=current_user,
        has_cv=current_user.has_cv,
    )


@student_bp.route("/profile", methods=["GET", "POST"])
@login_required
@role_required("student")
def profile():
    if request.method == "POST":
        if request.form.get("form_type") == "cv_reanalyze" and current_user.cv_filename:
            file_path = _cv_folder() / current_user.cv_filename
            if file_path.exists():
                text = CVService.extract_text(file_path)
                analysis = GeminiService.analyze_cv(text)
                current_user.cv_analysis = analysis
                current_user.skills = analysis.get("skills", [])
                current_user.cv_uploaded_at = utcnow()
                db.session.commit()
                flash("CV re-analyzed. Dashboard updated.", "success")
                return redirect(url_for("student.dashboard"))
        else:
            current_user.full_name = request.form.get("full_name", current_user.full_name)
            current_user.bio = request.form.get("bio")
            current_user.department = request.form.get("department")
            db.session.commit()
            flash("Profile updated.", "success")
    return render_template("profile.html", user=current_user)


@student_bp.route("/certificates")
@login_required
@role_required("student")
def certificates():
    items = Certificate.query.filter_by(user_id=current_user.id).all()
    return render_template("certificates.html", certificates=items)


@student_bp.route("/references")
@login_required
@role_required("student")
def references():
    items = Reference.query.filter_by(student_id=current_user.id).all()
    return render_template("references.html", references=items)


@student_bp.route("/vacancies")
@login_required
@role_required("student")
def vacancies():
    active = Vacancy.query.filter_by(is_active=True).order_by(Vacancy.created_at.desc()).all()
    applied_ids = {
        a.vacancy_id for a in Application.query.filter_by(student_id=current_user.id).all()
    }
    return render_template(
        "vacancies.html",
        vacancies=active,
        applied_ids=applied_ids,
        role="student",
    )


@student_bp.route("/vacancies/<int:vacancy_id>/apply", methods=["POST"])
@login_required
@role_required("student")
def apply(vacancy_id):
    if not current_user.skills:
        flash("Upload your CV first so AI can build your verified skill profile.", "error")
        return redirect(url_for("student.upload_cv"))
    vacancy = Vacancy.query.get_or_404(vacancy_id)
    existing = Application.query.filter_by(
        student_id=current_user.id, vacancy_id=vacancy_id
    ).first()
    if existing:
        flash("You already applied to this vacancy.", "error")
        return redirect(url_for("student.vacancies"))
    score = GeminiService.match_score(
        current_user.skills,
        vacancy.required_skills,
        current_user.gpa or 0,
        vacancy.min_gpa or 0,
    )
    app = Application(
        student_id=current_user.id,
        vacancy_id=vacancy_id,
        match_score=score,
        status="pending",
    )
    db.session.add(app)
    db.session.commit()
    flash(f"Applied successfully. Match score: {score}%", "success")
    return redirect(url_for("student.vacancies"))