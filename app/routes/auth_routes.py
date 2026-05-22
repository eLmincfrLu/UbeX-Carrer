from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from app.services.auth_service import AuthService
from app.utils.security import post_login_route

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def index():
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user, err = AuthService.authenticate(
            request.form.get("email"),
            request.form.get("password"),
        )
        if err:
            flash(err, "error")
        else:
            login_user(user)
            return redirect(url_for(post_login_route(user)))
    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user, err = AuthService.register(
            email=request.form.get("email"),
            password=request.form.get("password"),
            full_name=request.form.get("full_name"),
            role=request.form.get("role"),
            university=request.form.get("university"),
            department=request.form.get("department"),
            gpa=request.form.get("gpa") or 0,
        )
        if err:
            flash(err, "error")
        else:
            login_user(user)
            if user.role == "student":
                flash("Upload your CV — AI will build your verified skill dashboard.", "success")
            return redirect(url_for(post_login_route(user)))
    return render_template("login.html", register_mode=True)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))