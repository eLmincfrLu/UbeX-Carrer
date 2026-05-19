from app.database.connection import db


class PartnerOrganization(db.Model):
    __tablename__ = "partner_organizations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    industry = db.Column(db.String(80))
    website = db.Column(db.String(255))
    description = db.Column(db.Text)
    logo_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)