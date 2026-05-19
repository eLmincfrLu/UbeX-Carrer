from flask import Blueprint, render_template
from flask_login import login_required

from app.models import User
from app.services.analytics_service import AnalyticsService
from app.utils.security import role_required

university_bp = Blueprint("university", __name__, url_prefix="/university")


@university_bp.route("/dashboard")
@login_required
@role_required("university")
def dashboard():
    stats = AnalyticsService.university_dashboard()
    top_students = (
        User.query.filter_by(role="student")
        .order_by(User.gpa.desc())
        .limit(6)
        .all()
    )
    return render_template(
        "university_dashboard.html",
        stats=stats,
        top_students=top_students,
    )