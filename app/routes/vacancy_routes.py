from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.database.connection import db
from app.models import Application, Vacancy
from app.utils.security import role_required

vacancy_bp = Blueprint("vacancy", __name__, url_prefix="/vacancies")


@vacancy_bp.route("/")
@login_required
def list_vacancies():
    if current_user.role == "partner":
        items = Vacancy.query.filter_by(partner_id=current_user.id).order_by(
            Vacancy.created_at.desc()
        ).all()
    else:
        items = Vacancy.query.filter_by(is_active=True).all()
    return render_template("vacancies.html", vacancies=items, role=current_user.role)


@vacancy_bp.route("/add", methods=["GET", "POST"])
@login_required
@role_required("partner")
def add_vacancy():
    if request.method == "POST":
        v = Vacancy(
            partner_id=current_user.id,
            title=request.form.get("title"),
            company_name=request.form.get("company_name") or current_user.full_name,
            location=request.form.get("location"),
            description=request.form.get("description"),
            required_skills=request.form.get("required_skills"),
            min_gpa=float(request.form.get("min_gpa") or 0),
            employment_type=request.form.get("employment_type") or "Full-time",
            is_active=True,
        )
        db.session.add(v)
        db.session.commit()
        flash("Vacancy published.", "success")
        return redirect(url_for("vacancy.list_vacancies"))
    return render_template("add_vacancy.html")


@vacancy_bp.route("/<int:vacancy_id>/applications")
@login_required
@role_required("partner")
def applications(vacancy_id):
    vacancy = Vacancy.query.get_or_404(vacancy_id)
    if vacancy.partner_id != current_user.id:
        flash("Access denied.", "error")
        return redirect(url_for("partner.dashboard"))
    apps = (
        Application.query.filter_by(vacancy_id=vacancy_id)
        .order_by(Application.match_score.desc())
        .all()
    )
    return render_template(
        "vacancies.html",
        vacancies=[vacancy],
        applications=apps,
        role="partner",
        detail_mode=True,
    )