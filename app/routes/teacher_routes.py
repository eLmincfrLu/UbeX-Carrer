from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.database.connection import db
from app.models import Reference, User
from app.services.analytics_service import AnalyticsService
from app.utils.security import role_required

teacher_bp = Blueprint("teacher", __name__, url_prefix="/teacher")


@teacher_bp.route("/dashboard")
@login_required
@role_required("teacher")
def dashboard():
    students = User.query.filter_by(role="student").limit(8).all()
    refs = Reference.query.filter_by(author_id=current_user.id).count()
    return render_template(
        "teacher_dashboard.html",
        students=students,
        reference_count=refs,
        stats=AnalyticsService.university_dashboard(),
    )


@teacher_bp.route("/references", methods=["GET", "POST"])
@login_required
@role_required("teacher")
def references():
    if request.method == "POST":
        student_id = int(request.form.get("student_id"))
        ref = Reference(
            student_id=student_id,
            author_id=current_user.id,
            content=request.form.get("content", ""),
            rating=int(request.form.get("rating") or 5),
        )
        db.session.add(ref)
        db.session.commit()
        flash("Reference submitted.", "success")
        return redirect(url_for("teacher.references"))
    students = User.query.filter_by(role="student").all()
    items = Reference.query.filter_by(author_id=current_user.id).all()
    return render_template("references.html", references=items, students=students, teacher_mode=True)