from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.models import PartnerOrganization
from app.services.analytics_service import AnalyticsService
from app.utils.security import role_required

partner_bp = Blueprint("partner", __name__, url_prefix="/partner")


@partner_bp.route("/dashboard")
@login_required
@role_required("partner")
def dashboard():
    stats = AnalyticsService.partner_dashboard(current_user)
    return render_template("partner_dashboard.html", stats=stats)


@partner_bp.route("/partners")
@login_required
def partners_list():
    orgs = PartnerOrganization.query.filter_by(is_active=True).all()
    return render_template("partners.html", partners=orgs)